# Security

Report security-sensitive issues privately, never in a public issue.

## Reporting

In the affected skill-cli repository, open **Security → Report a
vulnerability** to use GitHub private vulnerability reporting. The report URL
is `https://github.com/skill-cli/<repo>/security/advisories/new`; replace
`<repo>` with the affected repository's name.

Include:

- affected repository, version, command or code path
- reproduction steps and a minimal example
- expected impact
- any known mitigations

## Scope

Security review is especially important for:

- source downloads
- archive extraction
- filesystem writes and symlink handling
- installing agent skills
- lock and state files
