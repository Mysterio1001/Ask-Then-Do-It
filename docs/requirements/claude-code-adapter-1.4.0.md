# Ask Then Do It 1.4.0 Claude Code Adapter Requirement Decision Record

Artifact type: Requirement Decision Record

Artifact ID: `claude-code-adapter-1-4-0-requirements`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Target release version: `1.4.0`

Status: Approved

Inputs: 使用者於 2026-08-17、2026-09-01、2026-09-03 與 2026-09-04 逐項確認的 Claude Adapter 決策；Approved Project Knowledge Base；Completed local `1.3.1` release evidence；目前 `1.3.1` Core、Codex、Generic、release、conformance 與文件契約；使用者提供的 Anthropic 文章〈The new rules of context engineering for Claude 5 generation models〉；於 2026-09-01 與 2026-09-04 查核的 Anthropic 官方 Claude Code Skills、Plugins、Plugin marketplaces、Hooks、platforms 與 feature-availability 文件；使用者提供的 `docs/claude_sys/claude-code-adapter-feasibility-analysis.md` 諮詢報告。

Assumptions: Completed local `1.3.1` candidate 是實作基準；不假設 `v1.3.1` 已對外發布。Claude Code 官方契約以 `2.1.251+` 為本需求的最低支援基準。諮詢報告中的 token 預估、模型能力敘述、`/code-review ultra`、`skill-creator` 範例、成本與延遲預估，只有在官方文件、repository evidence 或實測另行支持時才能採用，否則不構成產品契約。

Deferred: Gemini CLI、GitHub Copilot 與其他 AI Agent adapters；通用 Adapter Registry 與跨 host installer；Claude Code `project`、`local`、`managed` Plugin 安裝／更新支援；Anthropic Community Marketplace 送審；Claude Desktop；Claude Code web／cloud sessions；完整九組作業系統與介面實機矩陣；自訂 `/doctor`；Skill 自動轉換；外部 Git tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement。

Handoff: 已依共同核准的 Knowledge Base Change Summary 同步正式 Project Knowledge Base，並交給 `$write-spec` 撰寫 Draft Specification；Specification 核准前不得進入 Ticket Planning 或產品實作。

Approval: 使用者於 2026-09-04 在本完整 Requirement Decision Record 與完整 Knowledge Base Change Summary 展示後，明確回覆「核准」，共同核准兩份文件的精確內容。

## 問題與目標

目前正式消費方式只有 Codex Plugin 與 Generic prompts。Claude Code 使用者沒有原生 Plugin、可驗證的模型 profile 路由、host-specific Config、安裝與更新流程、三語文件或 release evidence。直接把 Codex Skill 原樣複製給 Claude，無法證明 Claude Code lifecycle、命令、模型切換、reviewer 與 context reduction 都符合既有 Core 契約。

`1.4.0` 的目標是在不改變 Full/Lite 工作流語意的前提下，新增原生 Claude Code Adapter。同一個 Claude Plugin 同時包含通用 Claude profile 與 Claude 5 精簡 profile；前者提供相容基準，後者依 Claude 5 context-engineering 原則減少 Plugin 自有載入內容。兩者必須保留相同的 mandatory 行為、核准、安全、證據、artifact 與失敗邊界。

本版同時把 Claude 納入 deterministic release、conformance、文件與 package 契約，但保留 Codex、Generic 既有行為與 `1.3.1` 歷史資料。完成本機 `1.4.0` candidate 不授權任何外部發布動作。

## 使用者與成功訊號

### Claude Code 使用者

- 可透過官方 Claude Plugin／Marketplace 機制，在 `user` scope 安裝及更新一次後跨專案使用。
- 只需理解兩個公開入口：自動路由入口與明確 Claude 5 入口；不需記住每個內部工作階段的指令。
- 使用 Claude 4.6+ 與 Claude Code 2.1.251+ 時，可保留既有 Full/Lite、approval、implementation、Review 與 architecture 行為。
- 模型未知、版本過舊、Node 不可用、來源不符或 router 失敗時，得到明確且不誤導的結果，不會被偷偷切換模型、替換來源或降級。
- Marketplace 無法使用時，可用相符版本 ZIP 啟動一次性的 Claude Code 工作階段。

### 維護者

