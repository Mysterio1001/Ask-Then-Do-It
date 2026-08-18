# Ask Then Do It 1.3.1 Maintenance Ticket 3 Independent Closure Review After P2

Artifact type: Review Report

Artifact ID: `release-1-3-1-maintenance-ticket-3-review-after-p2`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `3 - 整合 lockstep 1.3.1 identities、packages 與 checksums`

Execution mode: `tdd`

Status: Changes Requested

Review label: `independent`

Reviewed inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md) Ticket 3、initial [Ticket 3 Review](release-1.3.1-maintenance-ticket-3-review.md)、final diff、相關 source/tests、current config、default `dist` 與 supplied raw verification。

Assumptions: Full mode 已證明；Tickets 1、2 已接受；同一 output directory 只由單一 builder 串行操作。

Deferred: Ticket 4 Completed release evidence、release-milestone architecture diagnosis，以及 tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement。

Handoff: 回 Ticket 3補上 Markdown envelope Red/Green，重跑 affected與完整 gates，再交另一個 fresh independent closure Review。Review 本身不授權修正或 external publication。

Independence boundary: Final verdict 由 `fork_turns=none` 的 fresh reviewer產出；該 reviewer未讀 [Ticket 3 Implementation Evidence](release-1.3.1-maintenance-ticket-3.md)、未參與實作，也未修改 repository files。第一個 reviewer context因 broad search意外讀到少量 implementation evidence而主動放棄 independent label，其輔助結果沒有傳給 fresh reviewer。

## Findings

沒有 P0、P1或P3 finding。以下一項 P2阻擋 Ticket 3完成。

### P2 - Setext、後續 H1 或 raw HTML body內的假 metadata仍被視為 artifact envelope

Trigger: 使用完整 passed ledger，但 Draft Markdown唯一的 `Release version: \`1.3.1\`` 與 `Status: Completed` 位於合法 Setext H2、後續第二個 H1或 `<details>` body內。Fresh reviewer的 temp-only probes都觀察到 validator exit `0`；未取得 independent label的輔助 context另以 `<pre>`重現相同行為。

Impact: 沒有 top-level Completed envelope的 Draft evidence仍可通過 release gate。Initial P2的 fenced code與HTML comment triggers已封住，但「只接受 artifact envelope」的 fail-closed root cause尚未完成。

Evidence: `SECTION_HEADING`只辨識 ATX H2-H6；`artifact_envelope()`因此保留其他合法 Markdown section/body內的 metadata。現有負向 tests只涵蓋 fenced code、HTML comment與ATX H3。

Remediation direction: 明確限定 envelope的允許結構及結束條件，加入 Setext heading、後續 H1與raw HTML body Red cases；不要逐項追補可繞過的Markdown constructs。

Locations: `scripts/validate_release_evidence.py:23`、`scripts/validate_release_evidence.py:98`、`scripts/validate_release_evidence.py:111`、`tests/release/test_release_evidence.py:260`。

## Initial P2 Closure

1. **Duplicate JSON keys - closed.** `object_pairs_hook=unique_json_object`遞迴拒絕 config、ledger與nested check object的重複鍵。
2. **Markdown fake envelope - not closed.** Fences、comments與ATX body section已封閉；Setext H2、後續 H1及raw HTML body仍可繞過。
3. **Default `dist` integrity - closed.** Fresh builds與default `dist`比較完整 file inventory及逐檔bytes；drift mutation只作用於temporary copy。

## Verification

- Fresh independent affected contracts: `36/36 passed`，9.236秒。
- Default `dist`: 48 files，與fresh candidate逐檔byte-equal。
- Codex SHA-256: `557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209`。
- Generic SHA-256: `6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b`。
- Hashes與`dist/checksums.sha256`相符；`git diff --check`無錯誤。
- Probes只使用已清理的 temporary directories。

Supplied, not rerun by the fresh reviewer: full discovery `215/215`、Skill `18/18`、Plugin `2/2`、Marketplace與Codex/Generic conformance、Token Full/Lite `14771/5480`、reduction `62.90%`。兩次真實 `WinError 5` failure及其後 isolated `2/2`、完整 `215/215`也屬supplied evidence。

## Architecture And Refactoring Lenses

1. **Duplicated Code or Policy - `no-finding`.** Candidate parity集中於共用tree-byte comparison。
2. **Long Function - `no-finding`.** JSON、Markdown與主流程已有具名helpers。
3. **Large Module or Class - `no-finding`.** Module維持單一evidence-validation責任。
4. **Long Parameter List - `no-finding`.** 三個artifact paths是穩定CLI contract。
5. **Data Clumps - `no-finding`.** Paths未形成多處重複coordination。
6. **Primitive Obsession - `finding`.** 手寫raw Markdown辨識不完整，形成上述P2。
7. **Feature Envy - `not-applicable`.** Scope是無狀態file-validation functions。
8. **Divergent Change - `no-finding`.** 變更原因均屬release validation。
9. **Shotgun Surgery - `no-finding`.** Default parity修正集中於helper及單一integration test。
10. **Message Chains - `not-applicable`.** 無多層object navigation。
11. **Leaky Abstraction - `finding`.** Caller仍須知道parser未涵蓋哪些標準Markdown constructs。
12. **Shallow Module - `no-finding`.** CLI封裝的validation價值高於interface cost。

此P2可在Ticket 3 ownership內修正，尚不需要`$improve-architecture`系統性診斷。

## Evidence Unavailable

Fresh reviewer未重跑完整`215` tests、官方validators、其他OS/CI或真實長時間kernel lock。沒有tag、push、GitHub Release、asset upload、Marketplace activation或announcement evidence，因這些actions未授權。

## Residual Risks And Untested Areas

Same-output concurrency不在Specification保證內；自訂config縮減required inventory仍是既有residual risk。Windows external lock超過既定retry window仍可能造成正確的build failure；final successful full run不消除該已記錄風險。

## Completion Assessment

Ticket 3 **does not appear complete**。Initial P2 #1與#3已關閉，但P2 #2的top-level envelope contract尚未fail closed；必須完成另一輪correction及fresh independent closure Review後才能標記Completed。
