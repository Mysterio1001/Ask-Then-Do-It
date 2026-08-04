# Optional Ticket Testing Ticket 6 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `optional-ticket-testing-ticket-6-evidence`

Workflow ID: `optional-ticket-testing`

Core version: `1.1.0`

Status: Completed

Inputs: Approved [Optional Ticket Testing Specification](../specs/optional-ticket-testing.md), Approved [Ticket Plan](../plans/optional-ticket-testing.md), completed [Ticket 5 evidence](optional-ticket-testing-ticket-5.md), and Ticket 6.

Assumptions: All Traditional Chinese, English, and Japanese user documents must explain the same batch add-tests choice. Internal `tdd` and `direct` names may be explained only after the plain-language decision and remain stable routing values.

Deferred: Installation, marketplace mutation, publication, upload, external CI and hosting execution, additional operating systems, and live third-party model behavior.

Handoff: Completed [Independent Ticket 6 Review](optional-ticket-testing-ticket-6-review.md), then maintainer-controlled inspection and any separate installation or publication decision.

## Outcome

All nine localized `START-HERE` files and all 22 user-facing README, guide, design, release, and adapter documents now show the same sequence: complete Ticket recommendations and per-Ticket time/risk warnings, then one response deciding whether to add tests to all Tickets, none, or an explicit subset. The initial question does not require knowledge of `tdd` or `direct`; later explanatory text maps the plain-language choices to those stable internal paths.

The Codex and Generic `1.1.0` packages were rebuilt from these sources with new verified checksums.

## Changed areas

- Root `README.md` and three root `START-HERE` files.
- Three Codex Plugin and three Generic release `START-HERE` files.
- Traditional Chinese, English, and Japanese Codex, Generic, beginner, and design guides.
- Documentation assertions covering every localized flow document and all nine start pages.
- Deterministic Codex and Generic managed outputs and `dist/checksums.sha256`.
- Current `1.1.0` release ledger and evidence, after final Review.

## Red evidence

Focused command:

`python -m unittest tests.release.test_documentation.ReleaseDocumentationTests.test_all_nine_start_pages_use_plain_language_batch_test_choices tests.release.test_documentation.ReleaseDocumentationTests.test_all_localized_flow_documents_avoid_mode_jargon_as_the_choice -v`

Observed before documentation changes: `Ran 2 tests`; `FAILED (failures=69)` across subtests. The failures identified missing localized batch/add-tests phrases and legacy user-facing `tdd`/`direct` choice wording in all document groups.

## Focused Green and documentation regression

Observed focused result after updating all localized sources: `Ran 2 tests in 0.009s`; `OK`.

The first full documentation-module run observed `Ran 14 tests`; `FAILED (failures=4)`. Three guides had shortened the required work-time warning to a generic phrase, and some start guides no longer contained later explanatory internal mapping required by the existing documentation contract. Production documentation was clarified without restoring internal names as the initial choice.

Observed corrected documentation result: `Ran 14 tests in 0.074s`; `OK`.

## Broader verification and release outputs

Full regression command:

`python -m unittest discover -s tests -v`

The earlier `68`-test result was discovered to be incomplete because Python's top-level discovery did not recurse into `tests/codex/` or `tests/conformance/`. Adding `tests/codex/__init__.py` and `tests/conformance/__init__.py`, together with a discovery regression assertion, made the same command include those 29 previously omitted tests.

The first corrected final run observed `Ran 98 tests in 5.551s`; `FAILED (failures=1)` because Windows returned transient `WinError 5` while a release test atomically replaced its temporary build directory. The affected test was rerun in isolation:

`python -m unittest tests.release.test_codex_release.CodexReleaseBuildTests.test_builder_emits_minimal_equivalent_plugin_zip_and_checksum`

Observed isolated result: `Ran 1 test in 0.208s`; `OK`.

The complete corrected discovery command was then repeated in the approved PyYAML environment. Observed final result: `Ran 98 tests in 5.134s`; `OK`.

Package build command:

`python scripts/build_release.py`

Observed: `Built codex, generic release 1.1.0 in C:\Users\Ian\Desktop\Grill Me\dist`.

Current archive hashes:

- `bc98595ddde5b06ae2a0d4419c5ef1dc95cc9a495b18047d50ced9f6ce547dc4  codex/ask-then-do-it-1.1.0.zip`
- `0cd6b9dd87c6dd262c67a7def05882c3463210c38296289b5c4b16ac160a7326  generic/ask-then-do-it-generic-1.1.0.zip`

Official validators observed:

- Canonical Plugin: `Plugin validation passed` and nine `Skill is valid!` results.
- Packaged Plugin: `Plugin validation passed` and nine `Skill is valid!` results.
- Codex conformance: `Conformance passed: codex against core 1.1.0`.
- Generic conformance: `Conformance passed: generic-prompts against core 1.1.0`.

Static Markdown scan found no legacy user-facing choice phrase outside durable requirements, specifications, plans, historical evidence, and legitimate internal routing or prohibition statements.

## Residual risks and boundaries

- Live Codex or third-party model responses were not executed, so exact runtime phrasing remains host-dependent.
- No installation, marketplace, publication, upload, hosting, or external CI mutation was performed.
- Independent Review completed with no remaining actionable finding, and the release ledger was synchronized to the corrected 98-test result.
