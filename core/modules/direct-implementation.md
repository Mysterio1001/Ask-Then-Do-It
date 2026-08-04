# Direct Implementation

## Purpose

Implement one approved `direct` Ticket without behavioral tests while preserving honest evidence about what was and was not verified.

## Capability requirement

Formal completion requires `tools`. A `conversation` host MAY provide explicitly unexecuted direct implementation guidance but MUST NOT claim edits, command execution, persistence, or completed Direct Implementation Evidence.

## Contract

- Require an Approved Specification, an Approved Ticket Plan, completed dependencies, and an eligible Ticket whose Approved implementation mode is `direct`.
- Read applicable repository instructions, relevant code, current changes, and approved boundaries before editing.
- Preserve unrelated user changes and implement only the approved Ticket behavior.
- MUST NOT create, modify, or execute behavioral tests, including unit, integration, end-to-end, or equivalent executable behavior checks.
- MAY run lint, type-check, build, static validation, or equivalent non-behavioral checks when supported by the host.
- If an external CI, hosting, or release system independently requires or executes behavioral tests, disclose that constraint and any delivery block. The workflow MUST NOT claim that `direct` bypasses the external system, and MUST NOT silently run the declined tests itself.
- Inspect the final change for scope drift and unintended files.
- Record changed areas, raw non-test commands and results, `tests: skipped-by-user`, unavailable behavioral evidence, residual risks, and the Ticket outcome in Direct Implementation Evidence.
- MUST NOT use Red, Green, passing-test, test-verified, or TDD-complete claims.
- Hand the approved artifacts, selected Ticket, final diff or supplied change evidence, available validation results, and skipped-test disclosure to Review.
- If implementation evidence contradicts an approved artifact, return to the earliest affected gate rather than redefining the requirement.
