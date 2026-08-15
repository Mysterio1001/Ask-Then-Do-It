# Ask Then Do It 1.3.0 Final Independent Review After Fixes

Artifact type: Review Report

Artifact ID: `ask-then-do-it-1-3-final-independent-review-after-fixes`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Review label: `independent`

Status: `changes-requested`

Reviewed inputs: Approved [1.3.0 Specification](../specs/lite-workflow-mode-1.3.0.md); Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md); complete current diff and relevant Core, Codex, Generic, documentation, build, validator, test, release configuration, expanded-package, ZIP, and checksum artifacts; candidate [release ledger](ask-then-do-it-release-1.3.0.json); pending [release evidence](ask-then-do-it-release-1.3.0.md); and the latest allowed [Architecture Improvement Report](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-review-fixes.md).

Approved implementation mode: `tdd` for Tickets 1-8. Tickets 1-7 are recorded Completed in the Approved Ticket Plan; Ticket 8 remains `In Progress`.

Independence: A fresh no-history reviewer context that did not implement the candidate inspected the allowed raw artifacts and independently confirmed the finding below. Implementation evidence and earlier Review, correction, and package-link Review reports were excluded from this pass.

Assumptions: Publicly documented direct Codex Skill and Generic stage-module entrypoints remain supported. The approved requirement to resolve one top-level mode for each operation applies to those entrypoints; direct stage selection does not silently imply Full. Canonical source remains authoritative and `dist/` remains generated release output.

Deferred: Live installed-Plugin dispatch and model adherence; live third-party Generic model adherence; remote `v1.3.0` links before publication; external CI and other operating systems; independent reproduction of the candidate ledger's historical transient Windows `WinError 5`; and publication itself.

Handoff: Keep Ticket 8 and release `1.3.0` blocked. Use a user-approved correction workflow to make every public stage entry resolve or require a proven current-operation mode, add direct-entry regression coverage, rebuild the release artifacts, rerun affected tests and source/package/ZIP/checksum parity, update the pending candidate evidence, and request another fresh independent Review. This Review authorizes diagnosis and reporting only; it does not authorize source fixes or publication.

## Findings

### [P1] Public direct stage entrypoints bypass top-level mode resolution

Trigger: Select Lite through Codex Project/User Config or an explicit current-operation instruction, then invoke a documented stage Skill directly, such as `$implement-tdd`, `$write-spec`, or `$review-code`; equivalently, give an explicit Lite instruction while directly pasting a Generic Full stage module. The Plugin exposes the complete Skill directory (`adapters/codex/plugin/ask-then-do-it/.codex-plugin/plugin.json:8`) and the guide says any Skill may be invoked directly (`docs/guides/codex.en.md:131-145`), but only `$ask-then-do-it` resolves explicit instruction, Project Config, User Config, and Full fallback (`adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md:22-52`). The eight stage Skills enter Full contracts directly; for example, `$write-spec` emits a durable Specification (`skills/write-spec/SKILL.md:21-27`), `$implement-tdd` requires and produces Full TDD evidence (`skills/implement-tdd/SKILL.md:14-22,56-58`), and `$review-code` performs Full Review (`skills/review-code/SKILL.md:42-102`). Generic documents direct use of any stage module (`docs/guides/generic.en.md:99-115`), while only `bootstrap.md:30-36` and `orchestration.md:31-45` resolve mode. Standalone modules immediately specify Full artifacts or behavior, including `requirements.md:14-18`, `tdd-implementation.md:8-18`, and `review.md:8-18`.

Impact: A selected Lite operation can execute Full artifact, approval, TDD/test-change, or twelve-lens Review contracts without Lite's Change Brief, approval, risk, validation, correction, and no-artifact/no-test boundaries. That violates the per-operation precedence and two-mode separation in `docs/specs/lite-workflow-mode-1.3.0.md:81-113`, and can violate the Lite lifecycle at `docs/specs/lite-workflow-mode-1.3.0.md:149-220`. Current tests assert the orchestrator and composed routes (`tests/codex/test_lite_workflow.py:76-187`; `tests/generic/test_generic_lite_workflow.py:95-157`) but do not exercise the documented direct-entry matrix. The live installed Codex dispatcher was not available, so host adherence remains deferred; the public standalone contracts are nevertheless incomplete on their own terms.

Remediation direction: Establish one enforceable entry contract. Every public Codex stage Skill and Generic module must delegate to mode resolution or require evidence that the current operation has already resolved Full before executing a Full stage. A resolved Lite operation must route to Lite regardless of direct stage invocation. Add regression coverage for all nine Codex Skills and eleven Generic modules under explicit Lite, configured or declared Lite, conflicting explicit input, invalid defaults, and Full fallback. Preserve direct Full stage selection after Full is proven. If direct stage selection is intended to imply Full, revise and approve the Specification before implementing that behavioral change.

