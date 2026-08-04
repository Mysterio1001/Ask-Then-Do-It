# Generic Ticket Planning Prompt

Prompt ID: `generic.ticket-planning`
Prompt version: `1.1.0`
Required capability: `conversation`
Core version: `1.1.0`

## Required inputs

- An Approved Specification with explicit approval evidence.
- The workflow ID and relevant upstream artifact references.
- An existing Ticket Plan, when resuming.

## Expected outputs

- A vertically sliced Ticket Plan in complete Markdown with status `Draft`.
- One batch request for every Ticket's plain-language add-tests or do-not-add-tests choice.
- After all test choices are resolved and mapped internally, one explicit Ticket Plan approval request displaying the complete selected plan.
- After explicit human approval, an `Approved` Ticket Plan containing approval evidence.

## Instructions

Match the user's language. Verify that the supplied Specification is Approved and has approval evidence. If planning exposes new or contradictory product behavior, return to Specification authoring instead of silently changing intent.

Split work into vertically testable behavior, not horizontal technical layers (`PLAN-VERTICAL-001`). Keep shared enabling work minimal and name its first behavioral consumer. State dependency order and proposed parallel groups; uncertain parallel safety defaults to sequential execution.

For every ticket define:

- outcome;
- covered Specification acceptance criteria;
- in-scope and out-of-scope behavior;
- dependencies;
- likely ownership areas;
- a TDD approach with the smallest meaningful first failing test, focused Green, and broader verification;
- a direct approach with permitted non-test validation and unavailable behavioral evidence;
- completion criteria;
- parallel-safety reasoning.

Include the artifact envelope: `artifact_type`, `artifact_id`, `workflow_id`, `core_version`, `status`, `inputs`, `assumptions`, `deferred`, `handoff`, and `approval`.

Present the complete Ticket definitions and all recommendations before requesting one batch test choice. Give every Ticket a risk-based test recommendation and a scope-specific reason. Use available evidence about correctness, regression, security, privacy, migration, integration, destructive behavior, and release risk; state when relevant evidence is unavailable. For every Ticket, warn that tests may increase work time and that skipping them lowers behavioral verification confidence.

Ask in the user's language whether tests should be added, and collect all Ticket choices in one response. Do not present `tdd` and `direct` as the initial user-facing options. Accept `Add tests to all Tickets`, `Do not add tests to all Tickets`, or an explicit mixed selection such as adding tests to named Tickets and declining them for the rest. Retain choices from an incomplete mixed selection and ask only about unresolved Tickets. There is no default; never infer an unresolved test choice from risk, repository conventions, another Ticket, prior history, or silence. For every resolved Ticket, map `Add tests` to internal mode `tdd` and map `Do not add tests` to internal mode `direct`.

Emit the first Ticket Plan as `Draft` (`ART-STATE-001`). A plan with any unresolved test choice or missing mapped mode must remain `Draft`. After all choices are resolved, display the complete Ticket definitions and plain-language test choices; internal modes may also appear for traceability. Ask for explicit human approval (`GATE-PLAN-001`). Only a direct approval of that selected plan counts. On a later turn, record approval evidence and emit status `Approved`. Changing a test choice or mapped mode after approval returns the plan to `Draft` and requires reapproval before affected implementation continues.

Whenever you emit the Ticket Plan, state: "The user owns cross-session persistence; save this artifact and re-supply it when the conversation no longer contains it."

## Stop conditions

- Stop at the Specification gate if status or approval evidence is missing.
- Stop and return to Specification authoring if a material behavior decision is missing or contradicted.
- Stop after emitting the Draft and requesting the batch test choices or only the unresolved choices.
- Stop after presenting the complete selected Draft and requesting explicit approval.
- Stop after emitting the Approved artifact and identify the first eligible ticket; do not claim implementation has started.
