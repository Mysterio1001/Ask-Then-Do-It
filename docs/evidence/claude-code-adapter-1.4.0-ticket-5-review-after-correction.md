# Claude Code Adapter 1.4.0 Ticket 5 Fresh Independent Review After Correction

artifact_type: Review Report

artifact_id: `claude-code-adapter-1-4-0-ticket-5-review-after-correction`

workflow_id: `claude-code-adapter`

core_version: `1.3.0`

Product authoring baseline: `1.3.1`

Target release version: `1.4.0`

Ticket: `5 - 交付 Claude 5-optimized profile 的完整工作流程`

Approved execution mode preserved: `tdd`

status: Changes requested — two actionable P2 findings; Ticket 5 is not complete

Review label: `independent`. This fresh reviewer implemented only the separate General profile and did not implement or correct the Claude 5 profile. The reviewer did not read the prior Ticket 5 Review findings or any implementer defense, and reached this verdict from the Approved artifacts, final bytes, tests, shared boundaries, and raw results listed below.

inputs: Approved `docs/specs/claude-code-adapter-1.4.0.md`; Approved `docs/plans/claude-code-adapter-1.4.0.md` Ticket 5 with mode `tdd`; final ten files under `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/`; `tests/claude/test_claude5_profile.py`; `tests/claude/fixtures/claude-5-profile/scenarios.json`; `docs/evidence/claude-code-adapter-1.4.0-ticket-5.md` for raw command/result records only; both public Skill bootstraps; the canonical Claude Plugin validator and public contract tests; the read-only Plugin reviewer; Core rules, orchestration, artifact, Review, and architecture contracts.

assumptions: The review target is the current workspace final bytes. Because these Claude Adapter files are not represented by a clean committed Ticket-only baseline, the review evaluates final content and surrounding contracts rather than claiming a reconstructable narrow Git diff. The 30-scenario tests are treated as deterministic instruction-contract evidence, not as live-model adherence or Ticket 6 paired equivalence.

deferred: Ticket 3 authenticated exact-host invocation, `additionalContext`, loading, resume/switch, and failure-semantics ledger; Ticket 6 paired fresh-session equivalence and same-session bidirectional authority; Ticket 7 context measurement; localized documentation, release integration, clean live smoke, and all external publication mutations. These deferred gates neither cause nor excuse the two findings below.

handoff: Return the two findings to Ticket 5's Approved `tdd` implementation path. Add focused contradiction/transition tests that first fail on the current bytes, make the smallest Claude-5-only corrections, rerun the Claude 5/public contract surfaces, and request another fresh independent Review. Do not modify the Approved Specification, Plan, General profile, router, Knowledge Base, or publication state to hide these findings.

## Findings

### [P2] Automatic known-Claude-5 entry conflicts with the profile's explicit-bootstrap-only entry gate

**Trigger:** The user invokes the automatic namespaced entry on a known Claude 5 model; its validated route selects `claude-5`, and the automatic public Skill loads the optimized orchestration resource. **Impact:** The first gate says it accepts exactly three states “established by the explicit public bootstrap,” which excludes the automatic bootstrap under this product's defined automatic-versus-explicit vocabulary. The same file later says automatic known Claude 5 may enter. A model following the earlier exact gate can therefore reject the primary automatic Claude 5 path, while following the later sentence accepts it; behavior is non-deterministic despite a valid ready binding. **Evidence:** `profiles/claude-5/orchestration.md:7-12` restricts all three states to the explicit bootstrap, while `:39` explicitly allows automatic known Claude 5. `skills/ask-then-do-it/SKILL.md:24` maps a ready automatic `selected_profile: claude-5` route to this exact resource. `test_claude5_profile.py:308-323` independently checks the ready-envelope phrase and later route phrases but does not reconcile bootstrap identity, so both contradictory statements pass together. **Remediation direction:** Make state 1 valid when established by either approved public bootstrap while keeping the two manual states exclusive to the explicit `-5` bootstrap. Add an automatic-ready versus explicit-ready/manual transition oracle and a contradiction mutation that makes ready state exclusive to the explicit entry.

### [P2] Conversation-only mode resolution has no host-unavailable Config transition

**Trigger:** Capability is `conversation`, no explicit Full/Lite instruction exists, and the host cannot expose the project Config; either the user Config is available and valid or it is also unavailable. **Impact:** The profile only defines filesystem `absent` and invalid cases. It does not say a host-unavailable project source is treated as absent and continues to an available user source, or that an unavailable user source is absent and reaches Full fallback. The workflow may stall, ask the user for a default that the host cannot inspect, or imply it read a file, violating capability honesty and the mandatory canonical mode resolver. **Evidence:** `profiles/claude-5/orchestration.md:58-69` defines explicit, absent, and invalid transitions but no unavailable-source outcome. Core `modules/orchestration.md:38-43` explicitly requires both host-unavailable sources to be treated as absent. The `MODE-CONFIG` oracle at `test_claude5_profile.py:91-95` checks paths and “both absent” only. An in-memory adversarial mutation appending “If conversation capability cannot expose either Config, stop and ask the user” produced `MODE-CONFIG: FALSE-PASS: []`, confirming the current oracle does not enforce the missing transition. **Remediation direction:** Add deterministic conversation/no-explicit transitions for project unavailable → available user Config, project unavailable → user unavailable → Full fallback, and project absent → user unavailable → Full fallback; prohibit claiming an unavailable source was read or was invalid. Add mutation coverage for wrong fallthrough and fabricated-read behavior.

No P0, P1, or P3 findings were identified.

## Verification performed

Focused Claude 5 plus shared public Plugin contracts were independently rerun:

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_claude5_profile tests.claude.test_public_plugin_contract -v
```

Observed:

```text
Ran 19 tests in 14.841s

