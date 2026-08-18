# Ask Then Do It 1.3.1 發布可靠性維護 Requirement Decision Record

Artifact type: Requirement Decision Record

Artifact ID: `release-1-3-1-maintenance-requirements`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Status: Approved

Inputs: 2026-08-17 使用者決策，包括後續明確核准 managed-output replacement 對 `WinError 5` 進行 bounded retry；目前 `dev` repository；Approved `1.3.0` requirements、Specification、Ticket Plan 與 release evidence；Approved Project Knowledge Base；`requirements-dev.txt`、Plugin asset tests、release builder 與 release safety tests 的唯讀證據。

Assumptions: `v1.3.0` 與其發布資產保持不可變。`1.3.1` 是新的 patch release，且不改變 Full/Lite 使用者行為。

Deferred: 精確 retry 次數與 backoff 間隔、除 `WinError 5` 外的最終 Windows error-code allowlist、每個 Ticket 是否加入測試、實作、Git tag、push、GitHub Release、資產上傳、Marketplace 生效與公告。

Handoff: 已同步正式 Project Knowledge Base，並交回 `$write-spec` 更新 Draft Specification。

Approval: 前一版於 2026-08-17 核准。使用者其後明確核准 `WinError 5` 的行為取捨，並於 2026-08-17 聯合核准包含該決策的本修訂版與 WinError 5 Knowledge Base Change Summary 精確內容。

## 問題與目標

完整測試目前依賴未在 `requirements-dev.txt` 宣告的 Pillow，乾淨環境會在載入 `PIL.Image` 時失敗。Windows 發布建置亦曾在 managed-output replacement 發生暫時性 `WinError 5`；目前 forward replacement 與 rollback 都直接呼叫 `os.replace`，沒有有限重試，rollback 再失敗時可能覆蓋原始錯誤並刪除可供人工復原的 staging/backup。

`1.3.1` 的目標是讓維護者能從已宣告的開發依賴執行完整驗證，並讓單一、串行 release build 對明確的 Windows 暫時性 replacement 錯誤安全復原，同時維持既有 package、checksum、歷史證據及外部發布核准邊界。

## 使用者與成功訊號

- 維護者可在乾淨 CPython 3.12 環境只安裝 `requirements-dev.txt`，不使用額外 `PYTHONPATH` 或 bundled Pillow 即載入並執行完整測試。
- 串行 release build 遇到 allowlisted 暫時性 Windows replacement 錯誤時，可在有限時間內成功，或以可診斷且可復原的狀態失敗。
- Plugin 與 Generic 使用者的 Full/Lite 行為、runtime dependency 與 package inventory 不因本維護版改變。

## 範圍

- 在 `requirements-dev.txt` 宣告 `Pillow>=12.3,<13`；`1.3.1` 的驗證基準為 CPython 3.12 與 Pillow 12.x。
- Managed-output replacement 與 rollback restoration 遇到 Windows `WinError 5` 時，將它視為 potentially transient 的 allowlisted error 並執行 bounded retry。因該 error code 無法區分暫時占用與永久 ACL，永久 access-denied 也可能短暫等待至 retry 上限才失敗；其他非 allowlisted path、permission、structural 或未知 `OSError` 立即失敗。
- forward replacement 與 rollback restoration 使用相同的暫時錯誤容忍邊界。
- replacement 失敗時保留或恢復先前已驗證的 release，不得留下被視為有效的新舊混合輸出。
- forward replacement 與 rollback 都失敗時，保留 staging/backup、回報其路徑，並同時揭露 primary 與 recovery failure。
- 以確定性的錯誤注入覆蓋 retry、retry exhaustion、rollback 與 rollback failure，不以偶發真實錯誤作為唯一驗收方式。
- 將 release、Core、Codex adapter、Generic adapter 與 current runtime identity 同步升至 `1.3.1`，重建本機 packages、ZIP、checksums 與 release evidence。
- 保留全部 `1.3.0` requirements、Specification、Ticket Plan、evidence、tag 與發布資產不變。

## 非目標

- 不支援兩個 builder 同時寫入同一 output directory；release 與驗證維持串行。
- 不修改 Token proxy algorithm、fixture、fingerprint 或固定 60% gate。
- 不建立 CI、不加入 dependency lock/constraints、不全面拆分類別或重構 `build_release.py`。
- 不新增或擴充 README、使用者指南或開發者指南；乾淨環境命令只記錄於測試及發布證據。
- 不改變 Full/Lite workflow、Core rule semantics、Plugin 功能、Generic prompt 行為或 package runtime dependency。
- 不在本流程中自動建立 tag、push、發布 GitHub Release、上傳資產、啟用 Marketplace ref 或公告。

## 主要行為

