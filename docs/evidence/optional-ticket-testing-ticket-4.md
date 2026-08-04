# Optional Ticket Testing Ticket 4 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `optional-ticket-testing-ticket-4-evidence`

Workflow ID: `optional-ticket-testing`

Core version: `1.1.0`

Status: Completed

Inputs: Approved [Optional Ticket Testing Specification](../specs/optional-ticket-testing.md), Approved [Ticket Plan](../plans/optional-ticket-testing.md), completed [Ticket 1 evidence](optional-ticket-testing-ticket-1.md), [Ticket 2 evidence](optional-ticket-testing-ticket-2.md), [Ticket 3 evidence](optional-ticket-testing-ticket-3.md), and Ticket 4.

Assumptions: Active Core, adapters, packages, documentation, and release evidence advance together to `1.1.0`. Historical `1.0.0` and `1.0.1` artifacts remain unchanged when they are not active release inputs.

Deferred: Installation, marketplace mutation, publication, upload, external hosting, external CI execution, and an independent reviewer.

Handoff: `$review-code` with the Approved artifacts, complete diff, generated `dist/`, and the raw results below.

## Outcome

The active release is now Ask Then Do It `1.1.0`. The Codex package exposes nine Skills including `$implement-direct`; the Generic package exposes ten prompt files including `direct-implementation.md`; localized documentation explains that all Tickets are listed before the user selects `tdd` or `direct`, warns that tests may increase work time, and preserves `tests: skipped-by-user` for the direct path. Both deterministic packages and their checksums were rebuilt without installation or publication.

## Changed areas

- Lockstep Core, adapter, Plugin, prompt, release, and active guide version declarations.
- Exact nine-Skill Codex and ten-prompt Generic inventories.
- Traditional Chinese, English, and Japanese root, Codex, Generic, beginner, and design guides.
- Release configuration, generated Codex and Generic directories, ZIP archives, and `dist/checksums.sha256`.
- Integrated release, documentation, inventory, reproducibility, ZIP parity, and skipped-test evidence tests.

## Red evidence

Command family: seven focused release modules covering clean-slate identity, Codex packaging, Generic packaging, documentation, release configuration, release evidence, and safe deterministic replacement:

`python -m unittest tests.release.test_clean_slate tests.release.test_codex_release tests.release.test_generic_release tests.release.test_documentation tests.release.test_release_contract tests.release.test_release_evidence tests.release.test_release_safety`

Observed before the Ticket 4 production and generated-output changes: 16 expected failures. Active Core, Plugin, and Generic prompt declarations still identified `1.0.1`; release configuration did not include the direct stages; root download documentation still linked `1.0.1`; and the existing release ledger and managed output inventory disagreed with the target `1.1.0` configuration.

## Focused Green evidence

PowerShell command:

`$env:PYTHONPATH='C:\Users\Ian\AppData\Local\Temp\codex-grill-me-pydeps'; & 'C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.release.test_clean_slate tests.release.test_codex_release tests.release.test_generic_release tests.release.test_documentation tests.release.test_release_contract tests.release.test_release_evidence tests.release.test_release_safety`

Observed after the minimum integrated changes and rebuilt outputs: `Ran 43 tests in 3.880s`; `OK`.

## Refactor and broader verification

The localized guides were refactored around one shared user-visible sequence: list Tickets, recommend tests and explain time/risk, collect one explicit mode per Ticket, approve the complete plan, route by mode, then Review. The root README was simplified into a Traditional-Chinese-first consumer entry with parallel English and Japanese guidance while retaining the required attribution and maintainer build command.

Full regression command:

`$env:PYTHONPATH='C:\Users\Ian\AppData\Local\Temp\codex-grill-me-pydeps'; & 'C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests`

Observed: `Ran 66 tests in 4.376s`; `OK`.

The first full run observed one documentation identity failure because the README rewrite omitted the required verbatim upstream attribution before the language entry links. The attribution was restored without weakening the test; a focused identity and documentation rerun observed `Ran 17 tests`; `OK`, followed by the successful 66-test result above.

Package build command:

`$env:PYTHONPATH='C:\Users\Ian\AppData\Local\Temp\codex-grill-me-pydeps'; & 'C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/build_release.py`

Observed: `Built codex, generic release 1.1.0 in C:\Users\Ian\Desktop\Grill Me\dist`.

Official validator loop observed:

- Canonical Plugin: `Plugin validation passed` and nine `Skill is valid!` results.
- Packaged Plugin: `Plugin validation passed` and nine `Skill is valid!` results.

The focused release suite also built two isolated complete releases and proved corresponding ZIPs and `checksums.sha256` byte-identical, proved both ZIPs equal their generated directories, verified exact inventories, and verified the two current SHA-256 entries:

- `b1d2aa0afb882c0a495cb2561cfd90226032681a4ef2708e69e3757fdcc37309  codex/ask-then-do-it-1.1.0.zip`
- `924392ed9b26d32d39c903db18d6f119e9b11b472d8db34c5308cb53a71ce42a  generic/ask-then-do-it-generic-1.1.0.zip`

## Approved Review-fix cycle

The first Final Review identified two P2 Specification gaps. The user explicitly approved returning Ticket 4 to `$implement-tdd` while keeping the broader conformance architecture proposals Draft.

Focused Red command:

`python -m unittest tests.conformance.test_validator.ConformanceValidatorTests.test_core_defines_user_selected_implementation_modes tests.codex.test_adapter.CodexAdapterTests.test_codex_routes_user_selected_tdd_and_direct_modes tests.generic.test_generic_prompts.GenericPromptScenarioTests.test_generic_routes_user_selected_tdd_and_direct_modes -v`

Observed before the Review-fix production changes: `Ran 3 tests`; `FAILED (failures=3)`. Core, Codex, and Generic all lacked the complete-before-selection clause, approved recommendation dimensions, external test-constraint disclosure, and prohibition on automatically prescribing declined tests.

Focused Green used the same three-test command and observed: `Ran 3 tests in 0.007s`; `OK`.

After rebuilding both packages, the full regression command first observed: `Ran 66 tests in 6.486s`; `OK`. After final evidence files were added, one later full run encountered a non-assertion Windows `WinError 5` while a temporary release directory was atomically replaced. The affected safety test passed immediately in isolation (`Ran 1 test`; `OK`), and the repeated complete suite observed `Ran 66 tests in 4.713s`; `OK`. Canonical and packaged Plugin validation passed again, with eighteen `Skill is valid!` results. `git diff --check` again reported no whitespace errors, only informational LF-to-CRLF checkout warnings.

## Test-first exceptions

None. Versioned documentation and generated packages were covered by failing release-contract tests before the production and output changes. No behavioral test was skipped for this `tdd` Ticket.

## Residual risks

- Verification was local on Windows; additional operating systems and external CI were not executed.
- Generic prompts cannot prove real file edits or command execution by conversation-only hosts; the package states this limitation.
- Plugin installation, marketplace behavior, publication URLs, and live third-party model behavior were intentionally not exercised.
- Final Review is necessarily non-independent in the current context; release architecture diagnosis remains read-only and pending.
