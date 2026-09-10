# Claude Code adapter 規格

適用來源：1.4.0。這是現行行為要求的彙整，不是實測通過聲明。當前已驗證範圍與缺口見[工作狀態](../project/status.md)，操作方法見[Claude 使用說明](../guides/claude-code.zh-TW.md)及[驗證手冊](../maintainer/validation.md)。跨平台共同流程以[工作流程規格](workflow.md)與 [Core](../../core/CORE.md)為準。

原始規格的行為章節保留在下方，移除重複的目標／情境敘述、施工交接與歷史版本切換指示。原始要求和核准時間可由[來源索引](../evidence/release-history.md#document-sources)追溯。前期可行性研究中的 95%／98% 通過率、其他命名及自訂 doctor 等方案均未採用，不能覆蓋本規格。

## 閱讀地圖

- 公開來源與入口：第 2–3 節。
- 模型、session、Config 與 reviewer：第 4–7 節。
- 安裝與資料安全：第 8–9 節。
- 封裝、behavior、context 與平台實測：第 10–15 節。

最低版本為 Claude model 4.6+、Claude Code 2.1.251+、automatic router 的 Node.js 22+，彼此獨立。General 與 Claude 5 profiles 沿用使用者 active model；profile 選擇不切換模型。Qualified Plugin identity 為 `ask-then-do-it@ask-then-do-it`。

本版持久安裝支援 `user` scope，本機 CLI／VS Code／JetBrains 是相容目標。`project`／`local`／`managed` lifecycle、Claude Desktop、web/cloud、其他 agent adapters、universal installer、personal-Skill fallback、自訂 `/doctor` 與 Community Marketplace submission 均未納入。它不保證真實 API 帳單、總 context 或 latency 減少 50%。

## 1. 規格與現行來源

本文件彙整原 Approved Claude 1.4.0 requirement/specification，並採用後續已核准的版本統一及文件整理決策。來源現行版本為 1.4.0，包含 Core、三 adapters、runtime、catalogs 與 release config；schema version、最低相依版本和歷史發布版本各自獨立。

歷史 Approved artifacts 的原始 bytes／核准證據保存在清理快照，參見[來源定位](../evidence/release-history.md#archive)。從工作目錄移除舊文件不等於改寫原始證據。新的摘要也不自動成為新行為的 Approved Specification。

2026-09-10 的版本對齊決策允許先完成來源與離線三套件 ZIP；正式驗收仍需要 Claude host、behavior、context、live-smoke 證據。封裝成功不能當成已實測或已發布。使用／維護文件的現行組織由本次核准的整理計畫接續。

## 2. Claude catalog 與 Plugin manifest

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

## 3. Public Skills、profiles 與 internal modules

Plugin MUST 恰好包含兩個 public Skill components：

1. `skills/ask-then-do-it/SKILL.md` → `/ask-then-do-it:ask-then-do-it`。
2. `skills/ask-then-do-it-5/SKILL.md` → `/ask-then-do-it:ask-then-do-it-5`。

兩個 Skill frontmatters MUST 明確使用各自的 `name`、精確 description、`disable-model-invocation: true`、`user-invocable: true`、`model: inherit` 與三項 version requirements 的 `compatibility`；MUST NOT 指定另一 model、effort、forked context、background execution、broad pre-approved tools 或 dynamic shell injection。User MUST 能透過 namespaced command 明確啟動，Claude MUST NOT 自行選擇何時啟動這個 gated workflow。Claude Code MAY 在沒有名稱衝突時另顯示 host-provided bare alias；該 alias 不是第三個 Plugin component，且本產品不把它列為 supported entry、也不保證它存在或不存在。

兩個 Skill bodies MUST只是profile-neutral bootstrap，且只接受同一次`UserPromptExpansion`提供的bounded、schema-valid route envelope；不得自己接收或轉送raw session ID，也不得以dynamic shell injection或另一個model判斷profile。Envelope只能含plugin/version、entry、operation ID、classification、selected profile、routing status與固定disclosure code；不得含prompt、arguments、paths或raw hook input。

Automatic entry MUST先取得schema-valid deterministic route envelope，再只載入所選profile的orchestration與需要的stage modules；envelope缺失、重複、invalid或failure時停止。Explicit entry在valid success envelope可用時依route result執行；valid `node-too-old` failure envelope MAY依manual-path contract揭露限制並載入optimized profile。Envelope缺失時，bootstrap MUST以可用host commands分別證明Claude Code `2.1.251+`且Node確實missing，才能使用相同manual path。Node `22+`卻沒有envelope、任一version無法證明或Claude Code低於minimum時都停止；不得把handler crash、state failure或hook misconfiguration猜成允許manual fallback，也不得把manual path稱為已驗證Claude 5或完整automatic-routing support。

Internal stage modules MUST 位於 `profiles/general/` 或 `profiles/claude-5/`，每個 profile 恰有以下十個檔案：`orchestration.md`、`lite-workflow.md`、`requirements.md`、`documented-requirements.md`、`specification.md`、`ticket-planning.md`、`tdd-implementation.md`、`direct-implementation.md`、`review.md`、`architecture-improvement.md`。它們不得位於 `skills/` 或 `commands/`，不得成為第三個 public command。

General MAY 使用較完整說明。Claude 5 profile MAY 合併重複敘述、使用短引用與 progressive disclosure，但每個 mandatory rule、gate、failure outcome、artifact state、authority boundary 與 evidence requirement MUST 有可追溯且可執行的映射。一次 operation 不得新載入另一 profile 的 modules。因 Claude Code 會把先前已叫用 Skill 的文字保留在 conversation，最新 public entry 與其 bound profile MUST 明確取代先前 operation 的 profile authority；舊 profile 內容只可當歷史 context，不得再控制目前 operation。General→Claude 5 與 Claude 5→general 的同 session 連續 invocation 都 MUST 以 behavioral tests 證明此 precedence；若無法證明，profile 改變時 MUST 停止並要求 `/clear` 或 new session，而不得混用。

## 4. Model classification 與 entry routing

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

## 5. Session lifecycle 與 operation binding

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

## 6. Capability 與 Review

兩個 profiles 在每次 operation 開始時 MUST 宣告實際可證明的最強 capability：`conversation`、`tools` 或 `multi_agent`。Static Claude conformance MAY 宣告三者，但 runtime tool availability與permission才是當次 authority。

Plugin MUST 提供 `agents/ask-then-do-it-reviewer.md`。Agent frontmatter MUST 使用 stable name、清楚 description、`model: inherit`，不強制 background，並把可用工具限制為 `Read`、`Grep`、`Glob`；不得有 Write、Edit、shell、network、MCP、memory、worktree isolation或其他 side-effect surface。Claude Code MAY 依 host/session mode在foreground或background執行它，但主 Claude MUST 等待 reviewer完成並取得結果後才可整合findings或完成Full Review。Reviewer instructions MUST 檢查 Approved requirements、Specification、Ticket mode、diff、tests、raw evidence及十二個 Core Architecture and Refactoring Lenses。

Review behavior MUST 為：

- Agent tool 與 reviewer 可用：Full 使用 independent read-only reviewer context；主 Claude驗證、整合 findings，不盲從 reviewer output。
- Tools 可用但 reviewer／Agent 不可用：Full 仍 Review，但明確標示 `non-independent` 與 unavailable independent evidence。
- 只有 conversation／user excerpts：只能做 `limited-evidence` Review，列出未讀 repository、未執行 tests 與 handoff；不得宣稱完成 repository Review。
- Lite：始終使用既有 same-context compact Review 與 findings correction approval；不得因 Plugin 含 reviewer 而升級為 Full 或 independent Review。

Reviewer unavailable 本身不阻擋完成；其他 Core validation、finding、approval 與 disclosure gates 仍決定是否可完成。

## 7. Full／Lite 與 Claude Config

General 與 Claude 5 profiles MUST 各自映射 [Core mandatory rules](../../core/rules/rules.yaml) 的全部 30 個 IDs，沒有 profile-specific exemption。Mapping MUST 保留 capability honesty、mode resolution、Full lifecycle、Lite lifecycle、requirement/knowledge/spec/plan gates、TDD/direct distinction、Review evidence/lenses、artifact states、architecture diagnosis/deletion/reflow及 explicit routing rules。

Full MUST 保留 Requirement Decision Record、documented Knowledge Base sync、Specification、Ticket Plan、逐 Ticket plain-language test choice、Approved `tdd`／`direct` implementation evidence、Review 與 architecture contract。Lite MUST 保留 blocking questions、single Change Brief gate、no workflow artifacts、no new tests、proportionate validation、same-context compact Review、correction approval、session non-persistence與 honest completion。

Claude mode Config paths MUST 為：

- user default：`~/.claude/ask-then-do-it.toml`；
- project override：`<project>/.claude/ask-then-do-it.toml`，且必須位於 active project root。

唯一 recognized value 是 top-level `mode = "full"` 或 `mode = "lite"`。Aliases、不同大小寫、unquoted value、nested value、missing/duplicate mode、malformed TOML 或 unsupported value 都不是有效 mode。

每次 operation MUST 使用以下 precedence：valid explicit current-operation instruction、project Config、user Config、Full fallback。Conflicting explicit Full/Lite MUST 暫停並問一次。Valid explicit instruction MUST 不讀 lower sources。Project Config absent 才讀 user Config；present unreadable/malformed/missing-mode/unsupported project Config MUST fail closed to Full 且不讀 user Config。User Config同理，absent 才 Full fallback。

Config resolution MUST 完全唯讀；不得建立、修復、正規化、持久化 override 或寫入 `settings.json`。Claude MUST 不讀 Codex Config；Codex MUST 不讀 Claude Config。

## 8. Marketplace lifecycle 與 authorization

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

## 9. Router state、資料與安全

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

## 10. Package 與 deterministic release inventory

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

`release/release.json` MUST 宣告 Claude family、archive、source、inventory與Claude-required checks；`managed_outputs` MUST 是 `codex`、`generic`、`claude`、`checksums.sha256`。Release MUST 產生三個 expanded families、三個 archives與每個archive恰一筆SHA-256。Checksum ordering MUST deterministic且由release config package order固定。

現有complete staging validation、unmanaged collision protection、managed replacement、Windows `WinError 5` bounded retry、rollback、incomplete-recovery preservation、two-build byte reproducibility、deterministic ZIP metadata、ZIP equivalence、SHA-256、removed-artifact scan及evidence validation MUST 不退化。

Codex／Generic除current version、Claude cross-entry docs與三-family release coordination所需變更外，observable behavior、package relative inventory、runtime dependency boundary與provider config MUST 不變。Node.js MUST 只出現在Claude consumer prerequisites／package tests，不得成為Codex或Generic runtime dependency。

## 11. Conformance 與 fresh-session behavior evidence

Claude MUST 維持獨立 `adapters/claude-code/conformance.yaml` 與 provider-specific validator/tests。Manifest MUST 使用 `adapter_id: claude-code`、`adapter_version: 1.4.0`、`target: claude-code-plugin`、`core_version: 1.4.0`，宣告 cumulative `conversation`、`tools`、`multi_agent`，為每個 capability提供非空evidence，並列出target Core全部30個mandatory rule IDs。

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

## 12. Claude 5 loaded-context proxy

Context fixture MUST 固定十個 scenarios：documented requirements、Specification、Ticket Planning、TDD implementation、direct implementation、Full Review、architecture diagnosis、normal Lite、high-risk Lite及model-switch continuation。每個scenario都以automatic entry與deterministicroute fixture分別產生general/optimized path，並使用相同user task、capability與stage outcome。

每個scenario MUST 有 `stage-ready` checkpoint：route已完成且執行該stage所需Plugin instructions已載入，但尚未讀task-specific repository source或必要tool output。Full Review另有 `reviewer-ready` checkpoint：read-only reviewer agent prompt已載入且尚未加入task-specific diff/evidence。每個scenario的每個checkpoint都必須獨立達到至少50% reduction；不得以平均值、另一checkpoint或另一scenario補償。

Counted material MUST 包含每次實際載入／注入的：public Skill body、Skill listing text若host實際載入、selected profile orchestration/stage modules、router route-result text、hook additional context、Plugin reviewer description與完整agent prompt。相同Plugin text若在同一scenario重複注入，MUST按每次實際注入重複計數；reviewer context不得因位於另一model context而排除。

Excluded material MUST 只有：host system prompt、tool/MCP definitions、user task text、task-specific repository source/diff/artifacts、必要tool output、hidden reasoning與model output。Router/script/config source若只由machine執行且未送入model不計；它們的model-visible output仍計。

每個source先以UTF-8讀取並保存raw SHA-256；measurement依actual load order將每一source做Unicode NFC、把每段Unicode whitespace collapse成單一ASCII space、trim，再以一個LF串接。`normalized_bytes`是結果UTF-8 byte length；`proxy_tokens = ceil(normalized_bytes / 4)`；`reduction = (general - optimized) / general × 100`。Pass判定 MUST 使用整數關係 `optimized × 100 <= general × 50`，避免rounding改變結果。

Evidence MUST 保存fixture/version、scenario/checkpoint、profile、input hashes、source paths、load order、每個raw SHA-256、normalized bytes、proxy tokens、公式、兩個raw totals、reduction與pass/fail。Claude `/context`、`claude plugin details` projected token cost或observed usage MAY作diagnostic，但不得取代deterministic gate或支援billing/cost claim。

## 13. Documentation 與 localization

`README.md` MUST 保留現有English／繁中／日本語平行layout與每語言既有Introduction、Quick Start、Automatic installation (CLI)、nested Codex CLI、Manual installation、Read more相對順序。Claude內容只能插入對應位置；不得重構無關Codex／Generic內容。

三個 root `START-HERE.*.md` MUST 包含 Claude consumer choice。三個 `docs/guides/getting-started-simple.*.md` MUST 保持 provider-neutral Full/Lite owner 並保留 Claude 起始路徑。MUST 保留 `docs/guides/claude-code.en.md`、`.zh-TW.md`、`.ja.md`，完整擁有版本、user-scope lifecycle、兩entries、routing、Config、reviewer、platform、ZIP recovery及troubleshooting。

Claude Plugin/ZIP的三個START-HERE MUST簡短並連到same-version detailed guide，不複製完整workflow。Root、Codex、Generic、Claude各三個，共12個START-HERE pages MUST通過存在、relative links、brevity、version與packaged-copy tests。

三語內容 MUST semantic-equivalent，並清楚區分：Claude model／Claude Code／Node versions；known unsupported／valid unknown／router failure；automatic／explicit `-5`；compatibility target／live-verified；persistent Marketplace／session-only ZIP。Built-in `/doctor` 只能列為optional Claude Code installation/config health check，不得宣稱會轉換、最佳化或驗證Ask Then Do It Skills。

## 14. Platform compatibility 與 live smoke

Compatibility contract涵蓋Windows、macOS、Linux上的local Claude Code terminal CLI、VS Code extension與JetBrains plugin。Automated tests MUST覆蓋path separator/space、Node exec form、四種hook JSON/event sources、hook-derived session key、`ready`／`pending`／`indeterminate` transitions、atomic state、classification、cross-session isolation、failure behavior與package extraction。Official feature-availability evidence MUST證明每個surface支援本規格依賴的local Plugin、Skill、Agent與hooks；surface 差異必須記錄於[驗證手冊](../maintainer/validation.md)及相應原始證據。

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

## 15. Publication boundary

Local completion只包括source、packages、ZIP、checksums、automated/live validation、Review、architecture diagnosis與Completed release evidence。Evidence MUST逐項分開observed、simulated、unavailable與not authorized。

本Specification核准、Ticket/implementation、local smoke或candidate完成都不授權tag、push、GitHub Release、asset upload、public Marketplace activation、Community Marketplace submission或announcement。每個external mutation需要後續明確核准與執行結果。

[回到 README](../../README.md)
