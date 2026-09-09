# Ask Then Do It 1.4.0 Claude Code Adapter Specification

Artifact type: Specification

Artifact ID: `claude-code-adapter-1-4-0-spec`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Target release version: `1.4.0`

Status: Approved

Inputs: Approved [Ask Then Do It 1.4.0 Claude Code Adapter Requirement Decision Record](../requirements/claude-code-adapter-1.4.0.md)、Approved [Project Knowledge Base](../project/knowledge-base.md)、Completed local [Ask Then Do It release 1.3.1 evidence](../evidence/ask-then-do-it-release-1.3.1.md)、目前 `1.3.1` Core／Codex／Generic／release contracts、Anthropic [Claude 5 context-engineering guidance](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)、2026-09-04 查核的官方 Claude Code Plugin、Marketplace、Skills、Hooks、CLI 與 platform contracts，以及 2026-09-06 [exact Claude Code 2.1.251 native preflight blocker evidence](../evidence/claude-code-adapter-1.4.0-ticket-3-preflight-blocker.md)。

Assumptions: Completed local `1.3.1` candidate 是 implementation baseline；不假設 external `v1.3.1` 或 `v1.4.0` 已發布。`Core version: 1.3.1` 表示本規格採用的既有行為基準；target product 的 current Core 與 adapters identity 將一同升至 `1.4.0`。2026-09-06 已取得並隔離執行由官方 manifest 與有效 Anthropic Authenticode 簽章支持的 exact Claude Code `2.1.251` Windows x64 binary；首次preflight接受canonical Plugin，但因Marketplace當時缺少top-level `description`而拒絕repository Marketplace。該欄位修正後，canonical Plugin、repository Marketplace與test-only compatibility Plugin的strict validation均已exit `0`且無warning。現行官方文件有 `UserPromptExpansion` 契約，但未標明首次支援版本；剩餘 exact Claude Code `2.1.251` compatibility 仍必須由真實 binary 證明，否則回到 Requirement／Specification gate，不得靜默提高最低版本或宣告完成。

Deferred: Ticket 垂直切分、依賴順序與逐 Ticket 測試選擇；不影響本規格可觀察結果的內部函式切分與錯誤文字；實作；實際首個 live-smoke OS／surface／model；Anthropic Community Marketplace；Claude Code `project`／`local`／`managed` Plugin scopes；Claude Desktop 與 web/cloud sessions；其他 AI Agent adapters；通用 Adapter Registry／跨 host installer；Git tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement。

Handoff: Marketplace top-level `description` correction與Ticket 1重新Review均已完成。使用者於2026-09-07核准調整implementation sequencing：Ticket 3保持`unverified`並保留為local `1.4.0`完成前的hard gate，但不再阻止Ticket 2、General profile或Claude 5 profile的provisional implementation。現在交給Ticket 2；所有尚未由exact host證明的command identity、hook與failure semantics只能標為provisional／simulated，日後Ticket 3若觀察不一致，必須返回最早受影響的Requirement／Specification／Ticket修正與重驗。

Approval: 使用者於2026-09-04在完整修正版Specification、行為摘要、驗證結果與remaining hard gates展示後明確回覆「核准」，核准當時文件的精確內容。2026-09-06 exact-host observation揭露其中一項Marketplace field inventory矛盾；使用者在完整Draft correction結果、最小修正內容、Knowledge Base Change Summary與preflight evidence展示後明確回覆「核准」，核准加入exact top-level `description`並同步明示Knowledge Base變更。使用者於2026-09-07另明確核准只調整implementation sequencing：允許Ticket 2與profiles先provisional implementation，Ticket 3仍為local `1.4.0` completion hard gate且不降低任何acceptance criterion。這些核准均不授權external publication。

## 問題

Ask Then Do It `1.3.1` 已有 provider-neutral Core、Codex Plugin、Generic prompts 與 deterministic release，但 Claude Code 使用者沒有 host-native Plugin。直接複製 Codex Skills 既不能證明 Claude Code 的命名、Marketplace、hook、model-switch、session state 與 reviewer lifecycle，也不能證明 Claude 5 精簡 instructions 與 general instructions 維持相同行為。

`1.4.0` 必須新增一個可持久安裝、可更新、可復原且可驗證的 Claude Code Adapter，同時解決兩個互相制約的目標：general 與 Claude 5 profiles 都完整遵守 Core；Claude 5 profile 又必須在每個固定測量情境顯著減少 Plugin-owned loaded context。任何 context 優化都不能弱化核准、安全、證據、artifact 或失敗邊界。

## 目標

- 以官方 Claude Code Plugin 與 repository-hosted Marketplace 提供 `user`-scope persistent installation。
- 在同一 Plugin 中只提供兩個 public Skill components，並以兩個 namespaced forms 作為 canonical、documented、supported entries。
- 以可信、session-isolated 的官方 hook signals 做 best-effort model classification，不切換、pin 或 override active model。
- 保持 Full／Lite、requirement、knowledge、Specification、Ticket、TDD/direct、Review 與 architecture contracts 的 observable semantics。
- 讓兩個 profiles 各自通過全部 30 條 Core `1.3.1` mandatory rules 及本規格的 host-specific scenarios。
- 在行為 gate 通過後，使 Claude 5 profile 在每個固定 context scenario/checkpoint 的 deterministic proxy 至少減少 50%。
- 把 Claude 納入三語文件、三-family deterministic packaging、checksums、release evidence 與歷史保護。
- 至少在一個乾淨真實 Claude Code environment 完成 end-to-end smoke，再允許宣告本機 `1.4.0` candidate 完成。

## 非目標

- 不在 `1.4.0` 新增 Gemini CLI、GitHub Copilot 或其他 Agent adapters，也不建立 universal installer／Adapter Registry。
- 不改變 Full／Lite 或 30 條 mandatory Core rules 的語意。
- 不公開 requirements、documented requirements、Specification、Ticket Planning、TDD/direct implementation、Review 或 architecture 的額外 commands。
- 不支援 Claude Code `project`、`local` 或 `managed` Plugin installation/update/removal lifecycle。
- 不提供 `~/.claude/skills` personal-Skill fallback 或 ZIP-backed persistent local Marketplace。
- 不支援 Claude Desktop、Claude Code web/cloud；Remote Control 不是獨立受支援 surface。
- 不要求 Windows／macOS／Linux × CLI／VS Code／JetBrains 九組全部 live-tested。
- 不切換 Claude model，不以 Skill `model` frontmatter 選擇另一個模型，也不承諾 future model 自動相容。
- 不新增自訂 `/doctor`、Skill 自動轉換、`/code-review ultra` contract 或 `skill-creator` dependency。
- 不保證 Claude 總 context、API billing tokens、prompt-cache cost、latency 或金額下降 50%。
- 不在本 workflow 執行任何 external publication mutation。

## 名詞與版本邊界

