# Ask Then Do It 1.3.1 維護 Ticket 3 第二輪獨立 Closure Review

Artifact type: Review Report

Artifact ID: `release-1-3-1-maintenance-ticket-3-review-after-envelope-p2`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `3 - 整合 lockstep 1.3.1 identities、packages 與 checksums`

Execution mode: `tdd`

Status: Complete - no actionable findings

Review label: `independent`

Reviewed inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md) Ticket 3、initial [Review](release-1.3.1-maintenance-ticket-3-review.md)、first [closure Review](release-1.3.1-maintenance-ticket-3-review-after-p2.md)、三個 scoped files 的 final diff 與相關周邊 code、default `dist`、supplied raw verification。

Assumptions: Full mode 已由 absent Config fallback 證明；Tickets 1、2 已接受；同一 output directory 只由單一 builder 串行操作。

Deferred: Ticket 4 final validation/evidence、release-milestone architecture diagnosis，以及 tag、push、GitHub Release、asset upload、Marketplace activation與announcement。

Independence boundary: Reviewer未參與實作、未讀 [Ticket 3 Implementation Evidence](release-1.3.1-maintenance-ticket-3.md)、未取得implementer narrative，也未修改repository files。先前Reviews只用於逐項closure核對，未提供實作者辯護或預設verdict。

Handoff: Ticket 3可標記Completed並凍結candidate，接續Ticket 4；本Review不授權external publication。

## Findings

沒有P0、P1、P2或P3 actionable finding。未觀察到scoped regression。

## Finding Closure

1. **Initial P2: duplicate JSON keys - closed.** `unique_json_object()`經`object_pairs_hook`套用於所有JSON object levels；config root、ledger root、nested check object均有負向coverage。
2. **Initial/first-closure P2: fake Markdown envelope - closed.** `artifact_envelope()`現在只接受首行canonical H1後的第一段連續`Field: value`區塊，遇第一個非欄位即停止，並拒絕會形成Setext heading的欄位。Fenced code、comments、ATX/Setext sections、第二個H1、plain body及raw HTML均無法再供應有效metadata。
3. **Initial P2: default `dist` integrity - closed.** Fresh builds、第二次build及default `dist`會比較完整file inventory與逐檔bytes；mutation只在temporary copy進行。Default candidate與fresh candidate byte-equal。

## Verification

- CPython `3.12.13`重跑evidence/base/1.3 contracts：`36/36 passed`。
- Temp-only adversarial probes：indented code、lazy blockquote、lazy list、raw HTML textarea、thematic break、Setext H1及title前空白，全部fail closed。
- Default `dist`：`48` files，與fresh candidate逐檔byte-equal。
- Codex SHA-256：`557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209`。
- Generic SHA-256：`6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b`。
- 兩個實際archive hashes與`dist/checksums.sha256`一致；scoped `git diff --check`通過。
- Supplied, not rerun by this reviewer：full discovery `215/215`、Skill `18/18`、Plugin `2/2`、Marketplace與Codex/Generic conformance、Token Full/Lite `14771/5480`與`62.90%` reduction。

## Evidence Unavailable

Reviewer未重跑完整`215` tests、官方validators、其他OS/CI或真實長時間Windows kernel lock。精確的歷史Red執行順序因independence boundary未取得；final regression tests與觸發案例則已可獨立觀察並通過。Tag、push、GitHub Release、asset upload、Marketplace activation及announcement未授權也未執行。

## Architecture And Refactoring Lenses

1. **Duplicated Code or Policy - `no-finding`.** Envelope policy及tree-byte parity各集中於單一helper。
2. **Long Function - `no-finding`.** `validate()`與candidate integrity test雖涵蓋多步驟，仍各自維持單一可追蹤責任。
3. **Large Module or Class - `no-finding`.** 變更未擴張至新的跨域責任。
4. **Long Parameter List - `no-finding`.** Config、ledger、evidence三個paths是穩定CLI contract。
5. **Data Clumps - `no-finding`.** Artifact paths未在多處形成重複coordination。
6. **Primitive Obsession - `no-finding`.** Canonical envelope grammar已由具名regex與單一parser boundary明確限制。
7. **Feature Envy - `not-applicable`.** Scope為無狀態file-validation functions，沒有跨物件ownership。
8. **Divergent Change - `no-finding`.** Scoped changes均服務release evidence或candidate integrity。
9. **Shotgun Surgery - `no-finding`.** Default candidate parity修正集中於共用helper與單一integration contract。
10. **Message Chains - `not-applicable`.** 變更沒有多層object navigation或call-chain coupling。
11. **Leaky Abstraction - `no-finding`.** Caller只消費已隔離的envelope，不再補償特定Markdown constructs。
12. **Shallow Module - `no-finding`.** Validator提供的fail-closed consistency gate明顯高於其interface cost。

沒有需要交由`$improve-architecture`診斷的系統性finding。

## Residual Risks And Untested Areas

自訂config仍可縮減除`workflow-token-proxy`外的required inventory；current `1.3.1` config則由exact 13-check contract鎖定。Same-output concurrency不在Specification保證內；Windows lock超過bounded retry仍會正確造成build failure。Ticket 4的isolated final validation與Completed release evidence尚未執行。

## Completion Assessment

Ticket 3 **appears complete**。Initial三項P2及first-closure envelope P2均已關閉，沒有未解Review blocker；candidate可凍結並交由Ticket 4完成最終整合驗證與release evidence。
