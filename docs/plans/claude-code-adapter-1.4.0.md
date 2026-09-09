# Ask Then Do It 1.4.0 Claude Code Adapter Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `claude-code-adapter-1-4-0-plan`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Target release version: `1.4.0`

Status: Approved

Inputs: Approved [Claude Code Adapter 1.4.0 Specification](../specs/claude-code-adapter-1.4.0.md)、Approved [Requirement Decision Record](../requirements/claude-code-adapter-1.4.0.md)、Approved and synchronized [Project Knowledge Base](../project/knowledge-base.md)、Approved [Specification Knowledge Base Change Summary](../project/drafts/claude-code-adapter-spec-kb-change-summary.md)、Approved [Specification Knowledge Base Correction Summary](../project/drafts/claude-code-adapter-spec-kb-correction-summary.md)、Completed local [1.3.1 release evidence](../evidence/ask-then-do-it-release-1.3.1.md)，以及目前 repository architecture、tests、release builder 與 frozen historical contracts。

Assumptions: Completed local `1.3.1` candidate 是 implementation baseline；不假設 external `v1.3.1` 或 `v1.4.0` 已發布。Exact Claude Code `2.1.251` binary、provenance與三個strict-validation results已取得，但authenticated namespaced invocation、`additionalContext`、bare alias與failure semantics仍`unverified`。依使用者2026-09-07核准，Ticket 2與profiles可先依官方文件及明確標示的simulated fixtures做provisional implementation；Ticket 3仍須在local `1.4.0`完成前通過。使用者已選擇十張 Ticket 全部加入測試，全部映射為 `tdd`。

Deferred: 不改變 observable contract 的 router 函式邊界、diagnostic prose 與 test helper 組織；實際第一個 live-smoke OS／surface／model；Claude Code `project`／`local`／`managed` scopes；Claude Desktop／web／cloud；其他 AI Agent adapters；universal Adapter Registry／cross-host installer；Anthropic Community Marketplace；Git tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement。

Handoff: 十張 Ticket 維持 Approved `tdd`。依下方 2026-09-09 核准的離線優先順序，現在進入 Tickets 6–9 的離線工具、文件與 preview 打包準備。Tickets 4、5 correction 已 accepted，但模型行為仍待驗證；Ticket 3 與所有 live／behavior／context／release gates 保留，不能提前宣稱完整 Ticket 或 local release 完成。

Approval: 使用者於 2026-09-05 在完整Ticket definitions、依賴順序、全部測試建議與十張Ticket的`tdd` mapping展示後明確回覆「核准」，核准本Plan的精確內容。使用者於2026-09-07在被告知可能因exact-host差異返工後，明確核准將Ticket 3從Ticket 2／profiles的前置gate移至local `1.4.0` completion gate，並立即進入Ticket 2；Ticket modes與test choices不變。這些核准均不授權external publication。

## 2026-09-09 核准的離線優先順序

使用者明確核准「先做完能離線準備的部分；需要 Claude 的實測與最終驗收集中到最後」。本節是目前執行順序的 authority，取代下方先前把整張 Ticket 完成作為離線開發前置條件的描述；產品 acceptance criteria、十張 Ticket 的 `tdd` mode、最低版本與真實驗收要求不變。

- Tickets 4、5 的指令與靜態修正已通過獨立 Review；實際模型觀察仍待補。這些已審閱來源可供離線工具使用，後續變更須重新驗證。
- Ticket 6 現在可建立 staged conformance、共用情境／paired／authority 驗收工具、固定 expected outcomes 與未執行結果模板。工具測試只能使用明示 synthetic fixtures；缺實際 transcript 時必須拒絕完整行為通過，不能製造 model evidence。
- Ticket 7 現在可建立計算工具與合成資料的單元測試。真實 source 的正式 context measurement／50% pass 仍等待行為 gate；不得以離線估算代替 release evidence。
- Ticket 8 現在可根據 Approved Specification、已有 native observations 與有日期的官方文件起草三語文件，依原 README 布局加入資訊；未驗證的相容性、指令與發佈状态明確揭露。host／behavior 結果取得後再做最終文案核對。
- Ticket 9 現在可擴充 builder 的 Claude 支援與隔離測試／preview 打包。current release config、Core／Codex／Generic identity、canonical Claude conformance、default `dist/` 與歷史 `1.3.1` 保持原狀；三-family `1.4.0` lockstep activation 與 candidate freeze 仍等待 required gates。
- 最後集中執行 Ticket 3、兩套各 30 scenarios、12 paired cases、雙向 authority、正式 context checkpoints、文件核對、正式打包與 Ticket 10 smoke／Review。缺實際結果的 Ticket 保持未完成。

離線 ownership 可平行：Ticket 6 擁有 behavior/conformance scripts 與 tests；Ticket 7 擁有 context script／tests；Ticket 8 擁有 user docs／documentation tests；Ticket 9 擁有 builder／package tests。共用介面先固定，full-suite／generated output／native validation 由協調者串行執行；profile source、router 與既有 Knowledge Base 不在本次修改範圍。

本次核准不包含登入、模型付費呼叫、安裝／啟用 Marketplace、tag、push 或發佈；使用者先前暫緩登入的決定繼續有效。

## 共同範圍與規劃原則

