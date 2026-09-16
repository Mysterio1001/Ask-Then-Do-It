# 發布歷史與原始文件索引

這是歷史結果摘要，不是新 release 的 Completed evidence。每次發布仍需使用當時的 source、config、raw verification 與 candidate hashes；不把舊 passed checks 套用到 1.4.0。現況見[狀態文件](../project/status.md)。

## 已有發布紀錄

| 版本 | 主要交付 | 歷史驗證 ledger |
| --- | --- | --- |
| Grill Me 1.0.0 | clean-slate workflow、Codex 與 Generic 的最早期結構 | [原 ledger](grill-me-release-1.0.0.json) |
| Ask Then Do It 1.0.0 | 名稱、來源歸屬與兩平台套件統一 | [原 ledger](ask-then-do-it-release-1.0.0.json) |
| 1.1.0 | Ticket「加測試／不加測試」選擇及 direct 路徑 | [原 ledger](ask-then-do-it-release-1.1.0.json) |
| 1.2.0 | command-installable Marketplace、state-aware updates、品牌圖示 | [原 ledger](ask-then-do-it-release-1.2.0.json) |
| 1.3.0 | Full／Lite、Config precedence、Codex tools 固定 60% workflow token proxy；Generic 共同固定成本單列，不宣稱 60% 縮減 | [原 ledger](ask-then-do-it-release-1.3.0.json) |
| 1.3.1 | 明確 Pillow 開發依賴、Windows bounded retry／rollback／recovery preservation | [原 ledger](ask-then-do-it-release-1.3.1.json) |
| 1.4.0-preview.1 | Claude 單平台離線 candidate 的歷史公開發布 | [2026-09-09 發布收據](claude-preview-publication-1.4.0-preview.1-receipt.md) |
| 1.4.0 | 三平台來源與文件對齊、離線建置整合 | [整合 Review](documentation-and-version-alignment-1.4.0-ticket-3-review.md)；完整 Claude／release gates 尚未完成 |

六份 JSON ledger 保留原始 bytes。早期 Markdown 中的 local completion 不自動證明當時或目前遠端已發布。Preview 收據記錄當時 GitHub API／下載比對，不能當成正式 1.4.0 發布證據；本次整理沒有重新查核遠端。

## 歷史候選 archive hashes

以下 hashes 逐字擷取自清理前各版 Markdown，只用於識別當時產物，不描述本次 candidate。完整命令、outcome、授權與限制在原始快照。

### grill-me-release-1.0.0

```text
4bd9733c50224aaeef7f6f0ded125a18c81340a3c31f99bf80396c324583d26e  codex/grill-me-1.0.0.zip
a8f22fcf80d9a0fee1c4cee85c7272f55e81f1bf40d203d55389e49de97af53b  generic/generic-prompts-1.0.0.zip
```

### ask-then-do-it-release-1.0.0

```text
3f7b83d697cb5d431693d76cce79500622d1fd4db45828317b71c5e03e817721  codex/ask-then-do-it-1.0.0.zip
a65d8c0282ba2b3ec51b891ae26255aaef1031673bddf29ac8dfc41ef6b7f436  generic/ask-then-do-it-generic-1.0.0.zip
```

### ask-then-do-it-release-1.1.0

```text
bc98595ddde5b06ae2a0d4419c5ef1dc95cc9a495b18047d50ced9f6ce547dc4  codex/ask-then-do-it-1.1.0.zip
0cd6b9dd87c6dd262c67a7def05882c3463210c38296289b5c4b16ac160a7326  generic/ask-then-do-it-generic-1.1.0.zip
```

### ask-then-do-it-release-1.2.0

```text
c5b19837336ba1ac54407a1d0878a1d552921ba45e4e9adafcf0c1a2013048f2  codex/ask-then-do-it-1.2.0.zip
b9b27fafddd80f60b4e2818f3d61757146973d41bee345a65d00ef1b18e99af0  generic/ask-then-do-it-generic-1.2.0.zip
```

### ask-then-do-it-release-1.3.0

```text
7f80461578791c25d07f81bbddebf6ec5ca30ae7f1f816335c77330d7045d19d  codex/ask-then-do-it-1.3.0.zip
511ecccadb39ced89182ce55c4dd96f2571a59928fdb374829b0c5d6e4f0bebd  generic/ask-then-do-it-generic-1.3.0.zip
```

### ask-then-do-it-release-1.3.1

```text
557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209  codex/ask-then-do-it-1.3.1.zip
6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b  generic/ask-then-do-it-generic-1.3.1.zip
```

## 關鍵 Review 與問題處理

| 範圍 | 保留紀錄 | 解讀限制 |
| --- | --- | --- |
| Claude manifest／Marketplace | [Ticket 1 correction](claude-code-adapter-1.4.0-ticket-1-marketplace-description-correction-review.md) | strict description 修正已接受，非模型實測 |
| Claude router／state | [Ticket 2 tenth correction](claude-code-adapter-1.4.0-ticket-2-review-after-tenth-corrections.md) | provisional host 契約；原 review-final 仍是 changes-requested，因此依最後實際狀態保留 |
| exact host | [Ticket 3 Review](claude-code-adapter-1.4.0-ticket-3-review.md) | 工具修正可接受；authenticated observations 仍阻擋完整 Ticket |
| General profile | [Ticket 4 correction](claude-code-adapter-1.4.0-ticket-4-review-after-third-correction.md) | correction accepted，不是完整 behavior pass |
| Claude 5 profile | [Ticket 5 correction](claude-code-adapter-1.4.0-ticket-5-review-after-third-correction.md) | correction accepted，不是完整 behavior pass |
| 1.4.0 文件／版本整合 | [Ticket 3 Review](documentation-and-version-alignment-1.4.0-ticket-3-review.md) | 來源／文件／離線驗證範圍；live gates 保留 |

