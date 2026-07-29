# Ask Then Do It 1.0.0 Ticket 4 Evidence

Artifact type: Implementation Evidence

Artifact ID: `ask-then-do-it-1-0-ticket-4`

Workflow ID: `ask-then-do-it-1-0`

Status: Completed

## Red

The first full run reported 18 failures caused by tests and `dist/` still asserting the former unpublished identity. After updating the tests, the sole remaining failure proved `dist/checksums.sha256` still named the old archives.

## Green

- `Ran 58 tests ... OK`.
- Sixteen official Skill validations passed.
- Canonical and packaged Plugin validations passed.
- Codex and Generic conformance passed against Core `1.0.0`.
- Two full builds produced byte-identical Codex and Generic archives.
- The managed `dist/` set was replaced through a recoverable backup-first workflow.
- Both canonical legal files are byte-identical in directories and ZIPs.

## Final archive hashes

```text
3f7b83d697cb5d431693d76cce79500622d1fd4db45828317b71c5e03e817721  codex/ask-then-do-it-1.0.0.zip
a65d8c0282ba2b3ec51b891ae26255aaef1031673bddf29ac8dfc41ef6b7f436  generic/ask-then-do-it-generic-1.0.0.zip
```

No installation, marketplace mutation, publication, upload, or external message occurred.
