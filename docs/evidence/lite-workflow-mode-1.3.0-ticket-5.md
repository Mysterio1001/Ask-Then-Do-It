# Lite Workflow Mode 1.3.0 Ticket 5 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `lite-workflow-mode-1-3-ticket-5-evidence`

Workflow ID: `lite-workflow-mode`

Workflow core version: `1.1.0`

Repository baseline core version: `1.2.0`

Target release version: `1.3.0`

Status: Completed

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), completed Tickets 2-4 and their final Reviews, Ticket 5 in approved `tdd` mode, the user-approved P2 correction from the [Ticket 5 Independent Review](lite-workflow-mode-1.3.0-ticket-5-review.md), and the two user-approved P2 corrections from the [Ticket 5 Closure Review](lite-workflow-mode-1.3.0-ticket-5-review-closure.md).

Assumptions: Ticket 5 consumes settled Codex, Generic, and canonical Full/Lite contracts. It owns only the localized host guides, nine short START-HERE sources, bounded README changes, focused documentation tests, and this evidence. The current public download version remains `1.2.0` until Ticket 7 performs lockstep release integration.

Deferred: Fresh independent after-fixes Review; release inventory and version integration; `release/release.json`; generated `dist/`; archives and checksums; external publication. The broader-suite exclusions recorded below remain owned by Ticket 7 or the test environment.

Handoff: A fresh `$review-code` context with the Approved Specification and Ticket, the initial and closure Review findings, the final corrected diff, focused test changes, this evidence, and the raw results below. No after-fixes Review was performed during either correction implementation.

## Outcome

- Added complete Codex Config instructions in all three host guides: both TOML paths, valid and invalid examples, explicit/project/user/fallback precedence, absent-versus-invalid behavior, read-only resolution, operation scope, session reset, and the high-risk handoff.
- Added complete Generic declaration instructions in all three host guides: exact Full/Lite declarations, explicit/declaration/fallback precedence, missing or unsupported fallback, no Codex Config access, operation and session scope, and honest conversation-only capability limits.
- Updated the Generic host-guide inventory to eleven modules and placed `lite-workflow.md` immediately after `orchestration.md`.
- Reworked all nine START-HERE sources into concise Full/Lite handoffs while retaining practical download, install, paste, and start actions plus links to the detailed host and canonical workflow guides.
- Changed each README language section to Introduction followed by Quick Start with a concise Full/Lite summary. Automatic installation (CLI), nested Codex CLI, Manual installation, and Read more blocks remain byte-protected after release-version normalization.
- Replaced obsolete all-mode assumptions with localized semantic, ownership, link, concision, and README-boundary tests. No expected README digest was changed to accommodate the implementation.
- Corrected nine mode-enabled guides and Generic entry pages so one-question and three-approval startup claims are explicitly Full-only, while Lite clearly permits zero questions, limits blocking questions to three per round, and uses one Change Brief approval.
- Scoped Generic cross-session continuation to Full in all three locales, documented Lite's non-durable session lifecycle, and restored the three named Full approval gates in the Japanese Codex guide.

## Files changed

- `README.md`
- `START-HERE.en.md`
- `START-HERE.zh-TW.md`
- `START-HERE.ja.md`
- `adapters/codex/plugin/ask-then-do-it/START-HERE.en.md`
- `adapters/codex/plugin/ask-then-do-it/START-HERE.zh-TW.md`
- `adapters/codex/plugin/ask-then-do-it/START-HERE.ja.md`
- `release/generic/START-HERE.en.md`
- `release/generic/START-HERE.zh-TW.md`
- `release/generic/START-HERE.ja.md`
- `docs/guides/codex.en.md`
- `docs/guides/codex.zh-TW.md`
- `docs/guides/codex.ja.md`
- `docs/guides/generic.en.md`
- `docs/guides/generic.zh-TW.md`
- `docs/guides/generic.ja.md`
- `tests/release/test_documentation.py`
- `tests/release/test_command_install_docs.py`
- `docs/evidence/lite-workflow-mode-1.3.0-ticket-5.md`

No canonical simple/design guide, runtime Skill or prompt, Core file, version declaration, release configuration, builder, generated package, checksum, `dist/` output, or Ticket Plan was changed by Ticket 5.

