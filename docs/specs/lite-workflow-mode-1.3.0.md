# Ask Then Do It 1.3.0 Full/Lite Workflow Mode Specification

Artifact type: Specification

Artifact ID: `lite-workflow-mode-1-3-spec`

Workflow ID: `lite-workflow-mode`

Core version: `1.2.0`

Target release version: `1.3.0`

Status: Approved

Inputs: Approved [Ask Then Do It 1.3.0 Full/Lite Workflow Mode Requirement Decision Record](../requirements/lite-workflow-mode-1.3.0.md), active Core `1.2.0`, existing Codex and Generic adapter contracts, current three-language documentation, and current deterministic release configuration.

Assumptions: Token limits are approximate user-visible output budgets because tokenizer behavior varies by model. A tools-capable Codex host can inspect the approved Plugin-owned Config paths within its actual permissions. Generic hosts receive configuration through the composed workflow and remain bound by their proven capabilities.

Deferred: Subagent optimization; exact user-facing prompt prose; exact deterministic token-proxy implementation; external publication, Git tag, GitHub Release, push, upload, and announcement work.

Handoff: `$plan-tickets` after explicit Specification approval.

Approval: The user explicitly replied `核准` on 2026-08-15 after reviewing the complete Specification.

## Problem

The current workflow offers strong traceability through requirements, Specifications, Ticket Plans, per-Ticket implementation evidence, and evidence-based Review. Those contracts are appropriate for consequential work but repeatedly generate and reload substantial workflow text even when a user knowingly wants a faster, lower-assurance path.

Ticket-level `direct` implementation does not solve this problem because it still requires the approved Full Specification and Ticket Plan and deliberately prohibits behavioral test execution. A distinct top-level Lite route is needed to reduce process context while retaining an approved scope, minimal validation, honest risk reporting, and explicit user authority over Review corrections.

## Goals

- Add user-selectable, persistently configurable Full and Lite top-level workflow modes.
- Keep Full backward-compatible and behaviorally unchanged.
- Reduce workflow-controlled token proxy by at least 60% for a representative Lite operation relative to Full.
- Let Lite move from focused clarification through one approved Change Brief to implementation without workflow artifact files.
- Preserve meaningful static and focused behavioral validation without adding tests or using TDD.
- Warn about high-risk work before and during implementation while keeping a switch limited to the current operation.
- Preserve explicit user approval before Review findings are corrected.
- Keep Core, Codex, Generic, three-language documentation, packaging, and release evidence aligned.

## Non-goals

- Replace Full, weaken Full gates, or redefine Full Ticket test choices.
- Treat top-level Lite and Ticket-level `direct` as the same mode.
- Add or modify tests for a Lite operation or claim TDD-equivalent confidence.
- Persist Lite task artifacts or resume Lite task state across sessions.
- Add a separate Lite guide.
- Add subagent orchestration in `1.3.0`.
- Promise a fixed API charge, total context size, hidden reasoning usage, or cache discount.
- Publish the release or mutate external release state.

## Users and scenarios

### User defaults to Lite

A user sets their Plugin-owned user Config to Lite. A normal low-risk operation asks only blocking questions, presents one concise Change Brief, waits for approval, implements without adding tests, performs proportionate validation and compact Review, and returns a concise evidence-honest summary.

### Project requires Full

A user generally defaults to Lite, but one repository has a project Config selecting Full. Operations in that trusted project use Full while other projects continue using the user default.

### One-operation override

A user explicitly requests Full or Lite for one operation. That instruction takes precedence over project and user Config but does not edit either file or change another session.

### High-risk Lite operation

The workflow detects an authentication, payment, migration, destructive, public-contract, concurrent, or external-side-effect risk. It explains the evidence and lets the user switch only this operation to Full or continue Lite with the risk retained.

### Mid-implementation risk discovery

New evidence reveals a material risk after implementation began. The workflow stops further modification and reopens only the current-operation mode choice before continuing.

### Generic user

A user pastes the composed Generic workflow whose header declares a default mode. The AI applies the same semantic Full/Lite behavior within its real conversation or tool capabilities and honors a current-operation override.

## Required behavior

### 1. Mode identities and separation

