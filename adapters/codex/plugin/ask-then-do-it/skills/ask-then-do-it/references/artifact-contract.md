## Portable artifact contract

This package-local contract owns the fields shared by every persisted workflow artifact. A stage keeps its own artifact type, domain fields, gate, status transition, evidence label, and handoff; this contract supplies only the common envelope and evidence boundary.

## Required envelope

Every artifact must include or unambiguously convey:

- `artifact_type`
- `artifact_id`
- `workflow_id`
- `core_version`
- `status`
- `inputs`
- `assumptions`
- `deferred`
- `handoff`

Artifacts that have an approval gate also include `approval` evidence. Preserve the envelope when revising an artifact; do not silently replace a stable ID or workflow ID.

When creating an artifact, assign a stable `artifact_id` and use the same `workflow_id` as upstream artifacts in this workflow; at the first artifact, establish one stable workflow ID for later stages. Set `core_version` to the Core contract version `1.4.3` (not the plugin version). Record upstream artifacts and decisions in `inputs`, and identify the next stage or owner in `handoff`. Preserve these values when revising an artifact.

## State and evidence honesty

Use the stage's allowed states and do not promote `Draft` to `Approved` (or another accepted state) without the stage's explicit approval evidence. `status` must agree with the conversation and the recorded evidence. Distinguish observed results, unavailable checks, assumptions, and deferred work; never describe an unavailable or skipped check as passed.

## Read-before-action failure

Each artifact-producing stage links here directly and must read this contract completely before creating or emitting its artifact. If the contract cannot be read, is missing, or is incomplete, stop before artifact creation and leave the stage handoff pending; do not reconstruct the common fields from memory.
