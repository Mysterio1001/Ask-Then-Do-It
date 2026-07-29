# Implementation Evidence - v2 Ticket 2

Artifact type: Implementation Evidence

Artifact ID: `v2-ticket-2`

Workflow ID: `portable-ai-development-v2`

Core version: `2.0.0`

Status: Completed

## Inputs

- Approved v2 Specification.
- Approved v2 Plan, Ticket 2.
- Frozen core `2.0.0` contract from Ticket 1.

## Outcome

Delivered a provider-neutral generic prompt adapter with one bootstrap prompt, six independently usable workflow prompts, a Conversation-only capability declaration, explicit artifact handoff behavior, and safe stops for execution or review claims that the adapter cannot substantiate.

## Expected red evidence

Command:

`python -m unittest discover -s tests/generic -p test_generic_prompts.py`

Observed result before implementation:

- 11 tests ran.
- 2 tests failed and 9 errored.
- Required prompt files such as `adapters/generic-prompts/bootstrap.md` did not exist.

The failures matched the planned absent adapter behavior.

## Focused green evidence

The same command completed with:

- 11 tests run.
- 11 tests passed.

The cases cover prompt inventory and headers, English provider-neutral sources, manifest coverage, default capability selection, resumed artifact import, one-question grilling, approval gates, user-managed persistence, unexecuted implementation guidance, and limited non-independent review.

## Broader verification

Command:

`python scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest adapters/generic-prompts/manifest.yaml`

Observed result:

`Conformance passed: generic-prompts against core 2.0.0`

Manual source inspection confirmed that every prompt:

- matches user-facing output to the user's language;
- declares its required inputs, expected outputs, capability, version, and stop conditions;
- avoids provider-specific names, paths, invocation syntax, and metadata;
- prevents fabricated repository changes, test execution, persistence, completed TDD, or reviewer independence.

## Changed areas

- `adapters/generic-prompts/`
- `tests/generic/`

## Refactoring

Repeated prompt interface fields and capability boundaries use consistent headings and terminology across all seven prompt files. No behavior-changing refactor was required after the focused suite became green.

## Exceptions

Prompt behavior cannot be proven completely through static tests. Contract checks and source inspection are supplemented by the fresh-context forward tests in Ticket 5.

## Residual risks

- Output quality still varies by the model receiving the prompts.
- Conversation mode relies on the user to save and re-supply artifacts across sessions.
- Static phrase checks establish declared behavior but cannot guarantee that every external model follows the prompts perfectly.

## Handoff

Ticket 4 may document the generic adapter after Ticket 3 establishes the final Codex adapter paths. Ticket 5 must forward-test representative generic scenarios from fresh context.
