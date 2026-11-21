# Direct Implementation

## Purpose

Implement one approved `direct` Ticket using its approved test choice without adding or changing behavioral tests.

## Capability requirement

Formal completion requires `tools`. A `conversation` host MAY provide explicitly unexecuted direct implementation guidance but MUST NOT claim edits, command execution, persistence, or completed Direct Implementation Evidence.

## Contract

- Require an Approved Specification, an Approved Ticket Plan, completed dependencies, and an eligible Ticket whose Approved implementation mode is `direct`.
- Read applicable repository instructions, relevant code, current changes, and approved boundaries before editing.
- Preserve unrelated user changes and implement only the approved Ticket behavior.
- For `Run existing tests only`, run relevant existing behavioral tests without adding or editing tests. Record each command and outcome, including failures and unavailable coverage. An unresolved failure prevents an unqualified success claim.
- For `Skip behavioral tests` and previously Approved `direct` Tickets without explicit authority to run existing tests, MUST NOT create, modify, or execute behavioral tests. Record `tests: skipped-by-user`.
- MAY run lint, type-check, build, static validation, or equivalent non-behavioral checks when supported by the host.
- If an external CI, hosting, or release system independently requires or executes behavioral tests, disclose that constraint and any delivery block. The workflow MUST NOT claim that `direct` bypasses the external system, and MUST NOT silently run the declined tests itself.
- Inspect the final change for scope drift and unintended files.
- Record changed areas, the approved test choice, observed command results, unavailable behavioral evidence, residual risks, and the Ticket outcome in Direct Implementation Evidence.
- Report passing results only for specific existing tests actually observed. Never claim TDD completion.
- Hand the approved artifacts, selected Ticket, final diff or supplied change evidence, available validation results, and the Approved test choice with its outcomes to Review.
- If implementation evidence contradicts an approved artifact, return to the earliest affected gate rather than redefining the requirement.
