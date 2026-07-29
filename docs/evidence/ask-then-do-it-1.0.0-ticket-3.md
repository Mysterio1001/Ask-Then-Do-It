# Ask Then Do It 1.0.0 Ticket 3 Evidence

Artifact type: Implementation Evidence

Artifact ID: `ask-then-do-it-1-0-ticket-3`

Workflow ID: `ask-then-do-it-1-0`

Ticket: 3 — Let a Generic user paste one renamed workflow and start immediately

Status: Completed

Date: 2026-07-29

## Red evidence

The new isolated Generic package test initially failed because release configuration still declared `generic/generic-prompts-1.0.0` instead of the approved `generic/ask-then-do-it-generic-1.0.0` directory.

## Green evidence

- Updated Generic directory and archive names in the release contract.
- Builder now copies canonical `LICENSE` and `THIRD_PARTY_NOTICES.md` into the Generic directory and ZIP root.
- Generic start guide now identifies the project, its independent status, and both legal files.
- Isolated package identity, manifest, legal byte-equivalence, ZIP-root, immediate-start, and guide test passed.
- Generic conformance validation passed against Core `1.0.0`.
- `tests.generic.test_generic_prompts` passed: `Ran 16 tests ... OK`.

## Boundary confirmation

Generic prompt modules remain English and provider-neutral. No unsupported filesystem, shell, installation, durable-memory, publication, or external capability was added.
