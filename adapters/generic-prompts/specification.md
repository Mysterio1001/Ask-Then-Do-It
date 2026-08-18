# Generic Specification Prompt

Prompt ID: `generic.specification`
Prompt version: `1.3.1`
Required capability: `conversation`
Core version: `1.3.1`

## Required inputs

- An Approved Requirement Decision Record, or equivalent confirmed decisions with explicit consensus evidence.
- The workflow ID and any compatible upstream artifact references.
- An existing Specification, when resuming.

## Expected outputs

- A behavioral Specification in complete Markdown with status `Draft`.
- One explicit Specification approval request.
- After explicit human approval, an `Approved` Specification containing the approval evidence.

## Instructions

Directly pasting this module selects its workflow stage, not Full or Lite. This is a bounded direct-entry guard, not complete resolver ownership. When composed orchestration supplies a proven current-operation mode, reuse it and MUST NOT re-resolve. Only when directly pasted without a proven current-operation mode, resolve (`MODE-RESOLVE-001`) in order: (1) an unambiguous explicit current-operation instruction selecting Full or Lite; (2) the embedded `Default workflow mode` declaration, when available, if exactly `full` or `lite`; (3) Full fallback for a missing or invalid declaration. If explicit current-operation instructions conflict, ask one clarification and stop. Any local result applies to only the current operation and MUST NOT persist. Continue this stage only when Full resolves. If Lite resolves, stop this Full stage and route to `lite-workflow.md`.

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
