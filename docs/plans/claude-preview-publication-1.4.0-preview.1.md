# Claude 1.4.0-preview.1 公開預覽版發布

Status: Approved — publication in progress

Approval: 使用者於 2026-09-09 明確回覆「核准 就先上線以及發布吧」，核准先發布 Claude preview、保留穩定版 1.3.1，並在實際使用後持續修正。此核准涵蓋版本、文件、打包、驗證、Git commit／push／tag、GitHub prerelease 與附件上傳。

本文件記錄本次發布例外，取代原 1.4.0 Plan 中「所有 external publication 均 deferred」的限制，僅適用此公開 preview。正式 1.4.0 的完整行為、context 與 live acceptance 不因此視為通過。

## 發布結果

- Claude Plugin、Marketplace、router envelope 與 ZIP 使用 `1.4.0-preview.1`；不可沿用未來正式版 `1.4.0` 的安裝快取 identity。
- Git tag 為 `v1.4.0-preview.1`。Marketplace 的 Plugin source 固定指向此 tag；使用者自願加入 `claude-preview` branch 的 catalog，以便後續更新 preview。
- 公開 GitHub Release 標示 prerelease，`make_latest=false`。既有 stable 1.3.1、Core／Codex／Generic release config、既有 tags 與附件維持。
- README 保留原 English／繁中／日本語布局，只調整 Claude additions；三語入口與 Claude guide 同步下載、安裝、更新、移除及回報方式。

## 執行與驗證

沿用已核准 Claude Tickets 的測試與 ownership：runtime identity／validator、文件與其 contract tests、builder／package checks 可在不同檔案平行調整。版本與文件同步屬已授權的發布收尾，無新增產品行為。

1. 同步 runtime identity、mapping digest 與 preview ZIP 名稱；保留未來 stable conformance target。
2. 執行 focused tests、完整離線測試與 exact Claude Code 2.1.251 的 strict Plugin／Marketplace validation。
3. 由 Git commit 的乾淨來源製作兩次 deterministic ZIP，比對 bytes、inventory 與 checksums，避免 Windows 工作目錄換行差異影響發布來源。
4. 獨立審閱版本、安裝命令、source ref、文件與附件；排除本機驗證輸出、下載的 CLI binary、個人資料及既有使用者 Knowledge Base 修改。
5. 建立發布 commit，正常 fast-forward push（不 force）、建立新 tag、上傳 ZIP 與 checksum，再公開 prerelease。
6. 以公開 URLs 重新下載附件並比對 SHA-256，確認 catalog／tag 存在且 latest stable 仍為 1.3.1。

Builder 的 `--preview-claude` 保持只證明離線打包；外部發布由這份明確核准與 GitHub prerelease 記錄授權，不把 `preview.json` 當正式驗收或發布證明，也不將它上傳為使用者附件。

## 已接受的限制

- 未執行登入後的官方 Claude Code 真實 session、完整雙 profile 行為、context reduction 與三作業系統實測。
- Claude 4.6+、Claude Code 2.1.251+、Node 22+ 是相容性目標；native strict validation 只證明結構可解析。
- 使用者提供的 VS Code／Cline 報告屬離線檢查，不能代替官方 Claude Code live evidence。
- 不登入、不進行模型付費呼叫、不對外發送訊息或公告。

正式 1.4.0 的原始需求、歷史證據與未完成 gates 保留原狀；本次不宣稱所有原 Tickets 完成。
