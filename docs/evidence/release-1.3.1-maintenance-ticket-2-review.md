# Ask Then Do It 1.3.1 維護 Ticket 2 Review Report

Artifact type: Review Report

Artifact ID: `release-1-3-1-maintenance-ticket-2-review`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Status: Changes Requested

Review label: `independent`

Reviewed inputs: Approved `docs/specs/release-1.3.1-maintenance.md`（requirements 2-7、acceptance criteria 3-8 與 11）、Approved Ticket 2 in `docs/plans/release-1.3.1-maintenance.md`（execution mode `tdd`）、`git diff -- scripts/build_release.py`、`scripts/build_release.py` 的最終 transaction 實作與直接周邊、`tests/release/test_release_transaction.py`、`tests/release/test_release_safety.py`，以及委託方提供的 raw verification results。

Assumptions: 本次 operation 已由上游 canonical resolver 證明為 Full；reviewer 未參與 Ticket 2 實作，且在形成 findings 前未讀取 implementation evidence 的結論；目前工作樹中的 Ticket 2 production diff 與 untracked transaction tests 是受審最終狀態；其他 Ticket 1 變更與使用者 draft 不在本次判定範圍。

Deferred: 未獨立重跑 204-test full discovery；未以真實外部程序持鎖製造 Windows sharing/access failure；same-output concurrency、root-directory swap、版本 identity 與外部 publication 依 Approved Ticket 邊界延後。

Next handoff: `$implement-tdd` 修正下列 P2 並加入會先失敗的 candidate-removal recovery fault-injection test；完成 focused 與 broader verification 後，再交由 fresh `$review-code` reviewer。

## Findings

### P2 - Rollback 移除已上線 candidate 時未套用 bounded retry

觸發條件是至少一個 staged managed output 已成功放入 active output，後續 output 的 forward install 失敗，且 recovery 在移除先前已放入的 candidate 時暫時遇到 Windows `WinError 5`。`replace_managed_path()` 在 `scripts/build_release.py:711` 對 backup、install 與 backup restore 提供 50 次 bounded retry，但 recovery 的 candidate removal 在 `scripts/build_release.py:763-770` 直接呼叫一次 `remove_path()`；該次暫時錯誤立即被記為 recovery failure。獨立 fault injection 設定 removal 前兩次失敗、第三次可成功，實際結果仍是 `remove_attempts=1`、`IncompleteRecoveryError`、`candidate_remains=True`。這不符合 Specification requirement 2-3、acceptance criterion 5 與 7 所要求的 rollback/recovery parity，並使原可自動復原的短暫檔案占用退化為人工復原，雖然現有 preservation 與診斷可避免誤報成功。修正方向是讓此 recovery removal 使用相同 Windows-only allowlist、attempt bound 與 delay contract，並在 `tests/release/test_release_transaction.py` 增加精確 fault injection；目前 `test_recovery_retries_transient_winerror_5_and_restores_prior_release`（`tests/release/test_release_transaction.py:291`）只涵蓋 backup-to-output 的 `os.replace`，無法偵測此缺口。

沒有 P0、P1 或 P3 finding。

## Verification

- 獨立執行 `.venv\Scripts\python.exe -m unittest tests.release.test_release_transaction tests.release.test_release_safety -v`：15/15 passed，8.512 秒。
- 獨立執行 candidate-removal fault injection：forward 第二項以非 allowlisted error 失敗；第一項 recovery removal 設定前兩次 `WinError 5`、第三次成功。觀測為 `IncompleteRecoveryError`、僅 1 次 removal attempt、candidate 仍存在，證實 finding 的 trigger 與 impact。
- 獨立執行 `git diff --check -- scripts/build_release.py tests/release/test_release_transaction.py`：無 whitespace error；只有工作樹 LF/CRLF 轉換警告。
- 已逐行檢查 forward backup、staged install、candidate removal、backup restoration、diagnostic aggregation、`main()` cleanup/preservation 與 unmanaged-output validation 的 state transitions。
- 委託方提供的 raw evidence：focused transaction 9/9、release safety 6/6、三條真實 Windows reproducibility/repeated-build paths 3/3、CPython 3.12.13 + Pillow 12.3.0 無 `PYTHONPATH` full discovery 204/204、`py_compile` 與 `git diff --check` 通過，且無 staging directory 或 Python process 遺留。這些結果未被當作上述 P2 未覆蓋分支的替代證據。

