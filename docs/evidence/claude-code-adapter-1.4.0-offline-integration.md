# Claude 離線優先開發整合

Artifact type: Integration Evidence

Artifact ID: `claude-code-adapter-1-4-0-offline-integration`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0` (workflow envelope；authoring baseline `1.3.1`)

Status: 本輪離線準備完成；獨立複查修正 accepted，最終回歸通過。完整 Claude／1.4.0 release 驗收仍待實際執行。

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md)、[Ticket Plan](../plans/claude-code-adapter-1.4.0.md) 與 2026-09-09 使用者核准「先做完能離線準備的部分，再集中真實驗收」；十張 Ticket 的 `tdd` 選擇不變。

Assumptions: project/user workflow Config 不存在，依 Full fallback；具備 repository 工具與隔離 agents，能力為 `multi_agent`。各 implementation ownership 分開，相關 reviewer 未實作受審範圍。

Deferred: 登入／模型呼叫、Ticket 3 exact-host authenticated behavior、兩 profiles 各 30 scenarios 與 12 paired／雙向 authority 的實際結果、正式 context gate、lockstep current version activation、default `dist/`、正式 release candidate freeze、final smoke、publication。

Handoff: 交付可執行的離線工具、未執行驗收套件與 preview ZIP。後續取得真實 Claude evidence，再完成正式 context、文件核對、lockstep 版本整合與 final smoke。完整 Tickets 3–10 與 local release 的必要門檻仍保留。

## 本次交付

- [Ticket 6](claude-code-adapter-1.4.0-ticket-6-offline.md)：staged 30-rule conformance、兩 profiles 情境／paired／authority 的共用驗證工具、131 subcase recipes、86 組未執行提示及結果模板。
- [Ticket 7](claude-code-adapter-1.4.0-ticket-7-offline.md)：行為證據優先的 context 計算器、10 scenarios／11 checkpoints 模板；合成資料只供工具測試。
- [Ticket 8](claude-code-adapter-1.4.0-ticket-8-offline.md)：三語完整 Claude guides、Plugin START-HERE、README/root/simple guides 最小插入與有日期官方 surface 資料。
- [Ticket 9](claude-code-adapter-1.4.0-ticket-9-offline.md)：沿用既有 builder 的 Claude-only 隔離 preview、exact source/package/ZIP inventory、hashes 與 transaction/recovery。

正式 activation 所需的 current release config、Core／Codex／Generic identities、canonical Claude conformance、default `dist/` 及 historical `1.3.1` 保持既有狀態。這次新增的是可使用的準備工具與 preview，不是正式發佈。

## Shared Plugin START-HERE 整合 Red / Green

文件新增 Approved Specification 所需的三份 Plugin START-HERE，使 shared validator 的既有七項 root inventory 需要擴充。先加入正向三檔接受、missing guide、directory 代替 file 與額外 guide 拒絕測試：

```text
.venv/Scripts/python.exe -B -m unittest tests.claude.test_public_plugin_contract.ClaudePublicPluginContractTests.test_validator_requires_three_regular_start_guides -v
Ran 1 test in 0.171s
FAILED (failures=1)
```

Red exit `1`，錯誤為舊 exact inventory 拒絕三份合法文件。只擴充 exact `START_GUIDES` inventory，保留 containment／non-link 並要求 regular file 後：`Ran 1 test in 0.688s; OK`，exit `0`。

三份實際 source 文件完成後，canonical `scripts/validate_claude_plugin.py` exit `0`。Context／public contract 合併 focused suite：`Ran 24 tests in 19.695s; OK`，exit `0`。後續 calculator independent finding 的修正另記 Ticket 7 evidence 與最終回歸。

## 尚未執行的驗收套件

本機 `.claude-offline/verification/` 已由 prepare CLI 產生 86 組提示、pending ledger 與空 transcript directory；`.claude-offline/context/capture.json` 是 unobserved template。

對 prepare 結果執行正常 behavior validate，觀察 exit `1`：`actual evidence required; unexecuted/synthetic records cannot pass the actual gate`。Context 計算同樣 exit `1`、`status: blocked`、`release_pass: false`、`measurements: []`。這是未執行資料的正確拒絕，不是測試失敗被忽略。

## 保留的使用者變更

`docs/project/knowledge-base.md` 原有修改保持不變；SHA-256 為 `D64B538EE04C65FC829891A37F5BB1FD7D6A00E44A18B406E1CDE8A7B130A062`。本次順序更新只記在 Specification／Plan，沒有覆寫既有 Knowledge Base。Claude adapter 和多數 evidence 是未追蹤檔，不能用 tracked diff alone 宣稱整個工作樹乾淨。

## Native 與輔助驗證

最終三份 Plugin START-HERE 完成後，以既有 exact Claude Code `2.1.251` binary 在獨立 temporary `CLAUDE_CONFIG_DIR` 執行 `--version`、canonical Plugin `plugin validate --strict`、repository Marketplace `plugin validate . --strict`，全部 exit `0`；兩次 validation 都回報 `Validation passed`。停用 auto-updates／nonessential traffic／telemetry，沒有登入、安裝或模型呼叫。Temporary config 經 absolute containment check 後清理。

Model-classification evidence validator exit `0`，`node --check router.mjs` exit `0`，`git diff --check` exit `0`；Git 僅回報 Windows LF/CRLF warnings。Current `release/release.json`、Core／Codex／Generic 與 default `dist/` 的 scoped diff 沒有變更。

## Full regression 暴露的 README 歷史保護整合

第一次完整回歸觀察：`Ran 390 tests in 133.443s; FAILED (failures=6, skipped=1)`，exit `1`。六個 failures 全來自 `test_readme_preserved_blocks_are_independent_of_git_head`，三語 automatic／read-more sections 納入已核准的新 Claude 段落後不再與舊 section hash 相同。沒有將這次 run 列為成功。

修正只改 test extractor：六段已獨立審閱的新增內容用固定 SHA-256／順序與 exact marker count 限定，排除後繼續驗證原有的全部 `README_PRESERVED_DIGESTS`。沒有刷新歷史 hash、刪除斷言或修改 README。新負例拒絕 Claude 段落改寫、任意額外 marker、missing marker；Codex 指令改壞仍導致原 hash 不符。

Focused command：`.venv/Scripts/python.exe -B -m unittest tests.release.test_command_install_docs tests.claude.test_documentation -v`，觀察 `Ran 11 tests in 0.026s; OK`，exit `0`。原文件獨立 reviewer 另執行 6 tests／0.004s 全通過，確認歷史 hash constants 與 HEAD 完全相同、排除六段後 README bytes 完整恢復原文；四種獨立 mutations 被拒絕，修正已接受。完整回歸重新執行。

## Preview artifact

兩次 canonical-source 隔離 build 的 35 個輸出檔案 bytes 完全相同：32 個 runtime/legal payload files、一個 ZIP、一份 checksum、一份外層 preview marker。Marker 不進 ZIP。

保留 `.claude-offline/package/claude/ask-then-do-it-claude-1.4.0-preview.zip`，55,573 bytes，SHA-256 `6c83d5b712b34c00131ad92c745f47cd57a49da7e63fc0a5ec7337b9c7c61348`。Root 另驗 archive hash 與 checksum 相同、marker 為 `not-a-release`。這不是正式 `1.4.0` release 或已通過模型測試的安裝包。

舊 Generic template 的兩個 Markdown hard-break 空白改寫為明示 `\x20\x20` source escape，前後生成 bytes 的獨立比較完全相同；此 source-format 整理不改 Generic package。補充掃描 84 個 source/test files 沒有 trailing whitespace，66 個本輪 artifact local links 可解析。

## 獨立 Review closure

| 範圍 | 結果 | 修正與證據 |
| --- | --- | --- |
| [Ticket 6](claude-code-adapter-1.4.0-ticket-6-offline-review.md) | 離線工具 accepted | Paired 完整 user／approval inputs 必須相同；authority responses 與 citations 必須在所屬 operation span。14 focused tests 通過，reviewer 另重驗原反例及合法 approval／stop-reset paths。 |
| [Ticket 7](claude-code-adapter-1.4.0-ticket-7-offline-review.md) | 離線工具 accepted | 合法同 profile 額外 stage 必須納入計數；11 tests 通過及獨立 mutation 確認。 |
| [Ticket 8](claude-code-adapter-1.4.0-ticket-8-offline-review.md) | 離線文件及 README 整合 accepted | 三語／layout／dated sources、shared START-HERE inventory 與 README 歷史保護皆經獨立檢查。 |
| [Ticket 9](claude-code-adapter-1.4.0-ticket-9-offline-review.md) | 離線打包 accepted | ZIP extra directories、特殊檔案模式與非canonical metadata 均拒絕；reviewer 對 candidate／prior-preview 共 10 個變異觀察皆遭拒，existing default dist 唯讀驗證通過。 |

上述 acceptance 僅適用本輪離線準備；沒有任何真實 model behavior、50% reduction 或完整 release completion 聲明。所有 Required live gates 仍保留。

## 最終整合驗證

全部 source/test 修正凍結後，重新執行：

```text
.venv/Scripts/python.exe -B -m unittest discover -s tests -p 'test_*.py'
Ran 391 tests in 125.151s

OK (skipped=1)
```

Exit `0`：390 tests 通過、1 項略過，沒有失敗。略過項是 `ClaudeRouterSecurityTests.test_state_file_symlink_is_not_followed`；本 Windows host 缺少建立符號連結權限，focused verbose check 回報 `WinError 1314`。該項仍是未取得的安全驗證證據，未改權限或將 skip 算成通過。

最後再次對現有未執行 kit 使用新版 validators，確認 behavior 仍拒絕 unexecuted evidence，context 仍回報 `measurements: []`／`release_pass: false`。沒有以 synthetic 測試或完整工具回歸通過來替代真實模型結果。
