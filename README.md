# skill-cli/.github

Organization profile, brand and shared standards for
[skill-cli](https://github.com/skill-cli).

skill-cli adopts the agents family [maintenance](MAINTENANCE.md) and
[versioning](VERSIONING.md) standards by reference. GitHub uses the community
files and issue/pull-request templates here as defaults for organization
repositories that lack their own. `GOVERNANCE.md` is linked guidance, not an
inherited GitHub file. Members keep their own workflows, CODEOWNERS, licenses
and development notes, including the CLI's repository-specific instructions.

## Contents

| Path | Contents |
| --- | --- |
| `profile/catalog.json` | Promise, links, quick start and repository groups of the organization profile |
| `profile/README.md` | Organization profile, generated from the catalog |
| `profile/assets/` | Organization avatar and profile mark |
| `DESIGN.md` | Colors, presentation tokens and the app icon entry |
| `Brand/Icon/` | Icon layer artwork |
| `Brand/Exports/skill-cli/` | Icon Composer document generated from the app icon entry |
| [Brand/Social/](Brand/Social/README.md) | Repository social card recipes, outlined SVGs, PNGs and layout receipts |
| `Scripts/` | Profile generator and repository checks |
| `MAINTENANCE.md` | Family adoption, member contexts, legacy commits and advisory review |
| `VERSIONING.md` | Family versioning reference, member release values and legacy tags |
| `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md` | Organization community defaults |
| `GOVERNANCE.md` | Project scope and maintainer responsibilities |
| `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` | Default issue and pull-request intake |
| `.github/workflows/` | Pinned family policy caller and local validation |

## Validate the standard

```sh
python3 -m unittest discover -s Tests
python3 Scripts/check --offline
python3 Scripts/check --public
python3 Scripts/check
```

Offline checks validate the catalog, generated profile, member declaration and
policy pin. CI uses `--public` to add public repository membership with its
read-only workflow token. The default online mode requires an authenticated
`gh` session with read access to settings for all three skill-cli members.

The online check reads `Scripts/settings.py` and `MAINTENANCE.md` directly from
the reviewed family revision in the adoption declaration. It reuses that
unmodified checker, selects only skill-cli members, verifies their declared
contexts/tag patterns, and compares merge settings, token defaults, full
repository/inherited rulesets, private reporting, descriptions and topics.
It also compares the live organization description with the catalog. All
requests are GETs; no settings are applied. `DRIFT` prints expected and observed
values; inaccessible endpoints or fields remain `UNKNOWN`. Exit codes are 0
for conformance, 1 for drift/local failure and 2 for unknown observations.
Offline and public modes do not establish settings conformance.

Follow the family's
[workflow integration guide](https://github.com/agents-tools/.github/blob/6e3ca28f4b96f9de51bbe629048ba6ab71dc6e97/Documentation/Reference/WorkflowIntegration.md)
when updating pins or activating protection. Update `standard_revision` and
the policy caller together. Both workflows run on branch pushes so adoption
can be validated before opening a pull request; their contexts are
`policy / policy` and `check`.

## Change the profile

Edit `profile/catalog.json`, then regenerate the profile and run the checks:

```sh
python3 Scripts/render-profile.py
python3 Scripts/check
```

The catalog must list every public, non-archived repository of the
organization except `.github`. The check compares it with the organization's
repositories on GitHub.

The catalog's optional `mark.dark` names an existing repository file for dark
mode; when present, the mark uses a `<picture>` with `mark.path` as the light
fallback, retaining its width and `mark.alt` text. Both `<picture>` paths are
URL-encoded; omitting `mark.dark` keeps the existing `<img>` output.

## Change the icon

The icon is generated from the app icon entry in `DESIGN.md` by `app_icons.py`
from the [apple-app-icon-design](https://github.com/showxu/skills/tree/master/skills/apple-app-icon-design)
skill. Native Liquid Glass rendering needs macOS with Xcode's Icon Composer
and `rsvg-convert`.

Edit the entry or the artwork in `Brand/Icon/`, then run, with `APP_ICONS`
set to that `app_icons.py`:

```sh
python3 "$APP_ICONS" DESIGN.md --name skill-cli --lint
rm -rf .build/icon .build/icon-document
python3 "$APP_ICONS" DESIGN.md --name skill-cli --style liquid-glass --out .build/icon
python3 "$APP_ICONS" DESIGN.md --name skill-cli --style liquid-glass --out .build/icon-document --document-only
```

Review `.build/icon/contact-sheet.png` and open the generated `.icon` in Icon
Composer, then replace the committed outputs:

| Generated | Committed |
| --- | --- |
| `.build/icon-document/` | `Brand/Exports/skill-cli/` |
| `.build/icon/web/avatar-1024.png` | `profile/assets/avatar.png` |
| `.build/icon/web/icon-512.png` | `profile/assets/icon.png` |
| `.build/icon/web/dark/icon-512.png` | `profile/assets/icon-dark.png` |

`python3 "$APP_ICONS" DESIGN.md --name skill-cli --style liquid-glass --check Brand/Exports/skill-cli --document-only`
reports any drift between the entry and the committed document.

The profile shows `icon-dark.png` (the Dark appearance) on light pages and
`icon.png` on dark pages, so the light icon keeps its edge on GitHub's light
theme; the entry's `web_dark` option produces the dark images.
