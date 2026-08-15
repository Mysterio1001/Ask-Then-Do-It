# Ask Then Do It 1.3.0 Direct-Entry Correction Review After P2

Artifact type: Review Report

Artifact ID: `lite-workflow-mode-1-3-direct-entry-correction-review-after-p2`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Status: `complete - no actionable findings`

Review label: `independent`

Approved implementation mode: Ticket 8 `tdd` (user selected Add tests).

Reviewed inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md); Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), especially Ticket 8; [direct-entry correction Review](lite-workflow-mode-1.3.0-direct-entry-correction-review.md) as the raw trigger report; the user-approved bounded Generic direct-entry decision; current Core, Generic, Codex, tests, localized Generic guides, release configuration, builder, expanded packages, ZIPs, and checksums; and supplied plus independently rerun raw verification.

Independence: This reviewer context did not implement the correction and did not use an implementer conclusion or correction-defense argument to determine the verdict. The prior changes-requested report was used only to identify the trigger and inspected surfaces.

Assumptions: `bootstrap.md` and `orchestration.md` remain the complete Generic mode-resolver owners. The nine other Generic modules are independently pasteable stages that cannot load another prompt, so the approved Core host-specific bounded projection applies. A mode proven by composed orchestration is reused without re-resolution. Canonical source is authoritative and `dist/` is generated release output.

Deferred: Updating the existing validation ledger and release evidence; any source or test correction; live installed-Plugin and third-party-model execution; remote URL dereference; external CI and other operating systems; Git tag, push, publication, installation, upload, and announcement; and the unaccepted Draft architecture proposals F2-F4.

Handoff: Return this no-finding Review to Ticket 8. Refresh release evidence from the current observed package hashes and complete the separately required evidence and completion gates. No source correction is requested by this Review.

## Findings

No actionable P0, P1, P2, or P3 finding was identified.

The prior P2 ownership contradiction is resolved under the approved decision: Core explicitly permits a bounded guard only for an independently distributable standalone stage that cannot load another module; the guard is expressly not complete resolver ownership. Generic keeps complete ownership in `bootstrap.md` and `orchestration.md`, and the nine stage projections reuse proven mode or apply the bounded unproven-entry matrix.

## Correction coverage

| Surface | Result | Evidence |
| --- | --- | --- |
| Core ownership contract | Pass | `core/modules/orchestration.md:27-30`, `core/adapters/manifest-contract.md:22`, and `core/rules/rules.yaml:24-27` distinguish canonical delegation, the permitted bounded projection, proven-mode reuse, and non-persistence. |
| Generic source modules | Pass | Exactly 11 modules exist. `bootstrap.md` and `orchestration.md` state complete ownership; `lite-workflow.md` and the eight Full stages carry the same bounded guard at their direct-entry boundary. |
| Direct-entry matrix | Pass | Every standalone guard applies explicit instruction > available declaration > Full fallback, pauses conflicts, treats invalid declarations as Full, does not persist, and routes away when the resolved mode does not match (`tests/generic/test_generic_lite_workflow.py:205-263`). |
| Localized Generic guides | Pass | English, Traditional Chinese, and Japanese guides describe the two resolver owners, nine bounded projections, proven-mode reuse, precedence, conflict pause, invalid fallback, and stage routing. The English contract is explicit at `docs/guides/generic.en.md:103-105`; localized documentation tests cover all three locales. |
| Codex non-regression | Pass | Canonical orchestrator discovery and all direct Skill mode guards remain covered; focused Codex tests and adapter identity tests pass. No Codex contract delegates to the Generic projection. |
| Generated Generic workflow | Pass | The composed entrypoint contains the qualified editable banner first, one default declaration, the two complete resolver sections, and all nine bounded guards (`dist/generic/ask-then-do-it-generic-1.3.0/generic-workflow.md:1-8`, `:68-138`, `:218`). |
| Packages, ZIPs, checksums | Pass | Current output validation accepts exact 27-file Codex and 18-file Generic inventories, expanded-to-ZIP bytes, and checksum inventory. Current archive hashes match `dist/checksums.sha256`. |

## Twelve architecture and refactoring lenses

This is a change-focused pass, not a system-wide architecture diagnosis. Each lens has exactly one required outcome.

