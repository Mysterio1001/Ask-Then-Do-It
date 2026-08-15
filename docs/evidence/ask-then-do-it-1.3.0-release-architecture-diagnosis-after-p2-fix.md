# Ask Then Do It 1.3.0 Release Architecture Diagnosis After P2 Fix

artifact_type: Architecture Improvement Report

artifact_id: `ask-then-do-it-1-3-release-architecture-after-p2-fix`

workflow_id: `lite-workflow-mode`

core_version: `1.1.0`

status: `draft`

inputs: Approved [1.3.0 Specification](../specs/lite-workflow-mode-1.3.0.md) and [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md); prior Draft [release architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis.md), [after-fix diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-fix.md), and [after-Review-fixes diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-review-fixes.md); [direct-entry correction Review after P2](lite-workflow-mode-1.3.0-direct-entry-correction-review-after-p2.md); current Core, Codex, Generic, tests, documentation, release configuration, builder, validators, token-proxy fixture, expanded `dist/`, ZIPs, and checksums; current pending ledger and release evidence; and current Final Review/correction evidence.

assumptions: Canonical source is authoritative and `dist/` is generated output. The current working tree is the post-approved P1/P2 correction candidate. The approved Generic bounded guard is a host-specific projection for independently pasted stages; complete resolver ownership remains in `bootstrap.md` and `orchestration.md`. The six tag-pinned guide URLs are intended to resolve after separately authorized `v1.3.0` publication.

deferred: Any refactor or actual deletion experiment; acceptance or implementation of F2-F4; live installed-Plugin dispatch; live third-party Generic model adherence; remote URL dereference; external CI and other operating systems; installation; Git tag, GitHub Release, push, upload, publication, and announcement.

handoff: No current release correctness blocker was found in the inspected source, tests, documentation, release configuration, expanded packages, ZIPs, or checksums. P1 (Codex discovery) and P2 (Generic editable-default/guard ownership) are structurally closed, and prior package-link F1 remains locally closed. Return the candidate to Ticket 8 for fresh release-evidence/ledger refresh and the separately required Final Independent Review. F2-F4 remain unaccepted, nonblocking Draft proposals and authorize no implementation.

approval: None. This is a diagnostic-only `draft`; acceptance would authorize only a return to Specification for an explicitly accepted proposal.

## 1. Analysis scope and limitations

Capability: `multi_agent`. This context had repository `tools` capability and participated in the active multi-agent task. The diagnosis itself used read-only inspection and serial checks; no independent child context was available in this pass.

The boundary is the Ask Then Do It `1.3.0` release path from provider-neutral Core mode resolution through Codex discovery and Generic direct-entry routing, localized ownership, deterministic Generic composition, package expansion, ZIP construction, checksums, and release-evidence validation. The specific closure questions were:

- whether the approved Codex direct-entry/discovery correction remains reachable for all public software-changing operations;
- whether Generic keeps one complete resolver owner while its nine standalone projections remain bounded and equivalent;
- whether source, tests, docs, generated output, ZIPs, and checksums remain aligned after P2; and
- whether any current release correctness blocker remains after excluding the already closed P1, P2, and F1 findings.

Evidence limitations:

- The worktree is cumulative and uncommitted; ownership was reconstructed from the Approved Plan and raw files, not commit boundaries.
- Focused suites, conformance CLIs, marketplace validation, token proxy, output validation, and direct byte/hash checks were run. The complete discovery suite was not rerun by this architecture context.
- Live Codex Skill discovery, live Config unreadability behavior, live Generic model adherence, remote guide availability, installation, external CI, and publication were not observed.
- `docs/evidence/ask-then-do-it-1.3.0-release-architecture-diagnosis-after-direct-entry-fix.md` was not present; the available prior after-fix and after-Review-fixes reports were read instead.
- The existing validation ledger and release evidence are still `Review Pending` and contain older archive/proxy values than the current `dist/`; refreshing those artifacts belongs to Ticket 8 and is not treated as a source architecture finding here.
- No file, directory, ZIP entry, configuration value, or authoritative data was removed, renamed, moved, or rewritten. All deletion analysis below is simulated (`ARCH-DELETE-001`).

