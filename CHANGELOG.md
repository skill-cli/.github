# Changelog

## Unreleased

## 0.1.0

- Define skill-cli's visual tokens and app icon entry in Google's DESIGN.md
  format, with tokens for terminal demos, social previews and profiles. Fonts
  and icon layers live in `.github/design/`, with consumed icon copies recorded
  in `provenance.json`.
- Provide reusable presentation and profile workflows with caller contexts
  `presentation / presentation` and, for the member dashboard,
  `check / profile`. Presentation checks follow each caller's catalog `kind`;
  tools, libraries and apps commit a `logo/` directory whose catalog icons
  match the recorded SHA-256 receipts, and regenerated files upload as
  `presentation.tar` in the `presentation` artifact.
- Generate the organization profile and this repository's social preview from
  the catalog and DESIGN with the TypeScript presentation toolchain, and
  compare catalog About sentences with live repository descriptions.
- Adopt the agents family maintenance and versioning standard by reference,
  with skill-cli's own organization values and pinned policy caller.
