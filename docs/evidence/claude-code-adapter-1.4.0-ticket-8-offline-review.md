# Claude Documentation Offline Independent Review

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-8-offline-review`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0` (Review envelope; Approved baseline `1.3.1`)

Status: Reviewed — offline documentation accepted；final host/behavior reconciliation pending。

Review label: `independent`

Approved implementation mode: `tdd`

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md) sections 3、6–8、13–14；Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 8 與 2026-09-09 離線核准順序；README 與三語 root／simple-guide insertions；三份 `docs/guides/claude-code.*.md`；三份 Claude Plugin START-HERE；`tests/claude/test_documentation.py`；platform-support source ledger／captured excerpts；shared `validate_claude_plugin.py` START_GUIDES change 與 focused public-contract test。

Assumptions: 本次 Full fallback／multi_agent 與 Approved `tdd` 由協調者證明。Reviewer 未編寫文件、documentation tests、platform sources 或 shared START_GUIDES validator change；相關 package builder 是此 reviewer 另行實作，因此本報告不對 builder 提供 independent verdict。文件已由 owner explicit freeze 後檢查。

Deferred: 官方來源重新 network fetch、exact 2.1.251 authentication／hook execution、兩入口 surface實測、model behavior／paired equivalence、正式 context結果、final candidate bytes 的文件核對、完整 Ticket 8 completion。

Handoff: 接受目前明示未發布與未驗證限制的離線文件；取得實際 host/model observations 後再同步最終 guide claims。Shared START_GUIDES inventory integration 可保留，final release completion gates 不變。

## Findings

沒有 actionable finding。三語新增內容在版本要求、route branches、Full/Lite Config、reviewer能力、read-only status、explicit install/update/remove authority、fresh recheck、disabled／newer／partial failure、last-scope data、session-only ZIP與platform限制上語意一致。完整 Ticket 8 尚需最後的 host／behavior結果核對。

README diff 只在三語既有對應位置加入 Claude development段落與guide link，保留原 section 順序、Codex/Generic內容與1.3.1下載。Root START-HERE與simple guides同樣採局部插入。三份詳細指南先揭露1.4.0未發布，安裝命令區再次標為未來正式版參考；沒有v1.4.0 download link或現有正式Marketplace可安裝的聲稱。短START-HERE連到same-version future guide，清楚說該tag連結發布後才可用，開發時讀matching source checkout。

兩個namespaced entries、`model: inherit`、unknown／unsupported／failure差別、bounded Node fallback與operation-bound profile語意一致。Lifecycle指令使用qualified identity/user scope，Marketplace refresh沒有硬加不支援scope flag；每次write前仍須fresh完整state。ZIP不建立persistent Marketplace/personal Skill。`/doctor`只作Claude Code health，沒有Skill轉換聲稱。

Platform來源ledger包含七份有日期官方URL、normalized snapshot SHA-256與十二格surface/feature matrix。Reviewer檢查引用句在captured sources存在，VS Code subset/bundled CLI、JetBrains integrated-terminal邊界與文案一致；不把文檔支援當exact minimum版本或nine-combination live evidence。本次未重新抓取遠端來源，因此只能驗證保存證據及引用一致性。

Shared validator 現在要求恰好三份 START-HERE 位於 exact root inventory，以既有 containment/link guard和regular-file check驗證；missing、directory replacement、extra locale都拒絕。沒有增加public Skill component或改route logic。

## Verification

```text
.venv/Scripts/python.exe -B -m unittest tests.claude.test_documentation -v
Ran 5 tests in 0.027s
OK

.venv/Scripts/python.exe -B -m unittest tests.claude.test_public_plugin_contract.ClaudePublicPluginContractTests.test_validator_requires_three_regular_start_guides -v
Ran 1 test in 0.515s
OK
```

均 exit `0`。Documentation tests包含原文字移除插入後的baseline hash、三語required-section與wrong-version/extra-command/未發布下載等negative cases、十二份source START-HERE inventory、local links及dated source引用檢查。Reviewer另逐語閱讀三份指南／短START-HERE與README raw diff；沒有只以關鍵字匹配判定語意。既有完整documentation suite由owner執行，未在此重複。

