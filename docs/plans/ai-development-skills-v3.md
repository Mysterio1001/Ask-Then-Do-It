# Portable AI Development Workflow - v3 Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `portable-ai-development-workflow-v3-plan`

Workflow ID: `grill-me-core-v3`

Core version: `3.0.0`

Status: Completed

Completion evidence: [Grill Me Release 3.0.0 Evidence](../evidence/grill-me-release-3.0.0.md)

Approval: Explicitly approved by the user in the project conversation on 2026-07-29 with the instruction `開始執行`.

## Inputs

- Approved [Portable AI Development Workflow - v3 Specification](../specs/ai-development-skills-v3.md).
- Specification approval recorded on 2026-07-29.
- Existing validated Core `2.0.0` and release `2.1.0` source and evidence.

## Planned outcome

Deliver Core, Codex, and Generic release `3.0.0` with evidence-backed project knowledge, documented requirement interrogation, twelve consistent Architecture and Refactoring Lenses, safe architecture diagnosis, explainable routing, non-destructive v2 migration, and reproducible packages.

Implementation remains unauthorized while this plan is Draft. Personal installation, marketplace mutation, publication, and external upload remain outside this plan.

## Delivery strategy

Tickets are vertical user capabilities rather than separate core, adapter, test, or documentation layers. Each behavior ticket updates the model-neutral contract, Codex adapter, Generic adapter, and tests needed to demonstrate the same behavior end to end.

All tickets are sequential because they update shared rule catalogs, conformance manifests, combined routing prompts, Plugin inventory, or release metadata. Independent file ownership alone is insufficient to prove parallel safety.

## Tickets

### Ticket 1 - Preserve project knowledge during requirement interrogation

Status: Completed — evidence: [v3-ticket-1](../evidence/v3-ticket-1.md).

#### Outcome

A user can directly run documented requirement interrogation in Codex or a Generic model, answer exactly one recommended question per turn, keep provisional discoveries in Draft Working Notes, and approve an evidence-backed Project Knowledge Base update together with the Requirement Decision Record.

#### Acceptance criteria covered

- Core `3.0.0` defines Project Knowledge Base, Draft Working Notes, and documented requirement interrogation without provider-specific dependencies.
- The canonical Knowledge Base uses `docs/project/knowledge-base.md` and all six required sections.
- Formal knowledge is derived only from approved evidence.
- Every proposed synchronization separates additions, modifications, and removals.
- Approval authorizes only the Knowledge Base changes displayed with the upstream artifact.
- Documented interrogation asks one question per turn and blocks implementation before consensus.
- Codex and Generic provide directly usable documented-interrogation entry points.
- Conversation-only output provides complete Markdown and honest persistence limits.

#### In scope

- Upgrade the core version identity and compatible rule catalog to `3.0.0`.
- Add model-neutral knowledge-management and documented-interrogation contracts.
- Add Project Knowledge Base and Draft Working Notes artifact contracts.
- Add `KB-EVIDENCE-001`, `KB-DRAFT-001`, and `KB-SYNC-001`.
- Add the Codex `grill-with-docs` Skill and its UI metadata.
- Add the Generic documented-requirements modular prompt.
- Add adapter rule mappings and capability declarations for this behavior.
- Add repository-backed and Conversation-profile scenario fixtures.
- Preserve the normal `grill-requirements` entry point.

#### Out of scope

- Automatic documented-mode routing.
- Architecture lenses or architecture diagnosis.
- v2 first-use migration.
- Release packaging.
- Personal installation.

#### Dependencies

The approved v3 Specification. This is the first implementation ticket.

#### Likely ownership areas

- `core/CORE.md`
- `core/modules/`
- `core/artifacts/`
- `core/rules/rules.yaml`
- `adapters/codex/`
- `adapters/generic-prompts/`
- `tests/conformance/`, `tests/codex/`, and `tests/generic/`

#### Test-first approach

