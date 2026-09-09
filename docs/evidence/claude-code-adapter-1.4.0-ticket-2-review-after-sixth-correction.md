---
artifact_type: Review Report
artifact_id: claude-code-adapter-1-4-0-ticket-2-review-after-sixth-correction
workflow_id: claude-code-adapter
core_version: 1.3.0
review_label: independent
status: Changes Requested
---

# Claude Code Adapter 1.4.0 Ticket 2 第六次修正後獨立 Review

## Findings

### [P2] Automatic PostModelSwitch commit failure 未留下 durable fail-closed state

**Trigger：** session 目前是 `ready`，Claude Code 以 `source: auto` 或 `resume` 送出 `PostModelSwitch`，但 router 在取得 session lock 或寫入新 classification 前失敗；可重現情境是另一個仍存活 process 持有 fresh session lock 超過 router retry window。**Impact：** `main()` 雖輸出「Stop both public entries until a new valid SessionStart state is established」，舊 state 仍保持 `ready` 與舊 model classification；鎖解除後下一次 public entry會產生成功 envelope 並按舊 model 選 profile。更嚴重的是，接著收到 model omitted 的 `compact` 時，`handleSessionStart()` 會把這個已失去可信度的舊 classification 當作可保留資料，讓警告所要求的停止條件消失，仍成功路由錯誤 profile。這違反 state/router failure 與 valid unknown 必須分離、Post commit failure 後兩個 entries fail closed，以及 compact 只能保留 trustworthy same-session classification 的契約。**Existing guard：** catch path 會輸出 system warning 與 additional context；requested switch通常也會因先前 `pending` state 而自然 fail closed。但 automatic／resume Post failure 沒有 `pending` state或其他 durable fence，warning 不是下一次 router decision 的狀態來源。**Location：** `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1548` 的 Post lock/commit 呼叫與 `:1567` 的 warning-only catch；stale classification 隨後由 `:1247` 的 compact preserve path沿用。**方向：**在 automatic／resume Post 處理開始或失敗時建立 route 與 compact 都會檢查的 durable、session-isolated invalidation fence，且只在 authoritative Post commit或可證明 current model 的新 SessionStart 後解除；新增 Post lock/write failure → compact/next-entry 的 regression tests。

### [P2] Valid unmapped canonical model 無法完成 requested model-switch transition

**Trigger：** `SessionStart.model` 是 mapping 尚未列出的 canonical future ID，例如 `claude-sonnet-6`，因此依規格是 valid `unknown`；之後使用者以 `command`／`picker`／`sdk` 從同一 ID 切到已知 model。**Impact：** router 在 startup 把 unmapped canonical ID折疊成 `null`；Pre hook再把相同 `from_model`折疊成 `null`並立即標記 `indeterminate`，Post hook因沒有 matching pending transition也失敗。即使 authoritative `to_model` 是已知、受支援 model，兩個 public entries仍被鎖住直到另一個 SessionStart，沒有依 Post event提交 `ready` classification。這違反「canonical ID不在 mapping 是 valid unknown」、pending switch保存 canonical `from_model`，以及 matching requested Pre/Post 應提交 authoritative `to_model` 的契約。**Existing guard：** exact mapping與 `allowlistedModelIdOrNull()` 防止 alias/custom gateway/任意 marker被持久化；現有測試也驗證 unknown 可路由及 unmapped字串不洩漏。然而它把「安全的未列 canonical ID」與「model omitted／不可信 custom ID」都壓成同一個 `null`，而 `test_unmapped_regex_shaped_pre_switch_from_model_fails_closed_without_secret_persistence` 正好固化了過度關閉行為，沒有測 canonical future ID 的完整 switch sequence。**Location：** `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:238`、`:1237`、`:1363`–`:1367`、`:1416`；相反期待位於 `tests/claude/test_router_security.py:413` 的單步 unknown test，但未延伸到 Pre/Post。**方向：**分開表示 omitted／unsafe provider ID 與符合 canonical contract但未列 mapping 的 future ID；classification仍必須是 exact-map `unknown`，同時保留足以安全匹配 Pre/Post 的 canonical identity或等價非敏感 correlation，並加入 unknown canonical → requested switch → known/unknown target 的端到端測試。

## Reviewed inputs

