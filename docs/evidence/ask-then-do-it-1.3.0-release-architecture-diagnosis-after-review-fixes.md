# Ask Then Do It 1.3.0 Release Architecture Diagnosis After Review Fixes

artifact_type: Architecture Improvement Report

artifact_id: `ask-then-do-it-1-3-release-architecture-after-review-fixes`

workflow_id: `lite-workflow-mode`

core_version: `1.1.0`

status: `draft`

inputs: Approved [1.3.0 Specification](../specs/lite-workflow-mode-1.3.0.md) and [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md); original [Final Independent Review](ask-then-do-it-1.3.0-final-review.md); original Draft [Release Architecture Diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis.md) and Draft [After-Fix Architecture Diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-fix.md); current raw Core, Codex, Generic, test, release-builder, release-configuration, expanded-package, ZIP, and checksum artifacts.

assumptions: The current working tree is the intended local candidate after the approved P1 and P2 corrections. Canonical source remains authoritative and `dist/` remains generated output. Codex Skill frontmatter description is the Plugin's implicit discovery surface; a downloaded Generic `generic-workflow.md` is the user-editable conversation entrypoint while the repository builder remains authoritative for official packages. A future authorized `v1.3.0` publication will provide the version-pinned guide targets used by package entry pages.

deferred: Acceptance or implementation of Findings F2-F4; any refactor or actual deletion experiment; changes to source, tests, configuration, `dist/`, plans, or release evidence; installed-Plugin and live-model execution; remote URL dereference; external CI and additional operating systems; Git tag, GitHub Release, push, upload, installation, publication, and announcement.

handoff: No new release correctness blocker was found. P1 and P2 are structurally resolved in current source, focused regression tests, expanded packages, ZIP entries, and checksums; prior F1 remains resolved locally. Return the candidate to the separately required fresh Final Independent Review and release-evidence gates. F2-F4 remain unaccepted, non-blocking Draft proposals and authorize no implementation.

approval: None. This is an initial `draft` closure report. Acceptance would authorize only a return to Specification for accepted proposals, never direct refactoring or release publication.

## 1. Analysis scope and limitations

Capability: `multi_agent`. This report was produced in a dedicated read-only architecture context with repository tools. An additional diagnostic child could not be started because the active agent limit was reached, so all retained conclusions were directly rechecked in this context against raw current artifacts.

The analyzed boundary is the Ask Then Do It `1.3.0` release path from provider-neutral Core through Codex discovery/mode resolution and Generic composition, then through release configuration, deterministic package expansion, ZIP construction, and checksums. The closure questions are:

- whether Final Review P1's Codex dispatch gap is structurally closed for trivial, fully specified, formatting-only, and single-line software changes;
- whether Final Review P2's Generic editable-default contradiction is structurally closed;
- whether canonical source, expanded package, ZIP, and checksum boundaries remain coherent after those corrections;
- whether original architecture Finding F1 remains resolved; and
- whether current raw evidence changes the status of Draft proposals F2-F4.

Evidence boundaries and limitations:

- No new correction implementation evidence and no correction Review were read. Conclusions come from the Approved Specification/Plan, the original Final Review, the two named prior architecture reports, and raw current source/tests/packages/configuration.
- The working tree is cumulative and uncommitted, so corrections cannot be attributed to commit boundaries. The inspected current archive hashes identify the package snapshot used by this report.
- Codex's installed live Skill-discovery behavior was not executed. P1 closure is a structural conclusion based on the actual discovery metadata, routing contract, regression test, and byte-identical packaged Skill.
- A live third-party Generic model was not exercised. P2 closure establishes a coherent edit instruction and deterministic composition/package boundary, not model adherence.
- The six `v1.3.0` guide URLs were not dereferenced. Their local mapping and package bytes are proven; remote availability remains dependent on separately authorized publication.
- Forty-one focused tests, both adapter conformance commands, the token-proxy command, current package validation, and direct byte/hash audits were run. A complete repository suite was not rerun by this architecture context. The focused release tests performed isolated clean builds; this context did not replace the persistent `dist/` tree.
- No current correction Review, completed ledger, or completed release-evidence conclusion was used as architecture evidence. This report does not substitute for Final Review or authorize a completion-state change.
- Simulated deletion only was used. No file, directory, ZIP entry, configuration value, or authoritative data was removed, renamed, moved, or rewritten.

