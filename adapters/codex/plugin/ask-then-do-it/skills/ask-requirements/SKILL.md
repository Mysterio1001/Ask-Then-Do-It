---
name: ask-requirements
description: Interrogate ambiguous or high-impact software requirements one decision at a time before specification or implementation. Use when the user asks to be grilled, an idea lacks clear behavior or boundaries, consequential product or architecture decisions remain unresolved, or a structured workflow needs requirement consensus. Do not use for trivial requests whose relevant decisions are already explicit.
---

# Grill Requirements

Turn a vague request into explicit human-owned decisions. Make the AI find blind spots and recommend options; keep final authority with the user.

<!-- Maintainer note: One question per turn prevents shallow batch answers and lets each decision reshape the next branch. -->

Match user-facing questions and generated artifacts to the user's language when discoverable.

## Reconnoiter first

Before asking a question, perform focused, read-only discovery of:

- Applicable repository instructions and documentation.
- Related code paths, tests, data contracts, and established conventions.
- Existing specifications, plans, decisions, and current changes.
- Constraints that can be established from evidence.

Do not ask the user for facts that the repository already answers. Do not edit files, install dependencies, begin implementation, or change external state during grilling.

## Maintain a decision map

Track confirmed, assumed, deferred, and unresolved items across these areas:

- Objective, users, and success signal.
- Primary flow and user-visible behavior.
- Scope and explicit non-goals.
- Edge cases and failure behavior.
- Data ownership, lifecycle, migration, and compatibility.
- External dependencies and integration contracts.
- Security, privacy, permissions, and abuse cases.
- Operational constraints, rollout, and recovery.
- Acceptance criteria and verification.

Do not march through this list mechanically. Prioritize the unresolved decision with the largest combination of impact and uncertainty.

## Ask exactly one question

For every turn:

1. Briefly state the decision already made when it affects the next branch.
2. Ask one question only.
3. Give a concrete recommended answer.
4. Explain the recommendation's most important consequence or tradeoff.
5. Stop and wait for the user's answer.

Do not hide multiple questions in bullets, clauses, or an "anything else" prompt. If the user accepts the recommendation, record it as an explicit decision. If the answer creates a new architectural, data, security, workflow, or acceptance consequence, follow that branch next.

## Use informed defaults carefully

Make low-impact, reversible assumptions when repository evidence supports them. State the assumption in the final summary. Never assume a choice that materially changes product behavior, access, stored data, external coordination, cost, or destructive operations.

## Reach consensus

Continue until every high-impact item is confirmed, intentionally deferred with an owner, or proven irrelevant. Then:

1. Present a concise decision summary covering goals, non-goals, behavior, failures, data and dependencies, constraints, and acceptance criteria.
2. Identify remaining assumptions and deferrals.
3. Ask one final question: whether this summary is the agreed requirement.
4. Stop until the user explicitly confirms.

## Emit the decision artifact

At consolidation, emit a Requirement Decision Record with `status` set to `Draft`. Include or unambiguously convey `artifact_type`, stable `artifact_id`, shared `workflow_id`, `core_version` `1.2.0`, upstream `inputs`, `assumptions`, `deferred` decisions, the next-stage `handoff`, and empty or pending `approval` evidence.

After explicit confirmation on a later turn, record the approval evidence, change `status` to `Approved`, and hand the approved record to `$write-spec`. Do not infer approval from silence or an unrelated response. Do not implement code from this skill.