- 只維護一份 canonical Claude Plugin source，Marketplace 安裝內容與 ZIP 內容由它產生並保持等價。
- 可證明 general 與 Claude 5 profiles 各自通過 100% applicable mandatory scenarios。
- 可證明 Claude 5 profile 在每個固定測量情境中，Plugin-owned loaded-context proxy 至少比 general profile 少 50%。
- 可產生 Codex、Generic、Claude 三個 deterministic package families、ZIP、checksums 與完整 release evidence。
- 至少在一個乾淨真實 Claude Code 環境完成 end-to-end smoke，並誠實區分 live-verified environment 與 compatibility target。
- 英文、繁中、日文文件、連結、安裝命令與 packaged start pages 保持同步。

## 名詞與版本邊界

- **General profile**：供已知受支援、非 Claude 5 的模型，以及自動入口在模型真正未知時使用的通用 Claude 指令設定。
- **Claude 5-optimized profile**：與 general profile 保持相同必要行為、但使用 progressive disclosure 與較少 Plugin-owned loaded context 的指令設定。
- **Automatic entry**：`/ask-then-do-it:ask-then-do-it`，依可信路由狀態選擇 profile。
- **Explicit Claude 5 entry**：`/ask-then-do-it:ask-then-do-it-5`，明確要求 Claude 5 profile，但不切換 active model。
- **Operation-bound profile**：一次公開入口開始一個 operation 時所選的 profile；該 operation 中途不因模型切換而改變。
- **Unknown-model compatibility mode**：router 正常工作，但官方事件沒有提供可可靠分類的 model ID 時，自動入口提示後使用 general profile。它不包含 router、Node 或 state 本身故障。
- **Compatibility target**：設計及自動測試應相容的 OS／介面，不等於已在該組合完成實機驗證。
- **Live-verified environment**：release evidence 已記錄並完成真實 Claude Code smoke 的精確 OS、介面與版本組合。
- **Loaded-context proxy**：只計算 repository 可控制、在固定 checkpoint 實際載入的 Plugin-owned 文字；不是 Claude 總 context、API usage 或帳單。
- **Session-only ZIP recovery**：解壓 Plugin 後以 `claude --plugin-dir <path>` 啟動當次 session；不建立永久安裝或自動更新狀態。

三個最低版本是不同契約：

- Claude model：`4.6+`。
- Claude Code：`2.1.251+`。
- Node.js：`22+`，供自動 router／hooks 執行。

## 範圍

- 新增 canonical source `adapters/claude-code/plugin/ask-then-do-it`。
- 新增 repository-root Claude catalog `.claude-plugin/marketplace.json`，並保持 `.agents/plugins/marketplace.json` 為獨立 Codex catalog。
- 建立官方 Claude Plugin manifest、兩個公開 Skills、general／Claude 5 profiles、按需載入的內部階段模組、router、hooks、唯讀 reviewer agent 與三語 Plugin START-HERE。
- 建立 Claude adapter conformance、capability evidence、router/hook/model-state tests、profile behavior scenarios、context proxy evidence 與官方 Plugin/Marketplace validation。
- 擴充 release definition、builder、inventory、checksums、reproducibility、ZIP equivalence、evidence 與歷史 artifact protection，產生 Codex、Generic、Claude 三個 package families。
- 將 current Core、Codex、Generic、Claude、文件、package、checksum、conformance 與 release evidence identity lockstep 更新為 `1.4.0`。
- 建立 `ask-then-do-it-claude-1.4.0.zip`，內容為完整 Claude Plugin。
- 更新英／繁中／日文 README、root START-HERE、getting-started-simple guides，新增三語 Claude Code guide，並將三語 Claude START-HERE 放入 Plugin／ZIP。
- 以 dependency-free JavaScript 實作跨平台 router，正式相容目標為 Windows、macOS、Linux 上的本機 Claude Code terminal CLI、VS Code extension 與 JetBrains plugin。
- 發布完成前至少執行一次乾淨真實 Claude Code end-to-end smoke。

## 非目標

