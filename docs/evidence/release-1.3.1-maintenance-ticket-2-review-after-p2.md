# Ask Then Do It 1.3.1 維護 Ticket 2 P2 修正後 Review Report

Artifact type: Review Report

Artifact ID: `release-1-3-1-maintenance-ticket-2-review-after-p2`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `2 - 讓 Windows replacement 與 recovery 可重試、可復原、可診斷`

Execution mode: `tdd`

Status: Complete - no actionable findings

Review label: `independent`

Reviewed inputs: Approved `docs/specs/release-1.3.1-maintenance.md` 的 requirements 2-7、acceptance criteria 3-8 與 11；Approved Ticket 2 in `docs/plans/release-1.3.1-maintenance.md`；初始 `docs/evidence/release-1.3.1-maintenance-ticket-2-review.md` 的 P2 trigger；`git diff -- scripts/build_release.py`；`scripts/build_release.py` 的最終 transaction 實作與直接周邊；`tests/release/test_release_transaction.py`、`tests/release/test_release_safety.py` 與相關 release contracts；委託方提供的 raw correction verification。

Assumptions: 本次 operation 已由上游 canonical resolver 證明為 Full；Approved Ticket mode 是 `tdd`；fresh reviewer context 未參與 Ticket 2 設計或實作，且形成 findings 前未讀取 implementation evidence conclusions；工作樹中的 production diff 與 transaction tests 是受審最終狀態；Ticket 1 變更與使用者 draft 不在本次判定範圍；同一 output root 仍只支援單一 serial builder。

Deferred: same-output concurrency lock、root-directory swap、`1.3.1` identity/package integration、final release evidence、其他 Windows error allowlist、通用 error framework 與所有 external publication actions 依 Approved Ticket 邊界延後。

Next handoff: Ticket Plan owner 可接受本 Review、將 Ticket 2 標記完成，並依 dependency order 交付 Ticket 3；本 Review 不修改 Plan 或 production artifacts。

## Findings

**沒有 actionable findings。** 沒有 P0、P1、P2 或 P3 finding。

初始 P2 已關閉。原缺口是 recovery 移除已上線 candidate 時直接呼叫單次 `remove_path()`；目前 `scripts/build_release.py:772-779` 改由 `remove_managed_path()` 執行，而 `scripts/build_release.py:731-732` 將該 operation 委派給與 replacement 共用的 `retry_managed_output_operation()`。精確 correction test 在 `tests/release/test_release_transaction.py:294-344` 令前兩次 removal 拋出 `WinError 5`、第三次成功，並斷言 3 attempts、2 sleeps、prior bytes 完整恢復、backup 清空，且結果不是 `IncompleteRecoveryError`。若 candidate removal 再次繞過 helper，該測試會失敗。

共用 retry boundary 沒有擴張 eligibility。`scripts/build_release.py:712-724` 只在 `IS_WINDOWS` 為真、`getattr(exc, "winerror", None) == 5` 且尚未到最後一次 attempt 時等待並重試；非 Windows、其他 `winerror`、沒有 `winerror` 的未知 `OSError` 與最後一次 failure 都立即向外拋出。50 次 total attempts 與 0.1 秒 delay 集中於 `scripts/build_release.py:40-42`。目前 helper 只由 managed-output replacement 與 rollback candidate removal 的窄 wrapper 呼叫，未包住 staging validation、unmanaged-output validation 或一般 cleanup。

## Behavior And State-Transition Review

- Staging 先完成完整 inventory、checksum、ZIP 與 source-equivalence validation，既有 output 再經 unmanaged/incomplete collision 驗證，之後才進入 commit，見 `scripts/build_release.py:474-527`、`scripts/build_release.py:530-573` 與 `scripts/build_release.py:843-857`。Retry correction 沒有跳過或放寬這些 gates。
- 舊 managed outputs 移入 backup 與 staged outputs 上線均使用 `replace_managed_path()`，見 `scripts/build_release.py:753-766`；兩個方向與 restore 共享相同 platform、allowlist、attempt 與 delay policy。
- Forward failure 保留精確 operation、absolute source、absolute target 與原始 `OSError`，見 `scripts/build_release.py:767-770`。每個已完成 operation 只有在成功後才加入 `moved_old` 或 `placed_new`，因此 recovery 不會處理尚未完成的 state transition。
- Recovery 先反向移除已上線 candidates，再反向恢復所有已移入 backup 的 prior outputs；每個 operation 即使失敗仍會繼續收集後續 recovery 結果，見 `scripts/build_release.py:772-790`。Candidate removal 與 backup restoration 現均遵守相同 bounded retry contract。
- Recovery 完整成功時，`commit()` 仍以一般 `BuildError` 明示 candidate 未提交且 pre-build state 已恢復，見 `scripts/build_release.py:799-802`；`main()` 回傳非零並在 `finally` 清除 transaction staging，見 `scripts/build_release.py:863-869`。
- Recovery 不完整時，`IncompleteRecoveryError` 同時保存 primary error、全部 recovery errors、output root、staging 與 backup absolute paths，見 `scripts/build_release.py:70-94` 與 `scripts/build_release.py:791-798`；`main()` 只對此窄 error type 保留 staging，沒有將 active output 誤報為成功。
- Output root 被限制在 repository 內，非 default output 需要明確 test opt-in，managed target 也再次檢查不得逃離 output root，見 `scripts/build_release.py:742-745` 與 `scripts/build_release.py:811-818`。既有 output 的 symbolic links、unmanaged 或不完整 inventory 會在 commit 前失敗，見 `scripts/build_release.py:530-545`。Correction 未擴張 destructive boundary，也未新增 network、credential 或 publication 行為。

