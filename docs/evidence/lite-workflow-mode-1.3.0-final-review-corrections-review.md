# Ask Then Do It 1.3.0 Final Review Corrections Independent Review

Artifact type: Review Report

Artifact ID: `lite-workflow-mode-1-3-final-review-corrections-review`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Status: Completed - No Changes Requested

Review label: `independent`

Reviewed inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md); Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), specifically Tickets 2, 3, 7, and 8; the two original findings in [Final Independent Review](ask-then-do-it-1.3.0-final-review.md); the current raw working-tree diff and relevant surrounding source; canonical and packaged Codex orchestrator Skills; `scripts/build_release.py`; `tests/codex/test_lite_workflow.py`; `tests/generic/test_generic_lite_workflow.py`; `tests/release/test_generic_release.py`; `tests/release/test_workflow_token_proxy.py`; the deterministic proxy source and fixture; current `dist/` directories, archives, and checksums; and independently observed verification results.

Approved implementation mode: `tdd` for Tickets 2, 3, 7, and 8.

Independence: This fresh reviewer did not implement either correction. Correction implementation evidence and implementer conclusions were not opened or used. An interpreter-location search after `python` was unavailable on `PATH` incidentally returned two command-only matches from a correction-evidence filename; those snippets exposed no rationale, verdict, or result beyond the raw orientation supplied in the review handoff. Every conclusion below was independently derived from the approved artifacts, current source, tests, generated packages, checksums, and fresh reruns.

## Findings

No actionable findings.

The original P1 and P2 are resolved in the current candidate. The reviewed corrections are consistent with the Approved Specification and Tickets, are covered at canonical and packaged boundaries, and do not introduce a new blocking correctness, security, compatibility, packaging, or maintenance defect.

## Correction Verdict

### P1 - Codex implicit discovery and the legacy small-change path

`resolved`. The canonical Skill frontmatter now applies the orchestrator to every software-changing operation and explicitly includes trivial or fully specified fixes, formatting-only edits, and single-line changes. The only implicit exclusion is for trivial non-software questions or answers. Mode resolution therefore precedes stage selection for the triggering request classes.

The downstream decision section is expressly limited to the resolved Full mode. Its legacy lightweight path is named an explicitly resolved-Full subpath, is not a third top-level mode, and cannot apply after Lite is selected. The canonical Skill, unpacked Codex package, and Codex ZIP entry are byte-identical. The focused regression parses the actual frontmatter and verifies both the discovery classes and the resolved-Full boundaries.

Tightest evidence: `adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md:3`, `:67`, and `:69`; `tests/codex/test_lite_workflow.py:76`; packaged copies at the corresponding Skill path under `dist/codex/` and inside `dist/codex/ask-then-do-it-1.3.0.zip`.

### P2 - Generic default declaration edit permission

`resolved`. The Generic composer now begins the generated workflow with an instruction that permits editing only the `Default workflow mode` declaration below it. The declaration remains unique and early. The former unqualified `GENERATED FILE - DO NOT EDIT` workflow banner is absent from the in-memory composition and current packaged workflow. The separate generated `manifest.yaml` prohibition is scoped to that different file and does not conflict with editing `generic-workflow.md`.

Source-level, current-package, isolated-build, and ZIP-equivalence checks cover this behavior. The unpacked Generic workflow and its ZIP entry are byte-identical, and the Generic archive checksum matches `dist/checksums.sha256`.

Tightest evidence: `scripts/build_release.py:570`, `:572`, and `:579`; `tests/generic/test_generic_lite_workflow.py:60`; `tests/release/test_generic_release.py:65`; `dist/generic/ask-then-do-it-generic-1.3.0/generic-workflow.md:1` and `:8`.

## Twelve Architecture and Refactoring Lenses

| Lens | Outcome | Correction-scope evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `no-finding` | The Codex rule has one canonical Skill owner and the Generic banner has one builder owner. `dist/` and ZIP copies are generated projections, while source/package tests intentionally guard different delivery boundaries. No contradictory duplicate policy remains. |
| 2. Long Function | `no-finding` | `compose_generic_workflow` remains a linear, cohesive composition routine; the correction changes only its owned header contract. The Skill correction is a small metadata and routing-boundary change. |
| 3. Large Module or Class | `no-finding` | `build_release.py` is broad, as already known before these corrections, but the reviewed edit adds no new responsibility outside Generic composition. No correction defect is triggered by module size. |
| 4. Long Parameter List | `no-finding` | No interface changed its parameter list. `compose_generic_workflow(config, source)` remains a two-input operation. |
| 5. Data Clumps | `no-finding` | The corrections introduce no loose group of values passed repeatedly across interfaces. Mode semantics stay in the Skill declaration or composed header. |
| 6. Primitive Obsession | `no-finding` | Exact `full`/`lite` and banner strings are the approved user-visible text contract, not unconstrained substitute domain types. Existing parsing and negative tests retain the two-value boundary. |
| 7. Feature Envy | `no-finding` | Discovery behavior remains owned by the orchestrator Skill, and generated-header behavior remains owned by the release composer. Neither correction reaches through another module's internals. |
| 8. Divergent Change | `no-finding` | Each correction changes the owner for its stated reason: Codex dispatch metadata/routing or Generic composition. The builder's pre-existing release responsibilities were not expanded. |
| 9. Shotgun Surgery | `no-finding` | Canonical edits flow mechanically into package directories and archives through the builder. Additional test assertions verify source, generated, and archive boundaries rather than duplicating runtime ownership. |
| 10. Message Chains | `not-applicable` | The reviewed behavior uses declarative Skill discovery, direct composition, file copies, and ZIP entries; it has no object-navigation or call-message chain to assess. |
| 11. Leaky Abstraction | `no-finding` | P1 no longer requires callers to know that the resolver Skill must be named for small software changes. P2 no longer requires users to disregard a contradictory generated-file instruction. |
| 12. Shallow Module | `no-finding` | The orchestrator metadata now matches its mode-resolution interface, and the composer hides deterministic header/module/encoding assembly behind one operation. No correction-facing interface promises more than its implementation provides. |

