# Claude Code Adapter 1.4.0 Ticket 4 Implementation Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-4-implementation`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Ticket: `4 - 交付 General profile 的完整工作流程`

Execution mode: `tdd` (`Add tests`, explicitly selected by the user)

Status: Correction accepted - mandatory model-behavior evidence pending

Inputs: Approved [Claude Code Adapter 1.4.0 Specification](../specs/claude-code-adapter-1.4.0.md)、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 4、Approved [Requirement Decision Record](../requirements/claude-code-adapter-1.4.0.md)、Ticket 1 public Plugin boundary、Completed／accepted Ticket 2 router and session-state evidence、[Ticket 4 independent Review](claude-code-adapter-1.4.0-ticket-4-review.md)，以及 [Ticket 4 Review After Correction](claude-code-adapter-1.4.0-ticket-4-review-after-correction.md) 的三項使用者核准 findings。

Assumptions: General profile consumes only a public bootstrap-validated ready binding whose selected profile is `general`; bootstrap/router validation stays owned by Tickets 1–2. The 30-scenario fixture maps static instruction coverage, not executed model decisions, a real Claude response, authenticated host session, or paired comparison. Exact Claude Code `2.1.251` authenticated command identity, `UserPromptExpansion` visibility, resume/switch behavior, and host failure semantics remain provisional until Ticket 3.

Deferred: Required model-behavior observations for the thirty General scenarios; Ticket 3 authenticated live-host ledger; cross-profile paired/fresh-session conformance; context proxy; localized documentation; release identity/build/packages; live smoke; and all tag, push, release, upload, Marketplace activation, or announcement actions. The shared Plugin validator inventory mismatch and latest correction Review are closed.

Handoff: Latest correction and direct-architecture lens follow-up accepted by the [fresh independent Review](claude-code-adapter-1.4.0-ticket-4-review-after-third-correction.md). [Central integration](claude-code-adapter-1.4.0-profile-correction-integration.md) records the lens Red/Green, final 349-test regression and both profile Reviews. Preserve the reviewed instruction baseline and obtain the missing model-behavior observations before marking Ticket 4 Completed. Ticket 3 remains a hard local `1.4.0` completion gate; paired behavior, context measurement, and live smoke also remain required. The current user approval covers the additive-contradiction correction.

Approval: Implementation authority comes from the Approved Ticket Plan, its approved Ticket 4 `tdd` mode, the user's explicit continuation approval for this operation, the earlier approved Review corrections, and the user's explicit approval to correct all three findings from the Ticket 4 Review After Correction.

## Outcome

- Added exactly ten internal General profile modules: orchestration, Lite, requirements, documented requirements, Specification, Ticket Planning, TDD, direct implementation, Review, and architecture improvement.
- Mapped all 30 mandatory Core rule IDs without a profile exemption and bound every ID to exactly one owning module with an independently asserted `Core rules:` declaration.
- Added a fixed 30-scenario General inventory and a test-owned structured contract for every scenario, each with a non-empty input state, expected outcomes, and prohibited actions. The oracle includes inverse mutations for Ticket test-mode mapping, Review downgrade mapping, deletion authorization, data retention, approval, and TDD/direct routing.
- Implemented Claude-specific read-only Config precedence and invalid fail-closed behavior without reading Codex Config or writing `settings.json`.
- Preserved Full gates, Lite budgets, TDD/direct distinction, evidence honesty, three-level Review downgrade, twelve-lens Review, diagnostic-only architecture analysis, and approved artifact states.
- Added explicit safe status/install/update/remove/ZIP lifecycle guidance with user-scope identity, no-op/disabled/newer/source/scope/partial-failure branches, reload requirement, data disclosure, and session-only ZIP boundary.
- Bound the profile to the current operation, prohibited profile-local model classification/rerouting/model override, rejected affirmative ambiguous other/optimized/alternate/different-profile instructions, and constrained deterministic scenario load traces to the General directory.
- Defined one always-loaded portable artifact envelope with nine fixed fields, stable artifact identity, and conditional approval evidence; all eight artifact-producing stages explicitly depend on that definition.
- Defined deterministic conversation-only Config transitions for project/user host-unavailable sources, including project-unavailable/user-available precedence, Full fallback, unavailable-versus-invalid separation, and no fabricated read claim.
- Restored all four Full architecture triggers, the local-versus-systemic Review boundary, automatic-route announcement, accepted-report-to-Specification reflow, and post-artifact durable-knowledge synchronization with complete change disclosure and joint approval.
- Required a fresh complete ownership/source/scope/state recheck immediately before install, update, and normal remove writes; stale, changed, ambiguous, or mismatched evidence stops without writes.
- Made direct architecture diagnosis precede delivery first-unmet gates after mode/capability/safety and the architecture stage's own prerequisites, while preserving diagnostic-only authority and Specification reflow after acceptance.

