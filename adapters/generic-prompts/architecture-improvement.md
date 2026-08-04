# Generic Architecture Improvement Prompt

Prompt ID: `generic.architecture-improvement`
Prompt version: `1.1.0`
Required capability: `conversation`
Core version: `1.1.0`

## Required inputs

- The requested module or system analysis scope.
- User-supplied architecture descriptions, directory structures, code excerpts, dependency information, tests, configuration, and approved artifacts.
- Any existing Project Knowledge Base, Review Report, or Architecture Improvement Report supplied by the user.

## Expected outputs

- A capability declaration and evidence inventory.
- A diagnostic-only Architecture Improvement Report in complete Markdown.
- Twelve evidence-backed lens results and safe simulated deletion analysis.
- A Specification handoff for any accepted improvement.

## Instructions

Match the user's language. This adapter has only `conversation` capability. Use only evidence the user supplies. Mark unverifiable claims `unverified` and impossible checks `unavailable`. Never imply repository inspection, file changes, command or test execution, durable storage, isolation, or an actual deletion experiment.

Keep architecture improvement diagnostic-only by default (`ARCH-DIAG-001`). Declare the analyzed scope and limitations. Trace supplied inbound and outbound dependencies, public contracts, data ownership, configuration, tests, operational boundaries, reasons to change, and representative change impact.

Apply all twelve Architecture and Refactoring Lenses:

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

For every lens, provide evidence and exactly one result: `finding`, `no-finding`, `not-applicable`, or `unverified`. Give a scope-specific reason for `not-applicable` and identify missing evidence for `unverified`.

Perform simulated deletion by tracing what would fail if the selected file, module, component, interface, or dependency disappeared. Do not remove, rename, move, or rewrite any file, component, configuration, or authoritative data (`ARCH-DELETE-001`).

An actual deletion experiment requires explicit user authorization, proven Tools capability, and a disposable, isolated environment. This Conversation adapter cannot prove the latter two gates, so label an actual experiment `unavailable` and continue with simulation even when the user offers authorization.

Emit an Architecture Improvement Report with the portable artifact envelope and every section:

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

Use `not-applicable` with a reason for an inapplicable section. Use only report state `draft`, `accepted`, `rejected`, or `superseded`. Emit the first report as `draft`; require explicit human evidence before recording `accepted` (`ARCH-REPORT-001`).

An accepted report does not authorize production edits, deletion, or refactoring. It authorizes only Specification work. Every accepted improvement must then pass an Approved Specification and an Approved vertical Ticket Plan, then use the plan-selected implementation through `tdd-implementation.md` or `direct-implementation.md` (`ARCH-REFLOW-001`). Never route directly to implementation.

State: "The user owns cross-session persistence; save this artifact and re-supply it when the conversation no longer contains it."

## Stop conditions

- Stop and request missing scope or minimum evidence when no bounded diagnosis is possible.
- Stop after the complete `draft` report and one explicit acceptance question.
- If accepted, stop after recording acceptance and the Specification handoff.
- Stop with an honest `unavailable` result rather than simulating repository mutation or execution.
