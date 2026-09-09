# Claude Code Adapter 1.4.0 — Ticket 2 Independent Review Report

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-2-review`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Review label: `independent`

Status: `changes-requested`

Ticket mode: `tdd`

Reviewed inputs: `docs/requirements/claude-code-adapter-1.4.0.md`; `docs/specs/claude-code-adapter-1.4.0.md`; Approved Ticket 2 in `docs/plans/claude-code-adapter-1.4.0.md`; current working-tree `adapters/claude-code/plugin/ask-then-do-it/{scripts/router.mjs,hooks/hooks.json,config/model-classifications.json,skills/*/SKILL.md}`; `scripts/validate_claude_plugin.py`; scoped `tests/claude/test_router_*.py`, `tests/claude/test_model_classification_evidence.py`, `tests/claude/test_public_plugin_contract.py` and fixtures; supplied raw verification listed below.

Assumptions: current-operation mode was proven `full` by absent project/user Ask Then Do It Config and Full fallback; reviewer capability is `tools + multi_agent`; this fresh reviewer context did not implement Ticket 2 and received no implementer verdict; exact authenticated host invocation/failure evidence remains provisional under the Approved Ticket 2→3 sequencing exception.

Deferred: authenticated exact-host command identity, `command_source`, `additionalContext` and failure-semantics observations belong to Ticket 3; release integration, profiles, conformance, context proxy, documentation and live smoke remain with their Approved downstream Tickets.

Next handoff: main Full workflow presents these findings for correction approval; if approved, `$implement-tdd` adds failing regressions and makes scoped fixes, then reruns proportional/full validation and requests a fresh independent Review. The architecture concern is routed separately to `$improve-architecture` for diagnosis only.

## Findings

### [P2] 孤兒 session lock 會永久封鎖 lifecycle 與 routing，且可超過 hook timeout

當 router 在持有 lock 時被 host timeout、終止或程序崩潰，或既有 `.lock` 因其他原因殘留時，`withSessionLock` 只反覆以 `O_EXCL` 嘗試開檔，不記錄 ownership、存活資訊或可安全回收的期限，也沒有其他 recovery path。於本機 Windows 實測建立同 session 的孤兒 lock 後再送 `SessionStart clear`，router 經過 `5.054s` 才以 exit `0`、空 stdout 返回，舊 state 仍為 `startup` 且 lock 仍存在；這已達／超過 `hooks.json` 的 `SessionStart`、`PostModelSwitch`、`UserPromptExpansion` 5 秒 timeout，因此真實 host 可先殺掉程序，無法取得 bounded failure envelope，之後同 session 的 clear/start/route 仍會重複失敗。這違反 Ticket 對 bounded failure、clear lifecycle 與可恢復 same-session state 的要求。修正方向應建立具有 ownership 的安全 lock recovery protocol（不得誤刪 live lock），把最大等待時間明確限制在最短相關 host timeout 之內，並以孤兒 lock 的 SessionStart、route 與 PostModelSwitch integration tests 證明 recovery/fail-closed 結果。位置：`adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:561`（retry constants 在 `:87`；host timeout 在 `adapters/claude-code/plugin/ask-then-do-it/hooks/hooks.json:15`、`:47`、`:63`）。

### [P2] Resume/compact 可在未揭露 unsupported model 的情況下恢復既有 operation

當同 session 已有 operation binding，之後 `SessionStart` 的 `resume` 或 `compact` 帶入已知不受支援的 model 時，handler 正確把 state 更新成 `model_classification: unsupported` 並保留 operation，卻一律呼叫 `continuationContext(state.operation)`，沒有傳入現有 helper 已支援的 `unsupported` flag。實測由 `claude-sonnet-4-6` operation resume 到 `claude-haiku-4-5-20251001` 時，輸出的 additional context 只要求沿用 general profile，完全沒有「active model has left formal support」揭露；主 Claude 因而可能在 `<4.6` model 上繼續 operation，直到下一次 public entry 才被阻擋。修正方向是讓所有保留 operation 的 authoritative SessionStart paths 依新 classification 加入同等 support disclosure，並新增 resume 與 compact 的 unsupported cases，確認 operation/profile 不重綁但支援狀態會揭露。位置：`adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:897`。

### [P2] Untrusted state 在驗證前被無上限讀入記憶體

`readState` 對 state file 做類型／symlink 檢查後直接 `readFile(pathname, "utf8")`，沒有檔案大小上限或 bounded streaming；但 Specification 明確把 persisted state 視為 untrusted input，且 authored state 本應非常小。損壞、誤建或刻意放入的大型 session file 會在 schema fail-closed 之前消耗任意記憶體與解析時間，可能使 5 秒 hook timeout 終止 router、造成沒有 failure envelope 的 local denial of service；同一檔案在每次 invocation 都可重現。修正方向是在配置保守的 state byte limit 後先以可信 metadata／bounded read 拒絕超限檔案，並加入超限 state 的 route、resume 與 cleanup tests。位置：`adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:705`（無上限讀取在 `:713`）。

### [P3] Model source-trace gate 不驗證引用的 snapshot 是否真的支持該 model record

`test_every_exact_model_classification_has_dated_source_trace` 只確認每筆 `source_refs` 非空且名稱屬於 sources，也只確認 snapshot 自身的 URL/date/hash；它沒有確認被引用 snapshot 含該 canonical ID、status 或 classification basis。因此，例如把 `claude-1.0` 的 refs 改為只指向不含該 ID 的 `models-overview`，或刪除 snapshot 中的 supporting row 並更新 hash，這項 gate 仍可通過。現有資料經人工對讀看似有可追蹤來源，但 TDD gate 無法防止 evidence drift，未充分證明 Ticket 要求的「每個 canonical ID 的官方來源可重算」。修正方向是將 normalized snapshots 轉成可驗證 records，逐筆確認至少一個引用來源實際包含 ID 與相符 status/basis，並加入錯誤引用與刪 row mutations。位置：`tests/claude/test_model_classification_evidence.py:68`。

### [P3] Router 模組同時承擔多個獨立 change reasons

任何 hook schema、model mapping、filesystem lock/cleanup、state lifecycle 或 envelope contract 的修改都集中在同一個 1,160-line runtime module；這些區域雖以函式分隔，仍共用大量 primitive enums、error codes 與 main dispatch，局部安全修正容易影響其他 hook paths，測試與審查負擔也集中。這是本次新 adapter 引入的 Large Module／Divergent Change 架構風險；上述 lock 與 unbounded-read defects亦落在同一 trust-boundary 區段。它不應在 Ticket 2 finding 修正中順手大改；應把 raw concern 交給 `$improve-architecture` 做只讀診斷，評估是否能在保持單一 dependency-free entrypoint 的前提下分離 schema、state-store/lock、classification 與 hook handlers。位置：`adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1`，主要責任區約在 `:360`、`:445`、`:508`–`:765`、`:855`–`:1067`、`:1090`。

## Verification performed

- 自行讀取 Approved Requirement Decision Record、Approved Specification、Approved Ticket Plan 的 Ticket 2，確認 Ticket mode 為 `tdd`，並檢查 current working-tree scoped files與 surrounding code；未採用 implementer verdict。
- 自行執行 focused suite：`.venv\\Scripts\\python.exe -m unittest tests.claude.test_router_contract tests.claude.test_router_state tests.claude.test_router_security tests.claude.test_model_classification_evidence tests.claude.test_public_plugin_contract -v`，結果 `Ran 38 tests in 27.923s`、`OK (skipped=1)`。唯一 skip 是 Windows file-symlink privilege；directory junction case通過。
- 自行執行 `node --check adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs`，exit `0`。
- 自行執行 `.venv\\Scripts\\python.exe scripts/validate_claude_plugin.py`，exit `0`。
- 自行執行 scoped `git diff --check`，exit `0`。
- 自行執行三組 temporary-directory probes：孤兒 lock 的 clear path重現 `5.054s` timeout-risk且 state/lock 未恢復；resume 至 unsupported model 重現缺少 disclosure；automatic PostModelSwitch 的 mismatched `from_model` 仍提交 `to_model`，此項因 host ordering/authority 尚未有 exact observation，列為 residual risk而非 finding。
- Supplied raw verification（未在本 review context 全量重跑）：Claude suite `Ran 59 tests in 36.926s OK (skipped=1)`；full repository `Ran 275 tests in 67.218s OK (skipped=1)`；exact Claude Code `2.1.251` 對 canonical Plugin與repository Marketplace strict validation均 exit `0`且無 warning。

## Evidence unavailable / deferred checks

- Exact Claude Code `2.1.251` authenticated invocation 尚未證明兩個 `command_name`、`command_source`、same-invocation `additionalContext` 可見性與 Node missing/nonzero/exit-2/timeout host semantics。依 Approved sequencing，這些仍是 Ticket 3 的 release-blocking provisional evidence，不把 strict validation等同於 runtime host verification。
- `<2.1.251` ready-envelope path 沒有獨立可信的 host-version datum；實際 fail-closed 是否可由 hook availability/host contract保證仍未驗證。現有 `compatibility` frontmatter 是聲明，不足以單獨證明 enforcement。若 Ticket 3 不能證明安全邊界，必須回到最早受影響的 Requirement／Specification／Ticket修訂，不能把它降為 unknown-model compatibility。
- Automatic／resume PostModelSwitch 在沒有 Pre event時不比對 stored `model_id` 與 `from_model`。其能否因 delayed/out-of-order events 把較新 state覆寫成較舊 `to_model`，取決於 exact host ordering semantics；目前缺 raw observation，因此是 `unverified`，不是 confirmed finding。
- Windows regular-file symlink test因 privilege skip；真實 directory junction防護已通過。macOS/Linux symlink與path race只有 automated/simulated evidence，未在本 review host重跑。
- 沒有在本 review context 重跑 supplied 59-test Claude aggregate、275-test full repository aggregate或 exact binary strict validation。

## Twelve Architecture and Refactoring Lenses

| # | Lens | Outcome | Evidence |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `no-finding` | JS router、Python validator與兩個 Skills重述 closed enums／route tuples，但 semantic mapping hash、exact validator與mutation tests顯示這是跨 runtime 的刻意 defense-in-depth；本次未找到已漂移的相反規則。 |
| 2 | Long Function | `no-finding` | `validateState`與各 handler雖不短，但仍各自維持單一 validation/transition責任；已確認 defects不是由單一函式內不可追蹤的控制流造成。 |
| 3 | Large Module or Class | `finding` | 1,160-line `router.mjs` 同時擁有 parser、mapping、filesystem/lock、state machine、hook handlers與output contract；trigger、impact與 remediation handoff見 P3「Router 模組同時承擔多個獨立 change reasons」。 |
| 4 | Long Parameter List | `no-finding` | 相關函式最多只傳遞少量 event/pluginData/mapping/path參數，沒有因不穩定協調而形成長參數介面。 |
| 5 | Data Clumps | `no-finding` | operation與pending-switch已封裝為有 exact-key validation 的 state subobjects；route tuple雖重複出現，但有 closed set驗證。 |
| 6 | Primitive Obsession | `no-finding` | model class、status、source、entry與failure code使用字串，但均以 Set／regex／exact keys限制；本次沒有找到未約束 primitive直接跨 trust boundary。 |
| 7 | Feature Envy | `not-applicable` | 變更以 functional module為主，沒有某 class/method反覆操控另一 object內部資料的對象模型。 |
| 8 | Divergent Change | `finding` | hook schema、mapping、locking、lifecycle與envelope均使同一 module改動；trigger與impact見同一 P3 architecture finding。 |
| 9 | Shotgun Surgery | `no-finding` | release mapping/envelope更新確實需同步 JS、validator、Skills與evidence，但這是核准的 cross-artifact exact contract，現有 semantic hash與mutation gates可偵測多數遺漏；未觀察到 current drift。 |
| 10 | Message Chains | `not-applicable` | Production path沒有長 object-navigation/call chain向 caller暴露深層結構；主要是直接函式 dispatch。 |
| 11 | Leaky Abstraction | `finding` | lock implementation的 retry duration必須由 `hooks.json` timeout補償，且 orphan lock會直接洩漏成 host timeout/缺 envelope；trigger、impact、evidence與位置見 P2「孤兒 session lock」。 |
| 12 | Shallow Module | `no-finding` | Router CLI surface僅四個 actions，背後隱藏實質 classification/state/security功能；介面複雜度低於其實作責任，並非 shallow wrapper。 |

這個 architecture concern 已以 raw scope交給獨立 `$improve-architecture` 診斷路徑；本 Review 不授權 refactor，也不把未核准 diagnosis當成修正要求。

## Residual risks and untested areas

- Ticket 3 的 authenticated host contract仍是 integration freeze前的硬閘門；任何 command identity、`additionalContext` 或 failure semantics差異都會使 Ticket 2與依賴它的 evidence失效。
- File-link TOCTOU、host kill恰好發生在 lock/rename期間、system clock大幅倒退／future timestamp，以及多個 rapid automatic PostModelSwitch 的 ordering尚未有 deterministic coverage。
- Source snapshots是人工 normalized transcription；本 review沒有重新連線比對 2026-09-07 官方頁面內容，只驗證 repository內的 trace/hash一致性與逐筆人工可讀性。
- Passing focused/full suites不覆蓋 findings列出的 orphan-lock recovery、resume/compact unsupported disclosure、oversized state或source-ref mutation。

## Completion assessment and next handoff

Approved Ticket 2目前**不顯示為 complete**：三個 P2 production findings與一個 P3 evidence-test gap尚未關閉；P3 architecture concern需獨立診斷但不應在本 Ticket順手重構。下一步由主流程展示 findings並取得修正授權；核准後交回 `$implement-tdd`，先增加可重現 red tests，再做最小 production/test修正、重跑 focused Claude與full repository suites，並安排新的 independent Review。Ticket 3 的 authenticated exact-host gate仍須在 integration freeze前另行完成。
