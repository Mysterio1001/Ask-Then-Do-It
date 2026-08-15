# Ask Then Do It 1.3.0 Full/Lite Workflow Mode Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `lite-workflow-mode-1-3-plan`

Workflow ID: `lite-workflow-mode`

Core version: `1.2.0`

Target release version: `1.3.0`

Status: Approved

Inputs: Approved [Ask Then Do It 1.3.0 Full/Lite Workflow Mode Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Requirement Decision Record](../requirements/lite-workflow-mode-1.3.0.md), active Core `1.2.0`, current adapter conformance contracts, current localized documentation, and current deterministic release configuration.

Assumptions: This feature is being developed through the existing Full workflow. The user owns every Ticket test choice and there is no default. `Add tests` maps internally to `tdd`; `Do not add tests` maps internally to `direct`. Adding tests while developing Lite does not change the approved runtime Lite rule that future Lite operations add no tests and do not use TDD.

Deferred: Subagent-based Lite optimization; exact user-facing prompt prose; external publication, Git tag, GitHub Release, push, upload, installation, and announcement work.

Handoff: Route Ticket 1 through `$implement-tdd`, then continue in dependency order through each approved Ticket and Review handoff.

Approval: The user selected `Add tests` for Tickets 1-8 and explicitly replied `核准` to the complete mapped Ticket Plan on 2026-08-15. Every Ticket is Approved in `tdd` mode.

## Planned outcome

Deliver a locally complete Ask Then Do It `1.3.0` release with backward-compatible Full behavior and an optional Config-driven Lite workflow. Codex and Generic users receive equivalent mode semantics within their host capabilities, three-language documentation reflects the approved ownership boundaries, a deterministic representative benchmark proves at least 60% lower workflow-controlled token proxy for Lite, and generated packages and release evidence agree.

## Test-time warning and recommendations

Adding tests increases work because each selected Ticket must establish an observable failing check before production changes, reach focused Green, and run broader risk-proportional verification. Skipping tests lowers behavioral regression confidence; only the Ticket's permitted non-test validation and Review remain available.

| Ticket | Outcome | Recommendation | Added work | User test choice |
| --- | --- | --- | --- | --- |
| 1 | Provider-neutral Full/Lite contract | Add tests | Medium | Add tests (selected; internal `tdd`) |
| 2 | Config-driven Codex Lite workflow | Add tests | High | Add tests (selected; internal `tdd`) |
| 3 | Configurable Generic Lite workflow | Add tests | Medium | Add tests (selected; internal `tdd`) |
| 4 | Canonical three-language Full/Lite guides | Add tests | Medium | Add tests (selected; internal `tdd`) |
| 5 | Host guides, short entry points, and bounded README update | Add tests | High | Add tests (selected; internal `tdd`) |
| 6 | Deterministic 60% token-proxy gate | Add tests | High | Add tests (selected; internal `tdd`) |
| 7 | Lockstep `1.3.0` conformance and deterministic packages | Add tests | High | Add tests (selected; internal `tdd`) |
| 8 | Integrated validation and release evidence | Add tests | High | Add tests (selected; internal `tdd`) |

All recommendations are advisory. The user selected tests for all eight Tickets and explicitly approved the complete mapped plan on 2026-08-15.

## Conditional execution policy

- A Ticket with tests added follows its TDD approach, records valid Red before production changes, reaches focused Green, and runs broader verification.
- A Ticket without tests must not create, modify, or execute behavioral tests. Its listed behavioral checks become unavailable evidence; permitted schema, syntax, static, native validator, deterministic build, checksum, link, and final-diff checks remain applicable according to their purpose.
- Both modes preserve scope, dependencies, unrelated user changes, raw evidence, and independent Full Review.
- A later test-choice change returns this plan to `Draft` and requires explicit reapproval before affected implementation continues.

## Delivery strategy

