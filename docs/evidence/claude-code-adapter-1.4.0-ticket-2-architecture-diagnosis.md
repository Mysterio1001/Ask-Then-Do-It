# Claude Code Adapter 1.4.0 — Ticket 2 Architecture Diagnosis

Artifact type: `Architecture Improvement Report`

Artifact ID: `claude-code-adapter-1-4-0-ticket-2-architecture-diagnosis`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Status: `Draft`

Inputs: Approved Claude Code Adapter 1.4.0 Specification、Approved Ticket Plan 的 Ticket 2、Project Knowledge Base、Ticket 2 implementation evidence、initial independent Review、目前凍結的 `router.mjs`、直接 `hooks/config/tests` boundaries 與 Claude Plugin validator。

Assumptions: 本診斷以 2026-09-07 凍結的 `router.mjs` 為準；該檔為 1,482 行、44,026 bytes，SHA-256 `2F81025993A27327EFFEE4F6E0EBD76B40D5EBDE74D8D93E528E484E75DD5901`。Project 與 user Ask Then Do It Config 均不存在，因此 top-level mode 依契約解析為 Full；能力為 `multi_agent`。Initial Review 的 lock、bounded-read、unsupported disclosure 與 source-trace findings 是本次架構診斷的歷史觸發點，不自動視為目前仍存在的 defects。

Deferred: 任何 production/test/config refactor、實際刪除、檔案移動、module split、bundling、package inventory 變更、Ticket 2 correction acceptance、authenticated Claude Code host verification、Ticket 3、後續 profiles、release integration 與 external publication。

Handoff: 本報告只提供唯讀診斷。若使用者接受任一改善方向，下一步必須回到 `$write-spec` 定義邊界與 observable invariants，再由 `$plan-tickets` 建立垂直、可驗證的票券；不得由本報告直接進行實作或重構。

Approval: `Not requested`。本 Draft 未被接受；接受本報告也不等於授權拆分、刪除或 refactor。

## 1. Analysis scope and limitations

範圍限於下列 runtime 與直接邊界：

- `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs`
- `adapters/claude-code/plugin/ask-then-do-it/hooks/hooks.json`
- `adapters/claude-code/plugin/ask-then-do-it/config/model-classifications.json`
- `scripts/validate_claude_plugin.py` 中直接固定 hooks、mapping、router contract 的部分
- `tests/claude/test_router_contract.py`
- `tests/claude/test_router_state.py`
- `tests/claude/test_router_security.py`
- `tests/claude/test_router_review_regressions.py`
- `tests/claude/test_router_schema_validation.py`
- `tests/claude/test_model_classification_evidence.py`
- `tests/claude/test_public_plugin_contract.py`

本 context 只做 source、configuration、tests、evidence 與 dependency trace 閱讀，沒有執行測試、validator 或真實 Claude session，也沒有修改 runtime、tests、Config 或 Project Knowledge Base。所有 deletion 都是 `ARCH-DELETE-001` 安全模擬；沒有刪除任何檔案。

Initial Review 所列的三個 runtime P2 與一個 evidence P3，在目前快照可看到對應 correction：

- mapping、state 與 lock record 都經 bounded reader 讀取，且 growing-file case 有專屬 helper/test boundary。
- lock 現在包含 owner token、PID、lease 與 grace；只有過期且可確認 owner process 已死亡時才進入 token-aware recovery，PreModelSwitch 則使用 non-waiting lock policy。
- resume/compact 保留 operation 時會依目前 classification 補上 unsupported disclosure。
- model evidence tests 已包含錯誤 source reference 與刪除 supporting row 的 mutation cases。

因此本報告不重複把這些 correction targets 列為 current defects。它們仍是重要的架構證據：四種不同修正都集中改動同一 runtime module，說明 change-reason concentration 與 trust-boundary impact radius。

## 2. System architecture summary

目前的 runtime 是一個 dependency-free Node.js executable module；Claude hooks 以四個 action 呼叫同一個 entrypoint：

