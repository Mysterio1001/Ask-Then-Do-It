# Ask Then Do It 1.3.1 Maintenance Ticket 2 Implementation Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `release-1-3-1-maintenance-ticket-2-implementation`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `2 - 讓 Windows replacement 與 recovery 可重試、可復原、可診斷`

Execution mode: `tdd` (`Add tests`, explicitly selected by the user)

Status: Completed

Inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md)、completed [Ticket 1 Implementation](release-1.3.1-maintenance-ticket-1.md) 與 accepted [Ticket 1 Review](release-1.3.1-maintenance-ticket-1-review.md)、[Ticket 2 initial Review](release-1.3.1-maintenance-ticket-2-review.md)、使用者核准的 P2 correction，以及目前 release builder 與 release safety contracts。

Assumptions: 同一 output root 仍只允許單一 serial builder。正式實作平台是 Windows；跨平台 immediate-failure branch 以 deterministic platform injection 驗證。`WinError 5` 無法區分短暫占用與永久 ACL，因此只在 Windows 套用相同的有限 retry policy。

Deferred: same-output concurrency lock、其他 Windows error allowlist、通用錯誤框架、progress UI、builder 全面重構、`1.3.1` identity/package integration（Ticket 3）、final release evidence（Ticket 4），以及全部 external publication actions。

Handoff: Fresh independent [P2 closure Review](release-1.3.1-maintenance-ticket-2-review-after-p2.md) completed with no actionable findings。Ticket 2 可接受並依 dependency order 交付 Ticket 3；不授權任何 external publication action。

Approval: Implementation authority comes from the Approved Ticket Plan and its approved `tdd` mode.

## Outcome

- Managed-output transaction operations 共用同一 policy：舊輸出移入 backup、staged output 上線、rollback candidate removal 與 prior-output restoration。
- Policy 是 Windows `WinError 5` 最多 50 次 total attempts、每次失敗後固定等待 0.1 秒，單一 operation 最長等待 4.9 秒；非 Windows、其他 `winerror` 與未知 `OSError` 第一次即失敗。
- Forward failure 後會移除已上線的新輸出並逐項恢復 prior outputs；成功 recovery 明確回報 candidate 未提交。
- Recovery 會收集 removal/restore failures。若不完整，`IncompleteRecoveryError` 同時保存 primary error、全部 recovery errors、output root、staging 與 backup，且 `main()` 不再刪除人工復原資料。
- 新 deterministic suite 覆蓋 transient success、retry exhaustion、nonallowlisted immediate failure、non-Windows immediate failure、backup parity、forward recovery、candidate-removal retry、restore retry 與 incomplete recovery preservation。

## Files changed

- `scripts/build_release.py`: Windows-only bounded retry、narrow incomplete-recovery error、recovery aggregation、診斷與 conditional staging cleanup。
- `tests/release/test_release_transaction.py`: 9 個 in-process deterministic transaction tests；fault injection 不依賴真實檔案占用。
- 本 evidence 與 Approved Plan 的 Ticket 2 status。
- 未修改 release identity、Core/adapters、consumer packages、default `dist`、Token proxy、CI、lockfile 或文件內容。

## First Red and Green

Command:

`.\.venv\Scripts\python.exe -m unittest -v tests.release.test_release_transaction.ReleaseTransactionTests.test_transient_winerror_5_is_retried_until_replacement_succeeds`

Initial observed result: exit `1`; `Ran 1 test`; `ERROR`。第一次 injected `WinError 5` 直接成為 `BuildError: Atomic release replacement failed`，證明原 builder 沒有 retry。

After adding the single replace helper and applying it to backup/install/restore: exit `0`; `Ran 1 test in 0.262s`; `OK`。

Persistent exhaustion、nonallowlisted failure、forward recovery 與 transient recovery 四個 tests 隨後第一次執行即通過，因為同一個最小 coherent helper 已同時具備 allowlist、bound 與 recovery parity；沒有為了形式製造額外 production failure。

## Incomplete-recovery Red and Green

Command:

`.\.venv\Scripts\python.exe -m unittest -v tests.release.test_release_transaction.ReleaseTransactionTests.test_incomplete_recovery_reports_both_errors_and_recovery_paths tests.release.test_release_transaction.ReleaseTransactionTests.test_main_preserves_recovery_data_after_incomplete_recovery`

Initial observed result: exit `1`; `Ran 2 tests`; one `ERROR` and one `FAIL`。Rollback 的 injected persistent `WinError 5` 直接覆蓋 primary error；`main()` 的 unconditional `finally` cleanup 使預期 staging count 從 1 變成 0。

After adding `IncompleteRecoveryError`, recovery-error aggregation and conditional cleanup: exit `0`; `Ran 2 tests in 1.040s`; `OK`。測試確認 candidate checksum 與 prior checksum 分別保留在 staging/backup，active output 不含完整 checksum set，stderr 同時含兩個 error marker 與兩個 recovery paths。

## Additional Red/Green checks

- Non-Windows Red: injected `IS_WINDOWS=False` + `winerror=5` observed 5 attempts instead of 1；加入 platform guard 後通過。
- Diagnostic Red: successful-recovery error 未包含 `candidate was not committed`；收斂訊息後通過。
- Backup-movement parity test added after the shared helper already existed and passed immediately with 3 attempts、2 sleeps and complete candidate bytes。
- Final focused command: `.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_release_transaction`。
- Final focused result: exit `0`; `Ran 9 tests in 1.182s`; `OK`。