- **General profile**：供 classifier 明確認定為受支援非 Claude 5 model，以及 automatic entry 的 valid unknown-model compatibility mode 使用。
- **Claude 5-optimized profile**：與 general profile 保有相同 mandatory outcomes，但使用較短 bootstrap、按需 stage modules 與 progressive disclosure。
- **Automatic entry**：`/ask-then-do-it:ask-then-do-it`，依可信 model state 選擇 profile。
- **Explicit Claude 5 entry**：`/ask-then-do-it:ask-then-do-it-5`。使用者叫用這個 command 本身就是對 Claude 5 profile 的明確選擇，不需再做第二次確認；它仍不得切換 active model。
- **Operation-bound profile**：public command 開始 operation 時綁定一次的 profile。下一次 public command 之前，不因 model switch 混用 instructions。
- **Valid unknown model**：router、Node、session ownership 與 state schema 都正常，但官方 event 沒有 model，或 canonical model ID 不在 release-owned mapping 中。
- **Router failure**：Node／router 無法執行、session key 缺失、state 不可安全解析、schema 不相容或 ownership 無法證明；它不是 unknown model。
- **Compatibility target**：由設計、automated tests 與官方 feature evidence 支持的 OS／surface；不代表 live-verified。
- **Live-verified environment**：release evidence 實際記錄並通過真實 Claude Code smoke 的 exact environment。
- **Loaded-context proxy**：按本規格固定 normalization 計算、repository 可控制且實際送入模型 context 的 Plugin text；不是 Anthropic 計費值。
- **Qualified Plugin identity**：`ask-then-do-it@ask-then-do-it`，前者是 Plugin name，後者是 Marketplace name。

三個獨立的最低版本契約為：Claude model `4.6+`、Claude Code `2.1.251+`、automatic router 的 Node.js `22+`。Claude Code 或 model 已知低於最低版本時停止；Node 不足只使 automatic routing 不受支援，因而不阻止 explicit Claude 5 manual path。

## 使用者與情境

### 第一次持久安裝

使用者在 supported Claude Code 上明確要求安裝。Guidance 先唯讀查核 Claude Code、Node、Marketplace、qualified Plugin、scope、version 與 enabled state；狀態安全時加入 repository Marketplace 並安裝 `user`-scope Plugin。新 session 可發現恰好兩個 public Skill components，文件只把它們的 namespaced forms 列為 canonical entries。

### 自動選擇 profile

使用者執行 automatic entry。Known Claude 5 使用 optimized profile；known supported non-5 使用 general；valid unknown model 在揭露 compatibility mode 後使用 general；known unsupported 或 router failure 在 operation 開始前停止。

### 明確要求 Claude 5 profile

使用者執行 explicit entry。Known Claude 5 使用 optimized；known supported non-5 揭露不相容並改用 general；valid unknown 或 Node/router automatic-detection unavailable 時，揭露無法驗證後使用 optimized；known Claude `<4.6` 仍停止。

### Operation 中途切換 model

`PostModelSwitch` 更新同一 session 的可信 model state並在下一次可用 request 告知使用者。當前 operation 繼續原 profile；若切到 unsupported model，必須同時揭露目前 operation 已離開正式 model support，但仍不注入另一 profile。State完成commit後的下一個permitted public entry依新state重新判斷並在unsupported時停止；host造成的commit前race window依best-effort限制誠實揭露。

### Full Review

當 Agent tool 與 Plugin reviewer 都可用時，主 Claude 委派唯讀、獨立 context reviewer，整合經驗證的 findings。若 reviewer 不可用但 tools 可用，改做 same-context `non-independent` Review；若只有 conversation evidence，標示 `limited-evidence`，不得冒稱已讀 repository 或有獨立複查。

### Config 選擇 Full 或 Lite

使用者可在 Claude-specific user/project TOML 設 default。Explicit operation instruction 優先；present invalid project Config fail closed to Full 且不落到 user Config；所有解析唯讀，不修改 Claude `settings.json`、Codex Config 或任何 default。

### 更新、移除與 ZIP recovery

明確 update request 只修改 expected `user`-scope installation；來源、identity 或 scope 不安全時停止。明確 remove request 只移除 qualified Plugin；ZIP 則以 `claude --plugin-dir <extracted-plugin-path>` 啟動當次 session，不建立 persistent state。

### 維護者建立 release candidate

維護者建立 Codex、Generic、Claude 三個 expanded packages 與 ZIP、完整 checksums及 evidence。所有 automated gates 與至少一個 clean live smoke 通過後，才可宣告 local candidate；流程在 tag、push、Release、upload、activation 或 announcement 前停止。

## 必要行為

### 1. Authority、identity 與歷史邊界

Approved Requirement Decision Record 是本規格的 upstream product authority。本規格只能細化其行為與官方外部契約，不得放寬任何 route、scope、context、Review、platform、documentation 或 publication gate。

Target current declarations MUST 對 `1.4.0` lockstep：Core、Codex adapter、Generic adapter、Claude adapter、Claude Plugin manifest、Claude Marketplace entry、current docs、release config、expanded packages、ZIP names、checksums、conformance 與 new release evidence。Specification envelope 的 `Core version: 1.3.1` 是 authoring baseline，不得誤寫成 target runtime identity。

Completed `1.3.1` requirements、Specification、Ticket Plan、release/review/architecture evidence、其中保存的 source/artifact hashes 與 frozen historical references MUST byte-for-byte 不變。`dist/` 的 managed current outputs 可由 `1.4.0` candidate 依既有 transaction contract 取代，但不得把歷史 assets 描述成被重寫。

### 2. Claude catalog 與 Plugin manifest

Repository root MUST 有 `.claude-plugin/marketplace.json`。它 MUST 使用 Claude Marketplace schema，且 authored top-level fields 恰為：`name`、`description`、`owner`、`plugins`；`name` 是 `ask-then-do-it`，`description` MUST 與唯一 Plugin entry 的 approved independent-project description 完全一致，`owner.name` 是 `Ian Wu, Handle by me Tech Studio`，`owner.url` 指向本 repository，`plugins` 恰有一個 Ask Then Do It entry。

該 entry MUST 使用：

- `name: ask-then-do-it`、`displayName: Ask Then Do It`、`version: 1.4.0`；
- 與現有產品一致的 independent-project description、author、repository、homepage、MIT license、Developer Tools category 與 discovery tags；
- `strict: true` 與 `defaultEnabled: true`；
- `git-subdir` source，URL 是 `https://github.com/Mysterio1001/Ask-Then-Do-It.git`，path 是 `adapters/claude-code/plugin/ask-then-do-it`，ref 是 `v1.4.0`；
- 不含 Codex-only `policy`、Codex `interface` 或指向 Codex source 的欄位。

Canonical Plugin manifest MUST 位於 `adapters/claude-code/plugin/ask-then-do-it/.claude-plugin/plugin.json`，authored fields 恰為：`name`、`displayName`、`version`、`description`、`author`、`homepage`、`repository`、`license`、`keywords`、`defaultEnabled`。Name、display name、version、author、repository、license、description 與 catalog MUST 一致；`defaultEnabled` MUST 是 `true`。

Plugin MUST 使用官方 default component directories，因此 manifest MUST NOT 重複宣告 `skills`、`commands`、`agents` 或 `hooks` path。Plugin MUST NOT 包含 MCP、LSP、monitor、theme、channel、userConfig、runtime dependency 或 unknown manifest fields。Plugin 與 repository Marketplace root 分別執行 `claude plugin validate <path> --strict` MUST exit `0` 且沒有 warning；baseline 不得依賴只在 Claude Code `2.1.259+` 才有的 `--json`。

Claude catalog/schema/validator/source MUST 與 `.agents/plugins/marketplace.json` 的 Codex catalog 分離。兩個 catalogs 都 MUST 留在 repository、都 MUST 排除於 consumer packages/ZIP，且任何 validation MUST 拒絕互指 source 或混用 provider-only fields。

### 3. Public Skills、profiles 與 internal modules

Plugin MUST 恰好包含兩個 public Skill components：

