# Ask Then Do It 1.3.0 Release Architecture Diagnosis

Artifact type: Architecture Improvement Report

Artifact ID: `ask-then-do-it-1-3-release-architecture`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Status: Draft

Inputs: Approved 1.3.0 Requirement Decision Record, Specification, and Ticket Plan; current working-tree diff; Core and both adapter contracts; localized documentation ownership; `release/release.json`; release builder, validators, token-proxy implementation and fixtures; tests; generated `dist/`; Ticket 1-7 implementation/Review evidence; the 1.2.0 release architecture diagnosis; and focused Git history through `v1.2.0`.

Assumptions: Canonical source is authoritative and `dist/` is disposable generated output. Standalone adapters and localized prose must remain independently usable, so some projection of shared policy is intentional. Ticket 8 is still in progress and no completed 1.3.0 validation ledger, release evidence, or final independent Review is assumed.

Deferred: Any fix, refactor, actual deletion experiment, dependency installation, Config change, package rebuild, publication, Git tag, push, upload, and external announcement.

Handoff: Stop release completion on Finding F1 and return it to the applicable approved Ticket ownership and independent Review path. Optional architecture proposals require explicit acceptance of this report, then a new Approved Specification and vertical Ticket Plan; this Draft authorizes no implementation.

Approval: None. This is the initial `Draft` report.

## 1. Analysis scope and limitations

Capability: `multi_agent`. The primary context inspected the repository with read-only commands, and two isolated read-only diagnostic contexts independently examined adapter/document ownership and release/evidence boundaries.

The analyzed boundary is the 1.3.0 Full/Lite policy from provider-neutral Core through the Codex and Generic adapters, deterministic token proxy, localized documentation, release configuration/build/validation, and generated packages. Evidence includes the complete Approved requirement, Specification, and Plan; all Ticket 1-7 Review artifacts; current source and diff; relevant tests; `dist/` inventory/checksums; and focused prior-release history.

Limitations:

- The working tree combines uncommitted changes from Tickets 1-7, so ownership was reconstructed from the Approved Plan and evidence rather than commit boundaries.
- No broad suite, package rebuild, installation, network check, or external publication check was run for this diagnosis. Final Ticket Reviews provide observed test evidence; this report adds only read-only structural inspection.
- Live-model adherence, OS-level unreadable Config behavior, native-speaker editorial quality, and external URLs remain unverified.
- Ticket 8 remains `In Progress`; absence of its final ledger/evidence/Review is expected unfinished work, not itself a source defect.
- No file was removed, renamed, moved, or rewritten for deletion analysis.

## 2. System architecture summary

The provider-neutral contract is defined by `core/CORE.md`, `core/modules/orchestration.md`, `core/modules/lite-workflow.md`, and the mandatory rule catalog. Codex maps that contract through the orchestrator Skill plus a progressively loaded Lite reference; Generic maps it through standalone prompt modules that the builder composes into one conversation-only workflow.

Localized getting-started guides own the complete user lifecycle. Host guides own Config/capability differences, while root and package `START-HERE` files should be short entry points. This ownership is enforced mainly by documentation tests rather than generation from Core.

`release/release.json` coordinates current identity, adapter inventories, required checks, and managed outputs. `scripts/build_release.py` validates canonical sources, composes Generic output, builds reproducible ZIPs, verifies inventories/checksums, and atomically replaces generated output. `scripts/measure_workflow_token_proxy.py` applies a fixed Codex Full/Lite benchmark and separately reports Generic composed-prompt fixed cost. `scripts/validate_release_evidence.py` accepts a completed evidence record only when every configured ledger entry declares an allowed status and required metadata.

The release flow is therefore:

```text
Core policy
  -> Codex Skill/reference ---------+
  -> Generic prompt modules --------+-> release.json -> builder -> dist + ZIPs + checksums
  -> localized documentation -------+

token-proxy fixture + adapter source -> token-proxy result --+
required-check ledger + release Markdown --------------------+-> evidence validator
```

## 3. Deletion-analysis results

Simulated deletion only (`ARCH-DELETE-001`). No actual deletion gate was authorized or attempted.

