# Claude Code Adapter 1.4.0 Ticket 5 Independent Review

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-5-review`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Status: Changes requested

Review label: `independent`

Approved implementation mode: `tdd`

Inputs: Approved [Claude Code Adapter 1.4.0 Specification](../specs/claude-code-adapter-1.4.0.md), Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 5, Core `1.3.1` rules/modules/artifact contracts, repository [Claude Code feasibility analysis](../claude_sys/claude-code-adapter-feasibility-analysis.md) and its dated Anthropic Claude 5 context-engineering/Claude Code references, the final Claude 5 profile and public-bootstrap/shared-inventory integration scope, focused tests/fixtures, [Ticket 5 Implementation Evidence](claude-code-adapter-1.4.0-ticket-5.md), supplied raw results, and independent verification recorded below.

Assumptions: This reviewer did not implement Ticket 5, received no proposed verdict, and deliberately did not read the Ticket 4 Review Report. The cumulative uncommitted worktree has no commit boundary for Ticket 5, so ownership was reconstructed from the Approved Ticket and named final scope. Passing static prompt checks are evidence of authored text, not evidence that Claude Code loaded or followed it.

Deferred: Ticket 3 authenticated/live host observations, Ticket 6 paired equivalence and bidirectional same-session authority, Ticket 7 formal per-checkpoint 50% context measurement, Ticket 9 release integration, and Ticket 10 live smoke remain their normal downstream gates. None is reported as a Ticket 5 defect below.

Handoff: Return F1-F3 to Ticket 5 `implement-tdd`. Add meaningful failing checks before correcting production prompt contracts, rerun focused/shared/Claude verification, then send the corrected raw diff and results to a fresh independent Review. Do not start Tickets 6 or 7 while these profile-loading, mandatory-Full-routing, and test-efficacy findings remain open.

## Findings

### P2 F1 — The optimized profile has no deterministic module handoff, and both manual routes contradict its entry invariant

Trigger: any successful explicit/automatic Claude 5 route reaches a bootstrap that says only to load “orchestration and stage instructions from the selected profile,” without naming or linking the Plugin-relative `profiles/claude-5/orchestration.md` resource; after the file is somehow found, it names subsequent modules only by bare filename. The two permitted Node-manual routes are additionally told to load the optimized profile without an operation binding, while `orchestration.md` says it may be entered only after a validated ready envelope bound `selected_profile: claude-5` to a new operation. Impact: the promised progressive-disclosure chain is not a bounded, executable mapping for a conversation-capability invocation, and the approved `node-too-old`/genuinely-missing-Node explicit paths can reach an instruction that rejects their own deliberately unbound state. The host may fail to find the module, guess a same-named resource, or stop a route that acceptance criterion 7 requires to continue with honest limitations. Evidence/location: `skills/ask-then-do-it-5/SKILL.md:22-28`, `skills/ask-then-do-it/SKILL.md:26`, and `profiles/claude-5/orchestration.md:5-23,30`; repository search finds no Skill-to-`profiles/claude-5` path or other module resolver. Remediation: give each selected profile a deterministic, containment-safe Plugin resource reference/load protocol, and make the optimized entry invariant explicitly admit the two approved manual states without inventing an operation binding, resume, or switch authority. Protect ready and both manual branches with negative tests for missing/wrong targets and contradictory entry guards.

### P2 F2 — Full routing can complete without mandatory architecture and durable-knowledge handoffs

Trigger: a Full Review exposes systemic architecture evidence, a related Ticket group completes, a release milestone approaches, or an Approved/accepted artifact changes durable project facts after requirement interrogation. The optimized orchestrator's first-unmet list ends at Review then completion and only says that architecture contracts and Knowledge Base synchronization are retained “where applicable”; it never gives the Core architecture-selection triggers, automatic-route announcement, local-versus-systemic distinction, or the post-artifact Project Knowledge synchronization route. Impact: Claude can follow the optimized prompt exactly and announce completion while skipping mandatory diagnostic architecture routing or leaving durable formal knowledge unsynchronized, contrary to `FULL-PRESERVE-001`, `ROUTE-DOCS-001`, Specification section 7, and the Ticket 5 requirement to preserve Full/knowledge/architecture behavior. The presence of `architecture-improvement.md` does not make an unreachable automatic branch executable. Evidence/location: `profiles/claude-5/orchestration.md:59-67`; compare `core/modules/orchestration.md` sections “Route Full architecture diagnosis” and “Synchronize durable knowledge.” Remediation: restore the compact but explicit architecture and durable-knowledge routing conditions/handoffs in the optimized orchestrator, including the rule that a focused local Review finding remains in Review and that architecture-report acceptance is diagnosis-only.

### P2 F3 — The claimed 30-scenario TDD gate is a self-referential substring oracle and demonstrably false-passes

Trigger: profile text keeps a fixture phrase somewhere while adding a contradictory instruction, making the branch unreachable, or deleting behavior that the fixture did not quote. `test_fixed_thirty_scenario_inventory_has_every_required_outcome` merely concatenates fixture-selected Markdown and performs case-insensitive substring membership; the rule test likewise treats a `Core rules:` label as executable coverage. An independent in-memory mutation replaced “Honor an explicit stage or requirement-mode choice…” with “Never honor an explicit user-selected stage or requirement mode,” and all five Claude 5 profile tests still reported `OK`. The suite also passes the F1 entry contradiction and F2 missing routes. Impact: the tests cannot establish Ticket 5's required 30 optimized behavior scenarios, can remain green when mandatory Core behavior is reversed, and therefore do not provide the approved `tdd` confidence or completion gate claimed by the implementation evidence. Ticket 6's later cross-profile harness does not waive Ticket 5's own Red/Green behavior requirement. Evidence/location: `tests/claude/test_claude5_profile.py:92-124,144-166` and `tests/claude/fixtures/claude-5-profile/scenarios.json` (notably the one-sided required fragments for `MODE-EXPLICIT`, `FULL-ARCH`, and route scenarios). Remediation: replace author-controlled phrase presence with independent, branch-oriented prompt-contract evaluation that rejects contradictory/missing guards and proves the loader selects only the expected modules/outcomes for all 30 cases; retain inventory and rule-ID checks only as supplementary static checks. Add mutation/negative cases for the defects above.

## Verification performed

- `& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_general_profile tests.claude.test_claude5_profile tests.claude.test_public_plugin_contract` — exit `0`; `Ran 23 tests in 13.715s`; `OK`.
- Independent verifier: `& '.\.venv\Scripts\python.exe' -m unittest tests.claude.test_claude5_profile tests.claude.test_public_plugin_contract` — exit `0`; `Ran 17 tests in 14.352s`; `OK`.
- `& '.\.venv\Scripts\python.exe' -B -m unittest discover -s tests\claude -p 'test_*.py'` — exit `0`; `Ran 118 tests in 69.706s`; `OK (skipped=1)`. The skip is the Windows symlink-privilege case.
- `& '.\.venv\Scripts\python.exe' -B scripts\validate_claude_plugin.py` — exit `0`; canonical Plugin validation passed without warning.
- `node --check adapters\claude-code\plugin\ask-then-do-it\scripts\router.mjs` — exit `0`; no output/warning.
- Scoped `git diff --check` over the Ticket 5 profile/test/fixture and shared validator/public-contract files — exit `0`; no output.
- Adversarial in-memory mutation of the explicit user-routing instruction — exit `0`; all `5` optimized-profile tests still passed, confirming F3 without modifying the worktree.
- The supplied Red/Green/integration/full-suite summaries and exact Claude Code `2.1.251` strict Plugin/Marketplace exit-`0` results were read as raw reported evidence only; implementer conclusions were not adopted.

## Evidence unavailable

- Bare `python` is not on this PowerShell `PATH`; the repository `.venv` Python `3.12.14` was used instead.
- This reviewer did not rerun the supplied full-repository `334`-test command or exact Claude Code `2.1.251` native strict validations. Their reported raw summaries remain supplied evidence.
- No authenticated Claude Code invocation, fresh transcript, real module-load trace, model switch, resume/compact observation, or live conversation-only invocation was performed. Those observations remain downstream Ticket 3/6/10 evidence, but they cannot repair the static F1 contradiction.
- Formal cross-profile equivalence and the 50% context proxy were not assessed because Tickets 6 and 7 own those gates.

## Residual risks and untested areas

- Static inventory validation correctly rejects missing/extra profiles and modules, but it does not validate semantic module reachability or prompt contradictions.
- The exact native Plugin schema result does not prove that a conversation can resolve the internal profile paths or obey the intended progressive load order.
- Other compressed clauses may have the same false-pass pattern as F2 because the fixture and production wording share ownership; a corrected test design should mutation-test all thirty outcomes rather than patch only the quoted examples.
- The Windows symlink-security branch remains skipped under current privileges; existing deterministic tests cover its non-privileged paths.

## Completion assessment

Ticket 5 does **not** appear complete. The ten-file inventory, compact stage split, Core-ID trace, shared Plugin inventory integration, and broad regressions are present and green, but F1 leaves optimized progressive loading/manual entry internally non-executable, F2 omits mandatory Full routes, and F3 means the required 30-scenario `tdd` gate has not been demonstrated. Status remains `Changes requested`.

## Twelve Architecture and Refactoring Lenses

| # | Lens | Outcome | Evidence |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `finding` | Manual-entry policy is repeated in the explicit Skill and optimized orchestrator with incompatible operation-binding preconditions (F1). |
| 2 | Long Function | `not-applicable` | The reviewed optimized profile is declarative Markdown; no changed function is in Ticket 5's production scope. |
| 3 | Large Module or Class | `no-finding` | `orchestration.md` is the intentional compact entry coordinator and delegates nine stages to separate modules; size itself did not create an additional finding beyond the missing routes. |
| 4 | Long Parameter List | `not-applicable` | Ticket 5 adds no callable interface or parameter list; route-envelope shape belongs to the surrounding bootstrap contract. |
| 5 | Data Clumps | `not-applicable` | The profile stores or passes no runtime data structure; the bounded route envelope is reviewed at the bootstrap boundary rather than duplicated as an unmodeled value group here. |
| 6 | Primitive Obsession | `finding` | Semantic scenario outcomes and Core conformance are represented as unconstrained phrase strings and header labels, producing F3's false pass. |
| 7 | Feature Envy | `no-finding` | Stage-specific behavior resides in its owning module; no reviewed stage primarily manipulates another module's data or responsibility. |
| 8 | Divergent Change | `no-finding` | The ten-module split gives workflow stages separate change owners; available history/diff evidence shows no unrelated reasons accumulating in a stage module. |
| 9 | Shotgun Surgery | `finding` | One manual-route rule is maintained across bootstrap text, orchestration text, fixture phrases, validator constants, and public tests; the inconsistent guard in F1 demonstrates the resulting multi-location change risk. |
| 10 | Message Chains | `not-applicable` | No object navigation or runtime call chain is introduced by these Markdown modules. |
| 11 | Leaky Abstraction | `finding` | The “selected profile” handoff requires the consumer to infer undisclosed Plugin paths and reconcile an operation-binding detail that the bootstrap intentionally omits on manual routes (F1). |
| 12 | Shallow Module | `finding` | The test named as a thirty-scenario gate exposes a rich scenario inventory but hides only substring membership, not behavioral enforcement (F3). |

