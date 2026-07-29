# Ask Then Do It Release 1.0.0 Evidence

Artifact type: Implementation Evidence

Artifact ID: `ask-then-do-it-release-1.0.0-evidence`

Workflow ID: `ask-then-do-it-1-0`

Core version: `1.0.0`

Release version: `1.0.0`

Status: Completed

## Outcome

The first public local release is complete with exactly one Codex package and one Generic package under the `Ask Then Do It` identity. Both independently carry the project's MIT License and Matt Pocock attribution and MIT notice.

## Validation

- 58 automated tests passed.
- 16 Skill validations and two Plugin validations passed.
- Both adapters conform to Core `1.0.0`.
- Two complete builds were byte-identical.
- ZIP contents equal their generated directories.
- `dist/checksums.sha256` contains exactly two verified entries.

## Package layout

```text
dist/
├─ codex/
│  ├─ ask-then-do-it/
│  └─ ask-then-do-it-1.0.0.zip
├─ generic/
│  ├─ ask-then-do-it-generic-1.0.0/
│  └─ ask-then-do-it-generic-1.0.0.zip
└─ checksums.sha256
```

## Archive hashes

```text
3f7b83d697cb5d431693d76cce79500622d1fd4db45828317b71c5e03e817721  codex/ask-then-do-it-1.0.0.zip
a65d8c0282ba2b3ec51b891ae26255aaef1031673bddf29ac8dfc41ef6b7f436  generic/ask-then-do-it-generic-1.0.0.zip
```

## Review and architecture

- [Final Review](ask-then-do-it-1.0.0-final-review.md)
- [Release Architecture Diagnosis](ask-then-do-it-1.0.0-release-architecture-diagnosis.md)
- [Validation ledger](ask-then-do-it-release-1.0.0.json)

## Handoff

The local release is ready for a separate maintainer-controlled publication decision. No installation or publication occurred.