| Simulated removal | Inbound dependencies and checks | Outbound/deployment consequence | Result |
| --- | --- | --- | --- |
| `core/modules/lite-workflow.md` | Linked by `core/CORE.md:16` and `core/modules/orchestration.md:76`; directly asserted by `tests/conformance/test_lite_core_contract.py`. | Both adapters retain copied Lite policy, but the normative provider-neutral contract and adapter-mapping basis disappear. Conformance fails; adapter text becomes unanchored. | Fail closed through conformance, but exposes manual policy projection. |
| Codex `skills/ask-then-do-it/references/lite-workflow.md` | Loaded by the orchestrator at `SKILL.md:51`, mapped by `adapters/codex/rule-mapping.yaml:28-51`, and tested by `tests/codex/test_lite_workflow.py`. | Codex Lite routing points to a missing lifecycle. The generic Codex source-inventory builder derives nested files from what exists, so the builder alone does not guarantee this semantic reference; Codex/release tests must reject it. | Consumer behavior breaks; required tests/gates should block release. |
| `adapters/generic-prompts/lite-workflow.md` | Explicitly listed in `release/release.json:32`, referenced by Generic bootstrap/orchestration, and covered by Generic tests. | `validate_generic_source` reports the configured module missing before composition; no Generic package is produced. | Strong configuration-to-builder fail-closed boundary. |
| `release/release.json` | Read by the builder, token-proxy Generic composition, evidence validator, and many release tests. | Current identity, inventories, required checks, archive paths, and managed outputs are unavailable; build and evidence validation cannot proceed. | Single authoritative coordination point with wide blast radius. |
| `scripts/build_release.py` | Executed by release tests and imported by the token proxy for `compose_generic_workflow`. | Codex/Generic package construction, Generic composition, reproducible ZIP/checksum verification, and atomic replacement disappear; the token-proxy CLI also fails at import time. | Release and benchmark share one build-module failure domain. |
| Canonical `getting-started-simple.*.md` guides | Linked from README, host guides, and package entry sources; repository-relative link tests inspect them. | Existing ZIP bytes remain unchanged and still contain links to the removed repository guides. This proves packaged entry navigation is not self-contained or version-bound. | Repository docs tests fail, but already-built packages do not detect the loss. |
| Token-proxy script/fixture | The script is exercised by focused release tests and named as a required ledger check. | Package build can still succeed. The evidence validator does not bind the check ID to the executable or its output, so a self-declared passed ledger can remain structurally acceptable. | Execution responsibility leaks outside the evidence-gate abstraction. |
| `scripts/validate_release_evidence.py` | Direct programmatic callers are focused evidence-gate tests and the Ticket 8 release workflow. | Release completion falls back to manual adherence to the Plan; no executable final acceptance gate remains. | Release assurance is reduced even though packages can still build. |
| `dist/` | Release and package tests inspect its directories, ZIPs, and checksums. | No canonical source is lost; the builder can recreate it. Until rebuild, inventory, ZIP-equivalence, and checksum validation complete, there is no deliverable release. | Recoverable generated-output loss. |
| Ticket 1-7 evidence/Reviews | Linked from the Approved Plan's Completed Ticket states and consumed by Ticket 8. | Runtime and packages may still build, but dependency completion, approved modes, correction history, and independent Review proof become unverifiable. | Evidence-chain failure blocks an honest release claim. |

## 4. Twelve-lens results

| Lens | Outcome | Evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `finding` | The Lite lifecycle is manually projected across Core (`core/modules/lite-workflow.md`), Codex reference, Generic prompt, localized guides, entry pages, fixtures, and literal contract tests. Ticket 4-6 Review history records multiple real drift corrections. |
| 2. Long Function | `no-finding` | `load_config` and `measure_modes` are long linear validation pipelines, but the inspected branches remain named, ordered, and covered; no independent defect was attributable to function length. |
| 3. Large Module or Class | `finding` | `scripts/build_release.py` is 778 lines and owns config schema, marketplace/Plugin/assets, Generic composition, package inventory, ZIP/checksum logic, and filesystem transaction. The token proxy imports it, widening its failure domain. |
| 4. Long Parameter List | `no-finding` | Public and internal interfaces use small cohesive path/config inputs; keyword-only flags separate optional validation behavior. |
| 5. Data Clumps | `no-finding` | Token-proxy event identity `(id, category, source, budget)` and release inventory are explicit validated records. Their deliberate duplication is a tamper oracle, not an unmodeled loose argument bundle. |
| 6. Primitive Obsession | `finding` | Evidence checks are identified by unconstrained strings whose `status`, `command`, and `outcome` fields prove shape but do not bind an executor, exit code, artifact, or digest. |
| 7. Feature Envy | `no-finding` | The token proxy delegates Generic composition to the owning builder rather than copying its header/module algorithm; adapters operate on their own declared surfaces. |
| 8. Divergent Change | `finding` | The builder changes for source-schema, marketplace, asset, composition, archive, and transaction concerns. Localized entry documents also change for installation, mode policy, and package-navigation concerns. |
| 9. Shotgun Surgery | `finding` | A Full/Lite semantic or current-version change requires coordinated edits across Core, two adapters, three locales, entry points, tests, fixtures, configuration, and generated output. The broad 1.3.0 diff and repeated localized Review corrections are observed evidence. |
| 10. Message Chains | `not-applicable` | The scoped implementation is declarative Markdown/YAML/JSON plus direct filesystem functions; no meaningful object-navigation chain exists. |
| 11. Leaky Abstraction | `finding` | Packaged entry pages expose repository-root guide paths absent from the packages. The evidence validator also exposes verification responsibility to ledger producers while presenting a completed-evidence gate. |
| 12. Shallow Module | `finding` | The evidence validator's small interface accepts self-asserted passed checks without connecting them to executable results, so much of the promised release-assurance behavior remains outside the module. |

