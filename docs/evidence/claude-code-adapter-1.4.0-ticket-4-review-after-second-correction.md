# Claude Code Adapter 1.4.0 Ticket 4 Fresh Independent Review After Second Correction

artifact_type: Review Report

artifact_id: `claude-code-adapter-1-4-0-ticket-4-review-after-second-correction`

workflow_id: `claude-code-adapter`

core_version: `1.3.0`

Target release version: `1.4.0`

Ticket: `4 - 交付 General profile 的完整工作流程`

Approved execution mode preserved: `tdd`

status: Changes requested — one actionable P1 finding; Ticket 4 is not complete

Review label: `independent`. This reviewer did not implement or correct the General profile. The verdict was rebuilt from the Approved Specification and Ticket 4, current final bytes, focused tests, public bootstrap/shared-validator boundaries, and raw command results. Earlier Ticket 4 Review verdicts and implementer defenses were not used.

inputs: Approved `docs/specs/claude-code-adapter-1.4.0.md`; Approved `docs/plans/claude-code-adapter-1.4.0.md` Ticket 4 with mode `tdd`; the ten current files under `adapters/claude-code/plugin/ask-then-do-it/profiles/general/`; `tests/claude/test_general_profile.py`; `tests/claude/fixtures/general-profile/scenarios.json`; `docs/evidence/claude-code-adapter-1.4.0-ticket-4.md` for raw command/result records only; both public Skill bootstraps; and the canonical Claude Plugin validator/public contract boundary.

assumptions: The current workspace bytes are the review target. The General scenario harness is evaluated as deterministic instruction-contract evidence, not as live-model adherence, authenticated Claude host behavior, or Ticket 6 paired equivalence. Because Ticket-owned files are untracked, this review does not claim a reconstructable clean Ticket-only Git diff.

deferred: Ticket 3 authenticated Claude Code host ledger; Ticket 6 paired/fresh-session conformance and same-session bidirectional authority; Ticket 7 context measurement; localized documentation, release integration, clean live smoke, and all external publication mutations.

handoff: Return the finding to Ticket 4's Approved `tdd` correction path. Strengthen the oracle so additive contradictions cannot retain a green result, observe focused Red on the current contract, apply only the minimum General-test/representation correction needed, rerun General and public boundaries, and request another fresh independent Review. Do not modify the Approved Specification, Plan, Claude 5 profile, router, Project Knowledge Base, or publication state to hide the finding.

## Finding

### [P1] The structured scenario oracle still false-passes additive inverse semantics

**Trigger:** A maintainer preserves the expected sentence or transition table but appends a later instruction that reverses it. **Impact:** The suite remains green while Claude receives contradictory authority for Ticket test-mode selection, cross-profile control, destructive remove authorization, or direct architecture precedence. This defeats Ticket 4's requirement that tests—not static text presence—prove the 30 mandatory General outcomes and can permit an unsafe or gate-bypassing profile to be treated as complete. **Evidence:** `assert_scenario_contracts` in `tests/claude/test_general_profile.py:483` only checks that expected substrings exist and a few exact prohibited substrings do not; `assert_no_affirmative_cross_profile_load` at `:511` recognizes only `load|follow|obey` plus four profile adjectives; and the transition validators at `:539` and `:555` compare the expected table/required sentence without rejecting a later contradiction. Four read-only in-memory mutations all exited `0` and printed `FALSE_PASS`: “Add tests uses direct / Do not add tests uses tdd”; “treat the other profile as authoritative”; “normal remove may reuse the earlier status result”; and “unresolved Requirements take precedence over a direct architecture request.” Current production wording at `ticket-planning.md:9` and `orchestration.md:13,104,152` is correct, so this is a test-gate defect rather than a claim that the present prose already contains those reversals. **Remediation direction:** Validate an exact normalized authoritative section or a structured decision representation for these gates, and add preservation-plus-additive-contradiction mutations for every authority/safety transition. The gate must reject contradictory later clauses without depending on one small vocabulary of inverse phrases.

