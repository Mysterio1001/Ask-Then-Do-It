# Codex Skill Runtime Slimming — Knowledge Base Change Summary

Artifact type: Knowledge Base Change Summary

Artifact ID: `codex-skill-runtime-slimming-kb-change-summary`

Workflow ID: `codex-skill-runtime-slimming-2026-09-15`

Core version: `1.4.1`

Status: Draft

Inputs: [Requirement Decision Record](codex-skill-runtime-slimming-requirement-decision-record.md), current Codex adapter audit, and existing [Project Knowledge Base](../knowledge-base.md).

Assumptions: This summary proposes only the durable facts needed to guide the approved first-version structural refactor. It does not approve implementation, release, or any deferred behavior changes.

Deferred: Trigger narrowing, Review auto-correction, conditional lens semantics, cross-model live results, version bump, and publication.

Handoff: Apply only the displayed changes after the Requirement Decision Record and this summary are explicitly approved together; then hand off to Specification authoring.

Approval: Pending

## Additions

- The Codex adapter will use a behavior-equivalent, progressive-disclosure refactor as the first version of skill slimming.
- The root Codex skill will own routing while shared Full routing, artifact envelope, specification template, and architecture lens instructions are plugin-local references loaded by need.
- Public stage skills will retain concise direct-entry guards so older models do not have to infer mode safety from an indirect reference.
- Contract tests will validate reachable semantics and package inventory rather than exact duplicated prose.

## Modifications

- The Codex adapter architecture map will distinguish the root router, stage skills, and shared references as separate runtime responsibilities.
- The Codex maintenance guidance will treat prompt text as an adapter implementation of Core rules, with Core semantics remaining authoritative.
- The Codex validation notes will include reference reachability, direct-stage guard coverage, and behavior-equivalent token-proxy/source inventory checks.

## Removals

- Remove duplicated mode-resolution prose from stage bodies after replacing it with an explicit equivalent guard.
- Remove duplicated portable-envelope field lists from stage bodies after adding a reachable canonical reference and stage-specific reminders.
- Remove runtime-visible maintainer comments that carry no execution rule.
- Do not remove any Core rule, approval gate, evidence requirement, test-choice rule, Review lens, or safety boundary.

## Approval boundary

Approval applies only to these displayed additions, modifications, and removals. It does not authorize implementation code, a Core semantic change, a trigger change, a model-specific prompt variant, a release, or external publication.

Approval: Pending explicit approval of this complete summary together with the linked Requirement Decision Record.
