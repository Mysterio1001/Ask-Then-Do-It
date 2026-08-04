# Optional Ticket Testing Ticket 5 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `optional-ticket-testing-ticket-5-evidence`

Workflow ID: `optional-ticket-testing`

Core version: `1.1.0`

Status: Completed

Inputs: Approved [Optional Ticket Testing Specification](../specs/optional-ticket-testing.md), Approved [Ticket Plan](../plans/optional-ticket-testing.md), completed Tickets 1-4, and Ticket 5.

Assumptions: `tdd` and `direct` remain stable internal routing values. User-facing planning uses localized meanings equivalent to adding or declining tests and collects all Ticket choices in one batch.

Deferred: Localized onboarding and explanatory documentation, generated release packages, checksums, release evidence integration, installation, marketplace mutation, publication, upload, and external CI execution. These are assigned to Ticket 6 where applicable.

Handoff: Completed [independent Ticket 5 Review](optional-ticket-testing-ticket-5-review.md), then Ticket 6.

## Outcome

Provider-neutral Core, Codex, and Generic planning now show complete Ticket definitions and all risk recommendations before one batch request. The request uses plain-language add-tests choices, accepts all-add, all-decline, and explicit mixed responses, retains partial choices, asks only about unresolved Tickets, and maps resolved choices to the existing internal implementation paths. Orchestration and the mandatory plan-gate rule preserve the same contract.

## Changed areas

- Provider-neutral Ticket Planning, Ticket Plan artifact, orchestration, and `GATE-PLAN-001` rule wording.
- Codex `$plan-tickets`, `$ask-then-do-it`, and `GATE-PLAN-001` rule mapping.
- Generic Ticket Planning and orchestration prompts.
- Focused Core, Codex, and Generic contract tests.

## Red evidence

Command:

`$env:PYTHONPATH='C:\Users\Ian\AppData\Local\Temp\codex-grill-me-pydeps'; & 'C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.conformance.test_validator.ConformanceValidatorTests.test_core_defines_user_selected_implementation_modes tests.codex.test_adapter.CodexAdapterTests.test_codex_routes_user_selected_tdd_and_direct_modes tests.generic.test_generic_prompts.GenericPromptScenarioTests.test_generic_routes_user_selected_tdd_and_direct_modes -v`

Observed before production changes: `Ran 3 tests`; `FAILED (failures=3)`. Each failure reported that its planning contract lacked `complete Ticket definitions and all recommendations before requesting one batch test choice`; the supplied source still asked users to choose `tdd` or `direct`.

## Focused Green evidence

The first post-change run reached the new Generic assertion but the Core and Codex tests stopped in setup with `AttributeError: module 'yaml' has no attribute 'safe_load'` because the sandbox-provided `yaml` module shadowed PyYAML. This was an environment error, not a product failure. The identical command was repeated in the approved external Python environment with the configured PyYAML dependency.

Observed valid focused result: `Ran 3 tests in 0.007s`; `OK`.

## Refactor and broader verification

The planning policy was consolidated around the same terms across all three contracts: one batch, all-add, all-decline, explicit mixed selection, unresolved-only follow-up, and deterministic internal mapping. Internal implementation and Review terms remain unchanged where they are required for routing and evidence.

Broader regression command:

`python -m unittest tests.conformance.test_validator tests.codex.test_adapter tests.codex.test_ask_then_do_it_codex_identity tests.generic.test_generic_prompts tests.generic.test_ask_then_do_it_generic_identity -v`

Observed in the approved PyYAML environment: `Ran 47 tests in 1.432s`; `OK`.

Official conformance commands:

- `python scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest adapters/codex/conformance.yaml` → `Conformance passed: codex against core 1.1.0`.
- `python scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest adapters/generic-prompts/manifest.yaml` → `Conformance passed: generic-prompts against core 1.1.0`.

Diff validation: `git diff --check` exited `0`; it reported only existing LF-to-CRLF working-copy warnings and no whitespace errors.

## Independent Review fix cycle

An independent Ticket 5 Review reported two P2 findings:

1. Core, Codex, and Generic planning required a general time warning rather than binding the warning to every Ticket.
2. The initial contract tests did not directly check ordering, resolved-choice retention, unresolved-only follow-up, or a broader set of legacy and sequential question forms.

The approved Ticket 5 TDD path was resumed. Tests were strengthened first with a per-Ticket warning assertion, ordering comparisons, exact partial-choice retention and unresolved-only assertions, and negative assertions for legacy mode questions and per-Ticket conversational loops.

Observed Review-fix Red: `Ran 3 tests`; `FAILED (failures=3)`. All three contracts lacked `For every Ticket, warn that tests may increase work time`.

Core, Codex, and Generic planning were then changed to require the warning for every Ticket.

Observed Review-fix focused Green: `Ran 3 tests in 0.007s`; `OK`.

Observed Review-fix broader regression: `Ran 47 tests in 1.184s`; `OK`.

The corrected raw diff and results were returned to the independent reviewer for final assessment.

The first re-review confirmed the production warning fix but found one remaining P2 test-protection gap: tests did not require the normative prohibition against presenting internal modes as the initial choice and did not compare the per-Ticket warning position with the batch request. Because production already contained the Approved behavior, no additional failing production state was manufactured. Tests were strengthened to require the prohibition, reject non-prohibitive `tdd`/`direct` choice lines, and prove both each recommendation and each warning precede the request.

Observed final focused result: `Ran 3 tests in 0.009s`; `OK`.

Observed final broader regression: `Ran 47 tests in 0.991s`; `OK`.

The final raw diff and results were returned for a second independent re-review.

## Incomplete checks and residual risks

- The full release and documentation suite is intentionally deferred until Ticket 6 updates all localized sources and rebuilt packages.
- Native Plugin and Skill validators and deterministic package comparisons are deferred to Ticket 6 because this Ticket changes canonical Skill content but not managed release outputs.
- String-contract tests verify the required policy clauses, but live model responses remain host-dependent and were not executed.
