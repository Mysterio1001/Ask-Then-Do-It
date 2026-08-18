# Ask Then Do It 1.3.1 發布可靠性維護 Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `release-1-3-1-maintenance-plan`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Status: Approved

Inputs: Approved [Ask Then Do It 1.3.1 發布可靠性維護 Specification](../specs/release-1.3.1-maintenance.md)、Approved revised [Requirement Decision Record](../requirements/release-1.3.1-maintenance.md)、Approved Project Knowledge Base、目前 repository architecture、release builder、release safety tests、dependency manifest 與 `1.3.0` release evidence。

Assumptions: 同一 output directory 只由單一 builder 串行寫入。正式驗證 baseline 是 CPython 3.12 與 `Pillow>=12.3,<13`。本機 `dist` 可被 `1.3.1` candidate 取代，但已發布 `v1.3.0` assets、Approved historical artifacts 與其記錄 hashes 不可修改。

Deferred: 精確 retry count/interval/backoff、除 `WinError 5` 外的 allowlisted Windows errors、implementation、Git tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement。

Handoff: 從 Ticket 1 的 Approved `tdd` mode 交給 `$implement-tdd`，完成後交獨立 `$review-code`。

Approval: 使用者於 2026-08-17 在四張 Ticket 全部選擇 Add tests、映射為 `tdd`，且完整 Plan 與 planning Knowledge Base Change Summary 展示後，明確聯合回覆「核准」。

## 共同範圍與規劃原則

- 只交付 Pillow development/test dependency、Windows serial replacement/recovery reliability，以及完成 `1.3.1` 本機 candidate 所需的 lockstep identity、packages、checksums、validation 與 evidence。
- 不支援 same-output concurrent builders，不加入 lock/stale-lock contract。
- 不修改 Token proxy algorithm、fixture、fingerprint、normalization 或 60% threshold；既有 required gate 原樣執行。
- 不建立 CI、dependency lock/constraints，不全面重構 builder，不擴充 README 或 guides 的內容；文件只更新必要的 current version identity 與 URLs。
- 每張 implementation Ticket 完成後交給獨立 `$review-code`。Review finding 必須回原 owning Ticket 修正，不得在後續整合或 evidence Ticket 暗中修補。
- 最終 external publication 不在本 Plan；完成本機 candidate 後停止並等待另一個明確核准。

## Ticket 1 - 讓 development dependency manifest 可獨立支撐完整測試

Status: Completed. Evidence: [Ticket 1 Implementation](../evidence/release-1.3.1-maintenance-ticket-1.md); [Ticket 1 independent Review](../evidence/release-1.3.1-maintenance-ticket-1-review.md) (`complete - no actionable findings`).

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。Pillow 漏列已讓完整 test collection 反覆依賴工作環境中的 bundled copy；一個小型 manifest contract test 成本低，能直接防止相同缺漏再次出現。測試會略增工作時間；跳過則只能靠每次 release 的乾淨環境操作才發現 dependency drift。

### Outcome and acceptance coverage

`requirements-dev.txt` 明確宣告 `Pillow>=12.3,<13`。一次性 CPython 3.12 isolated venv 只安裝該 manifest 後可 import Pillow、收集並執行完整 suite，且 Codex/Generic consumer source、package 與 archive 不新增 Pillow。

主要覆蓋 Specification acceptance criteria 1、2，以及 criterion 9 的 dependency/package-boundary 部分。

### Scope and boundaries

In scope:

- 保留既有 PyYAML range，新增核准的 Pillow development/test range。
- 若選擇 Add tests，新增 focused manifest contract，拒絕 Pillow 缺漏或超出核准 major range。
- 用 disposable CPython 3.12 venv 記錄 interpreter、venv isolation、Pillow version/path、manifest install、full discovery 與 suite 的實際結果。
- 沿用 exact package inventory checks 證明 Pillow 未進入 consumer artifacts。

Out of scope: README/guide 內容、lockfile、constraints、dependency updater、其他 Python/Pillow compatibility promise、consumer runtime dependency 與 release version integration。

### Dependencies and ownership

Dependencies: 無 implementation dependency；Approved Specification 已提供完整 contract。

Likely ownership: `requirements-dev.txt`、focused dependency assertion（優先放在既有 `tests/release/test_release_contract.py` 或一個專屬且小型的 release test）、本 Ticket implementation/review evidence。

### TDD approach