Ticket 1 establishes the minimal shared Core contract. Tickets 2, 3, and 4 can then proceed in parallel with non-overlapping Codex, Generic, and canonical-document ownership. Ticket 5 consumes the settled host behavior and canonical guide structure. Ticket 6 consumes the settled Core and adapter instructions and may run beside Ticket 5. Ticket 7 integrates all behavior, documentation, versions, inventories, and generated output. Ticket 8 performs final combined verification and records only observed release evidence.

## Ticket 1 - Establish the provider-neutral Full/Lite contract

Status: Completed - evidence: [Implementation](../evidence/lite-workflow-mode-1.3.0-ticket-1.md), [initial Review](../evidence/lite-workflow-mode-1.3.0-ticket-1-review.md), and [Review after fixes](../evidence/lite-workflow-mode-1.3.0-ticket-1-review-after-fixes.md).

Execution mode: `tdd` (user selected Add tests).

System recommendation: Add tests. This Ticket changes mandatory routing, approval, validation, Review, and compatibility rules consumed by both adapters. Tests add medium work but protect against silently weakening Full or leaving adapter mappings incomplete.

### Outcome and acceptance coverage

Core defines exactly two top-level modes, preserves the existing Full path, and exposes a complete host-neutral Lite contract without creating a Lite workflow artifact type.

This Ticket covers the shared semantics behind Specification acceptance criteria 1-17 and the Core portions of criteria 20-22.

### Scope and boundaries

In scope:

- Define `full` and `lite` separately from Ticket-level `tdd` and `direct`.
- Define abstract mode precedence, Full fallback, one-operation override, high-risk reconsideration, Lite question and output budgets, one approval, no workflow artifacts, minimum validation, compact Review, correction approval, completion, and session behavior.
- Preserve every existing Full gate, artifact, test-choice, implementation, Review, and architecture rule.
- Add the minimum mandatory Core rules and adapter-manifest obligations needed for deterministic conformance.

Out of scope: Provider-specific Config parsing prose, Codex or Generic prompt wording, user documentation, token fixtures, package generation, and release evidence. No Change Brief artifact template is added.

### Dependencies and ownership

Dependency: Approved Specification and this Plan. No implementation Ticket dependency.

Likely ownership: `core/CORE.md`, `core/modules/orchestration.md`, a focused Lite Core module, `core/rules/rules.yaml`, `core/adapters/manifest-contract.md`, and focused conformance tests or fixtures.

### TDD and direct approaches

TDD: First add focused checks that fail because Lite rules and module coverage are absent and because Full compatibility is not explicitly protected. Add the minimum Core contract and rule catalog to reach Green, then run broader conformance validation.

Direct: Update the Core contract without adding or running behavioral tests. Parse YAML, compare mandatory rule sets, inspect provider neutrality, and manually trace both routes; automated protection against semantic regression remains unavailable.

### Completion and parallel safety

Complete when Core independently describes both routes, Full content is not removed or redirected, no Lite artifact template exists, and every new mandatory rule has an adapter mapping obligation.

Parallel safety: `No`; Tickets 2 and 3 consume this shared contract.

## Ticket 2 - Let Codex resolve Config and execute Lite

Status: Completed - evidence: [Implementation](../evidence/lite-workflow-mode-1.3.0-ticket-2.md), [Independent Review](../evidence/lite-workflow-mode-1.3.0-ticket-2-review.md), [Final Review Corrections](../evidence/lite-workflow-mode-1.3.0-final-review-corrections.md), and [Correction Independent Review](../evidence/lite-workflow-mode-1.3.0-final-review-corrections-review.md).

Execution mode: `tdd` (user selected Add tests).

System recommendation: Add tests. Config precedence and fallback choose the assurance level for an operation, while high-risk pauses and correction approval prevent unauthorized continuation. Tests add high work but materially reduce the chance of selecting the wrong route or bypassing a user gate.

### Outcome and acceptance coverage

