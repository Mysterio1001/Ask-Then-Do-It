# Lite Workflow Mode 1.3.0 Ticket 3 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `lite-workflow-mode-1-3-ticket-3-evidence`

Workflow ID: `lite-workflow-mode`

Core version: `1.2.0`

Target release version: `1.3.0`

Status: Completed

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), Ticket 1 implementation and Review evidence, and Ticket 3 in approved `tdd` mode.

Assumptions: Ticket 1 established the provider-neutral mode and Lite contracts. Ticket 3 owns Generic prompt behavior and the composition header, while Ticket 7 owns the final `release/release.json` module inventory, release versions, generated packages, and checksums.

Deferred: Final Generic module inventory and `1.3.0` package integration; localized Generic documentation; deterministic token-proxy measurement; generated `dist/` output; external publication.

Handoff: `$review-code` with the approved artifacts, Ticket 3 prompt/composition/test diff, this evidence, and the raw results below. No Ticket 3 Review was performed during implementation.

## Outcome

- Added exactly one editable `Default workflow mode: full` declaration near the beginning of every composed Generic workflow.
- Added Generic resolution for explicit current-operation instruction, embedded declaration, then Full fallback; conflicting instructions require clarification and operation overrides do not persist.
- Preserved the existing Full stage order, approvals, artifact handling, Ticket `tdd`/`direct` routes, Review, and architecture routing.
- Added a dedicated conversation-only Lite module covering risk reconsideration, bounded questions, the Change Brief and approval, unexecuted implementation guidance, validation, compact Review, correction authority, completion, and session state.
- Kept Generic capability claims honest: no direct repository changes, command execution, durable persistence, observed validation without supplied evidence, or independent Review.
- Mapped all eight new mandatory rules in the Generic manifest with source and focused-test capability evidence.

## Files changed

- `adapters/generic-prompts/bootstrap.md`
- `adapters/generic-prompts/orchestration.md`
- `adapters/generic-prompts/lite-workflow.md`
- `adapters/generic-prompts/manifest.yaml`
- `scripts/build_release.py`
- `tests/generic/test_generic_prompts.py`
- `tests/generic/test_generic_lite_workflow.py`
- `docs/evidence/lite-workflow-mode-1.3.0-ticket-3.md`

## TDD evidence

### Setup attempts not accepted as Red

The first command used an unavailable global interpreter:

```text
python -m unittest tests.generic.test_generic_lite_workflow.GenericLiteCompositionTests.test_generated_workflow_has_one_early_full_default_declaration

CommandNotFoundException: python was not recognized as a command.
Exit code: 1
```

The repository-local interpreter then reached test import, but the initial direct package import did not expose the build script's sibling module:

```text
.venv\Scripts\python.exe -m unittest tests.generic.test_generic_lite_workflow.GenericLiteCompositionTests.test_generated_workflow_has_one_early_full_default_declaration

ModuleNotFoundError: No module named 'validate_marketplace'
Ran 1 test in 0.000s
FAILED (errors=1)
```

Neither setup failure was treated as Red. The test import was corrected before production implementation.

### Valid Red

Command:

```text
.venv\Scripts\python.exe -m unittest tests.generic.test_generic_lite_workflow.GenericLiteCompositionTests.test_generated_workflow_has_one_early_full_default_declaration
```

Observed result before production implementation:

```text
FAIL: test_generated_workflow_has_one_early_full_default_declaration
AssertionError: 0 != 1
Ran 1 test in 0.100s
FAILED (failures=1)
```

The failure was the approved missing behavior: the generated workflow contained zero exact `Default workflow mode: full` lines instead of one near its beginning. The test used an in-memory module inventory with `lite-workflow.md` immediately after `orchestration.md`; it did not modify the Ticket 7-owned release inventory.

### Initial Green attempt

After the production changes, the expanded focused suite found two prompt-searchability mismatches rather than behavioral omissions:

```text
FAIL: test_lite_reconsiders_material_risk_only_for_current_operation
FAIL: test_resolved_full_preserves_existing_order_gates_and_ticket_modes
Ran 14 tests in 0.014s
FAILED (failures=2)
```

The implementation wording was made directly traceable with a `Resolved Full` heading and the explicit phrase `before Change Brief approval`; no assertions or acceptance criteria were weakened.

### Focused Green

Command:

```text
.venv\Scripts\python.exe -m unittest tests.generic.test_generic_lite_workflow
```

Observed result:

```text
..............
Ran 14 tests in 0.014s
OK
```

### Post-refactor verification

The Change Brief budget was tightened to an explicit `MUST`, and the no-artifact statement received an explicit workflow subject. The focused suite was rerun:

```text
.venv\Scripts\python.exe -m unittest tests.generic.test_generic_lite_workflow

..............
Ran 14 tests in 0.017s
OK
```

No test-first exception was used.

## Broader verification

All Generic tests:

```text
.venv\Scripts\python.exe -m unittest discover -s tests/generic -t .

................................
Ran 32 tests in 0.624s
OK
```

Shared Generic conformance:

```text
.venv\Scripts\python.exe scripts\validate_conformance.py --catalog core\rules\rules.yaml --manifest adapters\generic-prompts\manifest.yaml

Conformance passed: generic-prompts against core 1.2.0
```

Relevant release composition checks:

```text
.venv\Scripts\python.exe -m unittest tests.release.test_generic_release

..
Ran 2 tests in 0.227s
OK
```

Python syntax check:

```text
.venv\Scripts\python.exe -m py_compile scripts\build_release.py tests\generic\test_generic_lite_workflow.py

Exit code: 0
```

Diff hygiene:

```text
git diff --check

Exit code: 0
```

Git reported only LF-to-CRLF checkout warnings. A separate trailing-whitespace scan of both new files returned no matches.

## Incomplete checks and residual risks

- `release/release.json` intentionally still omits `lite-workflow.md`; Ticket 7 must insert it immediately after `orchestration.md` and perform final `1.3.0` inventory/package/checksum integration. Until then, a build using the checked-in `1.2.0` inventory has the new header but not the Lite source section and is not a completed `1.3.0` deliverable.
- Generated `dist/` outputs were not modified or validated because they are owned by Ticket 7.
- Prompt contract and composition tests prove deterministic source content and ordering, but cannot guarantee that every downstream language model follows approximate 500/800/500-token budgets.
- Conversation-only Review quality remains limited to user-supplied diffs and validation evidence; the prompt explicitly labels unavailable evidence and prohibits independent-Review claims.