First Red: focused test 讀取 development manifest，要求保留 PyYAML 並包含精確核准的 `Pillow>=12.3,<13`；目前因 Pillow 缺漏而失敗。

Focused Green: 加入最小 manifest declaration，通過 dependency contract 與 Plugin asset import/behavior coverage。

Broader verification: 在 isolated CPython 3.12 venv 僅安裝 manifest，確認無 `PYTHONPATH`、Pillow 來自該 venv，再執行完整 tests 與 Codex/Generic inventory checks。外部 package installation 結果記入 evidence，不把網路安裝塞進 unit test。

### Direct approach

只更新 manifest，使用靜態內容檢查、isolated venv install/import/version/path 與 package inventory inspection 作非測試驗證。不得新增或執行 behavioral tests；repository 將缺少持續拒絕 Pillow range 被刪除或漂移的自動證據，完整 behavioral verification 延後且信心較低。

### Completion and parallel safety

Complete when dependency declaration、選定模式允許的驗證及 evidence 一致，且沒有 consumer package boundary 變更。

Parallel safety: **No in the current shared worktree**。雖然 Ticket 1、2 的主要編輯檔案分離，Ticket 1 的 broader suite 會讀取 Ticket 2 正在修改的 builder/tests，可能觀測到 Red 或中間狀態。只有在真正隔離的 worktrees 中，focused implementation 才可平行；完整 suite、Review 與整合驗證仍須串行。

## Ticket 2 - 讓 Windows replacement 與 recovery 可重試、可復原、可診斷

Status: Completed. Evidence: [Ticket 2 Implementation and correction](../evidence/release-1.3.1-maintenance-ticket-2.md); [Ticket 2 initial independent Review](../evidence/release-1.3.1-maintenance-ticket-2-review.md); accepted [Ticket 2 independent closure Review after P2](../evidence/release-1.3.1-maintenance-ticket-2-review-after-p2.md) (`complete - no actionable findings`).

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。這是多步檔案 transaction，包含 retry、rollback、cleanup 與人工復原資料；只有 deterministic fault injection 能可靠覆蓋成功與雙重失敗分支。測試會增加中高工作量，但 Approved Specification 強制要求這些 behavioral tests；若選擇不加測試，本 Ticket 無法符合目前規格，必須先回 `$write-spec` 修訂並重新核准。

### Outcome and acceptance coverage

Windows managed-output replacement 與 rollback restoration 遇到 `WinError 5` 時完整套用 bounded-retry policy。暫時錯誤解除可完成 build；持續錯誤在上限後進入 recovery；非 allowlisted errors 不重試。Recovery 成功會 byte-for-byte 還原 prior release；recovery 最終失敗則同時回報 primary/recovery errors 與 recovery paths，並保留 staging/backup。

主要覆蓋 Specification acceptance criteria 3-7、criterion 8 的 repeated/prior/unmanaged/failed-build paths，以及 criterion 11 的 builder behavior compatibility。

### Scope and boundaries

In scope:

- 為 managed-output forward replacement、backup movement 與 rollback restoration 定義單一一致的 bounded-retry behavior。
- 明確包含 Windows `WinError 5`；精確 attempt/time limit 與 interval/backoff 在規格邊界內決定並保持短暫、有上限、可測。
- 對非 Windows、非 allowlisted、錯誤 path、structural permission 與 unknown `OSError` 維持立即 failure。
- 保持完整 staging validation、unmanaged collision protection 與 serial-only contract。
- Recovery 成功時清理 transaction-only data；recovery 不完整時禁止 unconditional cleanup，保留並回報可用 staging/backup。
- 建立 deterministic failure injection 覆蓋 retry success、exhaustion、nonallowlisted failure、forward failure/recovery success、recovery transient success 與 recovery final failure。

Out of scope: same-output concurrency lock、root-directory swap、通用 error framework、progress UI、builder 全面 class/module 重構，以及除必要明確 allowlist 外的廣泛錯誤猜測。

### Dependencies and ownership

Dependencies: 無產品行為上的 implementation dependency；但目前共用工作樹，須等待 Ticket 1 implementation、broader verification 與 accepted Review 完成後再開始。

Likely ownership: `scripts/build_release.py` 的 transaction/retry/cleanup boundary、`tests/release/test_release_safety.py` 或一個 focused transaction test module、本 Ticket implementation/review evidence。

### TDD approach