## Files changed

- `adapters/claude-code/plugin/ask-then-do-it/profiles/general/orchestration.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/general/lite-workflow.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/general/requirements.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/general/documented-requirements.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/general/specification.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/general/ticket-planning.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/general/tdd-implementation.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/general/direct-implementation.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/general/review.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/general/architecture-improvement.md`
- `tests/claude/fixtures/general-profile/scenarios.json`
- `tests/claude/test_general_profile.py`
- This Implementation Evidence.

## Red evidence

Before any General profile production module existed:

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_general_profile -v
```

Observed raw summary:

```text
Ran 6 tests in 0.023s

FAILED (failures=33, errors=2)
```

The errors were missing `orchestration.md` and `review.md`; failures reported the exact ten-module inventory absent, all 30 mandatory Core IDs unmapped, every fixed scenario missing its owning module/contract, and missing model/cross-profile safety clauses. This was the expected missing General behavior, not an unrelated setup error.

## Focused Green and refactor

After adding the ten modules, the first focused run reached five passing methods and one precise scenario failure:

```text
Ran 6 tests in 0.013s

FAILED (failures=1)
```

`LITE-RISK` required the explicit before-or-during risk boundary. The production instruction was clarified without weakening the fixture. Final focused command:

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_general_profile -v
```

Observed final result:

```text
test_claude_config_and_lifecycle_are_read_only_and_fail_closed ... ok
test_fixed_thirty_scenarios_have_executable_general_contracts ... ok
test_general_profile_has_exact_internal_module_inventory ... ok
test_general_profile_maps_every_mandatory_core_rule ... ok
test_profile_never_overrides_model_or_loads_cross_profile_instructions ... ok
test_review_downgrades_are_honest_and_lite_stays_same_context ... ok

Ran 6 tests in 0.012s

OK
```

## Review correction Red and Green

After the independent Review's three P2 findings were approved, the following focused correction tests were added before production edits. They parse the shared envelope definition and exact transition tables and include negative mutations for a missing envelope field, a stage that stops depending on the shared definition, the wrong Config fallback, a local Review incorrectly routed to architecture, and knowledge changes applied without joint approval.

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_general_profile.ClaudeGeneralProfileTests.test_artifact_stages_depend_on_one_complete_portable_envelope tests.claude.test_general_profile.ClaudeGeneralProfileTests.test_conversation_unavailable_config_sources_follow_absence_transitions tests.claude.test_general_profile.ClaudeGeneralProfileTests.test_full_architecture_and_knowledge_routes_are_transition_complete -v
```

Observed before correction:

```text
test_artifact_stages_depend_on_one_complete_portable_envelope ... FAIL
test_conversation_unavailable_config_sources_follow_absence_transitions ... FAIL
test_full_architecture_and_knowledge_routes_are_transition_complete ... FAIL

Ran 3 tests in 0.002s

FAILED (failures=3)
```

Each failure identified the corresponding missing production section: `Portable artifact envelope`, `Conversation-only unavailable-source transitions`, or `Full architecture transitions`. This was the exact missing behavior reported by Review, not a setup failure.

After the smallest General-only production correction and a mechanical test-oracle fix preserving the approved assertions, the same focused command produced:

```text
test_artifact_stages_depend_on_one_complete_portable_envelope ... ok
test_conversation_unavailable_config_sources_follow_absence_transitions ... ok
test_full_architecture_and_knowledge_routes_are_transition_complete ... ok

Ran 3 tests in 0.003s

OK
```

Post-correction full General verification:

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_general_profile -v
```

Observed:

```text
Ran 9 tests in 0.015s

OK
```

Post-correction Python compilation and scoped `git diff --check` both exited `0` with no output.

## Review-after-correction Red and Green

After the Review After Correction's three findings were explicitly approved, the General test oracle was strengthened before any corresponding production edit. The scenario fixture now owns only the fixed inventory and module mapping; independent test code defines all 30 input states, expected outcomes, and prohibited actions. Exact Core rule ownership, General-only load traces, affirmative ambiguous cross-profile load rejection, lifecycle write transitions, and Full route precedence are separately parsed and mutation-tested.

