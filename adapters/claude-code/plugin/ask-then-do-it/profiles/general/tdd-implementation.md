# Claude Code General profile TDD implementation

This General profile Full-stage module requires proven `tools`, proven `full` mode, an Approved Specification, an Approved Ticket Plan, and one eligible Ticket whose Approved mode is `tdd`. Never infer that mode. Stop at the earliest missing, contradicted, or obsolete gate and preserve unrelated work.

Core rules: TDD-RED-001

Before production, add or identify the smallest meaningful stable-boundary test and observe the expected failing test for the missing behavior. A setup or unrelated failure is not Red. If the test passes immediately, investigate existing behavior or test weakness. Declare a test-first exception and alternative check before editing only when no meaningful automated surface exists.

Make the smallest coherent production change for Green; do not weaken assertions or encode an incorrect result. Rerun the focused test, then Refactor names, duplication, boundaries, or structure without behavior change and rerun it. Perform risk-proportional broader verification and inspect final diff/status for scope drift.

Produce Implementation Evidence only for work actually observed with tools. Use the `portable artifact envelope` defined in `orchestration.md`, then add the Approved inputs and mode, changed files, raw Red/Green/post-Refactor/broader commands and results, exceptions, unavailable checks, risks, and Review handoff. Do not mark completion while a required check fails.

[CORE: TDD-RED-001]
[SCENARIO: FULL-TDD]
