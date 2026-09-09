# Ask Then Do It 1.4.0 Claude Code Adapter Specification Knowledge Base Change Summary

Artifact type: Knowledge Base Change Summary

Artifact ID: `claude-code-adapter-1-4-0-spec-kb-change-summary`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Status: Approved

Inputs: Approved [Claude Code Adapter 1.4.0 Specification](../../specs/claude-code-adapter-1.4.0.md)、同步前的 Approved [Project Knowledge Base](../knowledge-base.md)、Approved [Claude Code Adapter 1.4.0 Requirement Decision Record](../../requirements/claude-code-adapter-1.4.0.md)，以及 Specification 於 2026-09-04 採用並標示版本限制的 Anthropic 官方 Plugin、Marketplace、Skills、Hooks、Subagents 與 CLI contracts。

Assumptions: 本摘要只提議同步 Approved Specification 新增或定稿的 durable technical knowledge，不宣稱 implementation、exact Claude Code `2.1.251` compatibility、live smoke、本機 `1.4.0` candidate 或任何 external publication 已完成。

Deferred: Ticket Plan、implementation、真實 Claude Code `2.1.251` compatibility fixture、實際 `UserPromptExpansion.command_name`、首個 live-smoke environment、Completed `1.4.0` evidence，以及所有 tag／push／Release／Marketplace activation／announcement actions。

Handoff: 以下明示變更已同步至正式 Project Knowledge Base，並交由 `$plan-tickets`；本摘要的核准不授權 implementation。

Approval: 使用者於 2026-09-04 在本摘要的完整精確內容展示後明確回覆「核准」；該核准只涵蓋本摘要明示的 Knowledge Base changes，不授權 implementation。

## Additions

### Glossary

- 新增 **Route envelope**：由 target public command 的 `UserPromptExpansion` handler 產生、與 Skill prompt 同次送入 Claude 的 bounded、schema-versioned routing result。它只可含 plugin/version、entry、operation ID、classification、selected profile、routing status 與固定 disclosure code，不含 prompt、arguments、path、raw session ID 或其他 hook input。
- 新增 **Routing status**：每個 session routing state 的 `ready`、`pending` 或 `indeterminate` 狀態。只有 schema-valid、same-session `ready` state 可建立 automatic operation；其他狀態 fail closed。
- 新增 **Post-switch race window**：Claude Code 可能在 `PostModelSwitch` 完成前先送出下一個 request，且 automatic fallback／resume restore 沒有 `PreModelSwitch`。因此 commit 前的第一個 invocation 只能 best effort；commit 後的下一個 permitted public entry 才有新 classification 保證。

### Architecture map

- Approved target router hooks 固定為 `SessionStart`、`PreModelSwitch`、`PostModelSwitch` 與 `UserPromptExpansion`，全部使用 synchronous command hook 與 dependency-free Node router；不使用 `CLAUDE_ENV_FILE` 作跨平台 session selector。
- 每個 hook 從自己的 structured stdin 取得 `session_id`，立即 SHA-256 成 session key，只讀寫 `${CLAUDE_PLUGIN_DATA}/routing/v1/sessions/<session-key>.json`；raw session ID 不進 path、state、log 或 model-visible output。
- `UserPromptExpansion` 在 target Plugin Skill 展開前驗證 plugin command identity、讀取 same-session state、建立 operation，並以 `additionalContext` 提供 route envelope。兩個 Skill bodies 保持 profile-neutral，只接受同次 valid envelope。
- Routing state 使用 atomic replacement、monotonic model generation、`ready`／`pending`／`indeterminate` 狀態及 closed failure-code enum；handler 已啟動後的預期 failure 以 exit `0` 產生 failure envelope，不用 exit `2` 阻止 Skill body載入。

### Important decisions