- 不在 `1.4.0` 同時新增其他 AI Agent adapters、通用 Adapter Registry 或 universal installer CLI。
- 不改變既有 Core Full/Lite 語意，也不讓 Claude 5 context 精簡弱化任何 mandatory rule。
- 不公開 requirements、specification、planning、implementation、review 或 architecture 的額外 slash commands。
- 不支援 Claude Code `project`、`local` 或 `managed` Plugin scope；正式安裝、狀態偵測與更新只處理 `user` scope。
- 不提供拆至 `~/.claude/skills` 的 personal-Skill fallback。
- 不建立 ZIP 專用的 persistent local Marketplace；ZIP 只支援 session-only recovery。
- 不把 Claude Desktop、Claude Code web/cloud 或 Remote Control 當成新的正式執行平台。Remote Control 只可控制原本受支援的本機 session。
- 不要求 Windows／macOS／Linux × CLI／VS Code／JetBrains 九組全部完成實機測試。
- 不切換、pin、override 或替使用者選擇 Claude model。
- 不提供自訂 `/doctor`、Skill 自動轉換或「內建 `/doctor` 會最佳化本 Skill」的承諾。
- 不依賴或宣稱 `/code-review ultra` 是 Review contract。
- 不保證 API billing tokens、總 context、prompt-cache 成本、latency 或金額下降 50%。
- 不在本需求流程建立 tag、push、發布 GitHub Release、上傳 asset、啟用 Marketplace 或公告。

## Plugin 與 Core 行為

Claude Plugin 恰好只公開以下兩個 Skill commands：

1. `/ask-then-do-it:ask-then-do-it`
2. `/ask-then-do-it:ask-then-do-it-5`

Requirements、documented requirements、Specification、Ticket Planning、TDD/direct implementation、Review 與 architecture diagnosis 都是 profile-specific 的內部模組，由公開入口依使用者自然語言、目前階段與 prerequisite 按需載入。內部模組不得被 Claude Code discovery 成第三個以上的公開 Skill command。

兩個 profiles 都必須映射目前 Core 的所有 applicable mandatory rules。Claude 5 profile 可移除重複說明、縮短防禦性文字及把詳細內容延後載入，但不得刪除或改寫 capability honesty、mode resolution、approval gates、artifact states、scope control、TDD/direct 選擇、Review、security、failure disclosure 或 evidence requirements。

Full/Lite 仍採 Approved `1.3.0` 契約。Full 保留 Requirement Decision Record、Specification、Ticket Plan、逐 Ticket 測試選擇、implementation evidence 與 Review；Lite 保留單一 Change Brief gate、禁止新增 behavioral tests、比例適當的 validation、同 context compact Review 及使用者核准修正。Claude Plugin 有 reviewer agent 不得使 Lite 自動升級為 independent Full Review。

## 模型與入口路由

所有 profile 都繼承使用者當下的 active Claude Code model。Skill frontmatter、router、hook 與 reviewer 不得為了選 profile 而切換或鎖定模型。

在 Claude Code 版本與 router runtime 可用時，入口依下表處理：

| 可信 model state | Automatic entry | Explicit Claude 5 entry |
| --- | --- | --- |
| 已知 Claude 5 | Claude 5-optimized profile | Claude 5-optimized profile |
| 已知受支援、非 Claude 5，且版本為 4.6+ | General profile | 提示不相容後改用 general profile |
| 已知 Claude 4.5 或更舊 | 停止並要求切換至 4.6+ | 停止並要求切換至 4.6+ |
| Model ID 真正未知或無法可靠分類 | 提示 compatibility mode，使用 general profile | 提示無法驗證 model，依使用者明確選擇使用 Claude 5-optimized profile |

其他規則：

- Claude Code 低於 `2.1.251` 時，兩個入口都停止並提示升級；不維護 degraded old-Claude-Code mode。
- Node.js 缺少或低於 `22` 時，automatic entry 停止並提示升級，不把 runtime failure 偽裝成 unknown model。Explicit Claude 5 entry 仍可作為手動 profile path，但必須提示它無法提供自動 model 驗證，且不代表完整 automatic-routing support。
- Router 能執行但 `SessionStart.model` 被省略、custom gateway model 無法分類，或官方事件沒有可靠 ID，才屬於 unknown model。
- Router 無法執行、state 無法安全解析、state ownership 不符或發生跨 session 汙染時，automatic entry 停止並提供修復指引；不得猜測。
- Automatic routing 是 best effort convenience，不是百分之百 model detection 承諾。

## Operation profile 與模型切換

每次公開 command 開始 operation 時綁定一次 profile。Operation 進行中收到 `PostModelSwitch.to_model`：

