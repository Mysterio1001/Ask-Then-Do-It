# Claude 5 Architecture Improvement

Core rules: ARCH-DIAG-001, ARCH-DELETE-001, ARCH-REPORT-001, ARCH-REFLOW-001, REVIEW-LENSES-001

Keep this stage diagnostic-only. Declare scope, capability, evidence, limitations, dependencies, ownership, change radius, and observable boundaries. Do not edit production or implement proposals.

Apply the same twelve Architecture and Refactoring Lenses required by Full Review, with one evidence-backed `finding`, `no-finding`, `not-applicable` reason, or `unverified` gap per lens. Findings state evidence, impact, confidence, and affected modules.

The canonical lens order is: Duplicated Code or Policy; Long Function; Large Module or Class; Long Parameter List; Data Clumps; Primitive Obsession; Feature Envy; Divergent Change; Shotgun Surgery; Message Chains; Leaky Abstraction; Shallow Module.

Use simulated deletion by default: trace inbound/outbound dependencies, contracts, tests, configuration, data ownership, deployment, and operational effects without deleting, renaming, moving, or rewriting anything. An actual experiment requires prior explicit user authorization after scope/risk disclosure, proven tools capability, and a disposable isolated environment; otherwise simulate. Record exact experiment commands/results and restoration/disposal only when all gates are proven.

Emit a complete Architecture Improvement Report with the common envelope and: scope/limits; architecture summary; labeled deletion analysis; twelve-lens results; finding evidence/impact/confidence; prioritized proposals; affected modules; unresolved items; artifact links; and a Knowledge Base Change Summary when durable facts changed. Start `draft`; only explicit approval changes it to `accepted`. Acceptance approves diagnosis only. Route accepted structural or behavioral proposals through Specification, Ticket Plan, and the plan-selected implementation path—never directly to edits.

Conversation capability uses only supplied evidence, marks gaps unverified/unavailable, and emits user-managed Markdown; it cannot claim repository inspection, persistence, commands, independence, or actual deletion.

For an authorized actual experiment, also record the isolated environment and exact deleted scope.