## 2. System architecture summary

Core `1.3.0` defines exactly two top-level modes and their host-neutral contracts in `core/CORE.md`, `core/modules/orchestration.md`, `core/modules/lite-workflow.md`, the mandatory rule catalog, and the adapter manifest contract.

Codex implements the entry boundary through the `ask-then-do-it` Skill. Its frontmatter description is the implicit discovery interface. Once loaded, the Skill resolves explicit instruction, project Config, user Config, and Full fallback before selecting either Lite or a Full subpath. The progressively loaded Lite reference owns the complete Lite lifecycle. Conformance YAML and rule mapping identify the normative Core rules, while package construction copies the Plugin source tree unchanged.

Generic uses a generated conversation entrypoint. `scripts/build_release.py::compose_generic_workflow` emits the narrowly editable default declaration and routing header, then appends the configured source modules in fixed order. The generated `manifest.yaml` remains fully generated and correctly retains its own `DO NOT EDIT` marker; that marker does not apply to `generic-workflow.md`.

`release/release.json` is the release coordination authority for version, Codex Skill inventory, Generic module order, expanded directories, archive names, required validation checks, and managed outputs. The builder validates canonical source, composes Generic, expands both packages, writes reproducible ZIPs, checks exact inventories and directory-to-ZIP bytes, calculates SHA-256 values, and atomically replaces managed output. `scripts/measure_workflow_token_proxy.py` imports the canonical Generic composer. `scripts/validate_release_evidence.py` separately validates the shape and declared status of release-check records.

The relevant flow is:

```text
Core mode policy
  -> Codex discovery description -> mode resolver -> Full or Lite reference
  -> Generic composer header/default -> ordered prompt modules

canonical source + release.json
  -> builder validation
  -> expanded Codex (27 files) + expanded Generic (18 files)
  -> byte-equivalent ZIPs
  -> checksums.sha256

six package START-HERE sources
  -> expanded entries -> ZIP entries
  -> version-pinned v1.3.0 guide URLs
```

P1 is therefore owned at the Codex discovery boundary, not merely inside the resolver. P2 is owned by the complete generated-entrypoint instruction, not merely the declaration string. F1 is owned by the source-to-package documentation delivery edge.

## 3. Deletion-analysis results

Simulated deletion only (`ARCH-DELETE-001`). Explicit authorization for actual deletion was absent, the user expressly prohibited it, and no disposable isolated working copy was established. The actual-deletion gates therefore fail even though repository inspection tools are available.

