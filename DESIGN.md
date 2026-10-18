# skill-cli Design

## Overview

The skill-cli mark is a glint star with a small companion glint, the twinkle
anime uses for a flash of insight: each skill is an ability an agent gains.
It is the star at the center of the agents crest without the crest, so the
skills-only edition and the full tool read as one family. The same app icon
is the organization avatar, the mark on the organization profile and the mark
of the `skill` CLI.

The icon is a Liquid Glass app icon built in Icon Composer. Its Icon Composer
document and its rendered assets are generated from the entry below; change the
entry or the layer artwork, then regenerate.

## Colors

| Token | Value | Use |
| --- | --- | --- |
| `background` | `#007A6D` | Icon background; Icon Composer derives its gradient from it |
| `star` | `#FFFFFF` | Glint star |
| `glint` | `#FFE07A` | Companion glint |

## Iconography

The companion glint is translucent glass at the star's upper right, so the
icon keeps depth while the opaque star keeps its shape in the dark, clear and
tinted appearances.

```json
{
  "app_icons": {
    "skill-cli": {
      "background": "#007A6D",
      "gradient": true,
      "groups": [
        {
          "name": "Glint",
          "layers": [{"source": "Brand/Icon/glint.svg", "name": "Glint"}],
          "shadow": {"kind": "neutral", "opacity": 0.5},
          "translucency": {"enabled": true, "value": 0.2}
        },
        {
          "name": "Star",
          "layers": [{"source": "Brand/Icon/star.svg", "name": "Star"}],
          "shadow": {"kind": "neutral", "opacity": 0.5}
        }
      ],
      "styles": {
        "liquid-glass": {"design_generation": 27}
      }
    }
  }
}
```

| Output | Path |
| --- | --- |
| Icon Composer document | `Brand/Exports/skill-cli/skill-cli.icon` |
| Organization avatar, 1024 px | `profile/assets/avatar.png` |
| Profile mark, 512 px | `profile/assets/icon.png` |