- Knowledge Base gate 已完成；本 Plan 不新增 Approved Specification 以外的行為。
- 每張 Ticket 交付可經公開 Plugin boundary、固定 fixture、package boundary 或 release evidence 驗證的結果。Ticket 1、2 是後續不可避免的最小 enabling slices，並明列第一個 consumer。
- Exact Claude Code `2.1.251` compatibility 是local completion前的fail-fast hard gate。Ticket 3完成前，任何host-dependent matcher、route或failure evidence只能是provisional／simulated；若真實binary不接受`UserPromptExpansion`或既定failure semantics，停止並返回最早受影響的Requirement／Specification／Ticket revision，不得靜默提高最低版本或保留失效evidence。
- Ticket編號是穩定識別，不代表執行順序。2026-09-07核准的provisional foundation順序為Ticket 1 → Ticket 2 → Tickets 4、5；Ticket 3可在取得authenticated environment後執行，但最晚必須在Ticket 9整合freeze與Ticket 10 local completion前通過。
- General 與 Claude 5 profiles 的行為 gate 必須先完成；context reduction 不能抵銷任何行為失敗。
- Finding 回到最早擁有該 source／contract 的 Ticket 修正、重驗與重審，不在後續 integration 或 evidence Ticket 暗改。
- `README.md` 只依現有 English／繁中／日本語平行布局插入 Claude 資訊，不重構無關 Codex／Generic 內容。
- Completed `1.3.1` requirements、Specification、Ticket Plan、evidence、recorded hashes 與 frozen references 全部唯讀。
- 本 Plan 最多完成 local `1.4.0` candidate；所有 external publication mutations 均不在授權範圍。

## Ticket 1 — 建立官方 Claude Plugin 公開邊界

Status: Completed. Evidence: [Ticket 1 Implementation and corrections](../evidence/claude-code-adapter-1.4.0-ticket-1.md); prior accepted [final independent Acceptance Review](../evidence/claude-code-adapter-1.4.0-ticket-1-review-accepted.md); exact-host [Ticket 3 preflight blocker](../evidence/claude-code-adapter-1.4.0-ticket-3-preflight-blocker.md); accepted [Marketplace description TDD correction](../evidence/claude-code-adapter-1.4.0-ticket-1-marketplace-description-correction.md) and [fresh independent correction Review](../evidence/claude-code-adapter-1.4.0-ticket-1-marketplace-description-correction-review.md) (`Accepted - no actionable findings`). Earlier initial and closure Reviews remain linked from the original implementation evidence.

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。Marketplace source、manifest、公開 Skill 數量與 reviewer 權限都是 supply-chain／安全邊界；加入測試會增加中等工作時間，但能持續拒絕錯誤 source、mutable ref、多餘 command 或 reviewer write surface。不加測試會降低公開安裝與 discovery 的驗證信心。

### Outcome and acceptance coverage

Repository 具有 provider-separated Claude Marketplace、canonical Plugin manifest、恰好兩個 profile-neutral public Skill bootstraps，以及只有讀取能力的 reviewer component；它們的 identity、version、namespaced entries 與 inventories 可被獨立驗證，且 bare alias 不被產品承諾。

主要覆蓋 Specification acceptance criteria 2、4、5、criterion 14 的 reviewer static boundary，以及 criterion 30 的 excluded-component boundary。

### Scope and boundaries

In scope:

- 建立 `.claude-plugin/marketplace.json` 與 Claude 專用 validator boundary，固定 exact fields、owner、tag-pinned `git-subdir` source、`strict` 與 `defaultEnabled`。
- 建立 canonical `.claude-plugin/plugin.json`，只使用官方 default component directories 與 approved authored fields。
- 建立兩個 public Skills；兩者只接受 route envelope、inherit active model、只能由使用者叫用，沒有第三個 public component。
- 建立 `agents/ask-then-do-it-reviewer.md` 的 read-only frontmatter與完整檢查責任：Approved requirements、Specification、Ticket mode、diff、tests、raw evidence及十二個Core Architecture and Refactoring Lenses；工具只允許 `Read`、`Grep`、`Glob`。
- Claude 與 Codex Marketplace schema、validator、source path、metadata 與 package exclusion保持分離。

Out of scope: Router/state、完整 profiles、behavior/equivalence fixtures、context measurement、user docs、release builder、generated packages 與真實 host validation。

### Dependencies and ownership

Dependencies: Approved Specification與已同步 Knowledge Base；無 implementation Ticket dependency。Ticket 3與Ticket 2都直接消費Ticket 1 boundary；Ticket 2在live host contract尚未完成時必須把相關假設標為provisional。

Likely ownership: `.claude-plugin/marketplace.json`、`adapters/claude-code/plugin/ask-then-do-it/.claude-plugin/plugin.json`、兩個 `skills/*/SKILL.md`、`agents/ask-then-do-it-reviewer.md`、Claude-specific marketplace/plugin validator，以及 focused `tests/claude/` contract tests。

### TDD approach

First Red: 先讓 focused tests 因 Claude catalog／manifest／兩 Skills／reviewer不存在而失敗，並包含wrong source/ref、Codex-only fields、extra Skill、side-effect reviewer tools，以及漏掉requirements／Specification／Ticket mode／diff／tests／raw evidence／任一十二個architecture lenses的negative cases。

Focused Green: 加入最小官方 Plugin structure、兩個 fail-closed bootstraps及read-only reviewer，使exact schema、identity、inventory與authority checks通過。

Broader verification: JSON/frontmatter parsing、Claude-specific validator、Codex Marketplace regression、secret/local-path scan、relative component resolution與`git diff --check`；真實Claude native validation留給Ticket 3。

### Direct approach

只建立上述結構，使用JSON/frontmatter parse、人工exact-field／inventory／path inspection及可用時的native validator，不新增或執行behavioral tests。自動拒絕錯誤source/ref、多餘components與reviewer權限漂移的證據會不可用，驗證信心較低。

### Completion and parallel safety

Complete when provider boundaries、兩個canonical entries、fail-closed bootstraps與read-only reviewer contract一致，reviewer完整檢查清單可追溯，且沒有冒稱真實`2.1.251`已驗證。

Parallel safety: **No**。這是所有Claude runtime與host validation共用的最小基礎，先完成並Review可避免下游同時改manifest、Skills或agent。

## Ticket 2 — 實作安全的 model router 與 session state

Status: Completed. Evidence: [Ticket 2 Implementation and corrections](../evidence/claude-code-adapter-1.4.0-ticket-2.md); accepted [fresh independent Review after tenth corrections](../evidence/claude-code-adapter-1.4.0-ticket-2-review-after-tenth-corrections.md) (`Accepted - no actionable findings`).

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。這是包含untrusted input、atomic file replacement、跨session隔離、model switch race與多種failure state的高風險runtime。測試會增加高工作量；不加測試會讓transition、race、安全與污染防護無法取得Approved Specification要求的deterministic behavioral evidence。