## 5. Finding evidence, impact, and confidence

### F1 - Packaged START-HERE links do not resolve inside either release package

Severity: `P1 release blocker`
Impact: High
Confidence: High

The Specification requires root, Codex Plugin, and Generic package `START-HERE` files to direct users to the appropriate complete guide (`docs/specs/lite-workflow-mode-1.3.0.md:244-248`). All six package entry sources use repository-root links such as `/docs/guides/getting-started-simple.en.md` (`adapters/codex/plugin/ask-then-do-it/START-HERE.en.md:54`, `release/generic/START-HERE.en.md:19`; equivalent links exist in Traditional Chinese and Japanese).

The builder copies those files unchanged. Its package inventory includes the three entry pages but not `docs/guides/getting-started-simple.*.md` (`scripts/build_release.py:426-439`, `544-553`, `647-668`). Read-only inspection of both generated `dist/` directories confirms neither package contains `docs/guides/`. Therefore, after download/extraction, the entry page's root-relative target is absent.

`tests/release/test_documentation.py:1587-1606` resolves a leading slash against repository root, so it proves the monorepo link, not the packaged link. Package tests prove copied-file equality and exact inventory, which reproduces rather than detects the broken navigation. Release completion must remain blocked until the owned correction and independent Review are complete.

### F2 - Shared workflow and localized policy rely on manual multi-surface projection

Severity: Maintainability proposal
Impact: Medium
Confidence: High

Core is normative, but neither adapter nor localized documentation is derived from a shared structured behavioral inventory. The same risk categories, question/brief/completion budgets, approval rules, validation paths, correction authority, and session behavior appear in Core, two adapter implementations, three complete guides, host guides, entry pages, fixture prose, and tests.

This is partly required because consumer prompts and translations must stand alone. The systemic cost is nevertheless observed: Ticket 4 and Ticket 5 Reviews repeatedly found missing risk categories, completion exceptions, zero-finding behavior, Full-only startup/persistence wording, and one-locale gate drift before correction. Current tests mitigate present drift but future semantic changes still require shotgun edits.

### F3 - Completed release evidence is a declaration gate, not an execution-bound evidence gate

Severity: Assurance/maintainability proposal
Impact: High if ledger provenance is wrong; no current defect when Ticket 8 records honest observations
Confidence: High

`scripts/validate_release_evidence.py:56-90` accepts each configured check when it has a unique ID, an allowed status, and non-empty `command`/`outcome` strings. The Markdown check at lines 92-104 verifies only Completed status, release version, and skipped-test disclosure. It does not bind a check ID to an executor, exit code, output digest, package digest, or timestamp.

This is visible under simulated deletion: the token-proxy executable can disappear while a separately produced ledger still claims `workflow-token-proxy: passed`. The current workflow can remain correct through honest Ticket 8 orchestration, but the validator's trust boundary is weaker than its completed-evidence name suggests and is vulnerable to stale or fabricated ledger data.

### F4 - Release building and Generic benchmark composition share an oversized failure domain

Severity: Maintainability proposal
Impact: Medium
Confidence: Medium-high

`scripts/build_release.py` owns validation of release schema, marketplace, Plugin identity/assets, inventories, reproducible archives, checksums, Generic composition, and atomic filesystem replacement. `scripts/measure_workflow_token_proxy.py:16` imports `compose_generic_workflow` from this CLI module so that benchmark composition remains canonical, which is behaviorally correct but couples a read-only measurement gate to all import-time builder dependencies.

Deleting or breaking the builder therefore removes both packaging and token measurement. A smaller pure release-model/composition boundary could preserve the desirable single composer while isolating filesystem mutation and packaging concerns.

## 6. Prioritized improvement proposals

