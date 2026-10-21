import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProfileAssetTests(unittest.TestCase):
    def test_profile_assets_match_provenance(self):
        catalog = json.loads((ROOT / "profile/catalog.json").read_text())
        repository = catalog["organization"]["login"] + "/.github"
        copies = [
            copy
            for receipt in (ROOT / ".github/design/icons").glob("*/provenance.json")
            for copy in json.loads(receipt.read_text())["copies"]
            if copy["repository"] == repository
        ]
        actual = {path.relative_to(ROOT).as_posix()
                  for path in (ROOT / "profile/assets").rglob("*") if path.is_file()}
        self.assertTrue(actual)
        self.assertCountEqual([copy["path"] for copy in copies], actual)
        for copy in copies:
            with self.subTest(path=copy["path"]):
                digest = hashlib.sha256((ROOT / copy["path"]).read_bytes()).hexdigest()
                self.assertEqual(digest, copy["sha256"])


if __name__ == "__main__":
    unittest.main()
