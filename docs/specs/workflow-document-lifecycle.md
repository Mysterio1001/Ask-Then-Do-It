# Workflow Document Lifecycle Specification

Artifact type: Specification

Artifact ID: `workflow-document-lifecycle-spec`

Workflow ID: `workflow-document-lifecycle-deduplication-2026-09-16`

Core version: `1.4.1`

Status: Approved

Inputs: User-approved document deduplication direction in the current conversation; [Project Knowledge Base](../project/knowledge-base.md); [current workflow specification](workflow.md); Core artifact and project-knowledge contracts; existing workflow drafts and historical cleanup evidence.

Assumptions: This change affects workflow-document organization and maintenance only. Full/Lite behavior, approval authority, evidence requirements, adapter runtime semantics, and release semantics remain unchanged. The implementation may add the minimum producer/template routing needed to create and link a Decision Packet; it must not change mode resolution, stage gates, approval authority, evidence meaning, or consumer package behavior. Existing artifacts may remain in their current locations until an approved migration plan is executed.

Deferred: Exact file format for a Decision Packet, whether pointer files are generated automatically, archive retention location and duration, migration tooling, and whether the policy should later apply to adapters other than Codex.

Handoff: After explicit approval, split this Specification into an implementation Ticket Plan. Do not migrate or delete existing documents from this Draft alone.

Approval: User explicitly approved this Specification on 2026-09-16 with `核准`. The user approved the minimum producer/template routing and validator scope clarification on 2026-09-16 with `核准`. This approval covers the document-lifecycle and deduplication behavior described here only; it does not approve implementation, migration, deletion, archive placement, or release.

## Problem

The Full workflow currently produces several documents that repeat the same problem statement, scope, decisions, artifact envelope, acceptance criteria, and approval history. Working Notes, Requirement Decision Records, Knowledge Base Change Summaries, Specifications, Ticket Plans, Status pages, and Evidence reports can therefore become competing copies of the same fact. This increases maintenance cost, creates stale-link and contradictory-status risk, and makes it unclear which document is authoritative after implementation finishes.

## Goals

- Give each durable category of information one canonical owner.
- Keep pre-approval requirement exploration traceable without creating several independent copies.
- Allow later stages to reference approved decisions instead of reproducing their full text.
- Make completed workflows converge to a small set of current documents plus recoverable historical evidence.
- Preserve every approval, artifact ID, source link, test result, and unresolved limitation during consolidation.
- Detect broken references, contradictory status, missing targets, and accidental content loss before migration is considered complete.

## Non-goals

- Changing Full/Lite mode resolution, stage gates, test-choice semantics, Review requirements, or completion claims.
- Removing required artifact envelope fields or approval evidence.
- Rewriting, weakening, or silently deleting historical Requirements, Specifications, Ticket Plans, Reviews, or release evidence.
- Changing Full/Lite mode resolution, stage gates, approval authority, evidence meaning, or consumer package behavior in Codex, Claude, Generic, or Core runtime instructions. Minimal producer/template routing and validator instructions are in scope only when they enforce this approved document lifecycle without changing those semantics.
- Introducing a new persistence service, network dependency, external database, or release payload.

## Users and scenarios

### Maintainer starts a Full workflow

The maintainer creates one workflow Decision Packet for provisional requirement material. The packet can contain Working Notes, the Requirement Decision Record, and the proposed Knowledge Base Change Summary as clearly labeled sections with separate stable IDs and statuses. The maintainer does not create separate files containing repeated copies unless a repository contract requires a pointer.

### Requirement and knowledge gates are approved

The approved behavioral decisions become inputs to the Specification. Durable project facts are applied to the Knowledge Base only from the explicitly approved change summary. The packet records the approval and points to the resulting canonical artifacts; it does not remain a second source of current behavior.

### Implementation and Review finish

The Specification remains the canonical behavioral contract, the Ticket Plan remains the canonical implementation plan, Evidence remains the canonical record of observed commands and results, and Status remains a concise current-state index. The completed packet is marked `Superseded` or moved to the approved historical archive with a stable link.

### A maintainer opens an old link

A pointer or archive index identifies the canonical replacement, the artifact status, and the historical location. It must not present stale substantive content as current truth.

### A Lite operation is completed

The existing Lite rule remains unchanged: it does not create Full workflow artifacts merely to satisfy this lifecycle. User-requested product documents remain outside this workflow policy.

## Canonical ownership

The following ownership is normative for new Full workflow artifacts:

| Information category | Canonical owner | Permitted derived material |
| --- | --- | --- |
| Durable project facts, glossary, architecture, unresolved project context | `docs/project/knowledge-base.md` | Short index links and historical source references |
| Observable product behavior and acceptance criteria | Approved Specification | Ticket and evidence references to acceptance IDs |
| Implementation slices, dependencies, test choices, and ordering | Approved Ticket Plan | Status summaries and implementation evidence links |
| Actual commands, outputs, test results, review findings, and limitations | `docs/evidence/` artifact | Status summary and navigation links |
| Current workflow state and next eligible action | `docs/project/status.md` | Links to canonical artifacts only |
| Unapproved requirement exploration and proposed knowledge changes | One workflow Decision Packet | Pointer/index files with no duplicated substantive content |

No derived document may redefine a fact owned by another category. When a derived view needs context, it references the canonical artifact and stable section or decision IDs.

## Required behavior

