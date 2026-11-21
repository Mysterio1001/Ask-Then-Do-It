# Claude 5 Ticket Planning

Core rules: GATE-PLAN-001, PLAN-VERTICAL-001, ART-STATE-001

Require a relevant Approved Specification with approval evidence. New or contradictory behavior returns to Specification.

Plan vertical behavior slices. Each Ticket states outcome, covered acceptance criteria, scope/non-scope, dependencies, ownership, completion, parallel-safety reasoning, a TDD path (first meaningful Red, focused Green, broader checks), and a direct path (relevant existing tests, static checks and missing coverage). Keep shared enabling work minimal and name its first consumer; uncertain parallel safety is sequential.

Show every Ticket and a risk-based test recommendation/reason, including the time cost and confidence cost of skipping tests. Then request all choices in one plain-language batch and offer `Add tests`, `Run existing tests only`, or `Skip behavioral tests`. Map `Add tests` to `tdd`. Both existing-only and skip use `direct`; preserve the approved choice. For a new answer that only declines adding tests, clarify execution. Legacy Approved direct Tickets without explicit permission to run existing tests keep their skip behavior. Retain partial choices and ask only about unresolved Tickets.

The plan remains Draft until every Ticket has a choice and mapped mode. Redisplay the complete selected plan and require explicit approval. Only then record approval and mark it Approved. Any later test choice or mode change returns it to Draft. Hand off the first eligible Ticket to its Approved path; do not start implementation here.
