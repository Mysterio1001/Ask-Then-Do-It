# Ask Then Do It Codex Plugin 1.0.0 使用說明

這個資料夾本身就是 `ask-then-do-it` Plugin。它包含八個 AI Agent Skills，但不包含安裝程式，也不會自動修改 Codex、marketplace 或你的個人設定。

這是獨立專案，受到 Matt Pocock 的 skills repository 啟發，但與 Matt Pocock 沒有從屬關係，也沒有獲得其背書。請讀套件根目錄的 `LICENSE` 與 `THIRD_PARTY_NOTICES.md` 了解適用授權與完整來源說明。

## 先確認你拿到完整檔案

如果你下載的是 `ask-then-do-it-1.0.0.zip`：

1. 同時取得發佈頁提供的 `checksums.sha256`。
2. 計算 ZIP 的 SHA-256。
3. 確認結果等於 `checksums.sha256` 中 `codex/ask-then-do-it-1.0.0.zip` 的值。
4. 解壓縮後，最外層應直接是 `ask-then-do-it/`，裡面要看得到本檔案、`.codex-plugin/` 和 `skills/`。

## 手動安裝

Codex Plugin 由你信任的 marketplace 管理。因此安裝是手動且需要你明確決定的操作：

1. 確認你有一個允許修改的本機 marketplace；若沒有，先停止並依你的 Codex 文件或管理規則建立。
2. 將完整的 `ask-then-do-it/` 放進該 marketplace 的 Plugin source 位置。不要只複製 `skills/`，也不要再多包一層版本資料夾。
3. 由你親自執行 Codex 的 Plugin 安裝或啟用步驟。
4. 開啟一個新的 Codex 任務測試，避免舊任務仍使用快取內容。

本套件不會自動執行以上步驟，也不會建立、改寫或刪除 marketplace entry。

## 第一次使用

建議在新任務中輸入：

```text
請使用 $ask-then-do-it 幫我開發這個功能：……
```

AI 會先判斷目前在哪個階段，再選擇正確的模組。需求共識、Specification 與 Ticket Plan 都需要你明確核准；核准前不應開始寫正式程式。

## 八個 Skill 入口

一般情況使用主要入口 `$ask-then-do-it`。你也可以直接指定：

| Skill | 用途 |
| --- | --- |
| `$ask-then-do-it` | 自動判斷階段並協調完整流程 |
| `$ask-requirements` | 一次問一題，把需求問清楚 |
| `$ask-with-docs` | 問需求並同步整理長期專案知識 |
| `$write-spec` | 把已核准需求整理成不含 production code 的 Specification |
| `$plan-tickets` | 把 Approved Specification 拆成垂直、可測的 Tickets |
| `$implement-tdd` | 依 Ticket 執行 Red、Green、Refactor |
| `$review-code` | 依證據做程式碼 Review 與十二項視角檢查 |
| `$improve-architecture` | 做唯讀架構診斷與模擬刪除分析 |

## 手動更新

先驗證新版 ZIP 與 checksum，再備份舊的 Plugin source，以新的完整 `ask-then-do-it/` 取代它。由你重新執行 Codex 的更新或安裝步驟，最後在新任務中檢查版本與 `$ask-then-do-it`。

不要直接修改已驗證 ZIP 或其中的 manifest 後繼續沿用原 checksum。

## 手動移除

先由你在 Codex 中停用或移除 `ask-then-do-it`。是否刪除 marketplace 中的 Plugin source 或 entry 是另一個動作；先確認沒有其他環境仍在使用並取得相應授權。本套件不會自動移除任何內容。