```text
hooks.json
  -> router.mjs main(action)
     -> bounded stdin + strict JSON/event validation
     -> exact model mapping gateway
     -> session-key derivation
     -> linked-path guard + bounded state I/O
     -> owned lock / stale-lock recovery + atomic write
     -> SessionStart / PreModelSwitch / PostModelSwitch / expansion handlers
     -> route envelope or lifecycle warning
```

| Responsibility | Current owner | Direct consumers / impact radius |
| --- | --- | --- |
| Hook invocation, matcher and host timeout | `hooks/hooks.json` | Claude Code host、Plugin validator、router contract tests |
| CLI action dispatch and failure translation | `router.mjs:1407` | All four hooks；錯誤會影響所有 runtime paths |
| Strict JSON parsing and event schema | `router.mjs:283`、`:412` | Hook stdin、mapping、state、lock record |
| Exact classification freeze | `config/model-classifications.json`、`router.mjs:560` | SessionStart、PostModelSwitch、all later public routing |
| Filesystem containment and bounded reads | `router.mjs:485`、`:623` | Mapping、state、lock inspection、cleanup |
| Locking, stale-owner recovery and atomic write | `router.mjs:676`–`:930` | All same-session lifecycle and public entry writes |
| State schema and lifecycle | `router.mjs:932`–`:1080` | Operation binding、switch ordering、cleanup、cross-session isolation |
| Route/envelope contract | `router.mjs:1082`–`:1167` | Two public Skills and model-visible disclosures |
| Four hook behaviors | `router.mjs:1169`–`:1383` | Session lifecycle、routing、model switching |
| Static anti-drift checks | `validate_claude_plugin.py:590`–`:734` | Hook inventory、mapping freeze、imports、Node gate、disclosure enums |
| Behavioral/security evidence | scoped `tests/claude/` files | Route table、state machine、lock races、unsafe input、mapping trace、Plugin boundary |

主要優點是單一 executable entrypoint、零第三方 runtime dependency、closed schemas、fail-closed behavior 與多層 deterministic gates。主要代價是 parser、domain contract、filesystem protocol、state machine、host orchestration與 output policy 全部共享同一 physical module 和 failure domain。

## 3. Deletion-analysis results

以下只描述「假設移除」的結果；沒有實際刪除授權。

| 模擬移除 | 直接失效 | 系統層影響 |
| --- | --- | --- |
| 整個 `router.mjs` | `hooks.json` 的四類 handlers 都找不到 executable；Plugin validator 的 scripts inventory、required text、Node gate與import checks失敗；router contract/state/security tests失敗 | Session model state、classification、operation binding與route envelope全數消失。兩個 public Skills只接受同次 valid envelope，因此正常入口 fail closed；這不會自動變成 approved explicit `-5` fallback |
| `hooks/hooks.json` | Claude Code不再自動呼叫四個 router actions；validator與public contract tests拒絕缺少hook inventory | Router即使仍可被人工執行，也不再是正式Plugin runtime path；same-invocation routing authority無法建立 |
| Strict parser／event validator | Duplicate keys、extra keys、錯誤型別與超限欄位可在trust boundary之前漏入；security mutation tests失去保護 | Mapping/state/handler收到未驗證 primitives，可能造成ownership、transition或output contract被繞過；這個 boundary不可直接刪除或以裸 `JSON.parse` 代換 |
| Exact mapping boundary（config、loader、semantic binding） | SessionStart與PostModelSwitch無法可靠把exact ID分類；mapping validator、digest gate與evidence tests失敗 | Known `<4.6` model可能被錯降為unknown compatibility，或Claude 5/general選錯profile；release-owned dated freeze與可追溯性消失 |
| State store／lock／atomic-write責任 | Hook handlers仍可被dispatch，但沒有same-session mutual exclusion、atomic replacement、owned recovery、state validation或30-day cleanup | Cross-session isolation、monotonic generation、pending/indeterminate switch、current-operation binding與commit後reroute guarantees無法成立 |
| Handler/lifecycle layer | 基礎parser與store仍存在，但四個events不再形成approved state transitions | Pre failure non-blocking、Post authoritative commit、resume/compact preservation及public route table都消失 |
| Envelope/output layer | Expansion無法輸出bounded framed route authority；switch/start warnings與continuation context消失 | Skills無法選擇profile或確認operation binding，應fail closed；handler-started failure的exit-0 envelope contract亦失效 |
| `validate_claude_plugin.py` 的router checks | Production bytes可能仍可執行，但hook timeout/matcher、mapping freeze、closed disclosure enum、built-in-only與Node minimum失去preflight gate | 變更可在沒有package-level deterministic rejection的情況下漂移，錯誤可能延後到runtime或release stage才出現 |
| Direct router tests | Production可能仍可執行，但route table、session isolation、races、bounded I/O、lock ownership/recovery、symlink/input rejection與source trace失去可重算證據 | 小型改動的impact radius無法被局部證明；Large Module造成的review成本與回歸風險顯著增加 |

