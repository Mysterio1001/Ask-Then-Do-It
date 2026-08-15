# Ask Then Do It Codex Plugin 1.3.0 使用說明

這個 Plugin 會引導專案從需求釐清進行到實作與 Review。使用 ZIP 備援安裝時，請先下載並解壓縮，再保持完整的 `ask-then-do-it/` 資料夾，不要只取出其中一部分。

這是受到 Matt Pocock 的 skills repository 啟發的獨立專案，與 Matt Pocock 沒有從屬或背書關係。授權與來源請見套件內的 `LICENSE` 與 `THIRD_PARTY_NOTICES.md`。

## 安裝或更新

在 Codex 任務中告訴 AI：

```text
請從官方 marketplace 安裝或更新 Ask Then Do It。
```

先檢查目前狀態：

```powershell
codex plugin marketplace list
codex plugin list
```

官方 marketplace 不存在時才加入：

```powershell
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
```

若已存在且需要更新，改為先升級：

```powershell
codex plugin marketplace upgrade ask-then-do-it
```

接著安裝或更新 Plugin：

```powershell
codex plugin add ask-then-do-it@ask-then-do-it
```

安裝或更新成功後，請開啟新的 Codex 任務。判斷規則、手動備援、更新與移除方式請見 [Codex Plugin 詳細說明](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides/codex.zh-TW.md)。

## 開始使用

在新的 Codex 任務輸入：

```text
請使用 $ask-then-do-it 幫我開發這個功能：……
```

需要指定階段時，可使用 `$ask-requirements`、`$ask-with-docs`、`$write-spec`、`$plan-tickets`、`$implement-direct`、`$implement-tdd`、`$review-code` 與 `$improve-architecture`。

## 選擇 Full 或 Lite

需要完整文件流程與較高驗證信心時使用 Full；範圍明確、適合較短流程與相應驗證的改動可使用 Lite。選擇前請閱讀 [完整 Full 與 Lite 流程](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides/getting-started-simple.zh-TW.md)。


[回到 README](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/README.md)