## Real Windows tuning evidence

The deterministic tests patch `time.sleep`, so the real wait window was also exercised by existing subprocess builds:

1. With 5 attempts at 0.1 seconds, full discovery collected 204 tests but three real staged-`codex` replacements exhausted the 0.4-second window.
2. With 20 attempts, a targeted three-test run still observed one real exhaustion in `test_clean_builds_are_byte_reproducible_and_zips_match_directories`; an immediate isolated rerun passed.
3. With 50 attempts, the same three real Windows paths passed: `Ran 3 tests in 9.860s`; `OK`。This became the final bounded policy.

The tuning changed only the attempt constant. Error eligibility stayed Windows `WinError 5` only, and all persistent-failure tests continued to assert exact exhaustion at the configured bound.

## Broader verification

- Existing release safety suite: `.\.venv\Scripts\python.exe -m unittest -v tests.release.test_release_safety` -> exit `0`; `Ran 6 tests in 4.903s`; `OK`。
- Python syntax: `.\.venv\Scripts\python.exe -m py_compile scripts\build_release.py tests\release\test_release_transaction.py` -> exit `0`。
- The first full run used an out-of-date project `.venv` and failed test-module import because Pillow was not installed; this was an environment setup failure, not accepted evidence。
- `.venv` was confirmed CPython 3.12.13 with `include-system-site-packages=false`; `pip install -r requirements-dev.txt` installed Pillow 12.3.0 and retained PyYAML 6.0.3。
- Final full command removed `PYTHONPATH`, set `PYTHONDONTWRITEBYTECODE=1`, and ran `.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p 'test_*.py'`。
- Final full result: exit `0`; `Ran 204 tests in 29.718s`; `OK`。
- `git diff --check`: exit `0`; only existing LF-to-CRLF warnings。
- Repository-root scan found no leftover transaction staging directories; no `.venv` Python/pip process remained running。

## Refactor and scope inspection

The retry code remains one helper and one narrow error type inside the existing builder; no class hierarchy or package-level utility module was introduced. Recovery no longer silently skips a missing backup source: restore attempts surface such a condition as incomplete recovery. Final diff inspection found no identity bump, generated package mutation, unrelated builder refactor, consumer behavior change or publication action。

## Residual risk

A real external lock lasting longer than 4.9 seconds still fails by design and enters recovery; a permanent ACL-related `WinError 5` waits the same bounded window because Windows exposes the same code. Same-output concurrent builds remain unsupported. Deterministic injection covers non-Windows behavior, but this Ticket did not execute the full suite on a non-Windows host. External publication and final `1.3.1` release claims remain unauthorized。

## Approved Review P2 correction

Approval: 使用者在 [initial independent Review](release-1.3.1-maintenance-ticket-2-review.md) 提出 candidate-removal retry P2 後明確回覆「核准」。本段只修正該 finding，不擴張 Ticket 2 範圍。

### Correction Red

Command:

`.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_release_transaction.ReleaseTransactionTests.test_recovery_retries_winerror_5_while_removing_installed_candidate`

Observed result before production correction: exit `1`; `Ran 1 test in 0.020s`; `FAIL`。第一個 candidate 已上線、第二個 install 以 nonallowlisted error 失敗；candidate removal 的前兩次 injected `WinError 5` 原本只執行一次，結果拋出 `IncompleteRecoveryError`，沒有等到第三次可成功的 removal。

### Correction Green and refactor

- 新 `retry_managed_output_operation()` 集中 Windows platform guard、`winerror == 5` allowlist、50-attempt bound 與 0.1-second delay。
- `replace_managed_path()` 與新 `remove_managed_path()` 都只投影各自 filesystem operation，不再複製或漏接 retry policy。
- Recovery candidate removal 改走 `remove_managed_path()`；replace/restore 行為與既有診斷、preservation contract 不變。
- 原本只描述 replace 的常數改名為 `WINDOWS_MANAGED_OUTPUT_*`，tests 同步引用同一 policy identity。

Same focused command after correction: exit `0`; `Ran 1 test in 0.029s`; `OK`。Test observed exactly 3 removal attempts、2 sleeps、prior bytes restored、empty backup，且最終 exception 是原始 forward `BuildError` 而非 `IncompleteRecoveryError`。

### Correction verification

- Affected transaction + safety command: `.\.venv\Scripts\python.exe -B -m unittest -v tests.release.test_release_transaction tests.release.test_release_safety` -> exit `0`; `Ran 16 tests in 5.894s`; `OK`。
- Python syntax check for builder and transaction tests: exit `0`。
- Final no-`PYTHONPATH` full discovery: exit `0`; `Ran 205 tests in 25.576s`; `OK`。
- `git diff --check`: exit `0`; only existing LF-to-CRLF warnings。
- Final scan found no transaction staging directory and no project-venv Python process left running。

Correction closure: fresh independent [Review after P2](release-1.3.1-maintenance-ticket-2-review-after-p2.md) reran focused `1/1`、transaction+safety `16/16` 與 full discovery `205/205`，reported no actionable findings，並判定 initial P2 closed、Ticket 2 appears complete。