1. Add failing contract tests for the three new rule IDs, two new artifact contracts, canonical Knowledge Base path, and six required sections.
2. Add a failing Codex inventory and official-validation expectation for `grill-with-docs`.
3. Add a failing Generic scenario that supplies a confirmed answer but verifies that it remains in Draft Working Notes before approval.
4. Add failing scenarios for invented knowledge, undisclosed synchronization, more than one question in a turn, and pre-consensus implementation.
5. Observe each expected failure against v2 behavior.
6. Implement the smallest coherent Core and adapter changes that satisfy the tests.
7. Refactor shared wording or schemas without weakening evidence and approval rules.

#### Focused verification

- Run knowledge-artifact and rule-catalog tests.
- Validate `grill-with-docs` with the official Codex validator.
- Run Generic documented-interrogation scenarios.
- Verify that a displayed approval covers only the exact Knowledge Base change summary.

#### Broader verification

- Run all conformance, Codex, and Generic tests.
- Confirm existing requirement interrogation still asks exactly one question and remains directly callable.
- Scan model-neutral Core files for provider invocation syntax or metadata.

#### Completion criteria

- Both adapters can complete the documented-requirements flow from fresh start to approved Requirement Decision Record and Knowledge Base synchronization.
- Unapproved notes never appear as formal Knowledge Base facts.
- Conversation-only output states user-owned persistence.
- All tests and validators required by this ticket pass with raw results recorded.

#### Parallel safety

`No`. This ticket establishes Core `3.0.0`, shared artifact contracts, mandatory rules, and adapter manifests used by all later tickets.

### Ticket 2 - Apply one evidence-based twelve-lens review vocabulary

Status: Completed — evidence: [v3-ticket-2](../evidence/v3-ticket-2.md).

#### Outcome

A user receives a code review that checks every core Architecture and Refactoring Lens over the change scope, supplies evidence for each result, and distinguishes findings, no findings, non-applicable cases, and unavailable verification consistently across Codex and Generic models.

#### Acceptance criteria covered

- Core defines the exact twelve mandatory lenses in the approved order.
- Projects may add lenses but cannot remove or silently skip a core lens.
- Code review evaluates all twelve lenses with evidence or a justified status.
- `not-applicable` and `unverified` cannot be used without reasons.
- Conversation-only review never converts missing evidence into `no-finding`.
- Existing v2 review responsibilities, severity ordering, and independence labels remain compatible.

#### In scope

- Add the model-neutral twelve-lens contract.
- Add `REVIEW-LENSES-001` to the rule catalog and adapter mappings.
- Extend the Review Report contract with per-lens outcomes and evidence.
- Update the Codex `review-code` Skill and directly referenced resources when progressive disclosure is useful.
- Update the Generic review prompt and combined-source inputs.
- Add fixtures for each permitted lens result and invalid omission cases.
- Preserve project-specific lens extensibility.

#### Out of scope

- System-wide architecture diagnosis.
- Simulated deletion analysis.
- Automatic review-to-architecture routing.
- Refactoring implementation.

#### Dependencies

Ticket 1.

#### Likely ownership areas

- `core/modules/review.md`
- `core/artifacts/review-report.md`
- A model-neutral lens reference under `core/`
- `core/rules/rules.yaml`
- Codex `review-code` Skill files
- Generic review prompt
- Review and conformance tests

#### Test-first approach

1. Add a failing test that requires the exact twelve core lens identities and order.
2. Add failing Review Report fixtures with a missing lens, unsupported result, evidence-free finding, unjustified `not-applicable`, and unjustified `unverified`.
3. Add failing Codex and Generic scenarios that attempt to skip apparently irrelevant lenses.
4. Add a regression scenario for existing correctness, security, test-quality, severity, and independence behavior.
5. Observe the expected failures.
6. Implement the smallest review-contract and adapter changes that satisfy all cases.
7. Refactor detailed lens explanations into one-level references where this keeps Skill context concise.

#### Focused verification