First Red: 在不依賴真實檔案占用的情況下注入前兩次 `WinError 5`、第三次成功，要求同一 replacement 最終完成且輸出完整；目前 builder 首次錯誤即失敗。

Focused Green: 實作最小 bounded retry boundary，使第一個案例通過；依序增加 persistent `WinError 5` exhaustion、nonallowlisted immediate failure、forward recovery、rollback retry 與 rollback-final-failure Red/Green cases。

Broader verification: 執行完整 release safety、prior upgrade、repeated build、unmanaged collision、failed rebuild、reproducibility、ZIP equivalence、checksum 及 relevant release suites；可補充真實 Windows serial build smoke evidence，但不得替代 deterministic tests。

### Direct approach

只允許靜態 transaction trace、isolated real build、手動 output/hash inspection 與 native syntax checks，不新增或執行 behavioral tests。這無法確定性證明 transient/persistent/recovery-failure branches，因而不能完成 Approved Specification；選擇 direct 會把 Plan 留在 Draft，直到規格修訂或測試選擇改變。

### Completion and parallel safety

Complete when全部核准 transaction branches 有實際 deterministic evidence、prior release safety成立、Review 無未解 blocker，且 failure diagnostics 不遺失 primary/recovery context。

Parallel safety: **No in the current shared worktree**。Ticket 1 broader verification 會讀取 builder/tests，Ticket 3 會消費本 Ticket 結果，Ticket 4 需要 frozen candidate。真正隔離 worktrees只允許 Ticket 1、2 的 focused implementation 平行，不允許 shared full-suite或Review observations平行。

## Ticket 3 - 整合 lockstep 1.3.1 identities、packages 與 checksums

Status: Completed. Evidence: [Ticket 3 Implementation and corrections](../evidence/release-1.3.1-maintenance-ticket-3.md); [Ticket 3 initial independent Review](../evidence/release-1.3.1-maintenance-ticket-3-review.md); [Ticket 3 first closure Review](../evidence/release-1.3.1-maintenance-ticket-3-review-after-p2.md); accepted [Ticket 3 second independent closure Review](../evidence/release-1.3.1-maintenance-ticket-3-review-after-envelope-p2.md) (`complete - no actionable findings`).

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。這張 Ticket 會同時改 current identity、Marketplace candidate ref、三語 version URLs、package paths、generated ZIP 與 checksum；現有 tests 也明確要求 `1.3.0`，必須在本 Ticket 以新 current contract更新並驗證。測試會增加高工作量，但不加測試會留下互相衝突的 active expectations，無法通過 Approved Specification；選擇 no tests 必須先修訂規格或重新切分一張 test-enabled integration Ticket。

### Outcome and acceptance coverage

所有 active/current release、Core、Codex/Generic adapter、Plugin、Marketplace candidate、current documentation reference、runtime/package/archive/checksum identity 一致為 `1.3.1`。本機 managed `dist` 完整替換為可重現的 `1.3.1` candidate；consumer inventory 不含 Pillow；已發布 `v1.3.0` assets、Approved historical artifacts 與記錄 hashes 保持不變。

主要覆蓋 Specification acceptance criteria 2、8-11，並提供 criteria 1-7 的 package-facing integration proof。

### Scope and boundaries

In scope:

- 先以 current-release contract 建立 `1.3.1` Red，再同步 active source/config/test identity；不得對 repository 做盲目全域取代。
- 更新 release/Core/adapters/Plugin/Marketplace candidate metadata、current runtime declarations、archive paths 與 current version URLs。
- 文件只改必要 current identity/URL，不新增或重寫說明內容。
- 保持 Codex 9 Skills、Generic 11 modules、legal/assets/package boundaries 與 required validation-check inventory不變。
- 明確凍結 Token proxy algorithm、fixtures、fingerprint 與 threshold；fixture 中作為 benchmark input 的 `1.3.0` 文字不得當成 stale active identity 盲目升版。
- 為 Approved `1.3.0` requirements/spec/plan/reviews/evidence/recorded hashes 增加或保留 historical guard。
- 在 candidate freeze 前確認既有 release-evidence validator 對 current `1.3.1` config 的 absent、incomplete、version-mismatched、missing-check 與 failed-check cases fail closed；只有確定性 Red 證明 generic gate有缺口時，才在本 Ticket修正並 Review。
- 只透過 builder 重建 default `dist`、兩個 ZIP 與 `checksums.sha256`。

Out of scope: 新 workflow behavior、Pillow/Windows fix 的重新設計、Completed `1.3.1` release evidence、external tag/release/upload/Marketplace activation。

