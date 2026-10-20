# Repository social cards

| Repository | Card |
| --- | --- |
| [skill-cli/cli](https://github.com/skill-cli/cli) | [cli/card.png](cli/card.png) |
| [skill-cli/homebrew-tap](https://github.com/skill-cli/homebrew-tap) | [homebrew-tap/card.png](homebrew-tap/card.png) |

Each directory holds `recipe.json`, `card.svg`, `card.png` and
`card.layout.json`. The accepted `card.png` supplies the exact bytes uploaded
as that repository's GitHub social preview.

Recipes use this repository's [dark icon](../../profile/assets/icon-dark.png)
and [OFL fonts](../Fonts/OFL.txt), with lettering outlined on a 1280×640 canvas.
Recipes copy the card colors from the front matter in [DESIGN.md](../../DESIGN.md).
After changing it, follow the [design procedure](../../README.md#change-the-design)
to lint it with zero errors and zero warnings, copy changed values into the
recipes and update every recipe's `design_sha256` to the SHA-256 of the final
file before rendering.

Run from the repository root with `rsvg-convert` on PATH. Install the
[github-readme-design](https://github.com/showxu/skills/tree/master/skills/github-readme-design)
renderer dependencies in the ignored producer directory:

```sh
README_DESIGN="$HOME/.agents/skills/github-readme-design/scripts"
python3 -m venv .build/social-cards/venv
.build/social-cards/venv/bin/python -m pip install -r "$README_DESIGN/requirements.txt" fonttools==4.67.0
```

Regenerate both cards and their layout receipts:

```sh
for repository in cli homebrew-tap; do
  .build/social-cards/venv/bin/python -B "$README_DESIGN/render_social.py" \
    --spec "Brand/Social/$repository/recipe.json" \
    --output "Brand/Social/$repository/card.svg" || exit
  rsvg-convert -w 1280 -h 640 "Brand/Social/$repository/card.svg" \
    -o "Brand/Social/$repository/card.png" || exit
done
```

Check the committed SVGs and layout receipts without rewriting them, then verify
that each PNG matches a fresh conversion:

```sh
for repository in cli homebrew-tap; do
  .build/social-cards/venv/bin/python -B "$README_DESIGN/render_social.py" \
    --spec "Brand/Social/$repository/recipe.json" \
    --output "Brand/Social/$repository/card.svg" --check || exit
  rsvg-convert -w 1280 -h 640 "Brand/Social/$repository/card.svg" \
    -o ".build/social-cards/$repository.png" || exit
  cmp "Brand/Social/$repository/card.png" ".build/social-cards/$repository.png" || exit
done
```

Inspect each PNG at full size and 400 px wide before accepting it. Commit the
recipes, SVGs, PNGs and layout receipts together. Remove the temporary PNGs and
environment in `.build/social-cards/` when finished.