OK
```

This directly passed the exact ten-module/no-subdirectory inventory, all 30 Core traces, the 30 test-owned scenario patterns, deterministic resource-path/allowlist/containment clauses, ready and two manual states, public bootstrap path mapping, shared profile inventory/path guards, reviewer boundary, route disclosures, and the four existing adversarial mutations.

Additional independently observed checks:

- Canonical `scripts/validate_claude_plugin.py` with explicit catalog and Plugin paths: exit `0`, `Claude Plugin validation passed`.
- Node syntax for `scripts/router.mjs`: exit `0`, no output.
- Scoped search for General-profile paths, parent traversal, model frontmatter, `claude --model`, `ANTHROPIC_MODEL`, or instructions to switch/override/pin the active model: no matches.
- Scoped `git diff --check` over the Claude 5 profile/test/fixture: exit `0`, no output.

The reviewer also ran four in-memory contradiction mutations against the final test oracle. All four false-passed with an empty failure list: conversation Config unavailable → stop; an appended wrong normal-remove command; removal of approval evidence from the common-artifact validation sentence; and automatic acceptance of a rejected architecture report. Only the first corresponds to an observed final production omission and is reported above. The other probes demonstrate residual oracle limits but are not reported as production findings because the final bytes retain the applicable positive contracts.

## Evidence unavailable or not independently reproduced

- Historical Ticket 5 Red/Green and correction Red/Green cannot be replayed without replacing final production bytes. The raw summaries in the implementation evidence were inspected but not treated as a verdict.
- The coordinator supplied a current 339-test full-repository raw result, and the implementation evidence records earlier central 118/334-test results. This reviewer did not rerun the full repository suite and does not use those summaries to override source-level findings.
- Exact Claude Code `2.1.251` strict-validation results were supplied but not rerun here. Strict schema success is not authenticated command/loading behavior.
- No live model response, namespaced invocation, `additionalContext`, install/update/remove mutation, paired profile comparison, context measurement, build, or live smoke was performed.

## Residual risks and untested areas

- The static oracle catches the four implemented mutations but is not generally contradiction-complete. The two findings show concrete false-pass states involving interaction between otherwise passing positive clauses.
- Lifecycle instructions preserve source, identity, user scope, state matrix, disabled preference, partial-failure recheck, removal/data, reload, and ZIP outcomes, but Ticket 6 still owns fresh-session behavioral proof of those outcomes.
- Cross-profile loading and active-model override searches are clean, while actual General↔Claude-5 same-session authority remains correctly deferred to Ticket 6.
- Ticket 3 host behavior and Ticket 7 context reduction remain release gates. No context-reduction claim is accepted from module brevity alone.

## Ticket completion assessment

**Changes requested.** Ticket 5 is not complete because its primary automatic known-Claude-5 entry has contradictory bootstrap authority and its conversation-only Config resolver lacks mandatory unavailable-source transitions. The remaining examined loader/manual, route, capability, Full/Lite, Review, architecture, lifecycle, security, cross-profile, model-authority, and release-boundary instructions contain no additional verified actionable defect in this review scope.

## Twelve Core Architecture and Refactoring Lenses

This lens pass covers only the Ticket 5 Claude 5 profile, its focused oracle/fixture, and directly surrounding bootstrap/validator/reviewer boundaries.

| # | Core lens | Outcome | Evidence / scope-specific reason |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `finding` | Entry authority is expressed at `orchestration.md:7` and again at `:39`, with conflicting automatic/explicit scope. Centralize the distinction in one closed entry-state table or make the shared gate terminology exact. |
| 2 | Long Function | `not-applicable` | Ticket 5 production consists of Markdown instruction modules, not executable functions; no changed function body exists in this scope. |
| 3 | Large Module or Class | `no-finding` | Orchestration is the largest module but remains the Approved always-loaded owner for routing, capability, mode, session, and lifecycle coordination; headings and one-stage progressive loading keep responsibilities navigable. |
| 4 | Long Parameter List | `not-applicable` | No positional public API or function parameter list is introduced by the profile. Route and artifact values use named, bounded contracts. |
| 5 | Data Clumps | `no-finding` | Route tuple, capability names, module inventory, and artifact fields are maintained as coherent closed contracts rather than repeated loose positional values. |
| 6 | Primitive Obsession | `no-finding` | Profile/module names and scenario IDs are strings, but fixed allowlists, exact inventories, and validator containment checks constrain them. |
| 7 | Feature Envy | `no-finding` | Public Skills own envelope/bootstrap validation; optimized orchestration owns stage selection and workflow policy; the final modules do not reach into router state or General internals. |
| 8 | Divergent Change | `no-finding` | The orchestration module has several coordinated policies, but they all change for the same Claude host/profile contract; no unrelated change axis requiring a new approved module is evidenced. |
| 9 | Shotgun Surgery | `no-finding` | Each finding can be corrected in Claude 5 orchestration plus its focused oracle without changing router, General, shared conformance, or public identity. |
| 10 | Message Chains | `no-finding` | Public bootstrap → bound orchestration → one allowlisted stage is the intended progressive-disclosure chain; no extra navigation through session or cross-profile internals is present. |
| 11 | Leaky Abstraction | `finding` | The phrase “explicit public bootstrap” leaks command-family identity into an otherwise route-state-based gate, forcing the loaded profile to distinguish which bootstrap loaded it and contradicting the valid ready binding. |
| 12 | Shallow Module | `finding` | The scenario oracle exposes broad positive regexes but does not hide or enforce the interaction semantics for bootstrap identity or capability×Config transition; both defects remain Green until explicit transition/contradiction tests are added. |
