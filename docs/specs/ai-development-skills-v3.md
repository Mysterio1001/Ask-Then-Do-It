# Portable AI Development Workflow - v3 Specification

Artifact type: Specification

Artifact ID: `portable-ai-development-workflow-v3-spec`

Workflow ID: `grill-me-core-v3`

Core version: `3.0.0`

Status: Approved

Approval: Explicitly approved by the user in the project conversation on 2026-07-29 with the response `好`.

## Inputs

- The approved [Portable AI Development Workflow - v2 Specification](ai-development-skills.md).
- The validated `2.1.0` Codex and Generic release maintained in this repository.
- Explicit requirement consensus reached with the user on 2026-07-29.

## Problem

Core v2 establishes a portable requirements-to-review workflow, but it does not yet preserve durable project knowledge during requirement interrogation, require a consistent refactoring vocabulary, or provide a dedicated architecture-diagnosis stage. As a result, models may need to relearn project context, code reviews may vary in depth and terminology, and architecture concerns may be reported without a safe path from diagnosis to approved refactoring.

The project needs a model-neutral Core v3 that adds evidence-backed project knowledge, documented requirement interrogation, consistent code and architecture lenses, safe deletion analysis, and an Architecture Improvement Report without weakening the existing human approval gates or capability boundaries.

## Goals

- Add a single canonical Project Knowledge Base derived only from approved evidence.
- Add a documented requirement-interrogation mode that maintains provisional working notes and proposes approved knowledge updates.
- Define twelve mandatory Architecture and Refactoring Lenses shared by code review and architecture diagnosis.
- Add a dedicated architecture-improvement module that is diagnostic-only by default.
- Define safe simulated deletion analysis and tightly gate any actual deletion experiment.
- Route systemic review findings into architecture diagnosis and route accepted architecture findings back through Specification, Ticket Plan, and TDD.
- Preserve direct modular invocation while allowing explainable automatic routing.
- Preserve honest degradation for conversation-only hosts.
- Upgrade the Core, Codex adapter, Generic adapter, and release identity to `3.0.0` without overwriting the validated `2.1.0` release.
- Provide deterministic conformance, scenario, regression, release, and reproducibility checks for all new behavior.

## Non-goals

- Automatically refactor code after an architecture diagnosis.
- Treat acceptance of an Architecture Improvement Report as implementation authorization.
- Perform destructive deletion testing in a normal working copy or user environment.
- Invent project knowledge to make the Knowledge Base appear complete.
- Require architecture diagnosis after every ticket or trivial code change.
- Replace the existing requirement, Specification, Ticket Plan, TDD, or review approval gates.
- Promise filesystem, command, persistence, testing, or isolation capabilities in a conversation-only host.
- Publish, upload, install, or modify a personal AI-agent environment as part of this Specification.
- Add a dedicated provider adapter other than Codex or Generic prompts in v3.

## Users and scenarios

- A user starts an existing-project change and the orchestrator selects documented requirement interrogation because durable project knowledge is relevant.
- A user directly invokes documented requirement interrogation and expects exactly one high-impact question per turn.
- A user approves a Requirement Decision Record together with a visible Knowledge Base change summary.
- A reviewer applies the same twelve lenses to a local change and routes a systemic finding to architecture diagnosis.
- A maintainer requests an architecture assessment and receives a report based on dependency tracing and simulated deletion without repository mutation.
- A user accepts an architecture diagnosis and is returned to Specification authoring before any refactoring begins.
- A v2 project uses v3 for the first time and receives a proposed, evidence-backed Knowledge Base without having existing approved artifacts rewritten.
- A conversation-only model analyzes user-supplied artifacts, labels unavailable evidence honestly, and emits Markdown for user-managed persistence.

## Terminology

- **Project Knowledge Base**: the canonical, current project-context artifact stored at `docs/project/knowledge-base.md` in a repository-backed workflow.
- **Draft Working Notes**: provisional notes collected during documented requirement interrogation. They are not approved project facts.
- **Knowledge Base Change Summary**: the additions, modifications, and removals proposed from a specific approved or accepted upstream artifact.
- **Documented requirement interrogation**: requirement interrogation combined with Draft Working Notes and evidence-backed Knowledge Base synchronization. Adapters may expose this as `grill-with-docs`.
- **Architecture and Refactoring Lens**: one mandatory diagnostic perspective used to inspect maintainability and change cost.
- **Simulated deletion analysis**: read-only dependency and impact tracing that asks what would break if a component were removed, without deleting it.
- **Actual deletion experiment**: temporary removal performed only in an explicitly authorized, disposable, isolated environment with real tools.
- **Architecture Improvement Report**: a diagnostic artifact that records architecture evidence and proposals but does not authorize refactoring.

