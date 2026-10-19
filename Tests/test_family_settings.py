import copy
import io
import json
from pathlib import Path
import shutil
import sys
import unittest
from unittest import mock
from urllib.error import URLError


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Scripts"))
import family_settings as settings


def catalog():
    return json.loads((ROOT / "profile/catalog.json").read_text())


class DeclarationTests(unittest.TestCase):
    def setUp(self):
        self.root = ROOT / ".build/test-family-settings"
        self.root.mkdir(parents=True)
        self.addCleanup(shutil.rmtree, self.root)
        (self.root / ".github/workflows").mkdir(parents=True)
        shutil.copyfile(ROOT / ".github/workflows/source-policy.yml",
                        self.root / ".github/workflows/source-policy.yml")
        self.declaration = settings.load_declaration(catalog())

    def write_declaration(self):
        (self.root / "MAINTENANCE.md").write_text(
            "<!-- settings-declaration -->\n```json\n" +
            json.dumps(self.declaration) + "\n```\n"
        )

    def test_catalog_and_declared_members_must_agree(self):
        del self.declaration["repositories"]["skill-cli/homebrew-tap"]
        self.write_declaration()
        with self.assertRaisesRegex(ValueError, "match the catalog"):
            settings.load_declaration(catalog(), self.root)

    def test_floating_or_mismatched_pins_fail_offline(self):
        for revision in ("master", "a" * 40):
            with self.subTest(revision=revision):
                self.declaration["standard_revision"] = revision
                self.write_declaration()
                with self.assertRaises(ValueError):
                    settings.load_declaration(catalog(), self.root)

    def test_invalid_values_and_duplicate_rules_fail_offline(self):
        for key, value in (("required_checks", []), ("required_checks", ["check", "check"]),
                           ("required_checks", "check"), ("release_tag_patterns", ["v*"]),
                           ("defaults", {})):
            with self.subTest(key=key, value=value):
                self.declaration = settings.load_declaration(catalog())
                self.declaration["repositories"]["skill-cli/cli"][key] = value
                self.write_declaration()
                with self.assertRaises(ValueError):
                    settings.load_declaration(catalog(), self.root)

    def test_duplicate_json_keys_are_not_silently_overwritten(self):
        with self.assertRaisesRegex(ValueError, "duplicate declaration key"):
            settings.declaration_from('<!-- settings-declaration -->\n```json\n{"schema":1,"schema":2}\n```')


class SharedCheckerTests(unittest.TestCase):
    def setUp(self):
        self.adoption = settings.load_declaration(catalog())
        self.standard = {"schema": 1, "defaults": {"sentinel": "shared settings"}, "repositories": {
            **copy.deepcopy(self.adoption["repositories"]), "agents-tools/core": {"sentinel": "other member"},
        }}
        for name, member in self.standard["repositories"].items():
            member["description"] = name
        self.checker = mock.Mock()
        self.checker.Unavailable = settings.Unavailable

    def test_selection_reuses_defaults_and_member_metadata_without_other_organization(self):
        selected = settings.select_members(self.adoption, self.standard, self.checker)
        self.assertEqual(set(selected["repositories"]), set(self.adoption["repositories"]))
        self.assertIs(selected["defaults"], self.standard["defaults"])
        self.assertEqual(selected["repositories"]["skill-cli/cli"]["description"], "skill-cli/cli")
        self.assertIn("agents-tools/core", self.standard["repositories"])
        self.checker.validate_declaration.assert_called_once_with(self.standard)

    def test_absent_member_or_changed_context_and_tag_pattern_fail(self):
        for key in (None, "required_checks", "release_tag_patterns"):
            standard = copy.deepcopy(self.standard)
            if key is None:
                del standard["repositories"]["skill-cli/cli"]
            else:
                standard["repositories"]["skill-cli/cli"][key] = ["different"]
            with self.subTest(key=key), self.assertRaises(ValueError):
                settings.select_members(self.adoption, standard, self.checker)

    def test_online_preserves_shared_drift_and_compares_catalog_description(self):
        self.checker.check_online.return_value = ["DRIFT branch rules"]
        self.checker.compare.return_value = ["DRIFT organization description"]
        observed = {"description": "previous description"}
        self.checker.api.return_value = observed
        with mock.patch.object(settings, "load_standard", return_value=(self.checker, self.standard)) as load:
            findings = settings.check_online(self.adoption, catalog())
        load.assert_called_once_with(self.adoption["standard_revision"])
        self.assertEqual(findings, ["DRIFT branch rules", "DRIFT organization description"])
        selected = self.checker.check_online.call_args.args[0]
        self.assertEqual(set(selected["repositories"]), set(self.adoption["repositories"]))
        self.checker.api.assert_called_once_with("orgs/skill-cli")
        self.checker.compare.assert_called_once_with(
            "skill-cli.organization", {"description": catalog()["description"]}, observed
        )

    def test_unknown_organization_does_not_hide_member_drift(self):
        self.checker.check_online.return_value = ["DRIFT branch rules"]
        self.checker.api.side_effect = settings.Unavailable("HTTP 403")
        with mock.patch.object(settings, "load_standard", return_value=(self.checker, self.standard)):
            findings = settings.check_online(self.adoption, catalog())
        self.assertEqual(findings, ["DRIFT branch rules", "UNKNOWN skill-cli.organization: HTTP 403"])

    def test_standard_code_and_declaration_use_the_same_pin(self):
        read = mock.Mock(side_effect=["marker = 42\n", '<!-- settings-declaration -->\n```json\n{"schema":1}\n```'])
        checker, declaration = settings.load_standard(self.adoption["standard_revision"], read)
        self.assertEqual(checker.marker, 42)
        self.assertEqual(declaration, {"schema": 1})
        self.assertEqual(read.call_args_list, [
            mock.call("Scripts/settings.py", self.adoption["standard_revision"]),
            mock.call("MAINTENANCE.md", self.adoption["standard_revision"]),
        ])

    def test_public_standard_fetch_uses_get_without_credentials(self):
        opener = mock.Mock(return_value=io.BytesIO(b"source"))
        revision = self.adoption["standard_revision"]
        self.assertEqual(settings.read_standard("Scripts/settings.py", revision, opener=opener), "source")
        request = opener.call_args.args[0]
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.full_url,
                         f"https://raw.githubusercontent.com/agents-tools/.github/{revision}/Scripts/settings.py")
        self.assertIsNone(request.get_header("Authorization"))

    def test_download_failure_is_unknown_and_sanitized(self):
        with self.assertRaisesRegex(settings.Unavailable, "^could not read pinned family standard: Scripts/settings.py$"):
            settings.read_standard("Scripts/settings.py", self.adoption["standard_revision"],
                                   opener=mock.Mock(side_effect=URLError("private diagnostic")))


if __name__ == "__main__":
    unittest.main()