### Dependencies and ownership

Dependencies: Tickets 1、2 implementation 及各自 accepted independent Review 完成。

Likely ownership: `release/release.json`、`.agents/plugins/marketplace.json`、Core/adapter/Plugin/Generic active declarations、current README/START-HERE/guides 的 version references、current conformance/release/documentation/package tests、generated `dist/` 與 checksum、本 Ticket evidence。`scripts/build_release.py` 只接受 Ticket 2 已 Review 的結果，不在此偷偷修 behavior。

### TDD approach

First Red: 將 current contract expectations 切到 `1.3.1`，使 active `1.3.0` declarations、URLs 與 package paths 明確失敗；同一 Red 必須已證明 historical `1.3.0` guards與 frozen token fixture未被改寫。

Focused Green: 同步最小 active declarations/tests，重建 default `dist`，通過 exact identity、marketplace drift rejection、inventory/no-Pillow、source-package parity、two-build reproducibility、ZIP equivalence 與 checksum checks。

Broader verification: current identity、clean-slate、Codex/Generic package、documentation/link、Marketplace、release safety、Codex/Generic/conformance suites；canonical+packaged Skill/Plugin validators；unchanged token proxy gate；historical/stale scan 與 `git diff --check`。

### Direct approach

同步 active declarations並執行 schema/native/build/hash/manual inventory checks，但不修改或執行 behavioral tests。Automated version-drift rejection、historical mutation guard、package regression與reproducibility evidence 將不可用，且現有 `1.3.0` test expectations 無法合法同步，因此此選擇不能完成目前 Approved Specification。

### Completion and parallel safety

Complete when source、generated packages、archives、checksums與全部 current identities一致為 `1.3.1`，historical guards通過，Review 無未解 blocker，且尚未建立 Completed release evidence。

Parallel safety: **No**。本 Ticket 消費前兩張修復、修改共享版本宣告與 release tests，並唯一擁有 generated `dist`/checksums。

## Ticket 4 - 完成本機整合驗證與 1.3.1 release evidence

Status: Complete. Evidence: [initial final independent Review](../evidence/ask-then-do-it-1.3.1-final-review.md) (`initial diagnostic P2 closed`); [final independent Review after P2](../evidence/ask-then-do-it-1.3.1-final-review-after-p2.md) (`P2 - final restored state is misclassified as incomplete recovery`); [fresh recovery P2 closure Review](../evidence/ask-then-do-it-1.3.1-final-review-after-recovery-p2.md) (`no actionable findings`); [evidence-only closure Review](../evidence/ask-then-do-it-1.3.1-evidence-closure-review.md) (`non-independent fallback; no actionable findings`).

User test choice: Add tests

Execution mode: `tdd`

System recommendation: **Add tests**。Approved Specification 要求完整 behavioral suites 與 fault-injection evidence均不可 skip；本 Ticket 也必須證明 missing/incomplete/failed actual release evidence會被拒絕。測試與完整 gate 會增加最高時間成本，但若選擇不加測試，就不能產生符合目前規格的 Completed release evidence，必須先回 `$write-spec` 修訂。

### Outcome and acceptance coverage

Frozen `1.3.1` candidate 在 disposable isolated CPython 3.12 environment 只安裝 declared dependencies後通過每個 required gate。Validation ledger、release evidence、final Review 與 release-milestone architecture diagnosis均來自實際觀測，沒有未解 release blocker，且清楚聲明所有 external publication actions未執行。

提供 Specification acceptance criteria 1-12 的最終 proof，特別是 criteria 9-12。

### Scope and boundaries

In scope:

- 以 current `1.3.1` config 再次證明 absent、incomplete、version-mismatched、missing-check 或 failed-check 的 actual evidence不能被接受；本 Ticket只執行 Ticket 3已 Review 的 validator，不修改 validator或test code。
- 在 fresh isolated CPython 3.12 venv 僅安裝 `requirements-dev.txt`，記錄 interpreter/venv isolation、Pillow version/path、full serial discovery、完整 suite與 exact結果。
- 串行執行 Windows deterministic transaction suite、Codex/Generic/conformance suites、Marketplace validator、canonical+packaged Skill/Plugin validation、unchanged Token proxy gate。
- 執行 default與兩個 isolated builds，核對 inventories/no-Pillow/source parity、reproducibility、ZIP equivalence、SHA-256、unmanaged/prior/repeated/failed-rebuild paths。
- 執行 documentation/link/current-version scan、Approved `1.3.0` hash preservation、working-tree scope與diff checks。
- 對整個 milestone做 fresh independent Full Review；finding回 owning Ticket 修正、重建、重跑 affected gates與Review。若 evidence validator有 fail-closed gap，也必須停止並回 Ticket 3處理。
- Candidate穩定後做 read-only release architecture diagnosis；診斷不授權任何 refactor，release correctness finding仍回 owning Ticket。
- 最後才建立 `1.3.1` validation ledger、release evidence及 evidence-only closure，逐項記錄 command、status、outcome、archive hashes與publication deferrals。

