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
| `profile/catalog.json` | Profile content, repository kinds, titles, About descriptions and icons |
| `.github/assets/social-preview/social-preview.png` | Organization repository social preview |
| `profile/README.md` | Organization profile, generated from the catalog |
| `profile/assets/` | Organization avatar and profile mark |
| `DESIGN.md` | Visual tokens in Google's DESIGN.md format and the app icon entry |
| `.github/design/icons/skill-cli/layers/` | Icon layer artwork |
| `.github/design/icons/*/provenance.json` | Verified icon outputs, consumed copies and SHA-256 digests |
| `.github/design/fonts/` | Variable font and its upstream license |
| `scripts/` | Presentation input resolver, family settings adapter and read-only repository checks |
| `tests/` | Workflow, input resolver, provenance, adoption and repository metadata tests |
| `MAINTENANCE.md` | Family adoption, member contexts, legacy commits and advisory review |
| `VERSIONING.md` | Family versioning reference, member release values and legacy tags |
| `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md` | Organization community defaults |
| `GOVERNANCE.md` | Project scope and maintainer responsibilities |
| `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` | Default issue and pull-request intake |
| `.github/workflows/` | Pinned family policy caller, reusable presentation and profile checks, and local validation |

## Validate the standard

```sh
python3 -m unittest discover -s tests
python3 scripts/check --offline
python3 scripts/check --public
python3 scripts/check
```

Offline checks read catalog membership fields and validate the member
declaration and policy pin. CI uses `--public` to compare public repository
membership and About descriptions with its read-only workflow token. The
profile workflow validates the catalog and generated profile. The default
online mode requires an authenticated `gh` session with read access to settings
for the declared skill-cli members.

