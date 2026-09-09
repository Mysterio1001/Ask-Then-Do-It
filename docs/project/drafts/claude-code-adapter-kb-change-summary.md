# Ask Then Do It 1.4.0 Claude Code Adapter Knowledge Base Change Summary

Artifact type: Knowledge Base Change Summary

Artifact ID: `claude-code-adapter-1-4-0-kb-change-summary`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Status: Approved

Inputs: Approved `claude-code-adapter-1-4-0-requirements`；同步前的 Approved Project Knowledge Base；Completed local `1.3.1` release evidence；2026-09-04 重新查核的 Anthropic 官方 Claude Code Plugin、Marketplace、Skills、Hooks、CLI 與 platform contracts。

Assumptions: 本摘要只描述 Requirement Decision Record 與本摘要共同核准後可同步的正式知識。它把 `1.4.0` 記為 approved implementation target，不宣稱 Claude Adapter 已完成、`1.4.0` 已發布，或 `v1.3.1` 已在外部可用。

Deferred: Specification、Ticket Plan、implementation、Completed `1.4.0` release evidence、Git tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement；其他 AI Agent adapters；通用 Adapter Registry／跨 host installer；Claude Code `project`／`local`／`managed` Plugin scopes；Anthropic Community Marketplace；Claude Desktop；Claude Code web/cloud sessions。

Handoff: 下列明示變更已同步至正式 Project Knowledge Base，並已交給 `$write-spec` 撰寫 Draft Specification。

Approval: 使用者於 2026-09-04 在完整 Requirement Decision Record 與本摘要展示後明確回覆「核准」，共同核准兩份文件的精確內容。

## Additions

### Glossary

- 新增 **Claude general profile**：供已知受支援的非 Claude 5 model，以及自動入口的 unknown-model compatibility mode 使用；不切換或 pin 使用者的 active model。
- 新增 **Claude 5-optimized profile**：與 general profile 保持相同 applicable mandatory workflow 行為，但用 progressive disclosure 減少 Plugin-owned loaded context。
- 新增 **operation-bound profile**：每次公開 Ask Then Do It command 開始時綁定 profile；操作途中切換 model 只更新下次呼叫的路由，不混用本次操作的兩套 instructions。
- 新增 **unknown-model compatibility mode**：router 正常但 model ID 無法可靠分類時，自動入口提示後使用 general profile；router／Node／state failure 不屬於 unknown model。
- 新增 **compatibility target** 與 **live-verified environment**：前者是設計與自動測試應相容的 OS／介面，後者是 release evidence 已實際跑過真實 Claude Code smoke 的精確環境。
- 新增 **Claude session-only ZIP recovery**：使用 `claude --plugin-dir <path>` 載入完整 Plugin，只對該 session 生效，沒有 persistent install 或 managed update claim。
- 新增 **Claude loaded-context proxy**：只計固定 checkpoint 實際載入的 repository-controlled Plugin text，不代表 Claude 總 context、API usage 或帳單。

### Architecture map（全部為 Approved `1.4.0` target architecture，尚未冒充現況）

- 新增 approved `1.4.0` target：`adapters/claude-code/plugin/ask-then-do-it/` 是 canonical Claude Plugin source，包含官方 manifest、兩個公開 Skills、general／Claude 5 profiles、按需階段模組、router/hooks、唯讀 reviewer agent 與三語 START-HERE。
- Approved target 新增 `.claude-plugin/marketplace.json`：Claude 專用 repository catalog，只解析到 Claude Plugin source；它與 `.agents/plugins/marketplace.json` 的 Codex catalog 分離，且兩者都不進 consumer ZIP。
- Approved target 新增 Claude host Config ownership：`~/.claude/ask-then-do-it.toml` 與 `<project>/.claude/ask-then-do-it.toml`。
- Approved target 新增 Claude runtime state ownership：immutable resources 從 `${CLAUDE_PLUGIN_ROOT}` 讀取；session-isolated、schema-versioned routing state 存於 `${CLAUDE_PLUGIN_DATA}`。
- Approved target 新增 dependency-free JavaScript router：使用 `SessionStart.model` 與 `PostModelSwitch.to_model` 做 best-effort routing，要求 Node.js `22+`。
- Approved target 新增 Claude adapter conformance、official Plugin/Marketplace validation、router/hook tests、雙 profile behavior/context gates 及真實 Claude Code smoke evidence。