1. `skills/ask-then-do-it/SKILL.md` → `/ask-then-do-it:ask-then-do-it`。
2. `skills/ask-then-do-it-5/SKILL.md` → `/ask-then-do-it:ask-then-do-it-5`。

兩個 Skill frontmatters MUST 明確使用各自的 `name`、精確 description、`disable-model-invocation: true`、`user-invocable: true`、`model: inherit` 與三項 version requirements 的 `compatibility`；MUST NOT 指定另一 model、effort、forked context、background execution、broad pre-approved tools 或 dynamic shell injection。User MUST 能透過 namespaced command 明確啟動，Claude MUST NOT 自行選擇何時啟動這個 gated workflow。Claude Code MAY 在沒有名稱衝突時另顯示 host-provided bare alias；該 alias 不是第三個 Plugin component，且本產品不把它列為 supported entry、也不保證它存在或不存在。

兩個 Skill bodies MUST只是profile-neutral bootstrap，且只接受同一次`UserPromptExpansion`提供的bounded、schema-valid route envelope；不得自己接收或轉送raw session ID，也不得以dynamic shell injection或另一個model判斷profile。Envelope只能含plugin/version、entry、operation ID、classification、selected profile、routing status與固定disclosure code；不得含prompt、arguments、paths或raw hook input。

Automatic entry MUST先取得schema-valid deterministic route envelope，再只載入所選profile的orchestration與需要的stage modules；envelope缺失、重複、invalid或failure時停止。Explicit entry在valid success envelope可用時依route result執行；valid `node-too-old` failure envelope MAY依manual-path contract揭露限制並載入optimized profile。Envelope缺失時，bootstrap MUST以可用host commands分別證明Claude Code `2.1.251+`且Node確實missing，才能使用相同manual path。Node `22+`卻沒有envelope、任一version無法證明或Claude Code低於minimum時都停止；不得把handler crash、state failure或hook misconfiguration猜成允許manual fallback，也不得把manual path稱為已驗證Claude 5或完整automatic-routing support。

Internal stage modules MUST 位於 `profiles/general/` 或 `profiles/claude-5/`，每個 profile 恰有以下十個檔案：`orchestration.md`、`lite-workflow.md`、`requirements.md`、`documented-requirements.md`、`specification.md`、`ticket-planning.md`、`tdd-implementation.md`、`direct-implementation.md`、`review.md`、`architecture-improvement.md`。它們不得位於 `skills/` 或 `commands/`，不得成為第三個 public command。

General MAY 使用較完整說明。Claude 5 profile MAY 合併重複敘述、使用短引用與 progressive disclosure，但每個 mandatory rule、gate、failure outcome、artifact state、authority boundary 與 evidence requirement MUST 有可追溯且可執行的映射。一次 operation 不得新載入另一 profile 的 modules。因 Claude Code 會把先前已叫用 Skill 的文字保留在 conversation，最新 public entry 與其 bound profile MUST 明確取代先前 operation 的 profile authority；舊 profile 內容只可當歷史 context，不得再控制目前 operation。General→Claude 5 與 Claude 5→general 的同 session 連續 invocation 都 MUST 以 behavioral tests 證明此 precedence；若無法證明，profile 改變時 MUST 停止並要求 `/clear` 或 new session，而不得混用。

### 4. Model classification 與 entry routing

只有 `SessionStart.model` 與 `PostModelSwitch.to_model` 的 canonical model ID 可建立 trustworthy classification。`requested_model`、Skill `model` field、`ANTHROPIC_MODEL`、使用者文字、model 自我宣稱、substring guess 或 transcript content MUST NOT 作為 classification authority。

`config/model-classifications.json` MUST 是 release-owned、schema-versioned exact mapping。它 MUST 列出 implementation freeze 時由 Anthropic 官方文件支持的 canonical IDs，並將每個 ID 映射為 `claude-5`、`supported-non-5` 或 `unsupported`。沒有 exact mapping 的值一律為 `unknown`；不得用寬鬆 pattern 將 custom gateway 或 future model 猜成 Claude 5。Mapping、來源日期與 fixtures MUST 納入 release evidence；更新 mapping 是 future release change。

在 Claude Code `2.1.251+`、Node `22+` 且 router/state trustworthy 時，routing MUST 為：

| Model classification | Automatic entry | Explicit Claude 5 entry |
| --- | --- | --- |
| `claude-5` | 綁定 Claude 5-optimized | 綁定 Claude 5-optimized |
| `supported-non-5` | 綁定 general | 揭露不相容後綁定 general |
| `unsupported` | 停止並要求 Claude `4.6+` | 停止並要求 Claude `4.6+` |
| `unknown` | 揭露 compatibility mode 後綁定 general | 將 command invocation 視為明確選擇；揭露無法驗證後綁定 Claude 5-optimized |

Claude Code `<2.1.251` 時兩個 entries 都 MUST 停止。Node missing／`<22` 時 automatic entry MUST 停止；explicit entry只有在另行證明Claude Code version受支援後才 MAY走manual optimized path，且 MUST揭露model無法驗證、automatic routing unavailable、正式完整支援前仍需升級Node。Router executable/hook unavailable MUST使automatic entry停止；schema、state transition或ownership failure則使兩個entries都停止。只有valid、`ready` state的omitted/unmapped canonical model才是`unknown`。

任何 route outcome MUST 保留 active model。Skills、hooks、router、profiles、reviewer 與 docs MUST NOT pin、switch、override 或暗示已切換 model。

### 5. Session lifecycle 與 operation binding

Router MUST 是 Node.js `22+` 執行、零第三方 runtime packages 的 `scripts/router.mjs`。Plugin hooks MUST 位於 `hooks/hooks.json`，只註冊 `SessionStart`、`PreModelSwitch`、`PostModelSwitch` 與 `UserPromptExpansion`，並以官方 exec form 呼叫 `node`，將 script path 與 action各自放在 argument vector；不得使用 shell concatenation，且所有 handlers 都不得設為 async。

每個 router hook action MUST 從自己的 structured stdin 取得 `session_id`，驗證後以 SHA-256 轉成 64 位 lowercase hexadecimal session key，且只讀寫該 key 精確對應的 state file。Raw `session_id` MUST NOT 成為 path segment、持久 state field或model-visible output；router MUST NOT 依賴 `CLAUDE_ENV_FILE`、process-global「current session」或掃描「最新」state。`UserPromptExpansion` 還 MUST 驗證 `expansion_type: slash_command`、`command_source: plugin` 與兩個 target Skill 的實測精確 `command_name`，不得持久化或回顯 `prompt`、`command_args` 或其他 untrusted input。

Startup、fork 或 clear 沒有可延續 operation 時，SessionStart hook MUST 保持 model-context output 為空。Resume 或 compact 找到 non-null、same-session operation binding 時，hook MUST 只注入最小 additional context：operation ID、原 bound profile、需要重新載入的同-profile modules，以及「不得重新路由」的 conditional reminder；不得注入另一 profile。若無法證明 operation 仍進行中，文字 MUST 說明這只是 last binding，並等待 workflow artifact／conversation evidence或下一次public entry決定是否延續。