已修問題與測試的對照集中在[驗證手冊](../maintainer/validation.md#重要修正與回歸測試對照)。既有架構診斷中尚未接受的提案移入[狀態](../project/status.md#可選的後續改善)，不因舊報告移除而消失或被視為已實作。

<a id="document-sources"></a>
## 合併來源與決策追溯

文件整理已於 2026-09-10 由使用者看過逐檔去向後明確回覆「核准 開始執行」。只變更維護文件組織，不改變 Full／Lite 的產品 artifact／approval 契約，也沒有把 consolidated 文件假設成另一次 Approved 行為規格。

| 原始文件群（檔名可在快照搜尋） | 主要承接位置 |
| --- | --- |
| grill-me-clean-slate-1.0.0、ask-then-do-it-1.0.0 的 requirements／specs／plans | [流程規格](../specs/workflow.md)、[知識庫](../project/knowledge-base.md) |
| optional-ticket-testing、lite-workflow-mode-1.3.0 的 requirements／specs／plans | 流程規格、既有三語設計與初學者指南；原始測試選擇核准留在快照 |
| command-install-update-1.2.0、release-1.3.1-maintenance | [發布手冊](../maintainer/releasing.md)、知識庫、JSON ledger |
| claude-code-adapter-1.4.0 的 requirement／spec／plan／研究 | [Claude 規格](../specs/claude-code-adapter.md)、[狀態](../project/status.md)、知識庫 |
| documentation-and-version-alignment-1.4.0 | 發布手冊、狀態及保留的整合 Review；原三 Ticket 的 tdd／direct 選擇仍可追溯 |
| github-release-publication-1.0.0、claude-preview-publication-1.4.0-preview.1 | 發布手冊、歷史摘要與 preview receipt |
| Codex skill runtime slimming lifecycle migration (2026-09-16) | [Decision Packet](../project/drafts/codex-skill-runtime-slimming/decision-packet.md)、[lifecycle manifest](../project/drafts/codex-skill-runtime-slimming/lifecycle-manifest.json)、[source manifest](../project/drafts/codex-skill-runtime-slimming/migration/source-manifest.json)；原三份草稿仍為 Draft/Pending，未視為新的核准 |
| docs/project/drafts 的既有 working-notes／kb-change-summary | 知識庫與狀態；只採用有正式依據的事實，不把研究 proposal 當正式要求 |
| docs/claude_sys/behavior-verification.md | [驗證手冊](../maintainer/validation.md#claude-behavior-證據)的操作／transcript 格式 |
| docs/evidence 的逐 Ticket、Review、correction、architecture 紀錄 | 本頁、驗證手冊、狀態與保留的七份關鍵 Review／receipt |
| claude-code-reference.en／zh-TW／ja | 各自同語言 [Claude 指南](../guides/claude-code.zh-TW.md#advanced-reference)收合區塊 |

原始 artifact ID、approval 日期、上游引用、raw command／result 與舊 hash 沒有重寫：可按原路徑從快照恢復。保留 Review 的導航若改指新摘要，會附歷史導航說明；摘要不冒充該次 reviewer 當時讀過的文件。

<a id="archive"></a>
## 歷史快照與復原

本機快照 ID：`repository-cleanup-2026-09-10`。維護者另行保存的 `cleanup-execution/` 包含：

- `before-cleanup.zip`：2055 份原始檔，涵蓋當時來源、docs、tests、HTML、一次性工具、快取與 `.claude-offline` 原始證據；逐檔重新讀取驗證 SHA-256。
- `backup-manifest.json`：每個原始相對路徑、bytes 與 SHA-256，以及 archive SHA-256。
- `document-actions.json`、`approved-plan.md`：218 份文件的完整處置、合併去向與核准清單；不放入 consumer ZIP。
- `git-status-before.txt`、`git-diff-before.patch`：原本未提交狀態。未追蹤檔案也在 archive 中，不能只靠 Git diff 還原。

Archive SHA-256：`e5e2dad06ea02416521b3f991d821e96406f619e1cc35d408c97750246c378aa`。

快照保存在本機專案之外的 Codex visualization 工作目錄，交付回報提供可點擊位置；維護者搬移專案時需一併保管此備份。它不在 repository／consumer ZIP，也沒有上傳。`.git`、`.venv`、`.ticket3-preflight`、`dist` 未納入此清理快照，因本次不清除或修改這四個頂層目錄；它不是整台機器的完整備份。

復原時先核對 archive 與 manifest，再把需要的原相對路徑解壓到另一個新目錄比對。不要直接覆蓋已有新工作。歷史原文缺少時，將需重新核准／驗證的範圍標為 unavailable，不靠新摘要猜測舊 approval。

[回到 README](../../README.md)