Codex resolves explicit operation instructions, project Config, user Config, and Full fallback deterministically, then executes the complete Lite workflow when selected and supported by runtime capabilities.

This Ticket covers Codex acceptance criteria 1-4 and 6-17, plus the Codex portions of criteria 20-22.

### Scope and boundaries

In scope:

- Read only `<project>/.codex/ask-then-do-it.toml` and `~/.codex/ask-then-do-it.toml`; accept only top-level `mode = "full"` or `mode = "lite"`.
- Apply explicit operation instruction > project Config > user Config > Full; clarify conflicting explicit instructions.
- Fall back to Full for missing, unreadable, malformed, missing-mode, or unsupported Config without repairing or writing Config.
- Keep Full routing unchanged and add a bounded Lite Skill or equivalent module for risk checks, questions, Change Brief, approval, implementation, validation, compact Review, correction authority, and completion.
- Preserve capability honesty and avoid packaging a default Config or task-specific Lite artifact.

Out of scope: Editing a user's machine Config, persisting operation overrides, Generic composition, localized guides, release inventory, and generated `dist/` output.

### Dependencies and ownership

Dependency: Ticket 1.

Likely ownership: canonical Codex orchestrator and focused Lite Skill areas under `adapters/codex/plugin/ask-then-do-it/skills/`, Plugin interface metadata if needed, `adapters/codex/conformance.yaml`, `adapters/codex/rule-mapping.yaml`, and focused `tests/codex/` coverage.

### TDD and direct approaches

TDD: Establish Red for the complete precedence matrix, invalid Config cases, conflicting explicit modes, high-risk pauses, no Config writes, one approval, no test/artifact creation, minimum validation disclosure, and Review-finding approval. Implement the smallest coherent Skill and mapping changes, then run focused Codex and conformance suites.

Direct: Use native Skill and Plugin validation, frontmatter/schema inspection, rule-mapping comparison, and manual scenario traces without behavioral tests. Model adherence across all conversations and regression rejection for precedence failures remain unavailable.

### Completion and parallel safety

Complete when every valid and invalid Codex mode source has one deterministic result, Lite covers the approved lifecycle, Full remains reachable and unchanged, and no Config or Lite workflow artifact is included as runtime state.

Parallel safety: `Yes after Ticket 1` with Tickets 3 and 4, provided shared version declarations, `release/release.json`, generated output, and checksums remain untouched until Ticket 7.

## Ticket 3 - Give Generic users an equivalent configurable Lite route

Status: Completed - evidence: [Implementation](../evidence/lite-workflow-mode-1.3.0-ticket-3.md), [Independent Review](../evidence/lite-workflow-mode-1.3.0-ticket-3-review.md), [Final Review Corrections](../evidence/lite-workflow-mode-1.3.0-final-review-corrections.md), and [Correction Independent Review](../evidence/lite-workflow-mode-1.3.0-final-review-corrections-review.md).

Execution mode: `tdd` (user selected Add tests).

System recommendation: Add tests. Generic is conversation-only and the generated workflow is its executable product surface, so composition and scenario checks are the main protection against missing routing or capability overclaims. Tests add medium work.

### Outcome and acceptance coverage

The generated Generic workflow exposes one editable default-mode declaration near its beginning and provides Full/Lite behavior equivalent to Core within conversation-only capabilities.

This Ticket covers acceptance criterion 5, Generic portions of criteria 6-17, and Generic portions of criteria 20-22.

### Scope and boundaries

In scope:

- Generate exactly one semantic declaration `Default workflow mode: full` or `Default workflow mode: lite` near the start of `generic-workflow.md`.
- Let an explicit current-operation instruction override the declaration; use Full for a missing or unsupported declaration.
- Add a focused Generic Lite module and route it from bootstrap/orchestration without claiming Codex Config access.
- Preserve conversation-only boundaries: questions and Change Brief are possible, but file changes, command execution, durable state, observed validation, and independent Review cannot be claimed without supplied evidence and a capable handoff.
- Preserve the complete existing Full modules and stop conditions.

