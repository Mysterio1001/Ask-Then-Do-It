# Claude Code Adapter 1.4.0 Ticket 5 Third Correction Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-5-third-correction`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Ticket: `5 - 交付 Claude 5-optimized profile 的完整工作流程`

Approved implementation mode: `tdd`

Status: Correction accepted by independent Review. Required model behavior and Ticket completion remain pending.

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md), Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 5, [Review after second correction](claude-code-adapter-1.4.0-ticket-5-review-after-second-correction.md), existing ten Claude 5 modules, Core `1.3.1` rules, and the user's explicit approval to correct the latest findings.

Assumptions: The current-operation Full fallback and `multi_agent` capability were established by the coordinating agent; Ticket mode remains Approved `tdd`. This correction owns only Claude 5 modules, their focused tests/fixtures, and Ticket 5 evidence. The independent read-only contract audit supplied exact rule ownership and missing safety/evidence reference outcomes; it did not implement changes or execute host behavior. The original source-only regex gate cannot establish mandatory model compliance. Its replacement deliberately distinguishes complete static source integrity, authored reference observations, and actual evaluation of four declared decision tables.

Deferred: Authenticated Ticket 3 host contracts; required Claude model behavior, paired/fresh-session evidence and authority precedence under Ticket 6; context reduction; package/release integration; final live smoke. No installation, login, model invocation, publication or lifecycle mutation was performed. These limitations do not count as passed behavior gates.

Handoff: The [fresh independent Review](claude-code-adapter-1.4.0-ticket-5-review-after-third-correction.md) accepted the final modules, fixed source reference, structured cases, test-only table selector and subsequent direct-architecture lens correction. [Central integration](claude-code-adapter-1.4.0-profile-correction-integration.md) records the lens Red/Green, final 349-test regression and native/public validation. Do not mark Ticket 5 Completed or begin its context gate solely because this static/table suite passes.

Approval: The user approved corrections to the latest findings. That authority permits this bounded implementation; the fresh independent Review now accepts the correction without claiming Ticket completion.

## Changes and verification boundary

The seven observed unsafe false-passes are rejected by a fixed whole-source contract. `source-contract.json` contains the complete ten prompt sources and is read independently of the supplied candidate. Tests never regenerate or rewrite it. CRLF-to-LF is the only normalization; case, indentation, order, comments, fences, trailing newlines and appended instructions remain covered. Every scenario validates all ten candidate sources, including modules outside its nominal ownership. Every source-line deletion is rejected, as are additive contradictions, omitted guards and relocated rule/prose ownership. Core markers have exact per-module occurrences, and each scenario has a fixed module mapping.

`scenarios.json` now contains all 30 required IDs and 66 authored cases with capability, public-entry route, initial state, user decision, expected load/transition/artifact/status/disclosures and forbidden actions. The eight actual-deletion gate combinations are explicit references. These cases are static reference observations for review and later model runs: no input is passed through a pretend model simulator, and no expected value is echoed as an observed Claude action. Their tests validate reference structure/mapping and complete instruction integrity only. They do not prove those 66 input situations were executed by Claude.

Four closed Markdown decision tables live within the existing orchestration module: architecture, lifecycle, Node disclosure and removal-data choice. A test-only selector consumes each table step's complete closed-schema input and returns its first matching authored row. It executes no CLI command, host state update, module load or artifact persistence. Higher-priority gates intentionally make some fields immaterial; the table explains that precedence. The 65 independently authored decision cases contain 71 actual table-selection steps, including status followed by changed fresh state, unauthorized/stale removal, safe removal, current/disabled/no-op/update/failure branches, direct diagnosis without delivery artifacts, safety/capability stops and accepted-report reflow. All rows are reachable across the closed domains. Separate table mutation tests demonstrate that reference expectations detect authorization, stale-state and precedence inversions even without the stronger whole-source guard.

