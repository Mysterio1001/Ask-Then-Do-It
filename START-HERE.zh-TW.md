# Ask Then Do It：先問清楚，再開始做

Ask Then Do It 提供兩種流程。Full 適合需要完整文件與嚴謹檢查的重要工作；Lite 適合範圍明確的改動，使用較短流程與相應的驗證、Review。

這是受到 [Matt Pocock skills repository](https://github.com/mattpocock/skills) 啟發的獨立專案，與 Matt Pocock 沒有從屬或背書關係。授權與來源請見 [LICENSE](LICENSE) 及 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 1. 我要在 Codex 使用

[下載 ask-then-do-it-1.3.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.1/ask-then-do-it-1.3.1.zip) 並解壓縮。安裝完整的 `ask-then-do-it/` Plugin 資料夾後，在新的 Codex 任務輸入：

```text
$ask-then-do-it 我想做一個……
```

安裝、更新與 Codex 模式設定請見 [Codex Plugin 使用說明](docs/guides/codex.zh-TW.md)。

## 2. 我要在 Gemini 或其他 AI 使用

[下載 ask-then-do-it-generic-1.3.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.1/ask-then-do-it-generic-1.3.1.zip) 並解壓縮。開啟 `generic-workflow.md`，將全文貼到新的 AI 對話，再說明你的需求。

設定方式、模式選擇與能力限制請見 [Generic 使用說明](docs/guides/generic.zh-TW.md)。

<!-- claude:begin -->

**3. Claude Code — 1.4.0-preview.1 公開預覽版**

[Claude Code 使用說明](docs/guides/claude-code.zh-TW.md)涵蓋主動選用的 `claude-preview` Marketplace 分支、兩個入口、更新、移除、回饋及 session-only ZIP 復原。指令須等預覽發布後才可使用；若尚不可用，請等待。Codex 與 Generic 維持穩定版 1.3.1。驗證範圍是 native strict validation 與本機自動化測試；真實官方 Claude 工作階段延後驗證。

<!-- claude:end -->
## 想先了解流程

- [完整 Full 與 Lite 流程](docs/guides/getting-started-simple.zh-TW.md)
- [設計說明](docs/design/ai-development-skills.zh-TW.md)


[回到 README](README.md)
