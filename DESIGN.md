---
version: alpha
name: skill-cli
description: Visual identity of the skill-cli organization and its repositories.
colors:
  primary: "#3B35D1"
  primary-dark: "#8F8AFF"
  ink: "#16143D"
  ink-dark: "#F1F0FF"
  terminal-surface: "#FBFBFE"
  terminal-surface-dark: "#0E0F24"
  terminal-bar: "#F0EFF8"
  terminal-bar-dark: "#16183A"
  terminal-border: "#DCDBEA"
  terminal-border-dark: "#2A2C55"
  terminal-output: "#3F3D5C"
  terminal-output-dark: "#C8C7E6"
  terminal-dim: "#67657F"
  terminal-dim-dark: "#8785AE"
  social-preview-background: "#F5F4FF"
  social-preview-muted: "#4F4C7A"
typography:
  terminal:
    fontFamily: Google Sans Code
    fontSize: 14px
    fontWeight: 400
    lineHeight: 21px
    fontVariation: "'MONO' 1"
  social-preview-title:
    fontFamily: Google Sans Code
    fontWeight: 700
    fontVariation: "'MONO' 0"
  social-preview-owner:
    fontFamily: Google Sans Code
    fontWeight: 500
    fontVariation: "'MONO' 0"
  social-preview-body:
    fontFamily: Google Sans Code
    fontWeight: 400
    fontVariation: "'MONO' 0"
rounded:
  terminal: 10px
spacing:
  terminal-padding: 20px
  terminal-title-bar: 34px
  terminal-min-width: 560px
  hairline: 1px
components:
  terminal:
    backgroundColor: "{colors.terminal-surface}"
    textColor: "{colors.terminal-output}"
    typography: "{typography.terminal}"
    rounded: "{rounded.terminal}"
    padding: "{spacing.terminal-padding}"
    width: "{spacing.terminal-min-width}"
  terminal-dark:
    backgroundColor: "{colors.terminal-surface-dark}"
    textColor: "{colors.terminal-output-dark}"
  terminal-frame:
    backgroundColor: "{colors.terminal-border}"
    size: "{spacing.hairline}"
  terminal-frame-dark:
    backgroundColor: "{colors.terminal-border-dark}"
  terminal-title-bar:
    backgroundColor: "{colors.terminal-bar}"
    textColor: "{colors.terminal-dim}"
    height: "{spacing.terminal-title-bar}"
  terminal-title-bar-dark:
    backgroundColor: "{colors.terminal-bar-dark}"
    textColor: "{colors.terminal-dim-dark}"
  terminal-prompt:
    backgroundColor: "{colors.terminal-surface}"
    textColor: "{colors.primary}"
  terminal-prompt-dark:
    backgroundColor: "{colors.terminal-surface-dark}"
    textColor: "{colors.primary-dark}"
  terminal-command:
    backgroundColor: "{colors.terminal-surface}"
    textColor: "{colors.ink}"
  terminal-command-dark:
    backgroundColor: "{colors.terminal-surface-dark}"
    textColor: "{colors.ink-dark}"
  social-preview:
    backgroundColor: "{colors.social-preview-background}"
    textColor: "{colors.ink}"
    typography: "{typography.social-preview-title}"
  social-preview-owner:
    backgroundColor: "{colors.social-preview-background}"
    textColor: "{colors.ink}"
    typography: "{typography.social-preview-owner}"
  social-preview-about:
    backgroundColor: "{colors.social-preview-background}"
    textColor: "{colors.social-preview-muted}"
    typography: "{typography.social-preview-body}"
---

# skill-cli Design

## Overview

The skill mark is the same ghost and shell on a light ground: `skill` is the
skills-only edition of `agents`. The same app icon is the organization avatar,
the mark on the organization profile and the mark of the `skill` CLI.

