# Contributing

These guidelines apply to every skill-cli repository.

## Development

Read the affected repository's README for its build and test commands and
follow its repository-specific development instructions. Update tests and
documentation with behavior changes. The CLI keeps its own
[development notes](https://github.com/skill-cli/cli/blob/master/CONTRIBUTING.md).

Follow the shared [maintenance change flow](https://github.com/agents-tools/.github/blob/master/MAINTENANCE.md)
for signing, validation, review and merging, and the
[versioning standard](https://github.com/skill-cli/.github/blob/master/VERSIONING.md)
when preparing a release.

Organization catalog and design changes follow the
[local rendering and validation instructions](https://github.com/skill-cli/.github#local-validation).
Reusable workflows and repository checkers are maintained in
[agents-tools/github-workflows](https://github.com/agents-tools/github-workflows).

## Pull Requests

- Keep each pull request to one logical change.
- Explain the change and include validation commands and results.
- State which documentation was updated, or why no update is needed.
- Use a Conventional Commit title, such as `feat: add source validation` or
  `fix: handle missing configuration`. Pull requests are squash-merged, and
  the pull-request title becomes the commit subject.

Maintainers review changes before merging. Durable decisions belong in the
affected repository's documentation decision records. See the organization's
[governance](https://github.com/skill-cli/.github/blob/master/GOVERNANCE.md)
for project scope and maintainer responsibilities.
