# Ask Then Do It Codex Plugin 使用說明

這份指南說明如何下載、安裝及使用 Ask Then Do It。Plugin 是一組可安裝到 Codex 的功能；其中每個 Skill 都負責一個開發階段。

## 下載與解壓縮

[下載 ask-then-do-it-1.0.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-1.0.1.zip) 並解壓縮。

解壓後最外層應是 `ask-then-do-it/`，裡面包含：

- `.codex-plugin/`
- `skills/`
- 使用說明、授權與來源文件

安裝時請使用完整資料夾，不要只複製 `skills/`，也不要在外面多包一層版本資料夾。

## 手動安裝

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

## 第一次使用

在新的 Codex 任務輸入：

```text
請使用 $ask-then-do-it 幫我開發這個功能：……
```

AI 會先判斷你目前位於哪個階段，再提出一個最重要的問題。每次只問一題，並附上建議答案與主要取捨。

流程中有三個需要你明確核准的地方：

1. 需求共識。
2. 規格。
3. Ticket 規劃。

第三個核准完成後，AI 才能開始正式實作。

## 八個 Skill 入口

| Skill | 適合用途 |
| --- | --- |
| `$ask-then-do-it` | 判斷目前階段並引導完整流程；一般情況從這裡開始 |
| `$ask-requirements` | 一次釐清一個高影響需求 |
| `$ask-with-docs` | 釐清需求並整理 Project Knowledge Base（專案知識庫） |
| `$write-spec` | 將已核准需求整理成規格 |
| `$plan-tickets` | 將規格拆成垂直、可測試的 Tickets |
| `$implement-tdd` | 依 Ticket 進行 Red、Green、Refactor |
| `$review-code` | 根據需求、程式碼差異與測試結果進行 Review |
| `$improve-architecture` | 分析架構問題與模組關係，提出改善方向 |

你可以直接指定任何 Skill。若只使用 `$ask-then-do-it`，AI 會根據你的要求與目前進度選擇下一個階段。

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
