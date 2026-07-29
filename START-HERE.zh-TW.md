# Ask Then Do It：先問清楚，再開始做

這是一個協助 AI 開發工作的流程工具。它的基本想法很簡單：先把需求問清楚、寫成大家都同意的文件，再開始規劃和實作。

這是獨立專案，受到 Matt Pocock 的 skills repository 啟發，但與 Matt Pocock 沒有從屬關係，也沒有獲得其背書。完整來源與授權請讀 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)；本專案新增內容的授權請讀 [LICENSE](LICENSE)。

## 1. 我要在 Codex 使用

下載並解壓 `dist/codex/ask-then-do-it-1.0.0.zip`。解壓後會得到 `ask-then-do-it/` Plugin 資料夾，內含本說明、兩份授權文件和八個 Skills。

依照 Codex 的手動 Plugin 安裝方式放入該資料夾後，在新任務輸入：

```text
$ask-then-do-it 我想做一個……
```

它會先問一個最重要的問題，而不是立刻寫程式。想直接使用某個階段時，也可以從八個 Skills 中選擇。詳情請看 [Codex Plugin 使用說明](docs/guides/codex.zh-TW.md)。

## 2. 我要在 Gemini 或其他 AI 使用

下載並解壓 `dist/generic/ask-then-do-it-generic-1.0.0.zip`。開啟其中的 `generic-workflow.md`，整份貼到新對話，再接著說明你的需求。

Generic 版本只能保證「對話中的流程引導」；它不會自行讀取你的電腦、執行指令、安裝檔案或永久保存資料。請自行保存 AI 產出的需求紀錄、規格書與 Ticket Plan。詳情請看 [Generic prompts 使用說明](docs/guides/generic.zh-TW.md)。

## 想先看最簡單的流程

請讀 [給初學者的完整說明](docs/guides/getting-started-simple.zh-TW.md)。它會用簡單的例子說明：需求提問、規格書、Ticket、測試、程式審查和架構改善分別在做什麼。

## 維護者

如果你要修改這個專案本身，請從 [README](README.md) 的維護者段落開始，並在修改前閱讀 [Ask Then Do It 1.0.0 Specification](docs/specs/ask-then-do-it-1.0.0.md)。一般使用者不需要執行建置命令。
