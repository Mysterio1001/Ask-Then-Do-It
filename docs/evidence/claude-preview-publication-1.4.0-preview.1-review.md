# Claude 1.4.0-preview.1 公開預覽發布獨立 Review

artifact_type: Review Report

artifact_id: `claude-preview-publication-1-4-0-preview-1-review`

workflow_id: `claude-code-adapter`

core_version: `1.3.0`

status: Accepted — no open actionable findings; publication verification remains a separate handoff.

Review label: `independent`

Approved implementation mode: `tdd`，沿用原 Claude Tickets；本次為已核准的 preview 發布收尾。

## Findings

最終候選沒有未解決的 actionable findings。本次 reviewer 是未參與實作的 fresh subagent，直接檢查核准文件、候選來源、測試、原始輸出及 ZIP bytes；只新增本 Review Report。

**已修正 P2：發布候選仍含舊版導覽文件。** 初次 frozen candidate 的三語 Plugin `START-HERE` 仍標示未發布的 `1.4.0`，並在第 16／20 行連到 `blob/v1.4.0/`；root 繁中／日文入口、三語 beginner additions 及 README insertion test 也仍是舊副本。公開 preview 使用者會遇到錯誤版本、未發布狀態及不可用的詳細指南連結。協調者重新複製完整文件／測試集合後，reviewer 再檢查三語導覽與 ZIP 內全部三個 START-HERE，確認皆使用 `1.4.0-preview.1`、對應 tag 連結及延後 live 驗證揭露；最終 suite 已通過。此 finding 已關閉。

## Inputs、assumptions 與範圍

- 核准 [preview publication plan](../plans/claude-preview-publication-1.4.0-preview.1.md)、原 [Specification](../specs/claude-code-adapter-1.4.0.md) 與 [Ticket Plan](../plans/claude-code-adapter-1.4.0.md)。協調者已證明本次 top-level Full；既有使用者核准明確涵蓋公開 preview 與發布操作，沒有新增核准 gate。
- 最終候選為 `.claude-offline/publication/source/` 的 staged source。重點檢查 `.claude-plugin/marketplace.json`、Claude runtime identity／mapping digest、兩個 public bootstraps、`scripts/build_release.py` preview path、Plugin／package／context validators、相關 tests、`.gitattributes`／`.gitignore`、三語 README additions、root／Plugin START-HERE 與 Claude／beginner guides。
- 既有 Claude runtime 的完整實作已有 `docs/evidence/claude-code-adapter-1.4.0-*` 歷史 Review；此 pass 評估 publication delta 與其影響範圍，不聲稱重新完成整個 runtime 的系統架構診斷。
- 另讀取一次性發布程式與 release notes。程式先核對帳號、tag 的 commit 與 latest stable，建立 draft、上傳確定的兩個 assets，再以 `prerelease=true`、`make_latest=false` 公開；實際遠端操作結果不由程式碼審閱代替。
- 原始本機證據位於 ignored `.claude-offline/publication/`：`native-validation.json`、`native-validation-final.json`、`full-suite-final.log`、`full-suite-verified.log`、`artifact.json`、`assets/checksums.sha256`。這些路徑用來識別 reviewer 實際讀取的本機輸入，不是公開下載承諾；local binaries、credentials、驗證輸出與個人資料不列入發布 source 或 ZIP。

## Verification

最終原始 suite 輸出：

```text
Ran 393 tests in 120.740s
OK (skipped=1)
```

協調者記錄 exit `0`；reviewer 直接讀取 `full-suite-verified.log`。此精簡輸出未附個別 skip 原因，不能把該項視為通過。

前一輪 `full-suite-final.log` 的 56 failures 全部來自兩組既有 immutable-byte checks：43 個歷史 1.3 artifacts 與 13 個舊 token fixtures。Git blob 為 LF，而原始凍結 SHA 期待其 CRLF checkout bytes。恢復既有 checkout bytes 後，reviewer 另以唯讀程式獨立驗證全部 56 個 raw SHA 與原測試常數相符，且每檔 LF-normalized 內容等於 staged Git blob；未修改 test 或弱化 expected hash。最終完整 suite 隨後通過，candidate 的 `git diff --quiet` 亦為 `0`。

Native evidence 顯示 exact Claude Code `2.1.251`，且最終 candidate Plugin 與 Marketplace 的 `plugin validate --strict` 均 exit `0`。這是 manifest/schema 可解析的證據，並非 authenticated session 或模型行為驗證。

