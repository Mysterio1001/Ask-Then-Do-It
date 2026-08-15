# Adapter Conformance Manifest

Every adapter MUST provide a machine-readable manifest with:

- `adapter_id`: stable adapter identifier.
- `adapter_version`: adapter semantic version.
- `target`: host or usage mode.
- `core_version`: compatible core version.
- `capabilities`: declared capability profiles.
- `artifact_persistence`: how artifacts are retained.
- `implemented_rules`: every mandatory core rule ID (`ADAPTER-COVERAGE-001`).
- `capability_evidence`: non-empty validation evidence for every declared profile.
- `validation.status`: current validation claim.
- `validation.environment`: tested environment.
- `validation.commands`: reproducible checks.

Every adapter MUST map the top-level modes `full` and `lite` without conflating them with the Full Ticket implementation modes `tdd` and `direct`. A conforming mapping MUST cover:

- `MODE-RESOLVE-001` and `FULL-PRESERVE-001` in orchestration;
- `LITE-QUESTIONS-001`, `LITE-BRIEF-001`, `LITE-RISK-001`, `LITE-VALIDATE-001`, `LITE-REVIEW-001`, and `LITE-SESSION-001` in its Lite route.

The `MODE-RESOLVE-001` mapping MUST cover every public workflow entry. Direct stage selection chooses only a stage and MUST NOT imply Full. Each entry MUST reuse a proven current-operation mode. Without proof, an entry either delegates to the adapter's canonical mode resolver or, only when an independently distributable standalone stage cannot load another module, applies a bounded direct-entry guard with equivalent supported sources, precedence, conflict handling, fail-closed behavior, and non-persistence. The bounded guard is not complete mode-resolution ownership. A resolved Lite route stops Full stage behavior, and only proven Full may continue through the selected stage's existing gates.

Host capabilities MAY change which default sources, implementation actions, or validation evidence are available. They MUST NOT change the resolved mode semantics, fabricate unavailable evidence, persist a current-operation override, or represent a Lite Change Brief as a durable workflow artifact.

Adapters that expose implementation MUST represent both Approved Ticket modes consistently: `tdd` routes to test-driven implementation and `direct` routes to direct implementation. Capability limitations may change what an adapter can execute, but MUST NOT change the selected mode or fabricate evidence.

Capability profiles are cumulative: `tools` includes `conversation`; `multi_agent` includes `conversation` and `tools`.

The shared validator MUST reject missing mandatory rules, unknown rules, incompatible core versions, unknown capabilities, incomplete capability hierarchy, and a declared capability without evidence.