## TDD evidence

### Valid Red

The nine focused tests were run before any of the 16 production documents changed.

Command:

```text
$env:PYTHONDONTWRITEBYTECODE='1'; .\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation.ReleaseDocumentationTests.test_all_nine_start_pages_are_concise_full_lite_handoffs tests.release.test_documentation.ReleaseDocumentationTests.test_detailed_full_guides_keep_plain_language_ticket_test_choices tests.release.test_documentation.ReleaseDocumentationTests.test_readme_uses_approved_localized_introduction_and_quick_start_order tests.release.test_documentation.ReleaseDocumentationTests.test_localized_codex_guides_document_mode_config_contract tests.release.test_documentation.ReleaseDocumentationTests.test_localized_generic_guides_document_embedded_mode_contract tests.release.test_documentation.ReleaseDocumentationTests.test_mode_configuration_stays_in_host_guides tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_start_pages_handoff_to_the_detailed_command_contract tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_readme_preserved_blocks_are_independent_of_git_head tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_readme_keeps_install_heading_order_and_single_sections
```

Observed result:

```text
test_all_nine_start_pages_are_concise_full_lite_handoffs ... FAIL
test_detailed_full_guides_keep_plain_language_ticket_test_choices ... ok
test_readme_uses_approved_localized_introduction_and_quick_start_order ... FAIL
test_localized_codex_guides_document_mode_config_contract ... FAIL
test_localized_generic_guides_document_embedded_mode_contract ... FAIL
test_mode_configuration_stays_in_host_guides ... ok
test_start_pages_handoff_to_the_detailed_command_contract ... FAIL (3 localized subtests)
test_readme_preserved_blocks_are_independent_of_git_head ... FAIL
test_readme_keeps_install_heading_order_and_single_sections ... FAIL

Ran 9 tests in 0.008s
FAILED (failures=9)
```

Every failure was an expected missing-documentation behavior: absent Full/Lite handoffs, host configuration contracts, package-guide links, or localized README headings. The two controls passed, proving that detailed Full test-choice wording and host ownership exclusions were already intact.

### Focused Green

The same command was rerun after the 16 production documents and the section-scoped README test refactor.

```text
test_all_nine_start_pages_are_concise_full_lite_handoffs ... ok
test_detailed_full_guides_keep_plain_language_ticket_test_choices ... ok
test_readme_uses_approved_localized_introduction_and_quick_start_order ... ok
test_localized_codex_guides_document_mode_config_contract ... ok
test_localized_generic_guides_document_embedded_mode_contract ... ok
test_mode_configuration_stays_in_host_guides ... ok
test_start_pages_handoff_to_the_detailed_command_contract ... ok
test_readme_preserved_blocks_are_independent_of_git_head ... ok
test_readme_keeps_install_heading_order_and_single_sections ... ok

Ran 9 tests in 0.009s
OK
```

### Test-scope refactor

The first README-only Green attempt exposed a test bug: the shared `#### Codex CLI` marker was looked up from the beginning of the entire README, so Chinese and Japanese ordering falsely pointed to the English marker. The preserved-block hash test already passed.

```text
Ran 3 tests in 0.003s
FAILED (failures=4)
```

The order checks were scoped to each locale section without changing required headings, counts, or preserved digest values. The rerun produced:

```text
Ran 3 tests in 0.002s
OK
```

## Broader verification

### Complete documentation modules

Commands and observed results:

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation

Ran 22 tests in 0.130s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_command_install_docs

Ran 5 tests in 0.003s
OK
```

These modules include localized parity, existing install commands, internal-material exclusions, START-HERE concision, README preserved-block digests, and relative links.

### Explicit link checks

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation.ReleaseDocumentationTests.test_all_relative_document_links_resolve tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_localized_guide_relative_links_resolve

Ran 2 tests in 0.057s
OK
```

### Settled upstream contracts

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.codex.test_lite_workflow tests.generic.test_generic_lite_workflow tests.generic.test_generic_prompts tests.release.test_workflow_token_proxy

Ran 55 tests in 2.602s
OK
```

### Full repository discovery

The first discovery run found two Ticket 5 START-HERE compatibility omissions plus two unrelated failures.

```text
.\.venv\Scripts\python.exe -B -m unittest discover -v -s tests -p 'test_*.py'