- Validate exact lens inventory and status values.
- Run Codex and Generic review scenarios against the same supplied change evidence.
- Confirm each finding includes trigger, impact, evidence, and location when available.

#### Broader verification

- Run full conformance and adapter suites.
- Run existing limited-evidence and independent-review regression scenarios.
- Verify project-specific additions do not replace core lenses.

#### Completion criteria

- Both adapters emit a complete twelve-lens assessment for the same review scope.
- Missing evidence is labeled honestly.
- Existing review gates and evidence labels remain intact.
- All ticket tests and validators pass with raw results recorded.

#### Parallel safety

`No`. It modifies shared review contracts, adapter manifests, and prompts consumed by Ticket 3.

### Ticket 3 - Diagnose architecture safely without authorizing refactoring

Status: Completed — evidence: [v3-ticket-3](../evidence/v3-ticket-3.md).

#### Outcome

A user can directly request architecture diagnosis in Codex or Generic mode and receive a complete Architecture Improvement Report using all twelve lenses, dependency and impact tracing, and non-mutating simulated deletion analysis. Accepting the report routes the work to Specification rather than changing code.

#### Acceptance criteria covered

- Architecture diagnosis is independently addressable and diagnostic-only by default.
- It applies all twelve lenses to the declared architecture scope.
- Default deletion analysis performs no repository mutation.
- Actual deletion is refused unless authorization, Tools capability, and disposable isolation are all proven.
- Reports contain all ten required sections and one valid state.
- Accepting a report does not authorize refactoring and routes to Specification.
- Codex and Generic provide direct architecture-improvement entry points.

#### In scope

- Add the model-neutral architecture-improvement module.
- Add the Architecture Improvement Report artifact contract.
- Add `ARCH-DIAG-001`, `ARCH-DELETE-001`, `ARCH-REPORT-001`, and `ARCH-REFLOW-001`.
- Implement read-only dependency and impact tracing instructions.
- Define simulated and explicitly authorized actual deletion evidence requirements.
- Add the Codex `improve-architecture` Skill and UI metadata.
- Add the Generic architecture-improvement modular prompt.
- Add refusal, downgrade, report-state, and handoff scenario tests.

#### Out of scope

- Automatic architecture triggers.
- Production refactoring.
- Executing an actual deletion experiment in this project workspace.
- Approving a future refactoring Specification or Ticket Plan.
- Release packaging.

#### Dependencies

Ticket 2 supplies the canonical lens contract.

#### Likely ownership areas

- `core/modules/`
- `core/artifacts/`
- `core/rules/rules.yaml`
- Codex `improve-architecture` Skill files
- Generic architecture-improvement prompt
- Architecture, safety, adapter, and conformance tests

#### Test-first approach

1. Add failing artifact tests for all ten report sections and four valid states.
2. Add a failing scenario proving that default simulated deletion attempts no write, move, rename, or delete operation.
3. Add one failing refusal scenario for each absent actual-deletion gate and one fixture in which all three gates are represented without touching the live workspace.
4. Add failing acceptance-handoff tests that reject direct routing from an accepted report to Ticket Plan or implementation.
5. Add Conversation-profile scenarios for `unverified` and `unavailable` evidence.
6. Observe the expected failures.
7. Implement the minimal Core, Codex, and Generic behavior.
8. Refactor report and lens references while preserving mandatory checks.

#### Focused verification

- Validate both new modular entry points.
- Exercise diagnostic-only and report-state scenarios.
- Prove through instrumented fixtures that default deletion analysis performs zero mutation.
- Prove refusal when any actual-deletion gate is missing.

#### Broader verification

- Run conformance, Codex, Generic, and safety suites.
- Confirm accepted reports route to Draft Specification authoring.
- Confirm review remains a separate focused stage.

#### Completion criteria

- A complete report can be produced in Tools and Conversation profiles with honest evidence labels.
- No direct architecture-diagnosis path can authorize production edits.
- Default deletion analysis is demonstrably read-only.
- All ticket tests and validators pass with raw results recorded.

#### Parallel safety