### Outcome and acceptance coverage

兩個public entries可經四個官方hooks取得same-session route envelope；exact model mapping、operation binding、`ready`／`pending`／`indeterminate` lifecycle、manual fallback與PostModelSwitch best-effort boundary全部可執行，且不切換model、不洩漏raw session ID或prompt。

主要覆蓋 acceptance criteria 6–10，以及 criterion 22 的automated path/event/state/failure部分。

### Scope and boundaries

In scope:

- 建立 `hooks/hooks.json`、零第三方dependency的Node.js `22+` router與release-owned exact model mapping。
- 為exact model mapping保存每個canonical ID的Anthropic官方來源、查核日期與fixture trace，並讓後續release evidence可重算來源快照；未列出的future/custom ID仍為unknown。
- 實作 `SessionStart`、`PreModelSwitch`、`PostModelSwitch`、`UserPromptExpansion` synchronous command actions。
- 從每個hook自己的stdin驗證／hash `session_id`，只在`${CLAUDE_PLUGIN_DATA}/routing/v1/sessions/`做atomic same-directory state replacement。
- 完整route table、operation binding、monotonic generation、startup/resume/fork/clear/compact、30-day cleanup與cross-session isolation。
- Handler-started failures形成bounded exit-0 failure envelope；只保留兩條approved explicit `-5` manual fallback路徑。
- 覆蓋Windows／macOS／Linux path separator、spaces、unsafe symlink/path、invalid JSON/schema/type/transition與race fixtures。

Out of scope: 真實Claude Code binary觀察、General／Claude 5 workflow modules、paired conformance、context proxy、docs與release integration。

### Dependencies and ownership

Dependencies: Ticket 1完成並通過Review，以及2026-09-07核准的provisional sequencing correction。Ticket 3未完成不阻止本Ticket，但所有exact `2.1.251` command identity、`additionalContext`與failure semantics假設必須集中、fail closed並標為尚待Ticket 3確認；不得宣稱live verified。

Likely ownership: Claude Plugin的`hooks/hooks.json`、`scripts/router.mjs`、`config/model-classifications.json`、兩個bootstrap的最小route-envelope integration、router fixtures與focused `tests/claude/` router/state tests。

### TDD approach

First Red: 以Approved Specification、官方hook contract、完整route/failure table及兩個不同session的injected events建立明確標示`simulated`的失敗測試，先證明目前沒有production matcher、可信classification、atomic state或cross-session protection；exact-host-specific expectations保留單一provisional boundary，等待Ticket 3確認。

Focused Green: 依序完成hash-derived ownership、exact classification、state machine、route envelope與operation binding，再加入Pre/Post switch、lifecycle、cleanup及failure handling。

Broader verification: 全部router fixtures、concurrent/atomic replacement simulations、secret/raw-ID/path scans、both-entry bootstrap integration、Node syntax，以及Tickets 1、3 Plugin／host-contract regressions。

### Direct approach

以靜態state-machine trace、Node syntax、人工stdin/output samples與filesystem inspection實作，不新增或執行behavioral tests。Atomicity、跨session隔離、race、failure transition與unsafe-input rejection無法被確定性證明，因此無法完成現行Approved Specification，必須先修訂規格或改選加入測試。

### Completion and parallel safety

Complete when所有deterministic route/state/security scenarios符合Specification，Pre failure不阻止model switch，Post commit後next-permitted-entry guarantee與commit前best-effort window清楚可觀察，且exact model mapping的官方來源與查核日期完整可追溯。

Parallel safety: **No**。它修改兩個shared Skills與單一router/state contract，並成為Tickets 4、5的直接輸入；Ticket 3日後若推翻provisional host assumptions，本Ticket與所有dependent evidence都必須重開。

## Ticket 3 — 驗證 exact Claude Code 2.1.251 host contract

Status: Approved

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。官方文件沒有標示`UserPromptExpansion`首次支援版本；只有真實`2.1.251` fixture能證明本產品最低版本成立。測試與乾淨環境準備會增加高工作量；不加入會留下release-blocking assumption。依2026-09-07 sequencing correction，這個assumption不再阻止provisional router/profile implementation，但仍阻止local `1.4.0`完成。

### Outcome and acceptance coverage

Exact Claude Code `2.1.251` binary對canonical Plugin與repository Marketplace通過strict validation；兩個namespaced invocations觸發實測command identity、收到route `additionalContext`，且Node unavailable／nonzero／exit `2`／timeout semantics有raw observations。任何不符都fail fast回Requirement／Specification。

主要覆蓋 acceptance criterion 3、criterion 4的host discovery部分，以及criterion 22的exact-binary hard gate；Ticket 10會對frozen final candidate重跑。

### Scope and boundaries

In scope:

- 在乾淨隔離環境保存binary來源、exact version、OS／surface、Node version與執行日期。
- 建立只供preflight的isolated compatibility Plugin/hook fixture：重用Ticket 1的兩個target Skill names，使用最小marker command產生bounded test route context；它不是production router或consumer package內容。
- 對Plugin root與Marketplace root執行`claude plugin validate <path> --strict`並要求exit `0`、無warning。
- 實際叫用兩個namespaced entries，記錄精確`UserPromptExpansion.command_name`、plugin source與route envelope可見性。
- 記錄host是否顯示每個public Skill的bare alias；只保存observed state，不把存在或不存在提升為產品保證。
- 觀察expansion command在Node missing、nonzero、exit `2`及timeout時的host結果；保存scrubbed raw evidence。
- 將實測command identity與host semantics交給Ticket 2確認或修正provisional production matcher；若host contract本身不成立，停止並返回最早受影響的Requirement／Specification／Ticket，撤銷失效implementation evidence，不能完成local `1.4.0`。