1. **Block release and restore valid package-to-guide navigation.** Under the existing Approved Plan, return F1 to the applicable Ticket 5/Ticket 7 ownership and independent Review path. Preserve concise entry pages, but ensure the distributed entry resolves to a version-appropriate complete guide, either by packaging the owned guides or by using an explicitly valid external target. Add package-root/ZIP-context link validation. This is a correctness correction, not authorization from this Draft.
2. **Specify an execution-bound release evidence model.** In a future Approved Specification, define a registry or typed record for each required check, including the executor/command identity, observed exit status, result artifact or digest, and how evidence binds to the exact package/checksum set. Keep release-specific required checks configurable while making non-removable mandatory gates explicit.
3. **Separate pure release composition from filesystem release transactions.** Move the validated release model and Generic composer behind a pure, side-effect-free module consumed by both builder and token proxy; keep ZIP creation, output collision handling, backup/rollback, and atomic replacement in the build CLI.
4. **Add a locale-neutral behavioral policy inventory for conformance.** Keep adapter prompts and localized prose editorial and standalone, but centralize exact domain items such as modes, precedence, risk categories, budgets, gates, completion exceptions, and document ownership. Use it to drive structural validators/checklists rather than generate prose.
5. **Retain explicit release declaration validation.** Extend the existing prior-release proposal for a structured current-release declaration inventory so version advances do not rely on broad manual search while historical artifacts remain immutable.

Proposals 2-5 are non-blocking Draft proposals. Acceptance authorizes only Specification work, never direct refactoring.

## 7. Potentially affected modules

F1 correction surface: localized Codex Plugin `START-HERE.*.md`, localized Generic release `START-HERE.*.md`, `release/release.json` if inventory changes, `scripts/build_release.py`, package/document link tests, generated `dist/`, ZIPs, and checksums.

Architecture proposal surface: `core/modules/lite-workflow.md`, `core/rules/rules.yaml`, both adapter mappings, localized documentation contract tests, `release/release.json`, `scripts/build_release.py`, `scripts/measure_workflow_token_proxy.py`, `scripts/validate_release_evidence.py`, release tests/fixtures, and future validation ledger/evidence artifacts.

Historical `1.2.0` and earlier artifacts are not affected and must remain immutable.

## 8. Unresolved items

- Which approved ownership route should correct F1: package the canonical guides, publish stable versioned URLs, or another user-valid handoff that preserves concise entry pages.
- Whether package documentation is required to work fully offline or may explicitly depend on a versioned external guide. The current root-relative repository link proves neither behavior after extraction.
- Whether the final evidence gate should execute checks, verify signed/digested result artifacts, or remain an explicitly trust-based structural validator.
- Whether pure Generic composition should move out of the builder without creating a second release schema authority.
- Ticket 8's final validation ledger, completed release evidence, final independent Review, and all required observed checks remain unavailable because Ticket 8 is still in progress.
- External Git tag, GitHub Release, push, upload, installation, and announcement remain deferred and unverified.

## 9. Artifact links

- [Approved Requirement Decision Record](../requirements/lite-workflow-mode-1.3.0.md)
- [Approved Specification](../specs/lite-workflow-mode-1.3.0.md)
- [Approved Ticket Plan](../plans/lite-workflow-mode-1.3.0.md)
- [Ticket 1 Review after fixes](lite-workflow-mode-1.3.0-ticket-1-review-after-fixes.md)
- [Ticket 2 Independent Review](lite-workflow-mode-1.3.0-ticket-2-review.md)
- [Ticket 3 Independent Review](lite-workflow-mode-1.3.0-ticket-3-review.md)
- [Ticket 4 Final Independent Review](lite-workflow-mode-1.3.0-ticket-4-review-final.md)
- [Ticket 5 Final Independent Review](lite-workflow-mode-1.3.0-ticket-5-review-final.md)
- [Ticket 6 Closure Review](lite-workflow-mode-1.3.0-ticket-6-review-closure.md)
- [Ticket 7 Independent Review](lite-workflow-mode-1.3.0-ticket-7-review.md)
- [Ticket 7 Implementation Evidence](lite-workflow-mode-1.3.0-ticket-7.md)
- [1.2.0 Release Architecture Diagnosis](ask-then-do-it-1.2.0-release-architecture-diagnosis.md)

No 1.3.0 completed release ledger, completed release evidence, or final Ticket 8 Review exists yet; no nonexistent artifact is linked.

## 10. Knowledge Base Change Summary

No Project Knowledge Base file was changed. This Draft records one release blocker and three unaccepted architecture proposals, so it does not establish new approved durable knowledge.

If the user later accepts an architecture proposal, the accepted report must return to Specification and vertical Ticket Planning. Any durable Knowledge Base additions, modifications, or removals must then be proposed through the project-knowledge workflow with separate explicit approval.