`No`. It consumes the shared lens contract and adds rules and modules required by orchestration.

### Ticket 4 - Route users automatically while preserving direct control

Status: Completed — evidence: [v3-ticket-4](../evidence/v3-ticket-4.md).

#### Outcome

A user can describe work naturally and have the orchestrator select documented interrogation or architecture diagnosis at the approved times, with a brief explanation, while any explicit module choice remains authoritative and every existing approval gate remains enforced.

#### Acceptance criteria covered

- Natural-language intent does not require users to know Skill or prompt names.
- Explicit user module selection overrides automatic routing.
- Automatic documented-mode selection uses only the three approved conditions and announces its reason.
- Architecture diagnosis triggers on direct request, systemic review evidence, or approved milestone conditions.
- Architecture diagnosis does not run after every Ticket by default.
- Systemic code-review findings route to architecture diagnosis without duplicate reports.
- Generic combined and modular prompts preserve equivalent routing behavior.

#### In scope

- Add `ROUTE-USER-001` and `ROUTE-DOCS-001`.
- Update model-neutral orchestration and stage-selection rules.
- Update Codex `ai-dev-workflow` routing across all eight Skills.
- Update Generic bootstrap, orchestration prompt, and generated combined workflow source order.
- Connect systemic review outcomes to architecture diagnosis.
- Add milestone routing after a related Ticket group or before release.
- Add knowledge synchronization proposals for approved or accepted artifacts that introduce durable facts.
- Add routing explanation, override, non-duplication, and gate-regression tests.

#### Out of scope

- Adding more trigger conditions.
- Running architecture diagnosis after every ticket.
- Provider-native adapters beyond Codex and Generic.
- Implementing findings.

#### Dependencies

Tickets 1-3.

#### Likely ownership areas

- `core/modules/orchestration.md`
- `core/rules/rules.yaml`
- Codex `ai-dev-workflow`, `review-code`, and related handoff instructions
- Generic bootstrap, orchestration, review, and combined-prompt composition
- Routing and integration tests

#### Test-first approach

1. Add table-driven failing cases for each automatic documented-mode condition and each architecture trigger.
2. Add failing precedence cases where an explicit normal or documented requirement mode conflicts with automatic selection.
3. Add a failing natural-language case with no module name.
4. Add a failing case that prevents architecture diagnosis after an ordinary single Ticket.
5. Add failing review-to-architecture and accepted-report-to-Specification handoff cases.
6. Add approval-gate regression cases that prevent route shortcuts.
7. Observe the expected failures.
8. Implement the smallest routing changes and refactor duplicated routing policy.

#### Focused verification

- Run routing tables for Core, Codex, and Generic behavior.
- Verify every automatic route includes a reason.
- Verify explicit user selection wins unless it violates a safety or approval gate.

#### Broader verification

- Run complete adapter and conformance suites.
- Generate the Generic combined workflow and verify all modular stages remain independently usable.
- Run an end-to-end fresh workflow and a resumed workflow from supplied artifacts.

#### Completion criteria

- Users can enter every v3 stage by natural language or direct invocation.
- Automatic routing is explainable, bounded, and gate-preserving.
- Both adapters make the same stage decision for the shared scenario fixtures.
- All ticket tests and validators pass with raw results recorded.

#### Parallel safety

`No`. This is the integration ticket over shared orchestrators and all preceding behavior contracts.

### Ticket 5 - Upgrade existing projects without destroying v2 evidence

Status: Completed — evidence: [v3-ticket-5](../evidence/v3-ticket-5.md).

#### Outcome

An existing v2 user can begin using v3, review a proposed initial Knowledge Base derived from approved artifacts, reject or approve it, and continue without any approved v2 artifact being rewritten. Traditional Chinese documentation explains the updated portable workflow and both supported usage modes.

#### Acceptance criteria covered

