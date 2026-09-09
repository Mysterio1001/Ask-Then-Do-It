# Claude Code General profile Ticket Planning

This General profile Full-stage module requires a proven `full` mode and an Approved Specification with approval evidence. Return to Specification when planning exposes new or contradictory product behavior.

Core rules: GATE-PLAN-001, PLAN-VERTICAL-001

Split work into vertically testable behavior, not horizontal technical layers. Each Ticket defines outcome, acceptance coverage, in/out scope, dependencies, likely ownership, completion, parallel safety, a TDD approach, and a direct approach. Keep shared enabling work minimal and name its first consumer. Uncertain parallel safety is sequential.

Use the `portable artifact envelope` defined in `orchestration.md` and emit the first complete Ticket Plan as `Draft`. Present every Ticket and its risk-based recommendation before asking in one batch for all plain-language `Add tests` or `Do not add tests` choices; explain that adding tests costs time and declining lowers verification confidence. Do not initially ask the user to choose `tdd`/`direct`, and never infer a missing choice. Map Add tests to `tdd` and Do not add tests to `direct` only after the user's choice.

After every choice is resolved, display the full selected plan and ask for explicit human approval. Missing choices keep the plan Draft. Only direct approval changes it to Approved. A later choice/mode change returns it to Draft and blocks affected implementation until reapproved.

[CORE: PLAN-VERTICAL-001]
[CORE: GATE-PLAN-001]
[SCENARIO: FULL-PLAN]
