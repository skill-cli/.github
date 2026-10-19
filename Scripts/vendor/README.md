# Profile renderer

These files are copied byte for byte from
[`showxu/skills`](https://github.com/showxu/skills) at commit
`346d15b5d50197fe41d24727c977679ee1e61e6f`. They are MIT-licensed, copyright
(c) 2026 showxu; the upstream notice is preserved in [LICENSE](LICENSE).

| Local file | Upstream path | SHA-256 |
| --- | --- | --- |
| `render_profile.py` | `skills/github-readme-design/scripts/render_profile.py` | `e1588ffc8a69cbe99041f2c733f62315e64315796c3ca353d5c2c917996b929e` |
| `presentation.py` | `skills/github-readme-design/scripts/presentation.py` | `5b3a8164c9eed21ac6d34c2c476f492339ff71c4c138aacb5efac56145506d00` |
| `LICENSE` | `LICENSE` | `16cce2b404888067eb74891e05f2281837fef58c1cc73d50025cc460ceff8bf1` |

[`Scripts/render-profile.py`](../render-profile.py) runs the renderer with
`profile/catalog.json` and `Brand/Profile/recipe.json`; `Scripts/check`
validates the catalog with it. The renderer and its input contract are owned by
`github-readme-design`. Update all three files together from one reviewed
upstream commit, never by local edits, then regenerate the profile.