The workflow MUST expose exactly two top-level modes named `full` and `lite` for this release.

Top-level mode MUST remain distinct from the Full Ticket Plan's internal `tdd` and `direct` implementation modes. Selecting Lite MUST NOT fabricate an Approved Full Specification, Ticket Plan, Ticket mode, or Full evidence artifact. Selecting Full MUST retain its existing per-Ticket test-choice contract.

### 2. Codex mode configuration

Codex MUST recognize Plugin-owned mode configuration at these externally visible paths:

- user default: `~/.codex/ask-then-do-it.toml`;
- project override: `<project>/.codex/ask-then-do-it.toml`.

The `1.3.0` Config contract MUST accept only a top-level mode value with the exact supported meanings `full` and `lite`. Question count, token budgets, validation policy, Review policy, and risk categories MUST remain workflow contracts rather than configurable settings in this release.

For each operation, Codex MUST resolve mode in this order:

1. explicit current-operation user instruction;
2. project Config;
3. user Config;
4. Full fallback.

Missing, unreadable, malformed, missing-mode, or unsupported Config MUST resolve to Full. The workflow MUST NOT reuse a previous session's mode as an undocumented fallback, silently repair Config, or write mode selection during normal routing.

Project Config MUST affect only its project. A current-operation override MUST affect only that operation. Neither MUST mutate user Config.

### 3. Generic mode configuration

The composed Generic entrypoint MUST expose one easily editable declaration at its beginning with the semantic form `Default workflow mode: full` or `Default workflow mode: lite`.

An explicit current-operation instruction MUST override the declaration. A missing or unsupported declaration MUST resolve to Full. The Generic workflow MUST NOT claim to read Codex user or project Config.

Provider-neutral Core and both adapters MUST define equivalent mode outcomes while preserving each host's proven capabilities.

### 4. Full compatibility

Full MUST preserve the current Core `1.2.0` order and gates for reconnaissance, requirement consensus, durable project knowledge when applicable, Requirement Decision Record, Specification, Ticket Planning, plain-language per-Ticket test choices, Approved `tdd` or `direct` implementation, evidence, Review, and architecture diagnosis.

The new mode resolver MAY precede Full orchestration, but it MUST NOT remove Full content, approvals, artifacts, test-choice authority, validation, Review lenses, capability limits, or evidence requirements.

Existing usage without valid Lite Config or an explicit Lite instruction MUST continue through Full.

### 5. Lite reconnaissance and risk evaluation

Lite MUST inspect applicable repository instructions, current changes, and only the code, tests, configuration, documentation, or contracts reasonably related to the requested change. It MUST preserve unrelated user changes.

Before the Change Brief approval, Lite MUST evaluate available evidence for material authentication, authorization, payment, data migration, destructive data operation, public contract, cross-module structural, concurrency, asynchronous, or external-side-effect risk.

When material risk is found, Lite MUST explain the evidence and ask whether the current operation should switch to Full. The user MAY remain in Lite. The choice MUST NOT persist to Config.

If new material risk appears after approval or during implementation, Lite MUST stop further modification and ask the same current-operation question again. A switch to Full MUST preserve observable current changes and return to the earliest unmet Full gate before additional implementation. Continuing Lite MUST retain the accepted risk for the completion report.

### 6. Lite requirement questions

Lite MUST ask only unresolved questions whose answers block or materially redirect implementation. It MUST use repository evidence instead of asking the user for discoverable facts.

Each questioning round MUST:

- contain no more than three questions;
- rank them by impact and uncertainty;
- avoid filler questions when fewer blockers exist;
- target approximately 500 tokens for the complete batch;
- keep each question to at most three short sentences;
- ask one decision per question;
- include one concrete recommendation and its principal consequence or tradeoff.

When more than three blockers exist, Lite MUST ask the highest-priority three and reassess the remaining questions after the answers. It MUST NOT mechanically ask every previously identified question when an answer makes one irrelevant.

### 7. Lite Change Brief and approval gate

After blocking decisions are resolved, Lite MUST display one conversation-only Change Brief containing:

- objective;
- in-scope behavior;
- explicit non-goals;
- three to five observable acceptance scenarios;
- material risks;
- intended validation.

