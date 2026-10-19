"""Reuse the pinned agents family settings checker for this organization's members."""

from http.client import HTTPException
import json
from pathlib import Path
import re
import types
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
STANDARD = "agents-tools/.github"


class Unavailable(ValueError):
    """The pinned standard could not be read."""


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate declaration key: {key}")
        result[key] = value
    return result


def declaration_from(text):
    blocks = re.findall(r"<!-- settings-declaration -->\s*```json\n(.*?)\n```", text, re.S)
    if len(blocks) != 1:
        raise ValueError("expected one settings-declaration JSON block")
    return json.loads(blocks[0], object_pairs_hook=unique_object)


def load_declaration(catalog, root=ROOT):
    value = declaration_from((root / "MAINTENANCE.md").read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema") != 1:
        raise ValueError("unsupported adoption declaration schema")
    if set(value) != {"schema", "standard_revision", "repositories"}:
        raise ValueError("adoption declares only schema, standard_revision and repositories")
    revision = value.get("standard_revision")
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("standard_revision must be a full commit SHA")
    expected = {catalog["organization"]["login"] + "/.github"} | {
        catalog["organization"]["login"] + "/" + member["name"]
        for group in catalog["groups"] for member in group["repositories"]
    }
    members = value.get("repositories")
    if not isinstance(members, dict) or set(members) != expected:
        raise ValueError("declared members must match the catalog plus .github")
    for name, member in members.items():
        if not isinstance(member, dict) or set(member) != {"required_checks", "release_tag_patterns"}:
            raise ValueError(f"{name}: declare only required_checks and release_tag_patterns")
        for key, items in member.items():
            if not isinstance(items, list) or any(not isinstance(item, str) or not item for item in items):
                raise ValueError(f"{name}.{key} must be a list of nonempty strings")
            if len(set(items)) != len(items) or (key == "required_checks" and not items):
                raise ValueError(f"{name}.{key} must be unique; required_checks cannot be empty")
        if any(not pattern.startswith("refs/tags/") for pattern in member["release_tag_patterns"]):
            raise ValueError(f"{name}: tag patterns must include refs/tags/")
    caller = (root / ".github/workflows/source-policy.yml").read_text(encoding="utf-8")
    pins = re.findall(r"uses: agents-tools/\.github/\.github/workflows/policy\.yml@(\S+)", caller)
    if pins != [revision]:
        raise ValueError("policy caller must use the declared standard revision")
    return value


def read_standard(path, revision, *, opener=urlopen):
    url = f"https://raw.githubusercontent.com/{STANDARD}/{revision}/{path}"
    try:
        with opener(Request(url, method="GET"), timeout=30) as response:
            return response.read().decode("utf-8")
    except (HTTPException, OSError, ValueError):
        raise Unavailable(f"could not read pinned family standard: {path}") from None


def select_members(adoption, standard, checker):
    checker.validate_declaration(standard)
    selected = {}
    for name, values in adoption["repositories"].items():
        member = standard["repositories"].get(name)
        if member is None:
            raise ValueError(f"{name}: absent from the pinned family declaration")
        for key, expected in values.items():
            if sorted(expected) != sorted(member[key]):
                raise ValueError(f"{name}.{key}: differs from the pinned family declaration")
        selected[name] = member
    return {**standard, "repositories": selected}


def load_standard(revision, read=read_standard):
    source = read("Scripts/settings.py", revision)
    standard = declaration_from(read("MAINTENANCE.md", revision))
    # Execute the reviewed source at the same immutable pin as the policy caller.
    # The implementation and common settings remain owned by the family standard.
    checker = types.ModuleType("agents_family_settings")
    checker.__file__ = str(ROOT / "Scripts/family_settings.py")
    exec(compile(source, f"{STANDARD}@{revision}/Scripts/settings.py", "exec"), checker.__dict__)
    return checker, standard


def check_online(adoption, catalog):
    checker, standard = load_standard(adoption["standard_revision"])
    declaration = select_members(adoption, standard, checker)
    findings = checker.check_online(declaration)
    organization = catalog["organization"]["login"]
    try:
        findings += checker.compare(
            organization + ".organization", {"description": catalog["description"]},
            checker.api("orgs/" + organization),
        )
    except checker.Unavailable as error:
        findings.append(f"UNKNOWN {organization}.organization: {error}")
    return findings