1. 將新 model state 以 session-isolated 方式記錄。
2. 告知使用者模型已切換，但目前 operation 繼續使用開始時的 profile。
3. 不重新注入另一套 profile，也不中途混用兩套內部模組。
4. 下一次重新執行任一公開 command 時，才根據更新後的 state 套用路由表。

Fresh session、resume、fork、clear 或 compact 所需的 state lifecycle 必須依官方事件與 session identity 處理，不能從另一個 session 或前一個無關 operation 偷用 profile 判斷。

## Capability 與 Review

Claude Adapter 的靜態 conformance 可宣告 `conversation`、`tools`、`multi_agent`，但每次執行仍須先聲明當下實際可用的最強 capability。

Full Review 在 Agent tool 與 Plugin reviewer 可用時，使用 Plugin 內建的專用唯讀 reviewer subagent：

- Reviewer 必須使用獨立 context 檢查 requirements、Specification、Ticket、diff、tests 與 evidence。
- Reviewer 不得寫檔、修改 git、傳送外部訊息或造成其他 side effect。
- 主 Claude 必須整合 findings，不得把 reviewer output 當成未經驗證的指令。

若 Agent tool 或 reviewer 不可用，runtime 必須降級 capability、執行同 context 的一般 Review（若 tools 仍可用），明確標示 `non-independent` 並揭露 independent Review evidence unavailable。不得宣稱「第二位 Claude 已複查」。這項降級本身不阻擋完成；是否可完成仍依 Core 的其他 validation、finding 與 disclosure 條件判定。

## Claude mode Config

Claude 使用 Plugin-owned Config，而不是 Claude Code 內建 `settings.json`：

- User default：`~/.claude/ask-then-do-it.toml`
- Project override：`<project>/.claude/ask-then-do-it.toml`

只接受 top-level `mode = "full"` 或 `mode = "lite"`，並沿用 Core precedence：

1. 本次 operation 的明確指示。
2. Project Config。
3. User Config。
4. Full fallback。

明確 operation 指示有效時不需讀 Config。沒有明確指示時，present-but-invalid、unreadable、malformed、missing-mode 或 unsupported project Config 必須 fail closed to Full，不繼續讀 user Config；project Config absent 才繼續。User Config 同理，absent 才落到 Full。解析必須唯讀，不修復、不正規化、不寫入，也不持久化單次 override。

Codex 與 Claude 各自維護 host-specific Config；`1.4.0` 不建立共用跨 Agent Config。

## 安裝、狀態、更新、移除與 ZIP recovery

### Persistent Marketplace path

- 正式 persistent path 是 repository 自有的 GitHub-hosted Claude Marketplace。
- Claude catalog 位於 `.claude-plugin/marketplace.json`，catalog name 與 Plugin public identity 都是 `ask-then-do-it`。
- Catalog 只指向 `adapters/claude-code/plugin/ask-then-do-it`，Plugin source pin 正式 `v1.4.0` tag；不得解析至同名 Codex source。
- Claude 與 Codex catalogs、schema、validator、metadata 與 source path 各自維護；兩個 catalogs 都不得進 consumer ZIP。
- `1.4.0` 只支援 Claude `user` scope。任何偵測到的 `project`、`local`、`managed` 或同名其他來源狀態都不得被當成可自動修改的正式安裝。

### State-aware lifecycle

- Ask Then Do It 的 status 或 version-check guidance 純讀，不授權任何 Marketplace、Plugin、Config 或檔案寫入。它仍須唯讀檢查並分別回報 Claude Code version、Node availability/version、Marketplace source、qualified Plugin identity、scope、installed version 與 enabled state；失敗或不相容時只報告，不自動修復。
- 對 Ask Then Do It 發出的明確 install、update 或 remove request，只授權該次 guidance 完成動作必要的最小 `user`-scope writes。產品不得自行啟用 Claude Code 的 background auto-update；若使用者已在 host 啟用該功能，該 host 行為不屬於本產品可禁止或冒充為 AI 授權的寫入。
- 寫入前必須查核 Claude Code version、Node version（automatic route）、Marketplace source、Plugin qualified identity、scope、installed version 與 enabled state。
- 已是正確目前版本時回報 no-op，不重裝。
- Marketplace source mismatch、同名衝突、scope ambiguity、unsupported version、unreadable state 或任何命令失敗時立即停止，保留已知狀態並回報；不得 remove-first、覆蓋未知來源、猜 alternate source 或自動 downgrade。
- 正常 remove 只 uninstall `user`-scope Plugin；不得順便刪除獨立 Ask Then Do It Config 或移除仍可能供其他 Plugin 使用的 Marketplace。完整 purge 必須有另一次明確要求。
- 依官方 lifecycle，最後一個 scope 的 uninstall 預設刪除 `${CLAUDE_PLUGIN_DATA}`；只有使用者明確要求保留時才使用 `--keep-data`。刪除前須說明其中只有可重建的 Plugin routing state，不得把它描述成使用者成果或專案 artifact。
- 安裝或更新完成後，依 Claude Code lifecycle 指示 reload 或開啟新 session；不能宣稱舊 session 已自動切換到新 Plugin bytes。

