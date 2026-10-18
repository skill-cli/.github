# skill-cli Design

## Overview

The skill-cli mark is a medal carrying a spark: each skill is an ability an
agent earns. It belongs to one family with the agents shield, sharing its glass
layering, so the skills-only edition and the full tool read as related. The
same app icon is the organization avatar, the mark on the organization profile
and the mark of the `skill` CLI.

The icon is a Liquid Glass app icon built in Icon Composer. Its Icon Composer
document and its rendered assets are generated from the entry below; change the
entry or the layer artwork, then regenerate.

## Colors

| Token | Value | Use |
| --- | --- | --- |
| `background` | `#007A6D` | Icon background; Icon Composer derives its gradient from it |
| `medal` | `#27B4A2` | Medal |
| `spark` | `#FFD54A` | Spark |

## Iconography

The medal is translucent glass behind the spark, so the overlap gives the icon
depth. The spark is opaque so it keeps its shape in the dark, clear and tinted
appearances. Each group's lightness differs from the background and from the
other group by at least the lint threshold.

```json
{
  "app_icons": {
    "skill-cli": {
      "background": "#007A6D",
      "gradient": true,
      "groups": [
        {
          "name": "Medal",
          "layers": [{"source": "Brand/Icon/medal.svg", "name": "Medal"}],
          "shadow": {"kind": "neutral", "opacity": 0.5},
          "translucency": {"enabled": true, "value": 0.5}
        },
        {
          "name": "Spark",
          "layers": [{"source": "Brand/Icon/spark.svg", "name": "Spark"}],
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
