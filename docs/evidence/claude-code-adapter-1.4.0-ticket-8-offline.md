# Ticket 8：Claude 三語文件的離線準備

Artifact type: Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-8-offline`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`（implementation workflow contract；Approved product Specification 採 `1.3.1` baseline）

Status: Offline implementation accepted by independent Review; final host/behavior wording check pending. Ticket 8 not Completed.

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md) sections 13–14、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) 的 Ticket 8 與 2026-09-09 離線優先核准、既有 README／START-HERE／guide owners、既有 documentation tests、實際讀取的 dated Anthropic official documentation。

Assumptions: 本輪已證明 Full fallback、tools 與 multi_agent，Ticket mode 保持 Approved `tdd`。使用者核准先做能離線準備部分，未授權登入、模型呼叫、安裝、Marketplace 啟用或外部發布。`1.4.0` 仍是未發布的開發候選版本；canonical native strict success 不等於 model/live 成功。

Deferred: Ticket 3 exact-host authenticated behavior、兩 profiles 的 mandatory model observations、Ticket 6 paired/authority freeze 後的最終三語語意核對、九組 platform 的實際覆蓋與 final live smoke。Expanded/ZIP START-HERE copy equality 由 Ticket 9 preview builder 整合，這裡只驗證 source inventory/links/version/brevity。Local release 不可因此標 Completed。

Handoff: Source docs 已 freeze，[獨立 Review](claude-code-adapter-1.4.0-ticket-8-offline-review.md) 已接受文件及 shared START-HERE validator 整合。Ticket 9 負責 preview packaged-copy parity；任何後續修正須重新跑受影響 focused checks。Required host/model evidence 取得後仍需 final wording review；未將其假作本輪通過。

## 交付範圍

- README 的 English／繁中／日本語區塊各插入 Claude 說明與 read-more 連結，保留原本 Introduction、Quick Start、Automatic installation、nested Codex CLI、Manual installation、Read more 的順序與既有文字。
- 三個 root START-HERE 增加 Claude consumer choice；三個 getting-started-simple guides 保留共用 Full/Lite owner，只插入 Claude guide handoff。
- 新增 `docs/guides/claude-code.{en,zh-TW,ja}.md`，逐語覆蓋三種版本、未發布狀態、兩 namespaced entries、routing／operation／session、read-only Config、read-only reviewer downgrade、status／user-scope install/update/remove、ZIP session-only、平台差異及 troubleshooting。
- 新增 canonical Claude Plugin 三個簡短 START-HERE。Same-version `v1.4.0` guide／README links 明確標示發布後才可用；開發期使用 matching source checkout。沒有把不存在的 future release download 寫成可用入口。
- 新增 `tests/claude/test_documentation.py`；新測試覆蓋局部插入原文 hashes、三語 shared contracts、遺漏與 prohibited claim mutations、12 個 source START-HERE、relative links，以及 dated official feature evidence 的完整度與 quote/hash 一致性。
- 新增 [platform-support fixture](../../tests/claude/fixtures/platform-support/sources.json)，保存七個本輪實際讀取的官方頁面正文及十二個 surface/feature records。

## Red

先新增 documentation tests，再執行：

```powershell
& '.venv/Scripts/python.exe' -B -m unittest tests.claude.test_documentation
```

Observed exit `1`：

```text
EFEEEEF
Ran 5 tests in 0.039s
FAILED (failures=2, errors=5)
```

兩個 assertion failure 是既有 README 尚未出現 Claude insertions，以及 Claude Plugin START-HERE 不存在。五個 errors 是預期交付檔案不存在：platform evidence ledger、一個 link test 首次讀取 English guide，以及三語 guide case。這些是尚未實作的公開文件 boundary，不是 Python import、dependency 或 unrelated setup failure。

## Green 與相關回歸

完成三語文件與平台證據後，先跑新舊 documentation suites：

