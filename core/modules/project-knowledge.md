# Project Knowledge

## Purpose

Preserve durable, evidence-backed project context during requirement interrogation without promoting provisional conversation into formal knowledge.

## Evidence boundary

- Derive formal Project Knowledge Base content only from approved or accepted evidence (`KB-EVIDENCE-001`).
- Read an existing Knowledge Base and its linked artifacts before asking for facts already supported there.
- Mark missing or conflicting evidence unresolved. Never invent a resolution.
- Treat the Knowledge Base as a current-context index, not a replacement for approved historical artifacts.

## Documented interrogation

- Compose with Requirement Interrogation; do not replace its approval gate or exactly one question per turn rule.
- Record discoveries in Draft Working Notes before approval (`KB-DRAFT-001`).
- Label every note `proposed`, `confirmed`, or `unresolved`.
- Do not treat `confirmed` notes as formal project knowledge before the upstream Requirement Decision Record is approved.
- Prohibit Specification authoring and implementation until requirement consensus is explicit.

## Synchronization

- Propose a Knowledge Base update whenever an approved or accepted upstream artifact changes durable project facts.
- Identify the upstream evidence and separate additions, modifications, and removals (`KB-SYNC-001`).
- Display the complete Requirement Decision Record and Knowledge Base Change Summary together.
- Request a single explicit approval for the displayed record and displayed changes.
- Apply only the changes included in that request. Materially changed or undisclosed edits require another approval.

## Capability downgrade

- A `conversation` adapter MUST use only user-supplied evidence and emit complete Markdown artifacts for user-managed persistence.
- It MUST NOT claim repository inspection, file persistence, or cross-session state.
- A `tools` adapter MAY persist Draft Working Notes and approved Knowledge Base changes under repository conventions.