No additional P0, P1, P2, or P3 production finding was identified in the reviewed scope.

## Verification performed

- `python -B -m unittest tests.claude.test_general_profile -v` → `Ran 11 tests in 0.037s`, `OK`. This includes the existing replacement-style inverse mutations, exact Core owner relocation rejection, General load-trace checks, normal-remove fresh-recheck replacement, and direct-architecture precedence replacement.
- `python -B -m unittest tests.claude.test_public_plugin_contract -q` → `Ran 13 tests in 15.148s`, `OK`.
- `python -B scripts/validate_claude_plugin.py` → exit `0`, canonical Plugin validation passed.
- Four additional in-memory additive contradictions described in the finding each exited `0`, proving the false-pass. They did not write repository files.
- The current General production modules were inspected against capability honesty, Full/Lite gates, portable artifacts, Config transitions, architecture/knowledge routes, lifecycle writes, Review downgrade, cross-profile/model authority, and publication boundaries. Their authored instructions were materially consistent with the Approved Ticket in this review scope.

## Evidence unavailable and residual risks

- Historical Red/Green runs recorded in the Implementation Evidence were read as raw records and were not replayed by replacing current production bytes.
- No live Claude response, authenticated namespaced invocation, `additionalContext`, install/update/remove mutation, fresh-session paired comparison, context measurement, package build, or live smoke was performed.
- Exact rule-to-module ownership now rejects removal or relocation of declarations and markers. It does not by itself prove the implementing prose; the P1 finding covers the remaining semantic-proof gap.
- Public bootstraps and the shared validator correctly constrain current profile selection, inventory, and contained paths, but they do not validate General module semantics and therefore do not close the finding.

## Ticket completion assessment

**Changes requested.** Ticket 4 does not yet appear complete because its mandatory 30-scenario TDD gate accepts additive instructions that reverse core authority and safety outcomes. The current General production prose otherwise appears contract-complete within the reviewed scope.

## Twelve Core Architecture and Refactoring Lenses

| # | Core lens | Outcome | Evidence / scope-specific reason |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `no-finding` | Current shared orchestration owns common profile policy, while stage modules reference the portable envelope and retain bounded stage responsibilities. |
| 2 | Long Function | `no-finding` | The test helpers are individually short and cohesive; the false-pass comes from their validation model, not function length. |
| 3 | Large Module or Class | `no-finding` | `orchestration.md` is large but owns the approved always-loaded coordination boundary; headings and parsed tables keep its responsibilities navigable. |
| 4 | Long Parameter List | `not-applicable` | No reviewed public function or profile interface exposes a positional parameter list; route/artifact values use named contracts. |
| 5 | Data Clumps | `no-finding` | `ScenarioContract` and the named transition tuples group related values coherently instead of passing loose positional data across production modules. |
| 6 | Primitive Obsession | `finding` | Mandatory semantics are represented as unconstrained string fragments. Presence/absence checks cannot distinguish a valid policy from the same text plus an additive reversal; this is the P1 finding. |
| 7 | Feature Envy | `no-finding` | General modules consume bootstrap authority without reaching into router state, and the public validator owns only Plugin/profile boundary validation. |
| 8 | Divergent Change | `no-finding` | The reviewed General orchestration changes around one provider/profile coordination contract; no unrelated reason-to-change split is evidenced. |
| 9 | Shotgun Surgery | `no-finding` | The remaining defect can be addressed in the General oracle/contract representation without changing router, Claude 5, Specification, or lifecycle production policy. |
| 10 | Message Chains | `no-finding` | Public bootstrap → General orchestration → one owned stage is the approved progressive-load chain and current production does not expose a longer internal navigation chain. |
| 11 | Leaky Abstraction | `finding` | Callers must know that “structured contract passed” means only selected substrings/tables survived, not that later contradictory authority is absent. This is another manifestation of the P1 finding. |
| 12 | Shallow Module | `finding` | `ScenarioContract` presents input/outcome/prohibition structure but hides very little semantic validation beyond substring membership, allowing all four additive inversions to pass. This is the P1 finding. |