Out of scope: 把partial Plugin冒稱完整workflow、提高minimum、使用較新binary替代exact `2.1.251`、General／Claude 5 profile內容、完整八步live smoke或external publication。

### Dependencies and ownership

Dependencies: Ticket 1及其Review完成；需要可用的exact `2.1.251` authenticated clean session。Binary與隔離config已存在，但尚未授權或取得authenticated model session，因此live observations維持`unverified`；這不再阻止provisional Tickets 2、4、5，但仍阻止Ticket 9 integration freeze與local completion。

Likely ownership: Isolated test-only compatibility Plugin/hook fixture、Claude host-contract harness、scrubbed Ticket evidence，以及由實測固定的command-identity／failure-semantics fixtures。Production router與matcher完全由Ticket 2擁有。

### TDD approach

First Red: Host compatibility ledger初始為`unverified`，gate必須拒絕缺binary、wrong version、warning、未觸發command或缺route context的結果。

Focused Green: 以isolated preflight fixture在exact binary上逐項取得strict-validation、兩entry identity、additional context與failure-semantics observations，直到ledger全部passed。

Broader verification: 重跑Ticket 1 focused suite，核對raw evidence scrub、host/runtime版本與captured fixtures一致，並由獨立Review確認test-only fixture沒有被冒充production Plugin、simulated evidence也沒有被冒充final live smoke。

### Direct approach

只能查看版本與官方文件，不能執行behavioral host fixtures。這無法證明`UserPromptExpansion`與failure semantics，故不能完成本Ticket或解除Approved Specification hard gate。

### Completion and parallel safety

Complete whenexact `2.1.251`的所有hard-gate observations通過並可追溯，且bare alias的實際observed state已記錄但未被寫成保證；若任一contract不成立，本Ticket以revision handoff結束而不是繼續實作。

Parallel safety: **No**。這是local integration freeze與completion之前的fail-fast gate；可在Ticket 2與profiles provisional implementation期間等待authenticated environment，但執行與整合必須串行。不符時須修正最早受影響的Ticket或返回Requirement／Specification revision，所有dependent evidence重驗。

## Ticket 4 — 交付 General profile 的完整工作流程

Status: Approved

Progress (2026-09-09): 本次指令與測試修正已通過[獨立複查](../evidence/claude-code-adapter-1.4.0-ticket-4-review-after-third-correction.md)及[整合驗證](../evidence/claude-code-adapter-1.4.0-profile-correction-integration.md)。仍缺 Claude 實際執行 30 情境的觀察，Ticket 尚未完成；靜態文字／決策表測試不取代此門檻。

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。General profile承擔Full／Lite、Config、安裝生命週期、Review與全部Core gates；加入測試會增加高工作量，但能逐情境證明沒有漏核准、安全或失敗邊界。不加測試只能靜態比對文字，無法證明30個mandatory scenarios全部成立。

### Outcome and acceptance coverage

Known supported non-Claude-5與automatic unknown routes可只載入General profile，完成Full／Lite與安全lifecycle guidance；全部十個stage modules、Config precedence、reviewer downgrade及30個scenario的General結果可被驗證。

主要覆蓋 acceptance criteria 11、12、14–18的General部分，並提供criteria 6–10的General consumer proof。

### Scope and boundaries

In scope:

- 建立`profiles/general/`恰好十個approved stage modules。
- 映射30條Core rules與30個Claude behavior scenarios，不建立額外public commands。
- 保留capability honesty、Full／Lite resolution、requirements／KB／Specification／Plan gates、TDD/direct、Review及architecture contracts。
- 實作Claude-specific user/project Config read-only precedence、invalid fail-closed、no settings/Codex Config behavior。
- 覆蓋status/install/update/remove/ZIP guidance matrix與reviewer可用／不可用／conversation-only降級。

Out of scope: Claude 5 modules、paired cross-profile claim、50% context measurement、localized docs、release identity與generated packages。

### Dependencies and ownership

Dependencies: Ticket 2 provisional production router完成並通過Review；Ticket 3可仍`unverified`，但本Ticket及其host-dependent evidence不得稱live verified或release-final。

Likely ownership: `profiles/general/`十個modules、General-only scenario fixtures/tests與Ticket evidence；不修改Ticket 1 reviewer、Ticket 2 router或Claude 5 files。

### TDD approach

First Red: 用General route執行固定30-scenario inventory，先得到missing modules／gates／outcomes的有效失敗。

Focused Green: 逐stage加入最小General instructions，先讓對應scenario通過，再補齊Config、lifecycle與Review downgrade branches。

Broader verification: General全部30 scenarios、Core mapping、router integration、Full／Lite、no-model-override、no-cross-profile-load及Ticket 1–3 regressions。

### Direct approach

只以逐條Core trace、manual scenario checklist與frontmatter/module inventory檢查，不新增或執行behavioral tests。模型在30個scenarios是否真正遵守所有gates無法證明，不能完成現行Specification。

### Completion and parallel safety

Complete whenGeneral profile恰有十個modules、每條Core rule可追溯、General的30 scenarios全數通過且Review無未解finding。

Parallel safety: **Yes after Ticket 2**，可與Ticket 5在分離檔案與focused test ownership下平行；Ticket 8仍等待Ticket 3。Shared full-suite與Reviews仍串行，Ticket 3差異會重開受影響項目。

## Ticket 5 — 交付 Claude 5-optimized profile 的完整工作流程

Status: Approved

Progress (2026-09-09): 本次指令與測試修正已通過[獨立複查](../evidence/claude-code-adapter-1.4.0-ticket-5-review-after-third-correction.md)及[整合驗證](../evidence/claude-code-adapter-1.4.0-profile-correction-integration.md)。仍缺 Claude 實際執行 30 情境的觀察，Ticket 尚未完成；不得據此宣稱等價或達成 context reduction。

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。Optimized profile最容易因精簡文字而漏掉核准、安全或evidence gate。測試會增加高工作量；不加測試只能看到「比較短」，不能證明它仍完整遵守30條Core rules與所有host-specific outcomes。

