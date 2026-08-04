# Optional Ticket Testing Ticket 3 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `optional-ticket-testing-ticket-3-evidence`

Workflow ID: `optional-ticket-testing`

Core version: `1.0.1`

Status: Completed

Inputs: Approved [Optional Ticket Testing Specification](../specs/optional-ticket-testing.md), Approved [Ticket Plan](../plans/optional-ticket-testing.md), completed [Ticket 1 evidence](optional-ticket-testing-ticket-1.md), and Ticket 3.

Assumptions: Versioned Generic package composition and localized release guides remain Ticket 4 ownership. Ticket 3 validates canonical provider-neutral prompt sources.

Deferred: `1.1.0` release inventory and package outputs, final Review, and architecture diagnosis.

Handoff: Ticket 4, integrated `1.1.0` release delivery.

## Outcome

The Generic adapter now contains ten prompt files: one bootstrap and nine stage modules including `direct-implementation.md`. Ticket Planning collects risk-informed modes, orchestration routes Approved `tdd` and `direct` Tickets exactly, TDD verifies its mode, direct guidance remains explicitly unexecuted, Review preserves skipped-test disclosure, and architecture reflow uses the plan-selected path without overstating Conversation capability.

## Changed areas

- New Generic direct implementation prompt.
- Generic bootstrap, orchestration, Ticket Planning, TDD, Review, and architecture prompts.
- Generic adapter capability evidence.
- Generic prompt inventory, scenario, provider-neutrality, and architecture tests.

## Red evidence

Command:

`python -m unittest tests.generic.test_generic_prompts.GenericPromptContractTests.test_adapter_has_exactly_one_bootstrap_and_nine_module_prompts tests.generic.test_generic_prompts.GenericPromptContractTests.test_every_prompt_declares_the_required_interface tests.generic.test_generic_prompts.GenericPromptScenarioTests.test_generic_routes_user_selected_tdd_and_direct_modes -v`

Observed before Generic production changes: `Ran 3 tests`; `FAILED (failures=2, errors=1)`. The inventory and interface checks could not find `direct-implementation.md`, and Ticket Planning lacked risk recommendations and mode selection.

## Focused Green evidence

The same three-test command observed: `Ran 3 tests`; `OK`.

## Refactor and broader verification

Command:

`python -m unittest tests.generic.test_generic_prompts -v`

The first broader run observed `Ran 17 tests` with one failure because an older architecture assertion required the literal `TDD`. The assertion was updated to require `plan-selected implementation`, `tdd-implementation.md`, and `direct-implementation.md`, matching the Approved behavior with stronger route coverage. The repeated command observed `Ran 17 tests`; `OK`.

The suite also observed:

- Exact ten-file prompt inventory.
- All prompts expose required interfaces at Core `1.0.1`.
- Canonical prompt sources remain English and provider-neutral.
- Conversation-only capability and persistence claims remain honest.
- Generic conformance passes against the current Core catalog.

## Residual risks

- Active release configuration and combined Generic output still list nine prompt files at `1.0.1`; Ticket 4 owns the ten-file `1.1.0` package.
- Conversation-only prompts cannot prove real repository editing or test behavior; this limitation remains explicit.