Deletion trace顯示 router 不是一個可任意移除的wrapper；它是多個安全與行為邊界的聚合點。可改善的是責任邊界，不是刪除功能。

## 4. Twelve-lens results

| # | Lens | Outcome | Current evidence |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `no-finding` | Hooks、router、validator與tests會重述action、timeout、mapping和disclosure contract，但目前值一致，且semantic hash、closed enums與mutation tests顯示多數是刻意的cross-runtime defense-in-depth。不能只為去重而讓validator依賴production implementation。 |
| 2 | Long Function | `no-finding` | `parseJsonStrict`、`validateState`與`main`較長，但各自仍有單一可描述責任；目前高風險來自module-wide ownership，而非某一函式內無法追蹤的流程。 |
| 3 | Large Module or Class | `finding` | `router.mjs` 已達1,482行／44,026 bytes，同時擁有parser、host schemas、mapping、path security、bounded I/O、lock recovery、state validation、cleanup、handlers與output contracts。 |
| 4 | Long Parameter List | `no-finding` | Handler多為`event/pluginData/mapping`三個inputs；lock API與envelope helpers亦未出現長參數介面。 |
| 5 | Data Clumps | `finding` | `entry/classification/profile`三元組同時存在於`READY_OPERATION_TUPLES`、persisted operation、state validation與`successEnvelope`參數；operation已擁有相同欄位，envelope仍平行接收另一份values，形成可分歧的route-decision資料群。 |
| 6 | Primitive Obsession | `finding` | Route/state/action/error等domain values主要由裸字串與Set管理，合法route decision又以`"entry|classification|profile"`拼接。Closed validators已降低current correctness風險，但新增entry/profile時需同步多個primitive集合。 |
| 7 | Feature Envy | `not-applicable` | 此範圍是functional/procedural module，沒有method長期操控另一domain object internals的class ownership問題。 |
| 8 | Divergent Change | `finding` | Claude hook payload、model evidence freeze、filesystem safety、locking、state lifecycle、route table與model-visible envelope任一改動都會修改同一module。Initial Review後四類corrections再次證明這些獨立change reasons共享一個檔案。 |
| 9 | Shotgun Surgery | `finding` | Hook contract變更通常須同步`hooks.json`、router、Python validator與contract tests；mapping變更又須同步config、semantic digest、validator constants、source trace/snapshots與tests。這是受控但真實的跨artifact fan-out。 |
| 10 | Message Chains | `not-applicable` | Runtime主要使用直接函式呼叫與plain records，沒有長object-navigation chain向caller洩漏深層結構。 |
| 11 | Leaky Abstraction | `finding` | `main`必須知道PreModelSwitch不能等待，直接傳入`retryCount: 0, allowReclaim: false`；default lock retry budget又必須保持在`hooks.json` timeout內。Host deadline與low-level lock策略分散在不同層，先前5秒timeout finding正是此耦合的實際表現。Current correction已降低風險，但ownership boundary仍未被明確封裝。 |
| 12 | Shallow Module | `no-finding` | 四個CLI actions背後確實隱藏大量classification、state、security與failure policy；router不是只轉呼叫的薄wrapper。未來拆分也不應製造只增加跳轉成本的微型modules。 |

