# Ask Then Do It Codex Plugin 使用說明

這份指南說明如何下載、安裝及使用 Ask Then Do It。Plugin 是一組可安裝到 Codex 的功能；其中每個 Skill 都負責一個開發階段。

## 下載與解壓縮

[下載 ask-then-do-it-1.3.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-1.3.0.zip) 並解壓縮。

解壓後最外層應是 `ask-then-do-it/`，裡面包含：

- `.codex-plugin/`
- `skills/`
- 使用說明、授權與來源文件

安裝時請使用完整資料夾，不要只複製 `skills/`，也不要在外面多包一層版本資料夾。

## 使用 AI 指令安裝或更新

主要介面是用自然語言告訴 AI：

```text
請從官方 marketplace 安裝或更新 Ask Then Do It。
```

AI 必須先唯讀檢查 marketplace 與已安裝的 Plugin：

```powershell
codex plugin marketplace list
codex plugin list
```

官方 marketplace 不存在時，才加入它並加入 Plugin：

```powershell
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
```

官方 marketplace 已存在且有較新的正式版本時，先升級 marketplace，再重新加入 Plugin：

```powershell
codex plugin marketplace upgrade ask-then-do-it
codex plugin add ask-then-do-it@ask-then-do-it
```

目前版本已是最新時，只回報狀態、不寫入。來源、版本、CLI 支援或結果無法可靠判斷時，停止並回報不確定性。任何寫入失敗都停止後續寫入；不得先移除目前 Plugin、改用其他來源或自動降級。只使用文件所列的 `add` 安裝子命令，其他安裝別名不支援。

成功後開啟新的 Codex 任務。如果 marketplace 流程失敗，使用相符的 `1.3.0` ZIP 備援；降級必須由使用者明確選擇舊版本。

## 手動安裝備援

目前的安裝方式需要一個已設定、可修改的本機 marketplace。該 marketplace 必須有名稱，並有一個指向 `<local-marketplace-root>/plugins/ask-then-do-it` 的 entry。

1. 備份 marketplace 中現有的 `plugins/ask-then-do-it/`；第一次安裝時可略過備份。
2. 將解壓後的完整 `ask-then-do-it/` 複製到 `<local-marketplace-root>/plugins/ask-then-do-it/`。
3. 確認 Codex 能看到該 marketplace：

```powershell
codex plugin marketplace list
```

4. 安裝 Plugin 並查看狀態：

