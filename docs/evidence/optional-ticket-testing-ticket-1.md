# Optional Ticket Testing Ticket 1 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `optional-ticket-testing-ticket-1-evidence`

Workflow ID: `optional-ticket-testing`

Core version: `1.0.1`

Status: Completed

Inputs: Approved [Optional Ticket Testing Specification](../specs/optional-ticket-testing.md), Approved [Ticket Plan](../plans/optional-ticket-testing.md), and Ticket 1.

Assumptions: `automated-tests` is the release ledger's behavioral-test check. Other required release checks remain non-skippable validations unless a later Approved Specification changes their meaning.

Deferred: Codex and Generic adapter implementations, active `1.1.0` versioning and packages, final release evidence, architecture diagnosis, and final Review.

Handoff: Ticket 2, the Codex `$implement-direct` path.

## Outcome

Core now requires an explicit user-selected `tdd` or `direct` mode for every Ticket before plan approval, routes only from the Approved mode, defines direct implementation and evidence contracts, preserves skipped-test disclosure through Review, and returns architecture work through the plan-selected implementation path. The release-evidence validator accepts `automated-tests: skipped-by-user` only with reason, approval metadata, and matching human-readable disclosure; other failed, blocked, or skipped required checks remain rejected.

## Changed areas

- Core index, Ticket Planning, orchestration, TDD, direct implementation, Review, and architecture contracts.
- Ticket Plan, TDD evidence, direct evidence, Review Report, adapter manifest, and mandatory rule semantics.
- Shared release-evidence validation.
- Core conformance and release-evidence regression tests.

## Red evidence

The first attempted command using `python` did not execute because no Python executable was on `PATH`; it is recorded as an environment setup failure and is not treated as Red. The bundled Python initially lacked PyYAML, so PyYAML `6.0.2` was installed to a temporary non-project directory and the valid Red command was rerun with that dependency available.

Command:

`python -m unittest tests.conformance.test_validator.ConformanceValidatorTests.test_core_defines_user_selected_implementation_modes tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_user_may_skip_automated_tests_with_explicit_evidence tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_user_skip_does_not_apply_to_non_test_release_checks tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_skipped_tests_require_approval_metadata -v`

Observed before production changes: `Ran 4 tests`; `FAILED (failures=3)`. Core lacked the risk recommendation and mode contract. The release validator rejected `automated-tests: skipped-by-user` as not passed and therefore could not validate its approval metadata. The negative test proving a non-test release check cannot be skipped already passed.

## Focused Green evidence

The same four-test command observed: `Ran 4 tests`; `OK`.

## Refactor and broader verification

Command:

`python -m unittest tests.conformance.test_validator tests.release.test_release_evidence -v`

The first broader run observed `Ran 18 tests` with one failure because an older architecture assertion still required every accepted proposal to enter `TDD`. That assertion contradicted the Approved plan-selected implementation behavior and was revised to assert the new contract rather than weakening coverage. The repeated command observed `Ran 18 tests`; `OK`.

Commands:

- `python scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest adapters/codex/conformance.yaml`
- `python scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest adapters/generic-prompts/manifest.yaml`
- `git diff --check`

Observed:

- `Conformance passed: codex against core 1.0.1`.
- `Conformance passed: generic-prompts against core 1.0.1`.
- `git diff --check` reported no whitespace error; Git only warned that its configured checkout may later normalize LF to CRLF.

## Residual risks

- Core behavior is not yet exposed by either adapter; Tickets 2 and 3 own those paths.
- The active release remains `1.0.1`; Ticket 4 owns lockstep `1.1.0` versioning and package evidence.
- Review independence and final release architecture diagnosis remain pending.