### Session-only ZIP recovery

- Release asset 名稱固定為 `ask-then-do-it-claude-1.4.0.zip`。
- Marketplace-installed Plugin runtime payload 與 ZIP 內的 Plugin runtime payload 都從同一 canonical source 衍生，並通過 behavior、runtime inventory 與 content equivalence checks；expanded Claude package 與其 ZIP 則必須逐檔 byte-equivalent。
- 使用者以 `claude --plugin-dir <extracted-plugin-path>` 啟動當次 session。
- ZIP 不建立 persistent Marketplace，不寫入 `~/.claude/skills`，也不提供自動更新；每次 ZIP-backed session 都要再次給 `--plugin-dir`。
- 想恢復 persistent install/update 時，必須修復並重新使用正式 GitHub Marketplace path。

## Router state、資料與安全

- Router 使用零第三方 runtime packages 的 JavaScript，要求 Node.js 22+，hooks 採 Claude Code cross-platform exec form。
- Immutable Plugin resources 只從 `${CLAUDE_PLUGIN_ROOT}` 讀取；不得把 runtime state 寫回 cached Plugin directory。
- Persistent runtime state 只存於 `${CLAUDE_PLUGIN_DATA}`，並以 Claude `session_id` 隔離及 schema version 管理。
- State 只保存 routing 所需最小資料，例如 schema version、session key、最近可信 model classification、operation profile binding 與必要時間／來源資訊。
- State 不得保存 prompt、task description、repository source、Requirement／Specification 內容、credential、secret、token 或個人資料，也不得增加 telemetry 或額外第三方傳輸。
- Hook JSON input、model ID、session ID 與 path 都視為需驗證的 structured input；不得直接拼接成 shell command 或不受限制的 filesystem path。
- Invalid、stale、schema-incompatible 或 cross-session state 不得被信任。能安全辨識為「model 資訊缺失」時按 unknown 規則；router 或 ownership 本身不安全時停止 automatic entry。

## Package、版本與 release integrity

`1.4.0` release 必須 lockstep 更新 current Core、Codex、Generic、Claude Adapter、Plugin manifest、catalog refs、conformance、current docs、package names、download URLs、checksums 與 release evidence。Current source declarations會明確前進到 `1.4.0`；Completed `1.3.1` requirements、Specification、Ticket Plan、evidence、其中記錄的 source／artifact hashes，以及任何已凍結的歷史 release references 保持不可變。

Release 產生三個 expanded consumer packages、三個對應 ZIP 與一份完整 checksum inventory：

- Codex family：沿用既有內容與命名規則，版本更新為 `1.4.0`。
- Generic family：沿用既有內容與命名規則，版本更新為 `1.4.0`。
- Claude family：完整 Claude Plugin 與 `ask-then-do-it-claude-1.4.0.zip`。

Claude package 至少包含官方 manifest、兩個公開 Skills、兩個 profiles、按需內部模組、router、hooks、reviewer agent、三語 START-HERE，以及依現有 release policy 必需的 license／notice files。精確 inventory 必須在 Specification 固定；runtime payload 由 canonical source 衍生，release-only legal files 若依既有 builder policy 加入則必須可追溯，expanded package 與 ZIP inventory/bytes 必須完全一致。Marketplace catalog 不屬於 package inventory。

現有 staging validation、managed-output replacement、rollback、unmanaged collision protection、two-build reproducibility、ZIP equivalence、SHA-256、removed-artifact scan、historical preservation 與 release-evidence gates 不得退化。Node.js 只可成為 Claude consumer prerequisite，不能滲入 Codex 或 Generic runtime inventory。

## Claude 5 context reduction 與 evidence

