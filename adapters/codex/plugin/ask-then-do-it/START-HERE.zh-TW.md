# Ask Then Do It Codex Plugin 1.2.0 使用說明

這個 Plugin 包含九個 Skills，協助你從需求釐清一路進行到實作、Review 與架構診斷。

這是受到 Matt Pocock 的 skills repository 啟發的獨立專案，與 Matt Pocock 沒有從屬或背書關係。授權與來源請見套件內的 `LICENSE` 與 `THIRD_PARTY_NOTICES.md`。

## 下載與解壓縮

解壓縮 `ask-then-do-it-1.2.0.zip` 後，最外層應是 `ask-then-do-it/`。請保持整個資料夾完整，不要只取出 `skills/`。

## 使用 AI 指令安裝或更新

主要介面是在 Codex 任務中用自然語言告訴 AI：

```text
請從官方 marketplace 安裝或更新 Ask Then Do It。
```

AI 必須先唯讀檢查狀態：

```powershell
codex plugin marketplace list
codex plugin list
```

官方 marketplace 不存在時，才加入 marketplace，再加入 Plugin：

```powershell
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
```

官方 marketplace 已存在且有較新的正式版本時，先升級 marketplace，再執行相同的 Plugin 命令：

```powershell
codex plugin marketplace upgrade ask-then-do-it
codex plugin add ask-then-do-it@ask-then-do-it
```

若目前版本已是最新，AI 只回報狀態，不進行寫入。若來源、版本、CLI 支援或結果無法可靠判斷，AI 必須停止並說明不確定性。任何寫入失敗都要停止後續寫入；不得先移除目前 Plugin、改用其他來源或自動降級。本專案只支援文件所列的 `add` 安裝子命令，其他安裝別名不支援。

安裝或更新成功後，請開啟新的 Codex 任務，讓新 Plugin 內容載入。如果 marketplace 流程無法完成，請使用相符的 `1.2.0` ZIP 作為手動備援。只有在使用者明確選擇舊版本時，才可以降級。

## 手動安裝備援

如果要手動安裝，請將完整的 `ask-then-do-it/` 放入本機 marketplace 的 `plugins/` 資料夾，確認 entry 指向它，再從該 marketplace 啟用 Plugin。完成後開啟新的 Codex 任務。

## 第一次使用

在新的 Codex 任務輸入：

```text
請使用 $ask-then-do-it 幫我開發這個功能：……
```

AI 會判斷目前階段並一次提出一個最重要的問題。需求、規格與 Ticket 規劃都需要你明確核准。第三個核准前，AI 會列出所有 Tickets、逐張提供測試建議，並讓你一次決定全部或部分 Ticket 是否加上測試；沒有預設值。

核准後，加上測試的 Ticket 會記錄為 `tdd` 並交由 `$implement-tdd`；不加測試的 Ticket 會記錄為 `direct` 並交由 `$implement-direct`。Review 會保留 `tests: skipped-by-user` 並說明未測試風險。第三個核准完成後，AI 才能開始正式實作。

## 九個 Skill 入口

一般情況從 `$ask-then-do-it` 開始。需要指定階段時，可以直接使用：

| Skill | 用途 |
| --- | --- |
| `$ask-then-do-it` | 判斷目前階段並引導完整流程 |
| `$ask-requirements` | 一次釐清一個高影響需求 |
| `$ask-with-docs` | 釐清需求並整理 Project Knowledge Base |
| `$write-spec` | 將已核准需求整理成規格 |
| `$plan-tickets` | 將規格拆成垂直 Tickets 並取得測試選擇 |
| `$implement-direct` | 不建立或執行行為測試，直接實作 `direct` Ticket |
| `$implement-tdd` | 依 Ticket 進行 Red、Green、Refactor |
| `$review-code` | 根據需求、變更與證據進行 Review |
| `$improve-architecture` | 分析架構問題並提出改善方向 |

## 手動更新

1. 下載並解壓縮相符版本的 ZIP。
2. 備份 marketplace 中原有的 `ask-then-do-it/`。
3. 用新版完整資料夾取代舊版。
4. 重新啟用 Plugin，並開啟新的 Codex 任務確認 `$ask-then-do-it` 可以使用。

不要自動降級；只有在使用者明確選擇舊版本時，才還原並安裝該版本。

## 手動移除

先在 Codex 移除或停用 `ask-then-do-it`。如果還要刪除 marketplace 中的 Plugin 資料夾或 entry，請先確認沒有其他環境仍在使用。