## 5. Finding evidence, impact, and confidence

### A1 — Router是Large Module並承擔Divergent Change

Evidence: Current snapshot為1,482行／44,026 bytes。Lines `8`–`179`定義host/domain/schema政策；`:283`–`:610`處理strict JSON與mapping；`:623`–`:930`處理path、lock與atomic write；`:932`–`:1080`處理state/cleanup；`:1082`–`:1383`處理operation、envelope與四個handlers；`:1407`起負責orchestration及所有failure translation。

Impact: 一個局部security或host-contract修正會讓整個runtime file進入review範圍；parser、state、filesystem與model-visible output共享同一merge/conflict與回歸半徑。單一入口仍有部署價值，但不要求所有責任都必須存在同一source module。

Confidence: `high`。

### A2 — Host deadline與lock policy之間存在Leaky Abstraction

Evidence: Host timeouts位於`hooks.json`（Pre為2秒，其餘為5秒）；router另有`LOCK_RETRY_COUNT = 100`、`LOCK_RETRY_MS = 10`，且`main`對Pre特別傳入non-waiting/reclaim-disabled options。Python validator驗exact hook timeouts，但目前沒有單一explicit action policy描述「每個action最多可花多少lock等待時間」及其與host timeout的關係。

Impact: Current implementation已把default nominal retry降到約1秒，且Pre不等待，所以Initial Review的實際timeout defect不再是current finding；然而未來單獨調整timeout、retry或recovery工作量仍可能重新產生host先終止process、來不及輸出failure envelope的問題。

Confidence: `high` for coupling；`medium` for future failure likelihood。

### A3 — Exact contract具有受控但高fan-out的Shotgun Surgery風險

Evidence: `hooks.json`的event/action/matcher/timeout由`validate_claude_plugin.py:607`–`:641`與router contract tests再次固定；mapping本體由router semantic SHA-256、Python validator常數、dated evidence trace/snapshots與model evidence tests共同固定。Public route/disclosure contract同時出現在router、two Skills、validator與tests。

Impact: 這些獨立gates是有價值的defense-in-depth，不能簡單合併成「production code驗自己」。但每次正式host或model catalog更新都需要識別完整impact set；漏改會fail closed，錯誤修改則可能產生大量非局部review工作。

Confidence: `high` for change fan-out；`low` for current correctness impact，因目前沒有觀察到drift。

### A4 — Route decision以平行primitives表達

Evidence: `entry/classification/profile`先被字串化於`READY_OPERATION_TUPLES`，再寫入`operationFor`建立的operation；`validateState`重新組合相同tuple，而`successEnvelope`同時接收operation及另外三個平行參數。現有caller從同一state計算這些值，但helper本身沒有驗證參數必然與operation欄位一致。

Impact: 增加新entry、classification或profile時，合法tuple、persisted operation與envelope projection可能分歧。Closed sets能使多數錯誤fail closed，卻也把一個domain concept分散成多個字串同步點。這是Data Clumps與Primitive Obsession的maintainability finding，不是current route defect。

Confidence: `medium-high`。

### A5 — Validator把implementation text暴露成外部架構約束

Evidence: `validate_claude_plugin.py:669`–`:734`會以source text count/regex檢查mapping hash constant、Set內容、imports、Node gate出現次數與相對順序；focused tests另直接import `readBoundedHandle`、`withSessionLock`等低階helper。

Impact: 即使observable hook behavior不變，單純改名、重排或抽取module也會破壞validator/tests。這種coupling目前能阻止危險drift，但若未來要演進內部結構，必須先把哪些implementation details真的是正式contract說清楚，不能把validator失敗當作任意改測試即可。