The Change Brief MUST target approximately 800 tokens. Material behavior, risk, failure handling, or validation MUST NOT be omitted to satisfy the target. When an honest brief cannot fit, the workflow MUST recommend Full and ask whether to switch.

Lite MUST have exactly one formal pre-implementation approval gate. It MUST NOT begin production modification before explicit user approval of the complete Change Brief.

For the Lite operation, the workflow MUST NOT create or update a Requirement Decision Record, Draft Working Notes, Project Knowledge Base, Specification, Ticket Plan, Implementation Evidence, Direct Implementation Evidence, Review Report, or Architecture Improvement Report. Requested production code, configuration, content, and documentation files remain valid implementation outputs and are not workflow artifacts.

### 8. Lite implementation boundaries

Lite MUST implement only the approved Change Brief and MUST stop when implementation requires materially new behavior or scope.

Lite MUST NOT create or modify unit, integration, end-to-end, or equivalent behavioral test files for the operation. It MUST NOT require or report Red, Green, Refactor, TDD-complete, or TDD-equivalent evidence.

Lite MUST NOT perform speculative cleanup, unrelated refactoring, or broad generated-output replacement beyond the approved behavior and repository release contracts.

### 9. Lite minimum validation

When relevant and available, Lite MUST:

1. inspect final repository status and diff for unintended files and scope drift;
2. run applicable existing syntax, lint, type-check, build, configuration, schema, or equivalent static validation;
3. execute an existing focused test or perform a manual smoke check for one principal success path;
4. execute an existing focused test or perform a manual smoke check for one most important failure or boundary path;
5. capture the observed outcome needed for the final report.

Lite MUST NOT run a complete behavioral suite by default solely because it exists. An external CI, repository, hosting, or release contract MAY independently require broader checks; Lite MUST disclose and obey real delivery constraints rather than claim to bypass them.

When an applicable check fails because of the implementation or an in-scope environment problem, Lite MUST correct the issue within the approved Change Brief and rerun the relevant check before Review. When a check is unavailable, Lite MUST state the unavailable evidence and risk. A known unresolved applicable failure MUST prevent an unqualified completion claim.

### 10. Lite compact Review

After implementation validation, the implementing AI MUST perform one compact, non-independent Review of:

- Change Brief coverage;
- diff and file scope;
- principal failure and boundary paths;
- security-sensitive behavior and sensitive information;
- observed and unavailable validation;
- residual risk.

Lite Review MUST NOT require a separate reviewer context, the fixed Full twelve-lens pass, or a Review artifact.

All actionable in-scope findings MUST be presented to the user in one batch. The workflow MUST NOT edit a finding before the user explicitly approves the batch. After approval, it MUST fix only the approved findings and rerun relevant validation. A fix requiring material scope expansion MUST return to the user instead of being treated as an in-scope correction.

When the user declines one or more corrections, the workflow MUST leave those items unchanged and report them as unresolved. It MUST NOT claim a clean Review or successful completion that hides their impact.

### 11. Lite completion output

A normal successful Lite completion response MUST target approximately 500 tokens and state:

- delivered behavior;
- changed files or ownership areas;
- observed validation and outcomes;
- unavailable checks;
- unresolved findings;
- residual risks.

It SHOULD omit implementation narration and avoid repeating the complete Change Brief. The token target MUST NOT suppress failures, blockers, security concerns, missing evidence, or unresolved Review findings; those cases MAY exceed 500 tokens.

### 12. Session lifecycle

Lite MUST NOT represent its conversation-only Change Brief, approval, progress, or Review as durable cross-session state.

A new session MUST resolve its mode from the current instruction and Config precedence again. It MAY reconstruct a new Change Brief from repository state and user input, but MUST NOT claim to resume unpersisted Lite workflow state.

### 13. Token-reduction verification

The release MUST include a deterministic comparison between equivalent representative Full and Lite scenarios.

The comparison MUST count workflow-controlled material such as questions, Change Brief or Full artifacts, stage instructions or composed prompt content, repeated workflow handoffs, and completion reporting. It MUST exclude task-specific source code, necessary tool output, and hidden model reasoning that the repository cannot deterministically control.

