---
name: improve-architecture
description: Diagnose module or system architecture with evidence-based refactoring lenses, dependency tracing, safe simulated deletion, and a structured Architecture Improvement Report. Use when the user requests architecture analysis, review exposes systemic coupling or shallow modules, or a related ticket group or release milestone needs architecture health assessment. Diagnosis is read-only by default and never authorizes refactoring.
---

# Improve Architecture

Assess architecture without changing it. Keep this skill diagnostic-only by default and Match user-facing communication and generated artifacts to the user's language when discoverable.

<!-- Maintainer note: Diagnosis and implementation stay separate so an attractive refactor cannot bypass product intent, planning, or the user's implementation-mode choice. -->

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

Evaluate the declared scope using this fixed core set:

1. Duplicated Code or Policy.
2. Long Function.
3. Large Module or Class.
4. Long Parameter List.
5. Data Clumps.
6. Primitive Obsession.
7. Feature Envy.
8. Divergent Change.
9. Shotgun Surgery.
10. Message Chains.
11. Leaky Abstraction.
12. Shallow Module.

For every lens, record evidence and one result: `finding`, `no-finding`, `not-applicable`, or `unverified`. Give a reason for `not-applicable` and identify missing evidence for `unverified`. Project-specific lenses may be added but cannot replace or skip the core set.

## Simulate deletion safely

Use simulated deletion by default (`ARCH-DELETE-001`). Trace what would fail if the selected file, module, component, interface, or dependency disappeared. Examine callers, callees, tests, configuration, data, deployment, and operational consequences.

Simulated deletion must not remove, rename, move, or rewrite files, components, configuration, or authoritative data.

An actual deletion experiment requires explicit user authorization, proven `tools` capability, and a disposable, isolated environment. Verify all three gates:

1. Explicit user authorization after the exact scope and risk are stated.
2. Proven `tools` capability for inspection, mutation, and verification.
3. A disposable, isolated environment that can be abandoned without affecting the working copy, personal installation, external system, or authoritative data.

If any gate is absent, continue only with simulation. When all gates are proven, record the isolated environment, deleted scope, raw commands or checks, raw outcomes, and restoration or disposal result.

## Emit the architecture report

Emit an Architecture Improvement Report with `artifact_type`, stable `artifact_id`, shared `workflow_id`, `core_version` `1.1.0`, `status`, `inputs`, `assumptions`, `deferred`, `handoff`, and `approval` evidence when accepted.

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
