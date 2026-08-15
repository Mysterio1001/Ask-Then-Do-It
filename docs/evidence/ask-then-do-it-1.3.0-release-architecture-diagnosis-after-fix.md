# Ask Then Do It 1.3.0 Release Architecture Diagnosis After Fix

Artifact type: Architecture Improvement Report

Artifact ID: `ask-then-do-it-1-3-release-architecture-after-fix`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Status: Draft

Inputs: Original Draft [1.3.0 release architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis.md); Approved 1.3.0 Specification and Ticket Plan; current relevant diff; six localized Codex/Generic package `START-HERE` sources; six expanded `dist/` copies; corresponding entries in both ZIPs; `dist/checksums.sha256`; updated documentation and clean-build package tests; and the independent [package-link correction Review](lite-workflow-mode-1.3.0-package-link-correction-review.md). Package-link implementation evidence was intentionally not read.

Assumptions: Canonical source remains authoritative and `dist/` is generated output. The approved correction uses version-pinned GitHub guide URLs rather than packaging the complete guides. The final `v1.3.0` tag will expose the referenced guide paths when external publication occurs.

Deferred: Acceptance or implementation of original Findings F2-F4; any refactor; actual deletion experiment; package rebuild; dependency installation; Config change; remote URL dereference; Git tag, push, GitHub Release, upload, installation, and announcement.

Handoff: Finding F1 is closed for the inspected local source/package artifacts, and no current release correctness blocker was found in this closure scope. Ticket 8 may continue its separately Approved integrated validation, final Review, and release-evidence gates. Findings F2-F4 remain unaccepted, non-blocking Draft proposals. This Draft authorizes no refactor or implementation.

Approval: None. This is the initial `Draft` after-fix closure report.

## 1. Analysis scope and limitations

Capability: `multi_agent`. The primary context performed direct read-only repository and package inspection. An isolated independent reviewer and an isolated package-artifact audit supplied separate no-finding evidence without reading implementer conclusions.

The closure boundary is the original F1 package-link defect and the immediately affected delivery chain:

- six localized Codex/Generic package entry sources;
- six corresponding expanded files under `dist/`;
- six corresponding ZIP entries;
- archive checksums;
- updated source and clean-build package tests;
- Approved documentation/package ownership and correction Review evidence.

Limitations:

- No package, source, test, Config, or existing evidence file was modified by this diagnosis.
- No implementation evidence was read, and no broad test suite or package rebuild was run. The independent Review records 32 passing focused tests; this closure independently performed a byte/link/checksum audit.
- Remote GitHub URLs were not dereferenced. Their target paths and `v1.3.0` pin are structurally verified, while actual availability remains part of deferred external publication.
- The cumulative working-tree diff is not commit-isolated. Scope was reconstructed from the Approved Plan, original F1, relevant final artifacts, and independent Review.
- Ticket 8 remains `In Progress`; this report does not claim final release completion.
- No actual deletion was authorized or attempted.

## 2. System architecture summary

The Full/Lite Core and adapter architecture is unchanged from the original diagnosis. This correction affects the documentation delivery edge only.

Package entry sources now point to version-bound complete guides:

```text
Codex START-HERE.{locale}.md
  -> .../blob/v1.3.0/docs/guides/codex.{locale}.md
  -> .../blob/v1.3.0/docs/guides/getting-started-simple.{locale}.md

Generic START-HERE.{locale}.md
  -> .../blob/v1.3.0/docs/guides/generic.{locale}.md
  -> .../blob/v1.3.0/docs/guides/getting-started-simple.{locale}.md

source -> deterministic builder -> expanded package -> ZIP -> checksum
```

This preserves the Specification's ownership split: package `START-HERE` files remain concise; host guides own host-specific behavior; getting-started guides own the complete Full/Lite lifecycle. The packages depend on published, tag-pinned guide content instead of leaking a repository-root filesystem path.

The updated documentation test defines one versioned guide root and checks the two-host/three-locale source matrix. The clean-build release test verifies generated package entries reject the former `](/docs/guides/` form and contain the correct host and complete-workflow URL for each locale. Existing ZIP-equivalence, reproducibility, checksum, and historical-preservation checks remain adjacent release controls.

## 3. Deletion-analysis results

