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
Colors and fonts come from [DESIGN.md](../../DESIGN.md); after changing it,
resolve the tokens and update each recipe's `design_sha256` before rendering.

Run from the repository root with `rsvg-convert` on PATH. Install the
`github-repo-steward` renderer dependencies in the ignored producer directory:

```sh
STEWARD="$HOME/.agents/skills/github-repo-steward/scripts"
python3 -m venv .build/social-cards/venv
.build/social-cards/venv/bin/python -m pip install -r "$STEWARD/requirements.txt" fonttools==4.67.0
```

Regenerate both cards and their layout receipts:

```sh
for repository in cli homebrew-tap; do
  .build/social-cards/venv/bin/python -B "$STEWARD/render_social.py" \
    --spec "Brand/Social/$repository/recipe.json" \
    --output "Brand/Social/$repository/card.svg" || exit
  rsvg-convert -w 1280 -h 640 "Brand/Social/$repository/card.svg" \
    -o "Brand/Social/$repository/card.png" || exit
done
```

Check the committed SVGs and layout receipts without writing:

```sh
for repository in cli homebrew-tap; do
  .build/social-cards/venv/bin/python -B "$STEWARD/render_social.py" \
    --spec "Brand/Social/$repository/recipe.json" \
    --output "Brand/Social/$repository/card.svg" --check || exit
done
```

Inspect each PNG at full size and 400 px wide before accepting it. Commit the
recipes, SVGs, PNGs and layout receipts together.