| Simulated removal or regression | Callers, callees, tests, configuration, and deployment effect | Result |
| --- | --- | --- |
| Codex orchestrator discovery description, or its coverage of one small-request class | The Plugin exposes Skills through `.codex-plugin/plugin.json`; implicit selection relies on Skill frontmatter. Removing `every software-changing operation`, `trivial`, `fully specified`, `formatting-only`, or `single-line` recreates P1 even though the resolver remains correct after load. `tests/codex/test_lite_workflow.py:76-107` fails. If the whole Skill directory disappears, `release.json` inventory and builder validation also fail. | Release gate fails through focused tests/inventory. Without those gates, runtime Config routing becomes unreachable for the removed request class. |
| Codex `Resolve the top-level mode` section or Lite reference | Rule mapping and conformance still claim `MODE-RESOLVE-001`/Lite rules, while the runnable contract disappears. Codex tests fail; deleting the reference also leaves an explicit broken link. Existing packages remain stale until rebuilt. | Consumer behavior breaks and conformance/package validation must block a new release. |
| Resolved-Full qualification around the legacy lightweight path | A small Full operation again appears to enter an unnamed third route, while a Lite operation could be misread as eligible for the legacy path. The discovery regression checks the four qualification phrases. | Recreates part of Final Review P1; focused test fails. |
| Generic edit-permission banner or sole default declaration | Removing the permission restores ambiguity; restoring unqualified `GENERATED FILE - DO NOT EDIT` recreates P2; removing the declaration forces fallback and removes the promised configurable default. Current-package and clean-build assertions in `tests/release/test_generic_release.py` fail. | User-facing Generic configuration contract fails closed at release testing. |
| `compose_generic_workflow` | Generic package generation cannot create its executable entrypoint. The token proxy also loses its imported canonical composer. | Both packaging and Generic fixed-cost measurement fail, demonstrating unchanged F4 coupling. |
| One version-pinned host or complete-workflow link in a package `START-HERE` source | Source documentation matrix tests and clean-build package tests reject the missing/wrong link or the former `/docs/guides/` form. Existing expanded/ZIP copies would diverge from source until rebuilt. | Recreates F1; focused source/package gates fail. Remote target existence remains a publication responsibility. |
| `release/release.json` | Builder, token proxy, evidence validator, and release tests lose version, inventory, path, and required-check authority. | Packaging and evidence validation cannot proceed; wide but explicit coordination boundary. |
| One expanded file, ZIP entry, or checksum record | `validate_output_set` compares exact output inventory, expanded-to-ZIP entry sets and bytes, archive inventory, and SHA-256. | Release validation fails; generated output is recoverable only through a successful rebuild. |
| Entire `dist/` tree | No canonical source is lost. A deterministic build can recreate it, but there is no deliverable until inventories, ZIP equivalence, and checksums pass. | Recoverable generated-output loss; release claim blocked until regeneration and validation. |
| Core Lite module or one adapter policy projection | Core links/rules and conformance tests fail for the normative module. Removing only one projection produces Core/adapter/localization drift. | Demonstrates F2's manual multi-surface policy projection; no deletion is authorized. |
| `scripts/validate_release_evidence.py` or the executable behind a declared ledger check | The release loses its structural completion gate; conversely, the current validator can still accept non-empty self-declared command/outcome text after an executor disappears. | Demonstrates unchanged F3 assurance boundary. |

## 4. Twelve-lens results

| Lens | Outcome | Current evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `finding` | F2 remains: modes, precedence, risks, budgets, approvals, validation, Review, and session policy are manually projected through Core, Codex, Generic, localized guides, fixtures, and literal tests. P2's specific banner/guide contradiction is resolved, but the broader projection remains. |
| 2. Long Function | `no-finding` | Builder, proxy, and validator routines are linear validation/composition pipelines. No current release defect or correction fragility was attributable to an individual function's length. |
| 3. Large Module or Class | `finding` | F4 remains: `scripts/build_release.py` is 778 lines and owns schema/source validation, Plugin assets, Generic composition, inventories, ZIPs, checksums, and filesystem transactions; the proxy imports its composer. |
| 4. Long Parameter List | `no-finding` | Inspected public functions accept cohesive config/path inputs and a small number of flags. Neither correction added coordination parameters. |
| 5. Data Clumps | `no-finding` | Release inventories, mode sources, proxy events, and host/locale link matrices are explicit records or configuration collections rather than repeatedly travelling loose value groups. |
| 6. Primitive Obsession | `finding` | F3 remains: required check IDs and ledger `status`, `command`, and `outcome` values are primitive strings without executor, exit-status, result-artifact, or package-digest binding. |
| 7. Feature Envy | `no-finding` | Package tests inspect their owned outputs; the token proxy reuses the owning Generic composer; adapters map their own host surfaces. No correction reaches through an unrelated unit's internal data. |
| 8. Divergent Change | `finding` | F2/F4 remain. Shared workflow policy changes require many projections, while the builder changes for validation, composition, archive, checksum, and transaction reasons. |
| 9. Shotgun Surgery | `finding` | F2 remains. P1 and P2 each required synchronized source, regression, package, ZIP, and checksum changes; broader mode semantics still span Core, two adapters, three locales, fixtures, and release tests. Deterministic packaging contains current byte drift but does not remove the edit fan-out. |
| 10. Message Chains | `not-applicable` | The scoped runtime is Markdown/YAML/JSON plus direct filesystem, ZIP, and hash functions. There is no meaningful object-navigation chain to assess. |
| 11. Leaky Abstraction | `finding` | P1's discovery/resolver leak and F1's repository-root package-link leak are resolved. F3 remains because check-execution provenance is supplied outside a validator whose interface presents a completed-release gate. |
| 12. Shallow Module | `finding` | P1 no longer shows a shallow dispatch boundary. F3 remains: the evidence validator checks declarations and status strings but does not encapsulate or bind execution of the checks it appears to gate. |

