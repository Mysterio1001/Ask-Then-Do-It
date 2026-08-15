# Lite Workflow Mode 1.3.0 Ticket 4 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `lite-workflow-mode-1-3-ticket-4-evidence`

Workflow ID: `lite-workflow-mode`

Core version: `1.2.0`

Target release version: `1.3.0`

Status: Completed

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), completed [Ticket 1 implementation evidence](lite-workflow-mode-1.3.0-ticket-1.md) and accepted Review, Ticket 4 in approved `tdd` mode, three approved P2 Review corrections covering clean Review behavior, broad high-risk categories, and token-proxy inputs, and two subsequently approved P2 corrections from [Ticket 4 Review After Fixes](lite-workflow-mode-1.3.0-ticket-4-review-after-fixes.md).

Assumptions: Ticket 1 established the provider-neutral Full/Lite contract. Ticket 4 owns only the localized canonical beginner and design guides plus focused documentation tests; host-specific Config guides, short entry pages, README, runtime behavior, version declarations, generated output, and token-proxy implementation remain separately owned.

Deferred: Independent Review; Codex and Generic host documentation; README and START-HERE changes; executable token-proxy measurement; `1.3.0` version and package integration; generated `dist/`; external publication.

Handoff: `$review-code` with the approved artifacts, the six localized guide/design files, focused documentation-test diff, this evidence, and the raw results below. No Ticket 4 Review was performed during implementation.

## Outcome

- Made the Traditional Chinese, English, and Japanese beginner guides the canonical complete Full/Lite flow reference.
- Documented Codex and Generic mode precedence without duplicating host-specific Config paths or examples.
- Added a mode comparison and separate numbered Full and Lite flows, including Full's one-question sequence and three approvals.
- Documented Lite's maximum three blocking questions, approximate 500/800/500-token budgets, single approval, no workflow artifacts or new tests, minimum static plus success/failure-path validation, findings-batch correction authority, completion behavior, high-risk current-operation switch, and session reset.
- Clarified that zero actionable Lite Review findings are reported explicitly without creating an empty correction gate.
- Preserved authentication/authorization and destructive data operations as broad high-risk categories in every locale.
- Aligned the three Lite completion-budget exceptions so failures, blockers, security concerns, missing or unavailable evidence, and unresolved findings may all exceed the approximate 500-token target.
- Updated all three design guides with Core/adapter ownership, equivalent observable outcomes, Lite's lower traceability, and the deterministic equivalent-scenario token-proxy contract.
- Included composed prompt content among workflow-controlled token-proxy inputs in every design guide.
- Removed the obsolete 180-line guide limit and protected the localized contracts with focused tests, including section-scoped ordering, exact numbered-flow structure, all material-risk categories, and completion exceptions.

## Files changed

- `docs/guides/getting-started-simple.zh-TW.md`
- `docs/guides/getting-started-simple.en.md`
- `docs/guides/getting-started-simple.ja.md`
- `docs/design/ai-development-skills.zh-TW.md`
- `docs/design/ai-development-skills.en.md`
- `docs/design/ai-development-skills.ja.md`
- `tests/release/test_documentation.py`
- `docs/evidence/lite-workflow-mode-1.3.0-ticket-4.md`

No README, Codex or Generic host guide, START-HERE file, runtime prompt or Skill, Core file, release configuration, version declaration, generated output, package, checksum, or Ticket Plan was changed by Ticket 4.

## TDD evidence

### Valid Red

Both focused localized-contract tests were added before any of the six documentation implementation files changed.

Command:

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation.ReleaseDocumentationTests.test_localized_simple_guides_define_complete_full_and_lite_flows tests.release.test_documentation.ReleaseDocumentationTests.test_localized_design_guides_define_ownership_and_token_proxy
```

Observed result before documentation implementation:

```text
EFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
Ran 2 tests in 0.004s
FAILED (failures=33, errors=1)
```

The error was a missing required localized mode-section heading, and every failure was a missing approved Full/Lite flow or design-contract marker. The tests imported and executed normally; there was no setup, dependency, or unrelated failure.

### Focused Green

Command:

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation.ReleaseDocumentationTests.test_localized_simple_guides_define_complete_full_and_lite_flows tests.release.test_documentation.ReleaseDocumentationTests.test_localized_design_guides_define_ownership_and_token_proxy
```

Observed result after updating the six canonical files:

```text
..
Ran 2 tests in 0.002s
OK
```

### Post-refactor focused verification

After removing the six extra EOF blank lines reported by `git diff --check`, the same focused command was rerun.

```text
..
Ran 2 tests in 0.001s
OK
```

## Broader documentation verification

### First broader run

Command:

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation
```

Observed result:

```text
...............F
Ran 16 tests in 2.008s
FAILED (failures=1)
```

The only failure was the older Traditional Chinese plain-language compatibility check looking for the exact phrase `一次問一題`. The Full section already stated the approved equivalent `一次只問一個需求問題`; it was updated to include the old plain-language phrase explicitly inside Full, without applying the rule to Lite.

### Final broader run

Command:

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation
```

Observed result:

```text
................
Ran 16 tests in 0.099s
OK
```

This suite includes all-localized-document presence, internal-material exclusions, semantic markers, existing command preservation, and relative-link resolution.

### Scoped whitespace check

Command:

