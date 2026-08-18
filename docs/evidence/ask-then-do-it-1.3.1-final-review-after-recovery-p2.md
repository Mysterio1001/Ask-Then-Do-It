# Ask Then Do It 1.3.1 Recovery P2 Closure Review

Artifact type: `Review Report`

Artifact ID: `ask-then-do-it-1-3-1-final-review-after-recovery-p2`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `4 - 完成本機整合驗證與 1.3.1 release evidence`

Execution mode: `tdd`

Status: `Complete - no actionable findings`

Review label: `independent`

## Findings

沒有 P0、P1、P2 或 P3 actionable finding。

先前 P2 已關閉。`scripts/build_release.py:773-799` 現在依 managed-output name 保存 candidate-removal error；只有同名 prior backup 在 `scripts/build_release.py:783-795` 成功恢復後，才消除已被最終 prior state 取代的 removal error。其餘 candidate-removal 或 restoration failure 仍會形成 `IncompleteRecoveryError`。

這符合 Approved Specification 對「整個先前 managed output set」的判定要求：

- `validate_existing_output_set()` 保證 `existing_names` 是空集合或完整已驗證集合；正式 caller 不會提供局部 prior set。
- 每個成功移入 backup 的 prior output 都記錄於 `moved_old`，並逐一嘗試恢復。
- 同名 restore 成功代表該 active target 已由 prior output 取代；若任何 restore 仍失敗，`restoration_errors` 保持非空，不會誤報完整恢復。
- 所有 unresolved recovery errors 消失後，只拋出明示 candidate 未提交、pre-build state 已恢復的一般 `BuildError`。
- `main()` 只為 `IncompleteRecoveryError` 保留 staging；這個完整恢復分支會經 `scripts/build_release.py:872-878` 清除 transaction-only staging。

新增測試 `tests/release/test_release_transaction.py:346` 對本缺陷具直接敏感度：它鎖定 50 次 candidate-removal exhaustion、後續同名 prior restore、一般 `BuildError`、正確診斷、prior bytes、空 backup，以及 exact retry/sleep 次數。提供的 Red 結果也證明 production correction 前測試只因錯誤拋出 `IncompleteRecoveryError` 而失敗。

## Reviewed Inputs

- Approved `docs/specs/release-1.3.1-maintenance.md`
- Approved `docs/plans/release-1.3.1-maintenance.md` Ticket 4
- `docs/evidence/ask-then-do-it-1.3.1-final-review-after-p2.md`，僅作為待關閉 finding 的輸入
- Final diff、`scripts/build_release.py` recovery/main surrounding code
- `tests/release/test_release_transaction.py` 與 release safety coverage
- 委託方提供的 raw Red/Green、builder、full-suite、hash 與 cleanup 結果

## Assumptions

- Canonical resolver 已證明本 operation 為 Full，runtime capability 為 multi-agent。
- 同一 output directory 僅有一個串行 builder；concurrent builders 不在保證範圍。
- CPython 3.12/Pillow 12.x 是正式驗證 baseline。
- `commit()` 是 builder 內部交易函式；正式呼叫前已由 existing-output validation 建立完整集合 invariant。
- 目前受審檔案是 recovery P2 correction 後的 final source state。

## Independent Verification

- CPython `3.12.13` transaction module：`11/11 passed`，1.052s。
- Release safety module：`6/6 passed`，4.306s。
- 完整 discovery clean run：`216/216 passed`，28.353s。
- 第二次 verbose 完整 discovery：`216/216 passed`，32.163s。
- `test_main_preserves_recovery_data_after_incomplete_recovery` 單獨重跑：`1/1 passed`。
- `git diff --check` 對受審檔案通過；只有既有 LF/CRLF 提示。
- `dist` 維持 48 files，沒有 `.dist-release-*` transaction root。
- Codex SHA-256：`557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209`。
- Generic SHA-256：`6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b`。
- 兩個實際 hash 均與 `dist/checksums.sha256` 一致，且與修正前值相同。

委託方提供的 raw evidence 另包含 focused Green `1/1`、transaction `11/11`、safety `6/6`、official isolated builder exit 0、full `216/216`、evidence/base/1.3 `36/36`。