Context reduction 有兩個依序執行的硬門檻：

1. General 與 Claude 5 profiles 各自通過 100% 相同 applicable mandatory behavior scenarios。
2. 行為門檻通過後，Claude 5 profile 在每個固定情境與 checkpoint 的 loaded-context proxy 都至少比 general profile 少 50%。

任何情境的行為失敗都不能用 context 減少抵銷；任何單一測量情境未達 50% 也不能用平均值掩蓋。

Proxy 只計算該 profile 在測量點實際載入的 repository-controlled Plugin text：

- Invoked public entry Skill body。
- 該次按需載入的 internal stage modules 與 references。
- 該 session 實際注入的 router／hook text。

排除相同 host system prompt、tool/MCP definitions、user task text、repository source、必要 tool output、hidden reasoning 與 model output。

Release evidence 對每個情境保存 general 與 Claude 5 的 source paths、load order、SHA-256、normalized byte count、proxy-token count、公式、raw results 與 reduction。Claude `/context`、`claude plugin details` projected cost 或觀察到的實際 usage 可作非阻擋 diagnostics，但不得取代 deterministic gate，也不得轉成 billing-saving claim。另需 fresh-session evaluation 證明精簡版不是只在靜態字數上較短。

## 平台與 live smoke

正式 local host contract 涵蓋 Claude Code terminal CLI、VS Code extension 與 JetBrains plugin。Router 與 path/state behavior 的設計及自動測試 compatibility targets 為 Windows、macOS、Linux，但不宣稱九個 OS × interface 組合都已 live-tested。

Release evidence 必須列出實際 live-verified 的 OS、interface、Claude Code version、Node version 與 model state。未實測組合只能稱為 compatibility target。

`1.4.0` 完成前，至少一個乾淨真實 Claude Code environment 必須完成：

1. `user`-scope Marketplace add／install 與狀態確認。
2. 兩個公開 commands 的 discovery 與執行。
3. 以該環境實際可用的 supported model 驗證 automatic 與 explicit entry；不能取得的 unknown、unsupported 或其他 model branches 不得冒充 live observation。
4. Model switch state 更新，且目前 operation profile 不變、下次 invocation 才改路由。
5. Session state isolation。
6. 從受控舊 candidate 更新至 `1.4.0` candidate。
7. Plugin remove 與重新安裝或 recovery。
8. ZIP `--plugin-dir` session-only recovery。

完整 routing table 另由 deterministic injected `SessionStart`／`PostModelSwitch` events 與 router-state fixtures 覆蓋，並在 evidence 清楚標示為 simulated branch validation，不得稱為真實 model observation。

在外部 tag／Marketplace 尚未獲准發布前，smoke 可使用 isolated local git／Marketplace fixture 與 exact candidate bytes 驗證真實 Claude Code lifecycle，但 evidence 必須明示尚未驗證 GitHub public transport。不得為了 smoke 偷做未授權的 tag、push 或 publication。完全沒有可用的真實 Claude Code 環境時，release completion 必須被阻擋。

## 文件契約

- `README.md` 保留現有英／繁中／日文平行布局與既有內容順序。每種語言仍依 Introduction、Quick Start、CLI automatic installation、manual installation、further reading 排列，只在對應位置加入 Claude，不重構無關 Codex／Generic 內容。
- Root `START-HERE.en.md`、`START-HERE.zh-TW.md`、`START-HERE.ja.md` 加入 Claude Code consumer choice。
- 新增 `docs/guides/claude-code.en.md`、`.zh-TW.md`、`.ja.md`，作為 Claude 版本需求、`user` scope install/status/update/remove、兩入口、routing、Config、reviewer、platform、ZIP recovery 與 troubleshooting 的詳細 owner。
- 三語 `docs/guides/getting-started-simple.*.md` 加入 Claude Code 起始方式，但仍由它們擁有 provider-neutral Full/Lite 說明。
- Claude Plugin／ZIP 內含三語短版 START-HERE，連到相同版本的 detailed guide，不複製整份流程說明。
- 三語內容必須語意等價；root、Codex、Generic、Claude 共 12 個 START-HERE pages 的連結、簡潔性與 package copies 都受 release tests 保護。
- 文件必須清楚區分 Claude model、Claude Code、Node 三種版本需求；known unsupported、unknown model、runtime failure；automatic 與 explicit `-5`；compatibility target 與 live-verified environment；persistent Marketplace 與 session-only ZIP。
- Claude Code 內建 `/doctor` 只能列為選用的 Claude Code 安裝／設定健康檢查，不得宣稱它會轉換、最佳化或驗證 Ask Then Do It Skills。