- Plugin 恰有兩個 public Skill components；兩個 namespaced forms 是 canonical、documented、supported entries。Claude Code 可能提供 bare aliases，但它們是 host behavior，不承諾存在或不存在，也不算第三個 Plugin component。
- 同 session 前一個 Skill 的文字可能留在 conversation。最新 public entry／operation 的 bound profile 明確取代舊 profile authority；general→Claude 5 與 Claude 5→general 都需 behavior tests，無法證明時要求 `/clear` 或 new session。
- `PreModelSwitch` 可 best effort 寫入 `pending`，但任何寫入失敗都不得 deny、delay 或改寫使用者切換模型。`PostModelSwitch` 提交 authoritative `to_model`；提交失敗只警告並使後續 routing fail closed，不鎖定 active model。
- Model switch 後不得宣稱實際第一個 invocation 必然使用新 profile；正式保證是 Post hook commit 後的下一個 permitted public entry。當前 operation 仍維持原 bound profile。
- Explicit `-5` 的 Node fallback 有兩條且只有兩條：valid `node-too-old` failure envelope，或 envelope 缺失但另行證明 Claude Code `2.1.251+` 且 Node missing。其他 failure、Node `22+` 下的缺失或 version 無法證明都停止。
- Reviewer agent 不宣稱可強制 foreground。Claude Code 可依 host/session mode 在 foreground 或 background 執行，但主 Claude 必須等待 reviewer 結果後才可整合 findings 或完成 Full Review。
- `UserPromptExpansion` 有現行官方契約，但官方文件沒有標示 introduced version。Exact Claude Code `2.1.251` binary 必須通過 strict validation、兩個 target namespaced invocations、route additional context 與 Node/failure semantics fixtures；否則返回 Requirement／Specification revision，不得靜默提高 minimum 或完成 release。

### External dependencies

- 新增 2026-09-04 採用的精確官方 contract entry points：Claude Code [Plugins reference](https://code.claude.com/docs/en/plugins-reference)、[Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)、[Skills](https://code.claude.com/docs/en/skills)、[Hooks reference](https://code.claude.com/docs/en/hooks)、[Subagents](https://code.claude.com/docs/en/sub-agents)與[CLI reference](https://code.claude.com/docs/en/cli-reference)。
- 新增 exact Claude Code `2.1.251` executable，作為 `UserPromptExpansion` availability、namespaced `command_name`、strict validation 與 failure semantics 的 release-blocking validation dependency。

### Unresolved items

- Exact Claude Code `2.1.251` 是否接受並執行 `UserPromptExpansion`，目前只有 current-doc contract，尚無 real-binary evidence。
- Namespaced Plugin Skill invocation 在 target binary 提供的精確 `UserPromptExpansion.command_name` 值，必須實測後固定 matcher 與 fixtures。
- 真實環境是否觀察到 PostModelSwitch commit 前 race window，以及確切環境與結果，必須由 release evidence 記錄。

### Artifact links

- 新增 Approved Specification：[Claude Code Adapter 1.4.0](../../specs/claude-code-adapter-1.4.0.md)。
- 新增本 Approved Knowledge Base Change Summary：[Claude Code Adapter 1.4.0 Specification KB Change Summary](claude-code-adapter-spec-kb-change-summary.md)。

## Modifications

### Envelope

- `Inputs` 加入 Approved `claude-code-adapter-1-4-0-spec`。
- `Deferred` 移除已完成的 Specification authoring／approval，保留 Ticket Plan、implementation、evidence、external publication 與其他 future scope。
- `Handoff` 改為本摘要核准及同步後交由 `$plan-tickets`；明確不授權 implementation。
- `Approval` 在同步時追加使用者對本摘要精確內容的核准證據。

### Architecture map

- 將 Claude runtime state bullet 補充為 hook-derived SHA-256 session key、固定 state boundary、atomic state 與 raw-session-ID prohibition。
- 將 JavaScript router bullet 從只描述 `SessionStart.model`／`PostModelSwitch.to_model`，擴充為四個 hooks、route envelope、state statuses、generation 與 best-effort race boundary。
- 將 `tests/release/` bullet 補充 exact `2.1.251` compatibility、command identity、failure-envelope、profile-authority 與 PostModelSwitch race tests。

### Important decisions

- 將「下一次公開 command 重新路由」細化為「Post hook commit 後的下一個 permitted public entry」，並加入 commit 前 race window 的 best-effort disclosure。
- 將 reviewer decision 補充為 foreground／background 由 host決定，但完成 Full Review前必須等待結果。
- 將兩個公開入口 decision 補充為兩個 public Skill components 與 canonical namespaced forms；不對 host bare aliases 作存在性承諾。

### Unresolved items

- 將原本「Plugin manifest、Marketplace、hooks、agent、router state 與 release inventory 的精確 Specification／implementation 形式仍待定稿」改為「Specification 已定稿；implementation及real-binary validation仍待完成」，並保留上述三個明確未驗證事項。

### Artifact links

- 將 `1.4.0 Specification: pending authoring and approval` 改為 Approved Specification 的 Markdown link。
- `1.4.0 Ticket Plan` 維持 pending Approved knowledge sync／Ticket Planning。

## Removals

- 從正式 Knowledge Base 的 `Deferred` 移除 `1.4.0 Specification`。
- 移除任何「Specification 尚待撰寫、定稿或核准」的過時敘述；不移除 implementation、validation、evidence 或 external-publication deferrals。