## Required behavior

### 1. Core v3 structure and rule compatibility

The project MUST evolve the model-neutral source under `core/` to Core `3.0.0` before changing provider adapters.

Core v3 MUST retain the semantic meaning and stable identifiers of all mandatory v2 rules. A v2 rule whose meaning must change MUST be superseded by a new rule identifier rather than silently redefined.

Core v3 MUST add normative contracts for:

1. Project knowledge management.
2. Documented requirement interrogation as a composition of requirement interrogation and knowledge management.
3. Architecture improvement diagnosis.
4. The twelve Architecture and Refactoring Lenses.
5. Architecture Improvement Reports and safe deletion analysis.

Core modules MUST remain model- and provider-neutral. Provider invocation syntax, metadata, installation paths, and host APIs MUST remain inside adapters.

The v3 mandatory rule catalog MUST add at least these stable rules:

- `ROUTE-USER-001`: honor an explicit user-selected module or interrogation mode over automatic routing.
- `ROUTE-DOCS-001`: announce why documented requirement interrogation was selected automatically.
- `KB-EVIDENCE-001`: derive formal Knowledge Base content only from approved or accepted evidence.
- `KB-DRAFT-001`: keep unapproved interrogation content in Draft Working Notes.
- `KB-SYNC-001`: disclose additions, modifications, and removals before a Knowledge Base update is approved.
- `REVIEW-LENSES-001`: evaluate all twelve core lenses with evidence or a justified non-applicable result.
- `ARCH-DIAG-001`: keep architecture improvement diagnostic-only unless a later approved workflow authorizes implementation.
- `ARCH-DELETE-001`: prevent actual deletion during default simulated deletion analysis and enforce all gates for an actual experiment.
- `ARCH-REPORT-001`: produce a structured Architecture Improvement Report whose acceptance does not authorize code changes.
- `ARCH-REFLOW-001`: return accepted refactoring proposals through Specification, Ticket Plan, and TDD.
- `MIGRATE-V2-001`: initialize v3 project knowledge without overwriting approved v2 artifacts.

Every conforming v3 adapter MUST map every mandatory v3 rule in its conformance manifest.

### 2. Logical artifacts

Core v3 MUST retain the five v2 logical artifact types and add three types:

1. Requirement Decision Record.
2. Specification.
3. Ticket Plan.
4. Implementation Evidence.
5. Review Report.
6. Project Knowledge Base.
7. Draft Working Notes.
8. Architecture Improvement Report.

All artifacts MUST retain the shared v2 artifact envelope where applicable. Type-specific states and fields MAY extend the envelope without weakening approval evidence.

Draft Working Notes MUST remain `Draft`. Individual entries MUST be labeled `proposed`, `confirmed`, or `unresolved`. A `confirmed` working-note entry means the user confirmed it during interrogation; it does not become formal project knowledge until the corresponding upstream artifact and disclosed Knowledge Base changes are approved.

### 3. Project Knowledge Base

A repository-backed workflow MUST maintain at most one canonical Project Knowledge Base at:

`docs/project/knowledge-base.md`

The Knowledge Base MUST contain these sections:

1. Glossary.
2. Architecture map.
3. Important decisions.
4. External dependencies.
5. Unresolved items.
6. Links to Requirement Decision Records, Specifications, and Ticket Plans.

The Knowledge Base MAY link to additional approved or accepted artifacts, including Architecture Improvement Reports, when they provide relevant evidence.

The workflow MUST propose a Knowledge Base update whenever an approved or accepted upstream artifact introduces, changes, supersedes, or resolves durable project knowledge.

Every proposed update MUST:

- Identify its upstream evidence.
- Separate additions, modifications, and removals.
- Avoid facts that are not supported by the cited evidence.
- Mark incomplete or conflicting facts as unresolved rather than inventing a resolution.
- Preserve traceability to superseded decisions instead of erasing their historical evidence.

The proposed update MUST be displayed with the upstream artifact approval request. Explicit approval of that upstream artifact also approves only the Knowledge Base changes disclosed in the same request. Hidden, later, or materially changed Knowledge Base edits require another explicit approval.

