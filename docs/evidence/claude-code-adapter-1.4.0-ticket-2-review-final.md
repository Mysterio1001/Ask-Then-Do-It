# Claude Code Adapter 1.4.0 — Ticket 2 Final Independent Review Report

Artifact type: `Review Report`

Artifact ID: `claude-code-adapter-1-4-0-ticket-2-review-final-independent`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Review label: `independent`

Status: `changes-requested`

Ticket mode: `tdd`

Reviewed inputs: Approved `docs/requirements/claude-code-adapter-1.4.0.md`; Approved `docs/specs/claude-code-adapter-1.4.0.md`; Approved Ticket 2 in `docs/plans/claude-code-adapter-1.4.0.md`; current working-tree `adapters/claude-code/plugin/ask-then-do-it/{scripts/router.mjs,hooks/hooks.json,config/model-classifications.json,skills/*/SKILL.md}`; `scripts/validate_claude_plugin.py`; `scripts/validate_claude_model_evidence.py`; scoped `tests/claude/test_router_*.py`, `tests/claude/test_model_classification_evidence.py`, `tests/claude/test_public_plugin_contract.py` and relevant fixtures; Draft `docs/evidence/claude-code-adapter-1.4.0-ticket-2-architecture-diagnosis.md`; supplied raw verification. Only after forming and probing the independent view, this review read `docs/evidence/claude-code-adapter-1.4.0-ticket-2-review.md` and the raw chronology in `docs/evidence/claude-code-adapter-1.4.0-ticket-2.md` to assess closure.

Assumptions: top-level mode was already proven `full` by the Approved Plan and existing Full/TDD workflow; reviewer capability is `multi_agent + tools`; this fresh reviewer context did not implement Ticket 2 and was not given an implementer verdict before reviewing raw artifacts; the working-tree adapter and evidence are untracked, so there is no Git base diff for the new files and the review instead inspected the complete scoped artifacts; exact authenticated host behavior remains provisional under the Approved Ticket 2→3 sequencing exception.

Deferred: authenticated exact Claude Code `2.1.251` command identity, `command_source`, `additionalContext`, Node missing/nonzero/exit-2/timeout behavior and operation ordering remain Ticket 3; General／Claude 5 profile modules, paired conformance, context proxy, lifecycle documentation, release integration and live smoke remain downstream Tickets; no architecture refactor is authorized by this Review.

Next handoff: return the actionable findings to the Full/TDD implementation stage. Add failing regressions before the smallest scoped fixes, rerun focused and full verification, and request another fresh independent Review. The existing Draft architecture diagnosis remains diagnostic-only and requires a future Specification/Plan gate before any refactor.

## Findings

### [P2] 最後一次 stale-lock 回收成功後會在沒有 ownership 的情況下執行受保護 callback

Trigger: `withSessionLock`在每次`EEXIST`後若`tryRecoverStaleLock`成功就執行`continue`；若成功發生在`attempt === retryCount`的最後一次iteration，loop直接結束，`ownerToken`仍是`undefined`，但函式仍進入`try`並執行callback。Default production path可在一個原本尚不可回收的dead lock恰於約1秒retry window最後一次嘗試跨過lease＋grace門檻時觸發。Temporary probe以`retryCount: 0`及可安全回收的expired/dead lock精確重現：第一個callback觀察到lock不存在，且在其尚未結束時第二個contender成功取得同一session lock並進入callback（`firstSawLock: false`, `secondEntered: true`）。Impact: SessionStart、UserPromptExpansion或PostModelSwitch可在未持有互斥ownership時和另一handler同時讀寫同一state；atomic rename只能避免partial JSON，不能避免lost update、operation binding被覆蓋或switch transition順序被破壞。Remediation direction: recovery後必須重新嘗試並成功建立owned record才能執行callback；loop耗盡時一律fail closed，且加入last-attempt recovery與concurrent contender regression。Location: `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:874`–`:898`，特別是`:884`–`:885`與`:893`–`:894`。