### Important decisions

- `1.4.0` 第一個新增的 AI Agent target 是 Claude Code；其他 Agents 與 universal Adapter Registry 延後。
- 一個 Claude Plugin 同時提供 general 與 Claude 5 profiles，但只公開 `/ask-then-do-it:ask-then-do-it` 與 `/ask-then-do-it:ask-then-do-it-5`。
- Claude model baseline 是 `4.6+`。已知 4.5 或更舊時停止；只有 model ID 真正未知時才使用 compatibility behavior。
- Claude Code baseline 是 `2.1.251+`；更舊版本不提供 degraded support。
- Node.js `22+` 是 automatic router 的 Claude consumer prerequisite；缺少或過舊時 automatic entry 停止，explicit `-5` 只能作有明確限制提示的手動 profile path。
- General 與 Claude 5 profiles 都繼承 active model，不 pin、override 或 switch model。
- Profile 在一次 operation 內保持穩定；`PostModelSwitch` 更新 state，但只在下一次公開 command 重新路由。
- Automatic entry：known Claude 5 用 optimized；known supported non-5 用 general；unknown 用 general compatibility mode。Explicit `-5`：known Claude 5 用 optimized；known supported non-5 提示後用 general；unknown 依使用者明確選擇用 optimized。Known `<4.6` 兩者皆停止。
- Claude mode Config 的 precedence 是本次明確指示、project Config、user Config、Full fallback；present invalid Config fail closed to Full，且解析不寫入。Claude 不使用 built-in `settings.json` 或 Codex Config。
- Claude Adapter conformance 支援 `multi_agent` 並提供唯讀 Full reviewer；reviewer unavailable 時 runtime 降級為同 context `non-independent` Review並揭露限制，不冒稱獨立複查。Lite 維持既有 compact Review。
- 正式 persistent distribution 是 repository 自有 GitHub Marketplace 的 `user` scope；`project`、`local`、`managed` scopes 延後。
- Marketplace-installed Plugin 與 Claude ZIP runtime payload 從同一 canonical source 衍生；ZIP 是 `--plugin-dir` session-only recovery，不建立 local Marketplace 或 personal Skill fallback。
- Ask Then Do It 的 status/update guidance read-before-write；status 唯讀回報 Claude Code、Node、Marketplace source、qualified identity、scope、version 與 enabled state。只有明確 install/update/remove request 授權該次最小必要 writes。來源不符、狀態不明或 command failure 即停止，不 remove-first、不自動覆蓋、降版或猜替代來源。
- 正常 removal 只 uninstall qualified `user`-scope Plugin，不移除 Marketplace 或獨立 mode Config。最後 scope uninstall 依 Claude Code 預設刪除 disposable `${CLAUDE_PLUGIN_DATA}`；保留 data 需使用者明確要求。
- Routing state 只保存 session key、可信 model classification、operation profile binding、schema version等最小必要資料；不得保存 prompt、task、repository source、credentials、secrets或個資，不新增 telemetry／第三方傳輸，且 hook input／paths必須驗證後使用。
- 兩個 profiles 各自必須通過 100% applicable mandatory behavior scenarios。
- Claude 5 profile 在每個固定 scenario 都必須比 general profile 少至少 50% Plugin-owned loaded-context proxy，並保存可重算 raw evidence；不得宣稱總 context 或帳單節省 50%。
- General 與 Claude 5 profiles 另須在相同固定 fresh-session cases 達成相同 mandatory outcomes並保存可稽核結果，不能只靠靜態文字計數。
- `1.4.0` lockstep 更新 current Core、Codex、Generic、Claude、current docs、packages、checksums、conformance 與 release evidence；active source declarations明確前進到 `1.4.0`，而 Completed `1.3.1` requirements、Specification、Ticket Plan、evidence、其中記錄的 hashes 與凍結歷史 references 保持不可變。
- Release target 由 Codex、Generic 擴為 Codex、Generic、Claude 三個 package families；Claude ZIP 固定命名 `ask-then-do-it-claude-1.4.0.zip`。
- Local Claude contract 涵蓋 terminal CLI、VS Code、JetBrains；Windows、macOS、Linux 是 compatibility targets，不是九組都已 live-tested 的聲明。
- Release 前至少一個乾淨真實 Claude Code environment 必須完成 install、兩入口、實際可用 supported-model routing、model switch、update、remove、reinstall/recovery smoke；完整 routing table 的 unavailable/unsupported branches 以明確標示的 deterministic injected-event tests 驗證，不冒充 live model evidence。沒有真實環境就不能完成 release。
- Claude Desktop、web/cloud 延後；Remote Control 只控制既有支援的本機 session，不是獨立 platform。
- 英／繁中／日文 README、root START-HERE、getting-started、Claude guide 與 Plugin START-HERE 必須同步，並保留目前 README layout。
- `1.4.0` 不提供自訂 `/doctor`、Skill 自動轉換、`/code-review ultra` contract 或 `~/.claude/skills` fallback。
- Anthropic Community Marketplace submission 與所有 external publication mutation 都另行決定，不是 `1.4.0` 本機 candidate 完成條件。