Lite MUST show at least a 60% reduction in that controlled token proxy. The proxy method and fixture MUST be stable, disclosed in test or release evidence, and applied identically to both modes. Passing the proxy MUST NOT be described as a guaranteed API bill reduction.

### 14. Documentation ownership and localization

Traditional Chinese, English, and Japanese user documentation MUST describe semantically equivalent mode names, precedence, fallback, high-risk switching, budgets, approval, validation, Review, and session behavior.

The root README MUST retain its existing three-language content and general structure except for required release-version updates and the explicitly approved Full/Lite changes. Within each language section:

- usage explanation MUST appear under an Introduction heading;
- the current Installation and updates section MUST be renamed Quick Start;
- the existing Automatic installation (CLI) and nested Codex CLI headings MUST remain;
- Manual installation and Read more MUST remain in their existing relative order;
- Introduction MUST contain only a concise Full/Lite difference and Config-default explanation.

The localized `docs/guides/getting-started-simple.*.md` files MUST be the canonical complete Full/Lite user guides. Each MUST show mode precedence, a comparison table, numbered Full and Lite flows, high-risk switching, Lite budgets, minimum validation, Review correction approval, and completion behavior.

Localized Codex guides MUST own Codex Config paths, precedence, examples, invalid-setting fallback, and one-operation override. Localized Generic guides MUST own the embedded declaration and Generic capability limits. Localized design guides MUST own maintainer architecture, contracts, and the 60% target.

Root, Codex Plugin, and Generic package `START-HERE` files MUST remain concise entry points. They MUST link or direct users to the appropriate complete guide and MUST NOT duplicate the complete Full/Lite flow. No separate Lite-specific guide MUST be added.

### 15. Packaging and release identity

Active Core, adapters, Codex Plugin, Generic manifest and composed workflow, current localized documentation, release configuration, generated package inventories, archive names, checksums, and completed release evidence MUST identify `1.3.0` wherever the current release version is declared.

Generated Codex and Generic outputs MUST preserve their canonical source semantics. Historical `1.2.0` and earlier approved artifacts and published release evidence MUST remain historical and MUST NOT be rewritten merely to remove earlier version references.

## Edge cases and failure behavior

- Conflicting explicit mode words in one operation are unresolved and MUST be clarified rather than selected by order of appearance.
- A project Config outside the active project root MUST NOT be treated as that project's override.
- A project Config selecting Lite and a user Config selecting Full MUST resolve to Lite; the inverse MUST resolve to Full.
- A Config file with an unsupported mode, malformed syntax, or unavailable read MUST fall back to Full and disclose the fallback when it affects the user's expected route.
- An explicit current-operation override MUST work even when Config is invalid, because it has higher precedence.
- If a high-risk prompt receives no mode answer, implementation MUST remain paused.
- If Change Brief approval is absent or ambiguous, Lite implementation MUST not begin.
- If the brief exceeds its target because material risk cannot be expressed concisely, the workflow MUST preserve the information and recommend Full.
- If no meaningful automated or manual behavioral surface exists, Lite MUST report that behavioral evidence is unavailable and rely only on applicable static and diff inspection without claiming behavior was verified.
- If Review finds no actionable issue, Lite MUST say so without manufacturing a correction gate.
- If the user approves only part of a findings batch, only the explicitly approved subset may be fixed.
- If correction reveals material new scope or risk, the workflow MUST stop and return to the appropriate user decision rather than chaining silent fixes.
- If external policy requires a broader suite or Full artifact, the workflow MUST report the real constraint; selecting Lite does not override external enforcement.

## Data, permissions, and external contracts

- The two Config paths, top-level `mode` meaning, mode precedence, Generic declaration, and Full fallback are user-visible contracts.
- Config stores only mode and contains no task content, credentials, approval evidence, or behavioral data.
- Project Config is repository-owned content and may be version-controlled according to user and repository policy. User Config remains machine-local unless the user separately chooses otherwise.
- Reading Config is a non-mutating operation. Normal mode routing MUST NOT write Config.
- Production writes remain governed by host sandbox, approval, and repository permissions; Lite does not broaden them.
- Generic hosts MUST label unavailable persistence, command execution, or Review evidence honestly.

## Compatibility, rollout, and recovery

