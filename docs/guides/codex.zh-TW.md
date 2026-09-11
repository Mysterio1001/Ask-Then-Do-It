# Ask Then Do It Codex Plugin 使用說明

使用 Codex Plugin 引導需求、實作與 Review。一般從 `$ask-then-do-it` 開始。

以下為 1.4.1 的安裝／下載目標；若遠端尚未提供，請等待發布。

## 安裝與準備

在終端機執行以下首次安裝指令，也可以請 AI 代為執行：

```bash
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
```

<a id="zip"></a>
<details>
<summary>ZIP 備援</summary>

[下載 ask-then-do-it-1.4.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.1/ask-then-do-it-1.4.1.zip)

保留完整 `ask-then-do-it/`，不要只複製 `skills/`。將它放到已設定且可修改的本機 Marketplace 的 `plugins/ask-then-do-it/`，其 entry 也須指向該位置，再執行：

```bash
codex plugin add ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

尚未設定本機 Marketplace 時，請先依 [官方說明](https://developers.openai.com/plugins/build/plugins) 建立。

</details>

## 開始使用

安裝後開啟新的 Codex 任務，再輸入：

```text
$ask-then-do-it 幫我建立一個預約網站，請使用繁體中文。
```

## Full／Lite 模式

**Full** 適合需要需求、規格與工作規劃紀錄的工作，實作前有三個核准點。**Lite** 適合範圍清楚的改動，使用簡短變更摘要與一次核准。

直接說「這次使用 Full」或「這次使用 Lite」即可，只影響這次操作。

若要設定預設模式，在以下任一檔案填入 `mode = "full"` 或 `mode = "lite"`：

- `<project>/.codex/ask-then-do-it.toml`
- `~/.codex/ask-then-do-it.toml`

優先順序是本次明確指示、專案設定、使用者設定，最後預設 Full。設定檔無效時回到 Full；無效專案設定不再讀使用者設定。判定過程不會修改設定。

完整流程、測試選擇與保存進度請看 [初學者流程](getting-started-simple.zh-TW.md)。

## 可用指令

一般使用 `$ask-then-do-it`；需要指定階段時再展開下表。直接指定階段仍需符合該階段前置條件。

<details>
<summary>查看進階入口</summary>

| Skill | 用途 |
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

</details>

## 更新與移除

已安裝時，在終端機執行：

```bash
codex plugin marketplace upgrade ask-then-do-it
codex plugin add ask-then-do-it@ask-then-do-it
```

手動更新時先備份，再以新版完整資料夾替換並重新加入 Plugin；載入失敗可還原備份。

更新成功後開啟新的 Codex 任務。

移除 Plugin：

```text
codex plugin remove ask-then-do-it --marketplace ask-then-do-it
```

如以本機 Marketplace 安裝，移除指令中的名稱請換成你的 `<local-marketplace-name>`。

這只移除 Plugin 安裝。若要刪除本機 Marketplace 裡的檔案，先確認沒有其他環境共用。

版本或來源不明、更新失敗時先停下並檢查，不先移除、不自動降版或換來源。已是目前版本就不必重裝，停用狀態也應保留。

## 常見問題

- 找不到 Skill：用 `codex plugin list` 查看是否安裝，再開新任務。
- 安裝來源不清楚：先用 `codex plugin marketplace list` 確認。

仍有問題時，可在 [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues) 提供專案版本、使用的 AI 服務／主程式、平台與重現步驟。

## 授權與來源

本專案受到 Matt Pocock 的 skills repository 啟發，與其沒有從屬或背書關係。授權與來源請見 `LICENSE` 與 `THIRD_PARTY_NOTICES.md`。

[回到 README](../../README.md)