## Architecture And Refactoring Lenses

1. **Duplicated Code or Policy - `no-finding`.** Retry eligibility、上限與 delay 仍集中於單一 helper；supersession policy 只存在 recovery classification 一處。
2. **Long Function - `no-finding`.** `commit()` 雖涵蓋 forward 與 recovery，但 state transition 仍線性且局部狀態命名明確；本修正未造成難以追蹤的責任混合。
3. **Large Module or Class - `no-finding`.** 修正留在 builder 既有 transaction ownership，沒有新增跨領域責任或耦合。
4. **Long Parameter List - `no-finding`.** `commit()` 與 `IncompleteRecoveryError` 的參數均直接對應必要 transaction state。
5. **Data Clumps - `no-finding`.** Primary error、unresolved recovery errors 與 recovery paths 已由專屬 error type 集中；新 mapping 只在 recovery scope 內存在。
6. **Primitive Obsession - `no-finding`.** 先前以非空 error list 代理 final recovery state 的問題已消除；name-keyed mapping 現在表達「哪個 candidate failure 可被同名 restore 取代」。
7. **Feature Envy - `not-applicable`.** 受審範圍是單一 procedural filesystem transaction，沒有相鄰 domain object ownership 可被錯置。
8. **Divergent Change - `no-finding`.** 本區所有變更均由 managed-output recovery correctness 驅動。
9. **Shotgun Surgery - `no-finding`.** 行為修正集中在 recovery classifier 與一個精確 regression test。
10. **Message Chains - `not-applicable`.** 沒有多層 collaborator navigation 或內部 object chain。
11. **Leaky Abstraction - `no-finding`.** `IncompleteRecoveryError` 現在只表示仍有 unresolved recovery state；caller 可可靠地依型別決定是否保留 staging。
12. **Shallow Module - `no-finding`.** Retry helpers與 structured recovery error 均封裝實質 policy；新增 mapping 修正 final-state 判定，沒有新增低價值介面。

沒有需要由 `$improve-architecture` 診斷的 systemic review finding。Ticket 4 規劃中的 release-milestone architecture diagnosis 仍須照原流程執行。

## Evidence Unavailable

- Reviewer 未親自觀察 pre-patch Red；該結果採用委託方提供的 raw TDD evidence。
- Reviewer 未重跑 official isolated builder 或獨立的 evidence/base/1.3 `36/36` command。
- 第一次完整 discovery 在工具 30 秒回傳邊界只留下單一 `F` 進度符號，沒有 test name、traceback 或 final result 可供診斷；後續兩次完整 discovery 及受影響 modules 均乾淨通過。
- 未以真實長時間 kernel lock、真正非 Windows host、external CI 或 live installed Plugin 驗證。
- 未執行任何 external publication、install、tag、push 或 release mutation。

## Residual Risks

- 真實 Windows lock 超過約 4.9 秒仍會按設計耗盡 retry；永久 ACL 型 `WinError 5` 亦使用相同 bounded window。
- 第一次無 traceback 的 discovery 異常無法歸因，應保留為 observed transient，而不是成功證據；目前沒有可重現行為支持 actionable finding。
- Superseding regression fixture 使用 file targets；實際 provider directories 依相同 Path/retry/state logic 處理，但真實 locked-directory 行為仍主要由 deterministic abstraction coverage 支撐。
- Same-output concurrent builders 明確不受支援。
- 任一後續 source/package 改動都會使本 Review、目前 hashes 與 candidate freeze 失效。

## Completion Assessment

Recovery P2 correction、相關 source state 與 frozen candidate review gate 看來完整；先前 Primitive Obsession 與 Leaky Abstraction findings 均已關閉，沒有剩餘 release-correctness blocker。

Approved Ticket 4 整體尚未達成其 Plan 定義的完成條件，因為 read-only release architecture diagnosis、validation ledger、Completed release evidence 與 evidence-only closure 仍未完成。下一個 handoff 是執行 release-milestone architecture diagnosis，之後建立並驗證本機 evidence；外部 publication actions 繼續延後且未獲授權。
