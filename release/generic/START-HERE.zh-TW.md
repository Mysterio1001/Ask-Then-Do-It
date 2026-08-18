# Ask Then Do It Generic 1.3.1 使用說明

這個套件適合 Gemini 或其他能接收長文字的 AI。它會在對話中引導流程，而且只能使用目前服務實際提供的檔案、指令或其他工具能力。

這是受到 Matt Pocock 的 skills repository 啟發的獨立專案，與 Matt Pocock 沒有從屬關係，也沒有獲得其背書。授權與來源請見套件內的 `LICENSE` 及 `THIRD_PARTY_NOTICES.md`。

## 每個新對話如何開始

1. 開啟 `generic-workflow.md`。
2. 複製全文，貼到一個新的 AI 對話。
3. 在同一則訊息或下一則訊息說明你的需求與偏好語言。

AI 的第一個有效回應會先判定流程模式，再依該模式的問題與核准規則進行。請保存重要進度。Generic 不能直接修改你的檔案或執行測試；其他操作仍取決於主機實際提供的工具。

每個新對話都要重新貼上 `generic-workflow.md`。設定方式、模式選擇、session 行為與能力限制請見 [Generic 詳細說明](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.1/docs/guides/generic.zh-TW.md)。

## 選擇 Full 或 Lite

Full 一次只問一個需求問題；第一個需求問題會附上建議答案，且流程有三個核准點。Lite 可以不提出問題；若有阻塞，每輪最多三個阻塞問題，之後顯示一份 Change Brief，並在實作前等待一次核准。選擇前請閱讀 [完整 Full 與 Lite 流程](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.1/docs/guides/getting-started-simple.zh-TW.md)。


[回到 README](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.1/README.md)
