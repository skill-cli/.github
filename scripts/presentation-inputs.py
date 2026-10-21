#!/usr/bin/env python3
"""Resolve a caller's presentation inputs from the pinned organization catalog."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit


ASSETS = {
    "tool": ("logo", "terminal", "social-preview"),
    "library": ("logo", "social-preview"),
    "app": ("logo", "social-preview"),
    "distribution": ("social-preview",),
    "organization": ("social-preview",),
    "website": (),
}


def relative_path(value, label):
    path = PurePosixPath(value)
    if (not value or path.is_absolute() or ".." in path.parts or "\\" in value
            or any(not character.isprintable() for character in value)):
        raise ValueError(f"{label} must be a relative path without .. segments: {value!r}")
    return path


def within(root, relative, label):
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"{label} escapes its checkout")
    return path


def check_provenance(path, relative, repository, standard):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    for receipt in sorted((standard / ".github/design/icons").glob("*/provenance.json")):
        provenance = json.loads(receipt.read_text(encoding="utf-8"))
        for copy in provenance["copies"]:
            if (copy["repository"] == repository and copy["path"] == relative.as_posix()
                    and copy["sha256"] == digest):
                return
    raise ValueError(f"{repository}: {relative} has no matching SHA-256 provenance entry")


def resolve_icon(url, organization, repository, caller, standard, *, standard_only=False):
    try:
        if not isinstance(url, str) or any(character.isspace() or not character.isprintable() for character in url):
            raise ValueError("expected a raw GitHub URL")
        parsed = urlsplit(url)
        parts = parsed.path.split("/", 4)
        if (not url.startswith("https://raw.githubusercontent.com/")
                or parsed.scheme != "https" or parsed.netloc != "raw.githubusercontent.com"
                or "?" in url or "#" in url or len(parts) != 5
                or parts[1] != organization or parts[3] != "HEAD"):
            raise ValueError("expected the organization's raw GitHub HEAD URL")
        source = parts[2]
        if source == ".github":
            root = standard
        elif source == repository:
            if standard_only:
                raise ValueError("kind requires an icon from the standard's .github repository")
            root = caller
        else:
            raise ValueError("repository must be the caller or .github")
        relative = relative_path(unquote(parts[4], errors="strict"), "icon path")
        path = within(root, relative, "icon")
        if not path.is_file():
            raise ValueError("icon file is missing")
        resolved = str(path.resolve())
        if not resolved.isprintable():
            raise ValueError("resolved icon path contains control characters")
        if source != ".github":
            check_provenance(path, relative, f"{organization}/{repository}", standard)
        return resolved
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        raise ValueError(f"invalid icon URL {url!r}: {error}") from None


def resolve(catalog, repository, *, caller, standard, assets=".github/assets",
            executable_artifact="", executable_path=""):
    organization = catalog["organization"]["login"]
    owner, separator, name = repository.partition("/")
    if not separator or owner != organization:
        raise ValueError(f"caller owner must equal {organization!r}: {repository!r}")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise ValueError(f"invalid caller repository: {repository!r}")
    if name == ".github":
        kind, icon = "organization", catalog["mark"]
    else:
        entry = next((entry for group in catalog["groups"] for entry in group["repositories"]
                      if entry["name"] == name), None)
        if entry is None:
            raise ValueError(f"caller repository is absent from the catalog: {repository}")
        kind, icon = entry["kind"], entry["icon"]
        if kind not in ASSETS or kind == "organization":
            raise ValueError(f"unsupported kind {kind!r} for {repository}")
    asset_root = within(caller, relative_path(assets, "assets"), "assets")
    logo = asset_root / "logo"
    if "logo" not in ASSETS[kind] and (logo.exists() or logo.is_symlink()):
        raise ValueError(f"kind {kind} rejects logo directory: {logo}")
    if kind == "website":
        raise ValueError("kind website has no presentation assets")
    if kind == "tool":
        if not executable_artifact or not executable_path:
            raise ValueError("kind tool requires executable-artifact and executable-path")
    elif executable_artifact or executable_path:
        raise ValueError(f"kind {kind} rejects executable-artifact and executable-path")
    for asset in ASSETS[kind]:
        directory = within(caller, asset_root.relative_to(caller) / asset, asset)
        if not directory.is_dir():
            raise ValueError(f"kind {kind} requires asset directory: {directory}")
    if "terminal" not in ASSETS[kind] and (asset_root / "terminal").exists():
        raise ValueError(f"kind {kind} rejects terminal directory: {asset_root / 'terminal'}")
    variants = icon if isinstance(icon, dict) else {"light": icon}
    resolved_icons = {
        appearance: resolve_icon(url, organization, name, caller, standard,
                                 standard_only="logo" not in ASSETS[kind])
        for appearance, url in variants.items()
    }
    return {
        "kind": kind,
        "repository": name,
        "icon": resolved_icons["light"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--caller", type=Path, default=Path("../caller"))
    parser.add_argument("--assets", default=".github/assets")
    parser.add_argument("--executable-artifact", default="")
    parser.add_argument("--executable-path", default="")
    args = parser.parse_args(argv)
    standard = Path.cwd()
    try:
        catalog = json.loads((standard / "profile/catalog.json").read_text(encoding="utf-8"))
        resolved = resolve(catalog, args.repository, caller=args.caller.resolve(), standard=standard,
                           assets=args.assets, executable_artifact=args.executable_artifact,
                           executable_path=args.executable_path)
        for key, value in resolved.items():
            if not value.isprintable():
                raise ValueError(f"{key} output contains control characters")
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
            for key, value in resolved.items():
                output.write(f"{key}={value}\n")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Presentation inputs: " + " ".join(str(error).splitlines()), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
