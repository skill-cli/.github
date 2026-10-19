import contextlib
import copy
from http.client import IncompleteRead
import importlib.machinery
import importlib.util
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import traceback
import unittest
from unittest import mock
from urllib.error import URLError


# Keep test imports from creating unignored bytecode beside repository sources.
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def load_script(name, filename):
    loader = importlib.machinery.SourceFileLoader(name, str(ROOT / "Scripts" / filename))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


renderer = load_script("render_profile", "render-profile.py")
checks = load_script("profile_checks", "check")


def committed_catalog():
    return json.loads((ROOT / "profile/catalog.json").read_text(encoding="utf-8"))


def repository(name, *, archived=False, private=False):
    return {"name": name, "archived": archived, "private": private}


class Response(io.BytesIO):
    def __init__(self, payload, link=""):
        super().__init__(json.dumps(payload).encode("utf-8"))
        self.headers = {"Link": link}

class SharedRendererTests(unittest.TestCase):
    def test_committed_profile_is_current(self):
        self.assertEqual(renderer.main(["--check"]), 0)

    def test_wrapper_uses_vendored_renderer_catalog_and_recipe(self):
        command = renderer.command(ROOT, check=True)
        self.assertEqual(Path(command[2]), ROOT / "Scripts/vendor/render_profile.py")
        self.assertEqual(command[3:], ["--catalog", str(ROOT / "profile/catalog.json"),
                                       "--spec", str(ROOT / "Brand/Profile/recipe.json"),
                                       "--output", str(ROOT / "profile/README.md"), "--check"])

    def test_vendored_files_match_the_receipt(self):
        rows = re.findall(r"^\| `([^`]+)` \| `([^`]+)` \| `([0-9a-f]{64})` \|$",
                          (ROOT / "Scripts/vendor/README.md").read_text(), re.M)
        self.assertEqual({name for name, _, _ in rows}, {"render_profile.py", "presentation.py", "LICENSE"})
        for name, _, digest in rows:
            with self.subTest(file=name):
                self.assertEqual(hashlib.sha256((ROOT / "Scripts/vendor" / name).read_bytes()).hexdigest(), digest)

    def test_catalog_is_validated_by_the_shared_schema(self):
        checks.validate_catalog(committed_catalog())
        for mutation in (lambda c: c["groups"][0]["repositories"][0].pop("icon"),
                         lambda c: c["groups"][0]["repositories"][0].update(summary="Old field."),
                         lambda c: c["quickstart"].update(commands=["echo ```"]),
                         lambda c: c.update(mark="javascript:alert(1)")):
            with self.subTest(mutation=mutation):
                catalog = copy.deepcopy(committed_catalog())
                mutation(catalog)
                with self.assertRaises(ValueError):
                    checks.validate_catalog(catalog)