## 5. Finding evidence, impact, and confidence

### Final Review P1 - Codex Config defaults did not reach small operations

Resolution: `resolved structurally in current candidate`
Original severity: P1 release blocker
Resolution confidence: High for source/package structure; live installed-host adherence unverified

The current orchestrator frontmatter at `adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md:3` now tells implicit discovery to use the Skill for every software-changing operation and names all four previously excluded classes. The same Skill requires mode resolution for every current operation at line 24. Lines 67-69 make the remaining lightweight handling explicitly a resolved-Full subpath, state that it is not a third top-level mode, and prohibit it after Lite selection.

`tests/codex/test_lite_workflow.py:76-107` parses the actual frontmatter and asserts the universal software-change scope, each small-request class, implicit discovery, mode resolution, and the resolved-Full qualifications. A direct audit found the canonical Skill, expanded Codex package, and ZIP entry byte-identical. There is no longer a normative discovery exclusion that bypasses the only resolver.

This is the strongest structural proof available for a natural-language Skill-discovery contract. A live installed Plugin operation with Config-selected Lite and Full fallback remains a useful host-level check, but the prior defect was directly visible in source and no longer exists there.

### Final Review P2 - Generic's editable default was under `DO NOT EDIT`

Resolution: `resolved structurally in current candidate`
Original severity: P2 release blocker
Resolution confidence: High

`scripts/build_release.py:572` now emits a first-line instruction that permits editing only the `Default workflow mode` declaration below. The sole declaration is emitted at line 579, and lines 583-587 describe its override and fallback semantics. The expanded workflow reproduces this at `dist/generic/ask-then-do-it-generic-1.3.0/generic-workflow.md:1` and line 8.

`tests/release/test_generic_release.py:67-73` checks the current package, while lines 162-168 check a clean build: the qualified permission must precede the declaration and the unqualified prohibition must be absent. Direct composition audit found composer output, expanded file, and ZIP entry byte-identical; the declaration occurs exactly once. The builder's separately generated `manifest.yaml` still says `DO NOT EDIT`, appropriately, but that instruction is in another file and does not contradict the entrypoint exception.

### Original architecture F1 - Packaged START-HERE links did not resolve in package context

Resolution: `remains resolved in current local artifacts`
Original severity: P1 release blocker
Resolution confidence: High locally; remote availability unverified

All six Codex/Generic host-locale sources still contain the appropriate host guide and complete-workflow guide under `https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides`. None contains the former `](/docs/guides/` target. For all six entries, source, expanded package, and ZIP bytes match, and both expected URLs are present. The documentation and clean-build release tests retain their versioned-root and stale-link guards.

The unresolved external boundary is unchanged: those URLs become dereferenceable only when separately authorized publication creates the `v1.3.0` tag with the referenced paths.

### F2 - Shared workflow and localized policy rely on manual multi-surface projection

Resolution: `open, unaccepted non-blocking Draft proposal`
Impact: Medium maintainability
Confidence: High

Current raw source still repeats the same domain items across Core, the two adapter implementations, three-language guidance, fixtures, and tests. The P1/P2 regressions now have focused guards, but no locale-neutral behavioral inventory or generation boundary was introduced. No raw evidence changes F2's prior status.

### F3 - Completed release evidence is declaration-based rather than execution-bound

Resolution: `open, unaccepted non-blocking Draft proposal`
Impact: High if ledger provenance is wrong; no current release defect established by this diagnosis
Confidence: High

