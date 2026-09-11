# Ask Then Do It Claude Code 使用說明

在 Claude Code 使用同一個 Plugin，即可取得一般 Claude 與 Claude 5 兩種流程設定。

以下為 1.4.0 的安裝／下載目標；若遠端尚未提供，請等待發布。

## 安裝與準備

需要 Claude model **4.6+**、Claude Code **2.1.251+**；自動判斷模型另需 Node.js **22+**。在 Claude Code 對話中執行：

此版支援 user 安裝範圍；以下首次安裝使用預設 user scope。

```text
/plugin marketplace add Mysterio1001/Ask-Then-Do-It
/plugin install ask-then-do-it@ask-then-do-it
```

<a id="zip"></a>
<details>
<summary>ZIP 備援</summary>

下載後可依 Release 的 checksums 檔核對 SHA-256。

[下載 ask-then-do-it-claude-1.4.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0/ask-then-do-it-claude-1.4.0.zip)

下載並解壓縮完整 Plugin。每次從終端機啟動時加上：

```bash
claude --plugin-dir "/path with spaces/ask-then-do-it"
```

只對這次工作階段生效（session-only）；之後每次都要再加 `--plugin-dir`，不建立持久 Marketplace 安裝。

</details>

## 開始使用

安裝後執行 `/reload-plugins` 或開啟新工作階段，再輸入：

```text
/ask-then-do-it:ask-then-do-it 幫我建立一個預約網站，請使用繁體中文。
```

## Full／Lite 模式

**Full** 適合需要需求、規格與工作規劃紀錄的工作，實作前有三個核准點。**Lite** 適合範圍清楚的改動，使用簡短變更摘要與一次核准。

直接說「這次使用 Full」或「這次使用 Lite」即可，只影響這次操作。

若要設定預設模式，在以下任一檔案填入 `mode = "full"` 或 `mode = "lite"`：

- `<project>/.claude/ask-then-do-it.toml`
- `~/.claude/ask-then-do-it.toml`

優先順序是本次明確指示、專案設定、使用者設定，最後預設 Full。設定檔無效時回到 Full；無效專案設定不再讀使用者設定。判定過程不會修改設定。

完整流程、測試選擇與保存進度請看 [初學者流程](getting-started-simple.zh-TW.md)。

## 可用指令

一般選第一個即可。兩個入口都沿用目前模型，不會替你切換模型。

| 入口 | 用途 |
| --- | --- |
| `/ask-then-do-it:ask-then-do-it` | 自動選擇一般 Claude 或 Claude 5 流程；無法識別的模型會提示後使用一般流程。 |
| `/ask-then-do-it:ask-then-do-it-5` | 明確要求 Claude 5 流程；已知受支援的非 Claude 5 模型仍使用一般流程。未知模型會提示這是未驗證路徑。 |

## 更新與移除

已安裝時，在 Claude Code 內執行：

```text
/plugin marketplace update ask-then-do-it
/plugin update ask-then-do-it@ask-then-do-it
/reload-plugins
```

移除 Plugin：

```text
/plugin uninstall ask-then-do-it@ask-then-do-it --scope user
```

移除保留 Marketplace 與流程設定；最後一個安裝範圍的可重建路由資料預設刪除。只有明確想保留資料時才使用 `--keep-data`。

版本或來源不明、更新失敗時先停下並檢查，不先移除、不自動降版或換來源。已是目前版本就不必重裝，停用狀態也應保留。

## 常見問題

- 找不到入口：確認 Plugin 已啟用，執行 `/reload-plugins`，或開新工作階段；VS Code 可用 `/` 查看可用指令。
- 自動判斷停止：先檢查 `claude --version` 與 `node --version`。不要把 `-5` 當成通用修復方式。
- `/doctor` 只檢查 Claude Code 安裝／設定健康，不會轉換或最佳化本專案 Skills。

