# Agent Guide

Read `README.md` first.

- `profile/README.md` is generated. Change `profile/catalog.json`, run
  `python3 Scripts/render-profile.py`, and commit both.
- Keep catalog membership equal to the organization's public repositories
  except this one; `python3 Scripts/check` verifies it against GitHub.
- Repository summaries state what the repository does for a visitor, in one
  sentence, from that repository's current behavior.
- Brand values live in `DESIGN.md`. Change the entry or `Brand/Icon/`
  artwork, regenerate every output listed there, and commit sources and
  outputs together.
- Run `python3 Scripts/check` and `python3 -m unittest discover -s Tests`
  before handing off a change.