`scripts/validate_release_evidence.py:60-90` still indexes string IDs, permits declared statuses, and requires non-empty `command`/`outcome` strings. Lines 92-104 check evidence status/version/disclosure. The validator does not bind executor identity, observed exit status, raw result artifact, timestamp, or the current archive digests. No raw evidence changes F3's prior status.

### F4 - Release building and Generic measurement share an oversized failure domain

Resolution: `open, unaccepted non-blocking Draft proposal`
Impact: Medium maintainability
Confidence: Medium-high

`scripts/build_release.py` remains 778 lines with composition and filesystem-release responsibilities in one module. `scripts/measure_workflow_token_proxy.py:16` still imports `compose_generic_workflow` from it and calls it at line 596. This preserves one canonical composer and current correctness, while deletion or import failure still removes both packaging and Generic fixed-cost measurement. No raw evidence changes F4's prior status.

### New release correctness findings and blocker verdict

No new release correctness finding was found. P1 and P2 are structurally closed, prior F1 remains locally closed, and F2-F4 remain non-blocking Draft proposals. This architecture verdict does not replace the required fresh Final Independent Review or completed release-evidence gate.

### Raw verification performed

| Check | Observed result |
| --- | --- |
| `python -B -m unittest` for Codex Lite, Generic Lite, Generic release, 1.3 release contract, and release contract modules | `41/41` passed in `3.077s`; `OK`. The selected release-contract tests include isolated clean builds and two-build reproducibility checks. |
| Current `dist/` through `build_release.validate_output_set(... require_source_equivalence=True)` | Passed; Codex expanded inventory `27`, Generic expanded inventory `18`; expanded-to-ZIP inventory and bytes and checksum inventory all accepted. |
| Direct canonical-source to expanded-package audit | Zero Codex source mismatches, zero Generic module mismatches, zero Generic START-HERE mismatches, zero legal-file mismatches; generated Generic manifest matched. |
| Direct ZIP audit | Codex `27/27`, Generic `18/18`; zero duplicate entries in either ZIP. |
| P1 direct audit | Canonical Skill = expanded Skill = ZIP Skill; universal discovery terms and resolved-Full boundary all present. |
| P2 direct audit | Composer = expanded entrypoint = ZIP entry; qualified banner is first line; one default declaration; unqualified `DO NOT EDIT` absent from entrypoint. |
| F1 direct six-entry audit | All six source = expanded = ZIP; correct host/locale and complete-workflow URLs; no former root-relative guide link. |
| SHA-256 recalculation through current output validation | Codex `f4448e20e2654ed5837cbddd5d0713c79b933a1410f4d13e91ac2ef84a775995`; Generic `b399c9de509acf65d2ed277ed9d86d29926fd756947b1dff68c434f5ffa059c1`; both match `dist/checksums.sha256`. |
| Codex and Generic conformance CLIs | `Conformance passed: codex against core 1.3.0`; `Conformance passed: generic-prompts against core 1.3.0`. |
| Deterministic token proxy | Full `13,828`; Lite `5,416`; difference `8,412`; reduction `60.83%` against minimum `60.00%`; Codex gate passed. Generic fixed cost `13,326`, with no 60% or billing claim. |
| `git diff --check` | Exit `0`; only informational LF-to-CRLF warnings. |

## 6. Prioritized improvement proposals

1. **Preserve P1/P2/F1 closure through the remaining release gates.** The fresh Final Independent Review should re-evaluate the public dispatch/edit contracts from raw source and generated artifacts. When publication is separately authorized, verify the six `v1.3.0` guide targets. This is release verification, not a new refactor proposal.
2. **F3 - Specify an execution-bound release evidence model.** If explicitly accepted, return through `$write-spec` and define executor identity, observed exit status, raw result artifact or digest, and binding to the exact ZIP/checksum set.
3. **F4 - Separate pure release composition from filesystem transactions.** If explicitly accepted, specify one side-effect-free validated release model/composer shared by builder and proxy while leaving ZIP creation, replacement, rollback, and other mutation in the build CLI.
4. **F2 - Add a locale-neutral behavioral policy inventory for conformance.** If explicitly accepted, centralize exact modes, precedence, risk categories, budgets, gates, completion exceptions, and ownership markers for structural validation while keeping adapter prompts and translations standalone and editorial.