Simulated deletion only (`ARCH-DELETE-001`). Nothing was removed, renamed, moved, or rewritten.

| Simulated removal or failure | Callers, callees, tests, and configuration | Deployment or operational consequence | Result |
| --- | --- | --- | --- |
| One localized package `START-HERE` source | Codex source validation requires all three Plugin start guides; Generic config validation requires all three release start guides. Documentation tests enumerate each host/locale pair. | The builder cannot produce a complete expected package, or focused documentation coverage fails before release. | Fail closed locally. |
| One host/locale URL from a source entry | `tests/release/test_documentation.py:99-137` defines both expected links per host/locale; the clean-build assertions at `tests/release/test_release_1_3_contract.py:301-315` repeat the package contract. | The affected user loses either host instructions or the complete Full/Lite guide. | Focused source/package tests fail. |
| Correct `v1.3.0` URL replaced by the former `/docs/guides/` target | Clean-build package tests explicitly reject `](/docs/guides/`; the closure audit scans all source, expanded, and ZIP entry bytes. | Reintroduces F1: an extracted package points outside its available package context. | Regression is now directly observable and blocked. |
| One expanded `dist/` entry | Builder output-set validation compares package inventory with canonical source and later verifies ZIP equivalence. The closure audit compares source and expanded SHA-256. | Expanded package and ZIP diverge; the deliverable cannot satisfy package evidence. | Recoverable through rebuild, but release evidence fails until restored. |
| One corresponding ZIP entry or byte | ZIP-equivalence logic and release tests compare exact inventory and payload bytes; the closure audit independently compares the six relevant entries. | Archive consumers receive content different from the expanded package. | ZIP/package validation fails. |
| `dist/checksums.sha256` or one correct digest | Builder/release validation requires exact archive inventory and matching SHA-256 values. | Archive identity is unavailable or inconsistent; release evidence cannot bind the deliverables. | Release gate fails. |
| The remote `v1.3.0` tag or one referenced guide at publication time | Local source/package tests validate URL shape and mapping but intentionally do not dereference external state. | The locally correct package link returns unavailable content to users. | `unverified` until external publication; publication must create and verify the promised targets. |
| Independent package-link correction Review | Approved Plan Tickets 5 and 7 link the correction Review as closure evidence. | Artifacts remain correct, but the Full workflow loses independent proof that the blocker was re-reviewed. | Ticket 8 evidence chain becomes incomplete. |
| Original F2 policy projections, F3 evidence validator, or F4 shared builder boundary | Their inbound/outbound dependencies are unchanged from the original simulated deletion analysis. | Removing them would still break adapter conformance, release evidence validation, or both packaging and token-proxy composition. | Original non-blocking architecture risks remain; no deletion is authorized. |

## 4. Twelve-lens results

| Lens | Outcome | Evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `finding` | Original F2 remains: Full/Lite policy is manually projected across Core, adapters, locales, fixtures, and tests. The bounded 12-link host/locale matrix is intentional delivery data and introduces no new blocker. |
| 2. Long Function | `no-finding` | The correction adds matrix assertions to existing test flows; no defect is attributable to function length. Original builder and token-proxy functions remain linear validation pipelines. |
| 3. Large Module or Class | `finding` | Original F4 remains: `scripts/build_release.py` still combines release model, source validation, composition, archives, checksums, and filesystem transaction, and is imported by the token proxy. |
| 4. Long Parameter List | `no-finding` | No correction interface adds a parameter list; existing release helpers retain small cohesive inputs and keyword-only flags. |
| 5. Data Clumps | `no-finding` | Host, locale, host-guide URL, and workflow-guide URL are modeled together as an explicit tested matrix. Token-proxy event tuples remain explicit validated records. |
| 6. Primitive Obsession | `finding` | Original F3 remains: evidence check IDs and self-declared status/command/outcome strings are not bound to typed executors or observed result artifacts. Exact URL strings are appropriate at this user-visible correction boundary. |
| 7. Feature Envy | `no-finding` | Package tests inspect owned built output, and the token proxy still delegates Generic composition to the owning builder. |
| 8. Divergent Change | `finding` | Original F2/F4 remain: workflow policy spans multiple projections, while the builder changes for validation, composition, archive, and transaction concerns. The F1 correction itself stays within package navigation ownership. |
| 9. Shotgun Surgery | `finding` | Original F2 remains. Six localized sources require coordinated edits, although generated copies/ZIPs/checksums are deterministically rebuilt and the new matrix tests bound this specific fan-out. |
| 10. Message Chains | `not-applicable` | The closure concerns static Markdown, direct path reads, ZIP entries, and checksums; no meaningful object-navigation chain exists. |
| 11. Leaky Abstraction | `finding` | The F1 repository-root package leak is resolved. Original F3 remains because release-evidence execution responsibility still leaks to ledger producers outside the validator. |
| 12. Shallow Module | `finding` | Original F3 remains: the evidence validator validates declaration shape without encapsulating check execution or result binding. The package-link correction adds no new abstraction. |

