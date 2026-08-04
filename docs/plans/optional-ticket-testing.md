# Optional Ticket Testing 1.1.0 Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `optional-ticket-testing-plan`

Workflow ID: `optional-ticket-testing`

Core version: `1.0.1`

Target release version: `1.1.0`

Status: Completed

Inputs: Approved [Optional Ticket Testing Specification](../specs/optional-ticket-testing.md) and Approved [Optional Ticket Testing Requirement Decision Record](../requirements/optional-ticket-testing.md).

Assumptions: The project continues its current lockstep release convention, so active Core, adapter, prompt, Plugin, and package version declarations move together to `1.1.0`. The user owns every test choice and there is no default. Internally, adding tests maps to `tdd` and declining tests maps to `direct`.

Deferred: Exact surrounding prompt prose and optional duration estimates. Publication, installation, marketplace mutation, and external messaging are outside this plan.

Handoff: All six approved Tickets completed through their selected implementation and Review paths. The local release handoff is complete; installation, marketplace mutation, publication, upload, and external messaging remain separate maintainer decisions.

Approval: The user previously chose to add tests for Tickets 1-4, mapping them to `tdd`, and explicitly approved that plan on 2026-08-04. Tickets 1-4 are complete. For this revision, the user chose to add tests for Tickets 5 and 6 and explicitly approved the complete revised Ticket Plan on 2026-08-04 with the response `核准`.

## Planned outcome

Deliver Ask Then Do It `1.1.0` with an explicit, risk-informed test choice for every Ticket. Codex and Generic users are asked whether tests should be added, while planning maps the answer to the internal implementation path and preserves it honestly through evidence, Review, documentation, conformance, and release packages.

## Test-time warning and recommendations

Running tests adds work because the implementer must establish Red, reach Green, rerun focused checks after refactoring, and perform broader verification. Estimates are qualitative because duration depends on host speed and failures encountered.

| Ticket | Outcome | Test recommendation | Added work | User test choice |
| --- | --- | --- | --- | --- |
| 1 | Core selection, routing, and evidence contract | Add tests | Medium | Add tests (Approved; internal `tdd`) |
| 2 | Complete Codex `$implement-direct` path | Add tests | Medium | Add tests (Approved; internal `tdd`) |
| 3 | Complete Generic direct-guidance path | Add tests | Medium | Add tests (Approved; internal `tdd`) |
| 4 | Integrated `1.1.0` packages and release evidence | Add tests | High | Add tests (Approved; internal `tdd`) |
| 5 | Batch plain-language test-choice contract across Core, Codex, and Generic | Add tests | Medium | Add tests (internal `tdd`) |
| 6 | Consistent three-language onboarding, documentation, packages, and evidence | Add tests | High | Add tests (internal `tdd`) |

All recommendations are advisory. The user may decline tests for any or every Ticket. The plan cannot be Approved while any Ticket's test choice remains `Pending`.

## Conditional execution policy

- A Ticket selected as `tdd` follows its TDD approach, observes Red before production changes, reaches focused Green, refactors safely, and runs broader risk-proportional tests.
- A Ticket selected as `direct` must not create, modify, or execute behavioral tests. Its listed test commands become unavailable evidence; permitted non-test validation and final-diff inspection remain applicable.
- Both modes preserve scope, dependencies, unrelated user changes, raw evidence, and Review.
- Changing a mode after approval returns this plan to Draft and requires explicit reapproval.

## Delivery strategy

Ticket 1 is the minimal shared provider-neutral contract and is first consumed by Ticket 2. Tickets 2 and 3 then deliver independently observable Codex and Generic paths in separate ownership areas. They are parallel-safe only after Ticket 1 and only under explicit delegation with non-overlapping files. Ticket 4 integrates both paths into versioned documentation, deterministic packages, checksums, and release evidence.

## Ticket 1 - Let a planner record and route the user's execution choice

Status: Completed — evidence: [Ticket 1 Implementation Evidence](../evidence/optional-ticket-testing-ticket-1.md).

Execution mode: `tdd`

System recommendation: `tdd` because this Ticket changes mandatory rules, approval gates, artifact contracts, and release-evidence semantics used by both adapters. A regression could silently run declined tests or bypass the user's decision.

