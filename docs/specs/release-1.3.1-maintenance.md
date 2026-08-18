# Ask Then Do It 1.3.1 發布可靠性維護 Specification

Artifact type: Specification

Artifact ID: `release-1-3-1-maintenance-spec`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Status: Approved

Inputs: Approved [Ask Then Do It 1.3.1 發布可靠性維護 Requirement Decision Record](../requirements/release-1.3.1-maintenance.md)、Approved Project Knowledge Base、Approved `1.3.0` release evidence，以及目前 development dependency、release builder、release safety 與 package contract。

Assumptions: `v1.3.0` 與其歷史 artifacts 不可變。`1.3.1` 只支援單一 builder 串行寫入同一 output directory。Windows `WinError 5` 已確定列入 managed-output replacement 與 rollback restoration 的 bounded-retry allowlist；精確 retry 次數、間隔與其他 error codes 可由後續 Ticket 在本規格邊界內決定。

Deferred: 每個 Ticket 的範圍與 `tdd`/`direct` 模式、精確 retry policy 參數、除 `WinError 5` 外的 allowlisted error codes、implementation、Git tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement。

Handoff: `$plan-tickets` after explicit Specification approval.

Approval: 使用者於 2026-08-17 在完整 Specification 展示與獨立規格審查完成後明確回覆「核准」。

## 問題

完整測試會載入 Pillow，但目前 development dependency manifest 未宣告它，因此乾淨環境無法只靠已宣告依賴完成測試。Windows release build 也曾在 managed-output replacement 遭遇暫時性存取拒絕；目前此類錯誤沒有 bounded retry，而 recovery 再失敗時可能遺失主要錯誤資訊，或清除人工復原需要的資料。

這會讓相同的有效 source 在維護者電腦上因未宣告依賴或短暫檔案占用而無法產生可靠 release candidate，也使失敗後的 release 完整性與復原狀態不夠清楚。

## 目標

- 讓 CPython 3.12 的乾淨開發環境能從單一 development dependency manifest 安裝完整測試所需依賴。
- 讓串行 Windows release build 能容忍明確、短暫的 replacement 存取或檔案占用錯誤，但不隱藏永久或未知錯誤。
- 在 replacement 失敗後恢復先前已驗證的 release；若無法完整恢復，保留人工復原資料並提供完整診斷。
- 將目前 release、Core、兩個 adapters 與 runtime identity 一致升至 `1.3.1`，產生可重現的本機 packages、ZIP、checksums 與 release evidence。
- 維持 `1.3.0` 歷史 artifacts 和既有 Full/Lite、Plugin、Generic、Token proxy 行為不變。

## 非目標

- 支援兩個 builder 同時寫入同一 output directory，或定義 lock ownership、stale-lock 與並行協調契約。
- 修改 Token proxy algorithm、fixture、fingerprint、正規化方式或 60% gate。
- 建立 CI、dependency lock/constraints 或 dependency update automation。
- 全面拆分、重新設計或模組化 release builder。
- 新增或擴充 README、使用者指南或開發者指南。
- 改變 Full/Lite workflow、Core rule semantics、Plugin 功能、Generic prompt 行為或 consumer runtime dependencies。
- 建立 tag、push、發布 GitHub Release、上傳資產、啟用 Marketplace ref 或發布公告。

## 使用者與情境

### 維護者建立乾淨驗證環境

維護者使用 CPython 3.12，安裝 repository 宣告的 development dependencies，接著收集並執行完整測試。Pillow 可直接載入，不需要另外猜測套件、使用 repository 外的 bundled copy，或加入 `PYTHONPATH` workaround。

### 暫時性 Windows replacement 錯誤解除

單一 builder 已完成 staging validation，在提交 managed outputs 時遇到 allowlisted 的短暫 Windows 存取或檔案占用錯誤。錯誤在 bounded retry 期間解除，builder 完成一致的 `1.3.1` output set，並清除不再需要的 staging/backup。

### Replacement 永久失敗但 recovery 成功