Out of scope: Codex Config, documentation localization, final module inventory/version integration, generated `dist/` editing, and release evidence.

### Dependencies and ownership

Dependency: Ticket 1.

Likely ownership: focused files under `adapters/generic-prompts/`, the Generic composition header in `scripts/build_release.py`, Generic manifest/conformance declarations, and focused `tests/generic/` plus Generic composition coverage.

### TDD and direct approaches

TDD: Establish Red for declaration location and uniqueness, explicit override, invalid fallback, Lite routing, Full preservation, capability limitations, and source-to-generated composition. Add the smallest prompt and composition changes, then run focused Generic and conformance suites.

Direct: Inspect Markdown interfaces, compose an isolated workflow, compare source order and capability statements, and parse manifests without behavioral tests. Continuous regression evidence for generated routing remains unavailable.

### Completion and parallel safety

Complete when a generated Generic workflow contains the editable declaration and complete Lite module, routes deterministically, preserves Full, and makes no unsupported tools or persistence claim.

Parallel safety: `Yes after Ticket 1` with Tickets 2 and 4. Ticket 3 owns only Generic prompt/composition semantics; Ticket 7 owns final inventories, versions, packages, and checksums.

## Ticket 4 - Publish the canonical three-language Full/Lite guides

Status: Completed - evidence: [Implementation](../evidence/lite-workflow-mode-1.3.0-ticket-4.md) and [Final Independent Review](../evidence/lite-workflow-mode-1.3.0-ticket-4-review-final.md).

Execution mode: `tdd` (user selected Add tests).

System recommendation: Add tests. The complete flow, budgets, correction authority, and maintainer contracts must remain semantically equivalent across three languages. Tests add medium work and reduce translation drift and accidental omission.

### Outcome and acceptance coverage

Traditional Chinese, English, and Japanese readers have one canonical complete Full/Lite guide, while maintainers have equivalent design contracts and the disclosed 60% target.

This Ticket covers the canonical-guide and design-document portions of acceptance criteria 18, 20, and 21.

### Scope and boundaries

In scope:

- Update `docs/guides/getting-started-simple.{zh-TW,en,ja}.md` with precedence, comparison table, numbered Full and Lite flows, high-risk switching, 500/800/500 token budgets, minimum validation, Review correction approval, completion, and session behavior.
- Update `docs/design/ai-development-skills.{zh-TW,en,ja}.md` with architecture ownership, adapter equivalence, Lite lower-traceability boundary, and deterministic 60% proxy contract.
- Preserve semantic parity, working links, readable structure, and the role of these files as canonical detail rather than package-local duplication.

Out of scope: Codex Config examples, Generic header instructions, README restructuring, START-HERE content, generated packages, and measured release evidence.

### Dependencies and ownership

Dependency: Ticket 1.

Likely ownership: the six canonical guide/design files and focused documentation contract tests.

### TDD and direct approaches

TDD: Add failing checks for every required section and cross-language semantic marker, including separate Full/Lite approval counts and budgets. Update only the canonical guide/design files, then validate links and documentation scope.

Direct: Use a shared three-language decision checklist, heading/order inspection, and relative-link validation without behavioral tests. Automated semantic-parity and omission detection remain unavailable.

### Completion and parallel safety

Complete when all three languages convey equivalent complete flows and maintainer contracts without turning START-HERE or README into duplicate full guides.

Parallel safety: `Yes after Ticket 1` with Tickets 2 and 3, using a separate documentation-test ownership boundary.

## Ticket 5 - Align host guides, short entry points, and README

Status: Completed - evidence: [Implementation](../evidence/lite-workflow-mode-1.3.0-ticket-5.md), [Final Independent Review](../evidence/lite-workflow-mode-1.3.0-ticket-5-review-final.md), [Package-link Correction](../evidence/lite-workflow-mode-1.3.0-package-link-correction.md), and [Correction Independent Review](../evidence/lite-workflow-mode-1.3.0-package-link-correction-review.md).

