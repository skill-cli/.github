import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "Scripts/presentation-inputs.py"
spec = importlib.util.spec_from_file_location("presentation_inputs", SCRIPT)
inputs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inputs)


class InputTests(unittest.TestCase):
    def setUp(self):
        self.root = ROOT / ".build/test-presentation-inputs"
        self.caller = self.root / "caller"
        self.standard = self.root / "standard"
        self.assets = self.caller / ".github/assets"
        (self.assets / "social-preview").mkdir(parents=True)
        (self.standard / "profile/assets").mkdir(parents=True)
        self.icon = self.standard / "profile/assets/icon.png"
        self.icon.write_bytes(b"icon")
        self.url = "https://raw.githubusercontent.com/example/.github/HEAD/profile/assets/icon.png"
        self.entry = {"name": "product", "kind": "library", "icon": self.url}
        self.catalog = {"organization": {"login": "example"}, "mark": self.url,
                        "groups": [{"repositories": [self.entry]}]}
        self.addCleanup(shutil.rmtree, self.root)

    def resolve(self, repository="example/product", **options):
        return inputs.resolve(self.catalog, repository, caller=self.caller,
                              standard=self.standard, **options)

    def test_every_supported_kind(self):
        for kind in ("tool", "library", "app", "distribution"):
            with self.subTest(kind=kind):
                self.entry["kind"] = kind
                options = {}
                if kind == "tool":
                    (self.assets / "terminal").mkdir()
                    options = {"executable_artifact": "binary", "executable_path": "product"}
                result = self.resolve(**options)
                self.assertEqual(result, {"kind": kind, "repository": "product", "icon": str(self.icon)})
                if kind == "tool":
                    (self.assets / "terminal").rmdir()

    def test_organization_uses_mark_in_pinned_standard(self):
        result = self.resolve("example/.github")
        self.assertEqual(result, {"kind": "organization", "repository": ".github", "icon": str(self.icon)})

    def test_website_and_unknown_kind_fail(self):
        for kind, message in (("website", "kind website has no presentation assets"),
                              ("unknown", "unsupported kind"), ("organization", "unsupported kind")):
            with self.subTest(kind=kind):
                self.entry["kind"] = kind
                with self.assertRaisesRegex(ValueError, message):
                    self.resolve()

    def test_owner_is_exact_and_membership_is_required(self):
        for repository, message in (("Example/product", "caller owner"),
                                    ("other/product", "caller owner"),
                                    ("example/missing", "example/missing"),
                                    ("example/Product", "example/Product"),
                                    ("example/.github-private", "example/.github-private")):
            with self.subTest(repository=repository):
                with self.assertRaisesRegex(ValueError, message):
                    self.resolve(repository)

    def test_tool_requires_both_executable_inputs(self):
        self.entry["kind"] = "tool"
        (self.assets / "terminal").mkdir()
        for options in ({}, {"executable_artifact": "binary"}, {"executable_path": "product"}):
            with self.subTest(options=options):
                with self.assertRaisesRegex(ValueError, "requires executable-artifact and executable-path"):
                    self.resolve(**options)

    def test_non_tools_reject_either_executable_input(self):
        for kind in ("library", "app", "distribution", "organization"):
            for options in ({"executable_artifact": "binary"}, {"executable_path": "product"},
                            {"executable_artifact": "binary", "executable_path": "product"}):
                with self.subTest(kind=kind, options=options):
                    self.entry["kind"] = kind
                    repository = "example/.github" if kind == "organization" else "example/product"
                    with self.assertRaisesRegex(ValueError, "rejects executable"):
                        self.resolve(repository, **options)

    def test_missing_expected_directories_fail(self):
        for kind in ("tool", "library", "app", "distribution", "organization"):
            with self.subTest(kind=kind):
                self.entry["kind"] = kind
                repository = "example/.github" if kind == "organization" else "example/product"
                options = {"executable_artifact": "binary", "executable_path": "product"} if kind == "tool" else {}
                (self.assets / "social-preview").rmdir()
                with self.assertRaisesRegex(ValueError, "requires asset directory"):
                    self.resolve(repository, **options)
                (self.assets / "social-preview").mkdir()
                if kind == "tool":
                    with self.assertRaisesRegex(ValueError, "terminal"):
                        self.resolve(**options)

    def test_non_tools_reject_unexpected_terminal(self):
        (self.assets / "terminal").mkdir()
        for kind in ("library", "app", "distribution", "organization"):
            with self.subTest(kind=kind):
                self.entry["kind"] = kind
                with self.assertRaisesRegex(ValueError, "rejects terminal directory"):
                    self.resolve("example/.github" if kind == "organization" else "example/product")

    def test_custom_asset_root_and_path_boundaries(self):
        (self.caller / "custom/social-preview").mkdir(parents=True)
        self.assertEqual(self.resolve(assets="custom")["kind"], "library")
        for value in ("", "/absolute", "../standard", "nested/../../standard", "nested/../custom", "x\\y", "x\ny"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "assets must be a relative path"):
                    self.resolve(assets=value)
        (self.caller / "link").symlink_to(self.standard, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "escapes its checkout"):
            self.resolve(assets="link")

    def test_light_page_and_caller_icon_resolution(self):
        caller_icon = self.caller / ".github/assets/logo.png"
        caller_icon.write_bytes(b"caller icon")
        self.entry["icon"] = {"light": "https://raw.githubusercontent.com/example/product/HEAD/.github/assets/logo.png",
                              "dark": "https://example.test/unused.png"}
        self.assertEqual(self.resolve()["icon"], str(caller_icon))
        self.catalog["mark"] = {"light": self.url, "dark": "https://example.test/unused.png"}
        self.assertEqual(self.resolve("example/.github")["icon"], str(self.icon))

    def test_invalid_icon_urls_name_the_url(self):
        urls = [
            self.url.replace("https:", "http:"),
            self.url.replace("raw.githubusercontent.com", "github.com"),
            self.url.replace("raw.githubusercontent.com", "raw.githubusercontent.com:443"),
            self.url.replace("raw.githubusercontent.com", "user@raw.githubusercontent.com"),
            self.url.replace("/example/", "/other/"),
            self.url.replace("/.github/", "/other/"),
            self.url.replace("/HEAD/", "/master/"),
            self.url.replace("/HEAD/", "/" + "a" * 40 + "/"),
            self.url + "?download=1", self.url + "#icon", self.url + "?", self.url + "#",
            self.url.replace("/HEAD/", "/HEAD//"),
            self.url.replace("/profile/", "/../profile/"),
            self.url.replace("/profile/", "/%2e%2e/profile/"),
            self.url.replace("/profile/", "/%2fprofile/"),
            self.url.replace("/profile/", "/profile/../../profile/"),
            self.url.replace("icon.png", "missing.png"),
            " " + self.url, self.url + "\n", "profile/assets/icon.png",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.entry["icon"] = url
                with self.assertRaises(ValueError) as failure:
                    self.resolve()
                self.assertIn(repr(url), str(failure.exception))

    def test_icon_symlink_cannot_escape_its_checkout(self):
        self.icon.unlink()
        self.icon.symlink_to(self.caller / ".github/assets/other.png")
        with self.assertRaisesRegex(ValueError, "escapes its checkout") as failure:
            self.resolve()
        self.assertIn(self.url, str(failure.exception))

    def test_resolved_icon_path_cannot_inject_outputs(self):
        target = self.standard / "profile/assets/safe.png\nkind=tool"
        target.write_bytes(b"icon")
        self.icon.unlink()
        self.icon.symlink_to(target)
        with self.assertRaisesRegex(ValueError, "control characters") as failure:
            self.resolve()
        self.assertIn(self.url, str(failure.exception))

    def test_script_runs_from_standard_and_appends_github_outputs(self):
        (self.standard / "profile/catalog.json").write_text(json.dumps(self.catalog))
        output = self.root / "output"
        output.write_text("existing=value\n")
        command = [sys.executable, "-B", str(SCRIPT), "--repository", "example/product"]
        result = subprocess.run(command, cwd=self.standard, env={**os.environ, "GITHUB_OUTPUT": str(output)},
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output.read_text(), f"existing=value\nkind=library\nrepository=product\nicon={self.icon}\n")
        before = output.read_bytes()
        result = subprocess.run(command[:-1] + ["other/product"], cwd=self.standard,
                                env={**os.environ, "GITHUB_OUTPUT": str(output)}, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
