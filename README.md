# skill-cli/.github

Organization profile, brand and shared standards for
[skill-cli](https://github.com/skill-cli).

## Contents

| Path | Contents |
| --- | --- |
| `profile/catalog.json` | Promise, links, quick start and repository groups of the organization profile |
| `profile/README.md` | Organization profile, generated from the catalog |
| `profile/assets/` | Organization avatar and profile mark |
| `DESIGN.md` | Colors and the app icon entry |
| `Brand/Icon/` | Icon layer artwork |
| `Brand/Exports/skill-cli/` | Icon Composer document generated from the app icon entry |
| `Scripts/` | Profile generator and repository checks |

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
