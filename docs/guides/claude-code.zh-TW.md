# Ask Then Do It — Claude Code 使用說明

本指南說明 Claude Adapter `1.4.0-preview.1` 公開預覽版。Codex 與 Generic 維持穩定版 `1.3.1`；共用 Full/Lite 流程請讀[初學者流程](getting-started-simple.zh-TW.md)。

<a id="versions"></a>
## 預覽狀態與三種版本

**這是需主動選用的公開預覽版 1.4.0-preview.1 發布說明。** 穩定版維持 **1.3.1**，其 Codex／Generic 套件不含此 Claude Adapter。安裝指令與[固定版本的預覽 ZIP](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0-preview.1/ask-then-do-it-claude-1.4.0-preview.1.zip)須等預覽 tag、ZIP 與 `claude-preview` Marketplace 分支發布後才可使用。若資產仍不可用，請等待發布，不要改用其他來源。

| 要求 | 意義 |
| --- | --- |
| Claude model `4.6+` | 模型支援基準；有效但未列入清單的模型仍未驗證。 |
| Claude Code `2.1.251+` | 主程式最低版本，與模型分開確認。 |
| Node.js `22+` | 自動 profile routing 的獨立需求；不是 native Claude Code 安裝本身的版本。 |

預覽版驗證範圍是 native `strict` validation 與本機自動化測試（`local automated tests`）。真實官方 Claude Code 工作階段的指令／hook 行為、模型情境、雙 profile 等價、context reduction 與完整 live smoke 均**延後驗證**，不作為此次預覽發布門檻，也不宣稱已通過。Exact Claude Code 2.1.251 schema validation 不代表 live 行為，也不保證未來 host 版本。

<a id="entries"></a>
## 兩個公開入口

確認安裝並 reload 後，由你明確輸入其中一個：

```text
/ask-then-do-it:ask-then-do-it 幫我完成這個功能……
/ask-then-do-it:ask-then-do-it-5 幫我完成這個功能……
```

第一個自動選 profile；第二個依下方規則明確要求 Claude 5 路徑。兩者皆為 `model: inherit`，保留目前模型，不會切換或固定模型。Plugin 恰有這兩個受支援的 namespaced entries；內部 stages 不形成額外指令。Host 提供的 bare aliases 可能不同，不保證存在或不存在。

<a id="routing"></a>
## Routing 與工作階段接續

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
## Full/Lite Config

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
## Review 能力

Full Review 在隔離的 Plugin reviewer 確實可用時使用它。允許工具只有 `Read`、`Grep`、`Glob`，沒有 write、shell、network；主流程等待報告並驗證 findings。單有 reviewer 檔案不代表 host 已獨立執行。

有 repository tools 卻無可用 independent reviewer 時，同 context 完整 Review 並標 `non-independent`。只有對話或摘錄證據則標 `limited-evidence`，列出不可用驗證並交接，不能聲稱完成 repository Review。只有隔離與原始證據已證明時才用 `independent`。Lite 一律維持同 context 精簡 Review；finding 本身不授權修正。

<a id="status"></a>
## 唯讀狀態

以下 `read-only` 指令不會安裝、refresh、更新、啟用、停用、移除或改 Config：

```sh
claude --version
node --version
claude plugin marketplace list --json
claude plugin list --json
claude plugin details ask-then-do-it@ask-then-do-it
```

分別回報 Claude Code／Node、Marketplace 名稱／source／scope、qualified Plugin identity、安裝 scope、version、enabled state，以及兩個入口是否可用。若 listing 缺少必要資訊，標 unknown 並查看適當的唯讀 host state；不得虛構 ownership 或假定可安全寫入。Component discovery 與 projected token cost 不是模型行為或計費證據。

<a id="install-update"></a>
## User scope 安裝與更新