### Outcome and acceptance coverage

A planner presents risk recommendations and a time warning, records one explicit `tdd` or `direct` mode for every Ticket, blocks approval when any mode is missing, and hands an Approved Ticket to the matching provider-neutral implementation contract.

This Ticket covers Specification acceptance criteria 1-6 and 11, the provider-neutral portions of criteria 8-10 and 12, and the rule that no risk or repository category creates a mandatory workflow test.

### Scope

In scope:

- Core orchestration, Ticket Planning, TDD, direct implementation, Review, architecture reflow, and capability contracts.
- Core rules plus Ticket Plan, direct evidence, Review Report, and common artifact semantics.
- Release-evidence semantics that distinguish passed tests from `skipped-by-user`.
- Shared conformance expectations and negative cases for missing, unknown, or conflicting modes.

Out of scope:

- Provider-specific Skill or Generic prompt wording.
- Final package inventories, versioned output, installation, publication, or external CI changes.

### Dependencies and ownership

Dependency: the Approved Specification. This is the first Ticket and the shared contract first consumed by Ticket 2.

Likely ownership: `core/CORE.md`, `core/modules/`, `core/rules/rules.yaml`, `core/artifacts/`, `core/adapters/manifest-contract.md`, `tests/conformance/`, shared release-evidence validation contracts, and Ticket evidence under `docs/evidence/`.

### TDD approach

1. Add focused contract tests or fixtures that fail because plans lack per-Ticket modes, orchestration always routes to TDD, and skipped tests cannot be represented honestly.
2. Capture expected Red before Core contract changes.
3. Add the smallest coherent selection, routing, direct implementation, evidence, and Review semantics.
4. Run focused checks to Green and refactor duplicated policy without behavior change.

### Direct approach

- Update the Approved Core contract without adding or running behavioral tests.
- Run only permitted static or schema checks that are not behavioral tests.
- Inspect the complete Core and artifact diff for conflicting mandatory rules and record unavailable behavioral evidence.

### Verification and completion

Focused TDD verification: Core rule, artifact, conformance-fixture, and release-evidence tests. Broader TDD verification: both adapter conformance checks and relevant release-evidence regressions.

Direct verification: YAML/Markdown parsing or other static validation, plus a manual trace from each mode to its route and evidence; no behavioral suite.

Complete when Core defines both paths without a default or mandatory-test escape hatch, all invalid-mode states stop safely, and raw evidence never treats skipped tests as passed.

Parallel safety: `No`; every later Ticket consumes this contract.

## Ticket 2 - Let a Codex user directly implement a selected Ticket

Status: Completed — evidence: [Ticket 2 Implementation Evidence](../evidence/optional-ticket-testing-ticket-2.md).

Execution mode: `tdd`

System recommendation: `tdd` because this Ticket adds a public Skill and changes orchestration, planning, Review handoff, conformance mapping, and exact Skill inventory. Tests protect against routing a `direct` Ticket to `$implement-tdd`.

### Outcome and acceptance coverage

A Codex user sees recommendations and the time-risk warning, approves per-Ticket modes, and can invoke or be routed to a valid `$implement-direct` Skill that performs bounded implementation without behavioral tests and hands honest evidence to `$review-code`.

This Ticket covers Specification acceptance criteria 1-9 and 11 for the Codex capability profile, plus the Codex portion of criterion 12.

### Scope

In scope:

- Update `$ask-then-do-it` and `$plan-tickets` for selection, approval, and routing.
- Add `$implement-direct` with valid frontmatter and UI metadata.
- Keep `$implement-tdd` intact for `tdd` Tickets.
- Update `$review-code`, architecture reflow, rule mapping, and Codex conformance evidence.
- Update Codex source onboarding needed to discover the ninth Skill.
- Codex adapter, Skill, routing, artifact, conformance, and source-inventory checks when mode is TDD.

Out of scope:

- Generic prompts, final release ZIPs and checksums, Plugin installation, or marketplace changes.

### Dependencies and ownership

Dependency: Ticket 1.

