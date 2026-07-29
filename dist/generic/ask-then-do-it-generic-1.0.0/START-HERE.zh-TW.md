# Ask Then Do It Generic prompts 1.0.0 使用說明

這個套件適合 Gemini 或任何能接受長文字提示的 AI。它不需要 Codex Plugin，也不會安裝或修改你的模型帳號。

這是獨立專案，受到 Matt Pocock 的 skills repository 啟發，但與 Matt Pocock 沒有從屬關係，也沒有獲得其背書。請讀套件根目錄的 `LICENSE` 與 `THIRD_PARTY_NOTICES.md` 了解適用授權與完整來源說明。

## 最快開始：貼上一次

1. 開啟這個資料夾內的 `generic-workflow.md`。
2. 複製整份內容，貼到一個新的 AI 對話。
3. 在同一則訊息後面或下一則訊息提供你的實際需求與偏好語言。
4. 如果你已有 Requirement Decision Record、Specification、Ticket Plan 或其他 Ask Then Do It Artifact，也請貼上完整內容與 approval evidence。

Fresh workflow 的第一個有效回應應該簡短宣告能力與目前階段，接著立刻提出第一個需求問題，並附上建議答案與主要取捨。它不應只報告狀態、承諾下一次再問，或要求你再說「開始」。

## 你會看到什麼

- 每一輪只問一個高影響問題。
- Requirement、Specification 與 Ticket Plan 都有明確的人類核准點。
- 實作只能提供 `UNEXECUTED IMPLEMENTATION GUIDANCE`，不能假裝已修改檔案或跑過測試。
- Review 只能依你提供的內容進行，並標示 `limited-evidence`、`non-independent` 或無法驗證的項目。

## Conversation-only 能力

這個 Generic adapter 只證明 `Conversation-only` 能力。除非另一個主機真的提供並證明工具能力，AI 不得聲稱：

- 已讀取或修改 repository。
- 已執行命令、測試、build 或部署。
- 已完成真實 TDD、獨立 Review 或實際刪除實驗。
- 已替你保存跨對話狀態。

## 請自行保存 Artifact

一般聊天模型不保證跨對話記憶。當 AI 輸出 Requirement Decision Record、Project Knowledge Base、Specification、Ticket Plan、Review Report 或 Architecture Improvement Report 時，請自行保存完整 Markdown。

之後開新對話時，重新貼上 `generic-workflow.md`、你的新要求，以及保存的完整 Artifact。工作流會驗證已核准內容並前往第一個未完成階段，不應無故重新開始需求審問。

## 進階用法

`prompts/` 內有九個獨立模組，供知道自己要直接使用哪個階段的人使用。一般使用者只需要 `generic-workflow.md`。