## 5. Finding evidence, impact, and confidence

### F1 - Packaged START-HERE links do not resolve inside either release package

Resolution: `resolved in inspected local artifacts`
Original impact: High release blocker
Resolution confidence: High

Every package source now contains exactly two tag-pinned URLs under:

`https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides`

Codex maps each locale to `codex.{locale}.md` and `getting-started-simple.{locale}.md`; Generic maps to `generic.{locale}.md` and the same-locale complete guide. No inspected source, expanded copy, or ZIP entry retains `](/docs/guides/`.

Independent closure audit results:

| Artifact | Source = expanded = ZIP | Exact two-link mapping | Stale link | SHA-256 |
| --- | --- | --- | --- | --- |
| Codex `en` | Yes | Yes | No | `79549d6ef3e874f4ca3b169af4f4c96132d4c333b81724621a602ca2ccb6e65f` |
| Codex `ja` | Yes | Yes | No | `48514604ae25709df2212292764a7e9c9092c964a8fefe48f51f5ba364234f17` |
| Codex `zh-TW` | Yes | Yes | No | `1bdfb3740c3969fa6bea76cd82406b76456e8403ab377775cadaca4ca6a8bf9c` |
| Generic `en` | Yes | Yes | No | `754bd047d543e040bfe54c4eb143b7b94ec9dadedeb03599d3f77feaa26c9485` |
| Generic `ja` | Yes | Yes | No | `367de63710889b78a828e5e4d3ba375146dea8722e511a054854cd7d0dbfeb71` |
| Generic `zh-TW` | Yes | Yes | No | `277a13117176b52cff0ce88afe72e66b886fe75ac3304f88cbd4175b35d242bc` |

Archive digests independently match `dist/checksums.sha256`:

- Codex: `f3c5ce1e7f48baf5ac619d1719313ca3d91cc1c96af38b67ba4b23aba16bfbd3`
- Generic: `df66b786a8ef855cea9d709f350e5abf3fa943fc61cbe8b903712c7e4e240f6b`

The independent correction Review found no P0-P3 issue and records 32 passing focused documentation/clean-build tests. Its remote-dereference and Red-evidence gaps do not contradict the final local source/package behavior. F1 is therefore no longer a local release correctness blocker.

### F2 - Shared workflow and localized policy rely on manual multi-surface projection

Resolution: `open, unaccepted non-blocking proposal`
Impact: Medium maintainability
Confidence: High

No architectural change was authorized or made. The correction's explicit host/locale test matrices improve F1 regression detection but do not centralize the broader risk, budget, approval, validation, Review, and session policy duplicated across Core, adapters, locales, fixtures, and tests.

### F3 - Completed release evidence is a declaration gate, not an execution-bound evidence gate

Resolution: `open, unaccepted non-blocking proposal`
Impact: High if ledger provenance is wrong; no observed current defect with honest Ticket 8 evidence
Confidence: High

No evidence-gate implementation changed. `scripts/validate_release_evidence.py` still validates configured IDs, declared statuses, and non-empty command/outcome text without binding them to executors, exit codes, exact output, or package digests. This remains an assurance design question, not a new F1 correction blocker.

### F4 - Release building and Generic benchmark composition share an oversized failure domain

Resolution: `open, unaccepted non-blocking proposal`
Impact: Medium maintainability
Confidence: Medium-high

No builder refactor was authorized or made. The token proxy still imports the canonical Generic composer from the release builder, preserving composition correctness while coupling packaging and measurement failure domains.

### New correctness findings