Ran 164 tests in 12.497s
FAILED (failures=3, errors=1)
```

The two owned failures required concise entry pages to retain ZIP extraction and Skill-entry information for Codex, and first-question, progress-saving, and capability-limit information for Generic. Those details were restored without adding tables, extra headings, Config details, token budgets, or Full tutorials. Their focused regression run produced:

```text
Ran 4 tests in 0.471s
OK
```

The final full-discovery run then contained only the two external conditions below:

```text
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p 'test_*.py'

Ran 164 tests in 12.149s
FAILED (failures=1, errors=1)
```

Known external conditions:

- `release.test_clean_slate.CleanSlateContractTests.test_retained_workflow_inventory_and_rules_are_unchanged` still expects the pre-Lite Generic prompt inventory and rejects Ticket 3's `lite-workflow.md`. Ticket 7 owns final inventory integration; changing that release test is outside Ticket 5.
- `release.test_plugin_assets` cannot import because Pillow is unavailable in the active `.venv`: `ModuleNotFoundError: No module named 'PIL'`. Test collection fails before Ticket 5 files are inspected.

## Approved Review P2 correction

The independent Ticket 5 Review found that six host guides and three Generic package entry pages presented Full-only startup behavior as universal. The user explicitly approved correcting that P2 finding. The correction remained limited to the nine affected documents, `tests/release/test_documentation.py`, and this evidence.

### Correction Red

Two section-scoped regression tests were added before changing the nine documents. They require Full-only one-question and three-approval statements to remain inside explicit Full context, reject stale unscoped first-question phrasing, and require Lite to state that it may ask no questions, asks at most three blocking questions per round when needed, and waits for one approval of one Change Brief.

Command:

```text
$env:PYTHONDONTWRITEBYTECODE='1'; .\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation.ReleaseDocumentationTests.test_mode_enabled_host_guides_scope_question_and_approval_contracts tests.release.test_documentation.ReleaseDocumentationTests.test_generic_start_pages_keep_full_only_startup_claims_mode_scoped
```

Observed result:

```text
Ran 2 tests in 0.005s
FAILED (failures=33)
```

All 33 failures were expected missing-behavior detections across English, Traditional Chinese, and Japanese. The Codex guides lacked Full/Lite startup subsections; the Generic guides lacked Lite sections and retained unscoped first-question text; the Generic START pages retained the same stale text and lacked the compact per-mode question and approval summary. Test collection and execution succeeded with no setup or unrelated failure.

### Correction focused Green

After the minimum nine-document correction, the same command produced:

```text
Ran 2 tests in 0.001s
OK
```

The two correction cases were then combined with the original nine Ticket 5 focused cases:

```text
$env:PYTHONDONTWRITEBYTECODE='1'; .\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation.ReleaseDocumentationTests.test_all_nine_start_pages_are_concise_full_lite_handoffs tests.release.test_documentation.ReleaseDocumentationTests.test_detailed_full_guides_keep_plain_language_ticket_test_choices tests.release.test_documentation.ReleaseDocumentationTests.test_readme_uses_approved_localized_introduction_and_quick_start_order tests.release.test_documentation.ReleaseDocumentationTests.test_localized_codex_guides_document_mode_config_contract tests.release.test_documentation.ReleaseDocumentationTests.test_localized_generic_guides_document_embedded_mode_contract tests.release.test_documentation.ReleaseDocumentationTests.test_mode_configuration_stays_in_host_guides tests.release.test_documentation.ReleaseDocumentationTests.test_mode_enabled_host_guides_scope_question_and_approval_contracts tests.release.test_documentation.ReleaseDocumentationTests.test_generic_start_pages_keep_full_only_startup_claims_mode_scoped tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_start_pages_handoff_to_the_detailed_command_contract tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_readme_preserved_blocks_are_independent_of_git_head tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_readme_keeps_install_heading_order_and_single_sections