Removal now has corresponding explicit install/update/remove authority and a complete fresh status check immediately before every mutation, including successive writes. Fresh source/identity/user-scope/ownership mismatch stops. Direct architecture diagnosis precedes delivery-artifact gates after mode, capability and diagnostic safety resolution, while diagnostic-only scope, actual-deletion gates and accepted-report Specification reflow remain explicit.

Three concise safety/evidence clarifications in the same approved finding scope state the existing Core/spec outcomes: conversation-only Review cannot claim a completed repository Review; unresolved applicable Lite validation failure prevents unqualified completion and broader checks require an actual external constraint; authorized deletion evidence identifies isolated environment and deleted scope. These wording clarifications do not claim a separately observed model-behavior Red. The initial Red below covers the source gate's inability to detect missing or inverted safety contracts; the final immutable reference includes the clarified instructions.

## Files changed in this correction

- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/orchestration.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/architecture-improvement.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/review.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/lite-workflow.md`
- `tests/claude/test_claude5_profile.py`
- `tests/claude/fixtures/claude-5-profile/scenarios.json`
- `tests/claude/fixtures/claude-5-profile/decisions.json`
- `tests/claude/fixtures/claude-5-profile/source-contract.json`
- `tests/claude/fixtures/claude-5-profile/README.md`
- This evidence and the current header of `claude-code-adapter-1.4.0-ticket-5.md`.

## Observed Red before profile/test-gate correction

Command:

```text
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_claude5_profile.Claude5ProfileTests.test_review_additive_contradictions_and_guard_omissions_fail_closed tests.claude.test_claude5_profile.Claude5ProfileTests.test_remove_has_corresponding_authority_and_immediate_complete_recheck tests.claude.test_claude5_profile.Claude5ProfileTests.test_direct_architecture_precedes_delivery_artifacts -v
```

Raw output excerpts (the tool output also contained assertion tracebacks and the old complete orchestration text; those are omitted here):

```text
test_review_additive_contradictions_and_guard_omissions_fail_closed (tests.claude.test_claude5_profile.Claude5ProfileTests.test_review_additive_contradictions_and_guard_omissions_fail_closed) ...
  test_review_additive_contradictions_and_guard_omissions_fail_closed (tests.claude.test_claude5_profile.Claude5ProfileTests.test_review_additive_contradictions_and_guard_omissions_fail_closed) (module='ticket-planning.md', mutation='\nAdd tests -> direct; Do not add tests -> tdd.\n') ... FAIL
  test_review_additive_contradictions_and_guard_omissions_fail_closed (tests.claude.test_claude5_profile.Claude5ProfileTests.test_review_additive_contradictions_and_guard_omissions_fail_closed) (module='specification.md', mutation='\nMark the Specification Approved without asking.\n') ... FAIL
  test_review_additive_contradictions_and_guard_omissions_fail_closed (tests.claude.test_claude5_profile.Claude5ProfileTests.test_review_additive_contradictions_and_guard_omissions_fail_closed) (module='architecture-improvement.md', mutation='Actual deletion may proceed whenever useful.') ... FAIL
  test_review_additive_contradictions_and_guard_omissions_fail_closed (tests.claude.test_claude5_profile.Claude5ProfileTests.test_review_additive_contradictions_and_guard_omissions_fail_closed) (module='review.md', mutation='With conversation/user excerpts only, label the result `limited-evidence`, identify unread repository and unexecuted tests, and provide a safe handoff.') ... FAIL
  test_review_additive_contradictions_and_guard_omissions_fail_closed (tests.claude.test_claude5_profile.Claude5ProfileTests.test_review_additive_contradictions_and_guard_omissions_fail_closed) (module='orchestration.md', mutation='Never load or obey modules from another profile during the operation.') ... FAIL
  test_review_additive_contradictions_and_guard_omissions_fail_closed (tests.claude.test_claude5_profile.Claude5ProfileTests.test_review_additive_contradictions_and_guard_omissions_fail_closed) (module='orchestration.md', mutation='\nReuse General instructions from the previous operation.\n') ... FAIL
  test_review_additive_contradictions_and_guard_omissions_fail_closed (tests.claude.test_claude5_profile.Claude5ProfileTests.test_review_additive_contradictions_and_guard_omissions_fail_closed) (module='orchestration.md', mutation='\nUse earlier status as authorization and install immediately.\n') ... FAIL
