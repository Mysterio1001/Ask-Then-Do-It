# Codex Skill Runtime Slimming — Requirement Decision Record

Artifact type: Requirement Decision Record

Artifact ID: `codex-skill-runtime-slimming-rdr`

Workflow ID: `codex-skill-runtime-slimming-2026-09-15`

Core version: `1.4.1`

Status: Draft

Inputs: [Draft Working Notes](codex-skill-runtime-slimming-working-notes.md), current Codex adapter sources and tests, Core 1.4.1 rules and artifacts, project Knowledge Base, and the user's GPT-6 Astra optimization guidance.

Assumptions: The first release is behavior-equivalent. The current universal trigger, Full/Lite semantics, approval gates, evidence boundaries, and model-neutral contracts remain observable requirements. Official GPT-6 guidance is treated as user-supplied input for this workflow because the official page was unavailable during the initial audit.

Deferred: Any narrowing of the universal trigger; conditional execution of the twelve Review lenses; autonomous Review finding correction; model-specific instruction variants; changes to Core rule semantics; changes to Generic or Claude adapters; release versioning and external publication.

Handoff: After approval, write the behavior-level Specification, then split it into implementation Tickets. Do not implement from this record alone.

Approval: Pending

## Problem and desired outcome

The Codex adapter's public skills preserve the required workflow contracts, but the runtime instructions repeat mode guards, artifact envelope fields, Full routing details, architecture lenses, and maintainer rationale. The main orchestrator is also longer than a router needs to be. This increases loaded context, makes policy drift more likely, and makes small maintenance changes harder to reason about.

The desired outcome is a smaller, clearer, responsibility-separated Codex runtime in which each instruction is loaded at the stage that needs it, shared contracts have one canonical source, and tests verify behavior rather than exact prose.

## Users and success signals

- Codex users receive the same Full/Lite routing, gates, evidence claims, and completion boundaries.
- Maintainers can update a shared contract once instead of synchronizing repeated prose.
- GPT-6 Astra can use a short router and load stage details progressively.
- GPT-5.x and earlier models still receive explicit, single-hop instructions for every direct stage entry.
- Codex contract and release tests pass without relying on duplicated prompt sentences.

## Scope

Included:

1. Codex public skills under `adapters/codex/plugin/ask-then-do-it/skills/`.
2. Codex rule mapping and conformance references only where required by the source reorganization.
3. Codex unit tests, token-proxy fixtures, and release contract tests required to validate the reorganized source.
4. New plugin-local references for Full routing, the portable artifact envelope, the specification template, and the architecture lenses when the approved Specification confirms those extractions.
5. Removal of runtime-only maintainer comments that do not carry model instructions.

Excluded:

- Changes to user-visible workflow semantics or trigger coverage.
- Changes to Core mandatory rule meaning.
- Changes to Full/Lite mode precedence or failure behavior.
- Changes to approval authority, Draft/Approved transitions, TDD Red, Direct test restrictions, evidence honesty, or completion claims.
- Changes to Generic or Claude adapter runtime behavior.
- New `AGENTS.md` files.
- Model calls, external publication, dependency installation, or release version changes.

## Primary behavior and user flow

1. Codex skill selection continues to expose the existing names and descriptions.
2. The root `ask-then-do-it` skill remains the canonical capability and Full/Lite mode resolver.
3. A resolved Lite operation continues to load and follow the canonical Lite workflow only.
4. A resolved Full operation continues to load the Full routing details and then the selected stage skill.
5. Direct stage selection continues to require current-operation mode proof; it cannot imply Full.
6. A stage that emits a logical artifact reads the canonical envelope reference and retains its stage-specific fields, status, approval, and handoff requirements.
7. Review and architecture work retain the fixed twelve-lens contract and all existing outcome labels.
8. The resulting package contains the new references and remains self-contained; runtime behavior does not depend on repository documentation outside the plugin.

## Edge cases and failure behavior

- Missing, malformed, unsupported, or unreadable Config keeps the existing fail-closed Full behavior.
- Conflicting explicit modes still pause for clarification.
- A stage with no mode proof still delegates to the root resolver.
- A missing reference, broken relative link, or incomplete contract is a packaging and validation failure; the adapter must not silently continue with inferred rules.
- A producer must not omit required envelope fields merely because they moved to a reference.
- Tests must distinguish absent evidence from a changed contract and must not accept a prompt that only contains a link with no reachable reference.
- Lite must not load Full-only references or fabricate Full artifacts.

## Data, dependencies, security, privacy, and operational constraints

- References must use repository-relative, plugin-contained paths and be included by the existing recursive package builder.
- No new runtime dependency, network access, persistence mechanism, or external side effect is introduced.
- Existing capability honesty, approval boundaries, safe simulated deletion, and evidence disclosure remain unchanged.
- Existing user changes and historical evidence are preserved.
- A source reorganization that changes package bytes requires the repository's normal candidate and release process; this task does not authorize publication.

## Acceptance criteria

1. The root skill is a router with explicit routes to Full-only references and Lite, while its canonical mode precedence and capability claims remain observable.
2. Each public stage has a concise direct-entry guard that preserves all five mode outcomes: stage selection is not Full, missing proof delegates, Lite exits to Lite, only proven Full continues, and mode is not persisted or reused.
3. Shared artifact envelope fields have one canonical plugin-local reference; each producer has an explicit read instruction and retains its stage-specific contract.
4. Full routing, specification template, and architecture lens content are loaded only by the stages that need them, with at most one reference hop.
5. Maintainer-only comments are absent from model-visible runtime instructions.
6. Existing mandatory rule IDs remain mapped to reachable Codex source sections, and the Codex conformance manifest remains complete.
7. Tests validate metadata, route/reference reachability, required invariant IDs, artifact fields, direct-stage behavior, Lite isolation, package inventory, and deterministic token-proxy contracts without requiring identical prose.
8. The Codex test and applicable release validation suites pass, with any environment-limited checks disclosed.
9. No observable Full/Lite, approval, evidence, test-choice, Review, architecture, or completion behavior changes in this first version.

## Confirmed decisions

- The first version is a behavior-equivalent structural refactor.
- The universal trigger remains unchanged for this version.
- Core safety, approval, mode, artifact, testing, Review, and evidence invariants remain explicit.
- Progressive disclosure uses one clear reference hop and explicit read-before-action wording.
- Codex is the only adapter in scope.

## Assumptions

- Existing release builders recursively include plugin-local reference files.
- The current 1.4.1 Core rule IDs remain the source of conformance truth.
- Cross-model live evaluation is not available as a prerequisite for this source refactor and will be a later validation activity.

## Deferred decisions

- Whether to narrow implicit trigger coverage after a trigger matrix and cross-model evaluation.
- Whether ordinary Review should report fewer than twelve lens outcomes.
- Whether an end-to-end implementation may auto-correct in-scope Review findings without a second approval.
- Whether the resulting source changes warrant a patch version and candidate build.

## Consensus evidence

The user explicitly approved the behavior-equivalent first-version boundary on 2026-09-16 with `核准`, in response to the complete scope decision presented from the Draft Working Notes.