Ran 11 tests in 0.009s
OK
```

### Correction broader verification

The first complete documentation run found one existing compatibility assertion requiring the literal Traditional Chinese phrase `第一個需求問題`. It was restored inside the explicit Full section and synchronized semantically across all three Generic guides; no universal startup claim was reintroduced.

Final commands and observed results:

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation

Ran 24 tests in 0.119s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_command_install_docs

Ran 5 tests in 0.003s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation.ReleaseDocumentationTests.test_all_relative_document_links_resolve tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_localized_guide_relative_links_resolve

Ran 2 tests in 0.056s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.codex.test_lite_workflow tests.generic.test_generic_lite_workflow tests.generic.test_generic_prompts tests.release.test_workflow_token_proxy

Ran 56 tests in 3.147s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_codex_release.CodexReleaseSourceTests.test_plugin_start_guide_explains_manual_first_use_and_all_entries tests.release.test_generic_release.GenericReleaseTests.test_builder_emits_self_contained_conversation_only_package

Ran 2 tests in 0.314s
OK
```

README and its preserved digest constants were not changed during this correction.

## Final diff checks

Commands:

```text
git diff --check -- README.md START-HERE.en.md START-HERE.zh-TW.md START-HERE.ja.md adapters/codex/plugin/ask-then-do-it/START-HERE.en.md adapters/codex/plugin/ask-then-do-it/START-HERE.zh-TW.md adapters/codex/plugin/ask-then-do-it/START-HERE.ja.md release/generic/START-HERE.en.md release/generic/START-HERE.zh-TW.md release/generic/START-HERE.ja.md docs/guides/codex.en.md docs/guides/codex.zh-TW.md docs/guides/codex.ja.md docs/guides/generic.en.md docs/guides/generic.zh-TW.md docs/guides/generic.ja.md tests/release/test_documentation.py tests/release/test_command_install_docs.py docs/evidence/lite-workflow-mode-1.3.0-ticket-5.md

git diff --check
```

Observed result for both commands:

```text
Exit code: 0
No whitespace errors. Git emitted only expected LF-to-CRLF working-copy warnings on Windows.
```

After the approved P2 correction, the correction-owned paths and the complete worktree were checked again:

```text
git diff --check -- docs/guides/codex.en.md docs/guides/codex.zh-TW.md docs/guides/codex.ja.md docs/guides/generic.en.md docs/guides/generic.zh-TW.md docs/guides/generic.ja.md release/generic/START-HERE.en.md release/generic/START-HERE.zh-TW.md release/generic/START-HERE.ja.md tests/release/test_documentation.py tests/release/test_command_install_docs.py docs/evidence/lite-workflow-mode-1.3.0-ticket-5.md

git diff --check

Exit code: 0
No whitespace errors. Git emitted only expected LF-to-CRLF working-copy warnings on Windows.
```

## Scope inspection

- The production diff is limited to the approved README, six host guides, and nine START-HERE sources.
- README preamble and all nine protected Automatic installation, Manual installation, and Read more block digests remain unchanged after the approved release-version normalization.
- START-HERE pages contain at most three level-two headings and retain practical install or start actions.
- Config paths appear only in Codex host guides; embedded Generic declarations appear only in Generic host guides.
- No separate user-facing Lite guide was added. The existing runtime `lite-workflow.md` remains owned by earlier Tickets.

## Residual risks

- Semantic-marker tests cannot prove perfect translation nuance after future prose edits.
- Generic behavior still depends on the consuming host accurately honoring its real capabilities.
- Release inventory, final versions, generated packages, and checksums remain incomplete until Ticket 7.
- Independent Review remains required before accepting Ticket 5 as reviewed.

## Closure Review Corrections

The closure Review found two remaining P2 documentation defects. Generic continuation instructions still described Full-only durable artifacts and resume behavior without mode scope, and the Japanese Codex guide stated that Full had three approval points without naming them. The user explicitly approved both corrections. This work remained limited to the three localized Generic guides, the Japanese Codex guide, `tests/release/test_documentation.py`, and this evidence.

### Closure correction valid Red

Before changing the four production documents, the existing localized host-guide test was strengthened to require the three semantic Full gate identities in every Codex locale. A new section-scoped regression test required Full durable artifacts and first-unfinished-Full-stage continuation, while requiring each new Lite session to resolve mode again, reject resume claims for unpersisted Change Brief, approval, progress, or Review state, and reconstruct a new Change Brief from repository state and user input. It also rejected the stale mode-neutral save, resume, and Generic quick-start sentences.

