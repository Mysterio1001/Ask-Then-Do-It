# Ask Then Do It：先問清楚，再開始做

Ask Then Do It 會引導 AI 先確認你的需求，再依序整理規格、拆分工作、實作與檢查成果。

這是受到 [Matt Pocock skills repository](https://github.com/mattpocock/skills) 啟發的獨立專案，與 Matt Pocock 沒有從屬或背書關係。授權與來源請見 [LICENSE](LICENSE) 及 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 1. 我要在 Codex 使用

[下載 ask-then-do-it-1.1.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.1.0/ask-then-do-it-1.1.0.zip) 並解壓縮。安裝完整的 `ask-then-do-it/` Plugin 資料夾後，在新的 Codex 任務輸入：

```text
$ask-then-do-it 我想做一個……
```

AI 會先提出一個重要問題，等你確認需求後才進入下一階段。Tickets 建立後，AI 會逐張提供測試建議，再由你一次決定每張 Ticket 是否加上測試，最後才核准完整規劃。安裝、更新與九個 Skill 入口請見 [Codex Plugin 使用說明](docs/guides/codex.zh-TW.md)。

## 2. 我要在 Gemini 或其他 AI 使用

[下載 ask-then-do-it-generic-1.1.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.1.0/ask-then-do-it-generic-1.1.0.zip) 並解壓縮。開啟 `generic-workflow.md`，將全文貼到新的 AI 對話，再說明你的需求。

AI 會先提出一個需求問題。請保存流程產生的重要文件；開啟另一個新對話時，再貼上工作流與先前保存的文件。完整步驟請見 [Generic 使用說明](docs/guides/generic.zh-TW.md)。

## 想先了解流程

- [初學者流程](docs/guides/getting-started-simple.zh-TW.md)
- [設計說明](docs/design/ai-development-skills.zh-TW.md)