The original Review's already-tracked systemic architecture observations are not new correction findings and receive no refactor authority from this report. Nothing in this focused pass requires a new `$improve-architecture` route; Ticket 8 retains its separately approved release-milestone architecture closure.

## Verification Performed

- Focused correction regressions: `4/4` passed. This covered Codex implicit discovery, Generic in-memory edit permission, current packaged edit permission, and a fresh isolated Generic package build.
- Combined named correction surfaces: `44/44` passed across `test_lite_workflow`, `test_generic_lite_workflow`, `test_generic_release`, and `test_workflow_token_proxy`.
- Codex discovery: `24/24` passed.
- Generic discovery: `33/33` passed.
- Release discovery: `105/105` passed in `13.242s` after exposing the repository's existing bundled Pillow site-packages through `PYTHONPATH`.
- Deterministic proxy module: `19/19` passed independently.
- Direct proxy execution observed Full `13,828`, Lite `5,416`, difference `8,412`, and reduction `60.83%` (`6,083` basis points). `MINIMUM_REDUCTION_BASIS_POINTS` remains fixed at `6,000`; the negative threshold test still fails a `59.99%` reduction. The exact expectation `(13828, 5416, 8412, 6083)` matches current source-derived output, so the correction did not weaken the required `>=60%` gate.
- Canonical and packaged Skill validation: `18/18` passed. Canonical and packaged Plugin validation: `2/2` passed.
- Direct artifact parity: canonical Codex Skill equals unpacked package bytes; unpacked Codex Skill equals ZIP entry bytes; unpacked Generic workflow equals ZIP entry bytes.
- Direct SHA-256 verification matched `dist/checksums.sha256`: Codex `f4448e20e2654ed5837cbddd5d0713c79b933a1410f4d13e91ac2ef84a775995`; Generic `b399c9de509acf65d2ed277ed9d86d29926fd756947b1dff68c434f5ffa059c1`.
- `git diff --check` exited `0`; its only output was informational LF-to-CRLF working-copy warnings.

Two environment attempts are not counted as product failures. Bare `python` was unavailable on this PowerShell `PATH`, so the workspace `.venv` interpreter was used. The first release discovery with that interpreter ran 103 tests but could not import `PIL`, preventing two asset tests from loading; the complete rerun with the existing bundled Pillow dependency passed `105/105`.

## Evidence Unavailable and Residual Risk

- Live installed-Plugin discovery was not executed. The correction is proven at the normative Skill frontmatter, packaged directory, and ZIP boundaries, but actual host/model dispatch adherence remains an external integration risk.
- Live third-party Generic model behavior and an interactive user edit were not exercised. Static composition, isolated build, current package, ZIP parity, and semantic tests cover the shipped instruction contract.
- Correction Red chronology was intentionally not reviewed to preserve the requested isolation. The Approved `tdd` modes were retained and the complete current Green behavior was independently rerun.
- External CI, additional operating systems, installed marketplace behavior, publication URLs, Git tag, push, GitHub Release, upload, installation, and announcement remain unverified and unauthorized.
- Sustained concurrent Windows build stress was not exercised. All review builds and release checks were run serially; the complete serial release suite passed.

## Assumptions and Deferred Work

Assumptions: Codex Skill discovery consumes the shipped frontmatter description as its applicability contract; `dist/` is generated from canonical source and is nevertheless a required release surface; the current working tree is the correction candidate; the approved phrase "for each operation" includes the software-changing request classes named in P1; and a prohibition in generated `manifest.yaml` governs only that file, not the separately editable `generic-workflow.md` declaration.

Deferred: Any correction-evidence or release-ledger status rewrite; external integration and publication checks; additional operating-system coverage; live host/model adherence; concurrency stress; and implementation of any pre-existing Draft architecture proposal.

## Completion Assessment and Handoff

The approved corrections to P1 and P2 appear complete under their `tdd` modes. The original blockers no longer prevent acceptance criteria 1, 2, 4, and 5 at the reviewed dispatch and configuration boundaries, and Ticket 7 package projections are internally consistent. No source, test, config, or `dist/` correction is requested.

Handoff: Ticket 8 may consume this blocker-free independent correction Review, complete its approved validation-ledger and release-evidence updates from actual observations, perform or confirm the separately required release-milestone architecture closure, and then make the final local release-completion decision. External publication remains out of scope and unauthorized.