- `1.3.0` is a backward-compatible feature release. Existing users without the Plugin-owned Config or Generic Lite declaration continue in Full.
- Existing `1.2.0` Full artifacts remain valid historical inputs under their recorded contracts.
- Removing or correcting an invalid Config restores Full fallback without migration of task data.
- A user can recover from an unsuitable Lite selection by switching the current operation to Full; no persistent Config mutation is required.
- A user can recover from an unsuitable Full selection only through an explicit current-operation Lite choice before relying on Lite behavior; existing approved Full artifacts are not deleted.
- Release completion requires aligned Core, adapter, documentation, configuration, conformance, deterministic package, checksum, and token-proxy evidence.

## Constraints and assumptions

- Token budgets are approximate across different model tokenizers and languages; deterministic tests may use a documented proxy but must apply it consistently.
- Full remains the assurance-oriented workflow and Lite is intentionally lower-traceability.
- Lite's lack of durable workflow artifacts is an approved product behavior, not missing evidence that may be silently fabricated later.
- The user remains responsible for choosing whether accepted high risk should remain in Lite.
- Exact implementation modules, helper names, parser choices, and prompt wording are Ticket Planning decisions and are not prescribed by this Specification.
- Canonical source remains authoritative; generated `dist/` output is rebuilt rather than hand-edited.

## Acceptance criteria

1. Given no explicit instruction and no valid Config, a new Codex operation selects Full.
2. Given user Lite, project Full, and no explicit instruction, the operation selects Full; given user Full and project Lite, it selects Lite.
3. Given any valid Config and an explicit current-operation mode, the explicit mode wins without changing either Config file.
4. Given malformed, unreadable, missing-mode, or unsupported Plugin Config, the operation selects Full and does not repair the file.
5. Given a valid Generic default declaration, the Generic route selects that mode; explicit instruction overrides it and invalid declaration falls back to Full.
6. Existing Full scenario, gate, artifact, Ticket test-choice, implementation, Review, and architecture contracts remain conformant.
7. A Lite question round contains at most three blocking decisions, approximately 500 tokens, one recommendation and tradeoff per question, and no repository-answerable question.
8. A Lite Change Brief includes every required section and three to five observable acceptance scenarios within approximately 800 tokens, or preserves material content and recommends Full.
9. Production modification cannot begin until one explicit approval covers the complete Lite Change Brief.
10. A completed Lite operation creates no workflow artifact file and a later session does not claim to resume its unpersisted state.
11. High-risk evidence before approval or during implementation pauses at the approved current-operation mode decision and never changes Config.
12. Lite changes only approved production scope, adds or modifies no test file, and makes no TDD evidence claim.
13. Lite inspects final status/diff, runs applicable existing static checks, and validates a principal success and failure path through existing focused checks or smoke behavior when available.
14. A known unresolved applicable validation failure prevents an unqualified completion claim.
15. Lite performs one compact non-independent Review and does not require a separate reviewer, twelve-lens pass, or Review artifact.
16. Actionable Review findings are shown in one batch and remain unmodified until explicit correction approval; partial approval limits the fix subset.
17. A normal Lite completion report stays near 500 tokens and reports delivered behavior, observed and unavailable validation, unresolved findings, and residual risk.
18. A deterministic representative benchmark shows at least 60% lower workflow-controlled token proxy for Lite than Full without claiming guaranteed billing savings.
19. README changes are limited to approved version, heading movement/rename, concise mode introduction, and preserved Automatic installation (CLI), Codex CLI, Manual installation, Read more structure in all three languages.
20. Localized getting-started guides contain the complete comparison and numbered flows, while START-HERE, Codex, Generic, and design documents stay within their approved responsibilities.
21. Traditional Chinese, English, and Japanese source and packaged documentation express equivalent behavior.
22. Active release identity, canonical and packaged adapters, inventories, deterministic archives, checksums, conformance, and release evidence agree on `1.3.0` while historical releases remain unchanged.

## Deferred decisions

- Subagent-based context isolation or parallel execution for Lite.
- Exact prompt prose and display formatting beyond approved content and budgets.
- Exact tokenizer or token-proxy library and benchmark fixture implementation.
- External publication, Git tag, GitHub Release, push, upload, and announcement.