## 2. System architecture summary

Core `1.3.0` is the normative host-neutral contract in `core/CORE.md`, `core/modules/orchestration.md`, `core/modules/lite-workflow.md`, `core/adapters/manifest-contract.md`, and `core/rules/rules.yaml`. `MODE-RESOLVE-001` requires one `full` or `lite` result for every public entry. Core permits a bounded direct-entry guard only when a standalone stage cannot load another module; that guard is explicitly not complete resolver ownership.

Codex exposes the orchestrator Skill as the implicit discovery boundary. Its frontmatter now covers every software-changing operation, including trivial, fully specified, formatting-only, and single-line requests, and its body resolves explicit instruction, project Config, user Config, and Full fallback before routing. Eight stage Skills carry a pre-stage guard that delegates unresolved mode to the canonical resolver and continues only with proven Full. The Lite reference owns the Lite lifecycle.

Generic is conversation-only. `bootstrap.md` and `orchestration.md` own complete mode resolution. The other nine modules, including `lite-workflow.md`, are independently pasteable and carry the approved bounded direct-entry matrix; a proven composed mode is reused without re-resolution. `scripts/build_release.py::compose_generic_workflow` emits one qualified editable declaration, the routing header, and the configured eleven modules in stable order.

`release/release.json` coordinates active identity, source inventories, package paths, required checks, and managed outputs. The builder validates source and manifests, composes Generic, expands exactly 27 Codex and 18 Generic runtime files, writes reproducible ZIPs, verifies directory/ZIP equivalence, and writes checksums. The token proxy imports the same composer so benchmark semantics cannot silently diverge from the package entrypoint. The evidence validator checks the configured ledger shape and statuses, while command execution remains outside that validator.

```text
Core mode contract
  -> Codex discovery -> canonical resolver -> Full or Lite
  -> Generic composer header -> resolver owners -> bounded standalone guards

source + release.json
  -> builder validation/composition
  -> expanded Codex (27) + Generic (18)
  -> reproducible ZIPs -> checksums.sha256
```

## 3. Deletion-analysis results

Actual deletion gates were not satisfied: there was no explicit authorization for destructive mutation and no disposable isolated copy. The following are safe simulations only.

