# skill-cli Design

## Overview

The skill-cli mark pairs a command prompt with a spark: one command gives an
agent a new skill. The same app icon is the organization avatar, the mark on
the organization profile and the mark of the `skill` CLI.

The icon is a Liquid Glass app icon built in Icon Composer. Its Icon Composer
document and its rendered assets are generated from the entry below; change the
entry or the layer artwork, then regenerate.

## Colors

| Token | Value | Use |
| --- | --- | --- |
| `background` | `#0E7C74` | Icon background; Icon Composer derives its gradient from it |
| `prompt` | `#F2FBFA` | Prompt chevron |
| `spark` | `#FFD23F` | Spark |

## Iconography

The prompt and the spark are separate glass groups so their depth and
highlights stay distinct. The prompt is opaque so it keeps its shape in the
dark, clear and tinted appearances.

```json
{
  "app_icons": {
    "skill-cli": {
      "background": "#0E7C74",
      "gradient": true,
      "groups": [
        {
          "name": "Prompt",
          "layers": [{"source": "Brand/Icon/prompt.svg", "name": "Prompt"}],
          "shadow": {"kind": "neutral", "opacity": 0.5}
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