### 4. Documented requirement interrogation

The normal requirement module MUST continue to ask exactly one high-impact question per turn, include a recommendation and principal tradeoff, and prohibit implementation before explicit consensus.

Documented requirement interrogation MUST add these behaviors:

- Read the existing Knowledge Base and relevant approved artifacts when the host has access.
- Record provisional discoveries in Draft Working Notes.
- Label each note `proposed`, `confirmed`, or `unresolved`.
- Keep unapproved notes out of the formal Knowledge Base.
- At consensus, produce a Requirement Decision Record and a Knowledge Base Change Summary.
- Request one explicit approval covering the displayed Requirement Decision Record and displayed Knowledge Base changes.

A tools-capable adapter SHOULD persist Draft Working Notes under the repository's documentation conventions. When no convention exists, it SHOULD use `docs/project/drafts/` with a workflow-specific filename. This default is not the canonical Knowledge Base path and MUST NOT be treated as approved knowledge.

### 5. Routing and user control

Adapters MUST support direct access to the normal requirement mode and documented requirement mode. The Codex adapter MUST expose documented requirement interrogation as `$grill-with-docs`; the Generic adapter MUST provide an independently usable equivalent prompt.

The orchestrator SHOULD automatically select documented requirement interrogation when at least one of these conditions holds:

- A Project Knowledge Base already exists.
- The requested work changes an existing system.
- The discussion introduces project knowledge that will likely be useful beyond the current workflow.

Automatic selection MUST be announced with a brief reason. An explicit user request for the normal requirement mode or documented mode MUST override automatic selection.

The orchestrator MUST NOT treat module names as required user knowledge. Natural-language requests MUST be routed by intent when sufficient evidence exists.

### 6. Twelve Architecture and Refactoring Lenses

Core v3 MUST define these twelve mandatory lenses in this order:

1. **Duplicated Code or Policy**: equivalent behavior or business rules maintained in multiple places.
2. **Long Function**: a function whose size or mixed responsibilities obstruct understanding, testing, or change.
3. **Large Module or Class**: a unit that owns too many responsibilities or reasons to change.
4. **Long Parameter List**: an interface whose parameters expose unstable coordination or missing concepts.
5. **Data Clumps**: related values repeatedly passed or stored together without a coherent abstraction.
6. **Primitive Obsession**: domain meaning represented primarily through unconstrained primitive values.
7. **Feature Envy**: behavior that depends more on another unit's data or responsibilities than its own.
8. **Divergent Change**: one unit repeatedly changed for unrelated reasons.
9. **Shotgun Surgery**: one behavioral change requiring edits across many locations.
10. **Message Chains**: long navigation or call chains that expose internal structure and amplify coupling.
11. **Leaky Abstraction**: callers must understand or compensate for implementation details hidden by an abstraction.
12. **Shallow Module**: a module whose interface complexity is not justified by the functionality it hides.

Adapters and projects MAY add project-specific lenses but MUST NOT remove, rename incompatibly, or silently skip a core lens.

For every core lens, an assessment MUST provide evidence and one of these outcomes:

- `finding`
- `no-finding`
- `not-applicable`, with a reason
- `unverified`, with the missing evidence identified

The lens set combines code-smell and architecture perspectives. It MUST NOT be represented as an unchanged canonical list from a single external publication.

### 7. Code review responsibilities

Evidence-based code review MUST apply all twelve lenses to the changed code and its relevant impact area. This is a focused screen, not automatically a system-wide architecture assessment.

Each reported lens finding MUST identify the trigger, impact, evidence, and precise location when available. Merely naming a lens does not satisfy review.

When a finding is cross-module, systemic, or indicates architecture-level change cost, the reviewer MUST route or recommend routing to architecture improvement diagnosis. If an accepted Architecture Improvement Report already tracks the same concern, the Review Report SHOULD reference it instead of creating a duplicate record.

Review remains diagnosis and does not authorize fixes.

### 8. Architecture improvement diagnosis

Core v3 MUST add an independently addressable architecture improvement module. The Codex adapter MUST expose it as `$improve-architecture`; the Generic adapter MUST provide an independently usable equivalent prompt.

The module MUST be diagnostic-only by default. It MUST NOT edit production code, delete project files, or begin a refactor merely because a user requested or accepted an architecture assessment.