上述控制流符合 Specification requirements 2-7 與 acceptance criteria 3-8、11。成功、forward failure with successful recovery、recovery transient success、recovery final failure、prior upgrade、repeated build、failed rebuild 與 unmanaged collision 均有直接或 broader test evidence。

## Architecture And Refactoring Lenses

本節只評估 Ticket 2 change 與 release transaction 的直接影響區，不代表 repository-wide architecture diagnosis。

1. **Duplicated Code or Policy - `no-finding`**：replacement 與 candidate removal 的 Windows eligibility、attempt bound 與 delay 已集中於唯一 `retry_managed_output_operation()`；兩個 operation wrapper 只投影 filesystem call，見 `scripts/build_release.py:712-732`。初始 Review 的局部 policy split 已關閉。
2. **Long Function - `no-finding`**：`commit()` 位於 `scripts/build_release.py:735-802`，雖同時呈現 forward 與 recovery，但整段只負責單一 transaction；`moved_old`、`placed_new`、primary/recovery error 的狀態可線性追蹤，未見長度造成的獨立 correctness 或 maintenance defect。
3. **Large Module or Class - `no-finding`**：新增 helper、窄 error type 與 recovery logic 均留在既有 release builder 的 validation/build/commit ownership；correction 沒有引入無關責任或新的跨模組耦合。
4. **Long Parameter List - `no-finding`**：retry helper 接受一個 operation，replace/remove wrappers 各只有必要 path 參數，`commit()` 的四個參數直接對應 transaction inputs，見 `scripts/build_release.py:712-741`。
5. **Data Clumps - `no-finding`**：primary error、recovery errors 與三個 recovery paths 已由 `IncompleteRecoveryError` 集中承載，見 `scripts/build_release.py:70-94`；同組資料沒有在多個呼叫介面散傳。
6. **Primitive Obsession - `no-finding`**：attempt count 與 delay 使用具名常數，唯一核准的 Windows code 以明確 `winerror == 5` policy 表達，見 `scripts/build_release.py:40-42`、`scripts/build_release.py:718-724`。目前只有單一 allowlisted code，不需要額外 domain type。
7. **Feature Envy - `not-applicable`**：受審區是 procedural filesystem transaction，沒有相鄰 domain object 或 class ownership 可供搬移；函式只操作自身 path/state 與標準 filesystem API。
8. **Divergent Change - `no-finding`**：本 Ticket 新增行為都由同一變更原因驅動，即 managed-output retry、recovery diagnosis 與人工復原資料 preservation；P2 correction 只補齊同一 transaction policy。
9. **Shotgun Surgery - `no-finding`**：eligibility、attempt 與 delay 的政策變更只需修改共用 helper/常數；replace 與 remove wrappers 已共用它，見 `scripts/build_release.py:40-42`、`scripts/build_release.py:712-732`。
10. **Message Chains - `not-applicable`**：受審流程沒有跨多層 collaborator 或 object navigation；path resolution、filesystem calls 與 exception chaining 都是直接操作。
11. **Leaky Abstraction - `no-finding`**：caller 不再需要自行知道 candidate removal 應複製 replacement retry contract；`remove_managed_path()` 與 `replace_managed_path()` 都封裝同一 policy，見 `scripts/build_release.py:727-732`。初始 Review 的 abstraction leak 已關閉。
12. **Shallow Module - `no-finding`**：retry helper 的介面雖小，但實際隱藏 Windows platform guard、error allowlist、50-attempt bound 與 delay；`IncompleteRecoveryError` 也封裝 recovery preservation diagnostics，兩者皆有足夠抽象收益。

沒有 cross-module 或 systemic architecture finding，因此不需要交由 `$improve-architecture` 建立診斷。

## Verification

獨立執行並觀測：