`UserPromptExpansion` router action只可在 schema-valid、same-session、`ready` state 下為 target command 建立新的 operation ID、保存 selected entry/profile/bound classification，並輸出 bounded、schema-versioned route envelope作為 `additionalContext`。Handler一旦啟動，所有supported route outcomes以及Node `<22`、schema、ownership、transition、`pending`、`indeterminate`與internal-error outcomes都 MUST被catch並以exit `0`輸出恰一個schema-valid envelope；failure envelope使用closed failure-code enum、不建立operation且不含untrusted原文。Router MUST NOT以exit `2`表示一般routing failure，因為該exit會阻止Skill展開。Automatic Skill body遇failure或缺失envelope都停止。Explicit `-5`只有valid `node-too-old` failure envelope，或envelope缺失且Claude Code version受支援、Node被獨立證明missing時，MAY走manual optimized path；其他valid failure envelope或Node `22+`下的缺失一律停止。

`PreModelSwitch` SHOULD在user/client-requested switch套用前，以atomic replacement把同session state標為`pending`並記錄generation；寫入失敗 MUST NOT阻止、延遲或改寫使用者的model switch，而應誠實顯示routing-state warning。Plugin不得用deny／ask決策鎖定model。`PostModelSwitch` MUST以自己的stdin session ID定位state，並嘗試以atomic replacement將authoritative `to_model` classification提交為`ready`。有對應Pre event的source必須匹配pending transition；沒有Pre event的`auto`／`resume`source則建立下一generation。需要匹配卻不成立且state可寫時 MUST改標`indeterminate`，不得保留舊classification作fallback。它 MUST保留operation binding，且下一-request context MUST指示主 Claude告知使用者「本operation profile不變；model state完成同步後的下一個permitted public entry才重新路由」。如果新model已知unsupported，還 MUST揭露當前operation已離開formal model support；若Post commit失敗，則顯示routing-state warning但仍不得切回、鎖定或改寫active model。

Claude Code允許`PostModelSwitch`在下一個request之後才完成，且automatic fallback／resume restore沒有`PreModelSwitch`。因此automatic change尚未開始寫state時，router無法區分「未切換」與「已切換但Post hook尚未commit」；best-effort automatic entry MAY在這個race window使用最後一個`ready` classification。Post hook完成後，當前operation仍維持其bound profile，下一個permitted public entry MUST使用新classification。Evidence MUST把這項host limitation與任何race observation明確列為best-effort，不得宣稱model change後實際第一個invocation必然重新路由。

SessionStart lifecycle MUST 為：

- `startup`：建立／重設該 session state，operation 為空；model omitted 時是 valid unknown。
- `resume`：只可沿用相同 session key、schema-valid operation binding；event model若存在則更新，若省略則先把classification設為`unknown`，不得以resume前classification冒充current model；後續valid `PostModelSwitch` resume event可再提交authoritative classification。
- `fork`：以新 session key 建立獨立 state，operation 為空，不複製 parent state；model omitted 時為 unknown。
- `clear`：即使 host 重用 session ID，也 MUST 清除 operation binding；model omitted 時 classification 重設為 unknown，不沿用 clear 前 model。
- `compact`：相同 session 可保留 operation binding；event model 存在時更新，省略時只沿用同 session 的 trustworthy classification。

下一次 public entry MUST overwrite prior operation binding。沒有可靠 host signal 可證明多回合 operation 已自然結束時，state MAY 保留 last binding，但 switch notice MUST 使用「若該 operation 仍進行中」的誠實措辭，不得把舊 binding 當成另一 session 的 authority。

### 6. Capability 與 Review

兩個 profiles 在每次 operation 開始時 MUST 宣告實際可證明的最強 capability：`conversation`、`tools` 或 `multi_agent`。Static Claude conformance MAY 宣告三者，但 runtime tool availability與permission才是當次 authority。

Plugin MUST 提供 `agents/ask-then-do-it-reviewer.md`。Agent frontmatter MUST 使用 stable name、清楚 description、`model: inherit`，不強制 background，並把可用工具限制為 `Read`、`Grep`、`Glob`；不得有 Write、Edit、shell、network、MCP、memory、worktree isolation或其他 side-effect surface。Claude Code MAY 依 host/session mode在foreground或background執行它，但主 Claude MUST 等待 reviewer完成並取得結果後才可整合findings或完成Full Review。Reviewer instructions MUST 檢查 Approved requirements、Specification、Ticket mode、diff、tests、raw evidence及十二個 Core Architecture and Refactoring Lenses。

Review behavior MUST 為：

- Agent tool 與 reviewer 可用：Full 使用 independent read-only reviewer context；主 Claude驗證、整合 findings，不盲從 reviewer output。
- Tools 可用但 reviewer／Agent 不可用：Full 仍 Review，但明確標示 `non-independent` 與 unavailable independent evidence。
- 只有 conversation／user excerpts：只能做 `limited-evidence` Review，列出未讀 repository、未執行 tests 與 handoff；不得宣稱完成 repository Review。
- Lite：始終使用既有 same-context compact Review 與 findings correction approval；不得因 Plugin 含 reviewer 而升級為 Full 或 independent Review。

Reviewer unavailable 本身不阻擋完成；其他 Core validation、finding、approval 與 disclosure gates 仍決定是否可完成。

### 7. Full／Lite 與 Claude Config

General 與 Claude 5 profiles MUST 各自映射 [Core mandatory rules](../../core/rules/rules.yaml) 的全部 30 個 IDs，沒有 profile-specific exemption。Mapping MUST 保留 capability honesty、mode resolution、Full lifecycle、Lite lifecycle、requirement/knowledge/spec/plan gates、TDD/direct distinction、Review evidence/lenses、artifact states、architecture diagnosis/deletion/reflow及 explicit routing rules。

Full MUST 保留 Requirement Decision Record、documented Knowledge Base sync、Specification、Ticket Plan、逐 Ticket plain-language test choice、Approved `tdd`／`direct` implementation evidence、Review 與 architecture contract。Lite MUST 保留 blocking questions、single Change Brief gate、no workflow artifacts、no new tests、proportionate validation、same-context compact Review、correction approval、session non-persistence與 honest completion。

Claude mode Config paths MUST 為：

- user default：`~/.claude/ask-then-do-it.toml`；
- project override：`<project>/.claude/ask-then-do-it.toml`，且必須位於 active project root。

唯一 recognized value 是 top-level `mode = "full"` 或 `mode = "lite"`。Aliases、不同大小寫、unquoted value、nested value、missing/duplicate mode、malformed TOML 或 unsupported value 都不是有效 mode。

每次 operation MUST 使用以下 precedence：valid explicit current-operation instruction、project Config、user Config、Full fallback。Conflicting explicit Full/Lite MUST 暫停並問一次。Valid explicit instruction MUST 不讀 lower sources。Project Config absent 才讀 user Config；present unreadable/malformed/missing-mode/unsupported project Config MUST fail closed to Full 且不讀 user Config。User Config同理，absent 才 Full fallback。

Config resolution MUST 完全唯讀；不得建立、修復、正規化、持久化 override 或寫入 `settings.json`。Claude MUST 不讀 Codex Config；Codex MUST 不讀 Claude Config。

### 8. Marketplace lifecycle 與 authorization

Status／version-check request MUST 完全唯讀，並分別回報：Claude Code version、Node availability/version、Marketplace name/source/scope、qualified Plugin identity、install scope、installed version、enabled state，以及 automatic／explicit entry availability。檢查可使用官方 `claude plugin marketplace list --json`、`claude plugin list --json --available` 與 `claude plugin details`；不得藉 status 執行 marketplace update、install、enable、disable、remove或 Config write。

正式 persistent source MUST 是 user-scoped repository Marketplace。Marketplace source command MUST 使用 `Mysterio1001/Ask-Then-Do-It`，Plugin identity MUST 使用 `ask-then-do-it@ask-then-do-it`。凡官方 CLI syntax支援scope的Marketplace／Plugin mutation，MUST明確使用`--scope user`；`list`、`details`、Marketplace refresh等不接受scope的commands不得硬加該flag，而必須從輸出與前後state verification證明操作對象。所有writes前 MUST重查上述state。