Execution mode: `tdd` (user selected Add tests).

System recommendation: Add tests. This Ticket spans host-specific Config claims, nine package/root entry points, a strict README preservation boundary, and three languages. Tests add high work but are the strongest protection against stale instructions or unrelated README churn.

### Outcome and acceptance coverage

Each host-specific guide owns only its approved configuration instructions, every START-HERE stays concise, and README keeps its current content while adopting the approved Introduction and Quick Start structure.

This Ticket covers acceptance criteria 19-21 and the host-documentation portions of criteria 1-5 and 22.

### Scope and boundaries

In scope:

- Update `docs/guides/codex.{zh-TW,en,ja}.md` with both TOML paths, precedence, examples, invalid-setting Full fallback, read-only behavior, and one-operation override.
- Update `docs/guides/generic.{zh-TW,en,ja}.md` with the embedded default declaration, override/fallback behavior, per-session use, and honest Generic capability limits.
- Keep root, Codex Plugin, and Generic package START-HERE files short and direct readers to the appropriate detailed guide without duplicating the full flow.
- Change each README language section only to `Introduction` followed by `Quick Start`, preserving existing Automatic installation (CLI), nested Codex CLI, Manual installation, and Read more order and wording except approved mode text and necessary version references.
- Replace obsolete documentation tests that assume one question and three approvals for every mode with explicit Full/Lite assertions; preserve bounded README-diff checks as structural invariants.

Out of scope: Runtime Skill/prompt behavior, token measurement implementation, generated `dist/` files, checksums, external publication, and unrelated README cleanup.

### Dependencies and ownership

Dependencies: Tickets 2, 3, and 4.

Likely ownership: localized Codex and Generic guides, nine localized START-HERE sources, `README.md`, and focused documentation, command-install, link, and source-equivalence tests.

### TDD and direct approaches

TDD: Establish Red for missing Config/header instructions, START-HERE overreach or missing handoff, README heading order, three-language parity, links, and the approved README change boundary. Apply the smallest documentation updates and run focused documentation suites.

Direct: Compare all languages against one checklist, inspect exact headings and diff boundaries, verify literal Config/header examples, and resolve links without behavioral tests. Automated parity, prohibited-claim, and README-regression evidence remain unavailable.

### Completion and parallel safety

Complete when each document stays within its approved ownership, all locales agree, README structure matches the approved order without unrelated reorganization, and no separate Lite guide exists.

Parallel safety: `No` with Tickets 2-4 while they are active because it consumes their final public contracts. It may run in parallel with Ticket 6 after those dependencies complete.

## Ticket 6 - Enforce the deterministic 60% token-proxy gate

Status: Completed - evidence: [Implementation](../evidence/lite-workflow-mode-1.3.0-ticket-6.md) and [Closure Independent Review](../evidence/lite-workflow-mode-1.3.0-ticket-6-review-closure.md).

Execution mode: `tdd` (user selected Add tests).

System recommendation: Add tests. The 60% result can be accidentally weakened by asymmetric fixtures, unstable counting, or excluded fixed costs. Tests add high work but are required for a repeatable and defensible acceptance claim.

### Outcome and acceptance coverage

A disclosed deterministic benchmark applies one method to equivalent representative Full and Lite operations and rejects Lite when the workflow-controlled token proxy is not at least 60% lower.

This Ticket covers acceptance criterion 18 and provides release input for criteria 17 and 22.

### Scope and boundaries

In scope:

