# Ask Then Do It Generic 使用說明

這份指南說明如何在 Gemini 或其他能接收長文字的 AI 使用 Ask Then Do It。Generic 版本不需要安裝 Plugin，只要在對話中貼上工作流。

## 下載與解壓縮

[下載 ask-then-do-it-generic-1.3.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-generic-1.3.0.zip) 並解壓縮。

套件內的主要檔案是：

- `START-HERE.zh-TW.md`：快速使用說明。
- `generic-workflow.md`：一般情況使用的完整工作流。
- `prompts/`：十一個可個別使用的階段模組。
- `LICENSE` 與 `THIRD_PARTY_NOTICES.md`：授權與來源。

## 快速開始

每個新對話都依照下列步驟開始：

1. 開啟 `generic-workflow.md`。
2. 複製全文並貼到新的 AI 對話。
3. 說明你想完成的事情與偏好語言。
4. 若要延續先前的 Full 工作，再貼上保存的 Full 文件。

例如：

```text
我想建立一個預約網站。
請使用繁體中文。
```

AI 的第一個有效回應會先判定流程模式，再依該模式的問題與核准規則進行；你不需要再輸入「開始」。

## 流程模式設定

每次操作開始時，貼入的工作流依下列順序判定模式：

1. 目前操作的明確指示，例如「這次使用 Full」或「這次使用 Lite」。
2. 工作流內的預設模式宣告。
3. Full fallback。

在 `generic-workflow.md` 開頭附近，將唯一的宣告編輯為下列其中一行：

- `Default workflow mode: full`
- `Default workflow mode: lite`

宣告不存在或不是支援值時，使用 Full。明確覆寫只影響目前操作，也不會修改宣告。新的工作階段以當次貼入的宣告為準，除非你另有明確指示。Generic 不會讀取任何 Codex Config。兩種模式的完整流程請見 [Full 與 Lite 流程指南](getting-started-simple.zh-TW.md)。

Generic 必須如實說明主機能力。如果 AI 只有對話能力，就不能檢查 repository、修改檔案、執行命令或測試、保存狀態、宣稱已觀察驗證結果，或執行獨立 Review。若服務另有工具，也只能在實際提供的能力內操作。

## Full 模式的核准點

在 Full 模式中，AI 一次只問一個需求問題；第一個需求問題與後續每題都會附上建議答案與主要取捨。Full 使用三個核准點：

1. 需求已經問清楚。
2. 規格正確描述預期成果。
3. Ticket 規劃可以開始執行。

第三個核准前，AI 會先列出所有 Tickets，逐張提供測試建議。每張都會提醒執行測試可能增加工時，而不加測試會降低行為驗證信心。接著你用一次回覆決定每張 Ticket 是否加上測試：全部加上、全部不加，或指定部分 Tickets；沒有預設值。若只指定部分但未說明其餘項目，AI 只會追問尚未決定的 Tickets。

核准後，加上測試的 Ticket 會在內部記錄為 `tdd` 並進入 TDD 模組；不加測試的 Ticket 會記錄為 `direct` 並進入 `direct-implementation.md`，只提供不建立、不執行行為測試的直接實作指引。Review 必須為 direct 路徑保留 `tests: skipped-by-user`。第三個核准完成後，流程才會進入實作。若你要求修改，AI 會停留在目前階段調整內容。

## Lite 模式的問題與核准

若現有證據已排除所有阻塞，Lite 可以不提出問題；否則每輪最多三個阻塞問題。接著顯示一份 Change Brief，並在實作前等待一次核准。

## 能力限制

Generic 版本只會在對話中引導流程，不能直接修改你的檔案或執行測試。它會提供建議、文件或實作內容，但實際能否操作檔案，取決於你使用的 AI 服務是否提供相應工具。

Review 也只能依照你貼進對話的程式碼、文件與測試結果進行。缺少資料時，AI 應直接說明目前無法確認。

## 保存進度

聊天服務可能無法在新的對話記住先前內容。兩種模式延續工作的方式不同。

### Full

Full 會建立可保存的流程文件。請保存每個 Full 階段產生的重要文件，例如：

- 需求紀錄。
- Project Knowledge Base（專案知識庫）。
- 規格。
- 包含每張 Ticket 是否加上測試及內部路徑的 Ticket 規劃。
- Review 或架構改善報告。

要在新對話繼續 Full 時：

1. 再次貼上 `generic-workflow.md`。
2. 貼上保存的完整文件。
3. 說明這次要繼續或調整什麼。

AI 會檢查已有內容，並前往第一個尚未完成的 Full 階段。

### Lite

新的 Lite 工作階段會依目前指示與當次對話貼入的宣告重新判定流程模式。Lite 不會保存 Change Brief、核准、進度或 Review，因此無法延續這些未保存的流程狀態。AI 會依可取得的 repository 現況與使用者輸入，重新建立一份 Change Brief。

## 十一個進階模組

一般情況使用 `generic-workflow.md`。熟悉流程後，可以直接貼上 `prompts/` 內的特定模組：

Generic 不一定使用 Lite。貼上模組只會選擇階段，不會選擇流程模式；既有的模式優先順序與結果都不變。`bootstrap.md` 與 `orchestration.md` 擁有完整的模式判定器。

其他九個可單獨貼上的模組，只因可能在沒有上述判定器時被貼上，才包含相同、範圍有限且最小化的直接入口保護規則；這不代表它們擁有完整的模式判定權。由組合後 orchestration 證實的模式會直接沿用。只有在直接貼上且模式尚未證實時，才依 `目前操作的明確指示 > 可取得的內嵌宣告 > Full fallback` 判定。指示衝突時暫停並要求釐清；無效宣告選擇 Full；結果不會保存。判定為 Lite 時會轉入 `lite-workflow.md`；判定為 Full 時直接進入 `lite-workflow.md` 會轉回 `orchestration.md`。

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

## 授權與來源

Ask Then Do It 是受到 Matt Pocock 的 skills repository 啟發的獨立專案，與 Matt Pocock 沒有從屬關係，也沒有獲得其背書。完整內容請見 Repository 或套件內的 `LICENSE` 與 `THIRD_PARTY_NOTICES.md`。


[回到 README](../../README.md)
