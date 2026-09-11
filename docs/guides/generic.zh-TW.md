# Ask Then Do It Generic 使用說明

適合 Gemini 或其他能接收長文字的 AI。貼上工作流即可使用，不需安裝 Plugin。

以下為 1.4.0 的安裝／下載目標；若遠端尚未提供，請等待發布。

## 安裝與準備

下載並解壓縮套件，保留 `generic-workflow.md` 與 `prompts/`。

[下載 ask-then-do-it-generic-1.4.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0/ask-then-do-it-generic-1.4.0.zip)

## 開始使用

每個新對話都先貼上 `generic-workflow.md` **全文**，再說明需求，例如：

```text
幫我建立一個預約網站，請使用繁體中文。
```

## Full／Lite 模式

**Full** 適合需要需求、規格與工作規劃紀錄的工作，實作前有三個核准點。**Lite** 適合範圍清楚的改動，使用簡短變更摘要與一次核准。

直接說「這次使用 Full」或「這次使用 Lite」即可，只影響這次操作。

在工作流中保留唯一一行 `Default workflow mode: full`，或改為 `Default workflow mode: lite`。這是貼入文字的設定，不讀取 Codex／Claude 設定檔。沒有有效宣告時使用 Full。

完整流程、測試選擇與保存進度請看 [初學者流程](getting-started-simple.zh-TW.md)。

## 可用指令

一般只需 `generic-workflow.md`。熟悉流程後，可以貼上 `prompts/` 中的單一模組；指定模組不會跳過模式判定或核准。

<details>
<summary>查看進階入口</summary>

| Prompt | 用途 |
| --- | --- |
| `bootstrap.md` | 判斷目前進度並找到下一階段 |
| `orchestration.md` | 協調完整流程 |
| `lite-workflow.md` | 模式判定後引導完整 Lite 流程 |
| `requirements.md` | 一次問一個需求問題 |
| `documented-requirements.md` | 問需求並整理長期專案知識 |
| `specification.md` | 將已核准需求整理成規格 |
| `ticket-planning.md` | 將規格拆成垂直 Tickets 並批次取得是否加上測試的選擇 |
| `direct-implementation.md` | 提供不執行行為測試的直接實作指引 |
| `tdd-implementation.md` | 依 Ticket 準備測試與實作 |
| `review.md` | 根據提供的內容進行 Review |
| `architecture-improvement.md` | 分析架構問題與改善方向 |

</details>

## 更新與移除

取得新版 ZIP，之後在新對話改貼新版工作流。要停止使用，只要不再貼入；需要時可刪除下載副本。請自行保留專案文件。

## 常見問題

- 新對話沒有之前的進度：重新貼上工作流；延續 Full 時再貼已保存的需求、規格與工作規劃。Lite 不自動保存跨對話狀態。
- AI 不能修改檔案或跑測試：能力取決於你使用的服務與工具；只有聊天時，需自行套用內容並提供結果。

仍有問題時，可在 [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues) 提供專案版本、使用的 AI 服務／主程式、平台與重現步驟。

## 授權與來源

本專案受到 Matt Pocock 的 skills repository 啟發，與其沒有從屬或背書關係。授權與來源請見 `LICENSE` 與 `THIRD_PARTY_NOTICES.md`。

[回到 README](../../README.md)