Replacement 發生非 allowlisted 錯誤，或 allowlisted 錯誤在 retry 上限內未解除。Builder 以非零狀態停止並恢復先前已驗證的 release；恢復後的 managed outputs 與建置前 byte-for-byte 相同。

### Replacement 與 recovery 都失敗

Builder 嘗試恢復先前 release 時仍無法完成。它以非零狀態停止，不宣稱任何有效新 release 或完整舊 release，保留可供人工復原的 staging/backup，並同時回報 primary error、recovery error 與相關路徑。

### 維護者完成本機 candidate

所有 dependency、release、package、reproducibility、checksum、conformance、documentation 與既有 Token proxy gates 通過後，維護者取得本機 `1.3.1` candidate 與觀測所得 evidence。流程在任何外部發布 mutation 前停止。

## 必要行為

### 1. Development dependency contract

Development dependency manifest MUST 宣告 `Pillow>=12.3,<13`。`1.3.1` 的正式開發與 release-validation baseline MUST 是 CPython 3.12 與 Pillow 12.x。

在該 baseline 的乾淨環境安裝 manifest 後，完整 test discovery 與 test execution MUST NOT 因缺少 `PIL`、repository 外 bundled Pillow 或額外 module-path 設定而失敗。

Pillow MUST remain development/test-only。Codex 與 Generic consumer package inventory、runtime manifest 與 archive MUST NOT 新增 Pillow 或其檔案。

### 2. Retry eligibility and bounds

在 Windows 上，managed-output replacement 與 rollback restoration 遇到 `WinError 5` 時 MUST 進入並完整套用已設定的 bounded-retry sequence；其他可重試錯誤 MUST 由明確列舉的 transient error allowlist 決定，且只涵蓋可合理重試的短暫存取或檔案占用條件。

每個 retry sequence MUST 有明確上限，並在有限時間內成功或失敗。`WinError 5` 無法區分暫時檔案占用與永久 ACL，因此同一 error code 持續發生時 MUST 依已設定 policy 重試至 attempt 或 time 上限，耗盡後再以 failure 進入 recovery。非 Windows 平台、非 allowlisted error、錯誤路徑、其他永久或結構性權限問題與未知 `OSError` MUST NOT 因本功能被重試或被重新分類為暫時錯誤。

失敗診斷 MUST 足以辨識受影響的 operation 與 path。Retry MUST NOT 改變 unmanaged-output collision 的既有立即失敗行為。

### 3. Forward replacement and recovery parity

將既有 managed outputs 移入 backup、將已驗證 staged outputs 移入正式位置，以及 recovery 時恢復 managed outputs，MUST 使用相同的 retry eligibility 與 boundedness contract。

Retry policy MUST NOT 跳過 staging validation、降低 output inventory 驗證，或允許未完整驗證的 staging 被視為 release。

### 4. Successful commit

只有當全部受管輸出完成一致 replacement，且 builder 所負責的 staging、inventory 與 output verification 通過時，builder 才可回報該次 build 成功。整個 `1.3.1` local candidate 只有在第 9、10 節的整體 release gates 與 evidence 完成後才可宣告完成。

成功後的 active output set MUST 完整屬於 `1.3.1`，不得混合舊版與新版 managed outputs。Builder MUST 清除只為該次交易建立且不再需要的 staging/backup 資料。

### 5. Failed commit with successful recovery

任何 forward replacement 的非 retryable failure 或 retry exhaustion MUST 使 build 失敗並啟動既有 release 的 recovery。

Recovery 成功時，建置前存在的 managed outputs MUST byte-for-byte 恢復，該次 build 的新 managed outputs MUST NOT 留在 active output set，且不再需要的 staging/backup MUST 被清除。錯誤結果 MUST 清楚指出 candidate 未提交成功。

### 6. Incomplete recovery

若 recovery 無法完整完成，builder MUST：

- 以非零狀態停止；
- 不把 active output directory 宣告為完整舊 release 或有效新 release；
- 同時保留並回報最初 replacement failure 與 recovery failure；
- 保留並回報仍可用於人工復原的 staging、backup 與其他相關路徑；
- 不以 unconditional cleanup 刪除上述 recovery data。

