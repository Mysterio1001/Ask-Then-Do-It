# Ticket Planning

## Purpose

Turn an approved Specification into small, dependency-aware slices that each deliver verifiable behavior.

## Contract

- Require a relevant approved Specification.
- Return to specification when planning requires new behavior or contradicts approved intent.
- Split work vertically across all necessary layers (`PLAN-VERTICAL-001`).
- Each ticket MUST define outcome, covered acceptance criteria, scope, dependencies, likely ownership areas, completion criteria, parallel-safety reasoning, and the verification approaches for adding tests, running existing tests only, or skipping behavioral tests.
- Shared enabling work SHOULD remain minimal and name its first behavioral consumer.
- Uncertain parallel safety MUST default to sequential execution.
- Emit or persist the first plan as `Draft` (`ART-STATE-001`).
- Present the complete Ticket definitions and all recommendations before requesting one batch test choice.
- Present a risk-based test recommendation and scope-specific reason for every Ticket. Use available evidence about correctness, regression, security, privacy, migration, integration, destructive behavior, and release risk; state when relevant evidence is unavailable.
- For every Ticket, warn that tests may increase work time and that skipping them lowers behavioral verification confidence.
- Request all per-Ticket choices in one batch using plain-language meanings equivalent to `Add tests`, `Run existing tests only`, and `Skip behavioral tests` in the user's language. Do not ask the user to choose between `tdd` and `direct` as the initial decision.
- Accept any one of the three choices for all Tickets, or an explicit mixed selection that resolves every Ticket.
- Retain resolved choices from an incomplete mixed selection and ask only about unresolved Tickets. There is no default; do not infer an unresolved choice from risk, repository conventions, another Ticket, prior history, or silence.
- For every resolved Ticket, map `Add tests` to internal mode `tdd` and both `Run existing tests only` and `Skip behavioral tests` to `direct`. Preserve the explicit choice in the Approved Ticket. A new answer that only says “do not add tests” leaves execution unresolved; ask whether to run existing tests or skip them. Previously Approved `direct` Tickets without explicit existing-test authority keep their original skip behavior.
- The Ticket Plan MUST NOT become `Approved` while any Ticket lacks an explicit plain-language test choice or mapped internal mode.
- Present the complete Ticket list and selected test choices, optionally including mapped internal modes for traceability, then require one explicit human approval (`GATE-PLAN-001`).
- Changing a selected test choice or mapped mode after approval MUST return the plan to `Draft` and require reapproval before affected implementation continues.
- Do not authorize implementation while the Ticket Plan remains Draft or disputed.
