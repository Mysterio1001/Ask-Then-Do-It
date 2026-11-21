# Claude 5 Direct Implementation

Core rules: FULL-PRESERVE-001, CAP-CLAIM-001

Require tools capability, Approved Specification and Ticket Plan, completed dependencies, and one eligible Ticket whose Approved mode is `direct`. Preserve unrelated changes and scope; contradictions return to the earliest gate.

Implement the smallest coherent approved change. For `Run existing tests only`, run relevant existing behavioral tests without adding or modifying tests. Record actual commands and outcomes, including failures or unavailable coverage. An unresolved failure prevents an unqualified success claim. For `Skip behavioral tests` and legacy Approved direct Tickets without explicit existing-test permission, do not create, modify, or execute behavioral tests. Run relevant non-test validation such as syntax, lint, type, build, schema, and final-diff inspection. An external system's mandatory tests remain an explicit delivery constraint; do not silently run declined tests or claim a bypass.

Emit Direct Implementation Evidence with the common envelope, upstream artifacts/mode, changed areas, the Approved test choice, raw validation results, scope inspection, unavailable behavioral evidence/untested paths, external constraints, incomplete checks, and risks. Record `tests: skipped-by-user` only for the skip choice or legacy direct approvals. Report only observed existing-test outcomes; never claim TDD. Hand raw evidence and diff to Review.