Recovery data 的保留 MUST 以診斷與人工復原為目的，不得被 package、checksum 或 release evidence 當成成功輸出。

### 7. Deterministic verification

Validation MUST 以確定性的 fault injection 分別證明：`WinError 5` 經數次失敗後成功、持續 `WinError 5` 的 retry exhaustion、非 allowlisted error 立即失敗、forward failure 後 recovery 成功、recovery 本身遇到 `WinError 5` 後成功，以及 recovery 最終失敗。

偶發的真實 Windows 檔案占用 MAY 作為補充 smoke evidence，但 MUST NOT 是上述行為的唯一證據。

### 8. Lockstep release identity

所有代表目前版本的 release、Core、Codex adapter、Generic adapter、Plugin、Marketplace candidate metadata、current documentation reference、runtime identity、package name/URL、archive、checksum 與新 release evidence MUST 對 `1.3.1` 一致。

升版 MUST 只影響 active/current declarations、本機 generated `dist` 與新 `1.3.1` artifacts。Approved `1.3.0` requirements、Specification、Ticket Plan、reviews、evidence、已發布 release assets、記錄於歷史 evidence 的 hashes、tag reference 與其他歷史 artifacts MUST 保持不變；本機受管 `dist` 被 `1.3.1` candidate 取代不視為改寫已發布的 `v1.3.0` assets。

### 9. Existing release gates

`1.3.1` candidate MUST 保持並通過既有的 unmanaged-output protection、complete staging validation、exact inventory、source/package equivalence、deterministic ZIP、two-build reproducibility、ZIP equivalence、SHA-256 checksum、adapter conformance、documentation、Plugin asset 與 required Token proxy gates。

本維護版 MUST NOT 藉由刪除、略過或放寬既有 required gate 取得成功結果。

### 10. Publication boundary

本流程 MUST 在本機 candidate、packages、checksums、完整 validation ledger 與 release evidence 完成後停止。Evidence MUST 清楚區分已觀測的本機結果與尚未執行的外部狀態。

未取得另一次明確核准前，流程 MUST NOT 建立 `v1.3.1` tag、push、建立 GitHub Release、上傳 assets、啟用 Marketplace ref 或公告。

## 邊界與失敗行為

- 同一 output directory 的 concurrent builders 不受支援；並行造成的結果不得被描述為本版保證。
- Retry 不得無限等待，也不得把相同永久錯誤轉為表面成功。
- 非 allowlisted failure 仍可觸發 recovery，但 forward operation 本身不得先做無資格重試。
- Recovery 成功與否以整個先前 managed output set 的完整性判定，不得只因部分檔案還原就回報成功。
- Recovery 失敗時 active output 可能需要人工處理；diagnostic 必須明示此狀態，不能產生成功 checksum 或 completed release evidence。
- Unmanaged files 不得被 backup、覆寫、刪除或納入 recovery data lifecycle。
- 成功與完整 recovery 的 cleanup 不得遺留 transaction-only 目錄；不完整 recovery 則以資料保存優先。

## 資料、權限與外部契約

- 本功能只處理 repository release artifacts 與暫時 transaction data，不新增個人資料、credentials、遙測或網路服務。
- Builder 只能在既有受管 output boundary 內替換、backup、restore 或清理 managed outputs；unmanaged outputs 的保護契約維持不變。
- Pillow 來源仍由 Python package installation environment 提供，只是 development/release-validation dependency，不成為 consumer dependency。
- GitHub、Git tag、Release assets 與 Marketplace 是外部 publication contracts；本規格只要求本機 candidate metadata 一致，不授權改變其外部狀態。

## 相容性、推出與復原

- Full 與 Lite 的使用者流程及輸出語意，除 current version identity 外，MUST 與 `1.3.0` 相容。
- Codex 與 Generic packages 的 runtime inventory MUST 與 `1.3.0` 維持相同 dependency boundary。
- `1.3.1` 採新的 artifacts 與 evidence，不原地修補或重新標記 `1.3.0`。
- Prior-release upgrade、repeated serial build、failed rebuild preservation 與從空 output 建置 MUST 持續受支援。
- 外部 publication 若日後獲准，必須以已驗證的本機 candidate 為來源；若未獲准，本機完成狀態仍不得被稱為已公開發布。

