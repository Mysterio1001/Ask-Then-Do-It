# Claude 1.4.0-preview.1 發布完成記錄

> 歷史紀錄：以下結論及測試數是原審查當時的觀察。本次文件整理只更新導航；原始 inputs／Ticket 檔名與核准證據可從[清理快照](release-history.md#archive)找回。新連結指向現行摘要，不代表 reviewer 當時審閱過新文件；目前進度見[狀態](../project/status.md)。

Status: Published and publicly verified — 2026-09-09

[GitHub 預覽版](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/tag/v1.4.0-preview.1) · [已合併發布 PR](https://github.com/Mysterio1001/Ask-Then-Do-It/pull/8)

- 發布 commit：`d43f237f0f75adcb03eb3ce5f6e3320a688c9ef3`；annotated tag：`v1.4.0-preview.1`。
- Main merge commit：`a95f2965bbc0dcd70dd71bb32cf589352d3a8483`；GitHub main 要求 PR，已正常以 PR #8 合併，沒有繞過保護或 force push。
- `claude-preview` 與 `codex/release-claude-preview-1` 指向發布 commit；main merge tree 與發布 commit tree 完全相同。
- Release `draft=false`、`prerelease=true`、`make_latest=false`；公開 API 確认 latest stable 仍為 `v1.3.1`，其 tag target仍為 `028412d6dde70d5b1cffe3f7bea3ecec866397d8`。
- 公開下載的 ZIP 與 checksum 已逐 byte 比對本機已驗證附件；ZIP `55,632` bytes，SHA-256 `38d228914bf52b4eaa71f3c92e04a3397593a24c5c3a7204bf911cc870336e7b`。
- 公開 Marketplace branch、tag manifest、三語固定版本 guides 均可讀取，版本都是 `1.4.0-preview.1`。
- 離線完整回歸 `393 tests; OK (skipped=1)`；native strict validation 與独立 [發布 Review](release-history.md) 通過。正式 Claude live／model／context 與全部 OS／IDE 驗收仍待補。

## 本機工作狀態

原開發工作目錄仍在 `dev`，所有原有修改與 Claude 開發來源保留。發布使用 `.claude-offline/publication/source` 隔離 worktree；不得把原工作目錄尚顯示的 Claude untracked files 誤認為未發布，tag/PR/Release 才是本次外部發布 authority。原 `docs/project/knowledge-base.md` 修改未提交且 bytes 保持原樣。

本記錄是在 tag 凍結與公開驗證後寫入本機，未修改既有發布 tag。Tag 中的 prepublication evidence 仍是建立 tag 時的驗證快照；外部發布完成由本記錄與 GitHub Release 證明。原始 API/附件比對結果保存在本機 ignored `.claude-offline/publication/public-verification.json`。
