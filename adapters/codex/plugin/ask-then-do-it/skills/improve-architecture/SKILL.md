---
name: improve-architecture
description: Diagnose module or system architecture with evidence-based refactoring lenses, dependency tracing, safe simulated deletion, and a structured Architecture Improvement Report. Use when the user requests architecture analysis, review exposes systemic coupling or shallow modules, or a related ticket group or release milestone needs architecture health assessment. Diagnosis is read-only by default and never authorizes refactoring.
---

# Improve Architecture

Assess architecture without changing it. Keep this skill diagnostic-only by default and Match user-facing communication and generated artifacts to the user's language when discoverable.

<!-- Maintainer note: Diagnosis and implementation stay separate so an attractive refactor cannot bypass product intent, planning, or the user's implementation-mode choice. -->

## Resolve the top-level mode before this stage

Direct selection of this Skill chooses this Full-workflow stage, not top-level `full`. Before stage behavior, require a current-operation mode proof from `$ask-then-do-it`; never persist or reuse mode.

- Missing proof: stop and delegate to `$ask-then-do-it`.
- Proven `lite`: stop this Full stage and route to the Lite workflow.
- Proven `full`: continue with this stage's prerequisites and gates.

## Declare scope and capability

State the analyzed module or system boundary, the available evidence, and the strongest proven capability:

- `conversation` can analyze only user-supplied artifacts.
- `tools` can inspect a repository and execute read-only checks.
- `multi_agent` may add an isolated diagnostic view when genuinely available.

Do not claim stronger evidence than the runtime produces. Record missing evidence as `unverified` and impossible checks as `unavailable`.

## Gather architecture evidence

Read applicable instructions, approved artifacts, Project Knowledge Base, module interfaces, dependency edges, tests, configuration, data ownership, operational boundaries, and representative change history when available. Distinguish observed evidence from inference.

Trace inbound and outbound dependencies, public contracts, ownership, reasons to change, and the impact radius of representative changes. Do not edit production code or implement a proposal.

## Apply all twelve lenses

Read the [canonical architecture and refactoring lens contract](../ask-then-do-it/references/architecture-refactoring-lenses.md) completely immediately before the lens pass. If it is missing or unreadable, stop and do not claim a completed twelve-lens pass. Evaluate the declared scope using every lens in that contract's fixed order, recording one contract outcome with evidence for each. Preserve this stage's diagnostic scope, dependency tracing, simulated deletion, report state, and accepted-proposal handoff; project-specific lenses may follow but cannot replace or skip the core set.

## Simulate deletion safely

Use simulated deletion by default (`ARCH-DELETE-001`). Trace what would fail if the selected file, module, component, interface, or dependency disappeared. Examine callers, callees, tests, configuration, data, deployment, and operational consequences.

Simulated deletion must not remove, rename, move, or rewrite files, components, configuration, or authoritative data.

An actual deletion experiment requires explicit user authorization, proven `tools` capability, and a disposable, isolated environment. Verify all three gates:

1. Explicit user authorization after the exact scope and risk are stated.
2. Proven `tools` capability for inspection, mutation, and verification.
3. A disposable, isolated environment that can be abandoned without affecting the working copy, personal installation, external system, or authoritative data.

If any gate is absent, continue only with simulation. When all gates are proven, record the isolated environment, deleted scope, raw commands or checks, raw outcomes, and restoration or disposal result.

## Use the portable artifact contract

Before creating or emitting an Architecture Improvement Report, read the [portable artifact contract](../ask-then-do-it/references/artifact-contract.md) completely. If it is missing or unreadable, stop before artifact creation and leave the handoff pending.

## Emit the architecture report

Emit an Architecture Improvement Report using the portable artifact contract for the common envelope. Preserve the diagnostic state, `approval` evidence when accepted, and the stage-specific sections below.

Include every section:

1. Analysis scope and limitations.
2. System architecture summary.
3. Deletion-analysis results.
4. Twelve-lens results.
5. Finding evidence, impact, and confidence.
6. Prioritized improvement proposals.
7. Potentially affected modules.
8. Unresolved items.
9. Artifact links.
10. Knowledge Base Change Summary when durable knowledge changed.

Use `not-applicable` with a reason rather than silently omitting a section.

## Enforce report state and handoff

Use only `draft`, `accepted`, `rejected`, or `superseded`. Emit the first report as `draft`. Require explicit user evidence before changing it to `accepted`.

An accepted report does not authorize production edits, deletion, or refactoring. It authorizes only a return to `$write-spec`. Every accepted improvement must then pass an Approved Specification and an Approved vertical Ticket Plan through `$plan-tickets`, then use the plan-selected implementation through `$implement-tdd` or `$implement-direct` (`ARCH-REPORT-001`, `ARCH-REFLOW-001`). Never route directly from this skill to implementation.

## Downgrade honestly

With only `conversation` capability, use only artifacts the user supplies and emit complete Markdown for user-managed persistence. State that the user must save and re-supply the report in a later session. Do not claim repository inspection, file changes, commands, tests, durable storage, independent analysis, or an actual deletion experiment.
