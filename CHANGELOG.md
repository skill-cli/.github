# Changelog

## Unreleased

## 0.2.0

- Check social previews and organization profiles with the TypeScript
  toolchain. DESIGN front matter carries the social preview and profile
  tokens, the profile workflow validates the catalog, and this repository
  commits its own social preview.
- Choose presentation checks from each caller's catalog `kind`: tools check
  their terminal and social preview; libraries, apps, distributions and
  `.github` check their social preview; website callers fail. Regenerated
  files upload as `presentation.tar` in the `presentation` artifact, laid out
  like the asset root.
- Add the reusable `profile.yml` for the public profile and member dashboards.
- Compare every catalog `about` with the live repository description in the
  public and online checks.
- Remove the terminal presentation fixture from this repository's CI; a tool's
  run at the candidate commit proves the tool path before pins roll.
- Read the variable font for every rendered role and remove the static
  proportional instances and their instantiation script.
- Move presentation fonts and icon layers to `.github/design/`, record consumed
  icon exports in `provenance.json`, and generate Icon Composer documents in
  ignored scratch.
- Require logo directories for tools, libraries and apps, verify every
  caller-owned catalog icon against the pinned standard's SHA-256 receipts,
  and check organization profile assets against their provenance.
- Use lowercase `scripts/` and `tests/` paths for standard tooling.

Upgrading from 0.1.0:

- Tools, libraries and apps must commit a `logo/` directory under their asset
  root (normally `.github/assets/logo/`). Every caller-owned catalog icon,
  including both light and dark variants, must match the repository, path and
  SHA-256 in the pinned standard's `.github/design/icons/*/provenance.json`.
  Regenerate changed icons with the recorded skill and renderer, update the
  receipt and copy the verified output before advancing the caller's pin.
  Distributions, websites and the organization use standard icons and must
  have no `logo/` directory.
- Update standard tooling paths from `Scripts/` to `scripts/` and `Tests/` to
  `tests/`; use `.github/design/fonts/` for fonts and
  `.github/design/icons/<name>/layers/` for icon sources. Replace references to
  `Documentation/Reference/WorkflowIntegration.md` with
  `docs/reference/workflow-integration.md` when adopting the new family
  revision. Fixed-revision links retain the paths at that revision.
- Generate Icon Composer documents in ignored `.build/` scratch; consumed
  exports and `.github/design/icons/<name>/provenance.json` are the committed
  outputs. Font consumers read `GoogleSansCode[MONO,wght].ttf` and select axes
  from DESIGN typography tokens.

- Add `kind`, `title` and the verbatim `about` to each catalog repository, and
  `about` to `organization`.
- Commit each member's card at
  `.github/assets/social-preview/social-preview.png`, rendered as described in
  `README.md`. Tools keep `.github/assets/terminal/` and pass both executable
  inputs; other kinds call `presentation.yml` without them; websites do not
  call it.
- Member dashboards call `profile.yml` with `mode: member` from a job named
  `check`, drop `catalog` from `profile/member.json` and remove their vendored
  renderer. Their required context becomes `check / profile` after it appears
  on a real run.
- Replace `Scripts/render-profile.py`, the vendored renderers and recipes with
  the toolchain commands in `README.md`.

## 0.1.0

- Define skill-cli's visual tokens and app icon entry in Google's DESIGN.md
  format.
- Provide the reusable presentation workflow with caller context
  `presentation / presentation`.
- Generate the organization profile from its catalog with the shared renderer.
- Adopt the agents family maintenance and versioning standard by reference,
  with skill-cli's own organization values and pinned policy caller.