## 限制與假設

- 唯一正式驗證的 interpreter/dependency 組合是 CPython 3.12 與 Pillow 12.x；本規格不承諾其他 Python 或 Pillow major versions。
- 精確 retry 次數、間隔、backoff 形式與除 `WinError 5` 外的 Windows error codes 是後續設計選擇，但必須符合 explicit allowlist、bounded、可確定性驗證的行為契約。
- 本規格假設每個 output directory 同一時間只有一個 builder。
- Required Token proxy gate 照常執行；其 algorithm、fixture、fingerprint 與 threshold 不變。
- Ticket 切分與 execution mode 仍由 Ticket Plan 決定，但負責 Windows replacement/recovery 行為的 Ticket 必須能建立並執行本規格要求的 deterministic fault-injection behavioral tests；禁止此類測試的 mode 無法滿足本規格，除非先修訂並重新核准規格。其他 Tickets 的 `tdd`/`direct` 選擇不由本規格預先決定。
- `Core version: 1.3.0` 是本 workflow artifact schema identity；target product release 是 `1.3.1`。

## 驗收條件

1. 在乾淨 CPython 3.12 環境安裝 development dependency manifest 後，實際 Pillow 版本符合 `>=12.3,<13`，且完整 test collection/execution 不需要未宣告套件或額外 module-path workaround。
2. Codex 與 Generic source/package/archive inventories 均不包含 Pillow runtime dependency 或 Pillow files。
3. 確定性測試顯示 managed-output replacement 的 `WinError 5` 在有限次失敗後解除時可成功，build 產生完整一致的 candidate，且 transaction-only staging/backup 已清除。
4. 確定性測試顯示持續 `WinError 5` 只重試至上限，再以 failure 進入 recovery；非 allowlisted error 不經 retry 即進入失敗處理，流程不會無限等待。
5. Forward backup/replacement 與 recovery restoration 均符合相同 retry eligibility 與 boundedness contract。
6. Forward commit 最終失敗但 recovery 成功時，builder 退出非零，原 release managed outputs 與建置前 byte-for-byte 相同，不含新舊混合輸出，也不遺留不必要 staging。
7. Recovery 遇到 allowlisted transient error 時可在界限內成功；若 recovery 最終失敗，結果同時包含 primary/recovery errors 與 recovery paths，保留可用 staging/backup，且不產生成功 release 宣告。
8. 從空 output、repeated serial builds、prior-release upgrade、unmanaged collision 與 failed rebuild preservation 的既有案例全部通過。
9. Exact inventories、source/package equivalence、two-build reproducibility、deterministic ZIP、ZIP equivalence、SHA-256、adapter conformance、documentation、Plugin assets 與 required Token proxy gates 全部通過。
10. 所有 active/current identities、新 packages、URLs、checksums、Marketplace candidate metadata 與 release evidence 一致為 `1.3.1`；歷史 `1.3.0` 文件、evidence、已發布 assets 與其記錄 hashes 無變更，而本機受管 `dist` 已一致取代為 `1.3.1` candidate。
11. 除版本 identity 與本規格明列的維護行為外，Full/Lite、Core、Plugin、Generic 與 Token proxy observable behavior 無回歸。
12. Release evidence 只聲明已觀測的本機 candidate 結果；Git tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement 均未執行。

## 延後決策

- 每個 Ticket 的垂直範圍、依賴順序，以及不負責強制 fault-injection coverage 之 Tickets 的 behavioral-test 選擇與 Approved `tdd`/`direct` execution mode。Windows replacement/recovery Ticket 的 plan 必須保留本規格要求的 deterministic behavioral-test 能力。
- 在符合本規格的前提下，精確 retry count、等待間隔、backoff 形式，以及除 `WinError 5` 外的 Windows transient error-code allowlist。
- 實作完成後的獨立 Review、release architecture diagnosis 與 evidence closure 細節。
- `v1.3.1` tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement；每個外部 mutation 都需要後續明確核准。
