# Ticket 4 Review After Fixes

Artifact type: Review Report

Artifact ID: `lite-workflow-mode-1-3-ticket-4-review-after-fixes`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0` (Review workflow)

Product Core version: `1.2.0`

Ticket mode: `tdd`

Status: Changes requested

Review label: `independent`

Independence basis: This reviewer did not implement Ticket 4 and reviewed only the approved Specification, the approved Ticket 4 plan, the six final documentation files, the documentation tests, the relevant diff against `HEAD`, and raw verification output. Implementer evidence and prior Review conclusions were deliberately not read.

## Findings

### P2 - The completion-budget safety exception is incomplete and differs across languages

Trigger: a Lite completion has a blocker, missing evidence, or unresolved Review finding whose honest disclosure does not fit the approximate 500-token target. The English guide expressly permits only failures or security concerns to exceed the target, the Japanese guide says only failures and security concerns must not be hidden, and the Traditional Chinese guide additionally permits missing evidence to exceed the target. None of the three expressly protects blockers and unresolved findings as over-budget exceptions. This conflicts with Required Behavior 11, which says the target must not suppress failures, blockers, security concerns, missing evidence, or unresolved Review findings, and it leaves different readers with different safety boundaries. Align all three completion paragraphs on the complete exception set. Evidence: `docs/guides/getting-started-simple.en.md:59`, `docs/guides/getting-started-simple.zh-TW.md:59`, and `docs/guides/getting-started-simple.ja.md:59`.

### P2 - The new semantic tests can pass materially incorrect guide behavior

Trigger: a translation swaps project and user Config precedence, removes most high-risk categories, drops unmarked steps from a numbered flow, or retains the 500-token phrase while weakening its non-suppression rule. The test checks the order of section headings, verifies only that one numbered item exists in each flow, and searches for global marker strings without asserting their behavioral order; the risk check covers only authentication/authorization and destructive operations. The current 17-test run therefore passes despite the completion-budget mismatch above, and would also pass several central precedence and risk omissions. This weakens the Ticket's TDD purpose of preventing translation drift and accidental omission. Add section-scoped, ordered expectations for the four precedence levels, exact Full/Lite flow structure, the complete material-risk set, and the complete completion-budget exception. Evidence: `tests/release/test_documentation.py:362`, especially the assertions at `tests/release/test_documentation.py:485-509`.

## Verification

- Read the complete approved Specification and the complete Ticket 4 plan section; retained the approved `tdd` mode.
- Read all six changed canonical guide/design documents and the complete `tests/release/test_documentation.py`.
- Inspected the seven-file Ticket 4 diff against `HEAD`; the relevant diff is limited to the six owned documents and focused documentation tests. Unrelated dirty-worktree files were not attributed to this Ticket.
- Ran `.\.venv\Scripts\python.exe -B -m unittest tests.release.test_documentation -v`: 17 tests ran and all passed.
- Ran `git diff --check` for the seven reviewed files: no whitespace errors; Git reported only expected LF-to-CRLF working-copy warnings.
- Checked repository-relative links through the passing documentation suite.

Evidence unavailable: no native-rendered Markdown visual inspection or external destination-content check was performed. No implementer Red/Green/Refactor narrative or earlier Review report was read, by design, so this assessment relies on final artifacts and raw current verification only.

## Scope And Acceptance Assessment

- The six document changes stay within Ticket 4 ownership; no README, START-HERE, Config example, generated package, or release-measurement change is part of the reviewed Ticket diff.
- The guides otherwise provide the required precedence section, comparison table, numbered Full and Lite flows, 500/800/500 budgets, high-risk switching before and during implementation, minimum validation, correction approval, completion fields, and new-session behavior.
- The design guides otherwise align Core, Codex, and Generic ownership, host-capability honesty, Lite's lower traceability, equivalent observable outcomes, and the deterministic 60% token-proxy contract.
- Ticket 4 does not yet appear complete because the canonical completion rule is not fully equivalent and the TDD coverage does not reliably reject important semantic regressions.

## Twelve Architecture And Refactoring Lenses

1. **Duplicated Code or Policy — finding.** The required three-language duplication has drifted at the completion-budget exception; Finding 1 identifies the trigger, impact, evidence, and locations.
2. **Long Function — no-finding.** The large localized-flow test is mostly one cohesive data table followed by a single uniform assertion loop; its length did not itself create a separate actionable defect.
3. **Large Module or Class — no-finding.** `ReleaseDocumentationTests` remains cohesive around release-document contracts, and the Ticket adds no unrelated responsibility.
4. **Long Parameter List — not-applicable.** Ticket 4 changes documentation and data-driven assertions, not a callable interface with a changed parameter list.
5. **Data Clumps — no-finding.** Per-locale headings and markers are intentionally grouped into one locale record and consumed together; no repeated loose value bundle crosses interfaces.
6. **Primitive Obsession — finding.** Bare substring markers stand in for ordered semantic contracts and allow central behavior to regress while tests pass; Finding 2 records the concrete cases and impact.
7. **Feature Envy — not-applicable.** No changed object behavior reaches into another object's state or responsibility.
8. **Divergent Change — no-finding.** The changed test module has one documentation-conformance reason to change, and the six documents retain their approved guide/design ownership split.
9. **Shotgun Surgery — no-finding.** Updating three localized copies is an explicit localization contract; the shared locale maps keep verification in one test location, and no additional unrelated consumer requires edits.
10. **Message Chains — not-applicable.** The changed code performs direct `Path` reads and local dictionary lookup, with no navigation or call chain exposing internal structure.
11. **Leaky Abstraction — finding.** The tests expose exact prose fragments while failing to encode the underlying ordering and safety semantics, forcing wording stability without guaranteeing behavioral stability; this is the test-contract defect in Finding 2.
12. **Shallow Module — not-applicable.** Ticket 4 introduces no new production module or public abstraction whose interface depth can be evaluated.

## Residual Risk And Untested Areas

Exact-string tests remain sensitive to harmless editorial changes while under-detecting semantic inversions and omissions. Markdown rendering and native-speaker editorial quality were not separately automated. Package-local copies, README/START-HERE routing, generated packages, and measured token-proxy release evidence are explicitly outside Ticket 4 and remain for their owning Tickets.

## Handoff

Return Findings 1 and 2 to the Ticket 4 implementer. After the three completion paragraphs and focused semantic assertions are corrected under the approved `tdd` Ticket, rerun the documentation suite and submit the final artifacts for another independent Review.