## 失敗、安全、隱私與操作邊界

- 已知不受支援的 Claude model 或 Claude Code version 必須停止，不得降成「相容模式」。
- 真正未知的 model state 可依路由表處理；router/runtime/state failure 必須停止 automatic entry，不得混為 unknown。
- Hook、Agent 或 Marketplace failure 不得產生虛構成功、獨立 Review、安裝版本或已驗證平台聲明。
- Plugin 不得新增 credentials、使用者 prompt、repository content、個人資料或 telemetry 的持久化與外傳。
- 不得因 Claude Adapter 變更 Codex／Generic capability claims、Full/Lite observable behavior 或 consumer runtime dependency。
- Release、installation、update、remove 與 recovery evidence 必須記錄實際執行結果；未執行或失敗的 check 不得標為 pass。
- External publication 仍由 maintainer 另行控制；本需求核准不授權外部 mutation。

## 驗收條件

1. 在受支援 Claude Code 上，canonical Plugin directory 與 repository Marketplace root 各自執行官方 `claude plugin validate <path> --strict` 並 exit `0`；Plugin manifest、Marketplace catalog、hooks、兩個 Skills 與 reviewer 沒有被 strict mode 放行的 warning 或 error。
2. Claude catalog 位於 `.claude-plugin/marketplace.json`、只指向 tag-pinned Claude source，且與 Codex catalog/schema/validator 分離。
3. Claude Plugin 只公開兩個核准 commands；所有階段模組按需載入且不成為額外公開 commands。
4. Claude Code `<2.1.251`、Node `<22`／missing、known Claude `<4.6`、known Claude 5、known supported non-5、unknown model、router failure 與 explicit `-5` 的結果逐一符合路由表及 failure boundary。
5. 兩個 profiles 都繼承 active model；沒有 Plugin component 因 profile 選擇而 pin、override 或 switch model。
6. `PostModelSwitch` 只更新下次 invocation 的路由；同一 operation 不混用 general 與 Claude 5 instructions。
7. Routing state schema-versioned、per-session isolated；invalid、stale 或 cross-session state 不被信任，且不保存 task、source、credential 或個人資料。
8. General 與 Claude 5 profiles 各自通過 100% applicable Core、Full/Lite、approval、safety、evidence、artifact、routing 與 failure scenarios。
9. Full 在 reviewer 可用時取得唯讀 independent Review；不可用時正確降級、標示 `non-independent`，不宣稱獨立證據。Lite 仍維持原 approved compact Review。
10. Claude mode Config 的 precedence、absent／invalid 行為、唯讀解析與 no-persistence override 全部符合 Core；不讀寫 Claude `settings.json`，也不共用 Codex Config。
11. Status check 完全唯讀並分別回報 Claude Code、Node、Marketplace source、qualified identity、scope、version 與 enabled state；install、update、remove 僅在明確授權後修改正確 `user` scope。Current version no-op、source mismatch、ambiguous scope、unsupported state 與 command failure 均 fail safe。
12. Marketplace lifecycle 使用 qualified Claude identity，不誤改同名 Codex或其他來源；正常 remove 不連帶刪 Config 或任意移除 Marketplace。最後 scope uninstall 預設刪除 disposable `${CLAUDE_PLUGIN_DATA}` 並事前揭露；只有明確要求保留時才使用 `--keep-data`，且兩條路徑都有驗證。
13. Marketplace-installed Plugin 與 ZIP runtime payload 由同一 canonical source 衍生並通過 behavior/content equivalence，expanded package 與 ZIP 通過 exact inventory/byte equivalence；ZIP 只以 `--plugin-dir` 支援當次 session，沒有 persistent install/update claim。
14. 每個固定 context scenario 先通過行為 gate，再證明 Claude 5 loaded-context proxy 至少減少 50%，且保存完整可重算 raw evidence。
15. General 與 Claude 5 profiles 在相同固定 fresh-session cases 達成相同 mandatory outcomes，並保存輸入、profile、observable result 與 pass/fail evidence；精確 case inventory 留給 Specification 固定。
16. Cross-platform automated tests 覆蓋 Windows、macOS、Linux 的 path、exec、event parsing、state isolation 與 failure behavior；官方 feature-availability/platform evidence 亦確認 terminal CLI、VS Code 與 JetBrains 共用本需求依賴的 local Plugin、Skill、Agent 與 hook contract，任何差異都須在文件揭露。
17. 至少一個乾淨真實 Claude Code environment 完成核准的 install、兩入口、實際可用 supported-model routing、switch、update、remove、reinstall/recovery smoke，並記錄 exact environment；其餘 routing branches 以明確標示的 injected-event tests 驗證，不冒充 live model evidence。沒有真實 smoke 則 release blocked。
18. README 保留三語平行 layout；三語 root START-HERE、Claude guides、getting-started guides 與 Plugin START-HERE 完整、連結有效、語意同步，12 個 START-HERE contract 通過。
19. Release 產生三個 expanded families、三個 ZIP 與完整 checksums；兩次 isolated build byte-reproducible，expanded/ZIP equivalent，catalogs 不進 ZIP。
20. Current identity 全部一致為 `1.4.0`，Claude ZIP 名稱為 `ask-then-do-it-claude-1.4.0.zip`，且 `1.3.1` historical artifacts/hashes 保持不變。
21. Codex 與 Generic 除核准的 identity、跨入口文件與 release inventory 擴充外，既有 observable behavior、package contents 與 runtime dependencies無回歸。
22. Packages、logs、fixtures 與 evidence 不含 credential、個人狀態、未清理 routing state、機器專屬絕對路徑或未授權資料。
23. 本地 candidate 不包含 Community Marketplace listing、自訂 `/doctor`、Skill 自動轉換、`~/.claude/skills` fallback、billing/cost guarantee 或任何未授權 external publication mutation。