Architecture diagnosis MUST apply all twelve lenses to the declared module or system scope and add dependency tracing, change-impact analysis, and simulated deletion analysis.

It MUST run or be offered under these conditions:

1. The user directly requests architecture diagnosis.
2. Code review discovers architecture-level signals such as Shallow Module, Leaky Abstraction, Shotgun Surgery, or equivalent systemic evidence.
3. A related group of Tickets is complete or a release milestone is approaching.

It MUST NOT run after every Ticket by default. An automatic trigger MUST be announced with its reason before diagnosis begins.

### 9. Deletion analysis safety

Simulated deletion analysis MUST be the default. It MUST use read-only dependency and impact tracing and MUST NOT remove, rename, move, or rewrite files or components.

An actual deletion experiment MAY occur only when all of these conditions are satisfied:

1. The user explicitly authorizes the actual deletion experiment after its scope and risks are stated.
2. The host proves the Tools capability required to inspect, modify, and verify the isolated copy.
3. The experiment occurs in a disposable, isolated environment that can be abandoned without affecting the user's working copy, personal installation, external system, or authoritative data.

The workflow MUST record the isolated environment, deleted scope, commands or checks performed, raw outcomes, and restoration or disposal result. A failure to prove any condition MUST fall back to simulated deletion analysis.

### 10. Architecture Improvement Report

Every architecture diagnosis MUST produce or emit an Architecture Improvement Report with:

1. Analysis scope and limitations.
2. System architecture summary.
3. Simulated or explicitly authorized actual deletion-analysis results.
4. Results for all twelve core lenses.
5. Finding evidence, impact, and confidence.
6. Prioritized improvement proposals.
7. Potentially affected modules.
8. Unresolved items.
9. Links to relevant artifacts.
10. A Knowledge Base Change Summary when durable knowledge changed.

The report MUST use one of these states:

- `draft`
- `accepted`
- `rejected`
- `superseded`

An inapplicable report field MUST contain `not-applicable` and a reason rather than being omitted silently.

Changing a report from `draft` to `accepted` requires explicit user evidence. Acceptance confirms the diagnosis and permits Specification work to begin; it MUST NOT authorize production-code changes, deletion, or refactoring.

Every accepted improvement that would change project behavior or structure MUST return through an approved Specification, an approved vertical Ticket Plan, and TDD implementation before it can be marked implemented.

### 11. Capability-aware behavior

Core v3 MUST retain the cumulative `conversation`, `tools`, and `multi_agent` capability profiles.

In the Conversation profile, an adapter MUST:

- Declare `conversation` as the proven capability before analysis.
- Ask the user to supply or upload required code, directory structure, and artifacts.
- Perform only logical analysis supported by supplied evidence.
- Mark unverifiable results as `unverified` and impossible checks as `unavailable`.
- Emit complete Markdown artifacts for user-managed storage and re-supply.
- Remind the user that cross-session persistence remains their responsibility when an artifact handoff depends on it.

A Conversation adapter MUST NOT claim it inspected a repository, modified files, executed tests, persisted artifacts, performed an actual deletion experiment, or completed an independent review unless the corresponding capability and raw evidence are genuinely available.

Tools and Multi-agent adapters MAY provide stronger evidence only to the extent their declared and validated capabilities support it.

### 12. v2 migration and compatibility

Core, Codex adapter, Generic adapter, and release versions MUST be `3.0.0` for this workflow extension. Existing `2.1.0` release artifacts MUST remain preserved and MUST NOT be overwritten by the v3 build.

Existing v2 Skill names, modular entry points, artifact meaning, approval gates, and mandatory rule semantics MUST remain compatible unless this Specification explicitly adds behavior.

Migration MUST be non-destructive and deferred until a v2 project first uses v3. On first use, the workflow MUST:

1. Inspect user-supplied or host-accessible approved v2 artifacts.
2. Propose an initial Project Knowledge Base derived only from those artifacts.
3. Display additions, modifications, and removals; an initial migration will normally contain additions only.
4. Ask for explicit user approval before creating or treating the Knowledge Base as active.
5. Mark unsupported or missing facts unresolved.

Migration MUST NOT rewrite, relabel, or overwrite approved v2 Requirement Decision Records, Specifications, Ticket Plans, Implementation Evidence, or Review Reports.

Existing v2 Generic prompts MAY continue to run independently but do not gain v3 behavior unless the user selects the v3 prompts.