## Twelve lenses

| Lens | Outcome | Evidence |
| --- | --- | --- |
| Duplicated Code or Policy | no-finding | 三語重複是明確localization contract；同一semantic section inventory協助同步，shared workflow詳情以guide link交接。 |
| Long Function | no-finding | Tests按guide、evidence、layout、links分工；validator reuse既有containment helper。 |
| Large Module or Class | no-finding | 詳細guides以既有專屬Claude範圍分節；短START-HERE維持導覽職責。 |
| Long Parameter List | not-applicable | 文件變更沒有新增複雜runtime介面；checker只接body/locale或ledger/root。 |
| Data Clumps | no-finding | Platform source與matrix引用有明確結構，版本要求以相同三項表達。 |
| Primitive Obsession | no-finding | Surface/feature/status集合與date/hash有驗證；未用文字pass取代live evidence。 |
| Feature Envy | no-finding | Claude guides連到provider-neutral workflow，沒有重寫Codex/Generic owner。 |
| Divergent Change | no-finding | Source doc插入與Claude provider guide界線清楚，未改runtime behavior。 |
| Shotgun Surgery | no-finding | 三語與入口頁的變更面為Approved inventory，tests保護無關baseline內容。 |
| Message Chains | no-finding | Short START-HERE直接連same-version完整指南，沒有多層必需跳轉才能辨認未發布限制。 |
| Leaky Abstraction | no-finding | Node/manual-path與session-only旗標是使用者做選擇必要條件，未暴露內部state檔案細節。 |
| Shallow Module | no-finding | 指南提供完整Claude使用邊界，short entry保留用途與限制後交接詳細內容。 |

Residual risk: keyword／section tests不能證明所有未來自然語言改動都正確，仍需逐語Review；future tag links目前刻意不可用且已披露。Schema通過與目前官方文件均不能證明目前source在exact host上的實際命令／hook／model行為。

## README historical-hash integration correction

獨立 Review 結果：**accepted，沒有 actionable finding**。此補充只評估協調者新增的 `tests/release/test_command_install_docs.py` integration change；本 reviewer 未實作該變更。

原有 preservation test 將已核准的新 Claude 段落計入既有 README hashes而失敗。新的 `preserved_readme_content` 只有在六段 insertion 的 SHA-256、順序與完整 begin/end marker 數全部相符時才排除它們；既有 `README_PRESERVED_DIGESTS` 未修改。任意 marker 內容不能成為 exemption。沒有 Claude markers 的舊 README 可原樣接受，讓既有歷史內容仍可驗證。

Reviewer 自行執行：

```text
.venv/Scripts/python.exe -B -m unittest tests.release.test_command_install_docs -v
Ran 6 tests in 0.004s
OK
```

Exit `0`。另外用 AST 比較 `HEAD` 與目前測試的 `README_PRESERVED_DIGESTS`，確認完全相同；將目前 README 經受控排除後與 `HEAD:README.md` 的完整 normalized bytes 比較，也完全相同。此檢查只作獨立原始碼驗證，沒有把 git HEAD 加成正式 tests 的新依賴。

四個獨立記憶體 mutations——交換兩段順序、附加一段重複 insertion、刪除一段、修改核准段落內空白——均被 helper 拒絕。另修改 insertion 之外的原始 Introduction 文字，確認排除後仍保留該變更、與原 README 不同；原有 hash／heading checks仍可偵測它。Reviewer 沒有修改 source 或 tests，也未重跑中央 full suite。

十二 lenses 沿用本報告的原 scope，補充檢查未改變結果：固定六段 hash 是有界的 approved-content reference；helper保持單一職責，未把舊 hash更新為新輸出，沒有引入新runtime介面、host dependency或跨module mutation。Candidate與新 hash 同時變更仍須重新Review，這項靜態檢查本身不提供approval authority。