The online check reads `scripts/settings.py` and `MAINTENANCE.md` directly from
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
[workflow integration guide](https://github.com/agents-tools/.github/blob/9b2955b052a2b8789e9c6e5f31c073a92163758a/docs/reference/workflow-integration.md)
when updating pins or activating protection. Update `standard_revision` and
the policy caller together. The CI and policy workflows run on branch pushes so adoption
can be validated before opening a pull request; their required contexts are
`policy / policy` and `check`.

## Presentation and profile workflows

Members pin `skill-cli/.github/.github/workflows/presentation.yml` by full
SHA, adding the `# vX.Y.Z` comment of a release; an unreleased commit has
none. Its inputs are `runner` (default `ubuntu-24.04`),
`executable-artifact` and `executable-path` (both default empty), and `assets`
(default `.github/assets`). The catalog kind determines the checked assets:

| Kind | Assets | Executable inputs |
| --- | --- | --- |
| `tool` | `logo`, `terminal`, `social-preview` | Both required |
| `library`, `app` | `logo`, `social-preview` | Both rejected |
| `distribution`, organization `.github` | `social-preview` | Both rejected |
| `website` | None; calling the workflow fails | Not applicable |

A tool uploads its built executable in a preceding job and passes that
artifact and the same runner OS to `presentation`. A library, app or
distribution calls without executable inputs. The workflow rejects an owner
other than the catalog organization, an unlisted repository, missing expected
asset directories and a terminal directory for a kind without terminal.
Tools, libraries and apps require a `logo/` directory under the asset root.
Distributions, websites and the organization use standard icons and reject a
`logo/` directory. Every caller-owned catalog icon, including both appearance
variants, must match a repository, path and SHA-256 entry in the standard's
`.github/design/icons/*/provenance.json`; failures name the file.
DESIGN, fonts and catalog come from this standard at `job.workflow_sha`.
Catalog icons use raw GitHub HEAD URLs, resolved to the
caller checkout or this standard's `.github` checkout; other hosts, owners,
repositories, refs, queries, fragments and escaping paths fail. The light-page
icon is the rendering input.

The terminal check records the real executable and compares its recording and
both SVGs; the social preview check compares the PNG. Failure artifact
`presentation` contains `presentation.tar`, preserving file modes and hidden
files. Extract it with `tar -xf presentation.tar -C .github/assets`, review and
commit the regenerated files. Upload is skipped when no files were generated.

`skill-cli/.github/.github/workflows/profile.yml` accepts `mode` (`public` by
default, or `member`), `member` (`profile/member.json`) and `output`
(`profile/README.md`). Paths are relative to the caller without `..` segments.
It validates mode and `job.workflow_sha` before checkout, uses the standard's
catalog and DESIGN at that SHA, and supplies that same revision only in member
mode. Failure artifact `profile` contains the regenerated Markdown file.
The member dashboard calls it from a job named `check`:

```yaml
jobs:
  check:
    uses: skill-cli/.github/.github/workflows/profile.yml@0000000000000000000000000000000000000000 # vX.Y.Z
    with:
      mode: member
```

Replace the zeros with the accepted standard commit, and the version comment
with its release version or nothing for an unreleased commit. Remove the `catalog` binding from `profile/member.json`; the workflow pin
selects the inputs. The resulting context is `check / profile`. Update the
member's maintenance declaration and live ruleset only after that context has
appeared on a real run under the family's activation gate.

Both workflows check out caller and standard without persisted credentials.
This repository calls both locally in CI with default inputs. Its required
contexts remain `policy / policy` and `check`. Keep member caller IDs
`presentation` and `check` for `presentation / presentation` and
`check / profile`. Before tag creation or pin rollout, a representative CLI
must run the candidate presentation workflow against its freshly built
executable on its build runner. The organization preview check does not prove
that tool path. See the family integration guide for caller examples and the
consumer real-run gate.

## Change the profile

Edit `profile/catalog.json`, then regenerate `profile/README.md` with the
pinned toolchain using the commands below. Commit the catalog and generated
README together. The catalog lists every public, non-archived repository of
the organization except `.github`. Each entry declares its `kind`, `title`,
verbatim repository `about`, plain-text `outcome` and README header `icon`.
The organization also declares its own `.github` repository's `about`.
Marks and icons may select light and dark images.

The profile workflow owns catalog validation and compares the generated
profile byte for byte. `scripts/check` reads membership fields and compares
membership and every `about` with GitHub in online and public modes; it lists
all description differences together. Offline mode skips these live checks.
The private `.github-private` dashboard uses the catalog and DESIGN at its
pinned profile workflow revision, with operational values in
`profile/member.json`.

## Change the design and regenerate assets

`DESIGN.md` owns the visual tokens in Google's DESIGN.md front matter and the
icon entries. Read it before visual or asset work. The same pinned TypeScript
toolchain lints DESIGN and renders profiles, social previews and terminals. Use
the package at `9e5d7268232b78f5fbef21ccfb9e3a079f2ef7e3` (`v0.1.0`) in the
ignored `.build/presentation-toolchain`, following its [local regeneration
contract](https://github.com/showxu/skills/blob/9e5d7268232b78f5fbef21ccfb9e3a079f2ef7e3/skills/github-readme-design/references/renderers.md#local-regeneration):

```sh
toolchain_commit='9e5d7268232b78f5fbef21ccfb9e3a079f2ef7e3' # v0.1.0
toolchain_dir="$PWD/.build/presentation-toolchain"
mkdir -p "$toolchain_dir"
curl -fsSL "https://api.github.com/repos/showxu/skills/tarball/$toolchain_commit" \
  -o "$toolchain_dir/source.tar.gz"
archive_root="$(tar -tzf "$toolchain_dir/source.tar.gz" | sed -n '1s,/.*,,p')"
tar -xzf "$toolchain_dir/source.tar.gz" -C "$toolchain_dir" --strip-components=4 \
  "$archive_root/skills/github-readme-design/scripts"
tar -xzf "$toolchain_dir/source.tar.gz" -C "$toolchain_dir" --strip-components=1 \
  "$archive_root/LICENSE"
node --version # Must match the copied .node-version; use that runtime below.
npm ci --ignore-scripts --omit=dev --prefix "$toolchain_dir"
node "$toolchain_dir/src/cli.ts" design lint --design DESIGN.md
node "$toolchain_dir/src/cli.ts" profile render \
  --design DESIGN.md --catalog profile/catalog.json --out profile/README.md
node "$toolchain_dir/src/cli.ts" profile check \
  --design DESIGN.md --catalog profile/catalog.json --out profile/README.md
node "$toolchain_dir/src/cli.ts" social-preview render \
  --design DESIGN.md --fonts .github/design/fonts --catalog profile/catalog.json \
  --repository .github --icon profile/assets/icon-dark.png \
  --out .github/assets/social-preview/social-preview.png
node "$toolchain_dir/src/cli.ts" social-preview check \
  --design DESIGN.md --fonts .github/design/fonts --catalog profile/catalog.json \
  --repository .github --icon profile/assets/icon-dark.png \
  --assets .github/assets/social-preview
```

DESIGN lint requires zero errors and zero warnings. The icon above is the
catalog mark's light-page image. Public profile commands omit member input and
catalog revision. These commands generate the organization's own assets;
members keep their previews in their own `.github/assets/social-preview/`.
Uploading the PNG in GitHub Settings remains a separate manual step.

Regenerate every output that reads changed DESIGN tokens or icon artwork,
review the outputs, and commit sources and outputs together. CI's local
`presentation` and `profile` calls check the organization's preview and public
profile. Reuse the package directory for a pin, replace its contents when
changing pins, and remove download and dependency outputs when finished.

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

Repository tests compare every `profile/assets/` file with its receipt;
member presentation checks verify each caller-owned catalog icon against the
receipts at the pinned standard.

The profile shows `icon-dark.png` (the Dark appearance) on light pages and
`icon.png` on dark pages, so the light icon keeps its edge on GitHub's light
theme; the entry's `web_dark` option produces the dark images.