## 已確認決策

- 第一個新增 Agent 是 Claude，target release 為 `1.4.0`；其他 Agent 一版一版延後。
- 同一 Claude Plugin 安裝 general 與 Claude 5 profiles，只公開兩個 namespaced commands。
- Automatic entry best effort 判斷；known Claude 5 用精簡版，known supported non-5 用通用版，unknown 用 general compatibility mode，known `<4.6` 停止。
- Explicit `-5` 不切模型；known supported non-5 改用 general，unknown 可依明確選擇使用精簡版。
- Profile 在 operation 內固定，模型切換於下次 command 才重新路由。
- Claude model baseline `4.6+`、Claude Code baseline `2.1.251+`、automatic router Node.js baseline `22+`。
- 一個唯讀 reviewer 支援 independent Full Review；不可用時誠實降級為 non-independent Review。
- Claude 使用獨立 `.claude/ask-then-do-it.toml` Config，不使用 built-in `settings.json` 或跨 Agent 共用 Config。
- 正式 persistent distribution 是自有 GitHub Marketplace 的 `user` scope；ZIP 是同內容、session-only 的 `--plugin-dir` recovery。
- Claude 與 Codex catalogs/source/schema/validator 分離；Claude canonical source 與 ZIP 命名已固定。
- 兩 profiles 都須 100% mandatory conformance；Claude 5 每個固定 scenario 的 Plugin-owned proxy 至少減少 50%。
- Windows、macOS、Linux 與 local CLI/VS Code/JetBrains 是 compatibility contract，不要求九組 live matrix；至少一個真實 clean smoke 是 release hard gate。
- Claude Desktop、web/cloud、Community Marketplace、自訂 `/doctor`、自動轉換與 personal-Skill fallback 延後或排除。
- README 保留現有布局，Claude 享有完整英／繁中／日文文件與 release tests。
- `1.4.0` 將 Core、Codex、Generic、Claude、文件、packages 與 evidence lockstep 更新；`1.3.1` 歷史不改，外部發布另行核准。

## 明確共識證據

使用者於 2026-08-17、2026-09-01、2026-09-03 與 2026-09-04 逐項明確回覆「核准」、「要」或「是」，確認本紀錄所列的 Claude-first scope、Plugin 形式、兩個入口、版本 baseline、路由、profile binding、Review、Config、distribution、ZIP、context gate、平台、live smoke、文件及 release 邊界。使用者並於 2026-09-04 在完整本紀錄與完整 Knowledge Base Change Summary 展示後明確回覆「核准」，構成本紀錄與該摘要的正式共同核准證據。