Evidence unavailable: 未獨立重跑完整 204-test suite，也沒有可重現、由外部程序持鎖造成的真實 Windows removal failure；Specification 允許 deterministic injection 作主要證據，因此後者不是完成 gate，但仍是 smoke-evidence gap。

## Architecture And Refactoring Lenses

範圍僅限 Ticket 2 變更及其 transaction 直接影響區，不代表整個 repository 的架構診斷。

1. **Duplicated Code or Policy - `finding`**：rollback 的 backup restoration 經 `replace_managed_path()`，但同一 recovery state transition 的 candidate removal 在 `scripts/build_release.py:763-770` 繞過 retry policy。觸發、影響與位置同 P2；這是局部 policy 分裂，而非可忽略的樣式差異。
2. **Long Function - `no-finding`**：`commit()` 雖包含 forward 與 recovery 約 68 行，但控制流仍聚焦單一 transaction，狀態清單與錯誤聚合可直接追蹤；除 P2 外未見長度造成的獨立 correctness 或 maintenance defect。
3. **Large Module or Class - `no-finding`**：新增內容仍屬 release builder 的既有 validation/build/commit 責任，`IncompleteRecoveryError` 只承載窄範圍 recovery state；本變更未加入無關 ownership。
4. **Long Parameter List - `no-finding`**：`replace_managed_path()` 只有 source/target，`commit()` 的四個參數對應 transaction 必要輸入；error class 的 keyword-only fields 是一次完整診斷狀態，未形成不穩定呼叫介面。
5. **Data Clumps - `no-finding`**：primary error、recovery errors 與三個 recovery paths 已集中於 `IncompleteRecoveryError`，沒有在多個介面重複散傳同組 primitives。
6. **Primitive Obsession - `no-finding`**：attempt count、delay 與唯一核准的 `winerror == 5` 以具名常數及明確平台 guard 表達；目前單一 allowlisted code 不足以要求額外 domain type。
7. **Feature Envy - `not-applicable`**：受審區是 procedural filesystem transaction，沒有相鄰 domain object 或 class ownership 可供比較；函式只操作自己的 path/state inputs 與標準 filesystem API。
8. **Divergent Change - `no-finding`**：本 diff 的新增責任均由同一原因驅動，即 Windows managed-output transaction 的 retry、recovery diagnosis 與 preservation。
9. **Shotgun Surgery - `no-finding`**：三個 `os.replace` 方向共用單一 helper，平台與 retry 參數集中；P2 是 policy coverage 遺漏，不是一次政策變更必須跨多個不相關模組修改。
10. **Message Chains - `not-applicable`**：受審流程沒有跨多層 collaborator/object navigation；path 組合與 exception chaining 都是直接操作。
11. **Leaky Abstraction - `finding`**：`replace_managed_path()` 只封裝 replace 型 rollback，caller 仍須自行知道 candidate removal 也是同一 rollback retry contract，因而在 `scripts/build_release.py:763-770` 漏套 policy。觸發與使用者影響同 P2，修正應讓 recovery operation boundary 明確涵蓋 removal，而不是要求 caller 補償 helper 的隱含限制。
12. **Shallow Module - `no-finding`**：retry helper 雖介面小，實際隱藏 Windows platform 判斷、allowlist、50-attempt bound 與 delay，抽象收益足夠；structured recovery error 也有效封裝 preservation diagnostics。

## Residual Risks And Untested Areas

- 成功 commit 與成功 recovery 之後的最終 `shutil.rmtree(staging)` 沒有 transient file-lock fault injection；現有 main/legacy paths 證明一般 cleanup，但沒有證明 cleanup 本身遭遇短暫 Windows error 的行為。
- 非 Windows 不 retry 由 `IS_WINDOWS=False` 的 deterministic test 證明，未在真正非 Windows kernel 上重跑。
- attempt-only bound 是每個 filesystem operation 最多 50 次、每次間隔 0.1 秒；它是有限且明確的，但真實持鎖期間的 operator experience 只有無 fault 的 Windows smoke evidence。
- same-output concurrency 仍依 Approved Ticket 的 serial-only boundary，不是本 Review 的 coverage。

## Completion Assessment

Approved Ticket 2 **尚未完成**。Retry eligibility、boundedness、diagnostics、成功 recovery、incomplete-recovery preservation、unmanaged collision 與既有 release safety 大部分均有一致實作及測試證據；然而 P2 使一個必要 rollback operation 未遵守相同 retry contract，也缺少能拒絕該回歸的 deterministic test。修正並重跑 affected focused/broader gates 後才適合重新進入 independent Review。