1. A Full workflow that needs durable requirement documentation MUST use one Decision Packet per workflow ID for provisional Working Notes, the Requirement Decision Record, and the proposed Knowledge Base Change Summary. The packet MUST identify each section's artifact type, stable ID, status, inputs, and approval state.
2. A Decision Packet MUST remain `Draft` until the relevant requirement consensus and Knowledge Base change approval are explicit. Approval of one section MUST NOT silently approve another section or authorize implementation.
3. After requirement approval, the packet MUST link to the canonical Specification and Knowledge Base result. It MUST NOT be treated as the current behavioral contract once those approved artifacts exist.
4. A Knowledge Base Change Summary MUST be created only when an approved or accepted artifact changes durable project facts. A workflow with no durable knowledge change MUST NOT create an empty summary solely to satisfy the document pattern.
5. A pointer file MAY remain at a historical or compatibility path, but it MUST contain only the target artifact ID, canonical path, status, replacement reason, and recovery/history link. It MUST NOT repeat the full problem, requirements, acceptance criteria, or evidence.
6. A completed workflow MUST expose one canonical path for each applicable information category. Any superseded packet, duplicate draft, or historical artifact MUST be labeled `Superseded` or indexed in the approved archive and MUST point to its replacement or explain why no replacement exists.
7. Migration MUST preserve stable artifact IDs, workflow IDs, approval evidence, source references, unresolved decisions, and the original observed evidence. Moving or consolidating a file MUST NOT convert a Draft, unverified, skipped, or blocked result into Approved or Passed.
8. Status pages and indexes MUST summarize current state and links. They MUST NOT become a second copy of the complete Specification, Ticket Plan, or Review.
9. The repository MUST validate that every pointer resolves, every canonical artifact has the required envelope, every referenced status agrees with the target, and no approved artifact is orphaned by migration.
10. The lifecycle change MUST be behavior-neutral for Full/Lite routing, all existing approval gates, artifact semantics, test-choice rules, Review outcomes, safety boundaries, and release contracts.

## Edge cases and failure behavior

- If two documents claim the same category as canonical, migration MUST stop and report the conflict; it MUST NOT select one by filename or modification time.
- If a pointer target is missing, unreadable, outside the repository policy, or has a contradictory status, validation MUST fail closed and the old source MUST remain recoverable.
- If a proposed consolidation cannot preserve an approval, evidence limitation, or unresolved decision, the affected artifact MUST remain Draft or unverified and the migration MUST stop for review.
- If a workflow introduces new durable facts after its Knowledge Base Summary was approved, the new facts require a new disclosed summary and approval; silently appending them to the old approval is invalid.
- If a migration partially completes, staging, backup, primary errors, recovery errors, and the original source locations MUST be retained until the state is reconciled.
- A direct stage selection or Lite operation MUST NOT create a Decision Packet merely because a pointer or archive policy exists.

## Data, permissions, and external contracts

- Decision Packets and pointers use repository-relative paths and remain outside consumer plugin payloads unless an existing package contract explicitly includes them.
- The policy introduces no network access, runtime dependency, telemetry, credential storage, or external side effect.
- Only a `tools`-capable operation may claim that a packet was persisted, files were migrated, or validators were executed. A conversation-only host must emit user-managed artifacts without claiming repository persistence.
- Existing Core artifact envelope fields and Draft/Approved semantics remain mandatory.
- Historical archives may be outside the working tree, but their manifest and recovery location must be recorded by an approved repository evidence index.

## Compatibility, rollout, and recovery

The first rollout is additive and staged. Existing files remain valid inputs while the migration inventory and mapping are reviewed. The implementation may introduce the Decision Packet format, canonical ownership index, pointers, and validators before moving current drafts. File moves or removals require an approved Ticket scope and a recoverable backup or archive. Rollback restores the previous paths and statuses without rewriting the original artifact bytes or approval evidence.

## Constraints and assumptions

- The existing Core, adapter, and release contracts remain authoritative for workflow behavior.
- The policy is initially scoped to Full workflow documentation in this repository; Codex runtime slimming and other adapter changes are separate decisions unless explicitly added to an approved Ticket.
- Stable IDs are the link contract; filenames and headings may change only when the replacement mapping remains unambiguous.
- Duplicate detection is a maintenance validation concern, not permission to remove content automatically.

## Acceptance criteria

1. A documented Full workflow can be represented by one Decision Packet before approval, with Working Notes, Requirement Decision Record, and Knowledge Base Change Summary sections that retain separate IDs and statuses without repeating their full content in sibling files.
2. The canonical ownership table is applied to a representative workflow: Knowledge Base, Specification, Ticket Plan, Evidence, and Status each have one authoritative responsibility and reference one another by stable IDs.
3. A pointer file contains no duplicated substantive requirements and resolves to its canonical target; a broken or contradictory pointer fails validation.
4. A workflow with no durable project-fact change produces no empty Knowledge Base Change Summary.
5. Consolidation preserves approval evidence, Draft/unverified/skipped states, unresolved decisions, source links, and observed command results; validation detects any loss or status contradiction.
6. A completed workflow marks the Decision Packet as `Superseded` or indexes it in the approved archive and provides a recoverable path to the original material.
7. Partial migration leaves enough staging/backup/error information to restore the pre-migration state without guessing which source was authoritative.
8. Existing Full/Lite routing, approval gates, test-choice behavior, Review requirements, evidence honesty, and release/package tests remain unchanged and pass the applicable validation suite.
9. The repository contains no newly generated duplicate full-text copies of the same canonical artifact after migration, except for an explicitly versioned historical archive.
10. The final implementation and Review identify any deferred adapter scope, archive-retention decision, or environment-limited validation rather than treating them as completed.

## Deferred decisions

- Whether a Decision Packet should use Markdown sections, front matter, or a structured format.
- Whether pointer files should be generated and validated by a dedicated tool or by existing documentation tests.
- Whether historical packets remain in-repository, in a versioned evidence archive, or in an external managed archive.
- Whether the same lifecycle should be adopted by Generic and Claude adapter documentation in a later workflow.
