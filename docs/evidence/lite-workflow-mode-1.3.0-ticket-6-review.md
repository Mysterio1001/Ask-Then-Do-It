# Ticket 6 Independent Review Report

Artifact type: Review Report

Artifact ID: `lite-workflow-mode-1-3-ticket-6-review`

Workflow ID: `lite-workflow-mode`

Review workflow core version: `1.1.0`

Product Core version: `1.2.0`

Implementation mode: `tdd`

Status: Changes requested

Review label: `independent`

Inputs: Approved `docs/specs/lite-workflow-mode-1.3.0.md`; Approved Ticket 6 in `docs/plans/lite-workflow-mode-1.3.0.md`; final `scripts/measure_workflow_token_proxy.py`; `tests/release/test_workflow_token_proxy.py`; `tests/release/fixtures/workflow-token-proxy/**`; `scripts/build_release.py::compose_generic_workflow`; relevant Codex Skills, Lite reference, Generic prompt modules, release configuration, and raw commands run by this reviewer.

Assumptions: The reviewed working tree is the intended Ticket 6 revision. Ticket 7 owns final release inventories, versions, required-check registration, packages, and checksums; Ticket 8 owns integrated validation and release evidence. Those later-Ticket responsibilities are not treated as Ticket 6 defects.

Deferred: Full repository test discovery, external CI, Ticket 7 package integration, and Ticket 8 evidence-gate validation. Implementation Evidence and implementer conclusions were intentionally not read to preserve independent review.

Handoff: Return the two findings to Ticket 6 implementation. After fixes and focused verification, provide the raw final artifacts and results to a fresh independent `$review-code` context before Ticket 7.

## Findings

### P1 - The fixed benchmark does not bind output events to their fixture sources

Trigger: change any non-instruction event's `source` to another existing UTF-8 repository file while retaining the expected event ID, category, and budget. `resolve_relative_path` accepts the replacement, while `measure_modes` fixes event IDs and only checks source paths for `selected-instructions`; the Full and Lite output-source inventory is therefore not fixed. An in-memory mutation first enlarged only Lite's unbudgeted outputs and correctly failed at Full `13768` versus Lite `26342`, then redirected every Full output event to the same large generated prompt; the unchanged schema accepted the asymmetric repetition and the gate changed to a false pass at Full `68384`, Lite `26342`, and `6147` basis points. This defeats the Ticket's durable protection against fixture gaming and can let a release claim 60% reduction using unrelated or duplicated Full material. Bind every event ID to its exact mode, category, canonical source path, and budget, reject duplicate/replayed output sources where the fixed scenario does not require them, and add source-redirection mutations for both modes. Evidence: `scripts/measure_workflow_token_proxy.py:324`, `scripts/measure_workflow_token_proxy.py:368`, `scripts/measure_workflow_token_proxy.py:378`, and `tests/release/test_workflow_token_proxy.py:125`.

### P2 - Failed comparisons can disclose the wrong negative percentage

Trigger: make Lite larger than Full. The gate remains correctly false, but `reduction_basis_points` is negative and the percentage string combines floor division with the absolute remainder. For example, `-1` basis point renders as `-1.01%`, `-101` as `-2.01%`, and `-6109` as `-62.09%` instead of `-0.01%`, `-1.01%`, and `-61.09%`. This makes the required disclosed result inaccurate precisely on a failure path and is not covered by the current growth mutation, which remains a positive reduction below 60%. Format the sign separately from the absolute basis-point magnitude and add a mutation where Lite exceeds Full. Evidence: `scripts/measure_workflow_token_proxy.py:553` and `scripts/measure_workflow_token_proxy.py:582`.

## Acceptance and correctness review

The current checked-in representative fixture describes the same low-risk, tools-capable Codex template-filter task in both modes. Full includes the selected orchestrator, documented-requirements, Specification, Ticket Planning, TDD implementation, independent Review instructions, two requirement questions, Draft Working Notes, Requirement Decision Record, Knowledge Base change, Specification, one-Ticket Plan, every approval/implementation/Review handoff, Implementation Evidence, twelve-lens Review Report, and completion. Those are required by the selected existing-system Full route; no gratuitous architecture diagnosis, extra Ticket, review finding, or unrelated task was added.

Lite includes the same two decisions and delivered behavior through its orchestrator and complete Lite reference, blocking questions, Change Brief, single approval handoff, implementation/validation summary, compact non-independent Review, and completion. It does not omit a required Lite lifecycle output or add a forbidden durable workflow artifact. The fixture's shared exclusions are exactly task-specific source code, necessary tool output, and hidden reasoning, and scenario facts are outside both measured mode streams.

