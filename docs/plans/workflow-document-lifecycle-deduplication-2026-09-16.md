# Workflow Document Lifecycle Deduplication - Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `workflow-document-lifecycle-deduplication-ticket-plan`

Workflow ID: `workflow-document-lifecycle-deduplication-2026-09-16`

Core version: `1.4.1`

Status: Approved

Inputs: Approved [Workflow Document Lifecycle Specification](../specs/workflow-document-lifecycle.md); current Core artifact contracts; current Full/Lite workflow specification; existing project Knowledge Base, Status, evidence indexes, documentation tests, and the three Codex slimming drafts.

Assumptions: The approved minimum producer/template routing clarification permits only the instructions and validation needed to enforce the Decision Packet lifecycle. It does not authorize changes to Full/Lite resolution, stage gates, approval authority, evidence semantics, consumer package contents, or release behavior. Existing files remain recoverable until the migration ticket passes validation.

Deferred: Exact Decision Packet serialization beyond the selected repository format, automatic generation versus manual templates, archive retention policy, adoption by Generic or Claude after this repository-scoped rollout, and any unrelated runtime slimming.

Handoff: After all Ticket test choices and this complete plan are explicitly approved, route each eligible Ticket to its selected implementation mode. Do not migrate or delete documents while this plan is Draft.

Approval: User explicitly approved the complete Ticket Plan on 2026-09-16 with `核准tickets` and selected `加測試全部 Tickets`. T1 through T6 are mapped to `tdd`. This approval authorizes only the displayed Ticket scopes and test choices; it does not authorize unrelated cleanup, external publication, or behavior changes outside the approved Specification.

Test source budget: User approved a maintenance constraint on 2026-09-16: this rollout may add at most one lifecycle validator script and one lifecycle test module. Reusable fixtures should use Markdown or JSON rather than additional Python modules. Tickets MUST NOT create one separate `test_t*.py` file per Ticket. This constraint limits source sprawl; it does not reduce the required behavioral coverage.

## Plan summary

The plan delivers one canonical document lifecycle in six sequential vertical slices. It starts with a small contract and format foundation, integrates the producer/template behavior, adds fail-closed validation, migrates the current representative drafts transactionally, updates current indexes, and finishes with full regression and Review evidence. No Ticket is marked parallel-safe because the shared artifact format, migration paths, and validator fixtures create ordering dependencies.

## Dependency order

| Order | Ticket | Depends on | Parallel safety |
| --- | --- | --- | --- |
| 1 | T1 - Decision Packet and canonical ownership contract | None | No; establishes shared schema and IDs |
| 2 | T2 - Full producer/template integration | T1 | No; changes producer guidance and shared lifecycle references |
| 3 | T3 - Lifecycle validator and duplicate detection | T1 | No; consumes T1 schemas and fixtures |
| 4 | T4 - Transactional representative migration | T1, T3 | No; moves or supersedes overlapping draft files |
| 5 | T5 - Canonical indexes and current-state links | T4 | No; target paths depend on the migration result |
| 6 | T6 - Regression, release-safety check, and Review evidence | T2, T3, T4, T5 | No; verifies the integrated result |

## Ticket T1 - Decision Packet and canonical ownership contract

### Outcome

Define the repository-local Decision Packet, pointer, canonical-owner, and archive-index contracts. Establish stable IDs, status rules, repository-relative link rules, and the conditional Knowledge Base Change Summary rule without changing workflow semantics.

### Acceptance criteria covered

Specification AC-1, AC-2, AC-3, AC-4, AC-6, and AC-10.

### In scope

- A format-level contract for one Decision Packet containing clearly labeled Working Notes, Requirement Decision Record, and proposed Knowledge Base Change Summary sections with separate IDs and statuses.
- Canonical ownership definitions for Knowledge Base, Specification, Ticket Plan, Evidence, Status, and Decision Packet content.
- Pointer and archive-index fields: target artifact ID, canonical path, status, replacement reason, and recovery/history link.
- Rules that a Knowledge Base Change Summary exists only when durable project facts change.
- Repository-relative path and stable-ID constraints, preserving the common artifact envelope.
- Contract fixtures representing Draft, Approved, Superseded, unverified, skipped, and blocked states.

### Out of scope

- Moving, renaming, or deleting existing workflow files.
- Changing Full/Lite routing, gates, approval authority, test selection, Review, or release payloads.
- Choosing a long-term external archive or adopting the policy in other adapters.

