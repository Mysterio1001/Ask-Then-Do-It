# Document Lifecycle Artifact Contract

Core version: `1.4.1`

This is the repository-local contract for Full-workflow document ownership and
consolidation. It defines the semantic shape of a Decision Packet, compatibility
pointers, archive indexes, and the conditional Knowledge Base Change Summary.
It does not change Full/Lite routing, approval authority, evidence meaning, or
consumer package behavior.

## Shared envelope

Every logical packet, packet section, pointer, archive index, and canonical
artifact MUST include or unambiguously convey the common artifact envelope:

- `artifact_type`
- `artifact_id`
- `workflow_id`
- `core_version`
- `status`
- `inputs`
- `assumptions`
- `deferred`
- `handoff`
- `approval`

`artifact_id` and `workflow_id` are stable identifiers. They MUST be non-empty,
repository-independent strings matching `^[A-Za-z0-9][A-Za-z0-9._:-]*$`.
`core_version` MUST identify the Core contract used to create the artifact.
`approval` is explicit evidence for an approved artifact and MUST be empty or
null while a gated artifact is Draft.

The contract recognizes these exact status values:

- `Draft`, `Approved`, and `Superseded` are lifecycle states.
- `unverified`, `skipped`, and `blocked` are evidence states.

Moving or consolidating a file MUST preserve its status and approval evidence.
No operation in this contract promotes `Draft`, `unverified`, `skipped`, or
`blocked` material to `Approved` or `Passed`.

## Decision Packet

A workflow that needs durable Full-mode requirement documentation MUST use one
Decision Packet per `workflow_id`. The packet is the one provisional owner for
Working Notes, the Requirement Decision Record, and, only when applicable, the
proposed Knowledge Base Change Summary.

The human-readable packet uses clearly labeled sections. Each section MUST
carry its own complete envelope, use the packet `workflow_id`, and have a
distinct stable `artifact_id`. The required section artifact types are:

1. `Draft Working Notes`
2. `Requirement Decision Record`
3. `Knowledge Base Change Summary` when `knowledge_change.summary_required` is
   true

The packet envelope and each section envelope have independent statuses and
approval evidence. Approval of one section MUST NOT silently approve another
section or authorize implementation. The packet remains `Draft` until all
applicable requirement and knowledge approvals are explicit.

The packet records a `knowledge_change` decision:

- `summary_required: true` requires exactly one Knowledge Base Change Summary
  section with additions, modifications, and removals.
- `summary_required: false` MUST omit that section and MUST NOT create an empty
  summary artifact. The reason for the decision remains recorded in the packet.

After the approved Specification and Knowledge Base result exist, the packet
links to them and is no longer the current behavioral contract. A completed
packet is marked `Superseded` or indexed in the approved archive.

## Canonical ownership

Each durable information category has one canonical owner:

| Information category | Canonical owner | Permitted derived material |
| --- | --- | --- |
| Durable project facts | `docs/project/knowledge-base.md` | Short index links and historical source references |
| Observable product behavior | Approved Specification | Ticket and evidence references to acceptance IDs |
| Implementation slices | Approved Ticket Plan | Status summaries and implementation evidence links |
| Actual commands and results | `docs/evidence/` artifact | Status summary and navigation links |
| Current workflow state | `docs/project/status.md` | Links to canonical artifacts only |
| Unapproved requirement exploration | One workflow Decision Packet | Pointer or index metadata with no duplicated substantive content |

Derived documents MUST reference the canonical artifact and stable section or
decision IDs. They MUST NOT redefine a fact owned by another category.

## Pointer contract

A `Document Pointer` is metadata retained at a historical or compatibility
path. In addition to the common envelope it MUST contain:

- `target_artifact_id`: the stable ID of the canonical replacement.
- `canonical_path`: a repository-relative path to the replacement.
- `status`: the target's current status; validation requires agreement with the
  target.
- `replacement_reason`: a concise explanation for the replacement.
- `history_link`: a repository-relative recovery or historical source link.

Pointer files MUST contain only these target and recovery fields plus envelope
metadata. They MUST NOT repeat the problem, requirements, acceptance criteria,
or evidence. `canonical_path` and `history_link` MUST be repository-relative,
must use `/` separators, MUST NOT start with `/` or `\\`, and MUST NOT contain `..`.
External URLs are not canonical repository paths.

## Archive index contract

An `Archive Index` is the recoverable map for superseded material. It uses the
common envelope and an `entries` list. Each entry MUST contain the same five
pointer metadata fields: `target_artifact_id`, `canonical_path`, `status`,
`replacement_reason`, and `history_link`. An entry MUST not contain a second
copy of substantive requirements, acceptance criteria, or evidence.

## Conditional knowledge summary

Create a Knowledge Base Change Summary only when an approved or accepted
artifact changes durable project facts. Display `additions`, `modifications`,
and `removals` together before approval. A workflow with no durable change
records `summary_required: false` in its packet and creates no empty summary.

## Validator manifest

The repository validator consumes an explicit JSON manifest with
`schema_version: 1`, `canonical`, `pointers`, `approved_artifacts`, and an
optional `historical_archive_paths` array. Canonical and pointer records carry
the common envelope plus their path and ownership fields. The manifest is an
index for validation, not another canonical copy of artifact content. The
validator is read-only and fails closed for missing files, unsafe paths,
contradictory status, duplicate canonical claims, orphaned approvals, invalid
envelopes, or duplicate full text outside explicitly listed historical
archives.

When a migration is present, the manifest MUST also contain a `migration`
object with a stable `migration_id`, matching `workflow_id` and `core_version`,
`status` (`staged`, `completed`, `partial`, or `failed`), relative
`source_manifest`, `source_manifest_sha256`, `backup_root`, and `staging_root`
paths, plus a `recovery` object. Recovery metadata MUST include a boolean
`rollback_available`, a null or string `primary_error`, and a string-array
`recovery_errors`. The source manifest lists each source's
`source_artifact_id`, `target_artifact_id`, `target_section_id`, original
`source_path`, recoverable `backup_path`, `original_sha256`,
`source_status_before`, `target_status_after`, `source_disposition`, and
`source_exists_after`. Every target and status MUST agree with the canonical
manifest; a Draft, unverified, skipped, or blocked source MUST NOT become
Approved. Every backup MUST remain inside `backup_root`, match its declared
digest, and remain distinct from its source. Completed migrations MUST retain
rollback availability and no error metadata; partial or failed migrations MUST
retain error metadata. Missing manifests, backup files, staging directories,
unsafe paths, duplicate entries, status promotion, or hash mismatches fail
closed.

## Recovery and compatibility

Stable IDs, workflow IDs, source references, approval evidence, unresolved
decisions, and observed command results survive consolidation. Existing source
bytes remain recoverable until an approved migration completes. A pointer or
archive entry is a navigation aid, never permission to delete or silently
repair a source artifact.
