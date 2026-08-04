# Ticket Plan Artifact

## Required content

- Link or reference to the approved Specification.
- Dependency order and proposed parallel groups.
- One or more vertically testable tickets.

Each Ticket includes outcome, acceptance criteria covered, scope, dependencies, ownership areas, completion criteria, parallel-safety reasoning, a risk-based test recommendation and reason, a test-time warning, and the verification approaches for adding or declining tests.

After all Ticket definitions and recommendations are visible, the workflow collects every plain-language test choice in one batch. It accepts tests for all Tickets, tests for no Tickets, or an explicit mixed selection. An incomplete mixed selection retains resolved choices and leaves only unresolved Tickets pending.

Every Ticket MUST record one plain-language test choice and its mapped internal implementation mode: adding tests maps to `tdd`, and declining tests maps to `direct`. There is no default. The plan cannot become Approved until every Ticket has both values, and one approval covers the complete Ticket definitions and displayed test choices.

Status starts as `Draft` and becomes `Approved` only with explicit approval evidence. Changing a test choice or mapped mode after approval returns the plan to Draft. The Approved artifact hands each eligible Ticket to its mapped implementation path.
