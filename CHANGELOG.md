# Changelog

## Unreleased

## 0.1.2

- **Breaking:** Organization and source-policy CI now use
  [agents-tools/github-workflows](https://github.com/agents-tools/github-workflows),
  with settings declared in the
  [family MAINTENANCE](https://github.com/agents-tools/.github/blob/master/MAINTENANCE.md).
  The local `scripts/check` and reusable `presentation.yml` and `profile.yml`
  workflows are removed. To upgrade, replace check-script invocations with the
  shared organization workflow, pin its implementation and declaration
  independently, and migrate presentation/profile callers to the local
  rendering and checking commands in [Local validation](README.md#local-validation).
  Render member dashboards with `profile/member.json` and an explicit accepted
  catalog revision, and update required checks from the family declaration.
- The profile links the [skill website](https://skill-cli.github.io/) as its
  documentation and lists `skill-cli.github.io` under Learn. The organization
  adopts the new member from the agents family standard at the commit that
  declares it.

## 0.1.1

- End the `.github` repository's About sentence with a period, like every
  member's; its catalog `about` and social preview match, and the agents
  family is adopted at its 0.1.1 release, which declares that description.

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
