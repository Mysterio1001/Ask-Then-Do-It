# Ask Then Do It 1.2.0 Ticket 2 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `command-install-update-1-2-ticket-2-evidence`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Status: Completed

Inputs: Approved [1.2.0 Specification](../specs/command-install-update-1.2.0.md), Approved [Ticket Plan](../plans/command-install-update-1.2.0.md), Ticket 1 output, and Ticket 2 (approved `tdd` mode).

Assumptions: Pillow is available in the bundled runtime for asset processing and tests. The native Plugin validator's optional PyYAML dependency is unavailable in this environment.

Deferred: Localized install/update documentation, lockstep release versioning, final generated `1.2.0` packages/checksums, final release evidence, independent Review, and architecture diagnosis.

Handoff: Ticket 3 after Ticket 2 Review.

## Outcome

Produced the approved red seahorse-question-mark derivatives as transparent 512x512 and 1024x1024 PNG assets, declared the approved interface fields, and extended deterministic Codex source validation and packaging to include the assets without marketplace metadata.

## Changed files

- `adapters/codex/plugin/ask-then-do-it/assets/icon.png`
- `adapters/codex/plugin/ask-then-do-it/assets/logo.png`
- `adapters/codex/plugin/ask-then-do-it/.codex-plugin/plugin.json`
- `scripts/build_release.py`
- `tests/release/test_plugin_assets.py`
- `tests/release/test_codex_release.py`

## Source verification

The approved temporary source was verified before processing:

`C22CF733EBF01ECFEB9C5E9A29AC37496A8B78BBE09F22D5942EC31F0B374EBB`

It was `1024x956`, RGB, and was not copied into the repository.

## Red evidence

Command:

`C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest tests.release.test_plugin_assets`

Observed before production changes: `Ran 3 tests`; `FAILED (failures=2, errors=2)`. The expected failures were missing `assets/icon.png`, missing `assets/logo.png`, missing `brandColor`, and a builder package lookup error because the source inventory rejected/omitted the asset directory.

## Focused Green evidence

The same command after adding the assets, manifest fields, builder validation, and package inventory expectation observed: `Ran 3 tests`; `OK`.

## Refactor and broader verification

The source and package checks were kept in the existing release builder boundary. PNG headers are checked with the standard library; behavioral asset tests use Pillow for alpha/corner/content assertions.

Commands and observed results:

- `...python.exe -m unittest tests.release.test_plugin_assets tests.release.test_codex_release`: `Ran 7 tests`; `OK`.
- `...python.exe -m unittest tests.release.test_release_contract tests.release.test_codex_release tests.release.test_plugin_assets`: `Ran 16 tests`; `OK`.
- `git diff --check`: passed; Git reported only its normal LF/CRLF normalization warning.
- Visual inspection of generated light/dark composites: subject recognizable, centered, padded, and corners transparent.

Native Plugin validator attempt:

`...python.exe C:\Users\Ian\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py adapters/codex/plugin/ask-then-do-it`

Blocked before validation because the bundled runtime has no `yaml` module (`ModuleNotFoundError: No module named 'yaml'`).

## Residual risks

Native Plugin validation and final package equivalence remain pending the later release validation stage. The target Codex CLI and external marketplace behavior remain unavailable for live testing.
