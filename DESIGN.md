# skill-cli Design

## Overview

The skill mark is the same ghost and shell on a light ground: `skill` is the
skills-only edition of `agents`. The same app icon is the organization avatar,
the mark on the organization profile and the mark of the `skill` CLI.

The icon is a Liquid Glass app icon built in Icon Composer. Its Icon Composer
document and its rendered assets are generated from the entry below; change the
entry or the layer artwork, then regenerate.

## Colors

| Token | Value | Use |
| --- | --- | --- |
| `background` | `#FFFFFF` | Icon background; Icon Composer derives its gradient from it |
| `shell` | `#1A1F5C` | Glass shell |
| `ghost` | `#FFFFFF` | Ghost star and its light |
| `spirit` | `#B57AFF`, `#FF7AD6` | Haze inside the shell |

## Presentation

These values drive README Quick look recordings and social cards for every
skill-cli repository. Renderer recipes copy them and record the digest of
this file; change a value here first, then regenerate.

### Typography

| Token | Value |
| --- | --- |
| `font-card-title` | Google Sans Code Proportional Bold, `Brand/Fonts/GoogleSansCodeProportional-Bold.ttf` |
| `font-card-body` | Google Sans Code Proportional Regular, `Brand/Fonts/GoogleSansCodeProportional-Regular.ttf` |
| `font-card-owner` | Google Sans Code Proportional Medium, `Brand/Fonts/GoogleSansCodeProportional-Medium.ttf` |
| `font-terminal` | `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` |

The card faces are static instances (`MONO=0`) of Google Sans Code v7.001
(`GoogleSansCode[MONO,wght].ttf` from the
[googlefonts/googlesans-code](https://github.com/googlefonts/googlesans-code)
release archive, SHA-256
`eebba2a438882396e8530cad6d6cb80182b0afb6e9e0ad07b7340359a53ba2e9`), licensed
under the SIL Open Font License 1.1 (`Brand/Fonts/OFL.txt`).
`python3 Brand/Fonts/instantiate.py` reproduces them byte for byte. Card
lettering is converted to outlines; terminal recordings keep live text in the
reader's monospace font.

### Social card

| Token | Value | Use |
| --- | --- | --- |
| `card-background` | `#F5F4FF` | Canvas |
| `card-ink` | `#16143D` | Owner label and title |
| `card-muted` | `#4F4C7A` | About sentence |

Cards show the skill mark in its dark appearance, which keeps its edge on the light canvas.

### Terminal

| Role | Light | Dark |
| --- | --- | --- |
| `surface` | `#FBFBFE` | `#0E0F24` |
| `bar` | `#F0EFF8` | `#16183A` |
| `border` | `#DCDBEA` | `#2A2C55` |
| `prompt` | `#3B35D1` | `#8F8AFF` |
| `command` | `#16143D` | `#F1F0FF` |
| `output` | `#3F3D5C` | `#C8C7E6` |
| `dim` | `#6F6D8B` | `#7C7AA3` |

These are the agents family values: the prompt carries the icon's indigo and
the dark surface is the shell's night blue. READMEs select the light or dark recording with `<picture>` and
`prefers-color-scheme`.

## Iconography

```json
{
  "app_icons": {
    "skill-cli": {
      "background": "#FFFFFF",
      "gradient": true,
      "groups": [
        {
          "name": "Spirit",
          "shadow": {
            "kind": "layer-color",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": true,
            "value": 0.4
          },
          "refractivity": {
            "enabled": true,
            "strength": 0.4,
            "depth": 0.16
          },
          "layers": [
            {
              "source": "Brand/Icon/spirit-a.svg",
              "name": "Spirit A",
              "fill": {
                "automatic-gradient": "#B57AFF"
              }
            },
            {
              "source": "Brand/Icon/spirit-b.svg",
              "name": "Spirit B",
              "fill": {
                "automatic-gradient": "#FF7AD6"
              },
              "opacity": 0.85
            }
          ]
        },
        {
          "name": "Bloom",
          "blend-mode": "plus-lighter",
          "specular": false,
          "shadow": {
            "kind": "none",
            "opacity": 0
          },
          "translucency": {
            "enabled": false,
            "value": 0
          },
          "layers": [
            {
              "source": "Brand/Icon/bloom-outer.svg",
              "name": "Bloom outer",
              "fill": {
                "solid": "#FFFFFF"
              },
              "opacity": 0.32
            },
            {
              "source": "Brand/Icon/bloom-inner.svg",
              "name": "Bloom inner",
              "fill": {
                "solid": "#FFFFFF"
              },
              "opacity": 0.65
            },
            {
              "source": "Brand/Icon/bloom-core.svg",
              "name": "Bloom core",
              "fill": {
                "solid": "#FFFFFF"
              },
              "opacity": 0.75
            }
          ]
        },
        {
          "name": "Shell",
          "shadow": {
            "kind": "layer-color",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": true,
            "value": 0.55
          },
          "blur-material": 0.55,
          "refractivity": {
            "enabled": true,
            "strength": 0.8,
            "depth": 0.14
          },
          "layers": [
            {
              "source": "Brand/Icon/shell.svg",
              "name": "Shell",
              "fill": {
                "automatic-gradient": "#1A1F5C"
              }
            }
          ]
        },
        {
          "name": "Ghost",
          "blend-mode": "plus-lighter",
          "shadow": {
            "kind": "layer-color",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": false,
            "value": 0
          },
          "refractivity": {
            "enabled": true,
            "strength": 0.2,
            "depth": 0.1
          },
          "layers": [
            {
              "source": "Brand/Icon/star.svg",
              "name": "Ghost",
              "fill": {
                "automatic-gradient": "#FFFFFF"
              },
              "fill-specializations": {
                "dark": {
                  "solid": "#FFFFFF"
                }
              }
            }
          ]
        }
      ],
      "styles": {
        "liquid-glass": {
          "design_generation": 27
        }
      },
      "web_dark": true
    }
  }
}
```

| Output | Path |
| --- | --- |
| Icon Composer document | `Brand/Exports/skill-cli/skill-cli.icon` |
| Organization avatar, 1024 px | `profile/assets/avatar.png` |
| Profile mark on dark pages, 512 px | `profile/assets/icon.png` |
| Profile mark on light pages (Dark appearance), 512 px | `profile/assets/icon-dark.png` |