- Approved Specification：`docs/specs/claude-code-adapter-1.4.0.md`，重點核對必要行為第3–5、9、11節、邊界與失敗行為、資料／權限契約及驗收條件6–10、22。
- Approved Ticket Plan：`docs/plans/claude-code-adapter-1.4.0.md` 的共同順序、Ticket 2及Ticket 3 hard-gate dependency；Approved mode確認為 `tdd`。
- Final production：`hooks/hooks.json`、`config/model-classifications.json`、`scripts/router.mjs`、兩份public `skills/*/SKILL.md`、`scripts/validate_claude_plugin.py`、`scripts/validate_claude_model_evidence.py`。
- Final tests：`tests/claude/` 全部檔案與 model-source／host-contract fixtures。
- 題目提供的 raw TDD／verification紀錄；未讀任何 `docs/evidence/*review*.md`、Ticket 2 implementation evidence、architecture diagnosis或implementer verdict/narrative。

## Assumptions

- 本 operation 已由上層證明 Project／User config皆不存在，因此採 Full fallback；本 Review不重新持久化 mode。
- Fresh reviewer未參與 implementation或先前 Reviews，且只使用題目允許的 raw artifacts，所以 label為 `independent`。
- 題目提供的 exact Claude Code `2.1.251 --version`、native strict validation及full-repository結果視為原始驗證輸入；本輪沒有把 strict validation誤當 authenticated Claude session。
- Local `.venv` 是 repository測試的可用 Python環境；首次使用 bundled Python因缺少 PyYAML而發生的 import error是執行環境選錯，不是產品失敗，改用 `.venv` 後成功。

## Raw verification

### 題目提供

- 新 focused version-proof test在 production修正前：`Ran 1 test; FAILED (failures=2)`；兩個 entry皆因缺少 ready-route version proof失敗。
- 修正後同 test：`Ran 1 test in 0.001s; OK`。
- Public Plugin contract：`Ran 11 tests in 11.773s; OK`。
- Claude suite：`Ran 99 tests in 62.221s; OK (skipped=1)`。
- Full repository：`Ran 315 tests in 81.103s; OK (skipped=1)`。
- Node syntax、Plugin validator、model evidence validator、`git diff --check`皆 exit 0。
- Exact `2.1.251 --version`、Plugin strict validation、Marketplace strict validation皆 exit 0；strict validation不是 authenticated Claude session。
- 唯一 skip是 Windows帳號無 file-symlink privilege；directory junction test已通過。

### 本輪重跑

- Focused ready-route version-proof test：`Ran 1 test in 0.001s; OK`。
- Public Plugin contract：`Ran 11 tests in 12.340s; OK`。
- Router security/state/public contract/model evidence組合：`Ran 48 tests in 32.213s; OK (skipped=1)`。
- 完整 `tests/claude/`：`Ran 99 tests in 61.508s; OK (skipped=1)`。
- Node `--check scripts/router.mjs`、Plugin validator、model evidence validator、`git diff --check`：exit 0；`git diff --check`僅回報既有 Knowledge Base working-copy LF/CRLF warning，沒有 whitespace error。

### Adversarial probes

1. 建立已知 `claude-sonnet-4-6` ready state，以 live fresh lock使 automatic Post switch到 `claude-sonnet-5`無法取得lock。Post正確輸出warning，但state仍為 `ready/supported-non-5`；解除lock後 automatic entry回傳 `ready/general/none`。再加入model-omitted `compact`仍可重現，compact不輸出新warning且下一route繼續成功使用舊classification。
2. 以未列 mapping但符合canonical形狀的 `claude-sonnet-6` startup；initial state是 `ready/unknown`。requested Pre切到 `claude-sonnet-5`後state變成 `indeterminate`，matching Post仍失敗，下一automatic entry回傳 `failure/state-indeterminate`。

## Acceptance criteria assessment

