# Ask Then Do It 1.3.0 Full/Lite Workflow Mode Requirement Decision Record

Artifact type: Requirement Decision Record

Artifact ID: `lite-workflow-mode-1-3-requirements`

Workflow ID: `lite-workflow-mode`

Core version: `1.2.0`

Target release version: `1.3.0`

Status: Approved

Inputs: User feedback that the current workflow may consume too many tokens; repository evidence from the existing Full requirements, Specification, Ticket Planning, TDD/direct implementation, Review, localization, packaging, and release contracts; OpenAI official Codex configuration documentation; and the user's decisions confirmed in conversation on 2026-08-14 and 2026-08-15.

Assumptions: Token counts vary by model and tokenizer, so all conversational token limits are approximate output budgets. Codex sessions with repository tools can read the approved Plugin-owned user and project configuration paths. Generic hosts cannot be assumed to read Codex files and instead receive their default mode from the composed workflow text.

Deferred: Subagent-based optimization; exact prompt prose; the deterministic token-proxy implementation used by release tests; external publication, Git tag, GitHub Release, upload, and announcement work.

Handoff: `$write-spec` after approval.

Approval: The user explicitly replied `核准` on 2026-08-15 after reviewing the complete Requirement Decision Record, including the Full/Lite behavior, Config precedence, validation, Review, documentation, compatibility, and token-reduction decisions.

## Problem and desired outcome

The existing Full workflow deliberately preserves requirements, Specifications, Ticket Plans, implementation evidence, Review evidence, and approval gates. Historical repository examples show that these artifacts and their repeated handoffs can dominate workflow-controlled context before source code, tool output, or model reasoning is counted.

Users need an optional Lite workflow that spends materially fewer tokens on process while retaining an explicit scope, one approval, proportionate validation, honest risk disclosure, and user control over corrections. The existing Full workflow must remain available and unchanged for users who prefer its traceability and assurance.

## Users and success signals

### Workflow user

- Can choose a persistent Full or Lite default without repeating that choice in every session.
- Can override the default for one operation without changing future sessions.
- Sees no more than three sharp blocking questions per Lite round and receives a concise Change Brief before implementation.
- Is warned when a Lite operation appears high-risk and decides whether only that operation should switch to Full.
- Retains authority over fixes discovered during Lite Review.

### Maintainer

- Can preserve the existing Full contracts while adding a separately identifiable Lite route.
- Can verify deterministic mode precedence, fallback, prompt budgets, validation disclosures, localized documentation, and package parity.
- Can demonstrate at least a 60% reduction in workflow-controlled token proxy for a representative Lite scenario compared with the equivalent Full scenario.

## Scope

- Add top-level workflow modes `full` and `lite` to provider-neutral Core, Codex Plugin, and Generic workflow behavior.
- Keep Full as the backward-compatible fallback and preserve every existing Full gate, artifact, test-choice, implementation, Review, and architecture contract.
- Add Plugin-owned user and project configuration files for Codex mode defaults.
- Add one embedded Generic default-mode declaration to the composed `generic-workflow.md`.
- Allow an explicit user instruction to override the configured mode for one operation only.
- Define Lite requirement questioning, Change Brief, approval, implementation, validation, Review, correction authorization, and final-report behavior.
- Add high-risk detection before and during Lite implementation without forcing a permanent Config change.
- Update Traditional Chinese, English, and Japanese source and packaged documentation according to the approved document ownership boundaries.
- Add deterministic behavioral, conformance, documentation, configuration, package, and token-proxy validation for release `1.3.0`.

## Non-goals

- Remove, shorten, weaken, or silently redirect the existing Full workflow.
- Use the existing Ticket-level `direct` mode as the top-level Lite mode.
- Add tests, require Red/Green/Refactor, or create Full workflow artifacts during a Lite operation.
- Preserve Lite task state across sessions.
- Add a dedicated Lite documentation file.
- Make the approved question, Change Brief, or final-summary budgets user-configurable in the first release.
- Add subagent orchestration to Lite `1.3.0`.
- Guarantee a specific API bill, hidden reasoning-token count, prompt-cache discount, or source-code context size.

## Primary behavior and user flow

### Mode resolution

The workflow resolves one top-level mode for each operation in this order:

1. An explicit Full or Lite instruction for the current operation.
2. Project configuration at `<project>/.codex/ask-then-do-it.toml`.
3. User configuration at `~/.codex/ask-then-do-it.toml`.
4. Full fallback.

Codex configuration accepts only `mode = "full"` or `mode = "lite"`. A missing file, unreadable file, malformed file, missing mode, or unsupported value resolves to Full. A one-operation selection never writes either Config file.