Focused Red command:

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_general_profile -v
```

Observed raw summary:

```text
test_direct_architecture_diagnosis_precedes_delivery_gates ... FAIL
test_every_lifecycle_write_requires_fresh_ownership_state ... FAIL
test_fixed_thirty_scenarios_have_executable_general_contracts ... FAIL
test_general_profile_maps_every_mandatory_core_rule ... FAIL

Ran 11 tests in 0.021s

FAILED (failures=4)
```

The failures were the intended missing contracts: no `Full route precedence` section, no `Lifecycle write authorization transitions` section, no remove-inclusive fresh pre-write outcome for `INSTALL-WRITES`, and no exact `Core rules:` ownership declaration in `orchestration.md`. Seven existing methods remained green; the run had no setup or unrelated error.

The smallest production correction added exact Core ownership declarations to the ten General modules, a fresh pre-write lifecycle transition table covering normal remove, and a direct-versus-automatic architecture precedence table. Direct architecture diagnosis now occurs before delivery gates but after mode/capability/safety and the architecture stage's own prerequisites. No Claude 5 or public/shared contract was changed.

Post-correction focused Green:

```text
test_artifact_stages_depend_on_one_complete_portable_envelope ... ok
test_claude_config_and_lifecycle_are_read_only_and_fail_closed ... ok
test_conversation_unavailable_config_sources_follow_absence_transitions ... ok
test_direct_architecture_diagnosis_precedes_delivery_gates ... ok
test_every_lifecycle_write_requires_fresh_ownership_state ... ok
test_fixed_thirty_scenarios_have_executable_general_contracts ... ok
test_full_architecture_and_knowledge_routes_are_transition_complete ... ok
test_general_profile_has_exact_internal_module_inventory ... ok
test_general_profile_maps_every_mandatory_core_rule ... ok
test_profile_never_overrides_model_or_loads_cross_profile_instructions ... ok
test_review_downgrades_are_honest_and_lite_stays_same_context ... ok

Ran 11 tests in 0.034s

OK
```

The structured oracle also proved that the focused suite rejects the Review's named inverse mutations: `Add tests`/`Do not add tests` swapped to the wrong implementation modes; `tools`/`conversation` Review labels swapped; deletion permitted without all three guards; unconditional `--keep-data`; approval bypass; and TDD/direct inversion. Removing or relocating a Core marker together with its declaration is rejected even when the global ID union is preserved. General load traces reject a Claude 5 path, and affirmative instructions to load/follow/obey the other, optimized, alternate, or different profile are rejected without misclassifying the existing negative prohibition.

## Additional focused checks

Python syntax:

```powershell
& '.\.venv\Scripts\python.exe' -B -m py_compile tests\claude\test_general_profile.py
```

Observed: exit `0`; no output.

Scoped whitespace validation:

```powershell
git diff --check -- adapters/claude-code/plugin/ask-then-do-it/profiles/general tests/claude/test_general_profile.py tests/claude/fixtures/general-profile/scenarios.json docs/evidence/claude-code-adapter-1.4.0-ticket-4.md
```

Observed: exit `0`; no output.

## Central shared-validator integration

When both required profiles first existed, the old canonical validator still rejected the Specification-required `profiles` root. The initial direct probe reported:

```powershell
& '.\.venv\Scripts\python.exe' -B scripts\validate_claude_plugin.py --catalog '.claude-plugin\marketplace.json' --plugin 'adapters\claude-code\plugin\ask-then-do-it'
```

Observed: exit `1` with:

```text
Claude Plugin validation failed: Claude Plugin root inventory must be exactly ['.claude-plugin', 'agents', 'config', 'hooks', 'scripts', 'skills']
```

The central focused TDD run then fixed this as an explicit integration Red rather than weakening either profile:

```text
Ran 2 tests in 0.282s

FAILED (failures=2)
```

The failures showed that the canonical validator still rejected profiles after profile delivery. Central integration updated the shared validator contract to require a Plugin root containing `profiles`, require exactly `general` and `claude-5`, and require each profile to contain the exact ten approved modules. Mutation coverage now rejects a missing or extra profile, a missing or extra module, and profile paths that violate the existing path/link containment guard.

Central focused Green:

```text
Ran 3 tests in 7.391s

OK
```

This closes the shared-validator integration item. The Ticket 4 worker did not modify shared validation code; the central owner integrated and verified it after both profile trees were available.

## Central combined verification

Combined profile/public contracts:

```text
Ran 23 tests in 13.869s

OK
```

Complete Claude suite:

```text
Ran 118 tests in 73.059s

OK (skipped=1)
```

Complete repository suite:

```text
Ran 334 tests in 91.245s

