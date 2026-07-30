---
name: ask-with-docs
description: Interrogate software requirements one decision at a time while preserving durable, evidence-backed project knowledge. Use when the user explicitly asks for documented grilling, an existing system or Project Knowledge Base is involved, or requirement discussion introduces glossary, architecture, dependency, or decision context that future sessions should reuse. Keep provisional discoveries in Draft Working Notes and synchronize formal knowledge only with explicit approval.
---

# Grill With Docs

Turn ambiguous intent into approved requirements while building a reusable project-context index. Match user-facing questions and generated artifacts to the user's language when discoverable.

<!-- Maintainer note: Formal knowledge stays approval-bound so later agents can trust it without treating brainstorming as fact. -->

## Use approved evidence

Perform focused read-only discovery before asking a question:

- Read applicable repository instructions, `docs/project/knowledge-base.md` when present, and linked approved artifacts.
- Inspect related code, tests, data contracts, dependencies, and established terminology when tools are available.
- Distinguish repository evidence, user-supplied evidence, assumptions, and unresolved conflicts.
- Derive formal knowledge only from approved or accepted evidence (`KB-EVIDENCE-001`). Never invent missing context.

Do not ask for facts that available evidence already answers. Do not edit production code, install dependencies, or begin implementation during interrogation.

## Keep provisional notes

Maintain Draft Working Notes with `status` fixed to `Draft`. Include `artifact_type`, stable `artifact_id`, shared `workflow_id`, `core_version` `1.0.1`, `status`, `inputs`, `assumptions`, `deferred`, `handoff`, and pending `approval`.

Label each entry:

- `proposed` for an unconfirmed possibility.
- `confirmed` for an answer explicitly confirmed during interrogation.
- `unresolved` for missing or conflicting evidence.

A confirmed working note must not become formal project knowledge before the Requirement Decision Record and disclosed knowledge changes are explicitly approved (`KB-DRAFT-001`). When persistence is useful and tools are available, use repository conventions or `docs/project/drafts/<workflow-id>-working-notes.md`.

## Ask exactly one question

For every turn:

1. Briefly state the decision already made when it affects the next branch.
2. Ask exactly one question.
3. Give one concrete recommended answer.
4. Explain its principal tradeoff.
5. Stop and wait.

Prioritize the unresolved decision with the greatest impact and uncertainty. Trace goals, users, scope, non-goals, behavior, failures, data, dependencies, security, privacy, operations, recovery, and acceptance criteria without using a fixed questionnaire.

## Prepare the formal artifacts

When high-impact decisions are confirmed, intentionally deferred with ownership, or proven irrelevant, prepare both artifacts as Draft.

The Requirement Decision Record must include its portable envelope and the confirmed problem, outcomes, users, behavior, boundaries, failures, contracts, constraints, acceptance criteria, assumptions, and deferrals.

The proposed Project Knowledge Base must use `docs/project/knowledge-base.md` and contain:

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

With only `conversation` capability, use only artifacts the user supplies. Emit complete Markdown for the Requirement Decision Record, Draft Working Notes, Knowledge Base, and change summary. State that the user owns cross-session persistence and must save and re-supply them. Never claim repository inspection, file writes, durable state, commands, tests, or independent review without real capability and evidence.
