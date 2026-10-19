#!/usr/bin/env python3
"""Render or check profile/README.md with the vendored shared profile renderer."""

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "Scripts/vendor/render_profile.py"


def command(root=ROOT, check=False):
    arguments = [
        sys.executable, "-B", str(RENDERER),
        "--catalog", str(root / "profile/catalog.json"),
        "--spec", str(root / "Brand/Profile/recipe.json"),
        "--output", str(root / "profile/README.md"),
    ]
    return arguments + ["--check"] if check else arguments


def main(argv=None, *, root=ROOT):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args(argv)
    return subprocess.run(command(root, args.check)).returncode


if __name__ == "__main__":
    sys.exit(main())
