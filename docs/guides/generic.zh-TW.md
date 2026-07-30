# Ask Then Do It Generic 使用說明

這份指南說明如何在 Gemini 或其他能接收長文字的 AI 使用 Ask Then Do It。Generic 版本不需要安裝 Plugin，只要在對話中貼上工作流。

## 下載與解壓縮

[下載 ask-then-do-it-generic-1.0.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-generic-1.0.1.zip) 並解壓縮。

套件內的主要檔案是：

- `START-HERE.zh-TW.md`：快速使用說明。
- `generic-workflow.md`：一般情況使用的完整工作流。
- `prompts/`：九個可個別使用的階段模組。
- `LICENSE` 與 `THIRD_PARTY_NOTICES.md`：授權與來源。

## 快速開始

每個新對話都依照下列步驟開始：

1. 開啟 `generic-workflow.md`。
2. 複製全文並貼到新的 AI 對話。
3. 說明你想完成的事情與偏好語言。
4. 如果要延續之前的工作，再一起貼上先前保存的重要文件。

例如：

```text
我想建立一個預約網站。
請使用繁體中文。
```

AI 的第一個有效回應會說明目前階段，接著提出第一個需求問題。每個問題都會附上建議答案與主要取捨；你不需要再輸入「開始」。

## 流程中的核准點

Ask Then Do It 會在三個地方等待你的明確核准：

1. 需求已經問清楚。
2. 規格正確描述預期成果。
3. Ticket 規劃可以開始執行。

第三個核准完成後，流程才會進入實作。若你要求修改，AI 會停留在目前階段調整內容。

## 能力限制

Generic 版本只會在對話中引導流程，不能直接修改你的檔案或執行測試。它會提供建議、文件或實作內容，但實際能否操作檔案，取決於你使用的 AI 服務是否提供相應工具。

Review 也只能依照你貼進對話的程式碼、文件與測試結果進行。缺少資料時，AI 應直接說明目前無法確認。

## 保存進度

聊天服務可能無法在新的對話記住先前內容。每完成一個階段，請保存 AI 產生的重要文件，例如：

- 需求紀錄。
- Project Knowledge Base（專案知識庫）。
- 規格。
- Ticket 規劃。
- Review 或架構改善報告。

要在新對話繼續時：

1. 再次貼上 `generic-workflow.md`。
2. 貼上保存的完整文件。
3. 說明這次要繼續或調整什麼。

AI 會檢查已有內容，並前往第一個尚未完成的階段。

## 九個進階模組

一般情況使用 `generic-workflow.md`。熟悉流程後，可以直接貼上 `prompts/` 內的特定模組：

| Prompt | 用途 |
| --- | --- |
| `bootstrap.md` | 判斷目前進度並找到下一階段 |
| `orchestration.md` | 協調完整流程 |
| `requirements.md` | 一次問一個需求問題 |
| `documented-requirements.md` | 問需求並整理長期專案知識 |
| `specification.md` | 將已核准需求整理成規格 |
| `ticket-planning.md` | 將規格拆成垂直 Tickets |
| `tdd-implementation.md` | 依 Ticket 準備測試與實作 |
| `review.md` | 根據提供的內容進行 Review |
| `architecture-improvement.md` | 分析架構問題與改善方向 |

## 授權與來源

Ask Then Do It 是受到 Matt Pocock 的 skills repository 啟發的獨立專案，與 Matt Pocock 沒有從屬關係，也沒有獲得其背書。完整內容請見 Repository 或套件內的 `LICENSE` 與 `THIRD_PARTY_NOTICES.md`。