### [P2] 非fatal stdin UTF-8 decode會把不同raw session IDs合併到同一state owner

Trigger: `readStdin`對raw bytes使用`Buffer.concat(chunks).toString("utf8")`；Node會以U+FFFD取代非法UTF-8而不拒絕。分別在JSON的`session_id`字串放入raw byte`0xFF`與`0xFE`的兩個SessionStart probes皆被接受，並只產生同一個SHA-256 filename`83d544…b097.json`，因兩者都先正規化成相同的`"�"`再hash。Impact: malformed但不同的hook session identities可cross-contaminate同一routing state，違反每個action驗證raw structured input、hash exact session identity及cross-session isolation的安全契約；後續operation/model state可被另一raw identity覆寫。Remediation direction: 對stdin bytes使用fatal UTF-8 decoder並在JSON解析前拒絕任何ill-formed sequence；新增至少兩組會replacement-collide的raw-byte tests，確認不建立state。Location: `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1387`–`:1404`，特別是`:1398`。

### [P2] Node 18／19 在版本 gate 前執行不存在的 API，explicit `-5` 無法取得核准的 manual fallback

Trigger: 在 Claude Code version 已受支援、系統有 Node 18 或 19、使用者執行 `/ask-then-do-it:ask-then-do-it-5` 時，`main` 先讀取並驗證 event，`requireString` 會呼叫該 runtime 沒有的 `String.prototype.isWellFormed()`，之後才執行 `checkNodeVersion(process.versions.node)`。該 `TypeError` 被轉成 `internal-error` failure envelope，而不是 `node-too-old`。Explicit Skill 對 `internal-error` 必須停止，只有 valid `node-too-old` envelope 才可揭露限制後使用 manual optimized path，因此 Node `<22` 路由矩陣在仍可啟動 JavaScript router 的舊 LTS runtime 上不成立。以目前 Node runtime刪除`String.prototype.isWellFormed`並將`process.versions.node`設為`18.20.8`的temporary probe，對有效explicit event穩定得到`entry: /ask-then-do-it:ask-then-do-it-5`、`routing_status: failure`、`disclosure_code: internal-error`。現有Node 21 test只在較新runtime覆寫version字串，沒有模擬舊runtime API surface。Impact: 使用者無法使用Specification特別保留的Node-too-old explicit manual path，且錯誤會被誤報成router internal failure。Remediation direction: 在使用任何不保證存在於舊Node的API前完成可保留entry identity的版本判定，或讓前置event parsing/validation只使用足以在所有欲辨識`node-too-old`的runtime執行的語法/API；加入實際舊runtime或等價API-surface regression。Location: `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:203` and `:1413`–`:1418`; current incomplete coverage at `tests/claude/test_router_contract.py:369` and `:400`.

### [P3] Source-trace validator沒有把trace metadata綁回canonical mapping，且boolean schema version被當成整數接受

Trigger: 保持production mapping不變，將temporary trace的`mapping_path`改成其他provider路徑、把trace與全部source的`checked_on`改為`2099-12-31`、把全部source URLs和snapshot headers改成`https://example.invalid/not-anthropic`，再更新snapshot hashes；`validate(mapping, trace)`仍回傳空errors。另一probe只將`schema_version`改成JSON boolean `true`也回傳空errors，因Python的`True == 1`。Validator只把`mapping_sha256`綁到傳入mapping bytes，逐snapshot驗證的是trace自我宣稱的URL/date/hash，沒有比較`trace.mapping_path`、`trace.checked_on`及`trace.sources[*].{url,checked_on}`與mapping中的canonical evidence metadata，也沒有做exact integer type check。Impact: current checked-in trace內容本身正確，runtime mapping亦由Plugin validator固定，因此沒有直接routing風險；但獨立model-evidence CLI可讓來源身份、查核日期與schema type漂移後仍宣告valid，削弱Ticket要求的dated official-source provenance與closed schema。Remediation direction: 驗證canonical `mapping_path`，要求trace date/source inventory/URL/date與mapping metadata完全一致，並以`type(value) is int`固定schema version；加入source URL/date/path mismatch及boolean-version mutations。Location: `scripts/validate_claude_model_evidence.py:89`–`:127`，特別是`:97`–`:109`。