- Migration occurs on first v3 use and remains non-destructive.
- Missing or unsupported facts are unresolved rather than invented.
- Existing v2 artifact meaning and approval evidence remain compatible.
- Existing v2 Generic prompts remain independently usable.
- Human documentation separates portable concepts from Codex-specific operation.
- Documentation describes Generic capability degradation and user-owned persistence accurately.

#### In scope

- Add `MIGRATE-V2-001` and migration routing.
- Add v2-to-v3 migration fixtures with complete, incomplete, conflicting, approved, and unapproved inputs.
- Update migration inventory and compatibility records.
- Update the Traditional Chinese design guide.
- Update Codex, Generic, and beginner usage guides with Knowledge Base, documented interrogation, twelve lenses, architecture diagnosis, and safety boundaries.
- Preserve English canonical machine- and model-consumed artifacts.
- Validate documentation links, terminology, provider separation, and beginner readability.

#### Out of scope

- Rewriting approved v2 artifacts.
- Translating canonical Specifications, plans, rule catalogs, prompts, manifests, or Skill instructions.
- Adding another provider adapter.
- Personal installation or migration of a personal Skill directory.

#### Dependencies

Ticket 4 establishes final v3 routing and behavior.

#### Likely ownership areas

- Core compatibility and adapter migration instructions
- `adapters/codex/migration-inventory.yaml`
- Migration scenario tests
- `docs/design/`
- `docs/guides/`
- Documentation tests

#### Test-first approach

1. Add failing migration fixtures that snapshot every existing approved v2 artifact before and after migration.
2. Add failing scenarios for incomplete and conflicting evidence that require unresolved output.
3. Add a failing case that rejects Knowledge Base creation without explicit approval.
4. Add failing documentation checks for required v3 topics, relative links, provider separation, and canonical-English references.
5. Observe expected behavioral and documentation failures.
6. Implement migration behavior and update the guides.
7. Refactor duplicated explanations while keeping the beginner guide intentionally simple.

#### Focused verification

- Compare byte-level or semantic snapshots of approved v2 inputs before and after migration.
- Verify first-use proposals contain only evidence-backed knowledge.
- Run documentation link and required-section checks.

#### Broader verification

- Run full conformance, adapter, migration, and documentation suites.
- Exercise Codex and Generic upgrade walkthroughs.
- Confirm no translated canonical contract or prompt set was introduced.

#### Completion criteria

- Users can accept or reject migration without risking v2 evidence.
- All v3 concepts and safety limits are documented for Traditional Chinese readers.
- Portable documentation does not present Codex as the only execution model.
- All ticket tests and documentation checks pass with raw results recorded.

#### Parallel safety

`No`. Migration and documentation must describe the final integrated behavior and paths from Tickets 1-4.

### Ticket 6 - Produce and prove the reproducible 3.0.0 release

Status: Completed - evidence: [v3-ticket-6](../evidence/v3-ticket-6.md).

#### Outcome

A maintainer can run the documented build and validation workflow to produce separate reproducible Codex and Generic `3.0.0` packages, verify their SHA-256 checksums, and inspect release evidence proving all required checks passed without installing or publishing anything.

#### Acceptance criteria covered

- Core, Codex adapter, Generic adapter, and release identity are `3.0.0`.
- Existing `2.1.0` artifacts remain preserved.
- The Codex Plugin contains exactly the six compatible Skills plus `grill-with-docs` and `improve-architecture`.
- The Generic package includes both new modular prompts and combined routing.
- Every mandatory rule is mapped by each conforming adapter.
- Existing v2 regressions remain green.
- Two unchanged builds produce byte-identical archives and matching SHA-256 content.
- No successful release evidence exists when a required check fails or is blocked.
- No installation, marketplace mutation, publication, external upload, or unsupported-provider claim occurs.

#### In scope

- Update release identity and managed-output configuration to `3.0.0`.
- Update Codex Plugin and Generic package inventories.
- Update deterministic build composition for the new prompts and Skills.
- Preserve existing versioned `2.1.0` archives and evidence.
- Run shared conformance and all adapter, migration, documentation, and release suites.
- Run official validation for all eight Codex Skills.
- Build twice from unchanged source and compare archives and checksums.
- Produce a `3.0.0` release evidence document with raw commands and outcomes.
- Update root entry documentation only after the packages validate.