```powershell
& '.venv/Scripts/python.exe' -B -m unittest tests.claude.test_documentation tests.release.test_documentation
```

第一次 combined result：

```text
Ran 34 tests in 4.455s
FAILED (failures=3)
```

新 tests 已通過，但 root START-HERE 各多一個 level-2 heading，觸發既有每頁最多三個 heading 的 brevity contract。將新增 Claude choice 改成 bold lead，保留原有 headings 與 tests，沒有放寬門檻。

最終同一指令 observed exit `0`：

```text
..................................
Ran 34 tests in 0.246s
OK
```

這包含每語十一個 section omissions、最低 host 版本錯誤、額外 namespaced command、未發布 download link，以及 `/doctor`、ZIP persistent、九組 live claim 的反例。Document contract checks 是静態保護；翻譯語意由完整對照三語內容與 Approved contract 檢查，沒有把詞句存在冒稱實際模型行為。

既有文件的正規化原文 SHA-256 在移除明確 Claude insertion blocks 後完全一致。`git diff --stat` 觀察到既有七份檔案只有 72 insertions、零 deletions；新增 guides/fixtures 屬 untracked source，未假裝由 tracked diff 完整涵蓋。

Scoped `git diff --check` observed exit `0`，只有 Windows checkout 的 LF→CRLF 提示，沒有 whitespace error。沒有跑 full repository suite、native binary、build、login、paid model call、install、update、remove 或 external publication。Shared validator 的 START-HERE root inventory integration 由 root owner 處理，不在本 worker 修改範圍。

## 本輪官方文件證據

日期：2026-09-09。用 Python `urllib.request` 實際 HTTPS GET 官方頁面；最初 `plugins.md`、`vs-code.md`、`jetbrains.md` endpoints 各回 HTTP `403 Forbidden`。改讀正式 HTML URLs、設定 `User-Agent: Mozilla/5.0` 後成功。七頁為：

1. <https://code.claude.com/docs/en/plugins-reference>
2. <https://code.claude.com/docs/en/vs-code>
3. <https://code.claude.com/docs/en/jetbrains>
4. <https://code.claude.com/docs/en/skills>
5. <https://code.claude.com/docs/en/sub-agents>
6. <https://code.claude.com/docs/en/hooks>
7. <https://code.claude.com/docs/en/plugin-marketplaces>

擷取方法：Python HTMLParser 保留 `<main>` 內文字、排除 script/style，Unicode whitespace 合成 ASCII space，末尾一個 LF。Ledger 記錄每頁 URL、final URL、checked date、response SHA-256、保存正文 SHA-256。Twelve matrix rows 的 quotations 必須確實出現在相應保存正文；測試也拒絕偽造 live status、缺 row、無效日期。

官方可直接支持 terminal local Plugin 可含 Skills／Agents／hooks，VS Code 的 graphical Plugin management 與 shared host hooks。VS Code 明示 commands／skills 僅 subset、panel 與 standalone terminal CLI 不同；對 exact namespaced entries、Plugin reviewer invocation/isolation 與 exact hook behavior 保留 conditional/unverified。JetBrains 官方使用方式是在 IDE integrated terminal 跑 Claude CLI，因此以 CLI feature availability 的 conditional support 描述，沒有把 IDE integration 假作另一個已驗證 graphical runtime。

這是本輪官方 document observation，不是重用先前自述，更不是 exact 2.1.251 runtime 或九組 live OS/surface 結果。Current official pages 可能涵蓋較新版本，exact minimum 與最後 model/live gates 保留。

## 殘餘限制

文件說明預定的公開 lifecycle，但不執行這些指令，也不宣稱未發布 source/asset 已可用。下次取得真實 host、model、authority 與 smoke evidence 後，必須對照結果更新有變化的語意；若實際行為與 Specification 衝突，回最早 affected gate，而不是只改文案掩蓋。Ticket 8 保持未完成。