### Outcome and acceptance coverage

Known Claude 5與allowed explicit-unknown/manual routes可只載入Claude 5 profile；恰好十個progressive-disclosure modules保留全部mandatory behavior，不載入或服從General modules。

主要覆蓋 acceptance criteria 7、11、12、14–18的Claude 5部分，並提供criteria 6–10的optimized consumer proof。

### Scope and boundaries

In scope:

- 建立`profiles/claude-5/`恰好十個approved stage modules。
- 以較短bootstrap／引用／按需載入保留30條Core rules與30個Claude behavior scenarios。
- 覆蓋known 5、supported non-5改General、unsupported stop、unknown explicit選擇與兩條Node manual fallback disclosures。
- 保留Full／Lite、Config、reviewer downgrade、install/update/remove/ZIP及evidence boundaries。
- 禁止cross-load General、model override、隱藏command或用context目標弱化behavior。

Out of scope: 修改General、宣告paired equivalence、正式50%計算、localized docs與release integration。

### Dependencies and ownership

Dependencies: Ticket 2 provisional production router完成並通過Review；Ticket 3可仍`unverified`，但本Ticket及其host-dependent evidence不得稱live verified或release-final。

Likely ownership: `profiles/claude-5/`十個modules、optimized-only scenario fixtures/tests與Ticket evidence；不修改General、shared conformance、router或docs。

### TDD approach

First Red: 用optimized route跑固定30 scenarios，先證明缺modules／gates／failure outcomes，並加入wrong-profile load與silent model-switch negative cases。

Focused Green: 逐stage加入最短且可執行的instructions，在每個behavior gate通過後才進一步精簡。

Broader verification: Optimized全部30 scenarios、Core trace、explicit `-5` routing、Config／lifecycle／Review branches、no-General-load與Tickets 1–3 regressions。

### Direct approach

只做靜態rule trace、module inventory與人工文字比較，不新增或執行behavioral tests。缺少mandatory behavior evidence，因此不能因文字較短就完成本Ticket或進入context gate。

### Completion and parallel safety

Complete whenoptimized profile恰有十個modules、30 scenarios全數通過、沒有behavior exemption或cross-profile load，且Review無未解finding。

Parallel safety: **Yes after Ticket 2**，可與Ticket 4平行；Ticket 8仍等待Ticket 3。本Ticket只擁有Claude 5 files及其focused fixtures，Ticket 3差異會重開受影響項目。

## Ticket 6 — 證明雙 profile 等價、authority precedence 與 conformance

Status: Approved

Progress (2026-09-09 offline): 離線工具、staged conformance 與 86 組未執行驗收套件已建立；獨立複查的 paired input／operation span 修正已完成，實際模型 gate 仍未執行。詳見 [Ticket 6 離線證據](../evidence/claude-code-adapter-1.4.0-ticket-6-offline.md) 與[整合紀錄](../evidence/claude-code-adapter-1.4.0-offline-integration.md)。完整 Ticket 尚未完成。

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。這張Ticket驗證「精簡但不減功能」的核心主張，包括雙向連續invocation與12個paired cases。測試會增加高工作量；不加入就沒有可稽核的behavior equivalence，只剩主觀文字審查。

### Outcome and acceptance coverage

Claude release-target conformance contract涵蓋全部30條Core rules與三層capability evidence；兩profiles各自30 scenarios為100%，12個相同環境的fresh-session paired cases結果等價，同session General→Claude 5與Claude 5→General都遵守最新operation authority。Target conformance先以staged fixture驗證，待Ticket 9與全部current identities一同啟用。

主要覆蓋 acceptance criteria 8、11–14。

### Scope and boundaries

In scope:

- 建立provider-specific `1.4.0` target conformance contract／staged fixture與rule/scenario mapping；內容對應最終`adapters/claude-code/conformance.yaml`，但在Ticket 9 lockstep升級Core／Codex／Generic之前不得提前放置會使current shared validator版本衝突的active manifest。
- 建立共享expected-outcome harness，重新驗證兩profiles各30 scenarios、不可skip／partial／exemption。
- 執行12個paired fresh-session cases，保存相同model、effort、tools、fixture、inputs與逐outcome結果。
- 驗證同session雙向profile authority、舊Skill文字只作歷史context；無法證明時要求`/clear`／new session。
- 驗證independent／non-independent／limited-evidence Review及Lite compact Review分流。

Out of scope: 用風格差異判失敗、修改router或profiles以隱藏finding、計算50% context、docs／packages，以及提前啟用canonical Claude conformance或current `1.4.0` identity。

### Dependencies and ownership

Dependencies: Tickets 4、5及各自Reviews完成。

Likely ownership: Claude target conformance staged fixture／mapping、provider-specific target validator、shared profile-equivalence harness、paired/fresh-session fixtures與Ticket evidence。Canonical `adapters/claude-code/conformance.yaml`由Ticket 9在lockstep identity transition時產生；profile defect回Ticket 4或5修正、重驗與重審。

### TDD approach

First Red: 缺Claude target conformance fixture、paired results與雙向authority evidence時，provider-specific target gate明確失敗；current `1.3.1` shared conformance suite仍須保持Green。

Focused Green: 先使staged `1.4.0` target的30-rule static mapping在provider-specific gate中valid，再逐一讓30-scenario／12-paired／兩個directional authority cases通過既定observable outcomes，不弱化shared version validator。

Broader verification: 完整Claude behavior suite、staged target conformance validation、current `1.3.1` shared conformance regressions、Tickets 1–5 regression與raw result completeness／scrub checks；canonical `1.4.0` shared validation留給Ticket 9。

### Direct approach

只做static mapping與人工對讀，不新增或執行paired behavioral tests。這無法證明fresh-session outcomes或舊context authority，不能完成criteria 12–13。

### Completion and parallel safety

