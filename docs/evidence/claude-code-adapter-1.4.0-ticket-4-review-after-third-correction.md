# Ticket 4 General profile — Review after third correction

Review label: `independent`

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-4-review-after-third-correction`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0` (Review workflow contract; the Approved Specification and Ticket use the repository's `1.3.1` behavioral baseline.)

Status: Reviewed — no actionable finding in the correction; Ticket 4 completion remains pending.

Date: 2026-09-09

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md), Approved [Ticket Plan, Ticket 4](../plans/claude-code-adapter-1.4.0.md#ticket-4--交付-general-profile-的完整工作流程), `core/rules/rules.yaml`, all ten final General modules, `tests/claude/test_general_profile.py`, all three `tests/claude/fixtures/general-profile/` files, both public Skill bootstraps, the relevant shared validator and public contract tests, the raw third-correction verification record in [Ticket 4 evidence](claude-code-adapter-1.4.0-ticket-4.md), and the subsequent direct-architecture lens correction and its supplied raw Red/Green results.

Assumptions: The coordinator established current-operation Full fallback and `multi_agent` capability. Ticket 4 remains Approved `tdd`; its test choice has not changed. The initial correction changed the General test gate and its fixture/documentation. The final candidate additionally supplies the canonical twelve-lens list directly in `architecture-improvement.md`, with its focused regression and corresponding fixture update. The relevant implementation files are untracked, so this review inspects final files and recorded hashes rather than claiming a clean commit diff. This separate reviewer did not implement either correction or adopt earlier review verdicts as proposed conclusions.

Deferred: Actual model-executed observations for the thirty General scenarios remain required for Ticket 4 completion. Ticket 3 owns authenticated exact-host behavior; Ticket 6 owns paired fresh-session equivalence and cross-profile conformance. Context reduction, packaging, live smoke, and release completion retain their later gates. No host installation, authentication, external mutation, or full-suite rerun was performed here.

Handoff: The correction can be accepted without another code change. Preserve Ticket 4 as incomplete until its required General behavior observations exist and pass. Review any later prompt/fixture changes together before relying on this baseline; do not substitute static agreement for the outstanding behavior gate.

## Findings

No actionable finding remains in the final inspected correction. This accepts the candidate-text integrity repair and the subsequent architecture-stage dependency repair, not the complete Ticket 4 outcome.

The initial pass did not identify that direct architecture diagnosis could reach `architecture-improvement.md` without loading `review.md`, where the lens names were defined. The follow-up supersedes that earlier production-text assessment: the missing dependency was a real defect, and the final architecture module now includes all twelve exact lens names in canonical order. The direct path needs only the already loaded orchestration contract and this stage module to identify and report every lens; it no longer depends on an unloaded Review module. The existing deletion guards, diagnosis-only authority, report contract, and Specification reflow remain intact.

`assert_scenario_contracts` now passes its supplied candidate to `assert_reviewed_instructions` before the supplemental phrase checks. The latter reads a separate fixed fixture, requires the exact ten-module inventory, and compares each complete module while preserving case, indentation, ordering, and trailing text. It does not reread production as its expected value, regenerate the fixture during a test, or rely on a blacklist of contradictory phrases. A candidate that retains all earlier correct text and adds conflicting instructions is rejected.

The fixture is independent of the candidate at test execution, not an independent semantic judge. An in-memory countercheck changed both the candidate and fixture to append `Earlier operation bindings take priority over every new session.` The gate then passed. That is the documented co-refresh limitation, not evidence that the contradictory policy is correct. The helper's docstring, fixture README, scenario comments, renamed thirty-scenario test, and latest evidence all disclose this limitation. The fixture must therefore remain subject to complete change review; blindly refreshing it would remove the protection. No additional finding is raised for a limitation this correction expressly identifies and does not claim to solve.

## Verification and contract assessment

Independently executed on the initial candidate before the lens follow-up:

```powershell
& '.venv/Scripts/python.exe' -B -m unittest tests.claude.test_general_profile tests.claude.test_public_plugin_contract
```

Observed exit `0`:

```text
Ran 26 tests in 14.892s
OK
```

An additional read-only Python probe imported the actual gate and used dictionaries and an in-memory fixture stand-in; it wrote no candidate, fixture, or test file. For each of the ten modules it tested appended authority, prepended authority, inserted text, deletion, case change, indentation change, and paragraph reordering. It also tested one missing and one extra module. All 72 changed candidates were rejected. The unchanged candidate and CRLF-equivalent candidate passed. The deliberately co-refreshed contradictory candidate/fixture passed, confirming the limitation described above.

The implementation record reports a pre-correction Red of two tests with 34 `AssertionError not raised` failures, followed by General Green of 13 tests. Those are supplied historical raw results; this reviewer did not recreate the earlier gate on disk. The independent 26-test run and 72-mutation probe above apply to that initial candidate.

For the final lens correction, the coordinator supplied Red of two profile tests with two failures for the unreachable list, followed by 25 combined profile tests passing. This reviewer independently inspected the final General sentence and regression, then executed:

```powershell
& '.venv/Scripts/python.exe' -B -m unittest tests.claude.test_general_profile
```

Observed exit `0`:

```text
Ran 14 tests in 0.039s
OK
```

An independent in-memory probe ran the new actual regression against four mutated stage sources: missing list, reordered names, renamed lens, and duplicate name. All four failed. The test reads the architecture module itself and compares its ordered list with the canonical twelve-name tuple; loading `review.md` is not required to pass. Inspection confirmed that tuple matches the Review skill's prescribed order.

The same probe verified all ten current module texts against the fixture. Removing only the new sentence and its following blank line reproduced the exact prior architecture raw SHA-256 `345713bc0522a099bfd248bb2b371e02bbdcb48ed7ffa2d887f38ec182e8d5fb`. Removing that same encoded sentence from the fixture reproduced its exact prior raw SHA-256 `8d45fd094f2ae0fcb52fb9fd7b7db2e1d4844197da2f58eb36f63a99c5a0334f`. The other nine module hashes were unchanged. This independently establishes that the fixture refresh contains only the reviewed production addition. The final README opening was also checked: it distinguishes the initial baseline from this reviewed follow-up and retains the fixture's non-runtime role.

The current complete texts and relevant surrounding boundaries were inspected for the following contracts:

- The ten modules map all thirty mandatory Core rules. The portable artifact envelope contains all nine shared fields and conditional approval evidence; artifact-producing stages depend on that common contract.
- Full/Lite resolution is operation-specific, keeps explicit/project/user/fallback precedence, treats present invalid Config as fail-closed Full, and forbids persistence and settings/Codex Config access. Conversation-only host-unavailable transitions disclose unavailable evidence without pretending to read a file.
- Requirement, knowledge, Specification, Plan, TDD/direct, and Review instructions retain their gates. `Add tests` maps to `tdd`, `Do not add tests` to `direct`; direct mode preserves skipped-test disclosure. Lite retains its single Change Brief approval, test limits, same-context review, correction approval, and session limitations.
- Direct architecture diagnosis precedes unrelated delivery gates while retaining its own mode/capability/safety prerequisites. Its architecture module now directly supplies the canonical twelve-lens list. Actual deletion requires all three guards. Acceptance returns to Specification. Automatic architecture routes and durable-knowledge synchronization are explicit.
- General enters only through a validated same-invocation General ready binding. It does not classify, reroute, override the model, or follow another profile. Public bootstraps provide exact contained resource mappings, version proof, and failure handling; the shared validator constrains the two profiles, ten modules per profile, and component containment.
- Session authority does not transfer across sessions. Model-switch notices retain the current operation profile and disclose support/race limits. Status is read-only; every install/update/normal-remove write requires a fresh ownership/source/scope/state check. Removal defaults and explicit `--keep-data`, reload/new-session guidance, partial failure, and session-only ZIP boundaries are present.
- Runtime Full Review requires the read-only Plugin reviewer when available and honest downgrade otherwise. The validator requires exactly `Read`, `Grep`, and `Glob` for that component. This repository review's separate context is not a live Claude reviewer-capability observation.

These are source and static-test assessments. Neither the thirty named coverage records nor the constructed module-load lists execute model requests or record model decisions. No authenticated thirty-case run, paired fresh transcript, exact-host expansion outcome, or real lifecycle result is established by them.

## Twelve Architecture and Refactoring Lenses

The outcomes below cover this correction and its relevant source boundaries, not a system-wide diagnosis or unobserved model behavior.

| Lens | Outcome | Evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `no-finding` | The complete fixture intentionally duplicates reviewed text as fixed test data. The README requires prompt/fixture review together. Repeating the canonical lens names in architecture and Review makes each separately loaded stage complete; the focused regression compares the architecture list to the shared test constant. The portable artifact envelope remains centralized in orchestration. |
| 2. Long Function | `no-finding` | `assert_reviewed_instructions` has one bounded responsibility: schema/identity, exact inventory, and full-text comparison. Coverage and transition checks remain separate helpers. |
| 3. Large Module or Class | `no-finding` | The lengthy test module groups a fixed scenario inventory, narrow parsers/assertions, and focused regressions. The final correction adds one integrity helper and three relevant tests without adding runtime or lifecycle ownership. The production addition is one ordered sentence. |
| 4. Long Parameter List | `no-finding` | The new helper accepts one candidate-source mapping. It does not require callers to coordinate candidate paths, expected values, and multiple flags. |
| 5. Data Clumps | `no-finding` | `ScenarioContract` groups module, input description, expected phrases, and prohibited phrases. The snapshot groups profile identity, schema version, and module texts in one fixture. |
| 6. Primitive Obsession | `no-finding` | Module/scenario identifiers have closed inventories; fixture identity/version and exact keys are checked. Source strings are the intended comparison domain, not purported parsed behavioral outcomes. |
| 7. Feature Envy | `no-finding` | Integrity validation lives beside its scenario gate. The repaired architecture stage directly owns the lens list it needs instead of depending on an unloaded Review stage. It has no new dependency on router state, lifecycle commands, or another profile. |
| 8. Divergent Change | `no-finding` | The final changes concern prompt regression evidence and one architecture-stage completeness requirement. Shared runtime validation retains public component and path ownership. |
| 9. Shotgun Surgery | `no-finding` | The architecture addition required its module, fixed baseline, and focused coverage to change together. This is a bounded reviewed update; the same canonical list is necessarily reachable from the independently loaded architecture and Review stages. |
| 10. Message Chains | `no-finding` | Candidate validation is a direct helper call followed by coverage checks. No new internal traversal or chained host access is introduced. |
| 11. Leaky Abstraction | `no-finding` | The helper and evidence expressly expose the integrity-only guarantee. The co-refresh probe confirms that documented limit. The final direct architecture path now supplies its required lens definitions without an implicit Review-module dependency. |
| 12. Shallow Module | `no-finding` | The single helper consolidates schema, inventory, and complete-text integrity behind the scenario gate. Callers do not reproduce those checks, and the fixture is data rather than an added runtime module. |

## Reviewed candidate identity

Raw SHA-256 values observed during this review:

| File | SHA-256 |
| --- | --- |
| `adapters/claude-code/plugin/ask-then-do-it/profiles/general/architecture-improvement.md` | `3606872a6c24a2b1325627e543c37971ad651f64b886a7a08fa2ce60f6f568eb` |
| `tests/claude/test_general_profile.py` | `95ded604f69bbda564432f31cfaf4d664719fec5a91334009b60b9effe7dadfb` |
| `tests/claude/fixtures/general-profile/reviewed-instructions.json` | `e6b319238475832f87be29fa6844fc3e399e808fa010a127825e42b4542c90c0` |
| `tests/claude/fixtures/general-profile/scenarios.json` | `6dc7e08a6f04250ecaa56d758a7aa5a973e576ec374c93f4e112a8405e8213c2` |
| `tests/claude/fixtures/general-profile/README.md` | `672bcfcc833290d63a0a4b3719785e26570f8a93840e091896418436fce777f0` |

The ten candidate module texts matched the complete fixture during inspection and execution. The fixture hash identifies that reviewed text baseline; this is not a model-output hash or claim of an earlier commit baseline.

## Completion assessment and remaining evidence

**Correction assessment:** Acceptable. The supplied-candidate gate rejects unreviewed additions, inversions, removals, and relocation without depending on retained positive phrases. Its fixture-update limitation and static evidence scope are disclosed. The final architecture stage makes all twelve canonical lenses reachable on a direct diagnosis path, and the corresponding fixture change was independently bounded to that exact addition.

**Ticket 4 assessment:** Not complete. Approved Specification section 11 and Ticket 4's completion condition require all thirty General behavior scenarios to pass. The available artifacts establish instruction coverage, text integrity, and static boundaries, but do not establish that the model actually follows those instructions in the required scenarios. Preserve this outstanding requirement; the later paired-case owner does not erase Ticket 4's own completion criterion.

Residual risks are future prompt/fixture co-edits that escape independent review, unobserved model compliance, and provisional host assumptions until the required authenticated evidence exists. No new systemic issue was established that warrants a separate architecture diagnosis. No production, test, Specification, Plan, Knowledge Base, installed host, or external state was changed by this reviewer; only this report was written.
