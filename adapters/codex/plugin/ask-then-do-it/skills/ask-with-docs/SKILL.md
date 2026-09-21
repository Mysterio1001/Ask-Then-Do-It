---
name: ask-with-docs
description: Interrogate software requirements one decision at a time while preserving durable, evidence-backed project knowledge. Use when the user explicitly asks for documented grilling, an existing system or Project Knowledge Base is involved, or requirement discussion introduces glossary, architecture, dependency, or decision context that future sessions should reuse. Keep provisional discoveries in Draft Working Notes and synchronize formal knowledge only with explicit approval.
---

# Grill With Docs

Turn ambiguous intent into approved requirements while building a reusable project-context index. Match user-facing questions and generated artifacts to the user's language when discoverable.

<!-- Maintainer note: Formal knowledge stays approval-bound so later agents can trust it without treating brainstorming as fact. -->

## Resolve the top-level mode before this stage

Direct selection of this Skill chooses this Full-workflow stage, not top-level `full`. Before stage behavior, require a current-operation mode proof from `$ask-then-do-it`; never persist or reuse mode.

- Missing proof: stop and delegate to `$ask-then-do-it`.
- Proven `lite`: stop this Full stage and route to the Lite workflow.
- Proven `full`: continue with this stage's prerequisites and gates.

## Use the portable artifact contract

Before creating or emitting a workflow artifact, read the [portable artifact contract](../ask-then-do-it/references/artifact-contract.md) completely. If it is missing or unreadable, stop before artifact creation and leave the handoff pending.

## Use approved evidence

Perform focused read-only discovery before asking a question:

- Read applicable repository instructions, `docs/project/knowledge-base.md` when present, and linked approved artifacts.
- Inspect related code, tests, data contracts, dependencies, and established terminology when tools are available.
- Distinguish repository evidence, user-supplied evidence, assumptions, and unresolved conflicts.
- Derive formal knowledge only from approved or accepted evidence (`KB-EVIDENCE-001`). Never invent missing context.

Do not ask for facts that available evidence already answers. Do not edit production code, install dependencies, or begin implementation during interrogation.

## Keep provisional notes

Maintain Draft Working Notes with `status` fixed to `Draft`; use the portable artifact contract for the shared envelope (including `core_version` `1.4.3`) and pending `approval`.

Label each entry:

- `proposed` for an unconfirmed possibility.
- `confirmed` for an answer explicitly confirmed during interrogation.
- `unresolved` for missing or conflicting evidence.

A confirmed working note must not become formal project knowledge before the Requirement Decision Record and disclosed knowledge changes are explicitly approved (`KB-DRAFT-001`). When persistence is useful, keep notes in the Decision Packet's Working Notes section; do not create a standalone copy.

For a Full operation needing durable documentation, use one Decision Packet per workflow ID at `docs/project/drafts/<workflow-id>/decision-packet.md` with Draft Working Notes, Requirement Decision Record, and any Knowledge Base Change Summary. Sections keep separate stable `artifact_id` and `status`; `summary_required: false` omits the summary. After approval, link the canonical Specification and canonical Knowledge Base at `docs/project/knowledge-base.md`; downstream stages use stable IDs instead of copying content. Lite MUST NOT create a Decision Packet.

## Ask exactly one question

For every turn:

1. Briefly state the decision already made when it affects the next branch.
2. Ask exactly one question.
3. Give one concrete recommended answer.
4. Explain its principal tradeoff.
5. Stop and wait.

Prioritize the unresolved decision with the greatest impact and uncertainty. Trace goals, users, scope, non-goals, behavior, failures, data, dependencies, security, privacy, operations, recovery, and acceptance criteria without using a fixed questionnaire.

## Prepare the formal artifacts

When high-impact decisions are confirmed, intentionally deferred with ownership, or proven irrelevant, prepare the Decision Packet and applicable sections as Draft.

The Requirement Decision Record section must include the shared envelope from the portable artifact contract and the confirmed problem, outcomes, users, behavior, boundaries, failures, contracts, constraints, acceptance criteria, assumptions, and deferrals.

The canonical Project Knowledge Base, when updated after approval, must use `docs/project/knowledge-base.md` and contain:

1. Glossary.
2. Architecture map.
3. Important decisions.
4. External dependencies.
5. Unresolved items.
6. Artifact links to Requirement Decision Records, Specifications, and Ticket Plans.

If a Knowledge Base already exists, propose a change rather than replacing unrelated content.

## Approve the record and knowledge together

Present a Knowledge Base Change Summary that identifies its upstream evidence and separates `additions`, `modifications`, and `removals` (`KB-SYNC-001`). Show the complete Requirement Decision Record and complete change summary before requesting approval.

Ask one single explicit approval question covering the displayed record and displayed changes. Approval applies only to that exact content. Silence, an unrelated response, approval of another artifact, or a hidden later edit does not count.

After approval:

1. Record the approval evidence.
2. Change the Requirement Decision Record to `Approved`.
3. Apply only the disclosed Knowledge Base changes when tools and permission allow persistence.
4. Hand off to `$write-spec`.

Do not begin Specification authoring or implementation from this skill. If the user disputes a material item, keep the artifacts Draft and resume one-question interrogation.

## Downgrade honestly

With only `conversation` capability, use only user-supplied artifacts. Emit one complete user-managed Decision Packet and state that the user owns persistence. Never claim repository inspection, file writes, durable state, commands, tests, or independent review without evidence.