class MembershipTests(unittest.TestCase):
    def setUp(self):
        self.catalog = committed_catalog()
        self.repositories = [
            repository(item["name"])
            for group in self.catalog["groups"] for item in group["repositories"]
        ]

    def test_matching_membership_excludes_archived_private_and_profile(self):
        checks.compare_membership(self.catalog, self.repositories + [
            repository(".github"), repository("old", archived=True), repository("secret", private=True),
        ])

    def test_missing_and_extra_are_reported_together(self):
        expected_extra = self.repositories[0]["name"]
        with self.assertRaisesRegex(
            ValueError, f"missing from catalog: alpha, zeta; extra in catalog: {expected_extra}"
        ):
            checks.compare_membership(self.catalog, self.repositories[1:] + [repository("zeta"), repository("alpha")])

    def test_archived_or_profile_in_catalog_is_extra(self):
        for name, archived in (("old", True), (".github", False)):
            with self.subTest(name=name):
                catalog = copy.deepcopy(self.catalog)
                catalog["groups"][0]["repositories"].append({"name": name, "outcome": "Example.", "icon": "https://example.test/icon.svg"})
                with self.assertRaisesRegex(ValueError, "extra in catalog: " + re.escape(name)):
                    checks.compare_membership(catalog, self.repositories + [repository(name, archived=archived)])

    def test_pagination_and_authorization_with_injected_responses(self):
        first = "https://api.github.com/orgs/skill-cli/repos?type=public&per_page=100"
        second = first + "&page=2"
        opener = mock.Mock(side_effect=[
            Response(self.repositories[:1], f'<{second}>; rel="last", <{second}>; rel="next"'),
            Response(self.repositories[1:] + [repository(".github")]),
        ])
        fetched = checks.fetch_repositories("skill-cli", "test-token", opener=opener)
        checks.compare_membership(self.catalog, fetched)
        self.assertEqual(len(fetched), len(self.repositories) + 1)
        self.assertEqual([call.args[0].full_url for call in opener.call_args_list], [first, second])
        for call in opener.call_args_list:
            self.assertEqual(call.args[0].get_header("Authorization"), "Bearer test-token")
            self.assertEqual(call.kwargs, {"timeout": 30})

    def test_no_authorization_header_without_token(self):
        opener = mock.Mock(return_value=Response([]))
        self.assertEqual(checks.fetch_repositories("skill-cli", opener=opener), [])
        self.assertIsNone(opener.call_args.args[0].get_header("Authorization"))

    def test_api_failure_is_explicit(self):
        opener = mock.Mock(side_effect=URLError("unreachable"))
        with self.assertRaisesRegex(ValueError, "^could not read GitHub API: request or response failed$"):
            checks.fetch_repositories("skill-cli", opener=opener)

    def test_interrupted_response_is_reported_as_api_failure(self):
        response = Response([])
        response.read = mock.Mock(side_effect=IncompleteRead(b"[", 12))
        with self.assertRaisesRegex(ValueError, "^could not read GitHub API: request or response failed$"):
            checks.fetch_repositories("skill-cli", opener=mock.Mock(return_value=response))

    def test_request_exception_traceback_does_not_echo_headers(self):
        token = "test-token-never-log"
        for failure in (
            ValueError(f"Invalid header value {('Bearer ' + token).encode()!r}"),
            URLError(f"Authorization: Bearer {token}"),
            IncompleteRead(token.encode(), 12),
        ):
            with self.subTest(failure=type(failure).__name__):
                opener = mock.Mock(side_effect=failure)
                try:
                    checks.fetch_repositories("skill-cli", token, opener=opener)
                except ValueError as error:
                    formatted = "".join(traceback.format_exception(type(error), error, error.__traceback__))
                    self.assertNotIn(token, formatted)
                    self.assertNotIn("Authorization", formatted)
                    self.assertIn("could not read GitHub API: request or response failed", formatted)
                else:
                    self.fail("Expected a safe request failure")

    def test_invalid_api_payloads_fail(self):
        for payload in ({"message": "error"}, [None], [{"name": "missing-flags"}]):
            with self.subTest(payload=payload):
                with self.assertRaisesRegex(ValueError, "invalid repository list"):
                    checks.fetch_repositories("skill-cli", opener=mock.Mock(return_value=Response(payload)))

    def test_pagination_rejects_external_endpoint_and_cycles(self):
        for url, message in (
            ("https://example.com/repos", "outside the repository endpoint"),
            ("https://api.github.com/orgs/skill-cli/repos?type=public&per_page=100", "repeated a page"),
        ):
            with self.subTest(url=url):
                opener = mock.Mock(return_value=Response([], f'<{url}>; rel="next"'))
                with self.assertRaisesRegex(ValueError, message):
                    checks.fetch_repositories("skill-cli", "test-token", opener=opener)
                self.assertEqual(opener.call_count, 1)