| Criterion | Outcome | Evidence |
| --- | --- | --- |
| AC 6 — exact mapping與完整route/failure table | **Fail** | Nominal table與validators通過，但valid unmapped canonical model的後續requested switch無法完成；Post failure後亦可用stale ready classification產生成功route。 |
| AC 7 — explicit `-5` unknown/manual routing | **Pass within reviewed scope** | ready/failure envelope union、唯一 `node-too-old` manual fallback、Claude Code independent proof與disclosures均由exact Skill bodies/validator/tests保護。 |
| AC 8 — operation binding與Pre/Post transitions | **Fail** | 兩個 findings都落在 transition/next-entry contract；其中automatic Post failure可在下一entry選錯 profile。 |
| AC 9 — lifecycle/state/cross-session/cleanup | **Fail** | Nominal lifecycle、generation、cleanup與isolation通過；但compact錯把failed automatic Post留下的舊ready classification視為trustworthy。 |
| AC 10 — fixed state boundary與資料最小化 | **Pass within reviewed scope** | Hash-derived filename、exact state keys、bounded strict JSON、atomic same-directory write、no prompt/raw-session/path persistence、symlink/junction guards與no-network checks通過。Finding 2要求保留switch correlation時仍須維持此boundary。 |
| AC 22 — automated path/event/state/failure + exact host | **Fail for Ticket 2 deterministic portion; exact-host deferred** | 99-test suite nominal通過，但兩個跨事件failure sequences未被測試且production probe失敗。Exact-host authenticated behavior仍是Ticket 3 hard gate。 |

## Route、state、failure、security與privacy結論

- Route表對known Claude 5、supported non-5、unsupported、initial unknown及兩entries的正常輸入正確；兩個 P2 是跨事件序列，而非單步table錯誤。
- State authored keys、operation tuple、generation上限、ownership hash、staleness、cleanup及cross-session isolation皆有正向與負向測試；但automatic Post failure缺少durable失效狀態，破壞「ready代表可安全route」的不變量。
- Failure envelopes是bounded、closed enum、exit 0且沒有 untrusted text；Pre failure不deny model switch。問題在warning與持久state不一致，而非warning缺失。
- Raw session ID、prompt、arguments、cwd、transcript與model-shaped secret marker未進state/envelope；讀取有byte上限，JSON拒絕duplicate keys，state path與lock具link/junction與atomic handling。
- Exact-map策略可信地拒絕substring/alias/future promotion；model source trace具日期、URL、snapshot hash、mapping byte hash及per-ID record。Finding 2不要求把untrusted custom gateway ID升格或輸出，而是不要讓規格明定的valid canonical unknown失去transition identity。

## 版本 proof 與 fail-closed ordering

- 兩份public Skill在接受ready envelope後、任何disclosure/profile load前都要求固定執行 `claude --version`，只接受可證明的 `2.1.251+`；fixed text與paragraph ordering受exact-body validator、mutation boundary及focused test保護。Node 22 gate在plugin data/state存取前執行，Node 18/19/21 failure envelope tests通過。
- Explicit manual path只接受valid `node-too-old` failure envelope，或missing envelope且可分別證明supported Claude Code與Node genuinely missing；其他missing/failure均停止。
- 題目提供的exact binary version與兩個strict validation支援schema/static相容性，但不證明authenticated `UserPromptExpansion`、failure semantics或完整session behavior；此限制列入deferred/hard gate，不另列finding。
- F1顯示跨request fail-closed ordering仍有缺口：model-visible warning先要求停止，後續router卻能從舊 `ready` state產生成功envelope；compact可進一步清除這個warning boundary。

## 十二個 Architecture and Refactoring Lenses