Windows、macOS、Linux 的本機 CLI、VS Code、JetBrains 是相容目標。真實模型、指令／hook、獨立複查與完整安裝更新流程仍有未驗證項目；離線測試不代表全部實測通過。 [進階參考](#advanced-reference)。

仍有問題時，可在 [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues) 提供專案版本、主程式／Node 版本、平台、使用入口與重現步驟。

<a id="advanced-reference"></a>
<details>
<summary>進階參考</summary>

這裡保存路由、設定解析、審查與平台驗證的完整細節；一般安裝與使用請回主指南。

[使用說明](claude-code.zh-TW.md)

<a id="routing"></a>
### Routing 與工作階段接續

| 可信 route 結果 | 自動入口 | 明確 `-5` 入口 |
| --- | --- | --- |
| 已知 Claude 5 | Claude 5 profile | Claude 5 profile |
| 已知受支援的非 Claude 5 | General profile | 說明不相容後使用 General |
| `known unsupported`：已知低於 4.6 | 停止 | 停止 |
| `valid unknown`：有效但未列出或未提供的模型 | 揭露未驗證相容模式，使用 General | 揭露這是使用者明確選擇的未驗證路徑，使用 Claude 5 |
| `router failure`：state、ownership、transition 或 handler 失敗 | 停止 | 停止，只有下述兩個 Node 例外 |

Node 遺失或過舊不等於模型未知。只有明確入口可在有效 `node-too-old` envelope，或 Node 確定遺失且 envelope 不可用時，走已揭露的手動 Claude 5 路徑。兩者都須另外證明 Claude Code 2.1.251+；不驗證模型，也不提供完整自動 routing、持久 binding、resume 或 switch tracking。Node 存在時 envelope 遺失／損壞／重複、版本無法證明及其他 router failure 都停止。不得從使用者文字或模型自述猜測模型。

一個 `operation` 保留已選 profile；中途切換模型不會載入或服從另一 profile。`PostModelSwitch` commit 後，下一次允許的公開入口才可重選，並取代歷史 profile 指示。Hook 有 `best-effort` 時序窗口，不能保證切換後第一次 invocation 一定 reroute。若切到不支援模型，也須揭露目前 operation 已離開正式支援。

Startup、fork、clear 不自動恢復上一個 operation；resume／compact 需要可信的同 session context 與目前 workflow evidence，舊 binding 不能跨 session 授權。Full 可使用已保存的核准 artifacts；Lite 對話狀態不具跨 session 持久性。

<a id="config"></a>
### Full/Lite Config

Profile 與流程模式分開選。每個 operation 依序使用：明確 `full`／`lite` 指示 → active project root 內的 project Config → user Config → Full fallback。明確模式衝突時暫停並問一題。Project boundary 由可信 host 的 active project root 決定，不猜測目前目錄。

- Project：`<project>/.claude/ask-then-do-it.toml`
- User：`~/.claude/ask-then-do-it.toml`

檔案只使用一個 top-level quoted assignment，例如：

```toml
mode = "full"
```

或 `mode = "lite"`。Project 檔不存在才讀 user 檔；已存在卻不可讀、格式錯誤、重複、缺 mode 或值不支援時，fail closed 為 Full。無效 project Config 不向下讀 user Config。大小寫變體、別名、nested keys、未加引號值均不接受。僅對話能力遇到 host-unavailable source 時視為 absence，但不冒稱讀取，也不要求你提供 host Config。

判定全程唯讀，不建立、修復或改寫任一檔案，不保存 operation override，不讀寫 Codex Config，也不寫 `settings.json`。此 Plugin Config 與 Claude Code 自身設定、可重建 routing data 是不同資料。[共用流程指南](getting-started-simple.zh-TW.md)說明 Full 核准 gates、逐 Ticket 測試選擇及 Lite 的一次 Change Brief。

<a id="review"></a>
### Review 能力

Full Review 在隔離的 Plugin reviewer 確實可用時使用它。允許工具只有 `Read`、`Grep`、`Glob`，沒有 write、shell、network；主流程等待報告並驗證 findings。單有 reviewer 檔案不代表 host 已獨立執行。

有 repository tools 卻無可用 independent reviewer 時，同 context 完整 Review 並標 `non-independent`。只有對話或摘錄證據則標 `limited-evidence`，列出不可用驗證並交接，不能聲稱完成 repository Review。只有隔離與原始證據已證明時才用 `independent`。Lite 一律維持同 context 精簡 Review；finding 本身不授權修正。

<a id="status"></a>
### 唯讀狀態

以下 `read-only` 指令不會安裝、refresh、更新、啟用、停用、移除或改 Config：

```sh
claude --version
node --version
claude plugin marketplace list --json
claude plugin list --json
claude plugin details ask-then-do-it@ask-then-do-it
```

分別回報 Claude Code／Node、Marketplace 名稱／source／scope、qualified Plugin identity、安裝 scope、version、enabled state，以及兩個入口是否可用。若 listing 缺少必要資訊，標 unknown 並查看適當的唯讀 host state；不得虛構 ownership 或假定可安全寫入。Component discovery 與 projected token cost 不是模型行為或計費證據。

<a id="platforms"></a>
### 平台與已知限制

Windows、macOS、Linux 上的 local `terminal CLI`、`VS Code`、`JetBrains` 是 **compatibility target**，不是九組 `live-verified` 組合。此 Adapter 尚未宣稱任何完整 live environment；提出 live 聲明前須記錄 exact OS、surface、Claude Code、Node、active model 與日期。

已於 **2026-09-09** 實際讀取官方文件：

| Surface | 官方文件支援與差異 |
| --- | --- |
| terminal CLI | Local Plugins 可含 Skills、Agents、hooks；CLI 提供完整 commands／skills 介面。文件支援不等於本 Adapter exact host hooks 已驗證。 |
| VS Code | 有圖形化 Plugin 管理，host settings／hooks 與 CLI 共用。Chat panel 內建自己的 CLI，但 commands／skills 只有子集合，須用 `/` 查看；integrated terminal 的 `claude` 另需 standalone CLI。Plugin reviewer 的 invocation／isolation 及兩個 exact namespaced entries 仍須逐 surface 實測。 |
| JetBrains | 官方使用方式是在 IDE integrated terminal 跑 `claude`，external terminal 可用 `/ide` 接入。Plugin 能力來自該 CLI runtime，IDE integration 加入編輯器功能；不能據此宣稱有另一套 graphical command interface，或本 Adapter 行為已驗證。 |

來源：[Plugin components](https://code.claude.com/docs/en/plugins-reference)、[VS Code](https://code.claude.com/docs/en/vs-code)、[JetBrains](https://code.claude.com/docs/en/jetbrains)、[Skills](https://code.claude.com/docs/en/skills)、[Subagents](https://code.claude.com/docs/en/sub-agents)、[hooks](https://code.claude.com/docs/en/hooks)。目前官方文件不能取代 exact 2.1.251 行為驗證；Claude Desktop、web/cloud 不在此 compatibility target。

<a id="lifecycle"></a>
### 安裝、更新與移除的詳細規則

正式來源是 `Mysterio1001/Ask-Then-Do-It`，Plugin 是 `ask-then-do-it@ask-then-do-it`，只支援 `user` scope。每次寫入前重新確認來源、scope、版本與 enabled 狀態；只有 Plugin 不存在時才安裝。已是目前版本則不寫入，並保留 disabled 狀態。較新版本不降級，其他來源或 scope 不明時停止。

安裝、更新與移除必須由使用者明確要求。多步操作中，每次寫入前都要重查狀態；部分失敗時先停下，唯讀重查並回報，不做破壞性 rollback。Marketplace refresh 不接受 scope 選項。Node 不可用時，安全且已授權的 lifecycle 操作仍可執行，但必須說明自動路由不可用。成功後 reload 或開新 session，才使用新版內容；不自動啟用背景更新。

以下命令在終端機執行，安裝、更新與移除是不同操作：

```sh
# Install
claude plugin marketplace add Mysterio1001/Ask-Then-Do-It --scope user
claude plugin install ask-then-do-it@ask-then-do-it --scope user

# Update
claude plugin marketplace update ask-then-do-it
claude plugin update ask-then-do-it@ask-then-do-it --scope user

# Remove
claude plugin uninstall ask-then-do-it@ask-then-do-it --scope user
```


</details>

## 授權與來源

本專案受到 Matt Pocock 的 skills repository 啟發，與其沒有從屬或背書關係。授權與來源請見 `LICENSE` 與 `THIRD_PARTY_NOTICES.md`。

[回到 README](../../README.md)
