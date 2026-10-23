# skill-cli/.github

Organization profile, brand and shared standards for
[skill-cli](https://github.com/skill-cli).

skill-cli follows the agents family [maintenance](MAINTENANCE.md) and
[versioning](VERSIONING.md) standards. GitHub uses the community files and
issue/pull-request templates here as defaults for organization repositories
that lack their own. `GOVERNANCE.md` is linked guidance. Members keep their own
workflow callers, CODEOWNERS, licenses and development notes.

## Contents

| Path | Contents |
| --- | --- |
| `profile/catalog.json` | Profile content, repository kinds, titles, About descriptions and icons |
| `profile/README.md` | Organization profile, generated locally from the catalog |
| `profile/assets/` | Organization avatar and profile mark |
| `.github/assets/social-preview/social-preview.png` | Organization repository social preview |
| `DESIGN.md` | Visual tokens in Google's DESIGN.md format and the app icon entry |
| `.github/design/icons/skill-cli/layers/` | Icon layer artwork |
| `.github/design/icons/*/provenance.json` | Verified icon outputs, consumed copies and SHA-256 digests |
| `.github/design/fonts/` | Variable font and its upstream license |
| `MAINTENANCE.md` | Family settings authority, legacy commits and advisory review |
| `VERSIONING.md` | Family versioning reference, member release values and legacy tags |
| `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md` | Organization community defaults |
| `GOVERNANCE.md` | Project scope and maintainer responsibilities |
| `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` | Default issue and pull-request intake |
| `.github/workflows/` | Thin callers for shared organization and source-policy checks |

## Organization checks

Reusable workflows and checkers live in
[agents-tools/github-workflows](https://github.com/agents-tools/github-workflows).
The [organization workflow](https://github.com/agents-tools/github-workflows#organization-checks)
reads skill-cli's settings, rulesets and required checks from
[agents-tools/.github MAINTENANCE](https://github.com/agents-tools/.github/blob/master/MAINTENANCE.md).
This repository supplies `profile/catalog.json` at the commit under test.
The caller pins the workflow implementation and declaration independently to
full commit SHAs.

CI runs public organization checks on branch pushes, pull requests and manual
dispatch. Public mode compares active public, non-fork repository membership
and About descriptions. The aggregate `check` job requires the organization
job to succeed. Source policy runs separately, including when a pull request
is edited. This repository's required contexts are `policy / policy` and
`check`.

Online mode additionally reads merge settings, token permissions,
vulnerability reporting and complete branch/tag rulesets. It needs an
organization token with Administration read access to the selected members;
see the shared workflow's input and secret contract. Checks only read settings.
Drift or declared enforcement gaps exit with 1; unknown observations exit with
2. Public checks do not establish settings conformance.

## Change the profile

Edit `profile/catalog.json`, then render and check `profile/README.md` locally
with the toolchain commands below. Commit the catalog and generated README
together. The catalog lists every public, non-archived, non-fork repository of
the organization except `.github`. Each entry declares its `kind`, `title`,
verbatim repository `about`, plain-text `outcome` and README header `icon`.
The organization also declares its own `.github` repository's `about`.
Marks and icons may select light and dark images.

The local renderer validates the catalog. The shared organization checker
compares membership and About descriptions with GitHub. The private
`.github-private` dashboard is rendered locally using this catalog and DESIGN
at an accepted commit, together with its own `profile/member.json` and an
explicit catalog revision.

## Local validation

Use the `github-readme-design`
[local rendering commands](https://github.com/showxu/skills/blob/master/skills/github-readme-design/references/renderers.md)
to prepare the toolchain at a reviewed commit in the ignored
`.build/presentation-toolchain` directory. Use the exact Node version from
its `.node-version` and its locked dependencies. From this worktree:

```sh
toolchain_dir="$PWD/.build/presentation-toolchain"
node "$toolchain_dir/src/cli.ts" design lint --design DESIGN.md
node "$toolchain_dir/src/cli.ts" profile render \
  --design DESIGN.md --catalog profile/catalog.json --out profile/README.md
node "$toolchain_dir/src/cli.ts" profile check \
  --design DESIGN.md --catalog profile/catalog.json --out profile/README.md
node "$toolchain_dir/src/cli.ts" social-preview check \
  --design DESIGN.md --fonts .github/design/fonts --catalog profile/catalog.json \
  --repository .github --icon profile/assets/icon-dark.png \
  --assets .github/assets/social-preview
actionlint
git diff --check origin/master
```

DESIGN lint requires zero errors and zero warnings. Review generated changes
before committing them. Profile and image rendering and byte comparisons run
locally; CI runs the shared organization and source-policy checks. Before a
release, complete these checks and follow the family release process in
[VERSIONING.md](VERSIONING.md).

## Change the design and regenerate assets

`DESIGN.md` owns the visual tokens and icon entries. Read it before visual or
asset work. After changing tokens or icon artwork, regenerate every affected
output locally and commit sources and outputs together. The same toolchain
lints DESIGN and renders profiles, social previews and terminal images.

To regenerate this repository's social preview:

```sh
node "$toolchain_dir/src/cli.ts" social-preview render \
  --design DESIGN.md --fonts .github/design/fonts --catalog profile/catalog.json \
  --repository .github --icon profile/assets/icon-dark.png \
  --out .github/assets/social-preview/social-preview.png
```

The icon is the catalog mark's light-page image. Members keep their previews
in their own repositories. Uploading the PNG in GitHub Settings remains a
separate manual step. Reuse the toolchain directory across runs and remove
download, dependency and review outputs when finished.

## Change the icon

The icon is generated from the app icon entry in `DESIGN.md` by `app_icons.py`
from the [apple-app-icon-design](https://github.com/showxu/skills/tree/master/skills/apple-app-icon-design)
skill. Native Liquid Glass rendering needs macOS with Xcode's Icon Composer
and `rsvg-convert`.

Edit the entry or the artwork in `.github/design/icons/skill-cli/layers/`, then
run with `APP_ICONS` set to that `app_icons.py`:

```sh
python3 "$APP_ICONS" DESIGN.md --name skill-cli --lint
rm -rf .build/icon .build/icon-document
python3 "$APP_ICONS" DESIGN.md --name skill-cli --style liquid-glass --out .build/icon
python3 "$APP_ICONS" DESIGN.md --name skill-cli --style liquid-glass --out .build/icon-document --document-only
```

Review `.build/icon/contact-sheet.png` and open the generated `.icon` in Icon
Composer. The document stays in ignored scratch. Copy the consumed outputs
to their owners:

| Generated | Consumed copy |
| --- | --- |
| `.build/icon/web/avatar-1024.png` | `profile/assets/avatar.png` |
| `.build/icon/web/icon-512.png` | `profile/assets/icon.png` |
| `.build/icon/web/dark/icon-512.png` | `profile/assets/icon-dark.png` |
| `.build/icon/web/dark/icon-512.png` | `.github/assets/logo/logo-light.png` in skill-cli/cli |
| `.build/icon/web/icon-512.png` | `.github/assets/logo/logo-dark.png` in skill-cli/cli |

Record each consumed copy in `.github/design/icons/skill-cli/provenance.json`:
its repository, path, generator output path and SHA-256, together with the
skill name, full skill commit, exact command, renderer version and verification
date. For a drift check, regenerate into `.build/icon` with the recorded skill
commit and renderer, then compare the output digests with the receipt:

```sh
python3 -B - <<'PYTHON'
import hashlib
import json
from pathlib import Path

receipt = json.loads(Path(".github/design/icons/skill-cli/provenance.json").read_text())
for copy in receipt["copies"]:
    output = Path(".build/icon") / copy["output"]
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    if digest != copy["sha256"]:
        raise SystemExit(f"Icon drift: {copy['repository']}: {copy['path']}")
PYTHON
```

When updating consumed icons, compare their SHA-256 digests with the receipt
and review both appearances locally.

The profile shows `icon-dark.png` (the Dark appearance) on light pages and
`icon.png` on dark pages, so the light icon keeps its edge on GitHub's light
theme; the entry's `web_dark` option produces the dark images.
