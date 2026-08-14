# Ask Then Do It 1.2.0 Ticket 1 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `command-install-update-1-2-ticket-1-evidence`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Status: Completed

Inputs: Approved [1.2.0 Specification](../specs/command-install-update-1.2.0.md), Approved [Ticket Plan](../plans/command-install-update-1.2.0.md), and Ticket 1 (approved `tdd` mode).

Assumptions: The repository marketplace contract is validated statically in this Ticket; live `codex.exe` marketplace operations remain unavailable in the current environment.

Deferred: Plugin assets and manifest, localized installation documentation, lockstep release versioning, generated packages, final release evidence, independent Review, and architecture diagnosis.

Handoff: Ticket 2 after Ticket 1 Review.

## Outcome

Added the repository marketplace catalog with exactly one official `ask-then-do-it` Plugin entry, using the approved GitHub `git-subdir` source and immutable `v1.2.0` tag.

## Changed files

- `.agents/plugins/marketplace.json`
- `scripts/validate_marketplace.py`
- `tests/release/test_marketplace_contract.py`

## Red evidence

Command:

`C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest tests.release.test_marketplace_contract`

Observed before the catalog was added: `Ran 2 tests`; `FAILED (failures=1)`. The expected failure was `missing marketplace catalog: C:\Users\Ian\Desktop\Grill Me\.agents\plugins\marketplace.json`.

After adding the catalog, the validator extension was established with:

`C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest tests.release.test_marketplace_contract`

Observed before adding the validator: `Ran 4 tests`; `FAILED (failures=1)` because `scripts/validate_marketplace.py` did not exist. The six mutation cases were therefore unable to pass validation, as expected for the missing behavior.

## Focused Green evidence

The focused command after adding the validator observed: `Ran 4 tests`; `OK`. It covers the official catalog plus mutable ref, alternate URL, wrong source type, wrong path, wrong policy, and duplicate-entry mutations.

`C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/validate_marketplace.py` observed: `Marketplace validation passed`.

## Refactor and broader verification

No refactor was needed; the catalog and test remain minimal and ownership is isolated to repository metadata.

`C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest tests.release.test_release_contract tests.release.test_marketplace_contract` observed: `Ran 13 tests`; `OK`.

`git diff --check` passed with no whitespace errors.

## Residual risks

The target Codex CLI could not be executed in this environment, so live marketplace parsing and installation are not observed. Ticket 4 owns integration of the catalog into release consistency gates, and Ticket 5 owns full validation.
