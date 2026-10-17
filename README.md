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

The catalog must list every public repository of the organization except this
one. The check compares it with the organization's repositories on GitHub.

## Change the icon

Edit the app icon entry in `DESIGN.md` or the artwork in `Brand/Icon/`, then
regenerate the Icon Composer document and the rendered avatar and profile mark
from the entry. Open `Brand/Exports/skill-cli/skill-cli.icon` in Icon Composer
to review the materials and appearances before committing.
