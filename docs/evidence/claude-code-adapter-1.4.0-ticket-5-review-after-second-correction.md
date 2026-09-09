# Claude Code Adapter 1.4.0 Ticket 5 Review After Second Correction

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-5-review-after-second-correction`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Ticket: `5 - 交付 Claude 5-optimized profile 的完整工作流程`

Approved implementation mode: `tdd`

Review label: `independent`

Status: Changes requested

Inputs: Approved `docs/specs/claude-code-adapter-1.4.0.md`; Approved `docs/plans/claude-code-adapter-1.4.0.md` Ticket 5; the current ten files under `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/`; `tests/claude/test_claude5_profile.py`; `tests/claude/fixtures/claude-5-profile/scenarios.json`; the current two public Skill bootstraps; the shared Plugin validator's profile/bootstrap boundary; only the raw command/result portions of `docs/evidence/claude-code-adapter-1.4.0-ticket-5.md`; and the independent raw verification below. No previous Ticket 5 Review artifact, previous finding text, implementer defence, or proposed verdict was read.

Assumptions: This reviewer did not implement or correct the Claude 5 profile. Ticket 5 remains provisional where it depends on authenticated Claude Code `2.1.251` command identity, `UserPromptExpansion`, resume/switch, and host failure semantics. Ticket 6 owns paired/fresh-session equivalence, but Ticket 5 itself owns an optimized-only deterministic 30-scenario gate capable of rejecting wrong behavior; later paired testing does not substitute for the Approved Ticket 5 TDD completion gate. Public-bootstrap routing and fixed-resource containment remain shared boundaries rather than Ticket 5-owned implementations.

Deferred: Ticket 3 authenticated host evidence; General/Claude-5 paired behavior; deterministic context reduction; localized documentation; release/package integration; live smoke; and all external publication mutations. These deferrals do not waive the findings below.

Handoff: Return Ticket 5 to TDD correction. Establish Red evidence for each finding, make the smallest profile/test corrections, rerun the optimized and public-contract suites plus the canonical validator, preserve raw results, and submit the new final bytes to a different fresh independent reviewer. Do not mark Ticket 5 Completed or begin its context-reduction gate while these findings remain open.

Approval: Not applicable. This Review authorizes diagnosis and reporting only, not corrections.

## Findings

### [P1] The 30-scenario gate still validates prose patterns rather than executable behavior

Trigger: `tests/claude/test_claude5_profile.py:279-298` implements `scenario_failures` by concatenating Markdown and applying regular expressions; `:393-405` calls that matcher the fixed 30-scenario independent oracle. The fixture at `tests/claude/fixtures/claude-5-profile/scenarios.json:1-32` contains only IDs and source-module names—no starting capability/state, route input, user decision, expected transition/artifact/disclosure, prohibited action, or observable pass/fail output. The four adversarial cases at `test_claude5_profile.py:407-462` cover only selected textual edits. An independent in-memory probe confirmed that all four of these material mutations still return an empty failure list: replacing the actual-deletion authorization guard with “Actual deletion may proceed whenever useful”; deleting the conversation-only unread-repository/unexecuted-test safe-handoff contract; appending a contradictory `Add tests -> direct` / `Do not add tests -> tdd` instruction while retaining the expected sentence; and deleting the explicit “Never load or obey modules from another profile” guard.

Impact: Tests can report all 30 optimized scenarios passed while destructive-action safety, limited-evidence Review, Ticket-mode selection, or no-General-load behavior is wrong. The Core trace at `test_claude5_profile.py:464-479` is also only set-union coverage, so a rule marker can remain or move after its implementation is removed. This contradicts Ticket 5's TDD rationale and First Red (`docs/plans/claude-code-adapter-1.4.0.md:257`, `:283-293`), which explicitly reject static rule/text comparison as completion evidence, and does not prove the Specification's 100%-pass/no-skip behavior outcomes (`docs/specs/claude-code-adapter-1.4.0.md:304-339`).

Existing guard checked: The revised oracle is stronger than a fixture-controlled substring list: expectations live in test code, many regexes encode ordering, global contradictions reject several dangerous phrases, and four negative mutations prove selected regressions. Public-contract tests and the validator also protect exact bootstrap bytes and profile inventory/containment. None executes an optimized route through a capability/state transition or observes the stage result, and the validator does not validate profile semantics.

Remediation: Model each scenario with structured initial capability/state, public-entry route, user decision, expected loaded module/transition/artifact/status/disclosure, and prohibited actions. Execute those cases against a deterministic decision/load representation or equivalent behavioral harness instead of treating prose matches as pass. Bind each Core rule to its approved module/scenario and expected occurrence, and add mutation cases that remove or relocate the implementing behavior. At minimum, add Red mutations for approval and Ticket-mode inversions, conversation-only Review completion claims, actual deletion without all three gates, lifecycle writes without fresh authorization/state, and cross-profile references expressed without the literal `profiles/general` path.

### [P2] Removal is both excluded from write authority and missing the mandatory fresh pre-write state check

Trigger: `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/orchestration.md:105` says “Only an explicit install or update request authorizes writes” and “Re-read all state first.” Line 114 later permits a normal user-scope removal, but never requires an explicit remove request or repeats the fresh state/ownership check. On an explicit remove request—or when source/scope/identity changes after an earlier status result—the agent must choose between the categorical write-authority exclusion and the removal instruction.

Impact: The workflow may refuse every legitimate removal, or may uninstall from stale/ambiguous state without the explicit authorization and ownership proof required for a destructive mutation. This violates the Specification's requirement that **all** writes recheck Claude Code, Node, Marketplace source/scope, qualified identity, installed version, enabled state, and entry availability (`docs/specs/claude-code-adapter-1.4.0.md:228-244`), plus its explicit-request boundary at `:410`.

Existing guard checked: Line 103 prevents status requests from authorizing removal; line 110 stops on observed source/scope mismatch and ambiguity; line 114 fixes the qualified identity/user scope, preserves Marketplace/Config/other scopes, and gates `--keep-data`. Those safeguards do not establish a valid explicit remove authority or ensure the unsafe states were freshly observed before uninstall. The test oracle intentionally requires the flawed “only install or update” sentence at `test_claude5_profile.py:224-231`, while `REMOVE-ZIP` at `:232-236` checks neither explicit removal authority nor a fresh re-read.

Remediation: State that only an explicit install, update, **or remove** request authorizes the corresponding write, and require the same complete read-only state recheck immediately before each. Permit uninstall only when the fresh result proves the expected source, qualified identity, exact user scope, and unambiguous ownership; otherwise stop. Add a Red scenario where state changes between an earlier status and removal, plus mutations removing `remove` from either the authorization set or the pre-write recheck.

### [P2] Direct architecture requests conflict with the first-unmet Full gate order

Trigger: `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/orchestration.md:77` requires choosing the first unmet requirement/Specification/Plan/implementation/Review/completion condition. Line 79 says to honor an explicit stage choice unless it breaks a safety or approval gate, while lines 83-87 require selecting diagnostic architecture analysis when the user directly requests it. For a direct architecture-diagnosis request in a repository without an Approved Specification or Plan, line 77 routes to the earlier delivery gate while lines 79 and 85 route to diagnostic architecture.

Impact: The same valid input has two incompatible routes. Claude may divert a read-only architecture request into requirement delivery, or bypass its stated first-unmet algorithm nondeterministically. This is material because architecture diagnosis can be needed to inform a future Specification and, by its own module contract, authorizes no implementation.

Existing guard checked: `test_claude5_profile.py:145-154` requires the four architecture trigger phrases and accepted-report reflow; `:384-391` confirms those regexes match. It does not provide workflow state or assert which route wins when a direct request coexists with an unmet delivery gate. `architecture-improvement.md:5-13` correctly keeps diagnosis read-only and sends accepted proposals back through Specification/Plan/implementation, but cannot resolve whether orchestration may load it.

Remediation: Define a single precedence. Direct architecture-diagnosis requests should route to the diagnostic module after mode/capability/safety resolution without requiring delivery artifacts that the diagnosis may precede; automatic architecture transitions can retain their separately specified evidence triggers. Add a Red scenario starting with no Approved Specification/Plan and assert diagnosis occurs without edits, while an accepted report still returns to Specification.

## Verification performed

The reviewer independently ran:

```text
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_claude5_profile -v
Ran 8 tests in 0.154s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_claude5_profile tests.claude.test_public_plugin_contract -v
Ran 21 tests in 14.620s
OK
```

```text
.\.venv\Scripts\python.exe -B scripts\validate_claude_plugin.py --catalog .claude-plugin\marketplace.json --plugin adapters\claude-code\plugin\ask-then-do-it
Claude Plugin validation passed
```

Python compilation of `tests/claude/test_claude5_profile.py` and `scripts/validate_claude_plugin.py` exited `0` with no output. A no-write, in-memory mutation probe invoked the production test oracle and observed:

```text
unsafe_actual_deletion: []
weak_limited_evidence: []
contradictory_ticket_mode: []
removed_cross_profile_guard: []
```

The Ticket 5 Implementation Evidence raw sections record an original five-test Red, focused Green, router regressions, shared-validator Red/Green, broader repository summaries, later eight-test correction Red/Green, and a 21-test focused integration pass. Only those raw commands/results were read; their finding descriptions, defences, and proposed conclusions were excluded. This reviewer did not rerun the full repository suite.

## Evidence unavailable and untested areas

- No authenticated Claude Code `2.1.251` command/session behavior was available; Ticket 3 remains provisional and release-blocking.
- No model-executed optimized 30-scenario trace, structured decision output, prohibited-action trace, or isolated fresh transcript was present in Ticket 5.
- No paired General/Claude-5 behavior or bidirectional same-session profile-authority test was reviewed; Ticket 6 owns that later gate.
- No complete repository suite, live lifecycle mutation, package extraction, context measurement, or live smoke was run by this reviewer.
- Host-provided bare aliases and external/public transport remain unverified and out of Ticket 5 completion scope.

## Residual risks

Even after correcting these findings, deterministic instruction-contract tests cannot by themselves prove live-model compliance; Ticket 6 and the final live smoke remain necessary. Exact command identity and hook behavior remain provisional until Ticket 3. The current bootstrap exact-body validator and fixed contained profile-resource mapping are strong present-source guards, but the profile validator proves inventory/containment rather than stage semantics.

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — `finding`.** Full-stage routing authority is duplicated between the first-unmet sequence, explicit-stage rule, and architecture-trigger rule with conflicting outcomes; write authorization is duplicated between the install/update paragraph and remove paragraph. Findings P2 identify exact triggers and repairs.
2. **Long Function — `no-finding`.** `scenario_failures` is compact and the test methods are bounded. Their defect is semantic shallowness, not function length.
3. **Large Module or Class — `no-finding`.** The optimized profile separates orchestration from nine stage modules. `orchestration.md` is central by approved design, and no size-only split would resolve the reported defects.
4. **Long Parameter List — `not-applicable`.** Production artifacts are Markdown instruction modules and the test helpers expose no unstable long callable interface.
5. **Data Clumps — `finding`.** Scenario meaning requires capability, state, route, user decision, expected outcome, and prohibited actions, but the fixture retains only ID/module pairs while the rest is dispersed as regex primitives. This contributes directly to Finding P1.
6. **Primitive Obsession — `finding`.** Mandatory behavior and contradictions are encoded as regex strings over prose instead of constrained scenario states and decisions. This is the principal mechanism of Finding P1.
7. **Feature Envy — `not-applicable`.** No production module reaches through another module's internal data; stage dependencies are resource references.
8. **Divergent Change — `no-finding`.** Stage-specific rules remain separated into the approved ten modules. The actionable problems are local policy contradictions and the shared test representation.
9. **Shotgun Surgery — `no-finding`.** Each production correction can remain localized with its focused test. No cross-system refactor is needed to close these findings.
10. **Message Chains — `not-applicable`.** The reviewed production surface has no runtime object-navigation chain.
11. **Leaky Abstraction — `finding`.** Tests depend on exact prose fragments while callers need behavioral decisions; authors must understand regex internals, and semantically wrong instructions can satisfy the interface. This is Finding P1.
12. **Shallow Module — `finding`.** `scenario_failures` and the named independent 30-scenario test promise behavioral conformance but provide only text matching and a small contradiction blacklist. The gap is demonstrated by the four accepted unsafe mutations in Finding P1.

## Completion assessment

Ticket 5 does not appear complete. Current optimized modules are substantially aligned, progressive loading and bootstrap containment are well guarded, and all independently rerun present-byte checks pass. However, the Approved `tdd` behavior gate remains vulnerable to material false positives, removal authority/preflight is incomplete, and direct architecture routing is contradictory. Verdict: **Changes requested**.
