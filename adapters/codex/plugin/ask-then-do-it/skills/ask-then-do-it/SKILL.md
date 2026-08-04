---
name: ask-then-do-it
description: Coordinate repository-aware software development through requirements, specification, mode-selected Ticket planning, TDD or direct implementation, review, and diagnostic architecture gates. Use for substantial new features, ambiguous requests, existing-system changes, cross-module work, architecture concerns, release milestones, or explicit requests for a structured end-to-end workflow. Do not invoke implicitly for trivial, fully specified fixes, formatting-only edits, or single-line changes.
---

# AI Dev Workflow

Keep orchestration thin. Discover the current stage, invoke the stage-specific skill, preserve approval state, and prevent premature implementation.

<!-- Maintainer note: A thin orchestrator avoids recreating the rigid monolithic workflow this suite is designed to replace. -->

## Declare capabilities

Before selecting or invoking a workflow stage, state the strongest capability profile proven in the current runtime:

- `conversation` can exchange text and produce user-managed artifacts.
- `tools` additionally requires actual repository read/write access, artifact persistence, and command execution.
- `multi_agent` additionally requires isolated worker or reviewer contexts.

If a required tool or isolation mechanism is unavailable, downgrade to the strongest proven profile. Never claim repository changes, test execution, persistence, parallel independence, or completed review evidence outside the declared profile. End an unsupported stage with the limitation, required handoff, and safe next action.

## Operating rules

- Match user-facing communication and generated documents to the user's language. Default to Traditional Chinese only when no preference is discoverable.
- Read applicable repository instructions before acting. Preserve user changes and follow existing project conventions.
- Answer questions from repository evidence instead of asking the user. Ask only for product decisions, unavailable context, or choices with material tradeoffs.
- Treat requirement consensus, specification approval, and ticket-plan approval as separate human gates.
- Never modify implementation code, install dependencies, or cause external side effects before all applicable gates pass.
- If implementation evidence contradicts an approved artifact, return to the earliest affected gate. Never silently redefine the requirement.

## Decide whether to orchestrate

Use the full workflow when the request is ambiguous, consequential, cross-cutting, architectural, or explicitly invokes this skill. For a small and fully specified change, explain briefly that the lightweight path applies and handle it normally unless the user explicitly requests the gated workflow.

## Honor explicit user control

Honor an explicit user selection of `$ask-requirements`, `$ask-with-docs`, `$write-spec`, `$plan-tickets`, `$implement-tdd`, `$implement-direct`, `$review-code`, or `$improve-architecture` over automatic routing (`ROUTE-USER-001`). Preserve every capability, safety, and approval gate; direct selection cannot bypass a missing prerequisite or a conflicting Approved Ticket mode.

Do not require the user to know Skill names. Route a natural-language request by intent when the evidence is sufficient.

## Choose the requirement mode

Use `$ask-requirements` for a fresh, self-contained requirement unless the user selects another mode. Select `$ask-with-docs` automatically when:

- A Project Knowledge Base already exists.
- The requested work changes an existing system.
- The discussion is likely to introduce durable project knowledge.

Before automatic selection, state a brief reason (`ROUTE-DOCS-001`). If the user explicitly chooses normal or documented interrogation, follow that choice.

## Discover the current stage

Perform focused, read-only reconnaissance:

1. Read applicable instruction files and repository documentation.
2. Inspect the project structure, relevant code and tests, current version-control state, and existing spec or plan conventions.
3. Locate artifacts for the requested feature.
4. Determine the first unmet condition in this order:

| Evidence | Next action |
| --- | --- |
| Important decisions remain ambiguous | Choose the requirement mode, then invoke `$ask-requirements` or `$ask-with-docs` |
| An accepted Architecture Improvement Report proposes unplanned change | Invoke `$write-spec` and preserve the report as input |
| Consensus exists but no specification exists | Invoke `$write-spec` |
| Specification is draft or disputed | Present or revise it and obtain approval |
| Approved specification exists but no ticket plan exists | Invoke `$plan-tickets` |
| Ticket plan is draft or disputed | Present or revise it and obtain approval |
| Approved Tickets remain | Route the next eligible Ticket from its Approved mode |
| Implementation changed | Invoke `$review-code` |
| Review contains systemic architecture evidence | Invoke `$improve-architecture` for diagnosis only |
| Review has no blocking findings and verification passes | Hand off the completed result |

Do not force users to replay completed stages. Verify that an existing artifact is relevant, internally consistent, and explicitly approved before relying on it.

## Route implementation modes

- Ticket Planning collects all plain-language test choices in one batch and maps adding tests to `tdd` and declining tests to `direct`; never ask the user to choose those internal names as the initial decision.
- Route an eligible Approved `tdd` Ticket to `$implement-tdd`.
- Route an eligible Approved `direct` Ticket to `$implement-direct`.
- Do not infer a default implementation mode from silence, repository conventions, risk, another Ticket, or earlier history.
- Return a missing, unknown, conflicting, or changed mode to `$plan-tickets`; changing an Approved mode returns the plan to `Draft` and requires reapproval.
- Preserve the selected mode in implementation evidence and `$review-code` handoff.

## Route architecture diagnosis

Invoke `$improve-architecture` for a direct architecture request, systemic review evidence, completion of a related Ticket group, or an approaching release milestone. Announce the evidence and reason before an automatic route.

Do not run architecture diagnosis after every Ticket. Keep local review findings in `$review-code`; route only cross-module or systemic evidence. An accepted Architecture Improvement Report returns to `$write-spec`, never directly to planning or implementation.

## Synchronize project knowledge

When an Approved or accepted artifact introduces, changes, supersedes, or resolves durable facts, propose a Knowledge Base Change Summary through `$ask-with-docs` rules. Show additions, modifications, and removals and bind approval only to the displayed changes. Do not invent a knowledge update when the artifact adds no durable fact.

## Enforce the gates

At each gate:

1. Lead with the proposed outcome and material tradeoffs.
2. Request explicit approval.
3. Record approval in the artifact by changing its status from `Draft` to `Approved`.
4. Continue only after the status and conversation agree.

Treat silence, an unrelated reply, or previous approval of another artifact as no approval.

## Coordinate tickets

- Execute tickets in dependency order.
- Parallelize only tickets explicitly marked safe whose contracts are settled and whose files and core abstractions do not overlap.
- When the runtime supports subagents, give each one only its approved ticket, relevant spec sections, necessary repository instructions, and ownership boundary.
- Integrate all parallel results centrally and run the combined verification suite before review.
- Prefer sequential execution whenever independence is uncertain.

## Finish

Report the delivered behavior, approved artifacts, tickets completed, test evidence, review outcome, residual risks, and any intentionally deferred work. Do not claim completion while required verification or blocking review findings remain.