### External dependencies

- 新增 Anthropic 官方 Claude Code Plugin、Marketplace、Skills、Hooks、model-switch、CLI 與 local platform contracts。
- 新增 Claude Code `2.1.251+`。
- 新增 Claude model `4.6+` availability。
- 新增 Node.js `22+`，僅為 Claude automatic-router consumer runtime prerequisite，不是 Codex／Generic dependency。
- 新增至少一個可用的乾淨真實 Claude Code environment，作為 `1.4.0` release smoke prerequisite。
- GitHub repository tags／Releases 擴充為 Claude tag-pinned Marketplace source 與 version-matched ZIP 的外部承載位置；其實際發布仍需另行核准。

### Unresolved items

- Claude Plugin manifest、Marketplace entry、hooks、agent、router state 與 release inventory 的精確 Specification／implementation 形式仍待定稿及驗證；這些是技術設計，不是未決產品偏好。
- 首次 live smoke 實際使用哪個 OS／surface/model，以及觀察到的結果，必須由 release evidence 記錄；未實測組合不得標為 verified。
- External `v1.3.1` 與未來 `v1.4.0` tag、GitHub Release、asset upload、Marketplace activation 與 announcement 狀態仍須在外部 mutation 前查證並另行授權。
- Anthropic Community Marketplace 是否送審仍為 future external-publication decision。

### Artifact links

- 新增 Requirement Decision Record：[Claude Code Adapter 1.4.0](../../requirements/claude-code-adapter-1.4.0.md)。
- 新增 `1.4.0` Specification：[Claude Code Adapter 1.4.0](../../specs/claude-code-adapter-1.4.0.md)（Draft，pending Specification approval）。
- 新增 `1.4.0` Ticket Plan：pending Approved Specification。
- 新增 Completed local release evidence：[Ask Then Do It release 1.3.1](../../evidence/ask-then-do-it-release-1.3.1.md)。
- `docs/claude_sys/claude-code-adapter-feasibility-analysis.md` 保持 consultation input，不升格為正式 project knowledge；未經官方或 repository evidence 支持的內容不成為契約。

## Modifications

### Envelope

- 將 Project Knowledge Base `Core version` 從 `1.3.0` 更新為已由 Completed local release evidence 證明的 `1.3.1`；不提前寫成尚未實作的 `1.4.0`。
- `Inputs` 加入 Completed `1.3.1` release evidence 與 Approved Claude Requirement Decision Record。
- `Assumptions` 改為：Completed local `1.3.1` candidate 是 implementation baseline；不假設 external `v1.3.1` availability；`1.4.0` 是 approved target，尚未實作或發布。
- `Deferred` 保留既有項目，再加入本摘要所列 Claude future scope 與 external publication boundaries。
- `Handoff` 改為依核准後的 Claude Requirement 進入 Specification；不宣稱 implementation 已開始。
- `Approval` 追加本次 Requirement Decision Record 與 Knowledge Base Change Summary 的共同核准證據。

