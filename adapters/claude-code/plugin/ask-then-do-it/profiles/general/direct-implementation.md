# Claude Code General profile direct implementation

This General profile Full-stage module requires proven `tools`, proven `full` mode, an Approved Specification, an Approved Ticket Plan, and one eligible Ticket whose Approved mode is `direct`. Never infer it from silence, risk, conventions, or another Ticket.

Core rules: none

Implement only the smallest coherent approved change. For `Run existing tests only`, run relevant existing behavioral tests without adding or modifying tests. Record actual commands and outcomes, including failures or unavailable coverage. An unresolved failure prevents an unqualified success claim. For `Skip behavioral tests` and legacy Approved direct Tickets without explicit existing-test permission, the workflow must not create, modify, or execute behavioral tests. It may run non-test validation such as lint, type-check, build, schema, syntax, and other static checks. An external system's mandatory tests remain a disclosed constraint; do not pretend direct mode bypasses them.

Preserve unrelated changes, inspect the final diff/status, and record every actually observed command and raw result. Record `tests: skipped-by-user` only for the skip choice or legacy direct approvals. Report only observed existing-test outcomes; never claim TDD. List unavailable behavioral evidence, untested paths, external constraints, incomplete checks, and residual risk.

Emit Direct Implementation Evidence. Use the `portable artifact envelope` defined in `orchestration.md`, then add the Approved inputs and mode, scope, files, the Approved test choice, raw validation results, and untested paths. A contradiction returns to the earliest affected gate.

[SCENARIO: FULL-DIRECT]