Lifecycle matrix MUST 為：

- Marketplace absent、Plugin absent、state unambiguous：明確 install request 可先 `claude plugin marketplace add Mysterio1001/Ask-Then-Do-It --scope user`，再 install qualified Plugin at user scope。
- Expected Marketplace present、Plugin absent：明確 install只安裝 Plugin，不重加 Marketplace。
- Expected current Plugin installed and enabled：install/update 都回報 no-op，不重裝、不刷新無關 state。
- Expected current Plugin installed but disabled：install/update 都維持使用者 disabled choice並回報 no-op；不得偷偷 enable。Guidance MAY 顯示官方 `claude plugin enable ask-then-do-it@ask-then-do-it --scope user` 作為另一次使用者主動動作，但本版 AI-assisted lifecycle 不代為執行 enable。
- Expected older Plugin：明確 update 可 refresh expected Marketplace，再 update qualified user-scope Plugin；原本 disabled 的 explicit setting MUST 保持 disabled。
- Installed version newer than target：停止並回報，不 downgrade。
- Node missing／`<22`：若其他 state 安全，明確 install/update MAY 完成 Plugin lifecycle供 explicit manual path 使用，但完成報告 MUST 說 automatic entry unavailable；不得稱完整 automatic-routing support。
- Any same-name other Marketplace、source mismatch、same Plugin at `project`／`local`／`managed` scope、multi-scope ambiguity、unreadable/invalid state或 unsupported Claude Code：停止且不寫入，不 remove-first、不猜 alternate source。
- Command partial failure：停止後唯讀重查可觀察 state，完整回報成功及失敗部分；不得用 destructive rollback掩蓋結果。

明確 remove request只可執行 `claude plugin uninstall ask-then-do-it@ask-then-do-it --scope user`。它 MUST 不移除 Marketplace、不刪兩個 Ask Then Do It Config、不修改其他 scopes。若為最後 scope，執行前 MUST 告知 `${CLAUDE_PLUGIN_DATA}` 只含可重建 routing state且 Claude Code預設刪除；使用者明確要求保留時才加 `--keep-data`。完整 purge需要新的明確 scope，不屬於 normal remove。

Install/update完成後 MUST 要求 `/reload-plugins` 或 new session依官方 lifecycle載入新 bytes；不得宣稱舊 session 的 Skills、hooks或state已自動換版。產品不得啟用 Claude Code background auto-update；host既有設定必須被描述成 host行為。

### 9. Router state、資料與安全

Immutable Plugin resources MUST 只從 `${CLAUDE_PLUGIN_ROOT}` 讀；runtime MUST 不寫 cached Plugin directory。Persistent state MUST 只位於 `${CLAUDE_PLUGIN_DATA}/routing/v1/sessions/<session-key>.json`。

State authored keys MUST 恰為：

- `schema_version`，值為 `1`；
- `session_key`，與 filename 相同的 64 位 lowercase SHA-256 hex；
- `session_source`，最後處理的 supported SessionStart source；
- `routing_status`，`ready`、`pending` 或 `indeterminate`；
- `model_generation`，從 `0` 開始且只能由有效 lifecycle transition 單調增加的整數；
- `model_id`，canonical ID 或 `null`；
- `model_classification`，`claude-5`、`supported-non-5`、`unsupported` 或 `unknown`；
- `model_observed_from`，`SessionStart`、`PostModelSwitch` 或 `null`；
- `pending_switch`，`null` 或只含 next generation、canonical `from_model`、supported switch source與started-at timestamp；
- `updated_at`，UTC timestamp；
- `operation`，`null` 或只含 random operation ID、public entry、bound profile、bound classification與started-at timestamp。

State MUST NOT 保存 raw session ID、prompt、arguments、task description、cwd/project/repository path、transcript、Requirement／Specification／Ticket content、diff、tool output、credential、secret、token、個資、billing/cost資料或telemetry。Router MUST 不新增network transmission。

Hook JSON、session ID、model ID、paths、Config與state全部視為 untrusted structured input。Script MUST 使用 argument-vector execution、fixed subdirectories、hash-derived filename、atomic same-directory replacement及 restrictive file handling；不得把 input 拼成 shell command、glob或可逃逸 `${CLAUDE_PLUGIN_DATA}` 的 path。

Invalid JSON、unknown keys、wrong type、unsupported schema、session-key/filename mismatch、unsafe symlink/path、impossible lifecycle transition、`pending`／`indeterminate` state或cross-session read MUST使automatic route fail closed。Model omitted/unmapped只有在state ownership/schema/lifecycle全都valid且routing state為`ready`時才成為`unknown`。

Session files last updated超過 30 days MAY 在成功的 SessionStart 後清理；current session file不得被清理。Time age本身不得讓 same-session `resume` 在 30-day boundary前失效。最後 scope uninstall依官方 lifecycle刪除 data；`--keep-data`保留時，下次使用仍須通過schema/ownership/lifecycle validation。

### 10. Package 與 deterministic release inventory

Canonical Claude source、expanded package `dist/claude/ask-then-do-it/` 與 ZIP root `ask-then-do-it/` MUST 有相同 runtime relative paths。Claude archive MUST 是 `dist/claude/ask-then-do-it-claude-1.4.0.zip`。

Claude expanded package與ZIP MUST 恰含下列 authored runtime/legal inventory，不得含 catalog、test fixture、source evidence、local state或machine path：

- `.claude-plugin/plugin.json`；
- `skills/ask-then-do-it/SKILL.md`；
- `skills/ask-then-do-it-5/SKILL.md`；
- `profiles/general/` 的十個固定 stage modules；
- `profiles/claude-5/` 的十個固定 stage modules；
- `agents/ask-then-do-it-reviewer.md`；
- `hooks/hooks.json`；
- `scripts/router.mjs`；
- `config/model-classifications.json`；
- `START-HERE.en.md`、`START-HERE.zh-TW.md`、`START-HERE.ja.md`；
- `LICENSE`、`THIRD_PARTY_NOTICES.md`。

Marketplace-installed runtime payload與Claude package runtime payload MUST 從同一 canonical source衍生並通過 relative-path/content equivalence；release builder依既有policy加入的兩個legal files必須可追溯。Expanded package與ZIP extraction MUST exact inventory and byte-equivalent。

`release/release.json` MUST 新增 Claude family、archive、source、inventory與Claude-required checks；`managed_outputs` MUST 是 `codex`、`generic`、`claude`、`checksums.sha256`。Release MUST 產生三個 expanded families、三個 archives與每個archive恰一筆SHA-256。Checksum ordering MUST deterministic且由release config package order固定。

現有complete staging validation、unmanaged collision protection、managed replacement、Windows `WinError 5` bounded retry、rollback、incomplete-recovery preservation、two-build byte reproducibility、deterministic ZIP metadata、ZIP equivalence、SHA-256、removed-artifact scan及evidence validation MUST 不退化。

Codex／Generic除current version、Claude cross-entry docs與三-family release coordination所需變更外，observable behavior、package relative inventory、runtime dependency boundary與provider config MUST 不變。Node.js MUST 只出現在Claude consumer prerequisites／package tests，不得成為Codex或Generic runtime dependency。

### 11. Conformance 與 fresh-session behavior evidence