The icon is a Liquid Glass app icon built in Icon Composer. Its Icon Composer
document and its rendered assets are generated from the entry in
[Iconography](#iconography); change the entry or the layer artwork, then
regenerate.

This file follows Google's [DESIGN.md format](https://github.com/google-labs-code/design.md)
(`version: alpha`). Every token lives in the front matter; the sections below
explain intent and cite token names instead of values. Renderers read the
tokens through the official `@google/design.md` parser, and CI rejects any
lint error or warning. Change a token, then regenerate every output that
reads it.

## Colors

skill-cli chooses the agents family values for every token, so `skill` reads as
an edition of `agents`. `primary` is the family indigo. It marks what a reader
acts on, the terminal prompt; `primary-dark` lifts the same hue for dark
surfaces.

`ink` is a deep indigo for titles and commands, so text keeps the family's hue
instead of a neutral black; `ink-dark` is its counterpart on dark surfaces.

The `terminal-*` colors build a quiet window around the session: a near-white
surface, a slightly deeper title bar and a hairline border in light, and the
shell's night blue in dark. Output is one step softer than commands, so the
eye goes to what was typed; `terminal-dim` is reserved for the window title.

The `social-preview-*` colors are the card's pale lavender ground and the
muted tone of its About sentence.

App icon colors are defined by its entry in [Iconography](#iconography).

## Typography

One family, Google Sans Code, carries every lettering role through its two
axes: `MONO` 1 is the monospaced design for terminal sessions and code,
`MONO` 0 the proportional design for titles, labels and body text. `wght`
sets the weight of each role.

Rendered lettering, terminal sessions included, is converted to glyph outlines
from `Brand/Fonts/GoogleSansCode[MONO,wght].ttf`, so every reader sees the same
letterforms and widths whatever fonts they have installed. The font is
Google Sans Code v7.001 from the
[googlefonts/googlesans-code](https://github.com/googlefonts/googlesans-code)
release archive (SHA-256
`eebba2a438882396e8530cad6d6cb80182b0afb6e9e0ad07b7340359a53ba2e9`), licensed
under the SIL Open Font License 1.1 (`Brand/Fonts/OFL.txt`).

The social preview renderer reads static `MONO` 0 instances,
`Brand/Fonts/GoogleSansCodeProportional-{Regular,Medium,Bold}.ttf`;
`python3 Brand/Fonts/instantiate.py` reproduces them byte for byte.

## Layout

A terminal window is never narrower than `terminal-min-width` and grows with
its widest line. Its maximum is the width of GitHub's README column, a
platform limit the renderer enforces: a session that does not fit is
shortened, never scaled down. The title bar is `terminal-title-bar` tall, the
session sits `terminal-padding` from every edge, and one empty line separates
commands.

### Organization profile

The public profile (`profile/README.md`) and the member dashboard in the
private `.github-private` repository are rendered by `github-readme-design`'s
`render_profile.py` from `profile/catalog.json`. `Brand/Profile/recipe.json`
resolves these values and records this file's digest.

| Name | Value | Use |
| --- | --- | --- |
| `public_header_icon_size` | 128 px | Umbrella mark on the public profile |
| `member_header_icon_size` | 64 px | Umbrella mark on the member dashboard |
| `public_row_icon_size` | 40 px | Repository icons on the public profile |
| `member_row_icon_size` | 24 px | Repository icons on the member dashboard |
| `badge_style` | `flat` | CI and release badges on the member dashboard |

| Field | Source |
| --- | --- |
| Mark and row icons | Light mode uses the dark appearance and dark mode the default appearance, as in README headers |
| Row icon | The logo in that repository's README header; the tap uses the skill mark |
| Outcome | One plain-text sentence per repository in the catalog |

## Elevation & Depth

Presentation surfaces are flat: no shadows, gradients or blur. A terminal
window stands apart from the page by its hairline frame alone. Depth belongs
to the app icon, whose glass is defined in Iconography.

## Shapes

Terminal windows use the `terminal` corner radius, a soft corner that echoes
the app icon without imitating its continuous curve. The title bar carries no
window buttons: the session is the subject, not a desktop.

## Components

Each component is a presentation role. The light appearance carries the base
name; the dark appearance adds `-dark` and lists only the properties that
change, which renderers merge over the base.

| Component | Role |
| --- | --- |
| `terminal` | Window body, output text and the terminal typography |
| `terminal-frame` | Hairline outline and the separator under the title bar |
| `terminal-title-bar` | Title band and the session title |
| `terminal-prompt` | The `$ ` before each command |
| `terminal-command` | Command text |
| `social-preview` | Card ground and repository title |
| `social-preview-owner` | Owner label |
| `social-preview-about` | About sentence |

### Social preview

| Field | Source |
| --- | --- |
| `owner` | The organization login, `skill-cli` |
| `title` | The repository's README title: `skill` for cli, `homebrew-tap` for the tap |
| `about` | The repository's About sentence, which is also its README tagline, complete and unchanged |
| `icon` | The skill mark in its dark appearance, `profile/assets/icon-dark.png` (512 px PNG), which keeps its edge on the light canvas |

Cards are rendered by `github-readme-design`'s `render_social.py`, which embeds
raster icons byte for byte. Sources and exports live in `Brand/Social/`.

## Do's and Don'ts

- Do change a value only in the front matter, then regenerate every output
  that reads it.
- Do keep a terminal session short enough to fit GitHub's README column at
  actual size.
- Do select light and dark images with `<picture>` and
  `prefers-color-scheme`.
- Don't restate token values in prose; cite token names.
- Don't ship live text in rendered images; outline it.
- Don't add window buttons, shadows or gradients to terminal windows.
- Don't use `primary` for body text or large fills; it marks what a reader
  acts on.

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
