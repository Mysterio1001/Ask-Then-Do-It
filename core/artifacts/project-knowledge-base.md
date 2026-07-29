# Project Knowledge Base Artifact

## Canonical location

A repository-backed workflow MUST maintain at most one canonical Project Knowledge Base at `docs/project/knowledge-base.md`.

## Required sections

1. Glossary.
2. Architecture map.
3. Important decisions.
4. External dependencies.
5. Unresolved items.
6. Artifact links to Requirement Decision Records, Specifications, and Ticket Plans.

## Evidence and updates

- Every formal fact MUST cite or link to approved or accepted evidence (`KB-EVIDENCE-001`).
- Unsupported or conflicting facts MUST remain in Unresolved items.
- Every proposed update MUST identify its upstream artifact and separate `additions`, `modifications`, and `removals` (`KB-SYNC-001`).
- Approval of an upstream artifact authorizes only the Knowledge Base changes displayed in the same approval request.
- Superseded current-state text MAY be removed, but its historical evidence MUST remain traceable through artifact links.

The Knowledge Base uses the shared artifact envelope and records the approval evidence for its current synchronized revision.
