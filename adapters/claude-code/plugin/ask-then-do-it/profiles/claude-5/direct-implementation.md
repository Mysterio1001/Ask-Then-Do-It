# Claude 5 Direct Implementation

Core rules: FULL-PRESERVE-001, CAP-CLAIM-001

Require tools capability, Approved Specification and Ticket Plan, completed dependencies, and one eligible Ticket whose Approved mode is `direct`. Preserve unrelated changes and scope; contradictions return to the earliest gate.

Implement the smallest coherent approved change. Do not create, modify, or execute behavioral tests. Run relevant non-test validation such as syntax, lint, type, build, schema, and final-diff inspection. An external system's mandatory tests remain an explicit delivery constraint; do not silently run declined tests or claim a bypass.

Emit Direct Implementation Evidence with the common envelope, upstream artifacts/mode, changed areas, raw non-test validation, scope inspection, `tests: skipped-by-user`, unavailable behavioral evidence/untested paths, external constraints, incomplete checks, and risks. Never claim Red/Green, passing tests, or TDD completion. Hand raw evidence and diff to Review.