### [P3] 合法上限的`model_generation`會在下一次transition被寫成不安全整數

Trigger: 將一份其餘欄位均valid、same-session的state設為`model_generation = Number.MAX_SAFE_INTEGER`。`validateState`接受該值；下一個requested `PreModelSwitch`計算`next_generation = state.model_generation + 1`並成功寫入`9007199254740992`，使剛寫入的state不再符合自己的safe-integer schema，下一次public entry因`state-invalid`停止。`SessionStart`需要增加generation以及沒有Pre的automatic/resume `PostModelSwitch`也使用相同unchecked increment。Impact: 需要crafted/corrupted local state或不可能的長期合法計數才觸發，故屬minor；但Specification把state視為untrusted，router不應把已通過validation的state轉成自己拒絕的格式，結果是持久same-session denial until reset/repair。Remediation direction: 在每個generation increment前做checked increment/headroom validation，於任何寫入前以closed transition failure停止，並新增三個increment path的boundary cases。Location: acceptance in `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:947`，unchecked increments at `:1191`, `:1307`, and `:1361`.

## Prior finding closure

- Prior P2 orphan lock／hook-timeout finding: `closed` for its exact permanent-orphan／five-second trigger. Current lock records carryowner token、PID、lease/grace；recovery requires an expired record and definitely-dead owner；release is token-aware；Pre usesno-wait/no-reclaim。The 10 review-regression tests, including stale recovery, concurrent reclaim and live/malformed non-reclaim, passed. The new last-attempt ownership P2 above is a distinct defect introduced/exposed by that recovery implementation and is not covered by the existing tests.
- Prior P2 resume/compact unsupported disclosure finding: `closed`. Both preserved-binding paths now call `continuationContext(..., state.model_classification === "unsupported")`; the focused regression passed.
- Prior P2 unbounded state read finding: `closed`. Mapping/state/lock reads are bounded at64 KiB／16 KiB／1 KiB with handle-level bounds and fatal UTF-8 decoding; exact-limit, oversized and growing-file regressions passed.
- Prior directly fixable P3 source-reference finding: `closed` for its exact wrong-ref/deleted-row trigger. The new validator verifies that at least one referenced snapshot contains the exact model ID and matching active/retired row, and both mutation cases passed. The new metadata-binding P3 above is distinct.
- Prior architecture P3: correctly remains in `docs/evidence/claude-code-adapter-1.4.0-ticket-2-architecture-diagnosis.md` with `Status: Draft`. Large Module、Divergent Change、Data Clumps／Primitive Obsession、Shotgun Surgery及Leaky Abstraction remain diagnostic findings/proposals only; they neither authorize refactoring nor count as accepted architecture work.

## Verification performed