OK (skipped=1)
```

The canonical Claude Plugin validator, model-evidence validator, Node syntax check, and `git diff --check` all exited `0`; diff check emitted only the pre-existing Project Knowledge Base line-ending warning. Exact Claude Code `2.1.251` strict validation of both the canonical Plugin and repository Marketplace exited `0` with no warning. These strict schema results do not replace Ticket 3 authenticated session behavior or the later live-smoke gate.

## Additive-contradiction correction (2026-09-09)

The user approved the P1 finding in the [Review after second correction](claude-code-adapter-1.4.0-ticket-4-review-after-second-correction.md). That review found the current production wording consistent but demonstrated four additive inverse instructions that still passed the scenario gate.

Before changing the gate, added two regression tests and ran:

```powershell
& '.venv/Scripts/python.exe' -B -m unittest tests.claude.test_general_profile.ClaudeGeneralProfileTests.test_additive_inverse_instructions_fail_the_scenario_gate tests.claude.test_general_profile.ClaudeGeneralProfileTests.test_all_modules_reject_unreviewed_additions_and_reordering
```

Observed Red, exit `1`:

```text
Ran 2 tests in 0.068s
FAILED (failures=34)
```

Four failures reproduce all reported additive contradictions (test-mode mapping, other-profile authority, stale remove status, and direct architecture precedence). Thirty additional failures preserve existing words while adding a new section, inserting text, or reordering paragraphs in each of the ten modules. Each failure was `AssertionError not raised`, not missing setup.

Added `tests/claude/fixtures/general-profile/reviewed-instructions.json` as an independent fixed copy of the already reviewed complete module texts, plus maintenance instructions in its sibling `README.md`. `assert_scenario_contracts` now verifies the supplied candidate against those ten complete texts before supplementary coverage checks. It rejects additions, removals, relocation, and new contradictory wording without a phrase blacklist. Only CRLF/LF differences are normalized; Markdown indentation, case, order, and trailing content remain significant. The test run cannot regenerate the fixture. No General production bytes changed in this correction.

Focused Green, exit `0`:

```powershell
& '.venv/Scripts/python.exe' -B -m unittest tests.claude.test_general_profile
```

```text
Ran 13 tests in 0.054s
OK
```

Evidence limit: this closes unreviewed-text false passes, not general natural-language interpretation. `ScenarioContract` inputs/outcomes remain static coverage notes; they are not executed Claude requests or observed decisions. The renamed thirty-scenario test explicitly says `reviewed_instruction_contracts`. A prompt and blindly refreshed fixture could agree, so fixture changes still require independent review. The Specification's mandatory model-behavior observations are not established by this correction, and the Ticket must not be marked Completed solely from these checks. Earlier entries using “executable” or “simulation” should be read with this explicit limitation; historical raw results are preserved.

Fresh [independent Review after third correction](claude-code-adapter-1.4.0-ticket-4-review-after-third-correction.md) found no actionable correction defect. The reviewer independently passed General/public `26` tests and rejected `72` mutation candidates. Correction acceptance is recorded separately from Ticket completion: the mandatory model-behavior observations remain pending.

## Scope inspection

- The Ticket 4 worker modified no Claude 5 profile, public Skill, router, reviewer, shared validator, Specification, Plan, README, package, release output, or Project Knowledge Base file. The shared validator change described above was performed separately by the central integration owner.
- No model command, model frontmatter, `ANTHROPIC_MODEL`, cross-profile path, public command, or dynamic shell injection was added to the General modules.
- The central owner subsequently ran the complete repository suite and exact native strict validation recorded above. No shared-output build, host install/update/remove mutation, external publication, authenticated behavior session, or live smoke was executed for this Ticket.

## Residual risks

- The General gate now combines a test-owned structured 30-scenario oracle, exact rule/module ownership, bounded load traces, parsed fixed-field/transition tables, and contradiction-oriented mutations; it still does not prove that a live model follows every instruction. Ticket 6 owns paired/fresh-session behavioral equivalence and no-skip evidence.
- Exact host behavior remains provisional until Ticket 3's authenticated session ledger; a contradictory observation must return to the earliest affected approved artifact and invalidate dependent evidence.
- Shared Plugin validation is closed, including negative inventory/path mutations and Tickets 1–5 combined regressions.
- Ticket 3 authenticated behavior, Ticket 6 paired/fresh-session conformance, Ticket 7 context measurement, and the final live-smoke/release gates remain required.
- Ticket 4's earlier corrections and the three approved Review After Correction findings are focused-verified, but the Ticket remains pending fresh Review and is not marked Completed.