### Dependencies and likely ownership areas

- Depends on the approved Specification and Core artifact contracts.
- Likely areas: `core/artifacts/`, `docs/specs/`, a new project document-lifecycle reference, and contract fixtures under `tests/`.

### Recommended verification

Add tests. The contract is shared by every later Ticket; malformed envelopes, duplicate IDs, invalid statuses, and missing conditional-summary decisions could cause silent document drift. Adding tests increases work time, while declining them leaves schema and state-transition behavior largely unverified.

### If tests are added

Use TDD: first add failing fixture/contract tests for separate section IDs and statuses, required envelope fields, valid pointer fields, conditional summary behavior, and forbidden out-of-repository targets; implement the smallest contract and fixture set; then run focused tests plus the existing conformance/documentation checks.

### If tests are declined

Use direct implementation with static Markdown/schema inspection and link checks only. Record `tests: skipped-by-user`; state that invalid envelope, status, pointer, and conditional-summary branches were not behaviorally verified.

### Completion criteria

The contract and fixtures are self-contained, preserve the existing Core envelope, document all unresolved format choices, and pass the selected verification approach without changing runtime behavior.

### Parallel safety

No. T1 owns the shared format and IDs consumed by every other Ticket.

## Ticket T2 - Full producer and template integration

### Outcome

Make the documented Full workflow produce and link one Decision Packet for durable requirement documentation, while keeping separate approval semantics and preserving Lite isolation.

### Acceptance criteria covered

Specification AC-1, AC-2, AC-4, AC-8, and AC-10.

### In scope

- Minimal Core/documented-requirement template language that routes Working Notes, Requirement Decision Record, and Knowledge Base Change Summary into the Decision Packet.
- Minimal in-scope adapter producer guidance needed for Codex documented requirements to use the packet and point approved outputs to canonical Specification and Knowledge Base paths.
- Explicit preservation of independent artifact IDs, status transitions, joint requirement/knowledge approval rules, and artifact envelope fields.
- Explicit Lite rule that no Decision Packet is created solely by this policy.
- Contract documentation for direct stage entry and conversation-only capability honesty.

### Out of scope

- Any change to mode precedence, stage selection, Full gates, Lite lifecycle, Ticket test-choice mapping, Review lenses, or completion claims.
- Generic or Claude adapter adoption beyond documenting it as deferred.
- Consumer plugin payload or release archive changes.

### Dependencies and likely ownership areas

- Depends on T1.
- Likely areas: `core/modules/project-knowledge.md`, `core/artifacts/`, `adapters/codex/plugin/ask-then-do-it/skills/ask-with-docs/SKILL.md`, related generic/core references if required for semantic parity, and contract tests.

### Recommended verification

Add tests. This ticket changes the producer path and could regress the existing ask-with-docs contract or create a packet in Lite. Adding tests increases work time, while declining them leaves producer routing and Lite isolation dependent on prose inspection.

### If tests are added

Use TDD: first add failing contract tests for one-packet production, separate section states, approved-output links, no empty summary, Lite no-packet behavior, and unchanged mode/gate wording; implement minimal producer/template guidance; then run Codex, Generic/Core contract tests and focused documentation checks.

### If tests are declined

Use direct implementation with source inspection, relative-link checks, and existing non-test validation where applicable. Record `tests: skipped-by-user`; disclose that Full producer routing, section-state behavior, and Lite isolation were not behaviorally tested.

### Completion criteria

New documented Full flows have one packet path and canonical downstream links; existing mode/gate semantics and Lite behavior remain unchanged; deferred adapters are explicitly identified.

### Parallel safety

No. T2 consumes T1's format and changes shared producer guidance that must be validated before migration.

## Ticket T3 - Lifecycle validator and duplicate detection

### Outcome

Provide a fail-closed validator that detects broken pointers, invalid envelopes, contradictory statuses, duplicate canonical claims, orphaned approved artifacts, unauthorized full-text duplicates, and missing conditional-summary decisions.

### Acceptance criteria covered

Specification AC-3, AC-4, AC-5, AC-8, AC-9, and AC-10.

### In scope

- A repository validator or equivalent test helper with deterministic input and output.
- Pointer resolution and repository-boundary checks.
- Canonical owner and stable-ID uniqueness checks.
- Status agreement checks between pointers, indexes, and targets.
- Preservation checks for approval evidence, unresolved decisions, unverified/skipped/blocked states, source links, and observed command results.
- Duplicate full-text detection with an explicit exemption for versioned historical archives.
- Failure fixtures for missing, unreadable, contradictory, out-of-repository, and duplicate cases.