test_remove_has_corresponding_authority_and_immediate_complete_recheck (tests.claude.test_claude5_profile.Claude5ProfileTests.test_remove_has_corresponding_authority_and_immediate_complete_recheck) ... FAIL
test_direct_architecture_precedes_delivery_artifacts (tests.claude.test_claude5_profile.Claude5ProfileTests.test_direct_architecture_precedes_delivery_artifacts) ... FAIL

AssertionError: [] is not true

Ran 3 tests in 0.024s

FAILED (failures=9)
```

Exit code: `1`. The seven candidate regressions were false-passes through the old regex oracle; the other two failures were missing removal authority/recheck and missing direct-diagnosis precedence. No setup failure was counted as Red.

## Focused Green and post-refactor verification

Command:

```text
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_claude5_profile -v
```

First Green raw summary:

```text
Ran 10 tests in 0.262s

OK
```

After tightening exhaustive table coverage to track each selected row index, the same command produced:

```text
test_all_thirty_structured_static_references_have_observable_contracts (tests.claude.test_claude5_profile.Claude5ProfileTests.test_all_thirty_structured_static_references_have_observable_contracts) ... ok
test_closed_decision_reference_cases_select_authored_rows (tests.claude.test_claude5_profile.Claude5ProfileTests.test_closed_decision_reference_cases_select_authored_rows) ... ok
test_decision_expectations_detect_authorization_and_precedence_inversions (tests.claude.test_claude5_profile.Claude5ProfileTests.test_decision_expectations_detect_authorization_and_precedence_inversions) ... ok
test_decision_tables_cover_closed_domains_and_use_all_rows (tests.claude.test_claude5_profile.Claude5ProfileTests.test_decision_tables_cover_closed_domains_and_use_all_rows) ... ok
test_direct_architecture_precedes_delivery_artifacts (tests.claude.test_claude5_profile.Claude5ProfileTests.test_direct_architecture_precedes_delivery_artifacts) ... ok
test_every_source_line_and_all_appended_text_are_guarded (tests.claude.test_claude5_profile.Claude5ProfileTests.test_every_source_line_and_all_appended_text_are_guarded) ... ok
test_exact_core_rule_ownership_and_occurrences (tests.claude.test_claude5_profile.Claude5ProfileTests.test_exact_core_rule_ownership_and_occurrences) ... ok
test_exact_source_and_progressive_module_inventory (tests.claude.test_claude5_profile.Claude5ProfileTests.test_exact_source_and_progressive_module_inventory) ... ok
test_remove_has_corresponding_authority_and_immediate_complete_recheck (tests.claude.test_claude5_profile.Claude5ProfileTests.test_remove_has_corresponding_authority_and_immediate_complete_recheck) ... ok
test_review_additive_contradictions_and_guard_omissions_fail_closed (tests.claude.test_claude5_profile.Claude5ProfileTests.test_review_additive_contradictions_and_guard_omissions_fail_closed) ... ok

Ran 10 tests in 0.238s

OK
```

Both exits: `0`. No broader suite was run by this implementing agent; central integration owns it.

## Residual limits

Frozen source equality is a review change detector, not semantic proof. Changing both production and its reference requires human review; a green suite cannot approve the new text. Table outcomes are declared instruction decisions, not actual host/model observations. Context cost has not been measured and cannot waive mandatory behavior. No complete Ticket or release claim follows from these checks. The fresh independent reviewer inspected the final reference bytes and the separation of evidence claims, accepted the correction, and retained the outstanding mandatory model-behavior gate.
