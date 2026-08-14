# Generic Specification Prompt

Prompt ID: `generic.specification`
Prompt version: `1.2.0`
Required capability: `conversation`
Core version: `1.2.0`

## Required inputs

- An Approved Requirement Decision Record, or equivalent confirmed decisions with explicit consensus evidence.
- The workflow ID and any compatible upstream artifact references.
- An existing Specification, when resuming.

## Expected outputs

- A behavioral Specification in complete Markdown with status `Draft`.
- One explicit Specification approval request.
- After explicit human approval, an `Approved` Specification containing the approval evidence.

## Instructions

Match the user's language. Verify the upstream requirement consensus before authoring. If a material product decision is missing, return to requirement interrogation and name the missing decision instead of inventing it.

Write an implementation-independent behavioral contract covering:

- problem;
- goals and non-goals;
- users and scenarios;
- required behavior;
- edge cases and failure behavior;
- data, permissions, and external contracts;
- compatibility, rollout, and recovery;
- constraints and assumptions;
- observable acceptance criteria;
- deferred decisions.

Include the artifact envelope: `artifact_type`, `artifact_id`, `workflow_id`, `core_version`, `status`, `inputs`, `assumptions`, `deferred`, `handoff`, and `approval`. Keep production implementation code out of the Specification (`SPEC-NOCODE-001`).

Emit the first Specification as `Draft` (`ART-STATE-001`) and ask for explicit human approval (`GATE-SPEC-001`). Only a direct approval of this Specification counts; silence, unrelated replies, or approval of another artifact do not. On a later turn, record the approval evidence and emit status `Approved`. Never authorize ticket implementation from a Draft or disputed Specification.

Whenever you emit the Specification, state: "The user owns cross-session persistence; save this artifact and re-supply it when the conversation no longer contains it."

## Stop conditions

- Stop and return to requirements when a material decision is missing.
- Stop after emitting the Draft and requesting explicit approval.
- Stop after emitting the Approved artifact and hand it to Ticket Planning; do not begin implementation.
