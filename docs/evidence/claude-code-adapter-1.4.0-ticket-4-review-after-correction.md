# Claude Code Adapter 1.4.0 Ticket 4 Review After Correction

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-4-review-after-correction`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Ticket: `4 - 交付 General profile 的完整工作流程`

Approved implementation mode: `tdd`

Review label: `independent`

Status: Changes requested

Inputs: Approved `docs/specs/claude-code-adapter-1.4.0.md`; Approved `docs/plans/claude-code-adapter-1.4.0.md` Ticket 4; the final ten files under `adapters/claude-code/plugin/ask-then-do-it/profiles/general/`; `tests/claude/test_general_profile.py`; `tests/claude/fixtures/general-profile/scenarios.json`; the two public Skill bootstraps; the shared Plugin validator's profile/bootstrap boundary; `docs/evidence/claude-code-adapter-1.4.0-ticket-4.md`; and the raw verification listed below. The prior Ticket 4 Review artifact was intentionally not read, and no implementer defence or proposed verdict was supplied to this reviewer.

Assumptions: This is a fresh review of final bytes, not a reconstruction of the implementing context. Ticket 3's authenticated Claude Code `2.1.251` command identity, `UserPromptExpansion`, resume/switch, and host failure semantics remain provisional. Ticket 6 still owns cross-profile paired/fresh-session comparison, but Ticket 4 itself remains responsible for a General-side deterministic 30-scenario gate that can reject incorrect behavior. The shared bootstrap and validator were examined only where they establish or constrain the General profile handoff.

Deferred: Authenticated Ticket 3 host behavior; Claude 5 profile behavior; Ticket 6 paired/fresh-session conformance; Ticket 7 context measurement; localized documentation; release/package integration; live smoke; and every external publication mutation. These deferrals do not waive the Ticket 4 findings below.

Handoff: Return Ticket 4 to TDD correction. Strengthen its scenario/rule/load-path oracles, repair the remove preflight and direct-architecture precedence instructions, obtain Red then focused Green evidence for each finding, rerun the General and public Plugin contract suites, and submit the corrected final bytes to another fresh independent Review. Do not mark Ticket 4 Completed while these findings remain open.

Approval: Not applicable. This Review authorizes diagnosis and reporting only; it does not authorize corrections.

## Findings

### [P1] The claimed executable 30-scenario gate is a keyword-presence linter and stays green when mandatory behavior is inverted

Trigger: `tests/claude/test_general_profile.py:248-266` normalizes each owning Markdown module and checks only for a scenario marker plus each `must_include` substring from `tests/claude/fixtures/general-profile/scenarios.json`. The test does not supply starting capability/state/input, execute a route or decision, compare an observable result, record pass/fail, or assert prohibited actions. Concrete inverse mutations can retain every required token: `ticket-planning.md:7` can map `Add tests` to `direct` and `Do not add tests` to `tdd`; `review.md:9-11` can swap the `tools` and `conversation` downgrade outcomes; `architecture-improvement.md:9` can make real deletion possible without all three guards; and `orchestration.md:151` can make `--keep-data` unconditional. The Core traceability check at `test_general_profile.py:240-246` likewise unions markers into a set, so a marker can be moved to an unrelated module or retained after its implementing rule text is removed. The no-cross-profile test at `test_general_profile.py:295-305` bans only two literal path spellings and accepts a contradictory instruction that refers to “the other profile” without those spellings.

Impact: The focused suite can report all 30 General scenarios and all 30 Core rules as passing while approval gates, TDD/direct selection, Review evidence labels, destructive-action safety, artifact behavior, or single-profile loading are wrong. That defeats the Approved Plan's reason for choosing `tdd` (`docs/plans/claude-code-adapter-1.4.0.md:205`) and its First Red/completion contract (`:233-241`), and it does not establish the Specification's 100%-pass/no-skip behavior gate (`docs/specs/claude-code-adapter-1.4.0.md:304-339`).

Existing guard checked: The suite correctly protects exact module inventory, exact Core-ID set membership, three parsed transition tables, the portable envelope field list, and several literal bootstrap/path strings. Those targeted guards do not establish the remaining stage decisions, rule-to-module ownership, prohibited outcomes, or actual loaded-module trace.

Remediation: Give every scenario structured starting capability/state/input, expected route/artifact/status/disclosures, and prohibited actions, then execute those cases against a deterministic decision representation or equivalent harness. Bind every Core rule to its approved module/scenario and expected occurrence, and add Red mutations that remove or relocate safety/gate rules. Record a General load trace that proves every loaded stage stays within the bound General directory and rejects conflicting other-profile authority. At minimum, add inverse mutations for every approval boundary, TDD/direct mapping, Review downgrade, deletion guard, lifecycle write, and ZIP/data-retention branch.

### [P2] Normal removal is permitted without the required fresh read-only ownership check

Trigger: `adapters/claude-code/plugin/ask-then-do-it/profiles/general/orchestration.md:138` requires a repeated read-only check only before install or update, while line 151 separately permits the qualified user-scope uninstall. If source, scope, identity, enabled state, or multi-scope ownership changes after an earlier status observation but before removal, the General instructions contain no requirement to re-observe that state immediately before the write.

Impact: The workflow can uninstall from stale or ambiguous state, or report a removal result against an ownership picture it never freshly established. This violates the Specification's “all writes” preflight requirement at `docs/specs/claude-code-adapter-1.4.0.md:230` and weakens the source/scope ambiguity stop boundary at lines 241-244.

Existing guard checked: Line 146 says to stop for source mismatch, non-user scope, multi-scope ambiguity, and unsafe ownership; line 151 fixes the qualified identity and `--scope user`. Those guards only help when current state has actually been read, and neither line makes a fresh pre-remove read mandatory. The scenario fixture checks removal command/data/ZIP keywords but not pre-remove state freshness.

Remediation: Require the same complete read-only state recheck immediately before install, update, **and remove**. Permit uninstall only when that fresh result proves the expected Marketplace/source, qualified identity, exact user scope, and unambiguous ownership; otherwise stop without writes. Add a Red scenario in which state changes between an earlier status result and the remove request, plus a mutation that deletes “remove” from the pre-write check.

### [P2] Direct architecture requests have two contradictory routing precedences

Trigger: `adapters/claude-code/plugin/ask-then-do-it/profiles/general/orchestration.md:89` places “an applicable architecture transition” after requirement consensus, Approved Specification, Approved Ticket Plan, implementation, and Review in the first-unmet Full gate order, and line 102 says to apply architecture routes only after checking that first unmet gate. Yet line 91 says to honor an explicit user-selected module, while lines 104-106 say a direct architecture request routes to `architecture-improvement.md` without an automatic-route announcement. With a direct architecture request in a repository that lacks an Approved Specification or Ticket Plan, the instructions therefore both require diagnosis now and require earlier delivery gates first.

Impact: Claude can nondeterministically enter architecture diagnosis or divert the user into requirements/specification/planning before a diagnostic-only request. The latter makes the explicit architecture route unusable precisely when architecture diagnosis may be needed to inform a future Specification, and the contradictory authority cannot be safely resolved by the model.

Existing guard checked: `test_general_profile.py:215-221` parses and protects the architecture transition table, and the correction mutation protects the focused-local-Review row. It does not inspect the first-unmet preamble or exercise a direct architecture request from an incomplete workflow state, so both contradictory clauses pass together. `architecture-improvement.md:3-13` correctly keeps the stage diagnostic-only and routes accepted proposals back through Specification, but it cannot resolve whether orchestration permits the stage to load.

Remediation: State one precedence explicitly. A direct architecture-diagnosis request should route directly to the diagnostic module after mode/capability/safety resolution and should not require delivery artifacts that the diagnosis may precede; automatic architecture transitions may retain their separately approved trigger timing. Add a scenario beginning with no Approved Specification/Plan and assert that the direct request loads diagnosis without authorizing implementation, while an accepted report still returns to Specification.

## Verification performed

The reviewer independently ran:

```text
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_general_profile -v
Ran 9 tests in 0.015s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_public_plugin_contract -v
Ran 13 tests in 14.428s
OK
```

```text
.\.venv\Scripts\python.exe -B scripts\validate_claude_plugin.py --catalog .claude-plugin\marketplace.json --plugin adapters\claude-code\plugin\ask-then-do-it
Claude Plugin validation passed
```

Python compilation of `tests/claude/test_general_profile.py` and `scripts/validate_claude_plugin.py` exited `0` with no output.

The supplied Implementation Evidence records its original Red, correction Red/Green, post-correction focused result, broader Claude/repository results, and exact strict-validation claims. This reviewer did not rerun the complete repository suite or an authenticated/live Claude Code session. Passing current-byte tests does not close Finding P1 because the issue is the oracle's inability to reject meaningful inverse mutations.

## Evidence unavailable and untested areas

- No authenticated Claude Code `2.1.251` session behavior was available in this Ticket; Ticket 3 remains the explicit gate.
- No model-executed General 30-scenario result, structured decision trace, prohibited-action trace, or fresh-transcript behavior evidence exists in the reviewed Ticket 4 fixture.
- No paired General/Claude-5 behavior or same-session authority-precedence result was reviewed; Ticket 6 owns that later gate.
- No full repository suite was rerun in this reviewer context. The supplied broader raw summaries were treated as implementation evidence, not as independently observed execution.
- No live install/update/remove/ZIP mutation was performed; this Review did not authorize external or persistent host changes.

## Residual risks

Even after the three findings are corrected, Markdown instruction conformance cannot by itself prove that a live model follows every instruction; the later paired/fresh-session and live-smoke gates remain necessary. Exact host command identity and `UserPromptExpansion` behavior remain provisional. The current bootstrap exact-body validator is a strong guard for the public handoff, but its profile validation proves containment and inventory, not the semantics of the General modules.

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — `finding`.** Direct architecture precedence is expressed in the first-unmet order, the explicit-module rule, the architecture preamble, and the transition table with contradictory results. Finding P2 describes the trigger, impact, locations, and correction.
2. **Long Function — `not-applicable`.** Production scope is Markdown instruction modules rather than callable functions; the focused Python helpers/methods do not present a separate actionable long-function defect.
3. **Large Module or Class — `no-finding`.** `orchestration.md` is broad but serves the approved central coordination role, while stage-specific behavior is split across nine bounded modules. No size-only defect beyond the concrete precedence conflict was found.
4. **Long Parameter List — `not-applicable`.** The reviewed production interface is instruction/resource loading, and no unstable callable parameter list exists in scope.
5. **Data Clumps — `no-finding`.** Portable artifact fields and transition rows are deliberately grouped in central definitions; no repeated loose field group creates an additional actionable defect.
6. **Primitive Obsession — `finding`.** Scenario and Core conformance are represented as unconstrained marker/substring primitives instead of typed starting states, decisions, expected outcomes, and prohibited actions. This is part of Finding P1.
7. **Feature Envy — `not-applicable`.** The Markdown stages do not reach through another module's internal data; the allowed dependencies are explicit orchestration and bootstrap contracts.
8. **Divergent Change — `no-finding`.** Although orchestration coordinates several policies, the stage split localizes implementation, Review, Lite, and architecture changes. No extra divergent-change remediation is justified beyond the named findings.
9. **Shotgun Surgery — `no-finding`.** The shared portable envelope and central transition tables reduce synchronized edits; the remove preflight correction is local and its test, not a cross-module redesign.
10. **Message Chains — `not-applicable`.** No runtime object-navigation or chained call surface exists in the reviewed General instruction modules.
11. **Leaky Abstraction — `finding`.** The tests must know exact prose fragments but cannot observe the decisions those fragments are meant to implement; contradictory prose can satisfy the interface. This is part of Finding P1.
12. **Shallow Module — `finding`.** `test_fixed_thirty_scenarios_have_executable_general_contracts` presents an executable-behavior interface while providing only marker/substring presence checks. The interface promise materially exceeds the hidden functionality, as detailed in Finding P1.

## Completion assessment

Ticket 4 does not yet appear complete. The current General bytes cover most approved behavior and the focused/public validation runs pass, but one TDD evidence gap allows high-impact inverse behavior to remain green and two production instructions diverge from or contradict the Approved Specification. Verdict: **Changes requested**.