No other actionable release correctness finding was identified.

## Acceptance Results

The canonical orchestrator and composed Lite implementations satisfy their local content checks. Results below are product-level: P1 makes a documented public route bypass those implementations, so lifecycle criteria are not met for every selected Lite operation.

| AC | Result | Evidence |
|---|---|---|
| 1 | Fail | A direct Codex stage does not execute the required per-operation resolver. Its Full behavior happens to match the fallback result, but the selection contract is not enforced. |
| 2 | Fail | Direct Codex stages do not inspect Project/User Config precedence. |
| 3 | Fail | An explicit Lite instruction has no guard on a directly invoked Full stage. |
| 4 | Fail | Direct Codex stages neither validate Config nor execute the specified invalid-Config fallback contract, even when their Full behavior happens to match the result. |
| 5 | Fail | Standalone Generic stage modules do not enforce declaration/override routing; only bootstrap/orchestration do. |
| 6 | Pass | The normal resolved Full route retains its existing stages, gates, Ticket modes, Review, and architecture contracts (`ask-then-do-it/SKILL.md:51-52,67-151`; `orchestration.md:43-73`). |
| 7 | Fail | The canonical Lite question loop passes focused checks, but direct Full stages can bypass it entirely. |
| 8 | Fail | Direct Full stages can bypass the Lite Change Brief and its content/budget contract. |
| 9 | Fail | A directly selected Full implementation stage can proceed from Full prerequisites without approval of a Lite Change Brief. |
| 10 | Fail | Direct requirements, specification, implementation, Review, and architecture stages can create Full workflow artifacts for a selected Lite operation. |
| 11 | Fail | Direct Full stages can bypass Lite's required risk evaluation and current-operation switch decision. |
| 12 | Fail | Direct `$implement-tdd` or `tdd-implementation.md` can add or propose tests and TDD evidence despite Lite selection. |
| 13 | Fail | Direct Full stages can bypass Lite's minimum-validation sequence. |
| 14 | Fail | Direct Full completion contracts are not guarded by Lite's known-failure completion rule. |
| 15 | Fail | Direct `$review-code` or `review.md` applies the Full fixed-lens Review contract instead of Lite's compact non-independent Review. |
| 16 | Fail | Direct Full Review/correction routing can bypass Lite's one-batch correction approval boundary. |
| 17 | Fail | A directly invoked Full stage is not required to produce the Lite completion report. |
| 18 | Pass | Full proxy `13,828`, Lite proxy `5,416`, difference `8,412`, reduction `60.83%`; the gate remains exactly 60% and makes no billing claim. Fixture SHA-256 is `03211645237dabb53d43458f9e10203d33c10be9f782cd8a13cb1dbef05d5277`; Generic fixed cost is `13,326`. |
| 19 | Pass | The three README language sections preserve Introduction, Automatic installation (CLI), Codex CLI, Manual installation, and Read more ownership/order under the approved Full/Lite edits. |
| 20 | Pass | Localized getting-started guides own the complete flow; root/Codex/Generic START-HERE, host guides, and design documents remain within their narrower responsibilities. No separate Lite guide was added. |
| 21 | Pass | Three-language documentation suites passed, and direct source/package inspection found no localized delivery mismatch. |
| 22 | Fail | Identity, conformance, package inventories, ZIP parity, hashes, and historical preservation pass, but P1 prevents release completion. Ticket 8 is still `In Progress` and release evidence correctly remains `Review Pending`. |

## Architecture And Refactoring Lenses