### 13. Adapter requirements

The v3 Codex Plugin MUST retain the six existing Skills and add:

- `grill-with-docs`
- `improve-architecture`

The primary Codex orchestrator MUST be able to route to all eight Skills. Direct invocation MUST remain available for advanced users, and explicit direct invocation MUST override automatic routing.

The v3 Generic adapter MUST retain one self-contained workflow entry point and modular prompts. It MUST add independently usable documented-requirements and architecture-improvement prompts and include both in the combined entry point's routing contract.

Adapter instructions, manifests, rule mappings, prompts, and Skill metadata MUST remain English. User-facing responses SHOULD match the user's language when discoverable.

Codex Skill instructions SHOULD remain concise and use progressive disclosure: essential procedures belong in `SKILL.md`, while detailed schemas or lens definitions SHOULD be placed in directly referenced resources when that reduces repeated context without obscuring mandatory behavior.

### 14. Validation and release

The v3 release MUST be rejected unless all applicable checks pass:

- Core rule-catalog and adapter conformance validation.
- Existing v2 regression tests.
- Automatic-routing tests, including explicit user override.
- One-question documented-interrogation tests and pre-consensus implementation blocking.
- Knowledge Base evidence, state, synchronization-summary, and migration tests.
- Twelve-lens coverage, evidence, `not-applicable`, and `unverified` tests.
- Code-review-to-architecture routing tests.
- Diagnostic-only architecture behavior and safe simulated-deletion tests.
- Actual-deletion gate tests that prove refusal when any required condition is absent.
- Architecture Improvement Report schema, state, and no-implementation-authorization tests.
- Conversation-profile claim-limit and Markdown handoff tests.
- Codex official validation for all eight Skills.
- Generic modular and combined-prompt scenario tests.
- Package inventory, reproducible-build, ZIP equivalence, and SHA-256 verification.

Required failures or blocked checks MUST prevent a successful `3.0.0` release evidence record.

## Edge cases and failure behavior

- If the Knowledge Base conflicts with a later approved upstream artifact, treat the approved upstream artifact as authoritative and propose a traceable Knowledge Base modification.
- If two approved artifacts conflict and precedence is unclear, mark the fact unresolved and return to requirement interrogation.
- If a Knowledge Base update summary is missing, approval of the upstream artifact does not authorize an undisclosed Knowledge Base edit.
- If a documented-requirements session ends early, preserve or emit Draft Working Notes without promoting them to formal knowledge.
- If the host cannot persist Draft Working Notes, emit complete Markdown and state that the user owns persistence.
- If a core lens cannot be assessed, mark it `unverified`; do not convert missing evidence into `no-finding`.
- If a core lens genuinely does not apply to the analyzed scope, use `not-applicable` with a scope-specific reason.
- If review detects a systemic issue but architecture diagnosis cannot run, report the limitation and provide a safe handoff.
- If simulated deletion cannot establish dependency impact, report uncertainty rather than recommending actual deletion as proof.
- If an actual deletion experiment lacks authorization, tools, or isolation, do not mutate the workspace and fall back to simulation.
- If an Architecture Improvement Report is accepted, route to Specification; do not route directly to Ticket Plan or implementation.
- If a project-specific lens conflicts with a core lens, the core lens remains mandatory and the additional lens must be distinguished clearly.
- If an automatic route conflicts with explicit user direction, follow the explicit direction unless doing so would violate a safety or approval gate.
- If v2 migration evidence is incomplete, create no unsupported facts and leave missing knowledge unresolved.
- If v3 packaging collides with unmanaged `dist/` content, stop without deleting or overwriting it.

## Data, permissions, and external contracts

The Project Knowledge Base, Draft Working Notes, review evidence, and Architecture Improvement Reports may contain repository structure, business terminology, dependency information, security observations, and unresolved risks. Adapters MUST follow host and project policies for sensitive data, filesystem access, external transmission, and retention.

This Specification authorizes no external upload, publication, marketplace change, personal installation, destructive working-copy operation, or live-system mutation.

The canonical repository path for the Project Knowledge Base is a project contract. Generic Conversation adapters MUST render the same logical structure but cannot claim that the path exists unless the user or a proven tool creates it.

Conformance manifests, rule identifiers, artifact schemas, release manifests, package inventories, and checksums are public technical contracts and MUST remain deterministic and free of credentials or private environment data.

## Compatibility, rollout, and recovery