Claude MUST 有獨立 `adapters/claude-code/conformance.yaml` 與 provider-specific validator/tests。Manifest MUST 使用 `adapter_id: claude-code`、`adapter_version: 1.4.0`、`target: claude-code-plugin`、`core_version: 1.4.0`，宣告 cumulative `conversation`、`tools`、`multi_agent`，為每個 capability提供非空evidence，並列出target Core全部30個mandatory rule IDs。

General與Claude 5 profiles MUST 各自對以下固定behavior scenario inventory取得100% pass；任何skip、partial或profile-specific exemption都算fail：

1. `CAP-CONVERSATION`：conversation-only claim與safe handoff。
2. `CAP-TOOLS`：repository persistence/commands只在tools可用時宣告。
3. `CAP-MULTI-AGENT`：independent reviewer與honest downgrade。
4. `MODE-EXPLICIT`：explicit Full/Lite及conflict pause。
5. `MODE-CONFIG`：project/user precedence、absent fallback與project-root boundary。
6. `MODE-INVALID`：present invalid fail closed且no persistence。
7. `FULL-REQUIREMENTS`：one-question requirement interrogation與RDR gate。
8. `FULL-KNOWLEDGE`：Draft notes、Approved evidence、完整KB change disclosure與joint approval。
9. `FULL-SPEC`：behavioral no-code Specification與approval gate。
10. `FULL-PLAN`：vertical Tickets、一次plain-language test-choice batch與plan gate。
11. `FULL-TDD`：Red-before-production、Green、Refactor、evidence與scope control。
12. `FULL-DIRECT`：no behavioral tests、non-test validation、skipped-test disclosure與evidence。
13. `FULL-REVIEW`：raw evidence、Ticket mode、12 lenses與findings severity。
14. `FULL-ARCH`：diagnostic-only、simulated deletion、report與spec reflow。
15. `LITE-QUESTIONS`：blocking-only question count/sentence/recommendation budgets。
16. `LITE-BRIEF`：single conversation-only Change Brief gate且no workflow artifacts。
17. `LITE-RISK`：before/during risk pause與operation-only mode switch。
18. `LITE-VALIDATION`：no new tests、diff/static/success/failure checks與unavailable evidence。
19. `LITE-REVIEW`：compact same-context Review與correction batch approval。
20. `LITE-SESSION`：completion budget、no durable/resumed Lite state。
21. `ROUTE-AUTO`：known 5、supported non-5、unsupported、unknown。
22. `ROUTE-EXPLICIT-5`：known 5、supported non-5、unsupported、unknown與Node unavailable。
23. `ROUTE-FAILURE`：old Claude Code、Node failure、router/state/ownership failure distinctions。
24. `ROUTE-SWITCH`：operation binding與next-invocation reroute。
25. `SESSION-LIFECYCLE`：startup/resume/fork/clear/compact與cross-session isolation。
26. `INSTALL-STATUS`：complete read-only state report。
27. `INSTALL-WRITES`：new/current/disabled/older/newer/source/scope/failure matrix。
28. `REMOVE-ZIP`：default/keep-data removal與session-only ZIP。
29. `DOCS-PACKAGE`：three-language ownership、two-command discovery與exact package inventory。
30. `RELEASE-INTEGRITY`：three families、history protection、local/external boundary與secret/path scan。

另 MUST 以相同 supported Claude model、effort、tools、repository fixture及isolated fresh transcript對兩 profiles 執行十二個 paired cases：requirements、documented requirements、Specification、Ticket Planning、TDD、direct、Full Review、architecture diagnosis、normal Lite、high-risk Lite、model routing/switch及safe lifecycle guidance。Harness MAY 直接選profile作test-only comparison，但不得新增consumer command或改active model。每一 case MUST 對預先固定的observable mandatory outcomes逐項pass；風格不同不算fail，缺gate、錯誤write、虛構evidence或失敗邊界不同都算fail。

Behavior/conformance gate MUST 先於context reduction。若任何profile behavior case fail，release blocked且不得計算context結果來抵銷。

### 12. Claude 5 loaded-context proxy

Context fixture MUST 固定十個 scenarios：documented requirements、Specification、Ticket Planning、TDD implementation、direct implementation、Full Review、architecture diagnosis、normal Lite、high-risk Lite及model-switch continuation。每個scenario都以automatic entry與deterministicroute fixture分別產生general/optimized path，並使用相同user task、capability與stage outcome。

每個scenario MUST 有 `stage-ready` checkpoint：route已完成且執行該stage所需Plugin instructions已載入，但尚未讀task-specific repository source或必要tool output。Full Review另有 `reviewer-ready` checkpoint：read-only reviewer agent prompt已載入且尚未加入task-specific diff/evidence。每個scenario的每個checkpoint都必須獨立達到至少50% reduction；不得以平均值、另一checkpoint或另一scenario補償。

Counted material MUST 包含每次實際載入／注入的：public Skill body、Skill listing text若host實際載入、selected profile orchestration/stage modules、router route-result text、hook additional context、Plugin reviewer description與完整agent prompt。相同Plugin text若在同一scenario重複注入，MUST按每次實際注入重複計數；reviewer context不得因位於另一model context而排除。

Excluded material MUST 只有：host system prompt、tool/MCP definitions、user task text、task-specific repository source/diff/artifacts、必要tool output、hidden reasoning與model output。Router/script/config source若只由machine執行且未送入model不計；它們的model-visible output仍計。

每個source先以UTF-8讀取並保存raw SHA-256；measurement依actual load order將每一source做Unicode NFC、把每段Unicode whitespace collapse成單一ASCII space、trim，再以一個LF串接。`normalized_bytes`是結果UTF-8 byte length；`proxy_tokens = ceil(normalized_bytes / 4)`；`reduction = (general - optimized) / general × 100`。Pass判定 MUST 使用整數關係 `optimized × 100 <= general × 50`，避免rounding改變結果。

Evidence MUST 保存fixture/version、scenario/checkpoint、profile、input hashes、source paths、load order、每個raw SHA-256、normalized bytes、proxy tokens、公式、兩個raw totals、reduction與pass/fail。Claude `/context`、`claude plugin details` projected token cost或observed usage MAY作diagnostic，但不得取代deterministic gate或支援billing/cost claim。

### 13. Documentation 與 localization

`README.md` MUST 保留現有English／繁中／日本語平行layout與每語言既有Introduction、Quick Start、Automatic installation (CLI)、nested Codex CLI、Manual installation、Read more相對順序。Claude內容只能插入對應位置；不得重構無關Codex／Generic內容。

三個root `START-HERE.*.md` MUST 加入Claude consumer choice。三個 `docs/guides/getting-started-simple.*.md` MUST 保持provider-neutral Full/Lite owner並加入Claude起始路徑。MUST 新增 `docs/guides/claude-code.en.md`、`.zh-TW.md`、`.ja.md`，完整擁有版本、user-scope lifecycle、兩entries、routing、Config、reviewer、platform、ZIP recovery及troubleshooting。

Claude Plugin/ZIP的三個START-HERE MUST簡短並連到same-version detailed guide，不複製完整workflow。Root、Codex、Generic、Claude各三個，共12個START-HERE pages MUST通過存在、relative links、brevity、version與packaged-copy tests。

三語內容 MUST semantic-equivalent，並清楚區分：Claude model／Claude Code／Node versions；known unsupported／valid unknown／router failure；automatic／explicit `-5`；compatibility target／live-verified；persistent Marketplace／session-only ZIP。Built-in `/doctor` 只能列為optional Claude Code installation/config health check，不得宣稱會轉換、最佳化或驗證Ask Then Do It Skills。