| Simulated removal | Inbound callers, tests, docs, and configuration | Outbound, package, and release effect | Result |
| --- | --- | --- | --- |
| Core bounded-guard contract in `core/modules/orchestration.md` (the direct-entry bullets) | Linked from `core/CORE.md`; mapped by `core/adapters/manifest-contract.md`; represented by `MODE-RESOLVE-001` in `core/rules/rules.yaml`; asserted by `tests/conformance/test_lite_core_contract.py` and adapter mapping tests. | Adapters could still contain copied guards, but the normative delegation-versus-bounded boundary would disappear. Conformance and contract tests should fail; Generic direct-entry behavior would become unanchored. | Release assurance fails closed; no runtime deletion performed. |
| Generic resolver owners `adapters/generic-prompts/bootstrap.md` and `orchestration.md` | Listed in `release/release.json` and the token-proxy fixture; composed first by `compose_generic_workflow`; referenced by all three Generic guides and `tests/generic/test_generic_lite_workflow.py`. | The generated workflow loses complete mode resolution, Full/Lite routing, and first-gate selection. Nine guards would not have an owner; Generic conformance, composition, documentation, and token-proxy checks fail, and the package cannot honestly claim the configured route. | Consumer behavior breaks and the builder/release gates block output. |
| One representative Generic bounded guard, `adapters/generic-prompts/requirements.md` | Included in the eleven-module inventory, copied into `prompts/`, composed into `generic-workflow.md`, and checked by the all-public-module direct-entry matrix in `tests/generic/test_generic_lite_workflow.py`. | Directly pasted requirements entry could run Full behavior without establishing or reusing a proven mode. The clean source inventory, Generic package inventory, ZIP equivalence, and direct-entry matrix fail; existing ZIPs remain stale until rebuilt. | A bounded public-entry contract is lost; release must fail closed. |
| `compose_generic_workflow` in `scripts/build_release.py` | Called by `build_generic`, release package tests, Generic Lite tests, workflow-token-proxy measurement, and source-to-generated comparisons. | No canonical `generic-workflow.md` can be generated; the Generic package build and its ZIP/checksum fail. The token proxy also fails at import/call time, coupling packaging and benchmark availability as documented by F4. | Both deliverable composition and Generic measurement disappear. |
| One package START-HERE URL or one expanded/ZIP entry | Source and package documentation matrices, clean-build release contract, ZIP byte audit, and checksum validation inspect all six host/locale entries. | The former F1 package-context navigation defect returns, or source/expanded/ZIP parity breaks. Remote target existence remains a publication responsibility. | Focused release gates reject the candidate; no current defect observed. |
| `release/release.json` | Read by builder, token proxy, evidence validator, package tests, and release safety checks. | Version, inventories, archive names, mandatory proxy gate, and managed-output boundaries disappear; no trustworthy package or evidence validation can run. | Wide but explicit coordination failure. |
| `dist/` or either ZIP/checksum record | Release tests inspect exact inventories, ZIP entries/bytes, and SHA-256. Canonical source remains available. | Generated output is recoverable through a clean builder run, but no release can be claimed until regeneration and all parity checks pass. | Recoverable generated-output loss. |

## 4. Twelve-lens results

| Lens | Outcome | Evidence and classification |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `finding` | F2 remains: mode precedence, risk categories, budgets, approvals, validation, Review, session behavior, and ownership markers are projected manually across Core, Codex, Generic, three locales, fixtures, and literal tests. The nine Generic guards are an approved bounded projection and P2 is closed; this is maintainability evidence, not a new release blocker. |
| 2. Long Function | `no-finding` | The inspected builder, composer, proxy, and evidence-validator routines are linear pipelines. No current release defect was attributable to a single function's length. |
| 3. Large Module or Class | `finding` | F4 remains: `scripts/build_release.py` is a large module owning schema/source validation, marketplace/assets, Generic composition, inventories, ZIPs, checksums, and filesystem transaction behavior. Current outputs are correct. |
| 4. Long Parameter List | `no-finding` | Public functions accept cohesive config/path inputs and small keyword options; `compose_generic_workflow(config, source)` remains a two-input interface. |
| 5. Data Clumps | `no-finding` | Mode sources, proxy events, package inventories, and host/locale URL pairs are explicit records or configuration collections. No new loose argument bundle crosses an interface. |
| 6. Primitive Obsession | `finding` | F3 remains: release-check IDs, statuses, commands, and outcomes are primitive self-declared strings. The validator does not bind an executor, exit status, result artifact/digest, or package digest. |
| 7. Feature Envy | `no-finding` | The token proxy delegates Generic composition to the owning builder; package tests inspect their owned output; adapters operate on their own surfaces. No current correction reaches through an unrelated unit's internals. |
| 8. Divergent Change | `finding` | F2/F4 remain: workflow policy projections change for many reasons, while the builder changes for validation, composition, archive, checksum, and transaction concerns. No additional correction defect was found. |
| 9. Shotgun Surgery | `finding` | A mode or direct-entry policy change still requires coordinated Core, adapter, localized-guide, fixture, test, package, ZIP, checksum, and evidence updates. Deterministic packaging contains current drift but does not remove the edit fan-out. This is F2, not a new blocker. |
| 10. Message Chains | `not-applicable` | The scoped implementation is declarative Markdown/YAML/JSON plus direct filesystem, ZIP, and hash calls; there is no meaningful object-navigation chain to assess. |
| 11. Leaky Abstraction | `finding` | P1 discovery/resolver and P2 ownership/banner leaks are closed. F3 remains a release-assurance boundary leak because ledger producers supply execution claims to a validator that only checks declaration shape and status. |
| 12. Shallow Module | `finding` | F3 remains: the evidence validator presents a completion gate but encapsulates only structural/status checks, leaving execution provenance outside its interface. Resolver owners and bounded Generic stages are not shallow under the approved contract. |

