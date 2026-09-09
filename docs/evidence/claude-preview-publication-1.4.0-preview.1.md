# Claude 1.4.0-preview.1 發布驗證

Artifact type: Publication Evidence

Status: Candidate verified — external publication pending

Approval: 2026-09-09 使用者「核准 就先上線以及發布吧」。範圍見 [公開 preview 發布核准](../plans/claude-preview-publication-1.4.0-preview.1.md)。本次為明確核准的 preview 例外，未完成的正式模型／host／context gates 不因此通過。

## 來源與隔離

以 GitHub main `0d0bfbb770cdd96265bb1f4f536f2e7600a240df` 建立獨立 `codex/release-claude-preview-1` worktree；base tree 與原 dev 完全相同。原 dev 保持不動，知識庫原有修改未提交且 SHA-256 仍為 `d64b538ee04c65fc829891a37f5bb1fd7d6a00e44a18b406e1cde8a7b130a062`。明確清單包含 Claude runtime、tests、官方來源 snapshots、文件與歷史開發 evidence；排除本機驗證 kits、CLI binary、無關 HTML 與私人資料。

新增 Claude 專用 LF attributes，Git stage 使用既有換行規則；Claude runtime、tests 與發布來源由 staged Git blobs 的精確 bytes 建立；歷史 raw-byte tests 保留原 checkout 的換行格式，Git content 不變。Core／Codex／Generic／release config／既有 tags 與 stable assets 不變。

## 版本與測試

- Runtime manifest、Marketplace、router、bootstrap、mapping、context route evidence 使用 `1.4.0-preview.1`；Marketplace source 固定 `v1.4.0-preview.1`，catalog 安裝來源為 `#claude-preview`。
- Runtime focused Red 4 tests／5 failures，Green 34 tests，再追加 2 tests 通過；model source trace Red 6 tests／4 failures，修正 raw mapping digest 後 6 tests 通過。Mapping canonical digest 與 raw source digest 各自驗證，不混用。
- Preview packaging test Red 10 tests／6 failures／1 error（舊 builder identity），調整固定版本與 ZIP 名稱後 10 tests 通過；未放寬 stable version parser 或正式 conformance gates。
- 三語文件保留原始布局、README 原有 hashes 與 stable 1.3.1 內容。僅更新六個 Claude 插入區塊的 reviewed digests；41 focused documentation tests 通過。
- 第一輪隔離 full suite：393 tests，23 failures／2 errors／1 skip。原因為過早複製的舊文件、尚未建置的 default dist，以及 clean checkout 的 CRLF 使原始歷史 byte hashes 不同。結果未計為成功。同步 frozen 文件與 test、從 staged blobs 還原候選 bytes，並在隔離目錄建置 stable dist 後，13 focused docs／歷史 byte checks 通過；無修改歷史 hashes 或放寬其檢查。
- Exact Claude Code `2.1.251` 對最終候選 Plugin 與 Marketplace 執行 `plugin validate <path> --strict`，兩者 exit 0、`Validation passed`。隔離 config、停用 auto-update／nonessential traffic／telemetry；沒有登入或模型呼叫。
- `git diff --cached --check` 僅有六個既存檔案 EOF blank-line 訊息（四份已凍結 profile、兩份歷史文件）。保留 frozen 原文，`core.whitespace=-blank-at-eof` 下 check exit 0；没有 trailing-whitespace defects。

- 第二輪隔離 full suite：393 tests／124.814s，僅 56 failures，全部来自兩項歷史 byte 測試（43 個既有 1.3.0 evidence、13 個既有 token fixtures），其凍結 hashes 使用 CRLF。從原 workspace 保留的歷史文件還原這 56 個 checkout bytes，逐檔先驗證正規化換行後與 staged Git blob 完全相同；不修改 index、source content、測試或 expected hashes。三項全部歷史 byte 測試随后通過，git unstaged diff 為空。Claude 新來源与ZIP始終維持 exact Git bytes。

- 最終完整回歸：`.venv/Scripts/python.exe -B -m unittest discover -s tests -p test_*.py`（在隔離發布 source 執行）；`Ran 393 tests in 120.740s; OK (skipped=1)`，exit 0。唯一 skip 是 Windows 建立 symlink 權限不足（WinError 1314）的 security fixture；不代表該真實檔案系統案例已執行。
- 獨立 [發布 Review](claude-preview-publication-1.4.0-preview.1-review.md) 在最終來源與ZIP上檢查版本、catalog、文件、package parity、stable 保留與十二個 lenses；發布副本的 stale docs finding 已修正。

## 打包

兩次獨立 preview build 的全部 35 個輸出檔 bytes 相同。ZIP 內恰好 32 個 runtime／legal files，逐檔等於 staged source，沒有 development evidence 或外層 `preview.json`。

- Asset: `ask-then-do-it-claude-1.4.0-preview.1.zip`
- Size: `55,632` bytes
- SHA-256: `38d228914bf52b4eaa71f3c92e04a3397593a24c5c3a7204bf911cc870336e7b`
- GitHub 附件 `checksums.sha256` 使用同層 ZIP basename，符合下載後的實際檔案布局。

Builder 的外層 `preview.json` 仍標 `not-a-release`、`packaging-only-no-host-or-model-verification`，只證明打包，不作為公開 Release 附件。本次對外公開以使用者核准與 GitHub prerelease 記錄為準。

## 已接受的限制

官方 Claude 真實 session、雙 profile 完整行為／等價、context reduction、全部 OS／IDE matrix 尚未驗證。Claude 4.6+、Claude Code 2.1.251+、Node 22+ 為 compatibility targets。VS Code／Cline 報告不視為官方 Claude Code live evidence。