- Use a fixed tools-capable Codex representative scenario as the release gate, with the same normalized proxy function and task facts for both modes.
- Count actual selected stage/Skill instructions, questions, Full artifacts or Lite Change Brief, repeated workflow handoffs, Review/completion outputs, and other workflow-controlled material.
- Exclude task-specific source code, necessary tool output, and hidden reasoning equally; disclose the algorithm, fixture, Full count, Lite count, difference, and percentage.
- Add negative coverage showing that Lite prompt growth below the threshold fails and that exclusions cannot be used asymmetrically.
- Report Generic's composed-prompt fixed cost or limitation separately; do not omit its initial prompt and then claim a Generic 60% guarantee.

Out of scope: API billing prediction, tokenizer-specific guarantees, hidden reasoning measurement, source-code optimization, and subagent optimization.

### Dependencies and ownership

Dependencies: Tickets 1, 2, and 3.

Likely ownership: a focused standard-library measurement script, structured representative fixtures, focused release tests, and benchmark result inputs for final evidence.

### TDD and direct approaches

TDD: First add deterministic count, symmetry, threshold, mutation-failure, and exclusion tests that fail before the proxy exists. Implement the smallest stable proxy and representative fixture, then run focused and relevant release checks.

Direct: Implement and run a disclosed one-off deterministic calculation, inspect fixture symmetry, and verify arithmetic without behavioral tests. Durable protection against fixture gaming, drift, and threshold regression remains unavailable.

### Completion and parallel safety

Complete when the same disclosed method yields at least 60% lower controlled proxy for Lite, failure cases reject invalid comparisons, and no billing guarantee is claimed.

Parallel safety: `Yes after Tickets 1-3`; it may run beside Ticket 5 because ownership does not overlap.

## Ticket 7 - Integrate lockstep 1.3.0 conformance and packages

Status: Completed - evidence: [Implementation](../evidence/lite-workflow-mode-1.3.0-ticket-7.md), [Independent Review](../evidence/lite-workflow-mode-1.3.0-ticket-7-review.md), [Package-link Correction](../evidence/lite-workflow-mode-1.3.0-package-link-correction.md), [Package-link Independent Review](../evidence/lite-workflow-mode-1.3.0-package-link-correction-review.md), [Final Review Corrections](../evidence/lite-workflow-mode-1.3.0-final-review-corrections.md), and [Final Correction Independent Review](../evidence/lite-workflow-mode-1.3.0-final-review-corrections-review.md).

Execution mode: `tdd` (user selected Add tests).

System recommendation: Add tests. This Ticket changes shared versions, runtime inventories, marketplace reference, generated manifests, deterministic archives, and checksums. Tests add high work and are the primary defense against an internally inconsistent release.

### Outcome and acceptance coverage

Every active source and generated release declaration identifies `1.3.0`, both adapters conform to the new Core, deterministic packages include exactly the approved runtime content, and historical `1.2.0` artifacts remain unchanged.

This Ticket covers acceptance criterion 22 and integrates package-facing proof for criteria 1-21.

### Scope and boundaries

In scope:

- Move active Core, adapter, Plugin, marketplace, release, current documentation, test, package, archive, and checksum identities to `1.3.0` without blind replacement of historical artifacts.
- Update `release/release.json` inventories for any added Codex Skill or Generic module and require the workflow token-proxy check.
- Preserve Generic header composition semantics from Ticket 3 and all canonical source-to-package ownership boundaries.
- Rebuild `dist/` through the release builder; verify exact inventories, atomic replacement, reproducibility, ZIP equivalence, and SHA-256 values.
- Update current-release tests explicitly rather than rewriting historical evidence or old approved workflow artifacts.

Out of scope: New behavior beyond Tickets 1-6, external Git/tag/release state, installation, publication, and final completed evidence claims.

### Dependencies and ownership

Dependencies: Tickets 1-6 completed through their required Reviews.

Likely ownership: active version declarations, `.agents/plugins/marketplace.json`, Plugin and adapter manifests, `release/release.json`, release builder integration, current-release and package tests, generated `dist/`, and checksums.

### TDD and direct approaches

