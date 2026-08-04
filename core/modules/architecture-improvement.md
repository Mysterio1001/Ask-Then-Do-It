# Architecture Improvement

## Purpose

Diagnose system-level change cost, coupling, and abstraction quality without treating analysis as permission to refactor.

## Diagnostic contract

- Keep architecture improvement diagnostic-only by default (`ARCH-DIAG-001`).
- Declare the analyzed module or system scope and unavailable evidence.
- Apply all twelve [Architecture and Refactoring Lenses](../references/architecture-refactoring-lenses.md).
- Trace dependencies, ownership, change impact, and observable boundaries.
- Support every finding with evidence, impact, confidence, and affected modules.
- Do not edit production code or implement a proposal during diagnosis.

## Deletion analysis

Use simulated deletion as the default (`ARCH-DELETE-001`). Trace inbound dependencies, outbound dependencies, public contracts, tests, configuration, data ownership, and operational consequences. Simulated deletion MUST NOT remove, rename, move, or rewrite any file, module, component, or authoritative data.

An actual deletion experiment MAY run only when explicit user authorization, proven Tools capability, and a disposable, isolated environment are all present:

1. Explicit user authorization after the exact scope and risk are stated.
2. Proven Tools capability for inspection, mutation, and verification.
3. A disposable, isolated environment that can be abandoned without affecting the working copy, personal installation, external system, or authoritative data.

If any gate is missing, fall back to simulated deletion. When all gates exist, record the isolated environment, deleted scope, raw commands or checks, raw outcomes, and restoration or disposal result.

## Report and handoff

- Produce an Architecture Improvement Report with every required section (`ARCH-REPORT-001`).
- Keep the first report `draft` and require explicit user evidence before changing it to `accepted`.
- Treat `accepted` as agreement with the diagnosis only. It does not authorize edits, deletion, or refactoring.
- Route every accepted structural or behavioral proposal to Specification, then an approved vertical Ticket Plan, then the plan-selected implementation path (`ARCH-REFLOW-001`).
- Never route an accepted report directly to implementation.

## Capability downgrade

A `conversation` adapter MUST analyze only user-supplied evidence, label unverifiable claims `unverified`, label impossible checks `unavailable`, and emit complete Markdown for user-managed persistence. It MUST NOT claim repository inspection, mutation, test execution, durable persistence, or an actual deletion experiment.