| # | Lens | Outcome | Evidence |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `no-finding` | Mapping在JSON、runtime semantic hash、validator freeze與source trace中的重複是刻意的tamper-evident release boundary；兩Skill共用envelope規則由exact body validation同步。 |
| 2 | Long Function | `no-finding` | 較長的strict JSON parser、state validator與dispatcher各自維持單一安全責任，且有直接unit/negative tests；未見因函式混責造成獨立finding。 |
| 3 | Large Module or Class | `no-finding` | `router.mjs`雖大，但依Approved package inventory是單一zero-dependency router boundary，內部已按parsing、mapping、locking、state與handlers拆函式；本輪缺陷不是單純module size造成。 |
| 4 | Long Parameter List | `no-finding` | 對外處理以structured event/state objects，少數內部函式使用短參數與options object，未暴露不穩定長位置參數介面。 |
| 5 | Data Clumps | `no-finding` | Envelope、operation、pending switch、state與lock都有exact key schema，沒有同組primitive在多處以鬆散參數傳遞。 |
| 6 | Primitive Obsession | `finding` | F2：`allowlistedModelIdOrNull()`用單一 `null`同時代表omitted、unsafe/untrusted與valid unmapped canonical identity，抹除domain distinction並破壞transition。 |
| 7 | Feature Envy | `not-applicable` | Reviewed scope沒有class/object owner間取用彼此內部資料的設計；handlers操作自己的validated state boundary。 |
| 8 | Divergent Change | `no-finding` | Runtime module的變更理由集中在同一Claude route/state contract；validators與fixtures的配套改動是該contract的verification owner。 |
| 9 | Shotgun Surgery | `no-finding` | Public entry與mapping freeze需同步多artifact，但exact validators可立即拒絕漂移；沒有發現同一行為必須在無guard的分散位置修改。 |
| 10 | Message Chains | `no-finding` | Hook → dispatcher →單一handler →state/output的call chain短且boundary明確；沒有深層navigation依賴。 |
| 11 | Leaky Abstraction | `finding` | F1：automatic Post failure的真實安全狀態沒有進入state abstraction，改由一次性的model-visible warning補償；後續route/compact因此看見錯誤的 `ready`。 |
| 12 | Shallow Module | `no-finding` | Bounded envelope與四個hook actions隱藏了hash ownership、strict parsing、atomic lock/write、lifecycle與classification複雜度，介面成本有相稱功能。 |

## Test strength

- 現有suite對route table、exact command identity、Node版本、schema optional fields、duplicate JSON、state tuple/generation、concurrency、stale lock recovery、symlink/junction、cleanup、cross-session、mapping mutations及Skill exact body有良好辨識力。
- Ready-route version proof的新RED確實在兩個entry都失敗，GREEN後focused/public/full suites通過；exact-body validator也讓任意文案漂移fail。
- 缺口一：lock tests覆蓋「route遇到live lock回failure envelope」與「Pre遇到live lock不阻擋」，但沒有覆蓋「automatic Post遇到live lock／write failure後解除故障，再compact或route」；因此F1未被攔截。
- 缺口二：unknown tests各自覆蓋initial route、unmapped Pre fail closed、automatic Post to unknown及canonical future initial route，卻沒有串起canonical future current model → requested Pre/Post → next route；因此F2被單步斷言遮蔽。

## Deferred

- Ticket 3 authenticated exact Claude Code `2.1.251` host ledger仍是local `1.4.0`完成前hard gate：需實測兩entry的exact command identity、`UserPromptExpansion` additionalContext/failure semantics與session behavior。依使用者指示，這不是本Review finding；若host觀察推翻假設，應回最早受影響artifact重開。
- General／Claude 5 workflow module行為、paired profile equivalence、context proxy、documentation、package/release integration與live smoke分屬後續Tickets，不以Ticket 2結果替代。
- Windows無file-symlink privilege的唯一skip仍是residual；directory junction protection已實跑通過。正式release仍應在具symlink privilege的受支援環境補足該branch。

## Residual risks

- Native strict validation只證明schema/static acceptance；未authenticated session前，hook matcher、event payload與failure output在exact host上的實際行為仍是provisional。
- Model evidence snapshots是有hash的人工normalized官方頁面摘錄；validator證明trace內部一致與per-ID coverage，不是遠端內容的獨立簽章。Release ledger仍須保存dated official provenance並在freeze時重驗。
- Model-switch commit前的host race window依Approved Specification仍是best-effort；本Review finding針對的是Post已到達但commit失敗後仍可重新route，不是把允許的commit前race誤列缺陷。

## Ticket completion assessment

Ticket 2目前**不符合完成條件**。Nominal tests、validators、版本proof修正與主要security/privacy boundary皆通過，但兩個P2使AC 6、8、9及22的deterministic部分未完成；尤其F1破壞router/state failure的fail-closed不變量，F2破壞valid unknown canonical model的requested switch lifecycle。因此status為 **Changes Requested**，不是Accepted。

## Handoff

回到Ticket 2 implementation：先為兩個findings各新增能重現本文序列的RED tests，再修正durable Post-failure fencing與valid-unmapped-canonical transition representation；重跑focused router tests、public contract、完整Claude suite、full repository、Node syntax、兩validators與`git diff --check`。修正後交給新的獨立reviewer；Ticket 3 authenticated host gate保持deferred/hard gate，不因本Review改寫或降級。