Reviewer 獨立讀取兩次 preview build，确认 35 個 output files 全部 byte-identical。公開 ZIP 的 32 個 payload files 逐檔等於最終 source runtime 與 canonical legal files；順序、固定 timestamp、regular-file mode 及三語 guide tag 連結均符合。`preview.json`、Marketplace catalog、開發 evidence 與 local state 不在 ZIP。公開 assets 只有 ZIP 與使用平面檔名的 checksum：

```text
File: ask-then-do-it-claude-1.4.0-preview.1.zip
Size: 55632 bytes
SHA-256: 38d228914bf52b4eaa71f3c92e04a3397593a24c5c3a7204bf911cc870336e7b
```

Catalog、manifest、router envelope、model mapping、bootstraps、validator 與 builder preview identity 一致為 `1.4.0-preview.1`；Plugin source 固定 `v1.4.0-preview.1`，user-facing Marketplace URL 明確選用 `#claude-preview`。Captured official Marketplace 文件包含 git URL `#ref` 語法及 refresh 跟隨該 ref 的說明。原 future `1.4.0` conformance target 未被假裝完成。

候選 staged diff 未修改 `release/`、`core/`、`adapters/codex/`、`adapters/generic-prompts/`、既有 Codex catalog 或使用者 `docs/project/knowledge-base.md`。目前 stable config 維持 `1.3.1`；本機輸出、下載的 binary、未相關 HTML 與原 Knowledge Base 修改皆未被帶入候選。

## Twelve Architecture and Refactoring Lenses

| Lens | Outcome | Evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | no-finding | 跨 native manifests、runtime 與三語文件的 identity／發布狀態已同步；contract tests 與 ZIP 檢查拒絕 drift。初次 stale-copy finding 已關閉。 |
| 2. Long Function | no-finding | 本次 version synchronization 未擴大 router responsibilities；preview helpers 分別處理 configuration、marker、isolation 與 packaging，無阻礙此變更理解或驗證的新混合責任。 |
| 3. Large Module or Class | no-finding | Builder 繼續共用既有 ZIP／transaction 流程，Claude inventory／source parity 位於專用 package validator；本次未引入須拆分的新大型責任。 |
| 4. Long Parameter List | not-applicable | Publication identity／文件同步沒有新增需協調多組不穩定參數的 public interface。 |
| 5. Data Clumps | no-finding | Claude source、directory、archive 已收在 family config；payload bytes 與其 hash 由同一 marker construction 推導。 |
| 6. Primitive Obsession | no-finding | Version、source ref、inventory、envelope fields 及 mapping digest 有 exact checks；未將任意字串當可發布 identity。 |
| 7. Feature Envy | no-finding | Builder 透過 package validator 取得／驗證 payload；新增 preview 工作未將 router state 或模型分類責任移入發布程式。 |
| 8. Divergent Change | no-finding | Offline preview 分支與現行 stable config 分開；文件與 native manifest updates 均由同一 preview publication 需求驅動。 |
| 9. Shotgun Surgery | no-finding | 本次跨檔版本與三語副本同步屬外部格式邊界，相關 tests、source parity 與 grouped copy 可驗證；沒有剩餘 drift 或新增的系統性拆分缺陷。 |
| 10. Message Chains | not-applicable | Publication delta 沒有新增深層 object navigation 或 chained runtime interaction。 |
| 11. Leaky Abstraction | no-finding | 文件清楚區分 moving catalog、tag-pinned Plugin、session-only ZIP 與 live 驗證；builder marker 只宣稱 offline packaging，公開 release 由獨立已核准步驟產生。 |
| 12. Shallow Module | no-finding | Package validator 實際封裝 inventory、link/path containment、identity 及 byte parity；preview helpers 共用 transaction 而非增加空轉介面。 |

## Deferred、residual risk 與 handoff

已核准 preview 的實作／文件／離線 package 準備可交付發布；本 Review 不把尚未執行的 public push／tag／release／下載回驗標成完成。下一步由協調者依既有核准正常發布，核对公開 `claude-preview` branch、`v1.4.0-preview.1` tag、prerelease flags、ZIP／checksum 下載 bytes，並確認 latest stable 仍為 `v1.3.1`。

Authenticated 官方 Claude sessions、完整兩個 profile 的 behavior／paired equivalence、context reduction、三作業系統／IDE matrix 與 live lifecycle smoke 仍未驗證；使用者僅對本公開 preview 接受此限制。Native strict 與本機測試不取代那些證據，原正式 `1.4.0` Tickets／acceptance gates 不因此視為全部完成。
