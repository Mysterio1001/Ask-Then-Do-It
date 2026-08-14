---
name: implement-tdd
description: Implement an approved software ticket with red-green-refactor evidence, scope control, and proportional verification. Use when the user asks to implement a ticket or behavior backed by an approved specification and plan, or explicitly requests test-driven implementation. Do not use before the relevant requirement, specification, and ticket-plan gates have passed.
---

# Implement TDD

Implement one Approved `tdd` Ticket at a time. Use executable tests to prevent the implementation from redefining the intended behavior.

<!-- Maintainer note: Observing the expected red state proves the test can detect the missing behavior instead of merely agreeing with existing code. -->

Match user-facing communication and generated artifacts to the user's language when discoverable.

## Verify readiness

1. Read repository instructions, the Approved Specification, the Approved Ticket Plan, and the selected Ticket.
2. Confirm the selected Ticket has Approved mode `tdd`. Never infer TDD mode from risk, repository conventions, or another Ticket.
3. Inspect relevant code, tests, commands, and current changes.
4. Confirm dependencies are complete and the Ticket remains compatible with repository state.
5. Preserve unrelated user changes and stay inside the Ticket boundary.

If an artifact is missing, Draft, contradictory, no longer feasible, or does not prove an Approved `tdd` Ticket, stop and return to the earliest affected workflow gate.

## Establish red

- Translate the ticket's approved behavior into the smallest meaningful automated test at a public or stable boundary.
- Add or identify that test before production implementation.
- Run it and capture that it fails for the expected missing-behavior reason.
- If it passes immediately, investigate whether the behavior already exists or the test is too weak. Do not manufacture a failure or proceed without evidence.
- If it fails for setup or an unrelated defect, repair the test environment or report the blocker before implementation.

## Reach green

- Make the smallest coherent production change that satisfies the failing test.
- Do not add speculative capabilities, unrelated cleanup, or unapproved behavior.
- Run the focused test until it passes.
- Do not weaken assertions, rewrite acceptance criteria, or encode the incorrect implementation into the test.

## Refactor and verify

1. Improve names, duplication, boundaries, or structure without changing behavior.
2. Rerun the focused test after refactoring.
3. Run broader relevant unit, integration, type, lint, build, or end-to-end checks in proportion to risk.
4. Inspect the final diff for scope drift and unintended generated files.

## Handle justified exceptions

Use a test-first exception only for documentation, formatting, generated output, or a change with no reasonable automated-test surface. Before editing, state why an automated failing test is not meaningful and name the alternative verification method. Perform and report that verification.

## Coordinate safe parallel tickets

Use parallel agents only when the approved plan marks the tickets safe, contracts are settled, ownership does not overlap, and the runtime permits delegation. Give each agent only its ticket, relevant spec sections, instructions, and ownership boundary. Otherwise work sequentially. Integrate centrally and rerun combined checks.

## Report evidence

Emit Implementation Evidence only for work actually performed with the `tools` profile. Include or unambiguously convey `artifact_type`, stable `artifact_id`, shared `workflow_id`, `core_version` `1.2.0`, evidence `status`, upstream `inputs`, `assumptions`, `deferred` work, and reviewer `handoff`.

Record the ticket outcome, files changed, raw commands and raw results for the observed red failure, focused green, post-refactor verification, and broader checks. Include any test-first exception rationale and alternative verification, incomplete checks, and residual risks. Do not set a completed status while a required check fails or is blocked. After all eligible tickets complete, hand the approved artifacts, final diff, surrounding code, test changes, and raw results to `$review-code`.