Complete whenstaged target static與全部behavior gates都是100% pass、raw evidence完整、current shared suite沒有因版本提前切換而失敗，且任何profile finding已回原Ticket關閉；canonical conformance啟用仍明確屬於Ticket 9。

Parallel safety: **No with Tickets 4–5**。它消費兩者的final reviewed behavior；完成profile freeze後可與仍在進行的Ticket 8並行。

## Ticket 7 — 建立 Claude 5 每情境 50% context proxy gate

Status: Approved

Progress (2026-09-09 offline): 離線 context 計算器與固定未執行模板已完成並通過獨立複查；正式量測與 50% 門檻尚未執行。詳見 [Ticket 7 離線證據](../evidence/claude-code-adapter-1.4.0-ticket-7-offline.md) 與[整合紀錄](../evidence/claude-code-adapter-1.4.0-offline-integration.md)。完整 Ticket 尚未完成。

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。Normalization、重複注入、reviewer context與每checkpoint threshold很容易因fixture或計算方式產生假通過。測試會增加高工作量；不加入就缺少deterministic、可重算且防不對稱排除的release evidence。

### Outcome and acceptance coverage

只有Ticket 6 behavior gate通過後，十個固定scenarios的每個`stage-ready`及Full Review `reviewer-ready` checkpoint才執行measurement；optimized在每一格都至少少50%，且raw paths、load order、hashes、bytes、proxy tokens與公式可重算。

主要覆蓋 acceptance criterion 21。

### Scope and boundaries

In scope:

- 建立Claude-specific context fixture、measurement tool與structured raw result。
- 固定UTF-8、NFC、whitespace collapse、trim、LF join、`ceil(bytes/4)`與integer pass relation。
- 計入實際Skill／listing／selected modules／route／hook／reviewer prompt及重複注入；只排除Specification允許項目。
- 每scenario／checkpoint獨立判定，禁止平均補償、asymmetric exclusion、padding General或把task text塞入optimized source。
- 確保behavior gate fail時measurement不得被視為release pass。

Out of scope: 把Claude `/context`、billing、cost或latency當release gate；直接修改profiles來掩蓋failure；Codex既有token-proxy algorithm變更。

### Dependencies and ownership

Dependencies: Ticket 6完成且兩profiles behavior已freeze。

Likely ownership: Claude context measurement script、`tests/release/fixtures/claude-context-proxy/`、focused release tests與raw result evidence。未達標依實際counted source回Ticket 1（public Skills／reviewer）、Ticket 2（route／hook output）或Ticket 5（optimized modules）修正；不得用padding General造假。重跑affected owning Ticket，若public／host boundary改變則重跑Ticket 3，並一律重跑Tickets 6、7。

### TDD approach

First Red: 先用missing fixture、asymmetric exclusions、wrong load order、rounding與未通過behavior gate的cases證明measurement會fail closed。

Focused Green: 實作固定normalization、inventory/hash ledger及每checkpoint integer threshold，產出可重算結果。

Broader verification: Determinism、source mutation／padding／omission negative cases、reviewer-ready counting、existing workflow-token-proxy regression與evidence scrub。

### Direct approach

只做一次性人工bytes/token估算，不新增或執行behavioral tests。缺少反作弊、mutation rejection與deterministic regression，不能完成Specification的50% release gate。

### Completion and parallel safety

Complete whenbehavior-first ordering成立、所有required格子各自pass、raw evidence可重算且Review無未解finding。

Parallel safety: **Yes with Ticket 8**，只讀frozen profiles並擁有獨立measurement files；若需改profile必須回Ticket 5，不能在本Ticket直接修改。

## Ticket 8 — 完成三語 Claude 文件並維持 README 布局

Status: Approved

Progress (2026-09-09 offline): 三語文件、保留 README 布局的入口與 dated official surface evidence 已完成並通過獨立複查；仍需實測後最終文案核對。詳見 [Ticket 8 離線證據](../evidence/claude-code-adapter-1.4.0-ticket-8-offline.md) 與[整合紀錄](../evidence/claude-code-adapter-1.4.0-offline-integration.md)。完整 Ticket 尚未完成。

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。三語語意、12個START-HERE、相對連結與README插入位置容易漂移。測試會增加中高工作量；不加入會降低layout preservation、翻譯等價與禁止錯誤`/doctor`／ZIP／版本聲明的驗證信心。

### Outcome and acceptance coverage

English／繁中／日本語使用者可從現有README與root START-HERE找到Claude；三語Claude guides、getting-started路徑與Plugin START-HERE一致說明三個版本、兩個entries、routing、Config、reviewer、user-scope lifecycle、platform與session-only ZIP，且不改壞現有布局。

主要覆蓋 acceptance criterion 24，以及criteria 16–18、22的user-facing disclosure部分。

### Scope and boundaries

In scope:

- 只在README三個平行區塊的對應位置插入Claude資訊，保留每語言現有section順序及無關內容。
- 更新三個root START-HERE與三個provider-neutral getting-started-simple guides的Claude入口。
- 新增三個完整`docs/guides/claude-code.*.md`與Claude Plugin三個簡短START-HERE。
- 清楚區分Claude model／Claude Code／Node、known unsupported／unknown／router failure、automatic／explicit `-5`、compatibility／live verified及Marketplace／ZIP。
- `/doctor`只可作optional Claude Code installation/config health check，不得宣稱會轉換或最佳化Skills。
- 查核並保存有日期的Anthropic官方feature evidence，逐一說明terminal CLI、VS Code與JetBrains對本規格所需local Plugin、Skill、Agent、hooks的支援狀態與任何surface差異；文件只宣稱evidence實際支持的範圍。

Out of scope: 重寫Codex／Generic guide owner、改workflow behavior、加入第三個command、建立自訂doctor、generated packages或external-publication claim。

### Dependencies and ownership

Dependencies: 起草需Ticket 3確認host command與hook terminology；通過後可與Tickets 4、5、6的focused work平行。完成明確依賴Ticket 6的behavior／authority contract freeze；Ticket 7不是文案依賴，可與Ticket 8最終semantic/evidence check平行。