Likely ownership: `adapters/codex/plugin/ask-then-do-it/skills/`, Plugin metadata, `adapters/codex/rule-mapping.yaml`, `adapters/codex/conformance.yaml`, Codex onboarding sources, `tests/codex/`, focused Codex release-source checks, and Ticket evidence.

### TDD approach

1. Add failing assertions for the ninth Skill, mode-complete plan gate, exact routes, direct no-test contract, skipped evidence, and unchanged TDD semantics.
2. Capture Red caused by the missing Skill and TDD-only routing.
3. Add the minimum coherent Codex Skill and route changes.
4. Validate the canonical Plugin and all Skills, reach focused Green, and refactor only while covered.

### Direct approach

- Add and connect `$implement-direct` without creating or running behavioral tests.
- Run official Skill and Plugin validators only as permitted non-test validation.
- Inspect all nine Skill identities, routes, mappings, and handoffs manually.

### Verification and completion

Focused TDD verification: Codex adapter tests, native validation for all nine Skills and the Plugin, exact routing, and Codex conformance. Broader TDD verification: relevant Core, Codex source-inventory, and documentation regressions.

Direct verification: native schema, Skill, and Plugin validation plus route-diff inspection; no behavioral commands.

Complete when `$implement-direct` is a valid ninth Skill reachable only for Approved `direct` Tickets, `$implement-tdd` remains TDD-only, and direct evidence reaches Review without test-success claims.

Parallel safety: `Yes after Ticket 1`; it can run beside Ticket 3 under explicit delegation and non-overlapping ownership.

## Ticket 3 - Let a Generic user receive matching direct guidance

Status: Completed — evidence: [Ticket 3 Implementation Evidence](../evidence/optional-ticket-testing-ticket-3.md).

Execution mode: `tdd`

System recommendation: `tdd` because conversation-only prompts cannot execute the workflow, so composition and scenario tests are the primary protection against capability overclaims, missing gates, and inconsistent routing.

### Outcome and acceptance coverage

A Generic user receives provider-neutral planning that records the selected mode and routes `direct` Tickets to unexecuted direct implementation guidance without claiming edits, tests, persistence, or completion.

This Ticket covers Specification acceptance criteria 1-9 and 11 for the conversation capability profile, plus the Generic portion of criterion 12.

### Scope

In scope:

- Add a provider-neutral direct implementation prompt with matching selection, scope, no-test, evidence, and stop contracts.
- Update Generic orchestration, Ticket Planning, TDD, Review, architecture reflow, bootstrap composition, and manifest evidence.
- Preserve Conversation-only limits and user-owned persistence.
- Update Generic onboarding needed to discover the tenth prompt file.
- Generic inventory, composition, scenario, provider-neutrality, and conformance checks when mode is TDD.

Out of scope:

- Codex Skills, final package paths and checksums, or any claim of tool use and completed implementation.

### Dependencies and ownership

Dependency: Ticket 1.

Likely ownership: `adapters/generic-prompts/`, Generic release start-guide sources, Generic portions of `docs/guides/`, `tests/generic/`, focused Generic release-source checks, and Ticket evidence.

### TDD approach

1. Add failing assertions for the tenth prompt file, mode selection, direct routing, unexecuted guidance, Review disclosure, and Conversation-only limits.
2. Capture Red caused by the missing prompt and TDD-only orchestration.
3. Add the minimum coherent prompts and composition changes.
4. Reach Green for focused scenarios and conformance, then remove duplicated wording without weakening provider neutrality.

### Direct approach

- Add and connect direct guidance without creating or running behavioral tests.
- Run only permitted Markdown, YAML, or static composition validation.
- Inspect prompt order, capability claims, routes, and handoffs manually.

### Verification and completion

Focused TDD verification: Generic inventory, composition, scenario, provider-neutrality, and conformance tests. Broader TDD verification: relevant Core, Generic release-source, and documentation regressions.

Direct verification: static prompt and manifest validation plus source-to-combined-output inspection; no behavioral commands.

Complete when Generic planning preserves the user-selected mode, direct guidance is clearly unexecuted, and all ten prompt files remain provider-neutral and capability-honest.

Parallel safety: `Yes after Ticket 1`; it can run beside Ticket 2 under explicit delegation and non-overlapping ownership.

