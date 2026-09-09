# Claude Code Adapter 1.4.0 Ticket 4 Independent Review

artifact_type: Review Report

artifact_id: `claude-code-adapter-1-4-0-ticket-4-review` (stable)

workflow_id: `claude-code-adapter`

core_version: `1.3.0`

Product authoring baseline: `1.3.1`

Target release version: `1.4.0`

Ticket: `4 - 交付 General profile 的完整工作流程`

Approved execution mode preserved: `tdd`

status: Changes requested — three actionable P2 findings; Ticket 4 is not complete

Review label: `independent`。本次由未參與實作的 fresh reviewer context 進行；reviewer 直接檢查 Approved artifacts、final source、surrounding bootstrap/router/reviewer/Core contracts、tests 與 raw verification records，未採納 Implementation Evidence 的結論。

Capability profile: `multi_agent`、`tools`、`conversation`。本 reviewer context 具獨立隔離、repository 讀取、command execution 與本 Review Report 持久化能力。

inputs: Approved `docs/specs/claude-code-adapter-1.4.0.md`；Approved `docs/plans/claude-code-adapter-1.4.0.md` Ticket 4（mode=`tdd`）；final `adapters/claude-code/plugin/ask-then-do-it/profiles/general/**`、`tests/claude/test_general_profile.py`、`tests/claude/fixtures/general-profile/**`；shared inventory integration in `scripts/validate_claude_plugin.py` and `tests/claude/test_public_plugin_contract.py`；surrounding public Skills、reviewer、router/state tests、Core `1.3.1` rules/modules/artifact envelope；`docs/evidence/claude-code-adapter-1.4.0-ticket-4.md`及使用者提供的 Red/Green/integration/full/native raw summaries。Repository內沒有找到適用的 `AGENTS.md` 或 `CLAUDE.md`。

assumptions: Review target是目前workspace的final bytes。Ticket 4 files與shared integration files目前皆為untracked，Git無法重建只含Ticket 4的narrow baseline diff；因此本Review依final bytes、Approved contracts及可執行checks判斷。Ticket 4的30-scenario gate按Approved sequencing視為deterministic General instruction-contract proof；真正fresh model adherence與cross-profile equivalence屬Ticket 6，不在此冒充或提前要求。

deferred: Ticket 3 authenticated exact-host invocation／`additionalContext`／failure-semantics ledger；Ticket 6 paired fresh-session equivalence、雙向authority precedence與正式conformance；Ticket 7每checkpoint 50% context gate；localized docs、release identity/build/packages、clean live smoke及所有external publication mutations。這些正常deferred gates不是下列Ticket 4 findings。

handoff: 回到Ticket 4的Approved `tdd` implementation path，修正下列General prompt contracts並先新增能因缺失分支而Red的focused assertions／fixtures；重跑focused General、shared profile inventory、完整Claude regressions，再交給另一個fresh independent Review。三項finding關閉前不得把Ticket 4標為Completed；不得在本handoff修改Approved Specification、Plan、Knowledge Base、Claude 5 profile或任何external state。

## Findings

沒有P0、P1或P3 finding。以下三項P2均由目前General bytes直接觸發，且surrounding bootstrap、Core或tests沒有提供可由General operation載入的guard。

### [P2] Undefined `portable envelope` leaves every Full artifact schema non-executable

**Trigger:** A General operation reaches requirements, documented requirements, Specification, TDD/direct implementation, Review, or architecture reporting and follows the instruction to emit a `portable envelope`. **Impact:** The loaded General modules never define that term or its required fields, so a fresh Marketplace/ZIP runtime can omit or invent `artifact_type`、stable `artifact_id`、`workflow_id`、`core_version`、`status`、`inputs`、`assumptions`、`deferred`、`handoff`及適用時的`approval` evidence. That breaks traceability and can make later approval/reuse gates accept structurally incomplete artifacts. **Evidence/location:** Undefined uses occur at `profiles/general/requirements.md:9`, `documented-requirements.md:7`, `specification.md:7`, `tdd-implementation.md:9`, `direct-implementation.md:9`, `review.md:25`, and `architecture-improvement.md:11`; no exact envelope definition exists anywhere in the packaged public bootstraps or General profile. Core requires the fields in `core/artifacts/common.md:3-16`. `test_general_profile.py:88-114` checks Core/scenario tags and positive substrings only, so all six focused tests pass while the schema remains absent. **Remediation:** Define the exact common artifact envelope once in the always-loaded General `orchestration.md` (without adding an eleventh module), state when approval evidence is required, and add a focused negative/field-completeness assertion proving every artifact-producing stage relies on that definition.

### [P2] Conversation-only mode resolution has no deterministic unavailable-source fallback

