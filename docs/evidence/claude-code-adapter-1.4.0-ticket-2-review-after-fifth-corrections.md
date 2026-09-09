# Claude Code Adapter 1.4.0 Ticket 2 第五輪修正後獨立 Review

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-2-review-after-fifth-corrections`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Review label: `independent`

Status: Changes Requested

Ticket mode: Approved `tdd`

## Findings first

### [P2] Ready route 沒有執行 Claude Code `2.1.251+` runtime gate

**Trigger：** Claude Code `<2.1.251` 仍能載入 Plugin 並觸發本 Plugin 所需的 `SessionStart` 與 `UserPromptExpansion` 時，router 只檢查 Node 版本、event、mapping 與 session state；它可以產生 `routing_status: ready`。兩份 Skill 對 ready envelope 驗證 tuple 後就載入 profile，沒有先證明執行中的 Claude Code 版本。這個 trigger 不需要假設 exact `2.1.251` authenticated host ledger 的結果；它是已核准的 old-Claude-Code route branch。

**Impact：** automatic 與 explicit entries 都可能在規格明定不支援的 Claude Code 上開始 operation，違反 Specification 第 4 節「Claude Code `<2.1.251` 時兩個 entries 都 MUST 停止」、acceptance criterion 6 的 old-Claude-Code route cell，以及 Ticket 2 的完整 route/failure table。這也會把尚未受支援的 hook／lifecycle semantics 當成可信 state authority。

**Existing guard：** 兩份 Skill frontmatter 的 `compatibility` 有宣告 `Claude Code 2.1.251+`；envelope 缺失時 automatic 會停止，explicit 的兩條 manual fallback 也要求以 host command 證明版本。然而，frontmatter 宣告不是 ready-path 的可執行判定；當 router 已回 ready envelope 時，automatic Skill 的 lines 12–22 與 explicit Skill 的 lines 12–24 都沒有版本 proof。Router `main` 在 lines 1491–1559 僅執行 `checkNodeVersion(process.versions.node)`，hook input、state 與 envelope 都沒有可信 Claude Code version 欄位或分支。

**Evidence and location：** `adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md:12`、`adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it-5/SKILL.md:12`、`adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1491`。Adversarial probe 以完整合法的 startup/expansion events 建立 ready state，另放入 `CLAUDE_CODE_VERSION=2.1.250` 標記後，router 仍輸出 Claude 5 ready envelope；該環境變數不是可接受的 host authority，因此此 probe 不冒稱 old-host observation，但它確認 production route 沒有任何 Claude Code version gate/input。現有 `tests/claude/test_router_contract.py:199` 的 route matrix只覆蓋 model classification，lines 383–452 覆蓋 Node minimum；`tests/claude/test_public_plugin_contract.py:429` 只檢查 explicit manual fallback 的 Claude Code gate，沒有「合法 ready envelope + Claude Code 2.1.250 必須停止」的 behavioral test。

**Remediation direction：** 在兩個 entry 消費任何 ready envelope 並載入 profile 前，加入同一個可信且 deterministic 的 Claude Code minimum-version proof；或修訂 host/router contract，提供不擴張既定 envelope／privacy boundary 的可信版本 authority。新增 TDD cases，至少證明 `2.1.250` 在 otherwise-valid ready path 對兩個 entries 都停止、`2.1.251` 通過，而且無法證明版本時 fail closed。不要把 `compatibility` prose、hook availability或 Ticket 3 尚未完成的 authenticated ledger當作 runtime version proof。

Finding count: 1 (`P0`: 0, `P1`: 0, `P2`: 1, `P3`: 0)

## Reviewed inputs

- Approved Specification：`docs/specs/claude-code-adapter-1.4.0.md`，特別核對 model classification、entry routing、session lifecycle、state/security、failure behavior 與 acceptance criteria 6–10、22。
- Approved Ticket Plan：`docs/plans/claude-code-adapter-1.4.0.md` 的 Ticket 2，以及其 Ticket 1 boundary、Ticket 3 provisional dependency與後續 Tickets 4/5 sequence；Approved mode 為 `tdd`。
- Final production：
  - `adapters/claude-code/plugin/ask-then-do-it/hooks/hooks.json`
  - `adapters/claude-code/plugin/ask-then-do-it/config/model-classifications.json`
  - `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs`
  - `adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md`
  - `adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it-5/SKILL.md`
  - `scripts/validate_claude_plugin.py`
  - `scripts/validate_claude_model_evidence.py`
- Final tests：`tests/claude/` 全部檔案，包括 model source-trace fixtures。
- Raw verification：題目提供的 focused correction batches、Claude suite、full repository suite、syntax、兩個 validators、`git diff --check`、exact binary version與兩個 strict validations；另包含本 reviewer 的獨立重跑與 adversarial probe。

本 Review 未讀取任何先前 Ticket 2 implementation evidence、review verdict、architecture diagnosis或其他 implementer narrative。

## Assumptions

- 本 operation 的 top-level mode 已由上游證明為 Full fallback：project 與 user 的 `.codex/ask-then-do-it.toml` 均不存在；本 Review 不重用該結論到其他 operation。
- Fresh reviewer context 未參與 Ticket 2 implementation，且審查輸入未包含 implementer defense 或既有 verdict，因此 label 為 `independent`。
- Ticket 2 可依已核准 sequencing 先做 provisional implementation；Ticket 3 authenticated live ledger仍是 local `1.4.0` completion hard gate，但不是本 Review 的 code finding。
- `compatibility` frontmatter是必要的 requirement declaration；在 production flow 未把它變成判定或 proof 的情況下，不把它視為已執行 old-host stop branch。
- Raw full-repository與exact-binary結果採題目提供的原始摘要；本 reviewer 沒有把 strict validation解讀為 authenticated Claude session。

## Raw verification

### 題目提供

- Focused correction batches：全部 exit `0`。
- Claude suite：`Ran 98 tests in 59.566s; OK (skipped=1)`。
- Full repository：`Ran 314 tests in 81.295s; OK (skipped=1)`。
- Node syntax、Claude Plugin validator、model evidence validator、`git diff --check`：全部 exit `0`。
- Claude Code exact `2.1.251 --version`、Plugin strict validation、Marketplace strict validation：全部 exit `0`。
- 唯一 skip 是 Windows 帳號沒有 file-symlink privilege；directory junction test已通過。

### 本 reviewer 獨立執行

- `.venv/Scripts/python.exe -m unittest discover -s tests/claude`：exit `0`；`Ran 98 tests in 62.696s`；`OK (skipped=1)`。唯一 skip與題目描述一致。
- `node --check adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs`：exit `0`。
- `.venv/Scripts/python.exe scripts/validate_claude_plugin.py`：exit `0`。
- `.venv/Scripts/python.exe scripts/validate_claude_model_evidence.py --mapping ... --trace ...`：exit `0`。
- `git diff --check`：exit `0`；只有既有 working-copy LF→CRLF warning，沒有 whitespace error。
- Adversarial old-host-gate probe：合法 startup/expansion events可產生 ready envelope；額外 process marker `CLAUDE_CODE_VERSION=2.1.250` 不改變結果。此 probe只證明程式沒有版本 gate，不是 authenticated host observation。

## Acceptance criteria assessment

| Criterion | Assessment | Evidence |
| --- | --- | --- |
| 6 — exact mapping與完整route table | **Not met** | known Claude 5、supported non-5、unsupported、unknown、Node/router/state failures有 production branch與測試；old Claude Code ready path缺少可執行 stop gate，見 P2 finding。 |
| 7 — explicit `-5` paths | **Met for Ticket 2 deterministic scope** | unknown→optimized disclosure、known non-5→general、unsupported→failure，以及兩條 Node unavailable manual fallback boundaries由兩份 Skill、router tests與public contract tests覆蓋。Ready path仍受 P2 的共用 host-version finding影響。 |
| 8 — operation/switch binding | **Met for router/state scope** | operation ID覆寫、Pre pending、matching/mismatching Post、generation、unsupported-mid-operation disclosure、Post-commit next-entry reroute、commit前 best-effort語意皆有實作及測試。跨 profile modules 的完整 behavior屬 Tickets 4/5。 |
| 9 — lifecycle/state | **Met** | startup/resume/fork/clear/compact、same-session binding、cross-session isolation、ready/pending/indeterminate、generation exhaustion、30-day cleanup、lock recovery與atomic concurrency均有 behavioral evidence。 |
| 10 — data/security boundary | **Met with residual platform caveat** | fixed `${CLAUDE_PLUGIN_DATA}/routing/v1/sessions`、SHA-256 key、exact state schema、bounded strict JSON、no prompt/raw ID/path persistence、mapping integrity、static link/junction rejection及atomic replacement均受測。Windows file-symlink case因權限跳過，但directory junction case通過。 |
| 22 — automated path/event/state/failure portion | **Partially verified** | current Windows環境的98 tests與strict validations通過；macOS/Linux實際執行結果未提供，exact authenticated hook/failure semantics依計畫留給 Ticket 3。這些未驗證項不得升格為 live claim。 |

## State-transition and failure review

- `SessionStart`：startup/fork不延續operation；resume/compact只延續same-session binding；clear清除binding；resume省略model重設unknown；compact省略model只在ready state沿用；generation overflow fail closed。
- `UserPromptExpansion`：只接受 target slash command/plugin identity；同session ready state才建立新operation；pending、indeterminate、missing、stale、invalid、ownership、schema、mapping與write errors都輸出closed、bounded、exit-0 failure envelope；沒有建立operation。
- `PreModelSwitch`：requested sources建立pending與next generation；mismatch轉indeterminate；任何失敗只輸出non-blocking warning，不傳deny/ask decision。
- `PostModelSwitch`：requested source要求matching pending；auto/resume可由ready state直接建立下一generation；mismatch轉indeterminate；成功時保留operation並輸出same-profile/next-entry notification；失敗警告且不改model。
- Race boundary：Post commit前可能使用最後ready classification；commit後下一個permitted entry必須依新classification。Production text與tests均未宣稱model change後第一個invocation必然reroute。
- 唯一 blocking差異是host minimum version未進入ready-route state machine，見 P2 finding。

## Security, privacy, and secret-boundary review

- Raw `session_id`只在process memory中hash成64位lowercase SHA-256 key；state、path、envelope與test assertions未保留raw ID。
- Prompt、command arguments、cwd/transcript path、billing/cache metadata與unknown event fields不進state或envelope；invalid/duplicate/oversized/invalid-UTF-8 input fail closed。
- Model classification只使用SessionStart model與Post `to_model`；requested model、user text、environment model variables與substring不成為authority。Unmapped/custom/future IDs為unknown且不持久化可能含tenant marker的原文。
- State inventory、operation/pending objects與failure codes均closed；mapping以semantic digest綁定release-owned config，source trace另綁byte digest與dated snapshots。
- State write採same-directory temporary file、exclusive create、file sync與rename；per-session owned lock避免同session並行lost update，stale recovery需lease、mtime與dead PID三重條件。
- Static symlink/junction及component escape被拒絕；檔案/目錄建立採restrictive modes。主動同權限filesystem attacker在ancestor-check與open/rename之間的TOCTOU仍列為低可利用性的residual risk，未發現由本變更新增的直接越界寫入probe。
- Router無第三方runtime dependency或network API；hook採argument-vector exec form，沒有shell concatenation、async handler、`CLAUDE_ENV_FILE`或global-current-session lookup。

## Test quality and gaps

- Positive matrix完整覆蓋known5、supported non-5、unsupported與unknown兩entries；negative tests覆蓋event schema/type/duplicate keys、mapping drift、state corruption、ownership、stale state、invalid operation tuple、generation exhaustion、concurrency、lock recovery與linked paths。
- Tests會檢查envelope exact keys、closed code sets、operation/state一致性、user-visible ready disclosures、manual fallback prerequisites及secret/raw-ID absence；這些 tests 對常見回歸具失敗敏感度。
- Blocking test gap：沒有把 Claude Code version放入 ready-route test fixture，也沒有測試otherwise-valid `2.1.250`必須讓兩entries停止。因此98-test suite無法偵測 P2 finding。
- Unverified而非本 Ticket code finding：authenticated namespaced invocation、real `additionalContext`、bare alias與exact host failure semantics仍留給 Ticket 3；strict validation不能替代這些 observations。
- Current runner是Windows；macOS/Linux native filesystem executions未提供。Path construction使用Node native `path`且Windows上覆蓋spaces、forward-slash hook arg、junction與lock/state behavior，但不可把本次run聲明成三平台live evidence。

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — outcome: `no-finding`。** Exact model table同時受config、router semantic digest、validator constants與source-trace digest約束；雖有多處representation，但每處各自擔任runtime、release validation與evidence角色，mutation tests會拒絕漂移，未形成未受控的雙重authority。
2. **Long Function — outcome: `no-finding`。** Router以strict parsing、mapping、path/lock、state validation及四個handlers拆分；較長的`parseJsonStrict`只負責duplicate-safe bounded JSON parsing，沒有混入state transition或I/O policy。
3. **Large Module or Class — outcome: `no-finding`。** `router.mjs`雖大，但保持單一Plugin runtime trust boundary，內部函式分隔event validation、mapping、filesystem ownership與lifecycle；沒有證據顯示本 Ticket 的變更需因不同產品理由反覆改同一分支。
4. **Long Parameter List — outcome: `no-finding`。** 公開內部helpers的參數最多仍可辨識；`withSessionLock`以options object承載policy，handlers接受event/pluginData/mapping三項。`readState`的兩個boolean僅在少數lifecycle呼叫使用，尚無錯置證據。
5. **Data Clumps — outcome: `no-finding`。** State、pending switch、operation、route envelope與hook events都用具名object及exact-key schema聚合；沒有相關值以平行primitive list反覆傳遞。
6. **Primitive Obsession — outcome: `no-finding`。** String/number primitives由closed Sets、regex、exact tuples、safe-integer與timestamp validation賦予domain constraints；invalid primitive不會直接進state transition。
7. **Feature Envy — outcome: `no-finding`。** 各handler主要操作自己的validated event與state；mapping classifier、state validator及lock abstraction沒有跨模組抓取其他owner內部資料。
8. **Divergent Change — outcome: `no-finding`。** Router的變更理由集中在同一model-routing/session-state contract；Plugin schema與model-source evidence驗證分離在兩個Python validators，未把release/catalog職責塞回runtime。
9. **Shotgun Surgery — outcome: `no-finding`。** Model freeze確實要求同步mapping、trace與integrity constants，但這是核准的release-owned fail-closed更新程序；semantic/byte digests與negative tests讓漏改成為明確validation failure，而不是silent surgery。
10. **Message Chains — outcome: `not-applicable`。** Reviewed runtime是procedural Node module與flat JSON state，沒有多層object navigation/caller chain暴露內部結構；state path由單一helper產生。
11. **Leaky Abstraction — outcome: `finding`。** P2 finding即此lens的唯一finding：public Skill把ready envelope視為完整routing authority，但該abstraction不攜帶或執行Claude Code minimum proof，呼叫端只能從frontmatter prose猜測host prerequisite；在old host仍觸發hooks時會越過已核准stop boundary。位置：兩份public `SKILL.md:12`與`router.mjs:1491`。
12. **Shallow Module — outcome: `no-finding`。** Strict parser、mapping loader、owned lock、atomic writer與state validator各自以窄介面封裝實質安全policy；介面複雜度有對應的validation、ownership或atomicity價值。

這十二項只評估 Ticket 2 change及直接impact area，不聲稱system-wide architecture diagnosis。

## Deferred checks and unavailable evidence

- Ticket 3 authenticated clean Claude session：兩個namespaced invocations、real `additionalContext`、bare alias observation、Node unavailable/nonzero/exit-2/timeout expansion semantics。現有strict Plugin/Marketplace validation與exact binary `--version`不等於這些證據。
- Exact `2.1.251` host若推翻 provisional command identity、matcher或failure assumptions，必須返回最早受影響的Requirement／Specification／Ticket並重驗本Ticket。
- macOS與Linux native test runs未提供；本reviewer只在Windows重跑。
- Windows file-symlink privilege不可用，因此該單一test skipped；directory junction rejection已實跑通過。若release要求file-symlink的本機實證，需在具權限runner補跑。
- General／Claude 5 profile modules、同session雙向module-authority、paired conformance與context reduction分屬後續Tickets 4–6，不以本Ticket production假裝已驗證。

## Residual risks

- Host hook JSON與source enum可能隨Claude Code版本改變；strict exact-key parsing會安全停止，但可能造成availability regression。Ticket 3與future release evidence需保存exact host observations。
- PostModelSwitch有官方best-effort commit race；commit前可能依最後ready classification路由，production已誠實揭露且commit後重新路由。
- Same-user或同權限process可對routing directory製造大量invalid files、lock contention或極窄filesystem TOCTOU；現有bounded reads、no-link checks、owned locks與atomic rename降低影響，但不是對惡意local administrator的security boundary。
- Manually normalized official source snapshots由hash與validator固定，可重算repository evidence，但不是2026-09-07官方網站的即時重新抓取；future mapping更新必須重新查核官方來源。
- Ticket 3尚未完成是local `1.4.0` completion hard gate；它是unverified host evidence，不是新增的Ticket 2 code finding。

## Ticket completion assessment

Ticket 2 **尚不可判定完成**。Approved `tdd` mode、絕大多數deterministic route/state/security scenarios與raw tests均成立，但 acceptance criterion 6 的 old-Claude-Code cell沒有production gate，也沒有會對該缺陷先紅的behavioral test。依findings-first規則，本次 verdict為 **Changes Requested**，不可標示Accepted。

## Next handoff

回交Ticket 2 implementer：以Approved `tdd` mode先加入兩個ready-entry的old-host failing tests，再實作可信Claude Code `2.1.251+` runtime gate，重跑focused Claude suite、full repository、Node syntax、Plugin/model-evidence validators、strict validations與`git diff --check`。修正後交給另一個fresh independent reviewer。Ticket 3 authenticated host ledger仍維持local `1.4.0` completion前的獨立hard gate，不得以本次修正或strict validation取代。