## Ticket 4 - Let a maintainer verify and package Ask Then Do It 1.1.0

Status: Completed — evidence: [Ticket 4 Implementation Evidence](../evidence/optional-ticket-testing-ticket-4.md) and [Final Review after fixes](../evidence/ask-then-do-it-1.1.0-final-review-after-fixes.md).

Execution mode: `tdd`

System recommendation: `tdd` because this Ticket changes lockstep versions, exact inventories, localized documentation, reproducible ZIPs, checksums, and release evidence. A missed reference can produce an inconsistent release.

### Outcome and acceptance coverage

A maintainer can build and inspect two deterministic `1.1.0` packages that expose nine Codex Skills and ten Generic prompt files, document the optional-test choice, and preserve honest passed or `skipped-by-user` evidence without publishing or installing anything.

This Ticket covers all thirteen Specification acceptance criteria across the integrated active release.

### Scope

In scope:

- Move active Core, adapter, prompt, Plugin, release configuration, archive paths, and current documentation from `1.0.1` to `1.1.0` under the lockstep convention.
- Update exact Codex and Generic inventories for the new direct stages.
- Update Traditional Chinese, English, and Japanese user documentation for selection, recommendations, time warning, and evidence meaning.
- Update release validation so passed and user-skipped tests are distinct without weakening safety, reproducibility, inventory, or checksum checks.
- Build isolated outputs, compare clean builds, verify ZIP parity, and replace only known managed outputs when authorized by the selected mode.
- Create Ticket evidence and final release ledger, Review, and architecture diagnosis matching the evidence actually available.

Out of scope:

- Installation, marketplace changes, publication, upload, external messaging, or rewriting immutable `1.0.1` evidence.

### Dependencies and ownership

Dependencies: Tickets 2 and 3 after Ticket 1.

Likely ownership: version declarations across Core and adapters, active human documentation, `release/release.json`, release builder and evidence validator, `tests/release/` when mode is TDD, `dist/`, and `docs/evidence/`.

### TDD approach

1. Add or revise failing integrated assertions for `1.1.0`, nine Skills, ten prompt files, mode-selection documentation, skipped-test evidence, deterministic packages, and absence of active stale `1.0.1` identity.
2. Capture Red before active version and output changes.
3. Complete the minimum version, documentation, inventory, builder, and evidence changes.
4. Build twice in isolated roots, reach focused and broader Green, then replace only validated managed outputs.

### Direct approach

- Update versioned source, documentation, inventories, generated packages, and evidence without adding or running behavioral tests.
- Run permitted non-test build, native validation, archive, checksum, link, and static conformance commands.
- Record every unavailable automated test and avoid claiming a fully test-verified release.

### Verification and completion

Focused TDD verification: version consistency, exact inventory, documentation, release contract, release evidence, and provider package tests. Broader TDD verification: complete automated suite, both conformance suites, native canonical and packaged Plugin and Skill validators, reproducibility, checksums, architecture diagnosis, and Review.

Direct verification: two isolated builds, byte comparison, ZIP parity, checksums, native validation, link/static scans, and manual inventory inspection where classified as non-test validation; no behavioral suite.

Complete when active source and outputs consistently identify `1.1.0`, both implementation paths are packaged, release evidence distinguishes passed from skipped checks, and `1.0.1` artifacts remain historical.

Parallel safety: `No`; this Ticket integrates shared versions, documentation, release configuration, output, checksums, and evidence.

## Ticket 5 - Collect all plain-language test choices in one batch

Status: Completed — evidence: [Ticket 5 Implementation Evidence](../evidence/optional-ticket-testing-ticket-5.md) and [Independent Ticket 5 Review](../evidence/optional-ticket-testing-ticket-5-review.md).

Test choice: Add tests.

Internal execution mode: `tdd`.

System recommendation: Add tests because this Ticket changes a cross-adapter approval gate, batch parsing behavior, and the mapping that determines whether behavioral tests run. Focused negative checks can prevent the old `tdd`/`direct` question and one-round-trip-per-Ticket behavior from reappearing, while verifying that all-add, all-decline, and mixed answers still route deterministically. Adding these tests is expected to add a medium amount of work.