## 5. Finding evidence, impact, and confidence

### Current release correctness blocker verdict

No current release correctness blocker was found in the source-to-package architecture. The raw current Codex Skill frontmatter and direct-stage guards cover the prior P1 dispatch boundary; the Generic composer banner is explicitly editable only for the declaration; the nine Generic guards distinguish bounded projection from complete ownership; and the earlier package-link F1 remains replaced by exact `v1.3.0` host/guide URLs. Focused tests, conformance, package validation, ZIP parity, and current checksums support those closure conclusions. These statements do not duplicate or reopen P1/P2/F1.

The local release is still not complete: `docs/evidence/ask-then-do-it-release-1.3.0.md` is `Review Pending`, and its ledger records older archive/proxy values than the current `dist/`. That is a required Ticket 8 evidence refresh and fresh Review handoff, not an architecture defect in the current source.

### F2 - Shared workflow and localized policy projection

Status: `open, unaccepted, nonblocking Draft proposal`
Impact: Medium maintainability
Confidence: High

The same mode sources, precedence, conflict/fallback rules, risk list, 500/800/500 budgets, approval gates, validation paths, correction authority, and session behavior appear in `core/modules/*`, the Codex Skill/reference, all eleven Generic modules, three complete guides, host entry pages, fixtures, and tests. Current tests catch the observed P1/P2 drift, but a future semantic change still requires many manual edits. No current release correctness failure is established.

### F3 - Release evidence is declaration-based rather than execution-bound

Status: `open, unaccepted, nonblocking Draft proposal`
Impact: High if an untrusted ledger is supplied; no current defect established by this diagnosis
Confidence: High

`scripts/validate_release_evidence.py` requires every configured ID, allowed status, and non-empty `command`/`outcome`, plus release status/version and skipped-test disclosure. It does not bind a check to an executor, observed exit status, raw result artifact, timestamp, or current package digest. The mandatory `workflow-token-proxy` ID is now protected from removal, and focused negative tests pass, but provenance remains a future architecture choice.

### F4 - Builder and Generic benchmark share a broad failure domain

Status: `open, unaccepted, nonblocking Draft proposal`
Impact: Medium maintainability
Confidence: Medium-high

`scripts/build_release.py` remains a 778-line release CLI containing validation, Generic composition, package/archive construction, checksums, and atomic replacement. `scripts/measure_workflow_token_proxy.py` imports `compose_generic_workflow` from it to preserve one canonical composer. Deleting or breaking the builder therefore removes both package composition and Generic fixed-cost measurement. Current behavior is correct and the shared composer avoids semantic duplication.

## 6. Prioritized improvement proposals

1. **Complete the existing release-evidence handoff.** Refresh the Ticket 8 ledger and pending release evidence from the current proxy output, archive hashes, package inventories, and fresh Final Independent Review. This is required release work, not refactor authorization.
2. **F3: specify an execution-bound evidence contract.** If accepted, return through `$write-spec` to define executor identity, observed exit status, result artifact/digest, and binding to the exact package/checksum set while retaining explicit skipped-test disclosure.
3. **F4: isolate pure composition from filesystem transactions.** If accepted, specify one side-effect-free validated release model/composer shared by builder and proxy, with ZIP creation, rollback, and atomic replacement kept in the CLI.
4. **F2: add a locale-neutral behavioral policy inventory.** If accepted, specify a structured inventory for modes, precedence, risks, budgets, gates, completion exceptions, and ownership markers while retaining standalone adapter prompts and translated editorial prose.