TDD: Establish Red for `1.3.0` identity, new runtime inventories, required proxy gate, package boundaries, reproducibility, and historical preservation. Apply the smallest lockstep source/config updates, rebuild atomically, reach focused Green, then run broader release/conformance suites.

Direct: Update active declarations and inventories, run native/schema validation, deterministic builds, inventory comparison, ZIP equivalence, checksum recalculation, and historical-diff inspection without behavioral tests. Automated rejection evidence for version and packaging drift remains unavailable.

### Completion and parallel safety

Complete when all current declarations and generated outputs agree on `1.3.0`, packages are reproducible and minimal, checksums match, and historical `1.2.0` evidence is untouched.

Parallel safety: `No`; it integrates shared versions, inventories, builder behavior, generated output, and checksums.

## Ticket 8 - Complete integrated validation and release evidence

Status: Completed - evidence: [Implementation](../evidence/lite-workflow-mode-1.3.0-ticket-8.md), [User-document footer independent Review](../evidence/ask-then-do-it-1.3.0-user-document-footer-independent-review.md), and [Final evidence-only closure](../evidence/ask-then-do-it-1.3.0-evidence-closure-after-footer.md).

Execution mode: `tdd` (user selected Add tests).

System recommendation: Add tests. Completed release evidence must reject a missing or failed token-proxy result and must not hide any failed required check. Tests add high work because this Ticket exercises the full validation matrix.

### Outcome and acceptance coverage

The local `1.3.0` release has evidence derived from observed results, no unresolved blocking Review finding, a release-milestone architecture diagnosis, and no claim of external publication.

This Ticket provides final proof for acceptance criteria 1-22.

### Scope and boundaries

In scope:

- Run focused suites, combined automated discovery selected by approved modes, Codex and Generic conformance, canonical and packaged Plugin/Skill validation, documentation/link checks, token proxy, two-build reproducibility, inventories, ZIP equivalence, and checksums.
- Prove the evidence gate rejects a missing or failed workflow-token-proxy check.
- Perform independent Full Review and the required read-only release-milestone architecture diagnosis; return source defects to their owning Ticket rather than silently fixing them here.
- Create the `1.3.0` validation ledger and release evidence only from actual observations and mark completion only after every required check is accepted.

Out of scope: New product behavior, unplanned architecture refactoring, Git tag, push, GitHub Release, upload, installation, and announcement.

### Dependencies and ownership

Dependencies: Ticket 7 and all earlier Ticket implementation/Review handoffs.

Likely ownership: `1.3.0` validation ledger, local release evidence, release architecture diagnosis, final Review artifacts, and narrowly required evidence-gate tests.

### TDD and direct approaches

TDD: Add or update a focused evidence-gate rejection case for absent/failed proxy evidence, record Red, reach Green, then run the complete selected regression and mandatory validation matrix before writing evidence.

Direct: Do not create, modify, or execute behavioral tests. Run every permitted native/static/build/checksum/link/diff validation, disclose behavioral suites as `skipped-by-user`, and create no completed evidence unless the release gate accepts that reduced-evidence state.

### Completion and parallel safety

Complete when all required observed checks and evidence agree, Review has no unresolved blocker, architecture diagnosis authorizes no implementation, and external work remains explicitly deferred.

Parallel safety: `No`; it consumes the final integrated repository and all prior evidence.

## Dependency order and parallel groups

1. Sequential foundation: Ticket 1.
2. Parallel-safe group after Ticket 1: Tickets 2, 3, and 4 with explicit non-overlapping ownership.
3. After Tickets 2-4: Tickets 5 and 6 may run in parallel.
4. Sequential integration: Ticket 7 after Tickets 1-6 and their required Reviews.
5. Sequential completion: Ticket 8 after Ticket 7 and all required handoffs.

All eight test choices are resolved as Add tests and mapped to `tdd`. Ticket 1 is the first eligible implementation Ticket.
