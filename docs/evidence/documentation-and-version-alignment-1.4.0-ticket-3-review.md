# 文件與版本統一 1.4.0 — Ticket 3 Independent Review

> 歷史紀錄：以下結論及測試數是原審查當時的觀察。本次文件整理只更新導航；原始 inputs／Ticket 檔名與核准證據可從[清理快照](release-history.md#archive)找回。新連結指向現行摘要，不代表 reviewer 當時審閱過新文件；目前進度見[狀態](../project/status.md)。

Artifact type: Review Report

Artifact ID: `documentation-and-version-alignment-1-4-0-ticket-3-review`

Workflow ID: `documentation-and-version-alignment`

Core version: `1.4.0`

Status: Completed (independent Review of local offline scope)

Review label: `independent`

Inputs: Approved [Specification](../maintainer/releasing.md)、Approved [Ticket Plan](../maintainer/releasing.md) Ticket 3；`.claude-offline/doc-alignment-1.4.0/before/` 與 `before-sha256.json`；凍結的來源／文件及最終文件測試；本次原始測試、validator、建置輸出。

Assumptions: 本 reviewer 是未參與實作的獨立子代理，從規格、基準、來源與原始輸出重建結論，未採用實作者 verdict。Full／multi_agent 與 gates 已核准。Ticket 1／3 為 `tdd`；Ticket 2 為 `direct`，保留 `tests: skipped-by-user`。本報告使用使用者明確要求的 1.4.0 artifact 版本。

Deferred: 真實 Claude 登入、exact host hooks／模型行為／context／reviewer／生命週期實測，正式 release Completed 驗收，所有遠端發布；本機無建立 symbolic link 權限而略過的一項既有測試。

Handoff: 回交主代理同步本 Ticket 的離線完成狀態與最終原始驗證紀錄；保留正式 Claude／release 驗收缺口，不延伸為舊 Claude adapter 計畫全部完成或遠端發布授權。

## Findings

本次範圍沒有可行動 findings，沒有阻塞來源、文件與離線整合交付的缺陷。最終 `-m unittest discover -s tests -v` 執行 394 tests，`OK (skipped=1)`，exit 0；獨立閱讀完整結果及修正 diff 後確認，原有三項 current-contract 遺漏與尚未建立的 Review 連結均已解決。

唯一略過的是 `ClaudeRouterSecurityTests.test_state_file_symlink_is_not_followed`，本機建立 link 時回報 Windows `WinError 1314`。這是未執行的既有真實 filesystem 分支，不能描述成通過。正式 Claude 實測與遠端發布仍未驗證，不能以修正測試預期或產生 ZIP 取代。

## 已完成的獨立檢查

- 基準索引包含 403 份檔案，副本 SHA-256 全部符合索引。以此基準判定本次差異，未將 HEAD 的既有使用者變更歸入本次。
- README bytes 完全相同；基準內 149 份既有 evidence、8 份規格、8 份需求、3 份設計文件未變。既有歷史保護方法及 72 個歷史／fixture hash entries 未改。
- 官方 platform ledger 與 model source-trace 的 7 加 4 份儲存快照 hash 相符。Model source-trace 的 JSON 語意只有衍生 `mapping_sha256` 改變，來源、取用日期、原始 hash 與 records 均保留。
- 逐一追查當前 Core／adapter／Plugin／catalog／runtime 版本差異。除必要版本與衍生 hash 外，routing／profile／最低版本／核准語意維持原樣；舊 preview helper 保持固定歷史版本與隔離／not-a-release 邊界。
- 檢查九份指南的七章結構、首次操作例子、Full／Lite 設定、平台差異、十二份 START-HERE 及 Claude 三語進階參考。README 的首次安裝、更新收合區與更多說明順序保持原樣；套件導引採固定 v1.4.0 文件連結並保留 `#zip`。
- 更新後文件測試保護操作契約、章節、導航、最低版本、兩入口、session-only、能力與實測限制；保留的 beginner／design／官方 evidence helper 共十個方法來源未改。未將已被使用者替換的 current prose／插入 hash 當成歷史 artifact。
- Builder 的雙套件到三套件升級僅接受完整 Codex／Generic／checksum 舊集合；仍驗證 provider inventory、ZIP bytes、checksum、links。追查 staging、commit 與 rollback，新增 failure 測試涵蓋 Claude／checksum 安裝失敗後回復舊集合。
- 直接讀取 build-a／build-b：81 個輸出檔案 bytes 相同；兩次三個 ZIP 的 SHA-256、精確 ZIP inventory、ZIP／目錄 bytes 均一致。Codex 27、Generic 18、Claude 32 個封裝 entries 相符；Codex／Claude payload 與當前來源／legal files 相同，Generic modules／START-HERE 與來源相同。
- `release/release.json` 保留全部既有 checks，另含 Claude 六項必要 checks。Canonical Claude conformance 是 `unverified`；builder 可證明來源／inventory 契約，正式 evidence validator 的成功僅能證明 ledger 結構及宣告狀態，不能自行證明 raw evidence 真實。Synthetic fixture 不構成 Claude live evidence。
- 最後三個測試修正僅同步當前契約：Claude canonical conformance 存在且版本為 1.4.0、狀態為 unverified、規則集合相符；Generic 保留無從屬／背書語意；START-HERE 保留版本與三平台入口。未改動 production 或刪除真實 evidence 驗收。

## Approved criteria 對照

| Criteria | 本次結論與證據 |
| --- | --- |
| DOC-01 | 九份指南七章順序一致，首次安裝區沒有更新步驟，開始章節包含可貼上例子；人工走讀與文件整合測試相符。 |
| DOC-02 | 三平台安裝／入口／模式／更新／停止使用／排錯完整；Claude 保留兩入口、4.6+／2.1.251+／Node 22+ 及 session-only；Generic 使用完整工作流貼入。 |
| DOC-03 | Full／Lite 詳解統一導向 beginner guide；Claude 三語進階參考保留 routing／Config／review／platform／lifecycle 細節及往返連結。 |
| DOC-04 | README bytes 不變，十二份 START-HERE 版本與入口一致，ZIP 錨點與固定版本套件文件連結可離線對應來源。 |
| VER-01 | Core、三種 adapter、catalog、runtime、封裝與文件版本一致為 1.4.0；錯誤版本／缺少必要 check／舊 preview helper 邊界的測試通過。 |
| VER-02 | 既有歷史 artifacts、原始來源 hash／日期及相依版本保留；衍生 hash 與現行 mapping 相符，現行使用文件沒有 preview 類版名。 |
| PKG-01 | 兩次三套件建置、81 個檔案、三個 ZIP／checksums 與來源 parity 相符；完整 suite 驗證 upgrade／inventory／rollback。唯一 host-permission skip 如上明列。 |
| EVD-01 | Claude conformance 維持 unverified，必需 checks 未取消；本次沒有生成冒充實測的 passed ledger 或正式 Completed release evidence，遠端發布狀態未宣稱。 |

## 十二個 Architecture and Refactoring Lenses

| Lens | Outcome | 本次範圍內的證據 |
| --- | --- | --- |
| 1. Duplicated Code or Policy | no-finding | Runtime 與驗證器的版本／semantic hash 有對應檢查；新 build fixture 集中隔離建置，共同 Full／Lite 詳解連到單一 beginner guide。沒有新增不同步的行為規則。 |
| 2. Long Function | no-finding | Production 僅在既有 output validator 加入十行選擇分支，驗證與 commit 責任仍分開；文件測試仍按可觀察契約分組。 |
| 3. Large Module or Class | no-finding | Builder 未加入發布或真實模型驗證責任；本次增加的 Claude 參考文件承接進階內容，未擴大主指南責任。 |
| 4. Long Parameter List | not-applicable | 本次 production 沒有新增或擴張 function signature；升級沿用既有 root／config／selected 介面。 |
| 5. Data Clumps | no-finding | Provider directory／archive 仍由 release config 管理，升級分支只處理既有 provider 名稱集合；未形成新增的跨模組資料搬運。 |
| 6. Primitive Obsession | no-finding | 版本使用既有 strict-semver／lockstep 驗證，provider 與 required checks 使用固定集合，錯誤版本與缺項仍拒絕。 |
| 7. Feature Envy | no-finding | 既有輸出驗證仍由 builder 負責，Claude payload／inventory 驗證委由既有 claude_package helper；沒有跨越新的資料所有權。 |
| 8. Divergent Change | no-finding | 變更集中於 approved 版本、文件與封裝整合，未引入 installer、host routing 或 release publication 新功能。 |
| 9. Shotgun Surgery | no-finding | 三語與多 provider 版本需同步是既有契約；共同細節集中並用整合測試檢查，未新增需要多處修改的新 runtime policy。 |
| 10. Message Chains | not-applicable | 變更未引入新的物件導航或連續服務呼叫，只有本機 config／檔案／ZIP 與純測試 helper。 |
| 11. Leaky Abstraction | no-finding | current_distribution 封裝隔離 test build；文件明確區分 Marketplace、session-only ZIP、Generic 貼入與 offline/live 證據界線，無需使用者推測內部狀態。 |
| 12. Shallow Module | no-finding | 新 test fixture 以單一無參數介面集中建置、錯誤處理與清理；production 沒有新增只轉傳參數的模組。 |

以上是本次變更與相關影響面的審查，不是整個系統的架構健康證明。

## 驗證證據與缺口

已閱讀本次目錄中的 `t1-red.log`、`t1-green.log`、`t1-broader.log`、`t3-release-red.log`、`t3-release-green.log`、`t3-doc-red.log`、`t3-doc-green.log`、`t3-doc-preservation.log`、`t3-builds.log`、`t3-validators.log`、`t3-full-suite.log`、`t3-corrections-green.log` 及 `t3-full-suite-final.log`。Focused 文件測試為 35 tests 通過；release focused log 為 82 tests 通過。最終完整 suite 為 394 tests／131.431 秒／`OK (skipped=1)`／exit 0。

第一輪正確 discovery 的四項 failures 為 canonical conformance 的舊不存在預期、Generic attribution 舊措辭、START-HERE 舊 slogan、當時尚未建立的 Review 連結。修正套件第一次 43 tests 出現 test code 誤從 behavior module 取 yaml 的 error；改為直接 import yaml 後該項通過，最終完整 suite 亦涵蓋四項修正。最初誤加 `-t .` 的 namespace-root discovery 錯誤保留，並未混算成通過。

`t3-release-red.log` 中既有雙套件原子升級測試確實因「Unmanaged or incomplete output collision」失敗，最小 builder 修正後通過。舊文件契約失敗記錄只證明舊預期與核准的新文件不相符，不冒稱 Ticket 2 做過 test-first 開發。

沒有執行或宣稱 Ticket 2 行為測試；本次文件整合屬使用者已核准的 Ticket 3。兩次 ZIP 可重現性及來源 parity 已獨立重算，無需重建或改寫歷史 dist。

尚無本次真實 Claude host／model／independent reviewer／完整 install-update-remove-recovery 結果，沒有檢查遠端 v1.4.0 tag／assets 是否存在。正式 release 仍須另外取得所需 raw evidence；現行來源、離線 fixture 及本 Review 均不能解除此門檻。

## 完成判定

Ticket 3 的核准來源、文件、離線整合與如實證據範圍已滿足，可完成本次 Ticket 並交付。Ticket 2 仍為 `tests: skipped-by-user`，本次整合測試屬 Ticket 3。既有 Claude adapter 的登入實測、正式 release Completed 與遠端發布仍有獨立門檻；本報告不解除那些門檻，也不將該計畫全部 Tickets 標為完成。
