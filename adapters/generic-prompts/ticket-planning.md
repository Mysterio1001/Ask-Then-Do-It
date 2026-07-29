# Generic Ticket Planning Prompt

Prompt ID: `generic.ticket-planning`
Prompt version: `1.0.0`
Required capability: `conversation`
Core version: `3.0.0`

## Required inputs

- An Approved Specification with explicit approval evidence.
- The workflow ID and relevant upstream artifact references.
- An existing Ticket Plan, when resuming.

## Expected outputs

- A vertically sliced Ticket Plan in complete Markdown with status `Draft`.
- One explicit Ticket Plan approval request.
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
- the smallest meaningful test-first approach;
- focused and broader verification;
- completion criteria;
- parallel-safety reasoning.

Include the artifact envelope: `artifact_type`, `artifact_id`, `workflow_id`, `core_version`, `status`, `inputs`, `assumptions`, `deferred`, `handoff`, and `approval`.

Emit the first Ticket Plan as `Draft` (`ART-STATE-001`) and ask for explicit human approval (`GATE-PLAN-001`). Only a direct approval of this plan counts. On a later turn, record the approval evidence and emit status `Approved`. A Draft, disputed, or unverifiably approved plan never authorizes implementation.

Whenever you emit the Ticket Plan, state: "The user owns cross-session persistence; save this artifact and re-supply it when the conversation no longer contains it."

## Stop conditions

- Stop at the Specification gate if status or approval evidence is missing.
- Stop and return to Specification authoring if a material behavior decision is missing or contradicted.
- Stop after emitting the Draft and requesting explicit approval.
- Stop after emitting the Approved artifact and identify the first eligible ticket; do not claim implementation has started.