### Outcome and acceptance coverage

A first-time user sees all per-Ticket recommendations and time warnings, then supplies every test choice in one plain-language batch response. The system accepts all-add, all-decline, and explicit mixed selections, stores each answer as the existing internal `tdd` or `direct` value, and asks only about unresolved Tickets when a mixed response is incomplete.

This Ticket covers revised Specification acceptance criteria 1-6 and 14-16 across provider-neutral Core, Codex, and Generic planning contracts.

### Scope

In scope:

- Provider-neutral Ticket Planning and Ticket Plan artifact wording that separates the user-facing test choice from the internal route value and collects all choices in one batch.
- Codex `$plan-tickets` and orchestration wording for all recommendations, the time warning, all-add/all-decline/mixed answers, answer mapping, unresolved-choice gate, and reapproval behavior.
- Generic Ticket Planning and orchestration wording with the same batch behavior and Conversation-only limits.
- Focused Core, Codex, and Generic contract or scenario checks when tests are added.
- Internal routing, implementation, evidence, and Review terms that legitimately retain `tdd` and `direct`.

Out of scope:

- Localized onboarding and explanatory documentation, generated release packages, publication, installation, marketplace changes, or renaming the internal modes.

### Dependencies and ownership

Dependencies: Completed Tickets 1-4 and the revised Approved Specification.

Likely ownership: `core/modules/ticket-planning.md`, `core/artifacts/ticket-plan.md`, relevant Core orchestration language, `adapters/codex/plugin/ask-then-do-it/skills/plan-tickets/SKILL.md`, Codex orchestration Skills, `adapters/generic-prompts/ticket-planning.md`, Generic orchestration prompts, and focused files under `tests/conformance/`, `tests/codex/`, and `tests/generic/`.

### TDD approach

1. Add focused assertions that fail while planning asks users to choose `tdd` or `direct`, requires one round trip per Ticket, lacks all-add/all-decline/mixed handling, or permits an unresolved test choice to pass the gate.
2. Capture Red before changing the planning contracts.
3. Make the smallest coherent Core, Codex, and Generic wording and mapping changes.
4. Reach focused Green, then run broader adapter and conformance checks to detect route or capability regressions.

### Direct approach

- Update the Approved planning contracts and mappings without creating, modifying, or running behavioral tests.
- Run only permitted Markdown, YAML, native Skill, or other static validation.
- Inspect the complete cross-adapter diff and manually trace both localized choice meanings to their internal routes, recording behavioral tests as skipped by user choice.

### Verification and completion

Focused TDD verification: Core selection-contract assertions, Codex planning scenarios, and Generic prompt scenarios that require one batch request, accept all-add/all-decline/mixed answers, retain partial choices, and reject the old initial question. Broader TDD verification: relevant conformance and adapter suites.

Direct verification: Markdown/YAML parsing, native Skill validation, targeted text scans, and a manual two-answer routing trace; no behavioral suite.

Complete when every planning surface shows all recommendations before one batch request, does not require a turn per Ticket, asks only about unresolved choices when necessary, and keeps the existing internal implementation routes deterministic and honest.

Parallel safety: `No`; Ticket 6 consumes this user-facing contract and both Tickets touch shared documentation and release assertions.

## Ticket 6 - Keep all localized onboarding and documentation consistent

Status: Completed — evidence: [Ticket 6 Implementation Evidence](../evidence/optional-ticket-testing-ticket-6.md) and [Independent Ticket 6 Review](../evidence/optional-ticket-testing-ticket-6-review.md).

Test choice: Add tests.

Internal execution mode: `tdd`.

System recommendation: Add tests because this Ticket updates nine localized `START-HERE` files plus README, guides, design documents, generated packages, checksums, and release evidence. Documentation and package checks can detect a missed locale, stale `tdd`/`direct` instruction, or mismatched generated artifact. Adding these tests is expected to add a high amount of work because the release outputs must also be rebuilt and verified.

### Outcome and acceptance coverage

Traditional Chinese, English, and Japanese users see the same beginner-friendly sequence everywhere: the AI presents all per-Ticket test recommendations, collects every test choice in one batch, and requests final plan approval only after all choices are complete. Explanatory material may describe the internal implementation paths later, but must not use `tdd` or `direct` as the initial user decision.