### Out of scope

- Automatic deletion or repair of documents.
- Selecting a canonical source by filename, modification time, or content similarity.
- Replacing existing release/package validators or changing their gates.

### Dependencies and likely ownership areas

- Depends on T1.
- Likely areas: one validator under `scripts/` or an existing documentation-validation module, one consolidated lifecycle test module under `tests/release/` or `tests/document_lifecycle/`, and non-Python fixture directories.

### Recommended verification

Add tests. Fail-closed edge cases are the primary value of this ticket; declining tests would leave the validator itself untrusted. Adding tests increases work time, while declining them leaves missing-target, conflicting-status, orphan, and duplicate detection unverified.

### If tests are added

Use TDD: add failing fixtures for each failure category, implement deterministic validation and diagnostics, then run focused validator tests plus the existing documentation and release-contract suite.

### If tests are declined

Use direct implementation with representative valid-tree validation and static command checks only. Record `tests: skipped-by-user`; disclose that failure branches and duplicate detection were not behaviorally verified.

### Completion criteria

The validator fails closed on every specified invalid state, permits only explicit archive duplicates, produces actionable paths/IDs, and has no write or deletion behavior.

### Parallel safety

No. T3 consumes the T1 contract and its result gates T4 migration.

## Ticket T4 - Transactional representative migration

### Outcome

Apply the approved lifecycle to the current three Codex slimming drafts using an explicit inventory and recoverable staging, preserving original bytes, IDs, approvals, unresolved decisions, and status semantics.

### Acceptance criteria covered

Specification AC-1, AC-2, AC-5, AC-6, AC-7, and AC-9.

### In scope

- An inventory/mapping for the three current Codex slimming draft files and their canonical Decision Packet sections.
- Staged creation of one packet path and any minimal compatibility pointers.
- Superseded or archive indexing with stable history links after successful validation.
- Backup/manifest and rollback information before any move or removal.
- Preservation of `Draft`, `Pending`, `unresolved`, and deferred states; no promotion to Approved or Passed.
- Injected or simulated partial-failure verification for recovery metadata.

### Out of scope

- Migrating unrelated historical artifacts without a separate approved mapping.
- Deleting the only copy of any file.
- Changing the already approved Specification or Knowledge Base facts.

### Dependencies and likely ownership areas

- Depends on T1 and T3; T2 must be complete if producer paths are changed before migration.
- Likely areas: `docs/project/drafts/`, a repository evidence/archive index, migration manifest/tooling if needed, and the consolidated lifecycle test module; do not add a separate migration test module.

### Recommended verification

Add tests. This ticket performs file movement and must prove status/evidence preservation and recoverability. Adding tests increases work time, while declining them leaves partial-failure rollback and content-preservation paths unverified.

### If tests are added

Use TDD or a test-first exception only if the repository has no reasonable migration harness: first create a failing temporary-repository scenario, then implement staged migration, backup, validation, and rollback; verify original bytes and all stable fields after success and injected failure.

### If tests are declined

Use direct implementation with a dry-run inventory, hashes, explicit backup manifest, validator execution, and manual diff review. Record `tests: skipped-by-user`; disclose that rollback and injected partial-failure behavior were not behaviorally tested.

### Completion criteria

The representative workflow has one canonical packet, no unauthorized duplicate full-text copies, validated pointers/indexes, preserved original evidence, and a documented recovery path. No destructive deletion occurs unless separately authorized by the approved Ticket scope and a verified backup exists.

### Parallel safety

No. T4 owns the overlapping source files and migration transaction.

## Ticket T5 - Canonical indexes and current-state links

### Outcome

Update current project navigation so Knowledge Base contains durable facts, Status contains current state and links, and historical evidence indexes preserve recoverable source locations without reproducing complete artifacts.

### Acceptance criteria covered

Specification AC-2, AC-5, AC-6, AC-9, and AC-10.

### In scope

- Links from the packet to the approved Specification and Knowledge Base result.
- Concise `docs/project/status.md` and `docs/project/knowledge-base.md` entries for the lifecycle and migration state.
- Evidence/archive index entries for the packet, pointer, mapping, manifest, and recovery location.
- Removal or relocation of only duplicated navigation prose that the validator and migration mapping identify as safe.
- Relative-link, anchor, and canonical-owner updates.

