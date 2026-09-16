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

## Full Decision Packet producer

- A Full workflow that needs durable requirement documentation MUST use one Decision Packet per `workflow_id` at `docs/project/drafts/<workflow-id>/decision-packet.md`.
- The packet MUST contain clearly labeled Draft Working Notes, Requirement Decision Record, and (when applicable) Knowledge Base Change Summary sections. Each section keeps a separate stable `artifact_id` and `status` and the common artifact envelope.
- The packet remains Draft until requirement consensus and any disclosed Knowledge Base changes are explicitly approved. Approval of one section MUST NOT silently approve another section or authorize implementation.
- After approval, the packet MUST link to the canonical Specification and the canonical Knowledge Base at `docs/project/knowledge-base.md`. Downstream artifacts reference stable IDs instead of copying substantive content.
- `summary_required: true` requires one Knowledge Base Change Summary with additions, modifications, and removals. `summary_required: false` records that no durable project fact changed and MUST NOT create an empty summary.

Lite operations retain their existing Change Brief lifecycle. Lite MUST NOT create a Decision Packet, Draft Working Notes, Requirement Decision Record, or Knowledge Base Change Summary merely because this Full-documentation policy exists.

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
