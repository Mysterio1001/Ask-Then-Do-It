# Claude 5 TDD Implementation

Core rules: TDD-RED-001, CAP-CLAIM-001

Require tools capability, approved upstream artifacts, completed dependencies, and one eligible Ticket whose Approved mode is `tdd`. Preserve unrelated changes and ticket scope; contradictions return to the earliest gate.

Add or identify the smallest meaningful test. Observe the expected Red before production changes; a passing test requires investigation, and unrelated/setup failure is not valid Red. Make the smallest coherent change to Reach Green. Refactor without behavior change, rerun focused tests, then run proportional broader checks and inspect the final diff. Never weaken a test or acceptance criterion.

Declare before editing when automated Red is not meaningful and name the alternative check. Record the common evidence envelope, upstream inputs, mode, changed files, raw Red/Green/refactor/broader results, exceptions, incomplete checks, and risks in Implementation Evidence. Do not mark complete while required checks fail; hand raw artifacts and diff to Review.