The normalized proxy is deterministic: NFC normalization, Unicode whitespace collapse, ordered LF joining, UTF-8 byte count, and integer ceiling by four bytes. The release gate uses the exact integer comparison `lite * 100 <= full * 40`; the passing fixture reports Full `13768`, Lite `5356`, a difference of `8412`, and `6109` basis points (`61.09%`). Lite's measured question, Change Brief, and completion outputs are `117/500`, `405/800`, and `112/500` proxy tokens. Strict top-level and nested key sets, fixed categories and event IDs, repository-relative POSIX paths, traversal/absolute/missing-file rejection, and UTF-8 decoding are present, subject to P1's missing event-to-source binding.

Generic is reported separately with `gate_applied: false`. The measurement calls the actual `compose_generic_workflow`, counts its generated header, editable default declaration, routing/capability text, all begin/end source boundaries, bootstrap, orchestration, Lite, and remaining Full modules, and hashes the exact returned bytes. It reports a fixed cost of `13313` proxy tokens applying equally to Full and Lite, with explicit statements that there is no Generic 60% guarantee and no billing guarantee. Replacing the release-config module list only for this prospective composition is a bounded Ticket 7 interface; Ticket 6 does not mutate the Ticket 7-owned inventory.

## Verification

- `.venv/Scripts/python.exe -m unittest tests.release.test_workflow_token_proxy -v`: 14 tests passed.
- `.venv/Scripts/python.exe scripts/measure_workflow_token_proxy.py`: exit 0; Full `13768`, Lite `5356`, reduction `61.09%`, Generic fixed cost `13313`.
- `.venv/Scripts/python.exe scripts/measure_workflow_token_proxy.py --json`: exit 0; deterministic structured report and the same counts.
- `.venv/Scripts/python.exe -m unittest tests.generic.test_generic_prompts -v`: 17 tests passed.
- Read-only in-memory mutations confirmed that Lite growth below the gate fails, subsequent Full source inflation can incorrectly restore a pass, and negative basis-point formatting is incorrect.

Unavailable evidence: external CI and complete repository discovery were not run. TDD chronology was not assessed because Implementation Evidence was deliberately withheld from this independent context. No source, test, fixture, Plan, or product file was modified by Review.

## Twelve-lens results

1. **Duplicated Code or Policy** - `no-finding`. The script and tests repeat expected inventories, but the executable checks remain centralized in the script and the test copy provides an independent assertion; no conflicting rule was observed.
2. **Long Function** - `no-finding`. `measure_modes` is the largest changed routine, but its ordered validation, measurement, budget, and report steps remain traceable; P1 is a missing invariant rather than size-caused ambiguity.
3. **Large Module or Class** - `no-finding`. The standard-library script owns one cohesive benchmark boundary: fixture validation, Codex measurement, Generic fixed-cost composition, and reporting.
4. **Long Parameter List** - `no-finding`. Changed functions take at most a small fixture/path/context set; no unstable coordination interface was introduced.
5. **Data Clumps** - `finding`. P1 shows that event ID, mode, category, source, and budget form one fixed benchmark identity but are validated as partially independent primitives, allowing source substitution without invalidating the event.
6. **Primitive Obsession** - `finding`. P2 arises because a signed percentage is assembled from raw integer division and remainder without a sign-safe percentage representation.
7. **Feature Envy** - `no-finding`. Generic measurement appropriately delegates composition to `build_release.compose_generic_workflow` rather than reproducing builder internals.
8. **Divergent Change** - `no-finding`. The measurement module changes for one benchmark/reporting policy, while package construction remains in the release builder.
9. **Shotgun Surgery** - `no-finding`. The canonical composition function and structured fixture keep behavioral changes localized; Ticket 7's later inventory registration is an approved integration boundary, not current scattered ownership.
10. **Message Chains** - `not-applicable`. The change is procedural file/structure validation and has no object-navigation or call-chain coupling of the kind this lens targets.
11. **Leaky Abstraction** - `finding`. P1 requires fixture authors and reviewers to know that an expected event ID does not imply its canonical source, although the fixed-inventory interface suggests that it does.
12. **Shallow Module** - `no-finding`. The CLI hides normalization, validation, arithmetic, builder composition, hashing, and deterministic reporting behind a small invocation interface; its depth is justified despite the two local defects.

## Residual risk and completion assessment

The present fixture content appears fair and complete by manual inspection, and all requested focused checks pass. Exact 60.00% boundary behavior is clear from the integer gate but lacks a dedicated boundary mutation; Generic fixed-cost behavior is covered without a Generic reduction claim. The mutable source inventory and incorrect negative disclosure remain actionable. Ticket 6 does not appear complete until both findings are corrected and independently re-reviewed.