### 14. Platform compatibility 與 live smoke

Compatibility contract涵蓋Windows、macOS、Linux上的local Claude Code terminal CLI、VS Code extension與JetBrains plugin。Automated tests MUST覆蓋path separator/space、Node exec form、四種hook JSON/event sources、hook-derived session key、`ready`／`pending`／`indeterminate` transitions、atomic state、classification、cross-session isolation、failure behavior與package extraction。Official feature-availability evidence MUST證明每個surface支援本規格依賴的local Plugin、Skill、Agent與hooks；surface差異必須進docs/evidence。

這是compatibility target，不是九組live claim。Release evidence MUST列出每個真正live-verified的exact OS、surface、Claude Code version、Node version、active canonical model與日期；其他組合只能標compatibility target。

至少一個clean real Claude Code environment MUST 完成：

1. Isolated test source 的user-scoped Marketplace add、qualified install、status與enabled確認。
2. Plugin details與恰好兩個public Skill components discovery；兩個namespaced forms可用，internal stage modules不形成額外Skill components。Host-provided bare aliases只記錄observed狀態，不作存在或不存在保證。
3. 以該環境實際可用supported model驗證automatic與explicit route；拿不到的model branches不得冒充live。
4. 真實model switch、同operation profile stability、Post hook commit後的next-permitted-entry reroute，以及general→Claude 5與Claude 5→general連續invocation的authority precedence；若觀察到host race，evidence明確標示best-effort window。
5. 兩個同時／先後sessions不cross-contaminate，且至少驗證resume或compact lifecycle。
6. 從isolated、test-only、明確標示「非正式release」的older Claude candidate更新到exact `1.4.0` candidate；不得冒充`1.3.1`，因`1.3.1`沒有Claude Adapter。
7. Normal remove、default data deletion disclosure，以及reinstall或recovery。
8. Exact release ZIP透過`claude --plugin-dir <path>`啟動，兩commands可用，bare `claude plugin list`不被誤稱為persistent install。

完整route／failure matrix MUST另以deterministic injected `SessionStart`／`PreModelSwitch`／`PostModelSwitch`／`UserPromptExpansion` fixtures測試並標`simulated`。Exact Claude Code `2.1.251` binary MUST另證明strict validation接受`UserPromptExpansion`、兩個namespaced commands都觸發預期identity、`additionalContext`route envelope可見，以及Node unavailable／nonzero／exit 2／timeout的expansion結果；任一不符即停止並返回Requirement／Specification revision。External publication未獲准前，live smoke MAY用isolated local git/Marketplace fixture與candidate bytes，但 MUST明示GitHub public transport未驗證。沒有任何clean real Claude Code smoke時，local release completion MUST blocked。

### 15. Publication boundary

Local completion只包括source、packages、ZIP、checksums、automated/live validation、Review、architecture diagnosis與Completed release evidence。Evidence MUST逐項分開observed、simulated、unavailable與not authorized。

本Specification核准、Ticket/implementation、local smoke或candidate完成都不授權tag、push、GitHub Release、asset upload、public Marketplace activation、Community Marketplace submission或announcement。每個external mutation需要後續明確核准與執行結果。

## 邊界與失敗行為

- Known Claude `<4.6`與valid unknown MUST始終分開；unsupported不得降成compatibility mode。
- Node/router/state failure與valid unknown MUST始終分開；automatic route不得靠猜測繼續。
- Explicit `-5`的unknown/manual path必須揭露unverified，不得說「已偵測到Claude 5」。
- Model在operation中切換不重新載入profile；切到unsupported只改support disclosure與Post commit後下一個permitted entry的結果。
- `SessionStart` omitted model只有在hook/state ownership成功時才是unknown；hook根本沒跑不是unknown。
- `UserPromptExpansion`的session key、command identity或route envelope缺失／不一致時automatic route停止，不搜尋其他session；handler已啟動的所有failure都必須形成valid failure envelope。Explicit `-5`只有valid `node-too-old` failure，或Claude Code受支援、envelope缺失且Node確定missing時可走已揭露的manual path；其他failure、Node `22+`下的缺失、ownership或transition invalid都使兩entries停止。
- Config conflict／invalid依Core fail closed；不得讓model-profile routing取代Full/Lite routing。
- Reviewer只要有write/shell/network surface就不得算read-only independent evidence。
- Current version disabled不得因install/update被偷偷enabled；current enabled亦不得重裝。
- Same-name other source或unsupported scope不得因使用者說「更新」被remove/replaced。
- Marketplace/plugin command失敗不得留下虛構installed/current/enabled聲明；必須重查並報observed partial state。
- ZIP每個session都需`--plugin-dir`；不得寫`~/.claude/skills`或建立local Marketplace。
- 任一profile behavior fail或任一context checkpoint未達50%都block release。
- Live smoke缺失、official strict validation非零、package bytes不等、history改動或secret/machine-path leak都block release。
- External publication狀態unknown不得改寫成pending success或completed。

## 資料、權限與外部契約

