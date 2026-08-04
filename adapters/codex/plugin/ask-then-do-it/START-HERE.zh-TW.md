# Ask Then Do It Codex Plugin 1.1.0 使用說明

這個 Plugin 包含九個 Skills，協助你從釐清需求一路進行到實作、檢查與架構改善。

這是受到 Matt Pocock 的 skills repository 啟發的獨立專案，與 Matt Pocock 沒有從屬或背書關係。授權與來源請見套件內的 `LICENSE` 及 `THIRD_PARTY_NOTICES.md`。

## 下載與解壓縮

解壓縮 `ask-then-do-it-1.1.0.zip` 後，最外層應是 `ask-then-do-it/`。請保持整個資料夾完整，不要只取出 `skills/`。

## 手動安裝

本安裝方式需要你已擁有一個可修改的本機 marketplace，以及指向 `plugins/ask-then-do-it/` 的 entry。

1. 將完整的 `ask-then-do-it/` 放進 marketplace 的 `plugins/` 資料夾。
2. 使用該 marketplace 安裝或啟用 `ask-then-do-it`。
3. 開啟新的 Codex 任務，讓 Codex 載入這次安裝的內容。

如果你尚未建立 marketplace，請先依 Codex 的 Plugin 文件完成設定，再回到這裡繼續。

## 第一次使用

在新的 Codex 任務輸入：

```text
請使用 $ask-then-do-it 幫我開發這個功能：……
```

AI 會先判斷目前階段並提出一個重要問題。需求、規格與 Ticket 規劃都需要你明確核准。所有 Tickets 列出後，AI 會逐張提供測試建議；每張都會提醒執行測試可能增加工時，而不加測試會降低驗證信心。你再用一次回覆決定每張 Ticket 是否加上測試，可以全部加上、全部不加，或指定部分 Tickets。所有選擇完成後才核准完整規劃；核准前不應開始正式實作。

系統內部會將「加上測試」記錄為 `tdd`，將「不加測試」記錄為 `direct`；你不需要用這些名稱回答。

## 九個 Skill 入口

一般情況從 `$ask-then-do-it` 開始。需要指定階段時，可以直接使用：

| Skill | 用途 |
| --- | --- |
| `$ask-then-do-it` | 判斷目前階段並引導完整流程 |
| `$ask-requirements` | 一次問一題，把需求問清楚 |
| `$ask-with-docs` | 問需求並同步整理長期專案知識 |
| `$write-spec` | 將已核准需求整理成規格 |
| `$plan-tickets` | 將規格拆成垂直 Tickets，並批次取得每張 Ticket 是否加上測試的選擇 |
| `$implement-direct` | 不建立也不執行行為測試，直接實作已核准的 `direct` Ticket |
| `$implement-tdd` | 依 Ticket 進行 Red、Green、Refactor |
| `$review-code` | 檢查程式碼；`direct` Ticket 沒有行為測試證據時保留 `tests: skipped-by-user` |
| `$improve-architecture` | 分析架構問題並提出改善方向 |

## 手動更新

1. 下載並解壓縮新版 ZIP。
2. 備份 marketplace 中原有的 `ask-then-do-it/`。
3. 用新版完整資料夾取代舊版。
4. 重新安裝或啟用 Plugin，並在新的 Codex 任務確認 `$ask-then-do-it` 可以使用。

## 手動移除

先在 Codex 移除或停用 `ask-then-do-it`。如果還要刪除 marketplace 中的 Plugin 資料夾或 entry，請先確認該 marketplace 沒有其他環境正在使用。