#### Out of scope

- Personal installation.
- Marketplace metadata or publication.
- External upload or remote release.
- Release signing beyond SHA-256.
- Dedicated provider packages beyond Codex and Generic.

#### Dependencies

Tickets 1-5.

#### Likely ownership areas

- `release/release.json`
- `scripts/build_release.py`
- Adapter manifests and package inventories
- `tests/release/`
- `dist/` managed v3 outputs
- `docs/evidence/`
- Root `README.md`

#### Test-first approach

1. Add failing release-contract expectations for version `3.0.0`, eight Codex Skills, the new Generic modules, and protected `2.1.0` artifacts.
2. Add failing package-inventory cases for missing, duplicate, stale, and extra runtime files.
3. Add a failing release-evidence gate that rejects any failed or blocked required validation.
4. Add or retain reproducibility, ZIP equivalence, collision safety, and checksum cases.
5. Observe expected failures against the `2.1.0` release configuration.
6. Implement the minimum release configuration and build changes.
7. Refactor build inventory data without expanding managed filesystem boundaries.

#### Focused verification

- Run release contract, inventory, checksum, and safety tests.
- Run official validation for all eight packaged Skills.
- Validate Generic combined-prompt composition and Conversation-profile limits.

#### Broader verification

- Run the complete automated suite.
- Run shared conformance for both adapters.
- Build twice from unchanged canonical source and compare bytes and checksums.
- Inspect ZIP-to-directory equivalence and absence of development-only files.
- Verify `2.1.0` outputs remain unchanged.

#### Completion criteria

- All required checks pass and raw outcomes appear in the v3 release evidence.
- Both `3.0.0` archives are reproducible and checksum-verifiable.
- Package inventories contain only approved runtime files.
- Root documentation points users to validated v3 packages without implying installation or publication.
- No unauthorized external or personal-environment mutation occurs.

#### Parallel safety

`No`. This is the final sequential integration and release-proof ticket.

## Dependency order

1. Ticket 1: Documented interrogation and project knowledge.
2. Ticket 2: Twelve-lens evidence-based review.
3. Ticket 3: Safe architecture diagnosis.
4. Ticket 4: Explainable automatic routing.
5. Ticket 5: Non-destructive migration and human documentation.
6. Ticket 6: Reproducible `3.0.0` release.

No parallel group is approved.

## Cross-ticket constraints

- Start every reasonably testable behavior with an observed failing test for the expected missing-behavior reason.
- Record any approved test-first exception before production edits and provide alternative verification.
- Preserve unrelated user files and existing `2.1.0` release artifacts.
- Keep canonical Core, prompt, manifest, Skill, Specification, and Ticket Plan content in English.
- Keep Project Knowledge Base synchronization evidence-backed and approval-bound throughout implementation.
- Treat code review, architecture diagnosis, release validation, and documentation checks as evidence-producing stages, not permission to broaden scope.
- Never perform an actual deletion experiment in the live workspace under this plan.
- Do not install, publish, upload, or modify marketplace state.

## Assumptions and deferred decisions

- Existing Python and repository validation infrastructure remains the implementation base unless a failing test proves an incompatible need.
- Detailed file placement for new Core references may be refined during a ticket when it preserves the approved contract and one-level discoverability.
- Dedicated third-party provider adapters, hosted persistence, actual deletion automation, signing, marketplace publication, and installers remain deferred as stated in the Specification.

## Handoff

After explicit plan approval, begin Ticket 1 with failing tests. Do not begin Tickets 2-6 early, and do not treat this plan as installation or publication authority.

## Plan approval gate

This Ticket Plan is explicitly Approved and authorizes implementation beginning only with Ticket 1 and its test-first step. Later Tickets remain blocked by the dependency order and completion evidence.