class CheckCommandTests(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.object(checks.family_settings, "check_online", return_value=[])
        self.settings = patcher.start()
        self.addCleanup(patcher.stop)

    def run_checks(self, arguments, *, api_error=None, render_status=0, validation_error=None):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), mock.patch.object(
            checks.subprocess, "run", return_value=subprocess.CompletedProcess([], render_status)
        ) as run, mock.patch.object(
            checks, "fetch_repositories", side_effect=api_error, return_value=[]
        ) as fetch, mock.patch.object(
            checks, "compare_membership"
        ) as compare, mock.patch.object(
            checks, "validate_catalog", side_effect=validation_error
        ), mock.patch.dict(checks.os.environ, {"GITHUB_TOKEN": "test-token"}):
            status = checks.main(arguments)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[0][-1], "--check")
        return status, output.getvalue().splitlines(), fetch, compare

    def test_success_prints_one_line_per_check_and_passes_token(self):
        status, lines, fetch, compare = self.run_checks([])
        self.assertEqual(status, 0)
        self.assertEqual(lines, ["PASS catalog validation", "PASS generated profile", "PASS family adoption declaration", "PASS repository membership"])
        fetch.assert_called_once_with("skill-cli", "test-token")
        compare.assert_called_once()

    def test_offline_skips_all_network_checks(self):
        status, lines, fetch, compare = self.run_checks(["--offline"])
        self.assertEqual(status, 0)
        self.assertEqual(lines, ["PASS catalog validation", "PASS generated profile", "PASS family adoption declaration", "SKIP repository membership (--offline)", "SKIP administrative settings (--offline)"])
        fetch.assert_not_called()
        compare.assert_not_called()
        self.settings.assert_not_called()

    def test_public_checks_membership_without_administrative_reads(self):
        status, lines, fetch, _ = self.run_checks(["--public"])
        self.assertEqual(status, 0)
        fetch.assert_called_once()
        self.settings.assert_not_called()
        self.assertEqual(lines[-1], "SKIP administrative settings (--public)")

    def test_settings_drift_and_unknown_have_distinct_statuses(self):
        for findings, expected in ((["PASS settings"], 0), (["DRIFT settings"], 1),
                                   (["DRIFT settings", "UNKNOWN settings"], 2)):
            with self.subTest(findings=findings):
                self.settings.return_value = findings
                status, lines, _, _ = self.run_checks([])
                self.assertEqual(status, expected)
                self.assertEqual(lines[-len(findings):], findings)

    def test_unavailable_standard_is_unknown(self):
        self.settings.side_effect = checks.family_settings.Unavailable("unreachable")
        status, lines, _, _ = self.run_checks([])
        self.assertEqual(status, 2)
        self.assertEqual(lines[-1], "UNKNOWN family standard: unreachable")

    def test_invalid_family_values_fail(self):
        self.settings.side_effect = ValueError("contexts differ")
        status, lines, _, _ = self.run_checks([])
        self.assertEqual(status, 1)
        self.assertEqual(lines[-1], "FAIL administrative settings: contexts differ")

    def test_render_failure_does_not_prevent_membership_check(self):
        status, lines, fetch, _ = self.run_checks([], render_status=1)
        self.assertEqual(status, 1)
        self.assertTrue(lines[1].startswith("FAIL generated profile"))
        fetch.assert_called_once()

    def test_offline_still_fails_catalog_and_render_checks(self):
        status, lines, fetch, _ = self.run_checks(
            ["--offline"], render_status=1, validation_error=ValueError("invalid catalog")
        )
        self.assertEqual(status, 1)
        self.assertEqual(len(lines), 5)
        self.assertEqual(lines[0], "FAIL catalog validation: invalid catalog")
        self.assertTrue(lines[1].startswith("FAIL generated profile"))
        fetch.assert_not_called()

    def test_api_failure_returns_failure_and_clear_message(self):
        status, lines, _, _ = self.run_checks([], api_error=ValueError("could not read GitHub API: request or response failed"))
        self.assertEqual(status, 1)
        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[3], "FAIL repository membership: could not read GitHub API: request or response failed")

    def run_with_opener(self, token, opener):
        fetch = checks.fetch_repositories
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error), mock.patch.object(
            checks.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)
        ), mock.patch.object(
            checks, "fetch_repositories",
            side_effect=lambda organization, token: fetch(organization, token, opener=opener),
        ), mock.patch.object(checks.os, "environ", {"GITHUB_TOKEN": token}):
            status = checks.main([])
        self.assertEqual(status, 1)
        self.assertEqual(error.getvalue(), "")
        lines = output.getvalue().splitlines()
        self.assertEqual(len(lines), 4)
        return lines[3]

    def test_malformed_token_is_rejected_without_a_request_or_disclosure(self):
        for character in (" ", "\t", "\n", "\r", "\x00", "\x1f", "\x7f", "\x85", "\u00a0", "\u200b"):
            with self.subTest(character=repr(character)):
                opener = mock.Mock()
                line = self.run_with_opener("test-token-never-log" + character, opener)
                self.assertEqual(line, "FAIL repository membership: GITHUB_TOKEN must not contain whitespace or control characters")
                self.assertNotIn("test-token-never-log", line)
                opener.assert_not_called()

    def test_request_and_response_errors_never_print_authorization_headers(self):
        token = "test-token-never-log"
        for stage in ("request", "response"):
            with self.subTest(stage=stage):
                failure = ValueError(f"Invalid header value {('Bearer ' + token).encode()!r}")
                if stage == "request":
                    opener = mock.Mock(side_effect=failure)
                else:
                    response = Response([])
                    response.read = mock.Mock(side_effect=failure)
                    opener = mock.Mock(return_value=response)
                line = self.run_with_opener(token, opener)
                self.assertEqual(line, "FAIL repository membership: could not read GitHub API: request or response failed")
                self.assertNotIn(token, line)
                opener.assert_called_once()


if __name__ == "__main__":
    unittest.main()