Confidence: `high`。

## 6. Prioritized improvement proposals

1. **先完成目前Ticket 2 correction Review，不在本輪重構。** Current safety corrections改動lock、bounded I/O、continuation disclosure與evidence trace；先以既定focused/full gates及fresh independent Review確認行為，避免architecture work混入correction evidence。
2. **以Specification定義穩定的內部責任邊界與dependency direction。** 建議未來形態為：single `router.mjs` composition root → hook handlers → `route contract`、`model classification gateway`、`session state store`；state store再唯一擁有path guard、bounded state I/O、lock/recovery、atomic replacement與cleanup。具體檔名、是否多檔或bundle必須由未來Specification決定。
3. **最先隔離state-store/lock boundary。** 這是untrusted filesystem、concurrency與host timeout相交的最高風險區。未來Ticket應保持observable state schema/path/exit/output完全不變，先建立characterization tests，再抽出窄介面，例如`readSession`、`updateSession`與`tryCleanupExpired`；handlers不應直接選`retryCount`或`allowReclaim`。
4. **把每個hook action的deadline policy變成可驗證contract。** 未來Specification需決定由action policy table、host timeout-derived validation或另一種方式表達budget；validator/tests必須證明router最壞等待小於host timeout，PreModelSwitch永不等待且不阻止model switch。不要在未定義clock、I/O與recovery budget前只改常數。
5. **建立單一`RouteDecision`／`BoundOperation` domain boundary。** Envelope應從validated decision/operation派生，不再另外傳入平行的entry/classification/profile primitives；這個邊界必須保留目前六個合法tuples與所有failure/unsupported behavior。
6. **分離pure domain contract，但保留獨立anti-drift gates。** Event/state/operation/envelope validation與mapping gateway可成為pure boundaries；Python validator仍應從外部驗證built artifact，而不是import production validator。若採canonical authored contract生成部分projection，必須保留至少一個independent semantic/mutation gate，並把source-text checks逐步改成明確的semantic artifact checks。
7. **以vertical Tickets逐步切分，不做一次性搬檔。** 建議順序為state-store/lock → route-decision與pure event/state/envelope contracts → classification gateway → handler/orchestration cleanup；每張Ticket都需同時證明both entries、four hooks、failure envelopes、operation binding與cross-session behavior沒有改變。

以上全是Draft proposals，不是implementation plan，也不授權新增modules、改validator inventory、改package bytes或刪除舊code。任何採用都必須回到未來`$write-spec`與`$plan-tickets`。

## 7. Potentially affected modules

| Proposal / finding | Potentially affected modules | Required protection |
| --- | --- | --- |
| A1 internal decomposition | `scripts/router.mjs`、Plugin scripts inventory、`validate_claude_plugin.py`、public Plugin/package contract tests | 保留單一official executable entrypoint、Node 22+、built-ins only、no network、same outputs |
| A2 deadline/lock ownership | `router.mjs` lock/orchestration、`hooks/hooks.json`、router state/review-regression tests、validator timeout checks | Pre non-blocking；all failure output在host timeout前完成；live/fresh/malformed lock不得誤回收 |
| A3 hook contract fan-out | `hooks/hooks.json`、router event/action dispatch、validator、router contract/public Plugin tests | Exact matcher、command identity、timeout與failure semantics維持fail closed |
| A3 mapping fan-out | `config/model-classifications.json`、router mapping gateway/digest、`validate_claude_plugin.py`、`validate_claude_model_evidence.py`、mapping fixtures/trace/tests | Exact-ID only、dated official source、unsupported不可降為unknown、independent semantic check |
| Pure contract extraction | router event/state/envelope helpers、two public Skills、router security/state/contract tests | Same-invocation envelope authority、closed codes、no raw session/prompt/path output |
| Route decision abstraction | `READY_OPERATION_TUPLES`、operation validation/creation、success envelope、route table tests | Six合法tuples、operation/envelope一致、profile不在operation中途重綁 |
| State-store extraction | router path/bounded I/O/lock/atomic/cleanup code、state/security/regression tests | SHA-256 session ownership、same-directory atomic replace、symlink rejection、30-day cleanup |

