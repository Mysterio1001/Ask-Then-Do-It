# Claude Code General profile requirement interrogation

This General profile Full-stage module requires a mode already proven as `full`. If the current operation has no proof, return to orchestration; if it is `lite`, load only the Lite workflow.

Core rules: GATE-REQ-001, GRILL-ONE-001

Use available read-only project evidence before asking. Trace outcome, users, success, scope/non-goals, behavior/failures, data, dependencies, security/privacy, operations/recovery, and observable acceptance criteria. Make only low-impact reversible assumptions and disclose them.

Ask exactly one question per turn. Select the unresolved decision with the greatest impact and uncertainty, give one concrete recommendation and principal tradeoff, then stop. Do not hide additional questions in bullets or clauses.

When high-impact decisions are confirmed, intentionally deferred with ownership, or proven irrelevant, emit a complete Requirement Decision Record. Use the `portable artifact envelope` defined in `orchestration.md`, then add problem/outcome, users/signals, scope/non-goals, behavior/failures, data/contracts, constraints, acceptance criteria, assumptions, and deferrals. Its first status is `Draft`. Ask one explicit human confirmation of the entire consensus. Only a later direct approval changes it to `Approved` with approval evidence; silence or another approval does not count. Do not authorize implementation.

[CORE: GRILL-ONE-001]
[CORE: GATE-REQ-001]
[SCENARIO: FULL-REQUIREMENTS]