Command:

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation.ReleaseDocumentationTests.test_mode_enabled_host_guides_scope_question_and_approval_contracts tests.release.test_documentation.ReleaseDocumentationTests.test_localized_generic_guides_distinguish_full_and_lite_session_continuation
```

Observed result:

```text
Ran 2 tests in 0.006s
FAILED (failures=42)
```

All 42 failures detected the approved missing behavior: three absent Japanese Codex gate identities and 39 absent or stale Generic session-lifecycle assertions across the three locales. Test collection and execution succeeded without setup or unrelated failures.

### Closure correction focused Green

The first Green attempt passed the strengthened host-guide contract but retained one stale Japanese substring inside otherwise explicit Full context:

```text
Ran 2 tests in 0.002s
FAILED (failures=1)
```

The Japanese Full sentence was rewritten with an explicit Full subject while retaining its meaning and the stale-phrase guard. No assertion was weakened. The same command then produced:

```text
Ran 2 tests in 0.002s
OK
```

The closure cases were combined with all prior Ticket 5 focused cases:

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation.ReleaseDocumentationTests.test_all_nine_start_pages_are_concise_full_lite_handoffs tests.release.test_documentation.ReleaseDocumentationTests.test_detailed_full_guides_keep_plain_language_ticket_test_choices tests.release.test_documentation.ReleaseDocumentationTests.test_readme_uses_approved_localized_introduction_and_quick_start_order tests.release.test_documentation.ReleaseDocumentationTests.test_localized_codex_guides_document_mode_config_contract tests.release.test_documentation.ReleaseDocumentationTests.test_localized_generic_guides_document_embedded_mode_contract tests.release.test_documentation.ReleaseDocumentationTests.test_mode_configuration_stays_in_host_guides tests.release.test_documentation.ReleaseDocumentationTests.test_mode_enabled_host_guides_scope_question_and_approval_contracts tests.release.test_documentation.ReleaseDocumentationTests.test_localized_generic_guides_distinguish_full_and_lite_session_continuation tests.release.test_documentation.ReleaseDocumentationTests.test_generic_start_pages_keep_full_only_startup_claims_mode_scoped tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_start_pages_handoff_to_the_detailed_command_contract tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_readme_preserved_blocks_are_independent_of_git_head tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_readme_keeps_install_heading_order_and_single_sections

Ran 12 tests in 0.375s
OK
```

### Closure correction broader verification

Commands and observed results:

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation

Ran 25 tests in 1.762s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_command_install_docs

Ran 5 tests in 0.003s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_documentation.ReleaseDocumentationTests.test_all_relative_document_links_resolve tests.release.test_command_install_docs.CommandInstallDocumentationTests.test_localized_guide_relative_links_resolve

Ran 2 tests in 1.808s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.codex.test_lite_workflow tests.generic.test_generic_lite_workflow tests.generic.test_generic_prompts

Ran 37 tests in 0.764s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.codex.test_lite_workflow tests.generic.test_generic_lite_workflow tests.generic.test_generic_prompts tests.release.test_workflow_token_proxy

Ran 56 tests in 4.210s
OK
```

```text
.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_codex_release.CodexReleaseSourceTests.test_plugin_start_guide_explains_manual_first_use_and_all_entries tests.release.test_generic_release.GenericReleaseTests.test_builder_emits_self_contained_conversation_only_package

Ran 2 tests in 0.471s
OK
```

README, START-HERE, runtime, version, Plan, Review report, and expected README digest content were not changed during this closure correction.

### Closure correction final diff checks

Commands:

```text
git diff --check -- docs/guides/generic.en.md docs/guides/generic.zh-TW.md docs/guides/generic.ja.md docs/guides/codex.ja.md tests/release/test_documentation.py docs/evidence/lite-workflow-mode-1.3.0-ticket-5.md

git diff --check
```

Observed result for both commands:

```text
Exit code: 0
No whitespace errors. Git emitted only expected LF-to-CRLF working-copy warnings on Windows.
```

The closure correction requires a fresh independent after-fixes Review. No Review was performed in this implementation context.