No new release correctness blocker was found within the approved after-fix closure scope.

## 6. Prioritized improvement proposals

1. **Preserve F1 closure through publication.** Keep the exact source/package URL matrix and clean-build stale-link rejection. When external publication is authorized, verify that tag `v1.3.0` exposes all six referenced guide targets. This is an operational completion check, not a refactor proposal.
2. **Specify an execution-bound release evidence model for F3.** If accepted, return through `$write-spec`; define executor identity, observed exit status, result artifact/digest, and package/checksum binding for every required check.
3. **Separate pure release composition from filesystem transactions for F4.** If accepted, specify a side-effect-free validated release model/composer shared by builder and token proxy, leaving archive/output mutation in the CLI.
4. **Add a locale-neutral behavioral policy inventory for F2.** If accepted, centralize exact domain items used by conformance while keeping standalone adapter prompts and localized prose editorial rather than generated.

F2-F4 remain optional Draft proposals. Neither this report nor their presence authorizes production edits, deletion, refactoring, Ticket implementation, or release publication. Explicit acceptance would authorize only Specification work, followed by an Approved vertical Ticket Plan and its selected implementation path.

## 7. Potentially affected modules

Resolved F1 boundary, to preserve without further change:

- `adapters/codex/plugin/ask-then-do-it/START-HERE.{en,ja,zh-TW}.md`
- `release/generic/START-HERE.{en,ja,zh-TW}.md`
- `tests/release/test_documentation.py`
- `tests/release/test_release_1_3_contract.py`
- expanded Codex/Generic `dist/` trees, both ZIPs, and `dist/checksums.sha256`
- externally published `v1.3.0/docs/guides/` targets when publication is authorized

Unaccepted architecture proposal surface remains unchanged:

- F2: Core Lite/orchestration/rules, both adapter mappings, localized documentation contracts, and related fixtures/tests
- F3: `release/release.json`, `scripts/validate_release_evidence.py`, validation ledger/evidence schema, and release-evidence tests
- F4: `scripts/build_release.py`, `scripts/measure_workflow_token_proxy.py`, Generic composition tests, release builder/package tests

Historical `1.2.0` and earlier artifacts remain outside every proposed change and must remain immutable.

## 8. Unresolved items

- Remote availability of the six tag-pinned guide targets is `unverified` until external `v1.3.0` publication is authorized and completed.
- Ticket 8's integrated ledger, completed release evidence, and final independent Review remain unfinished and outside this closure claim.
- The user has not accepted or rejected original F2-F4; they remain non-blocking Draft proposals only.
- If F3 is ever accepted, the project must decide whether the validator executes checks, verifies digested result artifacts, or explicitly remains trust-based.
- If F4 is ever accepted, the project must define a pure composer boundary without creating a second release-schema authority.
- Raw historical Red evidence for the package-link correction was intentionally unavailable to the independent reviewer; current Green/artifact correctness is observed, while TDD chronology is a separate workflow evidence gap.
- External tag, GitHub Release, push, upload, installation, and announcement remain deferred.

## 9. Artifact links

- [Original Draft release architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis.md)
- [Approved Specification](../specs/lite-workflow-mode-1.3.0.md)
- [Approved Ticket Plan](../plans/lite-workflow-mode-1.3.0.md)
- [Package-link correction Independent Review](lite-workflow-mode-1.3.0-package-link-correction-review.md)
- [Ticket 5 Final Independent Review](lite-workflow-mode-1.3.0-ticket-5-review-final.md)
- [Ticket 7 Independent Review](lite-workflow-mode-1.3.0-ticket-7-review.md)
- [Ticket 6 Closure Review](lite-workflow-mode-1.3.0-ticket-6-review-closure.md)

Implementation evidence for the package-link correction was not read and is not used as an input link. No Ticket 8 completed release artifact is linked because none is claimed by this closure.

## 10. Knowledge Base Change Summary

No Project Knowledge Base file was changed. F1 closure is supported by inspected source/package artifacts and an independent Review, but this Draft does not itself promote that observation into formal Project Knowledge Base content.

F2-F4 remain unaccepted proposals and introduce no durable approved knowledge. Accepting any proposal would authorize only a return to Specification; subsequent Knowledge Base changes, if any, require their own displayed additions/modifications/removals and explicit approval.