**Trigger:** The declared capability is `conversation`, no explicit Full/Lite instruction exists, and the host cannot expose one or both Claude Config files. **Impact:** `orchestration.md` distinguishes an absent Config from an invalid one but says only that an unavailable source is not evidence it was read; it never says to treat a host-unavailable project/user source as absent. The operation therefore has no deterministic route to the next source or Full fallback and may stall, ask for a discoverable default, or fabricate a read, contrary to the mandatory capability/mode contract. **Evidence/location:** `profiles/general/orchestration.md:46-50`; the missing branch is explicit in `core/modules/orchestration.md:38-43`. The fixture separates `CAP-CONVERSATION` from `MODE-CONFIG`/`MODE-INVALID` (`tests/claude/fixtures/general-profile/scenarios.json:5-10`), and `test_general_profile.py:116-130` never exercises their cross-product. **Remediation:** State that a host which cannot provide the project source treats it as absent and continues to the user source, and that an unavailable user source is absent and reaches Full fallback, while still prohibiting claims that either file was read. Add a deterministic conversation/no-explicit/unavailable-source case plus project-unavailable/user-available precedence coverage.

### [P2] Full orchestration can bypass mandatory architecture and durable-knowledge routes

**Trigger:** A related Ticket group completes or a release milestone approaches without a direct architecture request, or an Approved/accepted artifact introduces durable project facts after requirement interrogation. **Impact:** General's first-unmet list goes directly from Review to completion and contains no automatic architecture route for the group/milestone triggers and no general post-artifact Knowledge Base Change Summary route. A General operation can therefore declare completion without the Core-required architecture diagnosis or leave durable project knowledge stale. A direct user-selected architecture module and a systemic Review finding are guarded elsewhere, but they do not cover these triggers. **Evidence/location:** `profiles/general/orchestration.md:57-65`; `profiles/general/review.md:23` covers only systemic Review evidence, and `documented-requirements.md:9` covers only the requirement-consensus knowledge update. The missing routing requirements are explicit at `core/modules/orchestration.md:71-81`. The current `FULL-ARCH` fixture checks only words inside `architecture-improvement.md`, while `FULL-KNOWLEDGE` checks only `documented-requirements.md` (`tests/claude/fixtures/general-profile/scenarios.json:12,18`). **Remediation:** Restore all four architecture-selection triggers with the Core's local-versus-systemic guard and add the general rule that an Approved/accepted artifact changing durable facts proposes a complete KB Change Summary (without delaying an unrelated gate when no durable fact changed). Add orchestration-level transition tests for group completion, release milestone, systemic/local Review, and post-artifact durable/no-durable outcomes.

## Verification performed and evidence unavailable

Independently performed on the reviewed final bytes:

- Focused General suite: `python -B -m unittest tests.claude.test_general_profile -v` — exit `0`; `Ran 6 tests in 0.013s`; `OK`.
- Complete Claude suite: `python -B -m unittest discover -s tests/claude -v` — exit `0`; `Ran 118 tests in 76.080s`; `OK (skipped=1)`. The only skip was Windows symlink creation without the required privilege.
- Canonical Claude Plugin validator with explicit catalog/plugin paths — exit `0`; `Claude Plugin validation passed`.
- `node --check adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs` — exit `0`; no output.
- Scoped trailing-space scan over General, its tests/fixture, shared validator and public contract test — no matches (`rg` exit `1`, expected for no match).
- The full Claude run independently executed and passed the shared exact-profile inventory mutations, canonical component containment checks, public bootstrap contracts, reviewer boundary, model evidence, and router/state/security regressions. The shared validator exact `general`/`claude-5` plus ten-module inventory integration is therefore verified and is not a finding.

Evidence not independently reproduced:

- Historical Red chronology cannot be replayed without replacing the final production state. The only available record is the supplied summary: General Red `Ran 6 tests in 0.023s; FAILED (failures=33, errors=2)` and shared-validator Red `Ran 2 tests in 0.282s; FAILED (failures=2)`; no separate raw log artifact was found.
- Supplied focused/integration/combined/full results (`6`、`3`、`23`、`118`、`334` tests), Plugin/model validators, diff check and exact Claude Code `2.1.251` strict-zero-warning results were read but not treated as reviewer conclusions. This Review reran the focused and complete Claude surfaces, not the complete `334`-test repository suite.
- Exact native strict validation was not rerun in this Ticket 4 pass; its supplied static result remains distinct from Ticket 3 authenticated behavior. No namespaced command invocation, live model response, `additionalContext` observation, context measurement, package build, install/update/remove mutation, or live smoke was performed.
- Ordinary `git diff --check` cannot cover these untracked Ticket files. The independent scoped trailing-space scan covers the principal whitespace condition but is not a substitute for a committed narrow diff.