- Independently read the approved requirements, full Specification and Approved Ticket 2 before reading any prior Ticket 2 review/conclusion; retained Ticket mode `tdd`.
- Read the complete 1,482-line router and direct hooks/mapping/Skill/validator/test boundaries. Because the new adapter files are untracked, no meaningful Git base diff exists for them; complete scoped files were treated as the review surface.
- Ran `\.venv\Scripts\python.exe -m unittest discover -s tests\claude -p 'test_*.py' -v`: exit `0`; `Ran 79 tests in 58.582s`; `OK (skipped=1)`. The only skip was Windows regular-file symlink privilege; the real directory-junction test passed.
- Ran both validators with the repository virtual environment: Claude Plugin validator passed; Claude model classification evidence validator passed.
- Ran `node --check adapters\claude-code\plugin\ask-then-do-it\scripts\router.mjs`: exit `0`, no output.
- Ran the full repository suite once: `Ran 295 tests in 92.745s`; `FAILED (failures=2, skipped=1)`. Both failures were transient Windows `WinError 5` atomic release-replacement errors in Codex/release tests outside Ticket 2. Immediately rerunning exactly those two tests produced `Ran 2 tests in 1.217s; OK`; a subsequent clean full-suite rerun produced `Ran 295 tests in 78.623s; OK (skipped=1)`. The initial raw failure remains recorded rather than being rewritten as a pass.
- Ran the Node-old-API probe described in P2: valid explicit event produced `internal-error`, confirming the control-flow defect.
- Ran the source-trace metadata mutation described in P3: validator returned `[]`, confirming it accepted the drift.
- Ran the maximum-safe generation mutation described in P3: Pre wrote`pending/9007199254740992`; the next automatic expansion returned`state-invalid`.
- Ran a last-attempt stale-lock recovery probe with a nested contender: the protected callback observed no lock and the contender entered concurrently, confirming absent ownership.
- Ran two raw-byte stdin probes whose only session-ID difference was illegal byte`0xFF` versus`0xFE`: both SessionStart events were accepted and resolved to the same state filename.
- Ran a source-trace schema mutation with`schema_version: true`: the evidence validator returned no errors.
- Supplied but not independently repeated as authenticated evidence: exact local Claude Code binary reports`2.1.251`; canonical Plugin and repository Marketplace `plugin validate --strict` both exit `0` with no warning. These results prove schema acceptance only, not an authenticated invocation/session contract.

## Evidence unavailable / deferred checks

- No authenticated exact Claude Code `2.1.251` session evidence yet proves the two runtime command identities, `command_source`, same-invocation `additionalContext`, bare alias observation, or Node missing/nonzero/exit-2/timeout host semantics. Ticket 3 remains a local `1.4.0` completion hard gate.
- Exact Claude Code `2.1.251` required/optional hook-field inventory and the closed set, if any, for`permission_mode` remain provisional. The Approved Specification requires the fields actually used for routing plus bounded/type-safe handling of other untrusted input, but current approved repository fixtures do not establish that omitted`transcript_path`／`cwd`／`permission_mode` must be rejected or that an unknown bounded`permission_mode` changes routing. This candidate is therefore`unverified`, not an actionable finding; Ticket 3 must reconcile exact host observations before freeze.
- `claude-mythos-5` appears in none of the four Approved dated model-source snapshots (`models-overview`, `model-ids-and-versions`, `model-deprecations`, `claude-code-model-config`). No approved repository evidence available to this review establishes it as an active canonical ID at the 2026-09-07 freeze, so omission from the mapping is`unverified`, not a finding. If later official evidence establishes it existed at freeze, the mapping/evidence/spec gate must be reopened rather than silently expanded here.
- An actual Node 18/19 binary was not present in this review environment. The P2 is established by source ordering plus an adversarial probe that removed the absent API and set the version to18.20.8; a real-old-runtime regression remains required as correction evidence.
- Windows file symlink creation was unavailable (`WinError 1314`); directory junction protection passed. macOS/Linux filesystem behavior and link/path TOCTOU were not live-tested here.
- The source snapshots were not re-fetched from the network. This review verified current repository consistency and the validator's mutation behavior, not the truth of external pages on 2026-09-07.
- The full suite had two transient non-Ticket-2 Windows release replacement failures on the first personal run; their exact rerun and the subsequent complete 295-test rerun passed. The transient filesystem behavior remains a raw environmental observation, not a Ticket 2 finding.
- General／Claude 5 workflow profiles are not implemented in Ticket 2, so model-visible execution of disclosure codes and profile-equivalence behavior remains downstream evidence.

## Twelve Architecture and Refactoring Lenses

