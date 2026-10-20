# Versioning

The agents family [VERSIONING](https://github.com/agents-tools/.github/blob/aaddcb297cecb9e9273c807214e547d763cd85b4/VERSIONING.md)
applies to skill-cli. It owns version selection, dependency order, release
notes, signed immutable tags and publication. The
[maintenance declaration](MAINTENANCE.md#members) lists skill-cli's required
contexts and tag protection patterns.

| Repository | Version source | Release tag | Release owner/checklist |
| --- | --- | --- | --- |
| `skill-cli/.github` | Git tag | `vX.Y.Z` | This repository's README |
| `skill-cli/cli` | `BuildInfo.version` in `Sources/CLI/EntryPoint.swift` | `vX.Y.Z` | [skill release checklist](https://github.com/skill-cli/cli/blob/master/Documentation/Reference/Release.md) |
| `skill-cli/homebrew-tap` | Upstream CLI version in each formula | None of its own | [skill tap](https://github.com/skill-cli/homebrew-tap#readme); formula validation in the skill checklist |

## Legacy exceptions

The 2026-10-19 CLI audit verified these published annotated tags as unsigned.
They are legacy signature exceptions with the following existing identities:

| Tag | Tag object | Commit |
| --- | --- | --- |
| `v0.1.0` | `b540fb6ae8714eefd742071947f494ac7819a47c` | `ffd8897ba8978f0e27362fbe677912b6c93ac01c` |
| `v0.2.0` | `74e3f6a493f2cde580a348245d08e3d618d8f755` | `4722385279154b57653f2e7cccd143f182e848bd` |
| `v0.2.1` | `5d0d764e321c6fd8cc03df361214fed26e48990f` | `87917b99b857b1fc7a16ca3b02c74356709aeba9` |