| Lens | Outcome | Evidence |
|---|---|---|
| 1. Duplicated Code or Policy | `finding` | Trigger: change top-level mode semantics. Impact: manually projected policy can omit a public surface, as P1 does. Evidence: the resolver/lifecycle is repeated across Core, two adapters, localized docs, fixtures, and literal tests, while direct stage entries lack the guard. This is the existing non-blocking Draft F2 plus P1's concrete release defect. |
| 2. Long Function | `no-finding` | Reviewed Python builder, proxy, and validator routines remain linear enough to inspect and have focused tests; no individual changed routine creates a separate actionable defect. |
| 3. Large Module or Class | `finding` | Trigger: change release schema, Generic composition, package inventory, archives, checksums, or replacement behavior. Impact: one module carries a broad release failure domain. Evidence: `scripts/build_release.py:80-770` owns all of those responsibilities. This is existing non-blocking Draft F4, not a second release blocker. |
| 4. Long Parameter List | `no-finding` | Changed interfaces pass cohesive config/path values; no unstable coordination interface or missing domain concept was found. |
| 5. Data Clumps | `no-finding` | Package inventories, proxy events, and link matrices are represented as explicit collections rather than recurring loose argument groups. |
| 6. Primitive Obsession | `finding` | Trigger: provide plausible `status`, `command`, and `outcome` strings in the ledger. Impact: validation can prove declaration shape but not that a bound command execution produced the stated outcome. Evidence: `scripts/validate_release_evidence.py:60-90`. This is existing non-blocking Draft F3. |
| 7. Feature Envy | `no-finding` | Reviewed modules primarily operate on data and outputs they own; no behavior materially belongs to another unit. |
| 8. Divergent Change | `finding` | Trigger: independently change schema validation, prompt composition, packaging, archives, hashes, or atomic replacement, or change mode policy across adapters/locales. Impact: unrelated reasons converge on `build_release.py` and repeated policy surfaces. Evidence: `scripts/build_release.py:171-770` and the F2/F4 scopes. These remain non-blocking Draft architecture concerns. |
| 9. Shotgun Surgery | `finding` | Trigger: correct direct-entry mode semantics. Impact: the current design requires coordinated edits across exposed Codex Skills, Generic modules, documentation, tests, generated packages, ZIPs, and checksums. Evidence: P1's affected scope and existing Draft F2. |
| 10. Message Chains | `not-applicable` | The reviewed runtime is primarily declarative Markdown plus procedural build/validation scripts; it has no meaningful object-navigation chain whose internal structure is exposed to callers. |
| 11. Leaky Abstraction | `finding` | Trigger: use a documented stage entry directly. Impact: callers must know that only the orchestrator/composed entry owns mode resolution, although the stage is presented as independently usable. Evidence: `docs/guides/codex.en.md:145`, `docs/guides/generic.en.md:101`, and the resolver-only locations in P1. This is part of the P1 blocker. F3 separately remains a non-blocking validator-interface leak. |
| 12. Shallow Module | `finding` | Trigger: enter through a stage instead of the resolver, or treat the evidence validator as execution-bound. Impact: the dispatch boundary does not hide mode-entry complexity, and the evidence gate does not bind execution provenance. Evidence: P1 and `scripts/validate_release_evidence.py:39-90`. The first is part of P1; the second is existing non-blocking Draft F3. |

The latest Architecture Improvement Report's F2-F4 remain unaccepted, non-blocking Draft proposals and authorize no refactor. They are referenced here rather than duplicated as additional release findings. P1 is the only actionable current release finding.

## Verification Performed

- Full serial discovery: `180/180`, OK.
- Release suite: `105/105`, OK.
- Codex suite: `24/24`, OK.
- Generic suite: `33/33`, OK.
- Conformance suite: `18/18`, OK.
- Canonical and packaged Codex Skill validation: `18/18` valid.
- Canonical and packaged Plugin validation: `2/2` passed.
- Codex and Generic conformance CLIs passed against Core `1.3.0`.
- Marketplace validation passed.
- `git diff --check` exited `0`; only line-ending conversion warnings were emitted.
- Persistent source/package audit found zero canonical-to-expanded mismatches.
- Codex expanded/ZIP audit: `27/27`, zero duplicate entries and zero byte mismatches.
- Generic expanded/ZIP audit: `18/18`, zero duplicate entries and zero byte mismatches.
- SHA-256 matched the checksum manifest: Codex `f4448e20e2654ed5837cbddd5d0713c79b933a1410f4d13e91ac2ef84a775995`; Generic `b399c9de509acf65d2ed277ed9d86d29926fd756947b1dff68c434f5ffa059c1`.
- All 16 pinned historical `1.2.0` hashes passed through the release suite.
- The release-evidence validator correctly rejected the current artifact while its status is `Review Pending`.

## Evidence Unavailable And Residual Risk

- No live installed Codex Plugin dispatch or model-adherence run proves how the host combines implicit orchestrator discovery with an explicitly named stage Skill. This uncertainty does not supply the missing direct-entry contract or regression matrix.
- No live third-party Generic model-adherence run was performed.
- Remote tag-pinned `v1.3.0` guide targets cannot be checked until publication, which is not authorized by this Review.
- External CI and operating systems other than this Windows workspace were not exercised.
- The earlier transient candidate-ledger `WinError 5` sequence was not independently replayed; current serial suites and parity checks passed.
- Ledger check provenance remains declaration-based rather than execution-bound, as tracked by Draft F3.
- The measured proxy clears the fixed gate by only `0.83` percentage points, so small controlled-content growth could regress AC 18.
- Current `dist/` source-byte parity was audited directly, but the absence of a durable regression covering every current expanded source byte remains a release-maintenance risk.

## Completion Assessment

Ticket 8 does not appear complete. The actionable P1 finding blocks Ticket 8 and release `1.3.0`; the candidate Release Evidence must remain `Review Pending`. No source fix, release-evidence completion, or publication is authorized by this Review.