| Lens | Outcome | Evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `no-finding` | The nine repeated guards are an explicitly approved standalone projection, use one standardized sentence, and are checked as a group. The broader policy-projection concern remains the unaccepted Draft F2, not a new correction defect. |
| 2. Long Function | `not-applicable` | The correction is declarative Markdown and release composition text; it adds no production function whose length or mixed responsibility creates a correction risk. |
| 3. Large Module or Class | `no-finding` | No module or class acquired a new responsibility. Existing builder size is outside this correction's defect scope and remains covered by prior architecture diagnosis. |
| 4. Long Parameter List | `not-applicable` | No callable interface or parameter list changed. |
| 5. Data Clumps | `no-finding` | Mode sources and routing outcomes remain explicit textual contracts; no new loose value group crosses an interface. |
| 6. Primitive Obsession | `no-finding` | Exact `full` and `lite` values are the approved public mode contract and are constrained by source, conformance, and matrix tests. |
| 7. Feature Envy | `no-finding` | Complete resolution remains owned by bootstrap/orchestration; stage guards only establish or route the current mode and do not perform stage orchestration. |
| 8. Divergent Change | `no-finding` | The correction adds one bounded, standardized projection for an approved standalone-host limitation; it does not give stages a second complete resolver responsibility. |
| 9. Shotgun Surgery | `no-finding` | Source-to-package generation, ZIP equivalence, and checksum checks make the required release projections deterministic. The multi-surface policy risk is recorded as the deferred F2 proposal, not an introduced blocker. |
| 10. Message Chains | `not-applicable` | The reviewed behavior is declarative Markdown/YAML/JSON and direct package composition; no object-navigation chain was introduced. |
| 11. Leaky Abstraction | `no-finding` | The former Core/stage ownership contradiction is replaced by an explicit delegation-versus-bounded-guard contract. The remaining live model-adherence boundary is disclosed as unavailable evidence. |
| 12. Shallow Module | `no-finding` | Resolver owners and stage modules each expose behavior proportional to their interfaces; the bounded guard does not claim to hide complete orchestration. |

## Verification performed

- Focused reruns passed: Generic bounded-entry/composition `21/21`; Generic prompt contracts `17/17`; Codex mode/non-regression `9/9`; Codex adapter and identity `18/18`; Core contract `7/7`; Generic release and documentation `30/30` (102/102 total).
- `tests.release.test_release_1_3_contract`: `7/7` passed, including isolated package inventory, ZIP, checksum, historical, and reproducibility checks.
- `tests.release.test_release_evidence`: `9/9` passed, including mandatory workflow-token-proxy rejection cases.
- A combined release-contract/safety run observed one Windows atomic-upgrade `WinError 5` in the known temporary-directory rename test. The focused serial retry passed `1/1`; no source assertion remained failed and no temporary directory remained.
- Both conformance CLIs passed: `codex against core 1.3.0` and `generic-prompts against core 1.3.0`. Marketplace validation passed.
- Read-only `build_release.validate_output_set(... require_source_equivalence=True)` returned `['codex', 'generic', 'checksums.sha256']` for the current `dist/` tree. Expanded inventories are Codex `27` files and Generic `18` files.
- Direct checksum recalculation matched `dist/checksums.sha256`: Codex `e2838c830ca56b3c8dc901783e8c773127a65cd0096ddef63f2e919c615bb73e`; Generic `7751999bb2fc01a6ddae0717ddfbd7dc213796d7c2f79d0b7bfe6556eaf39e9d`.
- Direct proxy execution passed the gate: Codex Full `14,771`, Lite `5,480`, difference `9,291`, reduction `62.90%`; Generic fixed composed cost `15,376`, with no Generic 60% or billing claim.
- `git diff --check` exited `0`; output consisted only of informational Windows LF-to-CRLF warnings.
- Supplied integrated evidence additionally records focused integrated `40/40`, final discovery `192/192` after the transient retry, release `107/107`, Codex `27/27`, Generic `39/39`, conformance `19/19`, packaged forward scenarios, and both adapter conformance CLIs passing.

## Evidence unavailable and residual risks

- No live installed Codex Plugin operation exercised every direct-entry and Config combination. Static Skill, mapping, package, and regression coverage cannot prove host/model discovery adherence.
- No live third-party Generic model was run through all eleven direct-paste cases. The tests establish instruction and package parity, not conversational model compliance.
- The current `dist/` hashes differ from the older hashes recorded in `docs/evidence/ask-then-do-it-release-1.3.0.md` and `docs/evidence/lite-workflow-mode-1.3.0-ticket-8.md`. Those artifacts are intentionally `Review Pending`; their refresh is Ticket 8 evidence work and was not performed here.
- This independent context did not rerun the complete 192-test discovery; it relies on the supplied final `192/192` result and the focused reruns above. The known atomic-rename transient was reproduced once and passed on the serial retry.
- TDD Red chronology for the correction was not independently re-executed; the approved Ticket 8 `tdd` mode is preserved and current Green behavior is independently observed.
- External publication, tag-pinned URL availability, installation, external CI, additional operating systems, and sustained concurrent build stress remain unverified or deferred. Draft architecture proposals F2-F4 remain non-blocking and unaccepted.

## Completion assessment

The approved P2 correction appears complete and blocker-free. Generic now has one clear complete resolver ownership boundary, nine explicitly bounded standalone projections, proven-mode reuse without re-resolution, and the approved direct-entry fallback/conflict/non-persistence behavior. Canonical source, localized guidance, tests, composed workflow, expanded package, ZIPs, and checksums agree.

Ticket 8 and the local `1.3.0` release do not yet appear complete solely from this Review: release evidence remains `Review Pending`, and its recorded hashes must be refreshed to the current observed package output before the evidence gate can support completion. This is a pending evidence handoff, not an actionable source finding. External publication remains out of scope and unauthorized.
