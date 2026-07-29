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

## v2 first use migration

On v2 first use under Core v3 (`MIGRATE-V2-001`):

For this migration, propose an initial Project Knowledge Base only from approved evidence.

1. Inspect only user-supplied or host-accessible approved v2 artifacts.
2. Propose an initial Project Knowledge Base derived from that evidence.
3. Display its additions, modifications, and removals; an initial proposal will normally contain additions only.
4. Request explicit approval before creating or treating the Knowledge Base as active.
5. Mark missing, unsupported, or conflicting facts unresolved.

Migration MUST NOT rewrite, relabel, or overwrite any approved v2 Requirement Decision Record, Specification, Ticket Plan, Implementation Evidence, or Review Report. Rejection or failure leaves every v2 artifact unchanged and continues without an active v3 Knowledge Base.