| # | Lens | Outcome | Evidence |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `finding` | Dated source identity is repeated in mapping and source trace, but the model-evidence validator does not reconcile the two copies; concrete trigger/impact/location are the source-trace P3 above. Other router/Skill/validator repetition remains intentional defense-in-depth and currently agrees. |
| 2 | Long Function | `no-finding` | `parseJsonStrict`, `validateState` and `main` are substantial, but each has a traceable single role; the confirmed defects arise from boundary ordering/validation rather than one mixed, unreviewable function. |
| 3 | Large Module or Class | `finding` | `router.mjs` is 1,482 lines and owns parsing, host schema, mapping, filesystem/locking, state, handlers and output. Trigger is any local change across these independent concerns; impact is broad review/regression radius; location `router.mjs:1`. This is already routed to the existing Draft architecture diagnosis and is not an authorized Ticket 2 refactor. |
| 4 | Long Parameter List | `no-finding` | Handler and lock interfaces have short argument lists; no current defect is caused by unstable long-call coordination. |
| 5 | Data Clumps | `finding` | `entry/classification/profile` travel together through tuple sets,operation state and success-envelope arguments; adding/changing a route can diverge these projections. Evidence/location and improvement proposal are recorded in Draft architecture finding A4; no current tuple drift was found. |
| 6 | Primitive Obsession | `finding` | Route decisions, statuses, errors and generation are primitive strings/numbers. The unchecked maximum-safe counter transition and nonfatal conversion of raw identity bytes into a JavaScript string are concrete consequences; the wider route-decision concern remains in Draft A4. |
| 7 | Feature Envy | `not-applicable` | Reviewed production is a functional/procedural module rather than an object model with methods depending primarily on another object's internals. |
| 8 | Divergent Change | `finding` | Hook schema, model freeze, filesystem safety, state lifecycle and envelope behavior independently modify one router module; impact/location are documented in Draft A1. No refactor is authorized here. |
| 9 | Shotgun Surgery | `finding` | Hook/mapping/envelope changes require coordinated edits across JSON, JavaScript, Python validators, Skills, fixtures and tests. The new source-metadata validation gap demonstrates the risk; broader fan-out is documented in Draft A3/A5. |
| 10 | Message Chains | `not-applicable` | Runtime uses direct function calls/plain records and does not expose a long navigation chain to callers. |
| 11 | Leaky Abstraction | `finding` | Host timeout policy and low-level lock retry/recovery loop semantics remain coupled across`hooks.json` and `main`; the last-attempt recovery P2 shows callback safety depends on an unstated loop postcondition. The Node-old-API P2 separately shows runtime capability assumptions leaking ahead of the version boundary. Draft A2 remains diagnostic-only. |
| 12 | Shallow Module | `no-finding` | Four hook actions hide substantive classification, state, concurrency and failure policy; the interface is materially simpler than the implementation it protects. |

## Residual risks and untested areas

- Ticket 3 authenticated host behavior can still invalidate the provisional command matcher, envelope visibility or failure assumptions; strict schema validation does not close this risk.
- Automatic/resume PostModelSwitch ordering before commit remains best-effort by approved host limitation; rapid/out-of-order observations are not independently live-verified.
- File-link TOCTOU, forced process termination during lock/rename, PID reuse and system-clock anomalies remain residual filesystem topics. The Draft architecture diagnosis records them without granting scope.
- Hard-link lock publication passed on this Windows/NTFS environment, but other supported OS/filesystem combinations were not live-tested.
- Current mapping/source artifacts are internally consistent, but the independent validator metadata gap means future evidence drift is not fully rejected until the P3 is fixed.
- Exact required-field and`permission_mode` semantics remain unavailable until Ticket 3; accepting currently unused optional strings has no demonstrated routing impact in the approved evidence, but exact-host drift could require a later schema correction.
- No approved dated fixture supports`claude-mythos-5`; its status at the mapping freeze remains unavailable rather than presumed absent or active.

## Completion assessment

Approved Ticket 2 does **not** appear complete. The prior three P2 findings and prior directly fixable P3 are closed for their exact triggers, and the architecture P3 is correctly retained as an unapproved Draft diagnosis. The current actionable inventory is **three P2** findings (last-attempt lock ownership, malformed UTF-8 session collision, Node-old manual fallback) and **two P3** findings (source-trace metadata/schema binding, generation safe-integer overflow). Ticket 2 should return to TDD correction and another fresh independent Review before dependent Tickets treat it as passed.
