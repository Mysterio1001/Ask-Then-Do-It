# Optional Ticket Testing Ticket 2 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `optional-ticket-testing-ticket-2-evidence`

Workflow ID: `optional-ticket-testing`

Core version: `1.0.1`

Status: Completed

Inputs: Approved [Optional Ticket Testing Specification](../specs/optional-ticket-testing.md), Approved [Ticket Plan](../plans/optional-ticket-testing.md), completed [Ticket 1 evidence](optional-ticket-testing-ticket-1.md), and Ticket 2.

Assumptions: Versioned package configuration, localized release guides, generated ZIPs, and checksums remain Ticket 4 ownership. Ticket 2 validates the canonical Codex Plugin source.

Deferred: Generic adapter behavior, `1.1.0` release inventory and packages, final Review, and architecture diagnosis.

Handoff: Ticket 3, the Generic direct-guidance path.

## Outcome

The canonical Codex Plugin now contains a valid ninth Skill, `$implement-direct`. Planning collects explicit modes with risk and time warnings; orchestration routes Approved `tdd` Tickets to `$implement-tdd` and Approved `direct` Tickets to `$implement-direct` without a default; TDD verifies its selected mode; Review preserves skipped-test evidence; and architecture improvements return through the plan-selected path.

## Changed areas

- New `implement-direct` Skill and OpenAI interface metadata.
- Codex orchestrator, Ticket Planning, TDD, Review, and architecture Skills.
- Plugin metadata, Codex conformance evidence, and rule mappings.
- Codex adapter and source-identity tests.

## Red evidence

Command:

`python -m unittest tests.codex.test_adapter.CodexAdapterTests.test_plugin_skills_are_the_only_source_copy tests.codex.test_adapter.CodexAdapterTests.test_codex_routes_user_selected_tdd_and_direct_modes tests.codex.test_adapter.CodexAdapterTests.test_artifact_producers_require_the_portable_envelope tests.codex.test_ask_then_do_it_codex_identity.AskThenDoItCodexIdentityTests.test_plugin_folder_manifest_and_skill_inventory_agree -v`

Observed before Codex production changes: `Ran 4 tests`; `FAILED (failures=3, errors=1)`. Both inventories lacked `implement-direct`, planning lacked the recommendation and mode gate, and the artifact-envelope check could not open the missing Skill.

## Focused Green evidence

The same four-test command observed: `Ran 4 tests`; `OK`.

## Refactor and broader verification

Command:

`python -m unittest tests.codex.test_adapter <three non-package Codex identity tests> -v`

The first run observed `Ran 16 tests` with one failure because an older architecture test required the literal `TDD`. The Skill already routed through both `$implement-tdd` and `$implement-direct`, so the outdated assertion was strengthened to verify `plan-selected implementation` and both exact Skill routes. The repeated command observed `Ran 16 tests`; `OK`.

Official local validation ran `quick_validate.py` against every canonical Skill. Observed nine consecutive `Skill is valid!` results and `Validated 9 Codex Skills`.

`git diff --check` remained free of whitespace errors apart from Git's informational LF-to-CRLF checkout warnings.

## Residual risks

- The active release configuration still lists eight Skills at `1.0.1`; Ticket 4 owns the intentional breaking inventory update to nine Skills at `1.1.0` and the packaged Plugin validator.
- Generic behavior is not yet implemented.
- No Plugin was installed and no marketplace or personal state was changed.
