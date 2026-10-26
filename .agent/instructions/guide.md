---
description: Route changes to skill-cli organization data, generated assets, design tokens and their checks.
---
# Agent Guide

Read `README.md` first.

- This repository owns organization data, generated assets and documents.
  Reusable workflows and checkers live in
  [agents-tools/github-workflows](https://github.com/agents-tools/github-workflows);
  local workflows are thin callers.
- `profile/README.md` and `.github/assets/social-preview/social-preview.png`
  are generated locally with the `github-readme-design` toolchain. Follow the
  [renderer commands](https://github.com/showxu/skills/blob/master/skills/github-readme-design/references/renderers.md)
  and `README.md`; commit inputs and outputs together.
- Keep catalog membership equal to the organization's public, non-archived,
  non-fork repositories except `.github`. Every catalog `about` must equal the
  live repository description, including `organization.about` for `.github`.
  The shared organization checker verifies membership and About text.
- Settings, rulesets and required checks are declared in
  [agents-tools/.github MAINTENANCE](https://github.com/agents-tools/.github/blob/master/MAINTENANCE.md).
  The organization caller pins that declaration separately from its workflow
  implementation and reads this repository's catalog at the commit under test.
  Required checks here are `policy / policy` and `check`.
- Repository summaries state what the repository does for a visitor, in one
  sentence, from that repository's current behavior.
- `DESIGN.md` owns the organization's visual tokens and icon entry. Read it
  before visual or asset work. Lint it with zero errors and zero warnings and
  regenerate every affected output after token or icon artwork changes.
  Record consumed icon copies and their SHA-256 digests in
  `.github/design/icons/*/provenance.json`; verify updated copies locally.
- Before handoff, run `actionlint`, toolchain DESIGN lint, profile check,
  social-preview check where an output exists, and
  `git diff --check origin/master`. Review generated output changes locally.
  Report live drift and unknowns; shared checks never change settings.