主動選用預覽版時，使用完整 Marketplace source `https://github.com/Mysterio1001/Ask-Then-Do-It.git#claude-preview` 與 qualified Plugin `ask-then-do-it@ask-then-do-it`，scope 為 `--scope user`。URL fragment 選定持續更新的 `claude-preview` 分支；refresh 會跟隨該分支，後續預覽版不必更換 URL，也不會提升穩定版 1.3.1。[官方 Marketplace 文件](https://code.claude.com/docs/en/plugin-marketplaces)說明了此 `#ref` 語法。

每次寫入前立即重新確認完整 ownership、source、scope、current state；先前 status 不足以授權。預期 Marketplace 與 Plugin 都不存在且無歧義時：

```sh
claude plugin marketplace add "https://github.com/Mysterio1001/Ask-Then-Do-It.git#claude-preview" --scope user
claude plugin install ask-then-do-it@ask-then-do-it --scope user
```

在 Claude Code 內，對應的 Marketplace 指令是 `/plugin marketplace add https://github.com/Mysterio1001/Ask-Then-Do-It.git#claude-preview`。若只有 Plugin 不存在且 Marketplace source／ref 正確，只跑 install。預期預覽安裝較舊且有明確更新請求時，可 refresh 該 Marketplace 再更新該 Plugin：

```sh
claude plugin marketplace update ask-then-do-it
claude plugin update ask-then-do-it@ask-then-do-it --scope user
```

Marketplace refresh 沒有 scope 選項，須驗證前後 source／scope，下一次寫入前仍須重新確認。Current version 無論 enabled 或 `disabled` 都是 no-op，保留停用選擇；啟用須另一個明確操作。已安裝 `newer` version 則停止，不降級，也不先移除再更新。

Source 不符、同名其他來源、project／local／managed 或多 scope、state 變更／不可讀、Claude Code 不支援時，停止且不寫。Node 缺少不阻止其餘安全且已授權的 lifecycle 操作，但自動 routing 仍不可用。Partial failure 停止後續 writes，唯讀重查並如實回報成敗，不做破壞性 rollback。成功後使用 `/reload-plugins` 或新 session，才可說新 bytes 已生效；不藉此啟用背景 auto-update。

<a id="remove"></a>
## 移除與資料保留

明確要求移除時，在執行前立即重查 ownership／source／user scope／state：

```sh
claude plugin uninstall ask-then-do-it@ask-then-do-it --scope user
```

移除最後一個 scope 前，先說明 Plugin data 只有可重建 routing state，預設會刪除；只有你明確要求保留時才加 `--keep-data`。Normal remove 保留 Marketplace、兩個 workflow Config 及其他 scopes；刪除它們屬於另一次 purge 請求。須驗證實際結果，指令失敗不能聲稱已移除。

<a id="zip"></a>
## Session-only ZIP 復原

從[固定版本的預覽 release](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/tag/v1.4.0-preview.1)下載 [ask-then-do-it-claude-1.4.0-preview.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0-preview.1/ask-then-do-it-claude-1.4.0-preview.1.zip)，依該 release 的 checksums 驗證 SHA-256，解壓縮並保留完整 Plugin folder。此 tag 固定於本預覽版，不隨 Marketplace 分支前進。每次 test／recovery session 都以一個加引號參數傳入完整路徑：

```sh
claude --plugin-dir "/path with spaces/ask-then-do-it"
```

這是 `session-only`，不是 `persistent` Marketplace 安裝或更新，每個 session 都須再加 `--plugin-dir`。單跑 `claude plugin list` 不能證明該 ZIP session 已載入；須帶相同 flag 或在該 session 內查看。不建立 local Marketplace、不複製到 `~/.claude/skills`，也不把復原稱作 personal Skill 安裝。Plugin 簡短 START-HERE 連到不可變更的 same-version guide。

<a id="platforms"></a>
## 平台與已知限制

Windows、macOS、Linux 上的 local `terminal CLI`、`VS Code`、`JetBrains` 是 **compatibility target**，不是九組 `live-verified` 組合。此 Adapter 尚未宣稱任何完整 live environment；提出 live 聲明前須記錄 exact OS、surface、Claude Code、Node、active model 與日期。

已於 **2026-09-09** 實際讀取官方文件：

| Surface | 官方文件支援與差異 |
| --- | --- |
| terminal CLI | Local Plugins 可含 Skills、Agents、hooks；CLI 提供完整 commands／skills 介面。文件支援不等於本 Adapter exact host hooks 已驗證。 |
| VS Code | 有圖形化 Plugin 管理，host settings／hooks 與 CLI 共用。Chat panel 內建自己的 CLI，但 commands／skills 只有子集合，須用 `/` 查看；integrated terminal 的 `claude` 另需 standalone CLI。Plugin reviewer 的 invocation／isolation 及兩個 exact namespaced entries 仍須逐 surface 實測。 |
| JetBrains | 官方使用方式是在 IDE integrated terminal 跑 `claude`，external terminal 可用 `/ide` 接入。Plugin 能力來自該 CLI runtime，IDE integration 加入編輯器功能；不能據此宣稱有另一套 graphical command interface，或本 Adapter 行為已驗證。 |

來源：[Plugin components](https://code.claude.com/docs/en/plugins-reference)、[VS Code](https://code.claude.com/docs/en/vs-code)、[JetBrains](https://code.claude.com/docs/en/jetbrains)、[Skills](https://code.claude.com/docs/en/skills)、[Subagents](https://code.claude.com/docs/en/sub-agents)、[hooks](https://code.claude.com/docs/en/hooks)。目前官方文件不能取代 exact 2.1.251 行為驗證；Claude Desktop、web/cloud 不在此 compatibility target。

<a id="troubleshooting"></a>
## 疑難排解

- 入口不存在：檢查實際安裝、source、scope、enabled、reload／新 session。Host bare alias 不是受支援入口契約；VS Code 可能只顯示子集合。
- Routing 停止：區分 Claude Code／model 不支援、Node 遺失／過舊、`UserPromptExpansion` envelope 失敗及 state invalid／pending。不得猜另一個 profile／model 或借用另一 session；僅使用前述有限 explicit fallback。
- 更新失敗：回報 partial state 並停止，不先移除、不換 source、不暗中啟用 disabled Plugin。
- Built-in `/doctor` 只作可選的 Claude Code **安裝／設定健康**檢查，不會轉換、最佳化或驗證 Ask Then Do It Skills；沒有自訂 Plugin doctor 指令。
- Claude Code `2.1.251` 的 native `strict` validation 通過只是 schema 證據；官方工作階段的入口行為、實際模型結果與 live lifecycle smoke 延後至本預覽版之後驗證。不宣稱 context reduction 或計費節省結果。

<a id="feedback"></a>
## 預覽版回饋

請在 [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues)回報可重現問題，附上預覽版 `1.4.0-preview.1`、OS 與 surface、Claude Code／Node 版本、使用中的 model、入口，以及預期／實際結果。分享 logs 前請移除憑證與私人對話內容。

[回到 README](../../README.md)
