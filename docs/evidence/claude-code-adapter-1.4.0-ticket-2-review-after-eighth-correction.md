# Claude Code Adapter 1.4.0 Ticket 2 Review After Eighth Correction

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-2-review-after-eighth-correction`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Review label: `independent`

Status: Changes requested

Reviewed inputs: Approved `docs/specs/claude-code-adapter-1.4.0.md`；Approved `docs/plans/claude-code-adapter-1.4.0.md` Ticket 2；必要的 Approved `docs/requirements/claude-code-adapter-1.4.0.md` routing/state boundary；final `hooks/hooks.json`、`config/model-classifications.json`、`scripts/router.mjs`、兩個 public `SKILL.md`；`scripts/validate_claude_plugin.py`、`scripts/validate_claude_model_evidence.py`；`tests/claude/` tests 與 fixtures；使用者提供的 raw verification ledger。

Assumptions: 本 operation 的 top-level mode 已證明為 Full fallback，capability 為 `multi_agent`；Approved Ticket mode 與 supplied mode 都是 `tdd`，沒有 mode conflict。Review 對象是 router SHA-256 `0b2b401c5e1270ece8d3e86b5fc7da0ff6d242feae10170184f12dcc626d5647` 的 current final files。Ticket 3 exact-host behavior 仍依 Approved sequencing 只允許 provisional／simulated status。Reviewer 沒有參與 implementation，且未讀 Ticket 2 implementation evidence、先前 Review、architecture diagnosis或 implementer conclusions。

## Findings

### P1 — 異常的 Post failure-fence 物件會被當成「沒有 fence」，讓 stale route fail open

位置：`adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:672`，最直接的錯誤分支在 line 677。Trigger 是 valid startup 後，該 session 的 `.<state-file>.post-failure` 路徑已存在為 directory，再收到 automatic `PostModelSwitch`。`establishPostFailureFence` 無法建立 fence，Post handler 正確輸出「Stop both public entries」warning；但 `hasPostFailureFence` 對既有 non-file、non-symlink 物件回傳 `false`，所以下一次 automatic entry 仍以舊的 `supported-non-5` state 回傳 `ready`／`general`／`none`。這使一個已明確宣告同步失敗的 model switch 仍可用 stale classification 開始 operation；若 active model 已切成不受支援或不同 generation，便違反 Specification sections 4、5、9 及 Post failure 必須停止兩入口的 boundary。現有 guard 會拒絕 symlink ancestor，regular fence 也會阻擋 route，但 final path 的 directory 等異常物件落入 `false`。Remediation direction 是讓任何已存在但不是精確可信 regular fence 的物件都成為 blocking state read/ownership failure（或保守視為 fence），並加入「failed Post → directory/其他可跨平台建立的 abnormal fence → automatic 與 explicit 都 failure」的 regression tests。

### P2 — `compact` 把 present-but-unmapped model 與 omitted model 混為同一個 `null`

位置：`adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1318`，錯誤判斷在 line 1329。Trigger 是 same-session state 已是 `pending` 或 `indeterminate`，接著有效 `SessionStart(source=compact)` 明確帶入 custom／unmapped model，例如 `gateway/custom-model`。`correlatableModelIdOrNull` 將它轉成 `null`，而 line 1329 以 `modelId === null` 判斷「沒有新 model」，因此拒絕這個 compact；下一個 public entry 仍回傳 `state-pending` 或 `state-indeterminate`。Specification section 5 要求 compact 的 event model 若存在就更新 state；model classification contract 又要求 custom／unmapped ID 在 ownership/schema/lifecycle valid 時成為 `unknown`，只有真正省略 model 的 compact 才能依 prior trustworthy state 決定是否保留。現有 `modelWasOmitted` 已在前一個 fence guard 正確保存兩者差異，resume 與 known-model compact 也能恢復，但 line 1329 遺失了這個區分。Remediation direction 是只在 `modelWasOmitted` 且 prior state 非 `ready` 時拒絕，讓 present、schema-valid、不可分類的 model 寫成新 generation 的 `ready`／`unknown`，並分別覆蓋 pending 與 indeterminate recovery tests。

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — `no-finding`。** Route/envelope constants 在 runtime、public bootstrap、validator與 tests 間有刻意的獨立 contract lock；本次沒有發現因 drift 造成的另一個可執行缺陷。
2. **Long Function — `no-finding`。** `main` 與四個 handlers 雖承擔完整 dispatch，但 transition、I/O、lock、validation 已拆成可個別檢查的 helpers；本次 findings 不由單一 long function 的混合責任造成。
3. **Large Module or Class — `no-finding`。** `router.mjs` 為 1,696-line security boundary，但責任仍集中在同一 session-state transaction domain，沒有足夠證據把檔案大小本身升格為本 Ticket 的 actionable architecture finding。
4. **Long Parameter List — `no-finding`。** Event、state與 options 以 structured objects 傳遞；主要 handlers 的參數數量有限，未見錯置參數或不穩定 coordination interface。
5. **Data Clumps — `no-finding`。** Session pathname/key、classification/profile與 lock metadata 有明確 state／operation／lock abstractions；未見重複散落且已造成缺陷的 value group。
6. **Primitive Obsession — `finding`。** Finding P2 證明 `null` 同時表示「event model omitted」及「present model 無法分類」，遺失兩個不同 lifecycle domain states，並在 compact guard 產生錯誤行為。
7. **Feature Envy — `no-finding`。** Routing handlers 主要操作其所擁有的 validated event/state；沒有 helper 大量窺探另一 module 的 internals。
8. **Divergent Change — `no-finding`。** 本次範圍內的變更理由集中於 Claude route/state/failure semantics；未見 unrelated policy 被迫聚集於同一函式。
9. **Shotgun Surgery — `no-finding`。** Hooks、bootstrap、validator與 tests 的同步是 provider contract 的必要 cross-check；沒有證據顯示本次兩個 runtime defects 必須跨不相干 owners 修補。
10. **Message Chains — `no-finding`。** Filesystem/state access 沒有長 navigation chains；helpers 隔離了 path、lock、read與write steps。
11. **Leaky Abstraction — `finding`。** Finding P1 的 `hasPostFailureFence` 將「不存在」與「存在但類型不可信」折疊成相同 `false`，使呼叫端無法維持其 fail-closed promise。
12. **Shallow Module — `no-finding`。** State/lock/envelope helpers 提供的 validation、bounded I/O與atomic behavior足以支撐其 interfaces；除上述兩個精確語意缺口外，未見整體 interface 成本大於隱藏的功能。

## Verification

Reviewer performed:

- 完整 Claude suite：`Ran 104 tests in 77.105s`，`OK (skipped=1)`；唯一 skip 是 Windows file-symlink privilege，directory-junction guard仍執行通過。
- `node --check adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs`：exit `0`。
- `scripts/validate_claude_plugin.py`：exit `0`，`Claude Plugin validation passed`。
- `scripts/validate_claude_model_evidence.py`：exit `0`，`Claude model classification evidence is valid`。
- `git diff --check`：exit `0`；只有既有 `docs/project/knowledge-base.md` LF→CRLF warning。
- Finding P1 direct read-only probe：valid supported-non-5 startup後，在 precise per-session fence path放入 directory；automatic Post 回報 synchronization failure與「Stop both public entries」，緊接的 automatic expansion卻回 `routing_status=ready`、`model_classification=supported-non-5`、`selected_profile=general`、`disclosure_code=none`。
- Finding P2 direct read-only probes：valid startup後形成 `pending` 或 `indeterminate`，再送出帶 present custom/unmapped model 的 compact；compact未建立 `ready`／`unknown`，後續 expansion仍回 `state-pending` 或 `state-indeterminate`。
- Fresh delegated reviewer另外獨立重現兩個 findings，並核對同一 router surrounding code；其環境沒有修改任何檔案。

Supplied raw verification retained as supplied evidence, not misrepresented as this reviewer's execution:

- 兩個 focused Red 在修正前分別為 `Ran 1` with failures `2`、`Ran 1` with failure `1`；current focused combined `Ran 3 in 12.739s, OK`。
- Six adjacent modules：`Ran 77 in 71.836s, OK (skipped=1)`；Claude suite：`Ran 104 in 78.024s, OK (skipped=1)`；full repository：`Ran 320 in 105.801s, OK (skipped=1)`。
- Node syntax、Plugin validator、model-evidence validator、`git diff --check`皆 exit `0`；同一換行 warning如上。
- Exact Claude Code `2.1.251 --version` 已回報 `2.1.251`；canonical Plugin 與 repository Marketplace 的 `plugin validate ... --strict` 都 exit `0`、`Validation passed`、無 warning。
- 先前 full run 曾因既有 release atomic directory replacement 暫時 `WinError 5` 出現單一 failure；該單測立即重跑通過，之後 full 320 green。

## Evidence unavailable and deferred checks

- 未登入 Claude Code，沒有 authenticated `UserPromptExpansion`／兩個 namespaced command identity、`additionalContext` visibility、Node unavailable/nonzero/exit-2/timeout semantics或實際 model switch ledger；這些仍屬 Ticket 3。
- Native strict validation證明 schema acceptance，但不等於 authenticated command execution或完整 host behavior。
- 未在 macOS／Linux、VS Code或JetBrains真實 surface執行；目前跨平台 path/event/state/failure evidence是 deterministic simulation。
- 本 reviewer 未重新執行 full repository 320-test suite或 six-module 77-test subset；保留 supplied raw results並自行重跑完整 Claude suite。
- Model source snapshots與 dated trace通過 repository validator；本次沒有 network refresh官方來源。

## Residual risk and untested areas

- Ticket 3 authenticated exact-host ledger仍是 local `1.4.0` integration/completion的 hard gate；本 Ticket 的 command identity、hook timing與failure semantics不得升格為 live-verified。
- `PostModelSwitch` commit前的 host race仍只能是 Approved best-effort boundary；不得宣稱 model change後第一次 invocation必然重路由。
- 現有 tests覆蓋 regular fence、symlink state path、directory junction、lock contention與 omitted compact，但未覆蓋 Finding P1 的 abnormal final fence object，亦未覆蓋 Finding P2 的 present-unmapped compact從 non-ready state恢復。

## Completion assessment

Approved Ticket 2目前**尚不構成 complete**。TDD mode與既有 broad verification本身成立，但 P1 直接破壞 Post synchronization failure 的 fail-closed承諾，P2 未實作完整的 valid-unknown compact lifecycle；兩者都屬 Ticket 2 acceptance criteria 6–10／22範圍，不能延後給 Ticket 3或後續 profile Tickets。

## Handoff

回到 Ticket 2 `tdd` implementation：先為兩個 findings建立 focused Red，再做最小 Green／Refactor，重跑 affected router/state/security/public-contract modules、完整 Claude suite與適當 broader repository verification。修正後需要 fresh independent Review。Review只授權診斷與報告，本 artifact不授權修改 production、tests、Specification、Plan或Knowledge Base。Ticket 3 authenticated host ledger在這些修正後仍維持 release hard gate。