- Persistent Marketplace/install/update/remove只在明確request下有最小必要`user`-scope write authority；status無write authority。
- Claude Plugin自己的mode Config與routing state是不同data owners：normal remove不刪Config，last-scope uninstall依官方預設處理routing data。
- `${CLAUDE_PLUGIN_ROOT}`是ephemeral cached code；`${CLAUDE_PLUGIN_DATA}`是跨Plugin update持久data；`${CLAUDE_PROJECT_DIR}`只用於判定project Config boundary，不持久保存。
- 每個router hook只從自己的stdin取得raw session ID並立即hash；raw ID不得寫入state、path、log或model-visible envelope，也不得透過`CLAUDE_ENV_FILE`傳遞。
- GitHub repository、formal tags、Releases與Claude Marketplace/CLI是external contracts；local fixture不證明public transport。
- 本規格採用的2026-09-04官方契約入口為：[Plugins reference](https://code.claude.com/docs/en/plugins-reference)、[Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)、[Skills](https://code.claude.com/docs/en/skills)、[Hooks reference](https://code.claude.com/docs/en/hooks)、[Subagents](https://code.claude.com/docs/en/sub-agents)與[CLI reference](https://code.claude.com/docs/en/cli-reference)。Release evidence MUST保存實際驗證日期、Claude Code version及任何契約差異。
- Node `22+`是Claude automatic-router consumer prerequisite；Plugin沒有third-party runtime package或network service。
- Release fixtures/logs/evidence MUST scrub credentials、raw session IDs、personal paths、unclean runtime state與machine-specific absolute paths。

## 相容性、推出與復原

- Codex與Generic consumers除`1.4.0` identity及approved docs/release coordination外，行為與runtime requirements MUST保持`1.3.1`相容。
- Claude Plugin只承諾Claude Code `2.1.251+`、Claude model `4.6+`；automatic route另需Node `22+`。
- Marketplace是唯一persistent path；ZIP是version-matched session recovery。兩者runtime bytes來自同source，但lifecycle聲明不同。
- Installed Plugin update後需reload/new session；old session可繼續old bytes，不得混稱已升級。
- Failed release build沿用`1.3.1` managed-output recovery；incomplete rollback保存recovery data與雙錯誤。
- `1.4.0`使用new artifacts/evidence，不原地修改、retag或重新包裝historical `1.3.1` evidence。
- External rollout日後若獲准，必須使用通過本規格gates的exact local candidate；若未獲准，local completion仍不得稱published。

## 限制與假設

2026-09-09 使用者核准離線優先開發順序：可先完成測試／context 計算工具、明示未驗證的文件草稿及隔離 preview 打包；詳見 [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) 的當日核准節。此順序不降低本規格的行為優先、真實 host／model evidence、正式 context threshold 或 local release completion 條件；只把不需登入的實作準備提前。

- Official Claude Code contracts可能在future versions改變；`2.1.251+`是本版minimum，不是無上限compatibility承諾。Future breaking behavior需新release處理。
- 現行official Hooks文件定義`UserPromptExpansion`，但官方`2.1.251` changelog只明載新增Pre/PostModelSwitch，沒有標出UserPromptExpansion的introduced version；因此exact minimum compatibility目前是release-blocking unverified assumption，而不是已完成證據。依2026-09-07核准的sequencing correction，Ticket 2與profiles可在清楚標示provisional／simulated evidence下先實作；此例外只移動驗證時點，不降低Ticket 3或local completion gate，且任何後續host差異都會使受影響implementation與evidence失效。
- Exact model mapping以release freeze時captured official evidence為準；unlisted future/custom IDs安全地成為unknown。
- Claude Code只在SessionStart可能提供model且可能省略；model switch authority來自PostModelSwitch。
- `disable-model-invocation: true`使兩個gated entries只能由使用者明確叫用，並降低未叫用時的Skill listing context；使用者需理解namespaced commands。
- 30-day stale-file cleanup只適用disposablerouting state；不適用任何workflow artifact或user Config。
- Fresh-session profile comparison可使用test-only direct profile selection，但consumer不能使用隱藏command切換profile。
- First live environment的實際OS/surface/model目前未定；選擇不改變compatibility target，但必須如實記錄。
- 本規格撰寫時local `claude` CLI unavailable；因此release前仍須在supported binary上重做strict validation與live smoke。

## 驗收條件

1. RDR、Knowledge Base與Draft/Approved artifact states可追溯；Specification核准前沒有Ticket Plan或production implementation。
2. `.claude-plugin/marketplace.json`與Claude `plugin.json`的exact fields、identity、version、author、source/ref、strict/default enablement符合第2節，且不含Codex-only或unknown fields。
3. Supported Claude Code對canonical Plugin與repository Marketplace root執行`claude plugin validate <path> --strict`各exit `0`且無warning。
4. Plugin discovery恰有兩個approved public Skill components，兩個namespaced forms都是canonical supported entries；十個×兩profiles internal modules不形成其他Skill components，bare alias只按host observed behavior記錄。
5. 兩Skills明確inherit active model且只能user-invoke；Plugin所有components都沒有model switch/pin/override。
6. Release-owned exact model mapping與route table對known5、supported non5、unsupported、unknown、old Claude Code、Node/router/state failure逐格通過。
7. Explicit `-5` unknown與Node-unavailable path將invocation視為明確選擇、揭露unverified後用optimized；knownnon5改general，knownunsupported停止。
8. Operation binding、Pre/PostModelSwitch transitions、notification、unsupported-mid-operation disclosure、Post commit後next-permitted-entry reroute及同session雙向profile authority tests通過；同operation不新載入或服從另一profile。
9. Startup/resume/fork/clear/compact、四種hook-derived session key、`ready`／`pending`／`indeterminate` state schema、30-day cleanup及cross-session tests通過。
10. State只位於`${CLAUDE_PLUGIN_DATA}`固定boundary且只有allowlisted fields；prompt、source、artifact、credential、PII、raw session ID與telemetry皆不存在。
11. General與Claude 5 profiles各自映射Core全部30條mandatory rules，static conformance/capability evidence均valid。
12. 第11節30個behavior scenarios在兩profiles都是100% pass，沒有skip/partial/exemption。
13. 十二個paired fresh-session cases在相同model/environment達成相同mandatory outcomes並保存input/profile/result/pass-fail evidence。
14. Full reviewer可用時產生read-only independent evidence；不可用時正確標non-independent或limited-evidence。Lite仍是same-context compact Review。
15. Claude Config paths、precedence、conflict、absent/invalid、project-root、read-only及no-persistence behavior全部符合第7節，且不讀寫settings.json/Codex Config。
16. Status request零writes並完整回報Claude Code、Node、Marketplace source/scope、qualified identity、version、enabled與entry availability。
17. Install/update lifecycle對absent/current-enabled/current-disabled/older/newer/Node-missing/source-mismatch/name-conflict/unsupported-scope/partial-failure outcomes符合第8節。
18. Normal remove只卸qualified user-scope Plugin；default delete與explicit keep-data都事先揭露並驗證，Config與Marketplace保持不動。
19. Marketplace runtime、canonical source、expanded Claude package及ZIP runtime relative content等價；expanded與ZIP extraction exact byte-equivalent。
20. Claude expanded/ZIP inventory恰符合第10節，archive名為`ask-then-do-it-claude-1.4.0.zip`，不含catalog/state/test/evidence/machine path。
21. 十個context scenarios先通過behavior gate，再於每個stage-ready及reviewer-ready checkpoint各自達成至少50% reduction；raw evidence可依固定algorithm重算。
22. Windows、macOS、Linux path/event/state/failure automated tests通過；CLI/VS Code/JetBrains official feature evidence與任何差異被記錄；exact `2.1.251` real binary另通過UserPromptExpansion與failure-semantics compatibility fixture，否則本規格返回revision。
23. 至少一個clean real Claude Code environment完成第14節八步smoke並記錄exact environment；其他branches只以明確simulated fixtures聲明，PostModelSwitch race limitation不被誤報為first-invocation guarantee。
24. README維持三語parallel layout；三語root START-HERE、getting-started、Claude guides與Plugin START-HERE完整且semantic-equivalent，12個START-HERE contract通過。
25. Release產生Codex、Generic、Claude三個expanded families、三個ZIP與三筆SHA-256；兩次isolated build byte-reproducible，ZIP/package equivalent。
26. Existing staging、collision、replacement/retry、rollback、checksum、removed-artifact、evidence與secret/path gates全部通過，沒有required gate被刪除或放寬。
27. Current identity一致為`1.4.0`；Completed `1.3.1` artifacts、evidence與recorded hashes無變更。
28. Codex／Generic除approved identity、docs入口及release coordination外，observable behavior、package inventory與consumer dependency無回歸；Node沒有滲入兩者。
29. Local Completed evidence誠實區分observed、simulated、unavailable與not-authorized；沒有live smoke或任何blocking failure時不得Completed。
30. Candidate不包含Community Marketplace、自訂`/doctor`、Skill conversion、personal-Skill fallback、billing/cost guarantee或未授權external publication mutation。

## 延後決策

- Ticket Plan中的垂直切分、依賴、parallel safety及每個Ticket的plain-language behavioral-test選擇；需要建立router/lifecycle/context/packaging behavior的Tickets必須保留本規格要求的deterministic evidence能力。
- 不改變observable contract的router函式邊界、diagnostic prose與test helper組織。
- 實際first live-smoke OS、surface與available supported model；一旦執行，exact facts進release evidence。
- `project`、`local`、`managed` Plugin scopes與任何跨scope migration。
- Claude Desktop、Claude Code web/cloud及其Plugin/hook/persistence驗證。
- Anthropic Community Marketplace submission、其他AI Agent adapters、universal Adapter Registry與cross-host installer。
- External `v1.4.0` tag、push、GitHub Release、asset upload、Marketplace activation與announcement；全部需後續明確核准。