### Glossary

- 將 **Repository marketplace** 改為 provider-specific 定義：Codex 使用 `.agents/plugins/marketplace.json`；Claude 使用 `.claude-plugin/marketplace.json`；Claude catalog 與 Claude Plugin identity 都固定為 `ask-then-do-it`，同時仍與 Codex 的 schema、validator、source path 與 release metadata 分離，且兩個 catalogs 都不進 consumer ZIP。
- 將 **Official Plugin source** 改為複數的 provider-specific sources：同一 GitHub repository 與 formal tag 下，Codex 保留 `adapters/codex/plugin/ask-then-do-it`，Claude 使用 `adapters/claude-code/plugin/ask-then-do-it`。
- 將 **AI-assisted update** 從 Codex-only 擴充為 host-specific、state-aware guidance；Claude 只支援 `user` scope，且不主動開啟或冒充 Claude Code 自身可選的 background auto-update。
- 將 **ZIP fallback** 擴充為 host-specific lifecycle：Codex 既有 fallback 不變；Claude ZIP 每個 session 都需明確 `--plugin-dir`，不建立 persistent Marketplace installation 或 automatic-update state。

### Architecture map

- 修改 `release/release.json` 與 builder 說明：Completed `1.3.1` 現況仍產 Codex＋Generic；Approved `1.4.0` target 新增 Claude family，並保留完整 staging、replacement、rollback 與 deterministic guarantees。
- 修改 `dist/` 說明：區分 Completed `1.3.1` 的兩個 families 與 Approved `1.4.0` 的三個 families，避免把尚未產生的 Claude artifacts 寫成現況。
- 修改 `tests/release/` 說明：Approved target 新增 Claude Marketplace/schema、Plugin/package inventory、router/hooks、雙 profile 100% behavior、每情境 50% proxy、三語文件與 live-smoke evidence gates。

### Important decisions

- 將「`1.3.1` 是 maintenance target」更新為「`1.3.1` maintenance scope 已完成為 frozen local candidate」並引用 Completed release evidence；外部發布狀態仍未知。
- 保留 `1.3.1` 的 Pillow、Windows `WinError 5`、serial build、rollback 與 excluded-scope 事實，不由 `1.4.0` 改寫。
- 將 catalog policy 擴充為 provider-specific catalogs：各 catalog 留在 repository、installable entry pin 對應 formal tag、Claude 與 Codex source 不可互指。

### External dependencies

- 保留 OpenAI Codex dependency。
- 擴充 GitHub dependency，使它同時承載各自獨立的 Codex／Claude catalog entries 與 release assets，不改 repository identity。
- 保留 CPython 3.12／Pillow 12.x 的 `1.3.1` development-only boundary；Node.js 不得被寫成 Codex 或 Generic consumer dependency。

### Unresolved items

- 保留 local Codex CLI help 未驗證的歷史限制，除非後續已有實際相反證據。
- 保留 external `v1.3.1` publication 尚未確認。
- 加入上述 Claude technical-validation、live-environment 與 external-publication items；不把 compatibility target 寫成 verified environment。

### Artifact links

- 保留全部既有 1.0.0、1.2.0、1.3.0、1.3.1 Requirement／Specification／Ticket Plan／evidence links。
- 補上 Completed `1.3.1` release evidence。
- 加入 Claude `1.4.0` Requirement；Specification 與 Ticket Plan 建立並核准後再把 pending 換成正式連結。

## Removals

- 移除已被 Completed local `1.3.1` release evidence supersede 的 Assumption：「`1.3.1` is the approved maintenance target until implementation and release evidence establish completion」。
- 不移除或改寫任何歷史 Requirement、Specification、Ticket Plan、Review、release evidence、tag reference、Pillow 或 Windows `WinError 5` 事實。
