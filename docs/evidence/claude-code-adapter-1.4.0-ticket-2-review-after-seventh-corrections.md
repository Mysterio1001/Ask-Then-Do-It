# Claude Code Adapter 1.4.0 Ticket 2 第七次修正後獨立 Review

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-2-review-after-seventh-corrections`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Review label: `independent`

Status: Changes Requested

## Findings-first

### [P1] 可定位 session 的 PostModelSwitch schema failure 沒有建立 durable fence，下一個 public entry 仍以舊 model 成功路由

Trigger：`PostModelSwitch` 已表示 active model 完成切換，但 event 含一個 schema-invalid optional field；獨立 probe 使用 valid session、`source: auto`、由 `claude-sonnet-5` 切到已知 unsupported `claude-3-7-sonnet-20250219`，只把 `pricing` 設為不在 enum 內的 `dynamic`。Impact：router 輸出「Stop both public entries」與 synchronization warning，state 卻仍為舊的 `ready`／`claude-5`；緊接的 automatic entry 產生 ready envelope、建立 operation 並選 `claude-5` profile。因此 known unsupported model 可在 Post failure 後繼續進入 workflow，違反 AC 6、8、9、Approved Specification 的 state/router failure 與 Post commit failure fail-closed boundary。Existing guard：`main()` 對 Post failure 的 catch 只輸出 warning；durable post-failure fence 要到完整 `validateEvent()`、Node gate、`statePath()` 與 action dispatch 之後才建立，所以 schema failure 在 fence 之前發生。Tight location：`adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1606`（完整 event validation）、`:1641`（過晚建立 fence）、`:1665`（只有訊息、沒有 durable state/fence 的 Post catch）。Remediation direction：對已能安全取得並驗證 `session_id` 的 Post event，應在其餘可失敗的 schema／mapping／state工作前建立 same-session durable failure fence，成功 commit 後才清除；並新增 regression，斷言 invalid optional metadata 後的 automatic 與 explicit entry 都是 failure，直到核准的 Post commit、model-bearing SessionStart 或 clear recovery。

Finding 數：1（P0: 0、P1: 1、P2: 0、P3: 0）。

## Reviewed inputs

- Approved Specification：`docs/specs/claude-code-adapter-1.4.0.md`，聚焦必要行為 3–5、9、failure boundaries 與 AC 6–10、22。
- Approved Ticket Plan：`docs/plans/claude-code-adapter-1.4.0.md` 的 Ticket 2 與必要 Ticket 1／3 dependency；Ticket 2 Approved mode 為 `tdd`。
- Final production：`hooks/hooks.json`、`config/model-classifications.json`、`scripts/router.mjs`、兩個 public `SKILL.md`。
- Validators：`scripts/validate_claude_plugin.py`、`scripts/validate_claude_model_evidence.py`。
- Final tests：`tests/claude/` 全部檔案與 fixtures。
- 未讀取任何被禁止的既有 Ticket 2 implementation evidence、`docs/evidence/*review*.md`、architecture diagnosis 或 implementer verdict／narrative。

## Assumptions

- 本 operation 的 Project 與 User mode Config 均不存在，已由上游證明 Full fallback；本 Review 不重用其他 operation 的 mode。
- Fresh reviewer context 未參與實作，也未取得 implementer 結論，因此標籤為 `independent`。
- Ticket 3 authenticated exact-host ledger 尚未完成；本 Review 將 command identity、`UserPromptExpansion` additionalContext 與 host failure semantics 視為 provisional，不把 strict validation 等同 authenticated session proof。
- 使用者提供的 raw test／validator結果視為 supplied raw evidence；本 reviewer 另做唯讀 code trace、tests 與 probes，不把環境缺依賴誤判為產品 regression。

## Raw verification

### Supplied raw evidence

- 修正前原始 3 tests：`Ran 3 in 11.509s; FAILED failures=6`；涵蓋 automatic/resume Post failure 後 next route、omitted compact、valid `claude-sonnet-6` requested Pre、future-ID Post correlation；既有 Pre lock 與 unsafe custom-marker tests 當時通過。另有 clear recovery 在 production 修正前的 1 failure。
- 修正後 focused 3：`Ran 3 in 14.087s; OK`。
- New/legacy privacy guard 7：`Ran 7 in 13.131s; OK`。
- Adjacent router/state/security/review/public 66：`Ran 66 in 66.936s; OK (skipped=1)`。
- Claude suite：`Ran 102 in 73.662s; OK (skipped=1)`。
- Full repository：`Ran 318 in 96.106s; OK (skipped=1)`。
- Node syntax、Plugin validator、model evidence validator、`git diff --check` 均 exit 0；exact Claude Code `2.1.251 --version`、Plugin／Marketplace strict validation均 exit 0。唯一 skip 是 Windows 無 file-symlink privilege，junction test通過。

### Reviewer rerun and probes

- Router identity重新計算：1,682 lines、50,713 bytes、SHA-256 `b5095e0437ef098bb2a1815cf8e0bb71bbc623f170130fac8df94fb7f000beff`，與 supplied metrics 相同。
- `node --check adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs`：exit 0。
- `validate_claude_model_evidence.py` 對 canonical mapping／source trace：exit 0，輸出 `Claude model classification evidence is valid.`。
- Scoped `git diff --check`：exit 0。
- Reviewer Claude discovery rerun：`Ran 92 tests in 65.429s; FAILED (errors=1, skipped=1)`；90 tests 通過，symlink privilege 1 skip，唯一 error 是 bundled reviewer Python 缺少 PyYAML，導致 `test_public_plugin_contract` import failure。這是 reviewer runtime dependency 缺失；supplied raw evidence已有 public tests 與完整 Claude suite green。
- Positive probes：missing-state `resume`／`compact` 建立 same-session ready unknown state且無 operation；future/custom privacy與 correlation code trace符合現有測試邊界，未發現另一路由或 secret persistence defect。
- Negative probe（finding F-1）：schema-invalid automatic Post 顯示 synchronization warning後，state仍是舊 `ready claude-5`，下一 automatic entry 回傳 `routing_status: ready`、`selected_profile: claude-5`；反例可重現。

## Acceptance-criteria assessment

- AC 6：exact mapping、四類 classification 與一般 failure envelope coverage大致完整，但 F-1 使 Post schema failure 退回舊 ready classification，未通過。
- AC 7：explicit unknown/manual、known non-5與unsupported routing在已驗證 envelope路徑符合規格；未發現獨立 defect。
- AC 8：operation binding、一般 Pre/Post transition、successful Post通知、future-ID correlation與下一 entry reroute有強測試；F-1 使一類 Post failure 的 next-permitted-entry guarantee失效，未通過。
- AC 9：startup/resume/fork/clear/compact、generation、pending/indeterminate、cleanup、cross-session與 durable fence正常路徑涵蓋良好；F-1 表明 fence 尚未包覆所有可定位的 Post failure，未通過。
- AC 10：固定 `${CLAUDE_PLUGIN_DATA}/routing/v1/sessions` boundary、hash-derived filename、exact state keys、bounded reads、atomic replacement、link/junction防護與 privacy tests整體有力；未發現 raw session ID、prompt、path、custom/tenant marker或 future-ID外洩。
- AC 22（Ticket 2 portion）：Windows實際路徑及跨平台模擬、event/state/failure tests廣泛；authenticated exact-host ledger仍是 Ticket 3 hard gate，且 F-1 顯示 failure矩陣尚有缺口。

## Test-strength assessment

測試對 exact mapping、six operation tuples、cross-session ownership、strict JSON、bounded reads、atomic writes、lock recovery/contention、generation exhaustion、model-omitted compact、clear recovery、custom/tenant marker privacy與 known→future correlation均具明確 negative assertions。主要缺口正是 F-1：`test_post_switch_rejects_invalid_optional_metadata_without_committing` 只檢查 state bytes unchanged與當次 warning，沒有在下一 request 呼叫兩個 public entries，也沒有檢查 durable fence；所以「舊 ready state」被誤當安全的不變性。既有 fence regression只以 lock contention造成的較晚期 failure觸發，無法覆蓋 `validateEvent()` 前置失敗。

## 十二個 Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — no-finding**：route tuple、disclosure enum、state keys與 mapping digest雖跨 production／validator／Skills重述，但 validator把這些作 release-owned contract lock；本 scope 未見造成行為漂移的第二套 production policy。
2. **Long Function — finding**：`main()` 同時負責 stdin parse、command identity、完整 schema validation、Node gate、path derivation、failure fencing、dispatch與錯誤輸出；F-1 正由這個排序耦合觸發，證據與位置同 finding F-1（`router.mjs:1591–1674`）。
3. **Large Module or Class — no-finding**：router 1,682 lines且責任多，但 session-state、lock、routing與hook I/O共同服務單一零依賴 runtime boundary；除 F-1 的具體排序缺陷外，沒有足夠證據把大小本身列為獨立 actionable defect。
4. **Long Parameter List — no-finding**：主要介面以 event/state object與少量 options傳遞，未見不穩定的長參數協調。
5. **Data Clumps — no-finding**：session path/key、state與mapping雖重複同行，但已有 state schema、operation與pending_switch具名結構，未造成獨立缺陷。
6. **Primitive Obsession — no-finding**：classification、status、source與disclosure均由 closed sets、regex或 exact mapping約束；未見 unconstrained primitive穿透信任邊界。
7. **Feature Envy — not-applicable**：本 scope為單一 functional Node module與兩個 declarative Skills，沒有 class/object ownership可判定 envy；跨 validator重驗是外部 contract gate。
8. **Divergent Change — no-finding**：雖 router涵蓋多 hook actions，但全部受同一 route/state lifecycle原因驅動；沒有 revision history或本次證據顯示無關理由反覆改同一區塊。
9. **Shotgun Surgery — no-finding**：model mapping更新需要 mapping、digest、fixtures與validators同步是刻意的 release freeze gate；未見一般 lifecycle修正必須散落多個 production owner。
10. **Message Chains — not-applicable**：沒有深層 object navigation或跨服務 call chain；filesystem helper鏈已封裝，未見 caller暴露內部結構的獨立問題。
11. **Leaky Abstraction — no-finding**：public Skills只消費 bounded envelope，未接觸 raw session、state path或lock；F-1 位於 hook orchestration內部，沒有向 Skill caller洩漏 state實作細節。
12. **Shallow Module — no-finding**：router的單一 CLI介面隱藏 classification、ownership、atomicity、locking、fencing與lifecycle transition，介面複雜度低於其承擔功能。

每個 lens 恰有一個 outcome；此處只評估 Ticket 2 change/impact area，不宣稱完成 system-wide architecture diagnosis。

## Residual risks and deferred checks

- Ticket 3 authenticated exact Claude Code `2.1.251` namespaced invocation／additionalContext／failure-semantics ledger仍為 residual hard gate。現有 strict Plugin／Marketplace validation只能證明 schema接受，不等同 authenticated session behavior；這不是本 Review 新增的 code finding。
- Windows reviewer host無 file-symlink privilege；junction traversal test已通過，但 file-symlink branch仍由 supplied single skip保留為未在本機執行的 residual。
- Automatic Post-before-next-request race仍是 Approved Specification明示的 best-effort host限制；本 finding不是該允許 race，而是 Post handler已執行並報失敗後仍允許下一 entry。
- Reviewer環境缺 PyYAML，未能獨立重跑11個 public-contract tests；以 supplied raw green、validator code trace及其餘 tests補足，但仍如實列為 unavailable rerun evidence。

## Completion assessment

Ticket 2 尚未完成。Final state在 route、privacy、correlation、clear recovery與一般 durable Post fence方面已有強證據，但 F-1 是會讓 unsupported／unknown新 model 在 Post failure後沿用舊 classification並開始新 operation 的 actionable P1 correctness/safety defect；因此不能接受 AC 6、8、9、22 或 Ticket 2 completion claim。

## Handoff

交回 Ticket 2 implementation：只修正可安全定位 same-session state 的 PostModelSwitch 前置失敗 fencing／recovery，先加入能重現 F-1 的 automatic＋explicit next-entry red tests，再依 Approved `tdd` 模式完成修正。修正後至少重跑 focused Post schema/fence/recovery tests、router/state/security/review/public adjacent suite、完整 `tests/claude/`、完整 repository suite、Node syntax、兩 validators與 `git diff --check`，再交由另一個 fresh independent reviewer。Ticket 3 authenticated host ledger仍保留為後續 local `1.4.0` hard gate，不以本次修正或 strict validation取代。
