# Workflow Orchestration

## Purpose

Select the first unmet workflow stage, enforce approvals, and coordinate bounded handoffs without duplicating stage-specific procedures.

## Contract

- The adapter MUST declare proven capabilities before stage selection (`CAP-DECLARE-001`).
- The workflow MUST NOT claim actions or evidence outside those capabilities (`CAP-CLAIM-001`).
- An explicit user selection of a module, requirement mode, or Ticket implementation mode MUST override automatic routing unless it would violate a safety or approval gate (`ROUTE-USER-001`).
- The orchestrator MUST inspect supplied artifacts and select the first unmet condition: requirement consensus, approved Specification, approved Ticket Plan, eligible implementation, review, or completion.
- Existing approved artifacts SHOULD be reused when relevant and internally consistent.
- A missing, disputed, incompatible, or unverifiable upstream artifact MUST return the workflow to the affected gate.
- Implementation MUST NOT begin before requirement, Specification, and Ticket Plan gates applicable to the work are approved.
- Ticket Planning collects all plain-language test choices in one batch, maps adding tests to `tdd` and declining tests to `direct`, and leaves every unresolved Ticket at the plan gate.
- Route an eligible approved `tdd` Ticket to test-driven implementation and an eligible approved `direct` Ticket to direct implementation.
- The orchestrator MUST NOT infer a default implementation mode from silence, repository conventions, risk, another Ticket, or prior workflow history.
- A missing, unknown, conflicting, or unapproved Ticket mode MUST return the workflow to Ticket Planning rather than falling back to an implementation path.
- A later mode change MUST return the Ticket Plan to `Draft` and block affected implementation until explicit reapproval.
- User-facing output SHOULD match the user's language when discoverable.

## Select the requirement mode

Use normal requirement interrogation by default for a fresh, self-contained request. Select documented requirement interrogation automatically when:

- A Project Knowledge Base already exists.
- The requested work changes an existing system.
- The discussion is likely to introduce durable project knowledge.

When automatic selection occurs, state a brief reason before starting (`ROUTE-DOCS-001`). An explicit user selection of normal or documented interrogation remains authoritative.

## Route architecture diagnosis

Select architecture improvement when the user directly requests architecture diagnosis, review reports systemic architecture evidence, a related Ticket group is complete, or a release milestone is approaching.

Announce an automatic architecture route and its evidence. Architecture diagnosis MUST NOT run after every Ticket by default. A focused local review finding remains in Review unless its evidence is cross-module or systemic.

An accepted Architecture Improvement Report routes to Specification. It MUST NOT route directly to Ticket Plan or implementation.

## Synchronize durable knowledge

When an approved or accepted artifact changes durable facts, request a Knowledge Base Change Summary through the project-knowledge contract. Do not delay an unrelated gate when the artifact introduces no durable knowledge.

## Capability downgrade

- A `conversation` host MAY orchestrate requirements, Specification, and Ticket Plan drafts.
- Formal TDD or direct implementation completion requires `tools`.
- Independent review and parallel workers require `multi_agent`.
- Unsupported stages MUST end with a limitation, required handoff artifact, and safe next action.
