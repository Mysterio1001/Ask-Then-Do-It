# Ask Then Do It Claude Code Plugin 1.4.0-preview.1

**需主動選用的公開預覽版。** 請保留完整 Plugin folder。Codex 與 Generic 維持穩定版 1.3.1。連結中的安裝指令於預覽發布後適用；若尚不可用，請等待。

相容目標是 Claude model 4.6+、Claude Code 2.1.251+，自動 routing 另需 Node.js 22+。驗證範圍是 native strict validation 與本機自動化測試；真實官方 Claude 工作階段延後驗證。

確認安裝或明確選擇本機 test session 後，由你使用兩個受支援入口之一：

```text
/ask-then-do-it:ask-then-do-it 幫我完成這個功能……
/ask-then-do-it:ask-then-do-it-5 幫我完成這個功能……
```

兩者保留目前模型；第二個依模型與 host 檢查明確選 Claude 5 路徑。內部 stages 不是公開指令。

Full/Lite、routing、Config、主動選用的 Marketplace 安裝、更新、移除、reviewer 限制、平台、session-only ZIP 復原及回饋，請讀不可變更的 same-version [Claude Code 詳細指南](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0-preview.1/docs/guides/claude-code.zh-TW.md)。以 `--plugin-dir` 使用 ZIP 不會建立持久安裝。

這是受 Matt Pocock skills repository 啟發的獨立專案，與 Matt Pocock 沒有從屬或背書關係。對應套件包含 `LICENSE` 與 `THIRD_PARTY_NOTICES.md`。

[回到 README](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0-preview.1/README.md)
