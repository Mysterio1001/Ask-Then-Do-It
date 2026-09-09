# Claude Code General profile architecture improvement

This General profile Full-stage module is diagnostic-only unless a later approved workflow authorizes implementation. Declare the analysis scope, available evidence, limitations, and strongest proven capability. Do not edit production code while diagnosing.

Core rules: ARCH-DIAG-001, ARCH-DELETE-001, ARCH-REPORT-001, ARCH-REFLOW-001

Inspect applicable approved artifacts, modules, dependencies, public contracts, tests, configuration, data ownership, operations, and representative change impact. Trace inbound/outbound dependencies and distinguish observation from inference.

Apply the same twelve Architecture and Refactoring Lenses required by Review, each with evidence and one result: `finding`, `no-finding`, `not-applicable` with reason, or `unverified` with missing evidence.

The canonical lens order is: Duplicated Code or Policy; Long Function; Large Module or Class; Long Parameter List; Data Clumps; Primitive Obsession; Feature Envy; Divergent Change; Shotgun Surgery; Message Chains; Leaky Abstraction; Shallow Module.

Perform simulated deletion by tracing what would break if the selected component disappeared; do not remove, rename, move, or rewrite it. An actual deletion experiment requires fresh explicit authorization for exact scope/risk, proven tools, and a disposable isolated environment. Without all three, simulation is the only allowed path.

Emit a complete Architecture Improvement Report. Use the `portable artifact envelope` defined in `orchestration.md`, then add scope/limitations, architecture summary, deletion analysis, twelve-lens results, finding evidence/impact/confidence, prioritized proposals, affected modules, unresolved items, artifact links, and Knowledge Base Change Summary or a reason it is not applicable. The first status is `draft`; only explicit user evidence may make it `accepted`, `rejected`, or `superseded`.

Acceptance authorizes only Specification work. Every accepted improvement must flow through an Approved Specification, Approved vertical Ticket Plan, and its plan-selected implementation path; never route directly to implementation.

[CORE: ARCH-DIAG-001]
[CORE: ARCH-DELETE-001]
[CORE: ARCH-REPORT-001]
[CORE: ARCH-REFLOW-001]
[SCENARIO: FULL-ARCH]
