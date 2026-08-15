# Workflow Orchestration

## Purpose

Select the first unmet workflow stage, enforce approvals, and coordinate bounded handoffs without duplicating stage-specific procedures.

## Contract

- The adapter MUST declare proven capabilities before stage selection (`CAP-DECLARE-001`).
- The workflow MUST NOT claim actions or evidence outside those capabilities (`CAP-CLAIM-001`).
- An explicit user selection of a module, requirement mode, or Ticket implementation mode MUST override automatic routing unless it would violate a safety or approval gate (`ROUTE-USER-001`).
- User-facing output SHOULD match the user's language when discoverable.

## Resolve the top-level workflow mode

The workflow exposes exactly two top-level modes: `full` and `lite`. This mode is separate from the Full Ticket implementation modes `tdd` and `direct`.

For each operation, an adapter MUST evaluate supported sources in this order (`MODE-RESOLVE-001`):

1. explicit current-operation instruction;
2. project-scoped default;
3. user-scoped default;
4. `full` fallback.

Every public workflow entry is an operation, including direct selection of a stage module. Selecting a stage does not select `full` or bypass top-level mode resolution.

- A directly selected stage MUST reuse a proven current-operation mode without resolving again.
- When the current operation has no proven resolved mode, an entry that can invoke or load the adapter's resolver MUST delegate to the adapter's canonical mode resolver before applying stage-specific behavior.
- An independently distributable standalone stage that cannot load another module MAY apply a bounded direct-entry guard. The guard MUST use the same supported sources, precedence, conflict handling, fail-closed behavior, and non-persistence contract as the canonical resolver. It is not complete mode-resolution ownership and MUST do nothing beyond establishing the mode and routing or stopping the selected stage.
- A resolved `lite` mode MUST stop the Full stage and route to Lite.
- Only a proven `full` mode may continue directly into the selected Full stage, and every existing stage prerequisite and approval still applies.
- Conflicting explicit mode instructions remain unresolved and MUST pause for clarification; direct stage selection MUST NOT break the conflict by implying Full.

Resolution is fail-closed and distinguishes absence from invalid content:

- A valid explicit current-operation instruction wins even when a lower-priority default is invalid.
- Conflicting explicit instructions require clarification and MUST NOT fall through to a default.
- An absent project-scoped default continues to the user-scoped default. A host that cannot provide a project source treats it as absent.
- A valid project-scoped default selects its mode.
- A present but unreadable, malformed, missing-mode, or unsupported project-scoped default resolves to `full` and MUST NOT fall through to the user default.
- An absent user-scoped default resolves to `full`. A host that cannot provide a user source treats it as absent.
- A valid user-scoped default selects its mode.
- A present but unreadable, malformed, missing-mode, or unsupported user-scoped default resolves to `full`.

The workflow MUST NOT persist a current-operation override or reuse it as an undocumented later-session default.

## Route Full mode

When the resolved mode is `full`, the workflow MUST preserve the existing assurance-oriented behavior (`FULL-PRESERVE-001`). In particular:

- The orchestrator MUST inspect supplied artifacts and select the first unmet condition: requirement consensus, approved Specification, approved Ticket Plan, eligible implementation, review, or completion.
- Existing approved artifacts SHOULD be reused when relevant and internally consistent.
- A missing, disputed, incompatible, or unverifiable upstream artifact MUST return the workflow to the affected gate.
- Implementation MUST NOT begin before requirement, Specification, and Ticket Plan gates applicable to the work are approved.
- Ticket Planning collects all plain-language test choices in one batch, maps adding tests to `tdd` and declining tests to `direct`, and leaves every unresolved Ticket at the plan gate.
- Route an eligible approved `tdd` Ticket to test-driven implementation and an eligible approved `direct` Ticket to direct implementation.
- The orchestrator MUST NOT infer a default implementation mode from silence, repository conventions, risk, another Ticket, or prior workflow history.
- A missing, unknown, conflicting, or unapproved Ticket mode MUST return the workflow to Ticket Planning rather than falling back to an implementation path.
- A later mode change MUST return the Ticket Plan to `Draft` and block affected implementation until explicit reapproval.

### Select the Full requirement mode

Use normal requirement interrogation by default for a fresh, self-contained request. Select documented requirement interrogation automatically when:

- A Project Knowledge Base already exists.
- The requested work changes an existing system.
- The discussion is likely to introduce durable project knowledge.

When automatic selection occurs, state a brief reason before starting (`ROUTE-DOCS-001`). An explicit user selection of normal or documented interrogation remains authoritative.

### Route Full architecture diagnosis

Select architecture improvement when the user directly requests architecture diagnosis, review reports systemic architecture evidence, a related Ticket group is complete, or a release milestone is approaching.

Announce an automatic architecture route and its evidence. Architecture diagnosis MUST NOT run after every Ticket by default. A focused local review finding remains in Review unless its evidence is cross-module or systemic.

An accepted Architecture Improvement Report routes to Specification. It MUST NOT route directly to Ticket Plan or implementation.

### Synchronize durable knowledge

When an approved or accepted artifact changes durable facts, request a Knowledge Base Change Summary through the project-knowledge contract. Do not delay an unrelated gate when the artifact introduces no durable knowledge.

## Route Lite mode

When the resolved mode is `lite`, route the operation through [lite-workflow.md](lite-workflow.md). Lite MUST NOT fabricate Full requirement consensus, an Approved Specification, an Approved Ticket Plan, a Ticket implementation mode, or Full evidence merely to satisfy the Full first unmet condition.

If the host cannot perform a requested Lite implementation or validation action, the workflow MUST stop with the capability limitation, the unavailable evidence, and a safe handoff. It MUST NOT silently route to Full or claim unobserved work.

## Capability downgrade

- A `conversation` host MAY orchestrate requirements, Specification, and Ticket Plan drafts.
- Formal TDD or direct implementation completion requires `tools`.
- Independent review and parallel workers require `multi_agent`.
- Unsupported stages MUST end with a limitation, required handoff artifact, and safe next action.