```text
git diff --check -- tests/release/test_documentation.py docs/guides/getting-started-simple.zh-TW.md docs/guides/getting-started-simple.en.md docs/guides/getting-started-simple.ja.md docs/design/ai-development-skills.zh-TW.md docs/design/ai-development-skills.en.md docs/design/ai-development-skills.ja.md
```

Observed result:

```text
Exit code: 0
No whitespace errors. Git emitted only expected LF-to-CRLF working-copy warnings on Windows.
```

## Approved Review correction TDD evidence

The correction tests were changed before the six owned documentation files. They added or strengthened these assertions:

- Every localized Lite guide explicitly reports zero actionable findings and skips an empty correction approval gate.
- Every localized high-risk section preserves broad authentication/authorization and destructive-data-operation categories.
- Every localized design guide counts composed prompt content as workflow-controlled proxy input.

### Correction Red

Command:

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation.ReleaseDocumentationTests.test_localized_simple_guides_define_complete_full_and_lite_flows tests.release.test_documentation.ReleaseDocumentationTests.test_localized_simple_guides_skip_empty_correction_gate_when_review_is_clean tests.release.test_documentation.ReleaseDocumentationTests.test_localized_design_guides_define_ownership_and_token_proxy
```

Observed result before correcting the documentation:

```text
FFFFFFFFFF
Ran 3 tests in 0.006s
FAILED (failures=10)
```

The ten failures were exactly the approved omissions: four broad-category markers missing from Traditional Chinese and Japanese, three clean-Review statements missing across all locales, and three composed-prompt markers missing across all design guides. Test collection and execution succeeded with no setup or unrelated failure.

### Correction focused Green

The same focused command was rerun after the minimum six-file prose correction.

```text
...
Ran 3 tests in 0.002s
OK
```

### Correction broader verification

Commands and observed results:

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation

.................
Ran 17 tests in 0.110s
OK
```

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation.ReleaseDocumentationTests.test_all_relative_document_links_resolve

.
Ran 1 test in 0.046s
OK
```

Both the Ticket 4-scoped `git diff --check` command and repository-wide `git diff --check` exited `0`. They reported no whitespace errors and only expected LF-to-CRLF working-copy warnings on Windows. Other agents' concurrent files were preserved.

## Second approved Review correction TDD evidence

The second correction round strengthened the tests before changing documentation. The new contract reads only the relevant Markdown sections and verifies:

- exactly four ordered Codex precedence levels: current-operation instruction, project Config, user Config, and Full fallback;
- exactly eight ordered, localized Full steps and eight ordered, localized Lite steps;
- all material risk categories inside the high-risk section: authentication, authorization, payment, migration, destructive data operation, public contract, cross-module structure, concurrency, asynchronous behavior, and external side effects;
- the approximate 500-token completion target and every non-suppression exception inside Lite step 8.

### Test assertion attempt not accepted as Red

The first run found the intended omissions but also treated English sentence-initial `Failures` as missing because the test expected lowercase `failures`.

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation.ReleaseDocumentationTests.test_localized_simple_guides_keep_section_scoped_workflow_contracts

FFFFFFF
Ran 1 test in 0.002s
FAILED (failures=7)
```

This run was not accepted as Red. The assertion case was corrected before any documentation change.

### Valid second correction Red

Command:

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation.ReleaseDocumentationTests.test_localized_simple_guides_keep_section_scoped_workflow_contracts
```

Observed result:

```text
FFFFFF
Ran 1 test in 0.003s
FAILED (failures=6)
```

The ordered precedence, exact Full/Lite flow structure, complete risk categories, existing failure/security exception, and unresolved-finding disclosure all passed. The six failures were exactly two omissions per locale: blockers and missing or unavailable evidence were not explicitly protected as reasons to exceed the completion target.

### Second correction focused Green

After changing only Lite step 8 in the three simple guides, the same command produced:

```text
.
Ran 1 test in 0.001s
OK
```

The complete Ticket 4 focused set then produced:

```text
....
Ran 4 tests in 0.003s
OK
```

### Second correction broader verification

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation

..................
Ran 18 tests in 0.141s
OK
```

```text
.venv\Scripts\python.exe -m unittest tests.release.test_documentation.ReleaseDocumentationTests.test_all_relative_document_links_resolve

.
Ran 1 test in 0.063s
OK
```

The Ticket 4-scoped and repository-wide `git diff --check` commands both exited `0`, with no whitespace errors and only expected LF-to-CRLF working-copy warnings.

## Scope inspection

- The final Ticket 4 implementation diff contains the six owned localized files and `tests/release/test_documentation.py`; this evidence is the only additional Ticket 4 file.
- Search results place all one-question and three-approval statements inside Full sections in every localized guide/design document.
- No separate Lite guide was added.
- Concurrent Ticket 2 and Ticket 3 changes were preserved and not included in Ticket 4 claims.

## Residual risks

- The tests use required localized semantic markers and structural sections, but cannot prove that every future prose edit preserves perfect translation nuance.
- The clean-Review test proves the canonical instruction is present; actual model adherence still depends on the consuming host following the workflow.
- The design documents specify the 60% deterministic token-proxy contract; Ticket 4 does not implement or measure that proxy. Ticket 6 owns executable proof.
- Host-specific mode configuration instructions and README/entry-page routing remain incomplete until Ticket 5.
- Independent Review remains required before accepting Ticket 4 as reviewed.