The Generic composed workflow carries one declaration with the meaning `Default workflow mode: full` or `Default workflow mode: lite`. An explicit user instruction overrides it for the current conversation operation. A missing or invalid declaration resolves to Full.

### Full mode

Full remains the current workflow: repository reconnaissance, requirement consensus, Requirement Decision Record, Specification, Ticket Plan, per-Ticket test choices, approved TDD or direct implementation, evidence, Review, and architecture diagnosis when its existing route applies.

Full mode is not equivalent to requiring TDD for every Ticket. Its existing user-owned Ticket test choices and `tdd`/`direct` routing remain unchanged.

### Lite requirement clarification

- Ask only questions that block or materially redirect implementation.
- Rank unresolved questions by impact and uncertainty.
- Ask no more than three questions in one round and do not invent questions to fill the limit.
- Keep the complete question batch to approximately 500 tokens.
- Keep each question to at most three short sentences containing one decision, a concrete AI recommendation, and the principal consequence or tradeoff.
- Do not ask the user for facts already answerable from repository evidence.
- When more than three blockers exist, ask the highest-priority three, then reassess whether the rest remain necessary after the answers.

### Lite Change Brief and approval

After blocking decisions are resolved, display one Change Brief in the conversation. It must contain the objective, in-scope behavior, explicit non-goals, three to five observable acceptance scenarios, material risks, and intended validation.

The Change Brief has an approximate 800-token budget. The workflow must not omit material behavior, risk, or validation merely to fit. If the work cannot be represented honestly within the budget, it must recommend Full and ask whether to switch.

Lite has one formal approval gate. Implementation begins only after the user explicitly approves the complete Change Brief. Lite does not create or persist a Requirement Decision Record, Draft Working Notes, Project Knowledge Base change, Specification, Ticket Plan, Implementation Evidence, Direct Implementation Evidence, Review Report, or Architecture Improvement Report for that operation.

### High-risk mode reconsideration

Before approving the Change Brief, Lite evaluates available evidence for high-risk behavior such as authentication or authorization, payments, data migration, destructive data operations, public contracts, cross-module structural change, concurrency, asynchronous behavior, or external side effects.

When material risk is present, the workflow explains it and asks whether only the current operation should switch to Full. The user may remain in Lite after the warning. Neither choice changes Config.

If new high-risk evidence appears after approval or during implementation, the workflow pauses further modification, reports the evidence, and asks the same one-operation mode question again. A switch to Full preserves observable current changes but returns to the earliest unmet Full gate before further implementation. Continuing Lite retains and later reports the accepted risk.

### Lite implementation and validation

- Implement only the approved Change Brief and preserve unrelated user changes.
- Do not create or modify test files for the Lite change and do not require Red, Green, or Refactor evidence.
- Inspect `git status` and the final diff for unintended files and scope drift.
- Run applicable existing syntax, lint, type-check, build, configuration, schema, or equivalent static checks when available.
- Use an existing focused test or a manual smoke check to validate one principal success path and one most important failure or boundary path when a meaningful executable surface is available.
- Do not run the complete behavioral suite by default merely because Lite was selected.
- Correct implementation or environment problems within the approved Change Brief and rerun the relevant validation before Review.
- Do not claim completion while an applicable required validation has a known unresolved failure. Report an unavailable check and its risk when the environment cannot execute it.

### Lite Review and correction authority

The implementing AI performs one compact, non-independent Review. It checks Change Brief coverage, diff scope, principal failure paths, security-sensitive behavior, sensitive information, and observed validation. It does not require a fresh reviewer, the fixed twelve Architecture and Refactoring Lenses, or a separate artifact.

The AI must collect all actionable in-scope Review findings and present them in one batch. It may not fix those findings until the user explicitly approves the batch. After approval it fixes only the approved findings and reruns relevant validation. If a proposed fix exceeds the Change Brief, it must stop and request a revised scope. If the user declines correction, the workflow leaves the change as-is and reports the unresolved findings and risks without claiming clean completion.

### Lite completion report

A normal completed Lite report has an approximate 500-token budget and includes delivered behavior, changed scope, observed validation, unavailable checks, unresolved findings, and residual risks. It does not repeat the full Change Brief or narrate the implementation process.

Failures, blockers, unresolved Review findings, and security risks may exceed 500 tokens and must never be hidden to satisfy the budget.

## Configuration data and lifecycle

- The Codex user Config is `~/.codex/ask-then-do-it.toml`.
- The Codex project Config is `<project>/.codex/ask-then-do-it.toml`.
- Project Config overrides user Config only for that project.
- A current-operation instruction overrides both without persisting.
- The initial Config schema stores only the top-level mode.
- Mode Config contains no credentials, personal task content, Change Brief, approval state, or cross-session progress.
- Lite conversation state ends with the session. A later session reads Config again but must reconstruct the task and Change Brief.