Likely ownership: `README.md`、root `START-HERE.*.md`、`docs/guides/getting-started-simple.*.md`、新`docs/guides/claude-code.*.md`、Claude Plugin `START-HERE.*.md`、三surface dated official feature-evidence artifact與focused documentation/evidence tests。

### TDD approach

First Red: 先讓tests因缺Claude consumer choice、guides、12-page inventory、required distinctions、README placement，以及缺少／無日期／不完整的CLI、VS Code、JetBrains Plugin／Skill／Agent／hooks official feature evidence而失敗，並加入prohibited claims的negative checks。

Focused Green: 依現有三語layout做最小插入／新增，逐語滿足同一semantic checklist與link boundary。

Broader verification: 三語parity、all relative links、brevity、version/command exactness、README approved-diff boundary、12 source/package START-HERE expectations、三surface官方URLs／dates／feature matrix／difference completeness及existing documentation regressions。

### Direct approach

以三語人工checklist、link resolver、exact command search與README diff inspection完成，不新增或執行behavioral tests。自動layout／semantic drift與prohibited-claim rejection evidence會不可用，且無法完成Specification明定的12-page test contract。

### Completion and parallel safety

Complete when全部三語內容semantic-equivalent、README現有布局被保留、所有links有效，三個surfaces的dated official feature evidence與差異可追溯，且Review無未解finding。

Parallel safety: **Yes for drafting after Ticket 3**，可與Tickets 4–6 focused work平行；但完成必須等待Ticket 6，之後可與Ticket 7平行。文件與focused tests有獨立ownership，不得與Ticket 9同時改shared version/docs integration。

## Ticket 9 — 整合 lockstep 1.4.0 與三-family deterministic release

Status: Approved

Progress (2026-09-09 offline): 離線 builder、exact package／ZIP validation 與 byte-identical preview 已完成並通過獨立複查；current 1.3.1/default dist 保留，正式 lockstep activation 與 freeze 尚未進行。詳見 [Ticket 9 離線證據](../evidence/claude-code-adapter-1.4.0-ticket-9-offline.md) 與[整合紀錄](../evidence/claude-code-adapter-1.4.0-offline-integration.md)。完整 Ticket 尚未完成。

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。這張Ticket同時改版本identity、builder、三個packages／ZIP、checksums與歷史保護，是最高回歸風險之一。測試會增加高工作量；不加入會缺少reproducibility、inventory、rollback、provider isolation與historical immutability的持續證據。

### Outcome and acceptance coverage

Current Core、Codex、Generic、Claude與docs identity一致為`1.4.0`；builder以同一canonical Claude source產生Codex／Generic／Claude三個expanded families、三個ZIP與三筆SHA-256，Claude inventory exact且Marketplace excluded，Completed `1.3.1`歷史內容不變。

主要覆蓋 acceptance criteria 19、20、25–28、30，並提供criteria 2–24的package-facing integration proof。

### Scope and boundaries

In scope:

- 更新active current declarations至`1.4.0`，不盲目全域取代historical/fixture文字。
- 在同一lockstep transition更新Core、Codex與Generic conformance identities，並從Ticket 6 reviewed staged contract產生canonical `adapters/claude-code/conformance.yaml`；只有此時才要求shared validator對全部current `1.4.0` manifests通過。
- 擴充`release/release.json`與builder的Claude family/source/inventory/archive/checks，managed outputs為`codex`、`generic`、`claude`、`checksums.sha256`。
- 保持Marketplace runtime／canonical source／expanded／ZIP content equivalence及legal-file policy。
- 重建default `dist/`，證明three-family inventories、兩次isolated builds byte-reproducible、ZIP exact bytes、deterministic ordering與checksums。
- 保持staging、collision、WinError 5 retry、rollback、incomplete recovery、removed-artifact、evidence與secret/path gates。
- 保護Codex／Generic observable behavior、package inventories與consumer dependencies；Node只屬於Claude。

Out of scope: 改profile behavior、修Ticket 1–8 finding、建立Completed final evidence、Git tag／push／Release／upload／activation／announcement。

### Dependencies and ownership

Dependencies: Tickets 1–8全部完成各自implementation與accepted Reviews；Claude sources與docs已freeze。

Likely ownership: `release/release.json`、`scripts/build_release.py`、current Core／Codex／Generic identities、canonical `adapters/claude-code/conformance.yaml`、release／Claude package validators、shared conformance tests、generated `dist/`與checksums。既有Codex validator維持provider owner；Claude schema使用separate dispatch/boundary。

### TDD approach

First Red: 先把integrated current contract切到`1.4.0`、canonical Claude conformance與three-family expectations，使目前two-family `1.3.1`狀態明確失敗，同時證明historical guards仍綠。

Focused Green: 加入最小Claude build/inventory/validation dispatch、同步active identities並透過builder重建managed outputs。

Broader verification: Full release/conformance/Claude suites、兩次isolated byte-reproducible builds、ZIP parity、checksums、transaction/recovery、history hashes、docs/package links、secret/path scans與`git diff --check`。

### Direct approach

只使用schema/native validation、兩次build、manual inventory/hash比較與diff inspection，不新增或執行behavioral tests。Mandatory rejection、recovery、reproducibility與historical-regression evidence不足，不能完成現行Specification。

### Completion and parallel safety

Complete whensource、expanded packages、archives、checksums與current identities一致，所有required gates通過，candidate bytes freeze但尚未宣稱Completed release。

Parallel safety: **No**。本Ticket唯一擁有shared versions、builder、release tests、`dist/`與checksums，並消費所有上游結果。

## Ticket 10 — 完成真實 smoke、最終 Review 與 local release evidence

Status: Approved

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。這是把source與packages升格為可信local candidate的最後硬閘門。測試與真實環境操作會增加最高工作量；不加入會缺少exact-binary、八步smoke、failure-gate與完整suite證據，不能建立Completed release evidence。

