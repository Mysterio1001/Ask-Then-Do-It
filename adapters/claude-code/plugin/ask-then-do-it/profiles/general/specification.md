# Claude Code General profile Specification authoring

This General profile Full-stage module requires a proven `full` mode and an Approved Requirement Decision Record (or equivalent explicitly confirmed decisions). Return to requirements when material intent is missing; never invent it.

Core rules: GATE-SPEC-001, SPEC-NOCODE-001, ART-STATE-001

Write an implementation-independent behavioral Specification covering problem, goals/non-goals, users/scenarios, required behavior, edge/failure behavior, data/permissions/external contracts, compatibility/rollout/recovery, constraints/assumptions, observable acceptance criteria, and deferrals. Keep production implementation code out of the document.

Use the `portable artifact envelope` defined in `orchestration.md` and emit the first version with status `Draft`. Ask for explicit human approval of that exact Specification. Silence, an unrelated reply, or approval of another artifact is not approval. Only after approval evidence exists may status become `Approved`; Draft or disputed Specifications cannot authorize Ticket Planning or implementation.

[CORE: SPEC-NOCODE-001]
[CORE: GATE-SPEC-001]
[CORE: ART-STATE-001]
[SCENARIO: FULL-SPEC]
