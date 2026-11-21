---
name: implement-direct
description: Implement an approved direct-mode Ticket with its approved choice to run existing tests only or skip behavioral tests. Use only for a Ticket whose Approved Ticket Plan mode is direct. Do not use for tdd Tickets or before all applicable approval gates pass.
---

# Implement Direct

Implement one Approved `direct` Ticket using its approved test choice.

<!-- Maintainer note: A distinct Skill keeps the user's time-risk choice visible instead of weakening TDD from inside the TDD path. -->

Match user-facing communication and generated artifacts to the user's language when discoverable.

## Resolve the top-level mode before this stage

Direct selection of this Skill chooses this Full-workflow stage, not top-level `full`. Before stage behavior, require a current-operation mode proof from `$ask-then-do-it`; never persist or reuse mode.

- Missing proof: stop and delegate to `$ask-then-do-it`.
- Proven `lite`: stop this Full stage and route to the Lite workflow.
- Proven `full`: continue with this stage's prerequisites and gates.

## Verify readiness

1. Read repository instructions, the Approved Specification, the Approved Ticket Plan, and the selected Ticket.
2. Confirm the Ticket's Approved implementation mode is `direct`, its dependencies are complete, and it remains compatible with repository state.
3. Inspect relevant code, authorized checks, and current changes.
4. Preserve unrelated user changes and stay inside the Ticket boundary.

If an artifact is missing, Draft, contradictory, no longer feasible, or does not prove `direct` mode, stop and return to the earliest affected gate. Never infer direct mode from silence or from another Ticket.

## Implement the approved behavior

- Make the smallest coherent production change that satisfies the Approved Ticket.
- For `Run existing tests only`, run relevant existing behavioral tests without adding or modifying tests. Record actual commands and outcomes, including failures or unavailable coverage. An unresolved failure prevents an unqualified success claim.
- For `Skip behavioral tests` and legacy Approved direct Tickets without explicit existing-test permission, skip all behavioral tests.
- Do not add speculative capabilities, unrelated cleanup, or unapproved behavior.
- Do not weaken an existing test or acceptance criterion merely because it was not executed.
- If an external CI, hosting, or release system independently requires or executes behavioral tests, disclose the constraint and any delivery block. The workflow must not claim that `direct` bypasses the external system, and must not silently run the declined tests itself.
- If implementation evidence contradicts an Approved artifact, stop and return to the earliest affected gate.

## Validate the approved change

- Run lint, type-check, build, static validation, or equivalent non-behavioral checks when relevant and available.
- Capture every command and raw result actually observed.
- Inspect the final diff for scope drift, unintended generated files, and unrelated edits.
- Record untested paths and unavailable checks.

## Use the portable artifact contract

Before creating or emitting Direct Implementation Evidence, read the [portable artifact contract](../ask-then-do-it/references/artifact-contract.md) completely. If it is missing or unreadable, stop before artifact creation and leave the handoff pending.

## Report direct evidence

Emit Direct Implementation Evidence only for work actually performed with the `tools` profile. Use the portable artifact contract for the common envelope and preserve the evidence boundary below.

Record the Ticket outcome, changed files or ownership areas, the Approved test choice, raw commands and results, final-diff inspection, external constraints, incomplete checks, and residual risks. Record `tests: skipped-by-user` only for the skip choice or legacy direct approvals. Report only observed existing-test outcomes; never claim TDD.

Hand the Approved artifacts, selected Ticket, final diff, surrounding code, approved test choice and available validation results to `$review-code`.