Out of scope: 在 evidence階段暗改 source/package、接受 skipped required tests、架構 refactor、Git tag、push、GitHub Release、asset upload、Marketplace activation與announcement。

### Dependencies and ownership

Dependencies: Ticket 3及所有 earlier Tickets 的 accepted Reviews完成，candidate bytes與source狀態凍結。任何 source defect都回原 owning Ticket，不在此修。

Likely ownership: 新 `docs/evidence/ask-then-do-it-release-1.3.1.json`、配對 Markdown release evidence、Ticket/final Review、release architecture diagnosis與closure artifacts。`tests/release/test_release_evidence.py`、`scripts/validate_release_evidence.py` 及所有 product source不屬於本 Ticket；缺口必須回 Ticket 3並重新 freeze candidate。

### TDD approach

First Red: 以 current `1.3.1` config 驗證尚不存在或未 Completed 的 actual ledger/evidence，必須被既有 validator拒絕。若沒有得到預期 Red，本 Ticket停止並回 Ticket 3修正 evidence contract，不在 frozen階段改 code。

Focused Green: 所有 raw observations完成後建立 exact ledger/evidence，使 validator只在每個 configured check恰好存在、status可接受且 command/outcome可追溯時通過。

Broader verification: 依本 Ticket scope完整執行全部 required gates、independent Review、architecture diagnosis與evidence-only closure；任何重建都使舊 hashes/observations失效並要求重跑。

### Direct approach

只允許 non-test validator/schema/hash/link/diff與手動 artifact inspection，不新增或執行 behavioral tests。因 Spec明定 full suites、Windows fault injection與required gates不可跳過，direct無法產生 Completed release evidence；選擇 direct會把 Plan留在 Draft，直到規格修訂或測試選擇改變。

### Completion and parallel safety

Complete when every required observed gate通過、Review與architecture diagnosis無未解 release blocker、validator接受 Completed local evidence，且沒有外部 publication claim或mutation。

Parallel safety: **No**。本 Ticket消費 frozen candidate與全部 Reviews；與任何 source/package工作並行會讓 observations、ZIP bytes與hashes失效。

## Dependency order and parallel groups

1. Shared-worktree foundation: Ticket 1 completes implementation、broader verification與independent Review first.
2. Builder foundation: Ticket 2 then completes implementation、broader verification與independent Review. Isolated worktrees may parallelize only focused Ticket 1/2 implementation, not full-suite or Review observations.
3. Sequential integration: Ticket 3 begins only after Tickets 1-2 and their Reviews are accepted.
4. Candidate Review gate: Ticket 3 receives independent Review; corrections require rebuild and affected verification.
5. Sequential completion: Ticket 4 consumes the frozen candidate, runs final Full Review and architecture diagnosis, then writes observed release evidence.
6. Stop at the completed local candidate. External publication remains outside this Plan and requires later explicit approval.

## Resolved test choices

使用者於 2026-08-17 在完整四張 Ticket 定義與 test recommendations 展示後，對「四張 Ticket 是否全部加測試」明確回覆「核准」。因此全部選擇均記錄為 Add tests，並依 workflow contract 映射為 `tdd`；沒有 unresolved choice。

- Ticket 1: Add tests -> `tdd`。保護 development dependency self-sufficiency。
- Ticket 2: Add tests -> `tdd`。提供規格要求的 deterministic transaction branch evidence。
- Ticket 3: Add tests -> `tdd`。保護 lockstep identity、historical preservation 與 package reproducibility。
- Ticket 4: Add tests -> `tdd`。允許完整 behavioral gates 與 Completed release evidence。

任何後續 test-choice 或 mapped-mode 變更都會使本 Plan 回到 Draft，並在 affected implementation 前重新核准。