1. 維護者在乾淨 CPython 3.12 環境安裝 `requirements-dev.txt`，完整 test discovery 不再因缺少 `PIL` 失敗。
2. Builder 完成 staging 與既有驗證後，對每次 managed-output replacement 執行相同的 allowlisted bounded-retry policy。
3. Allowlisted error（包括 managed-output replacement 的 `WinError 5`）在重試期限內解除時，build 正常完成並產生完整 `1.3.1` output set。
4. 非暫時錯誤或 retry exhaustion 觸發 rollback；rollback 成功時，先前 release 必須保持 byte-for-byte 完整。
5. Rollback 未完成時，builder 不宣稱先前 release 完整，不刪除人工復原所需資料，並回報所有相關路徑與兩層錯誤。
6. 本機 candidate 通過完整 release gates 後停止；外部發布等待另一個明確核准。

## 邊界與失敗行為

- Retry 必須有上限。持續發生的 `WinError 5` 最多等待至該上限；非 allowlisted 權限錯誤、錯誤路徑、unmanaged collision 或未知錯誤不得轉成重試等待。
- 可安全清理的成功或完整 rollback 路徑不得留下 staging；不完整 rollback 則必須保留可復原資料。
- Existing unmanaged-output protection、staging validation、deterministic ZIP、ZIP equivalence、checksum 與 historical-artifact preservation 必須維持。
- 同一 output directory 的 concurrent build 行為未受支援，不得因本版產生 lock ownership 或 stale-lock 契約。

## 資料、依賴、安全與操作限制

- Pillow 僅為 development/test dependency，不得進入 Codex 或 Generic consumer packages。
- 不新增個人資料、credential、網路服務或 production runtime dependency。
- 外部 publication 仍由 maintainer 控制，並在實際 mutation 前另行核准。
- Token proxy required release gate 照常執行，但本版不改其 implementation 或 evidence contract。

## 驗收條件

1. 乾淨 CPython 3.12 環境執行 `pip install -r requirements-dev.txt` 後可 import Pillow，並可收集與執行完整 test suite，無額外 `PYTHONPATH` workaround。
2. Pillow 版本符合 `>=12.3,<13`，且不出現在 Codex/Generic package runtime inventory。
3. 確定性測試證明 managed-output replacement 的 `WinError 5` 在前數次失敗後解除時可重試成功。
4. 持續發生的 `WinError 5` 只重試至 bounded 上限，再以非零狀態進入 recovery；非 allowlisted error 立即失敗，沒有無限等待。
5. Forward replacement 與 rollback 都遵守相同 retry boundary。
6. Rollback 成功時，先前 release byte-for-byte 不變，沒有新舊 managed output 混合，也沒有不必要 staging。
7. Rollback 失敗時，錯誤同時包含 primary 與 recovery failure，並保留及回報 staging/backup 路徑。
8. Repeated serial builds、prior-release upgrade、unmanaged collision、failed rebuild preservation、two-build reproducibility、ZIP equivalence 與 SHA-256 gates 通過。
9. 所有 current release/Core/adapter/runtime identity、Marketplace ref、package names、URLs、checksums 與新 release evidence 一致為 `1.3.1`。
10. 全部 `1.3.0` approved artifacts 與歷史 hashes 保持不變。
11. Full/Lite、Plugin、Generic 與 Token proxy observable behavior 除版本 identity 外保持不變。
12. 本流程不執行任何外部發布 mutation。

## 已確認決策

- 只處理 Pillow dependency 與 Windows serial-build replacement reliability。
- CPython 3.12 + `Pillow>=12.3,<13` 是本版唯一正式驗證的 dependency baseline。
- Managed-output replacement 與 rollback restoration 的 Windows `WinError 5` 明確列入 retry allowlist，且 retry 必須 bounded。由於 error code 無法區分暫時占用與永久 ACL，永久 access-denied 可能短暫等待至上限；其他非 allowlisted errors 立即失敗。
- Concurrent same-output builds、Token fingerprint、CI、lockfile、文件擴充與全面 builder 重構均不在範圍。
- Rollback 無法完成時保留 recovery data 並回報路徑。
- 所有 current version declarations lockstep 升至 `1.3.1`；歷史 `1.3.0` 不改寫。
- 完成本機 candidate 後停止；外部 publication 另行核准。

## 明確共識證據

使用者於 2026-08-17 逐項明確回答「是」，確認串行 build 邊界、Python/Pillow baseline、rollback failure 保留策略、allowlisted retry、無新開發者文件、外部發布另行核准，以及 `1.3.1` lockstep version policy；其後在完整 Requirements 與 Knowledge Base Change Summary 展示後明確回覆「核准」。獨立規格審查指出 `WinError 5` 無法單靠 error code 區分暫時占用與永久 ACL 後，使用者明確核准將 managed-output replacement 的 `WinError 5` 納入 bounded retry，接受永久 ACL 可能等待至上限的取捨。
