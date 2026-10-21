# Maintenance

The agents family [MAINTENANCE](https://github.com/agents-tools/.github/blob/9b2955b052a2b8789e9c6e5f31c073a92163758a/MAINTENANCE.md)
applies to every skill-cli repository. It owns change flow, signing, settings,
review, dependencies and workflow adoption. The
[workflow integration guide](https://github.com/agents-tools/.github/blob/9b2955b052a2b8789e9c6e5f31c073a92163758a/docs/reference/workflow-integration.md)
owns the reusable workflow interfaces and activation checks.
[VERSIONING.md](VERSIONING.md) records skill-cli's release values;
[DESIGN.md](DESIGN.md) owns its identity.

## Members

The declaration selects skill-cli's members and their required contexts and
release tag protection patterns from the family standard. Shared settings and
repository metadata come from that standard; the organization description
comes from `profile/catalog.json`'s `description`. The private
`.github-private` member dashboard is declared like the public members; the
family checker reports its Free-plan ruleset limitation as an explicit `GAP`.

The reviewed automation revision is `9b2955b052a2b8789e9c6e5f31c073a92163758a`.
The policy caller and read-only settings checker use this same revision.

<!-- settings-declaration -->
```json
{
  "schema": 1,
  "standard_revision": "9b2955b052a2b8789e9c6e5f31c073a92163758a",
  "repositories": {
    "skill-cli/.github": {
      "required_checks": [
        "policy / policy",
        "check"
      ],
      "release_tag_patterns": [
        "refs/tags/v*"
      ]
    },
    "skill-cli/cli": {
      "required_checks": [
        "policy / policy",
        "validate / swift-package",
        "smoke",
        "presentation / presentation"
      ],
      "release_tag_patterns": [
        "refs/tags/v*"
      ]
    },
    "skill-cli/homebrew-tap": {
      "required_checks": [
        "policy / policy",
        "homebrew",
        "presentation / presentation"
      ],
      "release_tag_patterns": []
    },
    "skill-cli/.github-private": {
      "required_checks": [
        "policy / policy",
        "check / profile"
      ],
      "release_tag_patterns": []
    }
  }
}
```

## Legacy exceptions

The family's legacy signature exceptions cover these published skill-cli
commits from the 2026-10-19 member audits:

| Repository | SHA | Subject |
| --- | --- | --- |
| `skill-cli/cli` | `87917b99b857b1fc7a16ca3b02c74356709aeba9` | chore: prepare 0.2.1 release |
| `skill-cli/cli` | `0f6c05b5416d48bcbfb4ce0d069be55f77459eb9` | fix: diagnose shared installations for selected agents |
| `skill-cli/cli` | `5679b75681c9346f6f8243eb0626eee295bd8e37` | chore: merge origin/master before validating install diagnostics |
| `skill-cli/cli` | `9dd6a1ce6b4b6dc6f1da1f0f4aadfaa64de81d12` | fix: stop doctor false positives and allow removing records with missing files |
| `skill-cli/cli` | `4722385279154b57653f2e7cccd143f182e848bd` | chore: prepare 0.2.0 release |
| `skill-cli/cli` | `6588d9b983f349d2cc035969dc48632c91e40bc4` | feat: add editable local skill installs and doctor diagnostics |
| `skill-cli/cli` | `ffd8897ba8978f0e27362fbe677912b6c93ac01c` | chore: initial commit |
| `skill-cli/homebrew-tap` | `16aaf2d3e978a76a16599af003e7e2fde1e38299` | chore: update skill-cli formula to 0.2.1 |
| `skill-cli/homebrew-tap` | `47854d4b80779a55a6bfc3b2dbd25689dead7d75` | chore: update skill-cli formula to 0.2.0 |
| `skill-cli/homebrew-tap` | `8a00824ec671adea64087bfa9132289a7f6b1449` | chore: initial commit |

Legacy release tag exceptions are listed in [VERSIONING.md](VERSIONING.md#legacy-exceptions).

## Advisory review

**Deferred: Codex code review.** skill-cli organization connection, repository
selection and automatic review verification remain deferred under the
[family advisory-review declaration](https://github.com/agents-tools/.github/blob/9b2955b052a2b8789e9c6e5f31c073a92163758a/MAINTENANCE.md#advisory-review).
Existing review receipts in `skill-cli/cli` do not establish organization-wide
activation.