F2-F4 retain their original IDs, evidence, and non-blocking Draft status. This report does not accept them. Even explicit report acceptance would authorize only Specification work, followed by an Approved vertical Ticket Plan and its selected `$implement-tdd` or `$implement-direct` path.

## 7. Potentially affected modules

P1 closure boundary:

- `adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md`
- `tests/codex/test_lite_workflow.py`
- Codex expanded package, `ask-then-do-it-1.3.0.zip`, and checksum entry

P2 closure boundary:

- `scripts/build_release.py`
- `tests/release/test_generic_release.py`
- Generic generated `generic-workflow.md`, expanded package, `ask-then-do-it-generic-1.3.0.zip`, and checksum entry

F1 preservation boundary:

- six localized Codex/Generic package `START-HERE` sources
- `tests/release/test_documentation.py` and `tests/release/test_release_1_3_contract.py`
- six expanded package entries, six ZIP entries, and future published `v1.3.0/docs/guides/` targets

Unaccepted proposal surfaces remain unchanged:

- F2: Core Lite/orchestration/rules, Codex and Generic mappings, localized behavior contracts, fixtures, and related tests
- F3: `release/release.json`, `scripts/validate_release_evidence.py`, ledger/evidence schema, result provenance, and release-evidence tests
- F4: `scripts/build_release.py`, `scripts/measure_workflow_token_proxy.py`, Generic composition tests, and release builder/package tests

Historical `1.2.0` and earlier artifacts remain outside every proposed change and must remain immutable.

## 8. Unresolved items

- Live installed-Plugin dispatch for Config-selected Lite and Full fallback across the four formerly excluded small-request classes remains unverified. The source-level exclusion is removed and the package is coherent.
- Live Generic model adherence to the editable declaration, explicit override, and invalid-declaration fallback remains unverified. The complete shipped instruction is now internally coherent.
- Remote availability of the six tag-pinned guide targets remains unverified until external publication is explicitly authorized and completed.
- The token proxy passes by `0.83` percentage points. This is not a current failure; the deterministic gate should remain mandatory because future workflow-text growth has limited margin.
- A fresh Final Independent Review, any release-evidence status transition, and external publication remain separate pending gates. This diagnosis intentionally did not read a correction Review or new implementation evidence.
- F2-F4 have not been accepted or rejected. They remain non-blocking Draft proposals only.
- If F3 is accepted later, the project must choose whether validation executes checks, verifies digested result artifacts, or explicitly documents a trust-based gate.
- If F4 is accepted later, the pure composer boundary must avoid introducing a second release-schema authority.
- The cumulative dirty working tree prevents commit-level ownership reconstruction. Current package hashes and raw paths identify the inspected state, but not a historical commit.

## 9. Artifact links

- [Approved Specification](../specs/lite-workflow-mode-1.3.0.md)
- [Approved Ticket Plan](../plans/lite-workflow-mode-1.3.0.md)
- [Original Final Independent Review](ask-then-do-it-1.3.0-final-review.md)
- [Original Draft Release Architecture Diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis.md)
- [Draft After-Fix Architecture Diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-fix.md)
- [Codex orchestrator Skill](../../adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md)
- [Codex discovery regression](../../tests/codex/test_lite_workflow.py)
- [Release builder and Generic composer](../../scripts/build_release.py)
- [Generic package regression](../../tests/release/test_generic_release.py)
- [Release configuration](../../release/release.json)
- [Current checksums](../../dist/checksums.sha256)

No correction implementation evidence or correction Review is linked because neither was read or used as an input to this diagnosis.

## 10. Knowledge Base Change Summary

No Project Knowledge Base file was changed. This report records closure evidence for existing release findings and retains three already-proposed architecture improvements without accepting them, so it creates no new approved durable project knowledge.

If the user later accepts F2, F3, or F4, that acceptance authorizes only a return to Specification. Any subsequent durable Knowledge Base additions, modifications, or removals must be displayed and approved through the project-knowledge workflow, followed by an Approved vertical Ticket Plan before implementation.
