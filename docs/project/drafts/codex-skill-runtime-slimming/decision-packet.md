# Codex Skill Runtime Slimming - Decision Packet

Artifact type: Decision Packet
Artifact ID: `codex-skill-runtime-slimming-decision-packet`
Workflow ID: `codex-skill-runtime-slimming-2026-09-15`
Core version: `1.4.1`
Status: Draft
Inputs: Existing Codex slimming draft set, current Core/Codex sources, tests, release contracts, and user-provided GPT-6 Astra optimization guidance.
Assumptions: The first version remains behavior-equivalent; Full/Lite routing, approval gates, evidence semantics, and release boundaries are unchanged.
Deferred: Cross-model live evaluation, other adapter changes, release versioning, external publication, and any behavior change beyond structural slimming.
Handoff: Complete requirement and Knowledge Base approval before Specification authoring; do not implement from this packet alone.
Approval:

This packet consolidates the three provisional draft artifacts for one workflow.
Their original bytes, stable IDs, unresolved decisions, and pending approval
states are retained in the migration backup recorded by
`migration/source-manifest.json`. The backup is historical recovery material;
this packet is the only current provisional owner of the substantive draft
content.

## Packet Sections

### Draft Working Notes

```json
{
  "artifact_type": "Draft Working Notes",
  "artifact_id": "codex-skill-runtime-slimming-working-notes",
  "workflow_id": "codex-skill-runtime-slimming-2026-09-15",
  "core_version": "1.4.1",
  "status": "Draft",
  "inputs": ["user-guidance", "runtime-audit", "core-and-codex-contracts"],
  "assumptions": ["Full fallback because project and user Config were absent during the audit."],
  "deferred": ["Cross-model live evaluation matrix", "Other adapters", "Release and publication"],
  "handoff": "Requirement Decision Record and Knowledge Base Change Summary",
  "approval": null
}
```

Preserved source approval state: the requirement boundary was confirmed by the
user on 2026-09-16, while formal RDR and Knowledge Base Change Summary approval
remained pending.

The working notes confirm the behavior-equivalent boundary, the goals of
slimming and responsibility separation, the repeated mode/artifact/lens
instructions, and the requirement to keep mode precedence, approval state,
TDD Red, Direct restrictions, and evidence honesty explicit. Progressive
disclosure remains one clear hop with direct-entry guards for older models.
The proposed first version is limited to Codex structural refactoring:
shorter descriptions, a router-shaped root skill, shared references, concise
guards, and contract tests instead of exact prompt copies. Universal trigger
coverage, Full/Lite semantics, approval gates, Review lenses, and Lite
correction approval remain unchanged. Trigger narrowing, conditional lenses,
and autonomous Review correction are deferred.

### Requirement Decision Record

```json
{
  "artifact_type": "Requirement Decision Record",
  "artifact_id": "codex-skill-runtime-slimming-rdr",
  "workflow_id": "codex-skill-runtime-slimming-2026-09-15",
  "core_version": "1.4.1",
  "status": "Draft",
  "inputs": ["working-notes", "codex-sources-and-tests", "core-1.4.1", "user-guidance"],
  "assumptions": ["The first release is behavior-equivalent."],
  "deferred": ["Universal trigger narrowing", "Conditional Review lenses", "Review auto-correction", "Model-specific variants", "Core/Generic/Claude changes", "Release versioning"],
  "handoff": "Behavior-level Specification",
  "approval": null
}
```

Preserved source approval state: `Pending`.

The RDR defines the desired outcome as a smaller, clearer Codex runtime with
one canonical source for shared contracts and stage-specific progressive
disclosure. Public skill names, the root resolver, Lite isolation, direct-stage
mode proof, the twelve Review lenses, package self-containment, and all safety,
approval, evidence, and completion boundaries remain observable requirements.
Missing or malformed Config remains fail-closed Full; conflicting modes pause;
missing references are packaging failures; Lite does not load Full references
or fabricate Full artifacts. No network, dependency, persistence, or release
side effect is introduced.

### Knowledge Base Change Summary

```json
{
  "artifact_type": "Knowledge Base Change Summary",
  "artifact_id": "codex-skill-runtime-slimming-kb-change-summary",
  "workflow_id": "codex-skill-runtime-slimming-2026-09-15",
  "core_version": "1.4.1",
  "status": "Draft",
  "inputs": ["requirement-decision-record", "codex-audit", "project-knowledge-base"],
  "assumptions": ["The summary proposes durable facts only and does not approve implementation or release."],
  "deferred": ["Trigger narrowing", "Review auto-correction", "Conditional lenses", "Cross-model results", "Version bump", "Publication"],
  "handoff": "Project Knowledge approval and Specification authoring",
  "approval": null
}
```

Preserved source approval state: `Pending`.

The proposed additions are a behavior-equivalent progressive-disclosure
refactor, a root router, plugin-local shared references, concise direct-entry
guards, and contract tests that validate reachable semantics and package
inventory. Proposed modifications separate the Codex architecture map into
router, stages, and shared references, and treat prompt text as an adapter
implementation of authoritative Core rules. Proposed removals are only
duplicated mode resolution, portable-envelope lists, and runtime-visible
maintainer comments; Core rules, approval gates, evidence requirements,
test-choice rules, Review lenses, and safety boundaries remain.

## Source and recovery links

- [Source manifest](migration/source-manifest.json) records all three original
  paths, stable IDs, and SHA-256 digests.
- [Migration backup manifest](migration/source-manifest.json) identifies the
  backup files that preserve the original bytes.
- The staging area remains available for rollback or a later approved
  transition; it is intentionally empty after the completed migration.
- This packet is not an approval of the RDR or Knowledge Base Summary. The
  original pending states remain unchanged.
