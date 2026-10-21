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
    fontSize: 72px
    fontWeight: 700
    lineHeight: 82.8px
    fontVariation: "'MONO' 0"
  social-preview-owner:
    fontFamily: Google Sans Code
    fontSize: 28px
    fontWeight: 500
    lineHeight: 28px
    fontVariation: "'MONO' 0"
  social-preview-body:
    fontFamily: Google Sans Code
    fontSize: 32px
    fontWeight: 400
    lineHeight: 44px
    fontVariation: "'MONO' 0"
rounded:
  terminal: 10px
spacing:
  terminal-padding: 20px
  terminal-title-bar: 34px
  terminal-min-width: 560px
  hairline: 1px
  social-preview-padding: 64px
  social-preview-gap: 64px
  social-preview-stack: 24px
  social-preview-icon: 384px
  profile-header-icon: 128px
  profile-member-header-icon: 64px
  profile-row-icon: 40px
  profile-member-row-icon: 24px
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
    padding: "{spacing.social-preview-padding}"
    size: "{spacing.social-preview-icon}"
  social-preview-gap:
    width: "{spacing.social-preview-gap}"
    height: "{spacing.social-preview-stack}"
  social-preview-owner:
    backgroundColor: "{colors.social-preview-background}"
    textColor: "{colors.ink}"
    typography: "{typography.social-preview-owner}"
  social-preview-about:
    backgroundColor: "{colors.social-preview-background}"
    textColor: "{colors.social-preview-muted}"
    typography: "{typography.social-preview-body}"
  profile-header:
    size: "{spacing.profile-header-icon}"
  profile-member-header:
    size: "{spacing.profile-member-header-icon}"
  profile-row:
    size: "{spacing.profile-row-icon}"
  profile-member-row:
    size: "{spacing.profile-member-row-icon}"
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
explain intent and cite token names instead of values. CI lints this file
with the official `@google/design.md` parser and rejects any error or warning.
`github-readme-design`'s toolchain renders terminal demos, social previews and
the organization profiles from these tokens through the same parser. Change a
token, then regenerate every output that reads it.

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

One family, Google Sans Code, carries every lettering role. Its `MONO` axis
switches between a monospaced and a proportional design and `wght` sets the
weight; each typography token selects both. Terminal sessions and code are set
monospaced so output keeps its column grid; titles, labels and body text are
set proportional, which reads more compactly at display sizes.

Rendered lettering, terminal sessions included, is converted to glyph outlines
from `.github/design/fonts/GoogleSansCode[MONO,wght].ttf`, so every reader sees
the same letterforms and widths whatever fonts they have installed. The font is
Google Sans Code v7.001 from the
[googlefonts/googlesans-code](https://github.com/googlefonts/googlesans-code)
release archive (SHA-256
`eebba2a438882396e8530cad6d6cb80182b0afb6e9e0ad07b7340359a53ba2e9`), licensed
under the SIL Open Font License 1.1 (`.github/design/fonts/OFL.txt`).

## Layout

A terminal window is never narrower than `terminal-min-width` and grows with
its widest line. Its maximum is the width of GitHub's README column, a
platform limit the renderer enforces: a session that does not fit is
shortened, never scaled down. The title bar is `terminal-title-bar` tall, the
session sits `terminal-padding` from every edge, and one empty line separates
commands.

### Social preview canvas

A social preview fills GitHub's 1280×640 canvas. The icon is a
`social-preview-icon` square set `social-preview-padding` from the left edge,
and the text column starts `social-preview-gap` after it. Owner, title and
About stack `social-preview-stack` apart, centered vertically. Text is never
cut: a long title shrinks, then breaks at a hyphen or slash, and the About
sentence wraps.

### Organization profile

The public profile (`profile/README.md`) and the member dashboard in the
private `.github-private` repository are rendered by `github-readme-design`'s
toolchain from `profile/catalog.json`. The umbrella mark is a
`profile-header-icon` square on the public profile and a
`profile-member-header-icon` square on the dashboard; repository icons use
`profile-row-icon` and `profile-member-row-icon`.

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
| `social-preview` | Card ground, padding, icon square and repository title |
| `social-preview-gap` | Gap after the icon and between the text blocks |
| `social-preview-owner` | Owner label |
| `social-preview-about` | About sentence |
| `profile-header`, `profile-member-header` | Umbrella mark on the public profile and the member dashboard |
| `profile-row`, `profile-member-row` | Repository icons on the public profile and the member dashboard |

### Social preview

| Field | Source |
| --- | --- |
| `owner` | The organization login, `skill-cli` |
| `title` | The catalog entry's `title`, the repository's README title: `skill` for cli, `homebrew-tap` for the tap; the organization `name` for `.github` |
| `about` | The catalog entry's `about`, the repository's About sentence and README tagline, complete and unchanged |
| `icon` | The catalog entry's light-page icon: the skill mark in its dark appearance, which keeps its edge on the light canvas |

Each repository commits its card at
`.github/assets/social-preview/social-preview.png`, and its presentation check
compares it with a fresh render from this file at the pinned standard.

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
              "source": ".github/design/icons/skill-cli/layers/spirit-a.svg",
              "name": "Spirit A",
              "fill": {
                "automatic-gradient": "#B57AFF"
              }
            },
            {
              "source": ".github/design/icons/skill-cli/layers/spirit-b.svg",
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
              "source": ".github/design/icons/skill-cli/layers/bloom-outer.svg",
              "name": "Bloom outer",
              "fill": {
                "solid": "#FFFFFF"
              },
              "opacity": 0.32
            },
            {
              "source": ".github/design/icons/skill-cli/layers/bloom-inner.svg",
              "name": "Bloom inner",
              "fill": {
                "solid": "#FFFFFF"
              },
              "opacity": 0.65
            },
            {
              "source": ".github/design/icons/skill-cli/layers/bloom-core.svg",
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
              "source": ".github/design/icons/skill-cli/layers/shell.svg",
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
              "source": ".github/design/icons/skill-cli/layers/star.svg",
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
| Icon provenance and regeneration | `.github/design/icons/skill-cli/provenance.json` |
| Organization avatar, 1024 px | `profile/assets/avatar.png` |
| Profile mark on dark pages, 512 px | `profile/assets/icon.png` |
| Profile mark on light pages (Dark appearance), 512 px | `profile/assets/icon-dark.png` |
