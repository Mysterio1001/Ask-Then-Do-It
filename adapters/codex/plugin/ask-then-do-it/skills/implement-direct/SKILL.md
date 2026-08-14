---
name: implement-direct
description: Implement an approved direct-mode Ticket without behavioral tests, while preserving scope, non-test validation, skipped-test disclosure, and Review handoff. Use only for a Ticket whose Approved Ticket Plan mode is direct. Do not use for tdd Tickets or before all applicable approval gates pass.
---

# Implement Direct

Implement one Approved `direct` Ticket without pretending that skipped tests passed.

<!-- Maintainer note: A distinct Skill keeps the user's time-risk choice visible instead of weakening TDD from inside the TDD path. -->

Match user-facing communication and generated artifacts to the user's language when discoverable.

## Verify readiness

1. Read repository instructions, the Approved Specification, the Approved Ticket Plan, and the selected Ticket.
2. Confirm the Ticket's Approved implementation mode is `direct`, its dependencies are complete, and it remains compatible with repository state.
3. Inspect relevant code, allowed non-test commands, and current changes.
4. Preserve unrelated user changes and stay inside the Ticket boundary.

If an artifact is missing, Draft, contradictory, no longer feasible, or does not prove `direct` mode, stop and return to the earliest affected gate. Never infer direct mode from silence or from another Ticket.

## Implement the approved behavior

- Make the smallest coherent production change that satisfies the Approved Ticket.
- Do not create, modify, or execute behavioral tests, including unit, integration, end-to-end, or equivalent executable behavior checks.
- Do not add speculative capabilities, unrelated cleanup, or unapproved behavior.
- Do not weaken an existing test or acceptance criterion merely because it was not executed.
- If an external CI, hosting, or release system independently requires or executes behavioral tests, disclose the constraint and any delivery block. The workflow must not claim that `direct` bypasses the external system, and must not silently run the declined tests itself.
- If implementation evidence contradicts an Approved artifact, stop and return to the earliest affected gate.

## Validate without behavioral tests

- Run lint, type-check, build, static validation, or equivalent non-behavioral checks when relevant and available.
- Capture every command and raw result actually observed.
- Inspect the final diff for scope drift, unintended generated files, and unrelated edits.
- Record behavioral tests and untested paths as unavailable evidence, not as passing checks.

## Report direct evidence

Emit Direct Implementation Evidence only for work actually performed with the `tools` profile. Include or unambiguously convey `artifact_type`, stable `artifact_id`, shared `workflow_id`, `core_version` `1.2.0`, evidence `status`, upstream `inputs`, `assumptions`, `deferred` work, and reviewer `handoff`.

Record the Ticket outcome, changed files or ownership areas, raw non-test commands and results, final-diff inspection, the exact disclosure `tests: skipped-by-user`, unavailable behavioral evidence, external test constraints or delivery blocks, incomplete checks, and residual risks. Do not use Red, Green, passing-test, test-verified, or TDD-complete claims.

Hand the Approved artifacts, selected Ticket, final diff, surrounding code, available validation results, and skipped-test disclosure to `$review-code`.