- Implement Core `3.0.0` first and validate its contracts before adapting Codex or Generic prompts.
- Implement provider adapters only from the approved v3 Core contract.
- Preserve all validated `2.1.0` source release artifacts while producing separate `3.0.0` outputs.
- Keep v3 Specification and Ticket Plan separate from approved v2 artifacts.
- Do not begin v3 implementation until this Specification and its subsequent Ticket Plan are explicitly approved.
- If v3 adapter validation fails, keep the adapter experimental and do not publish successful v3 release evidence.
- If migration fails or is rejected, leave existing v2 artifacts unchanged and continue without an active v3 Knowledge Base.
- Generated v3 release output MAY be discarded and rebuilt; canonical source and approved artifacts remain authoritative.
- Personal installation, if requested later, requires separate explicit authorization after source validation.

## Constraints and assumptions

- Markdown remains the portable format for model-consumed contracts and user-managed artifacts.
- YAML remains the default shared conformance-manifest and rule-catalog format; JSON remains valid for release and Plugin manifests.
- The Knowledge Base is a current-context index with evidence links, not a replacement for approved historical artifacts.
- Draft Working Notes are supporting workflow state, not an additional approval gate.
- Automatic architecture triggers perform diagnosis only and therefore do not broaden authorization to edit code.
- Model quality may vary; conformance validates behavioral instructions and evidence boundaries rather than identical prose or judgment.
- Human-facing design and usage guides may be translated, but canonical Specifications, plans, prompts, manifests, rule catalogs, and Skill instructions remain English.

## Acceptance criteria

- Core `3.0.0` defines Project Knowledge Base, Draft Working Notes, documented requirement interrogation, twelve mandatory lenses, safe deletion analysis, and architecture improvement diagnosis without provider-specific dependencies.
- The canonical Knowledge Base uses the required six sections and the repository path `docs/project/knowledge-base.md`.
- Formal Knowledge Base content is traceable to approved or accepted evidence, and every proposed update discloses additions, modifications, and removals.
- Approving an upstream artifact authorizes only the Knowledge Base changes displayed with that approval request.
- Documented requirement interrogation asks exactly one question per turn, records provisional notes, and blocks implementation before consensus.
- Direct user module selection overrides automatic routing, while automatic documented-mode and architecture triggers announce their reasons.
- Code review evaluates all twelve lenses over the change scope with evidence or justified status.
- Architecture diagnosis evaluates all twelve lenses over the declared architecture scope and includes dependency, impact, and simulated deletion analysis.
- Default deletion analysis performs no file removal or other repository mutation.
- An actual deletion experiment is refused unless explicit authorization, Tools capability, and a disposable isolated environment are all proven.
- Every Architecture Improvement Report contains all ten required sections and one valid state.
- Accepting an Architecture Improvement Report routes work to Specification and never directly authorizes refactoring.
- Every implemented architecture change has an approved Specification, approved vertical Ticket Plan, and TDD evidence.
- First-use v2 migration proposes an evidence-backed Knowledge Base without overwriting any approved v2 artifact.
- Generic Conversation behavior marks unavailable evidence honestly and never claims unperformed repository, testing, persistence, isolation, or deletion actions.
- The Codex Plugin contains the six compatible existing Skills plus `grill-with-docs` and `improve-architecture`, and all eight pass official validation.
- The Generic release contains modular equivalents for both new behaviors and a combined workflow that routes to them.
- Every mandatory v3 rule is mapped by each conforming adapter and enforced by deterministic tests.
- Existing v2 regression behavior remains green.
- Two unchanged v3 builds produce byte-identical distributable archives and matching SHA-256 content.
- No successful `3.0.0` release evidence is created while a required check is failed or blocked.
- No personal installation, marketplace mutation, publication, external upload, or unsupported-provider support claim occurs.

## Deferred decisions

- Dedicated Claude Code, Gemini CLI, or other provider-native adapters.
- Hosted or shared cross-model Knowledge Base persistence.
- A standardized historical revision-log format beyond evidence links and disclosed change summaries.
- Automated execution of actual deletion experiments.
- Release signing and provenance beyond SHA-256 checksums.
- Marketplace publication, installer behavior, and update automation.

## Specification approval gate

This Specification is explicitly Approved and authorizes creation of a separate Draft Ticket Plan. It does not authorize implementation until that Ticket Plan is explicitly approved.