不在直接修改範圍：General／Claude 5 profile內容、Codex/Generic adapters、release builder、README與Project Knowledge Base。未來若package inventory因多module或bundling受影響，必須在新Specification中顯式擴大範圍。

## 8. Unresolved items

- Current Plugin validator要求`scripts/`恰好只含`router.mjs`。未來要採多source modules、build-time bundle或仍維持單檔，只能由新Specification決定。
- 需要決定哪個boundary擁有host timeout/deadline budget；不能讓filesystem helper自行猜Claude hook deadline，也不能讓每個handler任意傳low-level retry knobs。
- 需要決定contract canonicalization只消除哪些人工projection，同時保留Python validator與mutation tests的獨立性。
- Authenticated exact Claude Code `2.1.251` command identity、`additionalContext`與failure semantics仍屬Ticket 3 hard gate；本architecture diagnosis沒有解除或替代它。
- File-link TOCTOU、host在rename/lock ownership移交期間終止process、system clock異常與PID reuse仍是residual engineering topics；是否需要額外contract需另行評估，不能在Draft下直接擴充。
- 本context沒有執行current correction tests或validator；correction是否Accepted仍由fresh independent Review與raw verification決定。
- 若`router.mjs`在本報告後再變更，snapshot hash會失效，必須先確認findings是否仍適用再接受本報告。
- A1–A5與全部proposals尚未被使用者接受或拒絕。

Architecture verdict: 沒有發現需要在目前Ticket 2 correction中立即插入重構的architecture blocker。Current findings涵蓋Large Module／Divergent Change、route-decision Data Clumps／Primitive Obsession、deadline與source-text Leaky Abstraction，以及受控的cross-artifact Shotgun Surgery；它們適合在Ticket 2完成後另開Specification處理。

## 9. Artifact links

- [Approved Specification](../specs/claude-code-adapter-1.4.0.md)
- [Approved Ticket Plan](../plans/claude-code-adapter-1.4.0.md)
- [Project Knowledge Base](../project/knowledge-base.md)
- [Ticket 2 Implementation Evidence](claude-code-adapter-1.4.0-ticket-2.md)
- [Initial Ticket 2 Independent Review](claude-code-adapter-1.4.0-ticket-2-review.md)
- [Claude router](../../adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs)
- [Claude hooks](../../adapters/claude-code/plugin/ask-then-do-it/hooks/hooks.json)
- [Exact model mapping](../../adapters/claude-code/plugin/ask-then-do-it/config/model-classifications.json)
- [Claude Plugin validator](../../scripts/validate_claude_plugin.py)
- [Model evidence validator](../../scripts/validate_claude_model_evidence.py)
- [Router contract tests](../../tests/claude/test_router_contract.py)
- [Router state tests](../../tests/claude/test_router_state.py)
- [Router security tests](../../tests/claude/test_router_security.py)
- [Review regression tests](../../tests/claude/test_router_review_regressions.py)
- [Router schema validation tests](../../tests/claude/test_router_schema_validation.py)
- [Model classification evidence tests](../../tests/claude/test_model_classification_evidence.py)
- [Public Plugin contract tests](../../tests/claude/test_public_plugin_contract.py)

## 10. Knowledge Base Change Summary

`Not applicable`。本診斷沒有產生已核准的durable project fact，也沒有修改`docs/project/knowledge-base.md`。A1–A5與所有improvement proposals都只是尚未接受的Draft diagnosis。

若使用者日後接受任一方向，只能先回`$write-spec`；Specification獲核准後再由`$plan-tickets`建立implementation plan。只有該流程產生並獲明確核准的durable knowledge，才可另行提出Knowledge Base additions、modifications或removals。