```powershell
codex plugin add ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

5. 開啟新的 Codex 任務。

如果你還沒有 marketplace 或 entry，請先依 [Codex Plugin 官方說明](https://developers.openai.com/plugins/build/plugins) 建立，再回到第 1 步。

## 流程模式設定

每次操作開始時，Codex 依下列順序判定流程模式：

1. 目前操作的明確指示，例如「這次使用 Full」或「這次使用 Lite」。
2. 專案 Config。
3. 使用者 Config。
4. Full fallback。

Plugin 擁有的設定檔位於：

- 專案：`<project>/.codex/ask-then-do-it.toml`。
- 使用者：`~/.codex/ask-then-do-it.toml`。

每個設定檔只接受頂層 `mode = "full"` 或 `mode = "lite"`：

```toml
mode = "full"
```

```toml
mode = "lite"
```

例如，`mode = lite` 是格式錯誤，`mode = "fast"` 是不支援的值。專案 Config 不存在時，才繼續讀取使用者 Config。無效的專案 Config 會直接回到 Full，且不會繼續讀取使用者 Config。設定檔存在但無法讀取、格式錯誤、缺少頂層 `mode` 或使用不支援的值，都視為無效。目前操作若有明確指示，該指示會在不需要讀取 Config 的情況下優先。

模式判定是唯讀操作，不會建立、寫入、修復或正規化任何設定檔。明確覆寫只影響目前操作，不會更改 Config；專案 Config 只影響所屬專案。新的工作階段會依該次操作的指示與當時的 Config 重新判定模式。

若工作有高風險，AI 可能詢問你是否只針對目前操作切換到 Full，或明確接受風險並繼續 Lite；選擇不會寫入 Config。Full、Lite 流程與高風險類別請見 [Full 與 Lite 流程指南](getting-started-simple.zh-TW.md)。

## 第一次使用

在新的 Codex 任務輸入：

```text
請使用 $ask-then-do-it 幫我開發這個功能：……
```

解析出的模式會決定接下來使用哪一套流程。

### Full 模式

Full 一次只問一個需求問題，並附上建議答案與主要取捨。

Full 使用三個核准點：

1. 需求共識。
2. 規格。
3. Ticket 規劃。

第三個核准前，AI 會先列出所有 Tickets，逐張提供測試建議。每張都會提醒執行測試可能增加工時，而不加測試會降低行為驗證信心。接著你用一次回覆決定每張 Ticket 是否加上測試：全部加上、全部不加，或指定部分 Tickets；沒有預設值。若只指定部分但未說明其餘項目，AI 只會追問尚未決定的 Tickets。

核准後，加上測試的 Ticket 會在內部記錄為 `tdd` 並交由 `$implement-tdd`；不加測試的 Ticket 會記錄為 `direct` 並交由 `$implement-direct`，不建立也不執行行為測試，但可執行 lint、type-check 或 build。Review 會保留 `tests: skipped-by-user` 並說明未測試風險。第三個核准完成後，AI 才能開始正式實作。

### Lite 模式

若 repository 證據已排除所有阻塞，Lite 可以不提出問題；否則每輪最多三個阻塞問題。接著顯示一份 Change Brief，並在實作前等待一次核准。

## 九個 Skill 入口

| Skill | 適合用途 |
| --- | --- |
| `$ask-then-do-it` | 判斷目前階段並引導完整流程；一般情況從這裡開始 |
| `$ask-requirements` | 一次釐清一個高影響需求 |
| `$ask-with-docs` | 釐清需求並整理 Project Knowledge Base（專案知識庫） |
| `$write-spec` | 將已核准需求整理成規格 |
| `$plan-tickets` | 將規格拆成垂直 Tickets，並批次取得每張 Ticket 是否加上測試的選擇 |
| `$implement-direct` | 不建立也不執行行為測試，直接實作已核准的 `direct` Ticket |
| `$implement-tdd` | 依 Ticket 進行 Red、Green、Refactor |
| `$review-code` | 根據需求、變更、可用證據與略過測試風險進行 Review |
| `$improve-architecture` | 分析架構問題與模組關係，提出改善方向 |

你可以直接指定任何 Skill。直接呼叫 Skill 只會選擇階段，不會選擇流程模式；`$ask-then-do-it` 仍是標準模式判定入口，也是一般情況的起點。

模式尚未判定時，會交由 `$ask-then-do-it`，再開始階段工作。判定為 Lite 時，會轉入 Lite 流程。判定為 Full 時，只有在一般前置條件都滿足後，才能繼續所選階段。模式訊號衝突時會暫停並要求釐清。無效 Config 會回到 Full。直接入口不會保存模式狀態。

## 手動更新

1. 下載並解壓縮新版 ZIP。
2. 備份 marketplace 中原有的 `plugins/ask-then-do-it/`。
3. 用新版完整 `ask-then-do-it/` 取代舊版。
4. 再次執行安裝命令，並以 `codex plugin list` 檢查版本。
5. 開啟新的 Codex 任務，測試 `$ask-then-do-it`。

如果新版無法載入，請還原備份並重新安裝舊版。

## 手動移除

在終端機執行：

```powershell
codex plugin remove ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

上面的命令會移除 Codex 中的安裝。若還要刪除 marketplace 裡的 `plugins/ask-then-do-it/` 或 entry，請先確認沒有其他環境仍在使用。

## 授權與來源

Ask Then Do It 是受到 Matt Pocock 的 skills repository 啟發的獨立專案，與 Matt Pocock 沒有從屬或背書關係。完整內容請見 Repository 或套件內的 `LICENSE` 與 `THIRD_PARTY_NOTICES.md`。


[回到 README](../../README.md)