- P2 correction focused command：`1/1` passed，0.023 秒。
- Transaction 與 release safety：`16/16` passed，8.952 秒。
- 執行前確認 process environment 沒有 `PYTHONPATH`；以 project `.venv` 跑完整 discovery：`205/205` passed，20.175 秒。
- Project `.venv` 為 CPython 3.12.13、Pillow 12.3.0，Pillow 由 `.venv/Lib/site-packages` 載入。
- 對 builder、transaction tests 與 safety tests 做 in-memory syntax compile：passed。
- `git diff --check -- scripts/build_release.py`：exit 0，只有 Git 的 LF/CRLF warning；三個受審檔案的 trailing-whitespace scan 無結果。
- Repository-root scan 未發現 `.*-release-staging-*`；`Get-Process` executable-path scan 未發現 project `.venv` Python process。
- 最終檔案 SHA-256 snapshot：`scripts/build_release.py` = `E46903E1F0D22019D3BCA01499C470DC6BE6BA99A48E13300CB7B751BBB48B09`；`tests/release/test_release_transaction.py` = `9587B37C68499BCB771C8533802300038556412C18BFF968F86503A6FA12FCBE`；`tests/release/test_release_safety.py` = `1A1F75FCC37A3F886B12E3FCA263DAC52854AAB5147E1C81436DFE0651451B57`。Review 結論與最後一次 `git diff -- scripts/build_release.py` 均以此狀態為準。

委託方提供並在形成獨立 verdict 後以 implementation evidence metadata 交叉核對：

- Correction Red：focused test 在 production correction 前為 `1 failed`，0.020 秒；只執行 1 次 candidate removal 後拋出 `IncompleteRecoveryError`。
- Correction Green：同一 focused test `1/1` passed，0.029 秒；觀測 3 removal attempts 與 2 sleeps。
- Final transaction+safety：`16/16` passed，5.894 秒。
- Final no-`PYTHONPATH` CPython 3.12.13/Pillow 12.3.0 full discovery：`205/205` passed，25.576 秒。
- `py_compile` 與 `git diff --check` 通過；沒有 staging directory 或 project-venv Python process 遺留。

一次探索性 full-discovery 呼叫加入了不符合本 repository package layout 的 `-t .`，因此在 collection 前由 `unittest` 以「start directory is not importable」拒絕。該無效 invocation 未被列為產品測試 failure，也未納入通過證據；隨後以 repository 支援的 `discover -s tests` 完整跑完 205 tests。

## Evidence Unavailable

- 本 fresh Review 沒有重建 correction 前的 Red，因為那需要暫時改回 production code；pre-fix failure 只採用委託方 raw result、初始 independent Review 的 trigger evidence，以及形成 verdict 後核對的 implementation metadata。
- 未由外部程序製造真實 Windows kernel file lock；Specification 明確允許 deterministic fault injection 作主要證據，因此這是 smoke-evidence gap，不是 completion gate。
- 非 Windows immediate-failure branch 由 deterministic `IS_WINDOWS=False` injection 驗證，未在真正非 Windows kernel 執行。
- `Get-CimInstance Win32_Process` 的完整 command-line audit 因作業系統拒絕存取而不可用；較窄的 `Get-Process` executable-path scan 沒有發現 project `.venv` Python process，且所有本次 test sessions 都已結束。

## Residual Risks And Untested Areas

- 真實 external lock 超過 4.9 秒仍會依設計耗盡 retry 並進入 recovery；永久 ACL-related `WinError 5` 因 error code 不可區分，也會等待相同 bounded window。
- 成功 commit 或成功 recovery 後，最終 transaction-staging `shutil.rmtree()` 本身沒有 transient file-lock fault injection；該 cleanup 不是 managed-output replacement/removal retry boundary，初始與本次測試只證明一般 cleanup 路徑。
- same-output concurrency 與 root-directory swap 仍不受本 Ticket 支援；serial-only boundary 未被 correction 改變。
- Exact `1.3.1` identity/package/checksum integration 與 final release evidence 屬後續 Tickets；本 Review 只判定 Ticket 2 transaction behavior，未宣告完整 `1.3.1` candidate 或公開 release。

## Completion Assessment

Approved Ticket 2 **appears complete**。Approved `tdd` mode 已保留；初始 P2 的 deterministic Red/Green 證據存在，fresh focused test 可拒絕 candidate-removal bypass；共用 helper 保持 Windows-only `WinError 5` allowlist 與有限 retry；forward/recovery transitions、成功 recovery、incomplete-recovery diagnostics/preservation、unmanaged collision protection、prior/repeated/failed-build safety 與 broader compatibility 均有一致 production/test evidence。

初始 Review 的 P2、Duplicated Code or Policy finding 與 Leaky Abstraction finding 均可標記 closed。沒有未解 blocker 阻止 Ticket 2 closure。