## Residual risks and untested areas

- The deterministic instruction-contract tests intentionally do not prove that a real model obeys the prompts. Ticket 6 owns fresh-session, paired outcome and same-session authority evidence; Ticket 3 owns exact-host behavior. Neither deferred gate excuses the three missing General instructions above.
- `test_fixed_thirty_scenarios_have_executable_general_contracts` verifies positive normalized substrings. It does not reject a contradictory sentence, test cross-scenario state transitions, or validate the artifact schema. The remediation tests need explicit negative and transition coverage so a Green run establishes the corrected deterministic contract rather than model adherence.
- Current source is untracked, so accepted bytes do not yet have commit-level provenance and a historical narrow diff is unavailable.
- Ticket 7 context thresholds and Ticket 10 clean live smoke/release gates remain required and unassessed here.

## Ticket completion assessment

Ticket 4 does **not** appear complete against its Approved `tdd` plan. Exact ten-module inventory、30 Core/scenario markers、General-only loading、lifecycle text、shared inventory validation and the fresh Claude regression suite pass, but three mandatory General behaviors are absent from the executable prompt contract and are not protected by focused tests. Ticket 3 live-host、Ticket 6 paired equivalence and Ticket 7 context work remain correctly deferred; they do not change this Ticket 4 changes-requested result.

## Twelve Core Architecture and Refactoring Lenses

本lens pass只涵蓋Ticket 4 General profile、其focused fixture/tests、shared inventory integration及直接bootstrap/router/reviewer/Core impact area，不代表整個repository architecture diagnosis。

| # | Core lens | Outcome | Evidence / scope-specific reason |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `no-finding` | General與Claude 5必須各自完整保有同一Core outcome；validator與test中的獨立exact-inventory oracle也是刻意的drift guard。此Review未找到General內兩份互相矛盾的同一policy；跨profile等價性保留給Ticket 6。 |
| 2 | Long Function | `no-finding` | General production是分節Markdown；`validate_plugin_root`與focused test methods保持單一inventory/contract責任。現有finding源自缺失branch，不是因任何單一長函式無法理解或測試。 |
| 3 | Large Module or Class | `no-finding` | `orchestration.md`涵蓋多個協調面但以明確heading分界，且十模組inventory是Approved Specification固定邊界；沒有僅因size成立的額外可行動缺陷。 |
| 4 | Long Parameter List | `not-applicable` | Ticket 4沒有新增需要評估的多參數public API；validator relevant functions接收bounded path/value inputs，Markdown stage contract也不是positional parameter interface。 |
| 5 | Data Clumps | `no-finding` | Profile/module/scenario集合都以named exact sets及schema固定；artifact envelope本應是單一coherent record，其問題是完全未定義，而不是值在多個呼叫間無結構地傳遞。 |
| 6 | Primitive Obsession | `no-finding` | Profile names、scenario IDs、Core IDs與module filenames雖為字串，但均受closed sets、exact inventory及fixture/schema constraints控制；未找到由unconstrained primitive直接造成的額外行為缺陷。 |
| 7 | Feature Envy | `no-finding` | General stages擁有各自workflow policy，shared validator只檢查Plugin inventory/containment；沒有一個changed unit主要操縱另一unit的私有資料或責任。 |
| 8 | Divergent Change | `no-finding` | General `orchestration.md`的routing、capability、Config與lifecycle都屬同一host orchestration boundary；Approved十模組限制下，未建立需要另行架構Ticket的無關change axis。 |
| 9 | Shotgun Surgery | `no-finding` | 三項finding可在always-loaded orchestration集中補齊，再對focused fixture/test增加垂直guard；不需要修改public bootstrap、router、Claude 5或Core。尚無證據顯示一般General policy修正必須散改多個production owners。 |
| 10 | Message Chains | `no-finding` | Public bootstrap → bound General orchestration → one required stage module是Specification要求的bounded progressive load chain；沒有暴露更深內部navigation或跨session chain。 |
| 11 | Leaky Abstraction | `finding` | 對應第一項P2。七個stage只說`portable envelope`，迫使fresh runtime依賴未封裝、且consumer package中不可用的Core artifact detail。應由always-loaded orchestration提供exact abstraction contract。 |
| 12 | Shallow Module | `finding` | 對應三項P2的test guard缺口。`test_fixed_thirty_scenarios_have_executable_general_contracts`的名稱／fixture表面提供30-scenario abstraction，實際只做tag與substring inclusion，未隱藏或驗證artifact schema、capability×Config及post-stage routing semantics；需加入negative與transition oracles。 |