### Outcome and acceptance coverage

Frozen `1.4.0` candidate通過全部automated gates與exact `2.1.251`重驗，至少一個clean real Claude Code environment完成八步smoke；獨立Full Review、read-only architecture diagnosis、validation ledger與Completed local evidence如實區分observed／simulated／unavailable／not-authorized，且沒有external publication。

主要覆蓋 acceptance criteria 23、29、30，對criteria 3、22做final-candidate重驗，並提供criteria 1–28的最終proof。

### Scope and boundaries

In scope:

- 先證明missing／incomplete／wrong-version／failed host、context、live-smoke或required check evidence會被validator拒絕。
- 對frozen candidate串行執行complete automated suites、native validators、isolated builds、package/checksum/historical/safety gates。
- 在exact `2.1.251`重跑strict validation、兩entry `UserPromptExpansion` identity／context／failure semantics。
- 重驗final ledger包含Ticket 2 exact model mapping的官方來源／查核日期，以及Ticket 8對terminal CLI、VS Code、JetBrains之Plugin／Skill／Agent／hooks支援與差異的dated official evidence。
- 至少一個clean environment使用isolated、test-only、明確標示「非正式release」的local git/Marketplace fixture及exact candidate bytes，完成user-scope Marketplace install/status、two-entry discovery/routing與bare-alias observed state、model switch／authority、two sessions＋resume/compact、older test candidate update、remove/data disclosure/reinstall，以及exact ZIP `--plugin-dir` recovery；bare alias只記錄觀察，不作存在性保證，也不得要求先tag/push或把public transport稱為已驗證。
- 記錄exact OS／surface／Claude Code／Node／model／date；unavailable branches只標deterministic simulated。
- 執行fresh independent Full Review與release-milestone architecture diagnosis；finding回owning Ticket修正後重新freeze與重驗。
- 最後建立`1.4.0` validation ledger、release evidence及evidence-only closure。

Out of scope: 在evidence階段暗改source、接受skipped required gate、architecture refactor、public transport claim、tag、push、GitHub Release、asset upload、Marketplace activation、Community submission或announcement。

### Dependencies and ownership

Dependencies: Ticket 9及所有earlier Reviews完成，candidate bytes與source freeze；clean real Claude Code environment可用。

Likely ownership: Claude live-smoke ledger/results、`docs/evidence/ask-then-do-it-release-1.4.0.{md,json}`、final Review、architecture diagnosis與closure artifacts。任何product defect回最早owning Ticket。

### TDD approach

First Red: Evidence validator必須拒絕尚不存在／不完整／failed的actual `1.4.0` ledger、缺exact-binary或缺live-smoke的Completed claim。

Focused Green: 只在每個raw observation真實通過後填入ledger/evidence，使gate逐項轉綠；不得以手寫`passed`取代command/result。

Broader verification: 完整repository suite、native Plugin/Marketplace validation、all Claude behavior/context gates、three-family reproducibility／ZIP／checksums、安全／歷史掃描、eight-step smoke、independent Review、architecture diagnosis與final evidence validation。

### Direct approach

不新增或執行behavioral tests，只能做靜態／build／hash檢查；不得執行required host/live behavior或把缺失標為passed。因此不能建立符合Approved Specification的Completed evidence，Plan必須回Specification revision或改選加入測試。

### Completion and parallel safety

Complete when全部required raw evidence、Reviews與diagnosis accepted，local candidate可重現且誠實標為未發布；任何bytes變更都使affected evidence失效並重跑。

Parallel safety: **No**。它只消費frozen final candidate並整合全部release observations。

## Dependency order and proposed parallel groups

1. Sequential provisional foundation: Ticket 1 → Ticket 2（production router；host-dependent assumptions標為provisional）。
2. After Ticket 2 passes: Tickets 4、5可在明確file/test ownership下平行。
3. Ticket 6 waits for Tickets 4、5；Ticket 8仍等待Ticket 3後才能起草，且不能在behavior freeze前完成。
4. Ticket 3可在authenticated exact-host environment可用時執行，但最晚必須在Ticket 9 integration freeze前通過；不符會返回最早受影響的Requirement、Specification或Ticket artifact，並使dependent implementation evidence失效。
5. Tickets 7與Ticket 8 final semantic/evidence check都等待Ticket 6；兩者可彼此平行，但任何host-dependent final claim也等待Ticket 3。
6. Sequential integration: Ticket 9 waits forTickets 1–8、Ticket 3 exact-host gate及各自accepted Reviews。
7. Sequential completion: Ticket 10 waits forTicket 9 frozen candidate。

共用工作樹中的full-suite、native host validation、Reviews、`dist/` generation與final evidence一律串行；平行安全只適用明確分離的source與focused fixtures。

## Test-choice gate

| Ticket | Recommendation | User choice | Internal mode |
| --- | --- | --- | --- |
| 1 | Add tests — medium supply-chain/discovery risk | Add tests | `tdd` |
| 2 | Add tests — high runtime/state/security risk | Add tests | `tdd` |
| 3 | Add tests — release-blocking exact-host contract | Add tests | `tdd` |
| 4 | Add tests — mandatory General behavior evidence | Add tests | `tdd` |
| 5 | Add tests — mandatory optimized behavior evidence | Add tests | `tdd` |
| 6 | Add tests — mandatory equivalence/conformance evidence | Add tests | `tdd` |
| 7 | Add tests — mandatory deterministic context gate | Add tests | `tdd` |
| 8 | Add tests — medium-high localization/layout risk | Add tests | `tdd` |
| 9 | Add tests — high release/inventory/history risk | Add tests | `tdd` |
| 10 | Add tests — mandatory live/release evidence | Add tests | `tdd` |

使用者於 2026-09-05 明確回覆「全部加入」；十張 Ticket 全部選擇 Add tests 並映射為 `tdd`。同日，使用者在完整Plan與mapping展示後明確回覆「核准」。任何choice變更都使Plan回到Draft並需重新核准。