## Failures, security, privacy, and operations

- Invalid or unavailable Config fails safely to Full and must not be guessed from prior sessions.
- External CI, repository policy, host permissions, or release systems may still require checks that Lite cannot bypass.
- Lite must not transmit repository data or credentials to an external system merely to satisfy smoke validation.
- A known failing required check, unapproved Review finding, or newly discovered scope expansion prevents an unqualified completion claim.
- A Generic conversation-only host may provide guidance and Review only to the extent its real capabilities permit. It must not claim file edits, command execution, persistence, or observed validation without evidence.
- Full and Lite mode names are user-visible workflow choices. Ticket `tdd` and `direct` values remain distinct internal Full planning routes.

## Documentation configuration

### README boundary

The root README remains based on its current content and three-language organization. Apart from required release-version updates and explicitly approved Full/Lite content, its structure and links are not generally redesigned.

Within each language section:

- the current usage explanation moves under an Introduction heading;
- the current Installation and updates heading becomes Quick Start;
- the existing Automatic installation (CLI) heading and nested Codex CLI heading remain;
- Manual installation remains;
- Read more remains after Quick Start;
- Introduction receives only a concise Full/Lite distinction and Config-default explanation.

### Guide ownership

- `docs/guides/getting-started-simple.zh-TW.md`, `.en.md`, and `.ja.md` are the canonical user-facing Full/Lite flow explanations.
- Each getting-started guide presents mode precedence, a comparison table, numbered Full and Lite flows, high-risk switching, Lite budgets, validation, Review, and completion behavior.
- Codex guides own Codex installation and Config paths, precedence, examples, and one-operation overrides.
- Generic guides own composed-workflow mode configuration and Generic capability limits.
- Design guides own maintainer-facing architecture, validation contracts, and the 60% token-reduction target.
- Root, Codex Plugin, and Generic package `START-HERE` files remain short entry points and do not duplicate the complete Full/Lite flow.
- No new Lite-specific guide is added.
- Traditional Chinese, English, and Japanese documentation must remain semantically equivalent.

## Acceptance criteria

1. A Codex operation resolves explicit instruction, project Config, user Config, and Full fallback in the approved order.
2. Missing, unreadable, malformed, missing-mode, or unsupported Config resolves to Full without persisting a guessed correction.
3. Generic mode declaration, explicit override, and Full fallback produce the same semantic mode outcomes as Codex within Generic capability limits.
4. Full conformance and existing Full scenario behavior remain unchanged apart from recognizing and routing the new top-level mode.
5. Lite asks no more than three blocking questions per round, stays within the approximate 500-token batch target, and does not ask repository-answerable questions.
6. Lite presents a complete Change Brief within the approximate 800-token target or recommends Full rather than omitting material information.
7. Lite cannot implement before its one explicit Change Brief approval and creates no workflow artifact files.
8. High-risk evidence before or during implementation triggers the approved one-operation reconsideration without changing Config.
9. Lite does not create or modify tests and does not require TDD evidence, while still performing the approved static and focused success/failure validation where available.
10. A known unresolved applicable validation failure prevents a successful completion claim.
11. Lite performs one compact Review without an independent reviewer or mandatory twelve-lens pass.
12. Review findings require one explicit batch correction approval before edits, and scope-expanding fixes return to the user.
13. A normal final report targets 500 tokens while always preserving failures, blockers, unavailable evidence, and security risk.
14. A later session uses Config but does not claim to recover unpersisted Lite task state.
15. A representative deterministic benchmark shows at least 60% lower workflow-controlled token proxy for Lite than equivalent Full, excluding source code, necessary tool output, and hidden model reasoning.
16. README changes stay inside the approved heading/content/version boundary.
17. Three-language getting-started, Codex, Generic, design, root start, and packaged start documentation satisfy their approved ownership and semantic-parity contracts.
18. Canonical and packaged Codex and Generic outputs agree on `1.3.0`, mode behavior, inventories, checksums, and deterministic release evidence.

## Confirmed decisions

All mode semantics, Config paths and precedence, budgets, one approval, no-artifact rule, non-TDD validation, high-risk reconsideration, Review correction authorization, documentation ownership, cross-adapter behavior, 60% target, and release `1.3.0` were explicitly approved by the user on 2026-08-14 and 2026-08-15.

## Explicit consensus evidence

The complete Draft Requirement Decision Record was presented in the conversation on 2026-08-15. The user explicitly replied `核准`, approving the complete requirement and authorizing Specification drafting.