### Out of scope

- Rewriting unrelated project decisions, historical evidence, or release status.
- Creating a second full copy of the Specification, Ticket Plan, or Review in Status/Knowledge Base.
- Changing user-facing workflow semantics.

### Dependencies and likely ownership areas

- Depends on T4 because final paths and statuses are migration outputs.
- Likely areas: `docs/project/knowledge-base.md`, `docs/project/status.md`, `docs/evidence/release-history.md`, packet/pointer index files, and the consolidated lifecycle test module; do not add a separate link test module.

### Recommended verification

Add tests. Link and canonical-owner regressions can strand approved artifacts or recreate duplicate navigation. Adding tests increases work time, while declining them leaves links, anchors, and no-duplicate navigation behavior dependent on manual review.

### If tests are added

Use TDD: add failing link/index tests and a representative duplicate-content assertion, implement only the approved navigation changes, then run the existing documentation/link suite.

### If tests are declined

Use direct implementation with repository-wide relative-link checks, diff review, and validator execution. Record `tests: skipped-by-user`; disclose that link/index and duplicate-navigation regressions were not behaviorally tested.

### Completion criteria

Each applicable category has one current canonical path, all indexes resolve, historical source locations are recoverable, and current pages remain concise rather than copying full artifacts.

### Parallel safety

No. T5 depends on the migration's final paths and statuses.

## Ticket T6 - Regression, release-safety check, and Review evidence

### Outcome

Verify the integrated lifecycle against the approved Specification, existing Full/Lite and artifact contracts, documentation links, package boundaries, and evidence honesty; produce final Review evidence with deferred scope and environment limits.

### Acceptance criteria covered

Specification AC-8 and AC-10, plus cross-ticket verification of AC-1 through AC-7 and AC-9.

### In scope

- Existing conformance, Codex, Generic, documentation, release, and applicable package-inventory checks.
- New lifecycle validator and migration tests, if selected.
- Source/package inspection proving repository-only lifecycle files do not enter consumer payloads.
- Review against every Specification acceptance criterion and the no-semantic-change boundary.
- Evidence of commands, outputs, skipped tests, residual risks, deferred adapter adoption, archive-retention decision, and environment-limited checks.

### Out of scope

- New feature work discovered during Review.
- Live model calls, external publication, or release version changes not separately authorized.
- Reclassifying unverified or skipped evidence as passed.

### Dependencies and likely ownership areas

- Depends on T2 through T5.
- Likely areas: `tests/`, `docs/evidence/`, `docs/project/status.md`, and the existing validation commands.

### Recommended verification

Add tests/run the full applicable suite. This is the integration and evidence boundary for a cross-document change. Adding or running the checks increases work time, while declining them leaves cross-ticket regressions and package-boundary errors unverified.

### If tests are added

Use the selected focused tests followed by the applicable full suite. Record exact commands, exit codes, skipped cases, outputs, and residual risks; perform Review only from those actual results.

### If tests are declined

Use direct non-test validation only where allowed, such as static inspection, link resolution, manifest/package inventory checks, and diff review. Record `tests: skipped-by-user`; do not claim the lifecycle or existing contracts are regression-tested.

### Completion criteria

All applicable checks pass or are honestly disclosed, no blocking Review finding remains, the final state points to canonical artifacts, and deferred or unavailable evidence is visible in the final Status/Evidence handoff.

### Parallel safety

No. T6 must inspect the integrated result after all prior Tickets.

## Test choice batch

The batch choice is resolved for every Ticket:

| Ticket | Recommendation | Choice | Internal mode |
| --- | --- | --- | --- |
| T1 | Add tests - shared contract and state schema | Add tests | `tdd` |
| T2 | Add tests - producer routing and Lite isolation | Add tests | `tdd` |
| T3 | Add tests - fail-closed validator edge cases | Add tests | `tdd` |
| T4 | Add tests - migration preservation and rollback | Add tests | `tdd` |
| T5 | Add tests - canonical links and duplicate navigation | Add tests | `tdd` |
| T6 | Add tests - integrated regression and Review evidence | Add tests | `tdd` |

Tests may increase work time; the approved `加測試全部 Tickets` choice selects behavioral verification for every Ticket. All selected coverage MUST fit within the approved one-module source budget, with at most one lifecycle validator script and one lifecycle test module. The complete plan is now Approved and hands T1 to the TDD implementation path.