This Ticket covers revised Specification acceptance criteria 13-15 and the documentation and generated-output portions of criteria 1-4.

### Scope

In scope:

- All nine Traditional Chinese, English, and Japanese `START-HERE` files in the repository root, Codex Plugin source, and Generic release source, including batch-selection wording where the interaction is explained.
- All affected localized README, guides, design, release, and adapter Markdown.
- The exact requested Traditional Chinese introductory sentence and equivalent English and Japanese meaning.
- Documentation and release-source checks when tests are added.
- Rebuilt deterministic Codex and Generic packages, checksums, release ledger, Ticket evidence, and final review evidence.

Out of scope:

- Publication, upload, installation, marketplace mutation, external CI execution, or rewriting immutable `1.0.1` evidence.

### Dependencies and ownership

Dependency: Ticket 5.

Likely ownership: root `README.md` and `START-HERE.*.md`, `adapters/codex/plugin/ask-then-do-it/START-HERE.*.md`, `release/generic/START-HERE.*.md`, localized files under `docs/guides/` and `docs/design/`, affected adapter Markdown, `tests/release/`, managed release outputs, checksums, and current `1.1.0` evidence.

### TDD approach

1. Add or revise documentation assertions that fail while any user-facing locale asks users to choose `tdd` or `direct`, implies one response per Ticket, or omits the required batch add-tests meaning.
2. Capture Red before editing documentation sources.
3. Update all three languages and every managed source, then rebuild release outputs.
4. Reach focused Green, run the complete suite and validators, and verify deterministic package parity and checksums.

### Direct approach

- Update all affected Markdown and rebuild managed release artifacts without creating, modifying, or running behavioral tests.
- Run permitted link, localization, text-scan, native validation, archive, checksum, and deterministic-build checks classified as non-test validation.
- Manually compare the three language sequences and record behavioral documentation and release tests as skipped by user choice.

### Verification and completion

Focused TDD verification: documentation coverage for all nine `START-HERE` files and affected localized document groups, plus release-source/package parity. Broader TDD verification: the complete automated suite, both conformance suites, canonical and packaged Plugin/Skill validators, clean builds, ZIP parity, and checksums.

Direct verification: exhaustive localized text scans, manual semantic comparison, links/static validation, two isolated builds, byte comparison, ZIP parity, native validators, and checksums; no behavioral suite.

Complete when every affected three-language entry and document explains one batch choice about adding tests, legitimate later explanations of internal routing remain clear, generated packages match their sources, and the `1.1.0` evidence describes the revised contract truthfully.

Parallel safety: `No`; it depends on Ticket 5 and integrates shared documentation, release outputs, checksums, and evidence.

## Dependency order and parallel groups

1. Ticket 1 establishes the shared Core contract.
2. Tickets 2 and 3 may proceed in parallel after Ticket 1 only under explicit delegation; otherwise they run sequentially.
3. Ticket 4 begins after Tickets 2 and 3 complete.
4. Ticket 5 revises the shared user-facing planning contract after Tickets 1-4.
5. Ticket 6 begins after Ticket 5 and synchronizes all localized documentation and release outputs.

## Plan-wide completion criteria

- Every Specification acceptance criterion maps to at least one Ticket.
- Every Ticket retains its Approved plain-language test choice and mapped internal `tdd` or `direct` mode through Review.
- No direct Ticket creates or executes behavioral tests, and no evidence labels skipped tests as passed.
- TDD Tickets retain genuine Red, Green, refactor, and broader-verification evidence.
- Core, nine Codex Skills, ten Generic prompt files, both adapters, all nine localized `START-HERE` files, affected three-language documentation, release packages, and conformance artifacts agree.
- Active release output and evidence identify `1.1.0`; existing `1.0.1` evidence remains historical.
- No personal installation, marketplace mutation, publication, upload, or external communication occurs.

## Test-selection and approval gate

Tickets 1-4 were previously approved with tests added and are complete. Tickets 5-6 both have the user choice `Add tests`, and the complete revised plan is Approved for test-driven implementation in dependency order.