Only proposal acceptance followed by an Approved Specification and vertical Ticket Plan may authorize implementation. This Draft authorizes none.

## 7. Potentially affected modules

Release-evidence handoff: `docs/evidence/ask-then-do-it-release-1.3.0.json`, `docs/evidence/ask-then-do-it-release-1.3.0.md`, current Ticket 8 evidence, `dist/checksums.sha256`, and the two current archives.

F2 surface: `core/modules/orchestration.md`, `core/modules/lite-workflow.md`, `core/rules/rules.yaml`, Codex rule mapping and Lite reference, all eleven Generic modules, three-language guides/design docs, fixtures, and policy tests.

F3 surface: `release/release.json`, `scripts/validate_release_evidence.py`, ledger/evidence schema, release check executors/results, and evidence-gate tests.

F4 surface: `scripts/build_release.py`, `scripts/measure_workflow_token_proxy.py`, Generic composition tests, release builder tests, generated Generic output, ZIPs, and checksums.

Closed correction surfaces remain under regression coverage: Codex orchestrator frontmatter and direct-stage guards; `tests/codex/test_lite_workflow.py`; Generic `bootstrap.md`, `orchestration.md`, nine bounded guards; `tests/generic/test_generic_lite_workflow.py`; qualified composer header; package-link matrices; expanded packages; ZIPs; and checksums. Historical `1.2.0` and earlier artifacts remain immutable.

## 8. Unresolved items

- Fresh Final Independent Review and completion of the release-evidence gate remain pending.
- Current ledger/evidence hashes and proxy numbers must be refreshed to match the inspected `dist/` snapshot before any completion claim.
- Live installed Codex dispatch/config behavior remains unverified; static discovery metadata and regression coverage are the strongest available proof.
- Live third-party Generic adherence to the editable declaration and all eleven direct-entry cases remains unverified.
- The six tag-pinned guide URLs require separately authorized publication before remote availability can be established.
- The proxy margin is 2.90 percentage points above the 60% gate in the current run; future workflow text growth could reduce that margin.
- F2-F4 remain neither accepted nor rejected and authorize no implementation.
- The dirty, uncommitted worktree prevents commit-level ownership reconstruction.

## 9. Artifact links

- [Approved Specification](../specs/lite-workflow-mode-1.3.0.md)
- [Approved Ticket Plan](../plans/lite-workflow-mode-1.3.0.md)
- [Original release architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis.md)
- [After-fix architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-fix.md)
- [After-Review-fixes architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-review-fixes.md)
- [Direct-entry correction Review after P2](lite-workflow-mode-1.3.0-direct-entry-correction-review-after-p2.md)
- [Final Independent Review](ask-then-do-it-1.3.0-final-review.md)
- [Final Independent Review after fixes](ask-then-do-it-1.3.0-final-review-after-fixes.md)
- [Codex orchestrator Skill](../../adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md)
- [Generic resolver](../../adapters/generic-prompts/orchestration.md)
- [Generic direct-entry regression](../../tests/generic/test_generic_lite_workflow.py)
- [Codex direct-entry regression](../../tests/codex/test_lite_workflow.py)
- [Release builder and Generic composer](../../scripts/build_release.py)
- [Release configuration](../../release/release.json)
- [Current checksums](../../dist/checksums.sha256)
- [Pending release evidence](ask-then-do-it-release-1.3.0.md)
- [Pending validation ledger](ask-then-do-it-release-1.3.0.json)

The requested `...after-direct-entry-fix.md` prior report was not present and is intentionally not linked.

## 10. Knowledge Base Change Summary

No Project Knowledge Base file was changed. This Draft records closure evidence for existing P1/P2/F1 corrections, retains F2-F4 as unaccepted nonblocking proposals, and introduces no approved durable project knowledge. Any later acceptance must return through Specification and vertical Ticket Planning; it does not authorize direct refactoring.
