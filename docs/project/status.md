# 目前狀態與後續工作

**目前可下載版本為 v1.5.0**，於台灣時間 2026-11-22 正式發布。Codex、Claude Code、Generic 三個 ZIP 與校驗檔均已從 GitHub 公開下載並驗證。[下載 v1.5.0](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/tag/v1.5.0)

1.5.0 包含精簡確認流程、分批清理 Claude 對話狀態及通用版獨立的 `LITE.md`。完整回歸 511 項，509 項通過，2 項因 Windows 權限略過。選配的 Claude live qualification 維持 `not run`／`unverified`。[發布驗證紀錄](../evidence/ask-then-do-it-release-1.5.0.md)

## 已交付與證據邊界

| 項目 | 狀態 | 可支持的結論 |
| --- | --- | --- |
| Core、Codex、Generic、Claude 來源版本 | 來源已統一為 1.5.0 | 正式下載與三個套件均對應 `v1.5.0` tag |
| 1.4.1 本機候選包與回歸驗證 | 2026-09-11 完成 | 原頂層 `ticket-release-141-build-candidate/` 目前不存在；三平台 ZIP 的本機保留副本位於 `.claude-offline/formal-release-1.4.1-20260911/source/ticket-release-141-build-a/`。396 tests、395 passed、1 Windows symlink skip；套件 inventory／checksum／來源一致性、兩次建置 81 個輸出檔案一致性及獨立 Review 通過；未實測 Claude Desktop 匯入／觸發，不等於正式 release gates 完成 |
| Claude Plugin 公開邊界／Marketplace | 原 Ticket 1 已完成 correction | [最新接受的 Review](../evidence/claude-code-adapter-1.4.0-ticket-1-marketplace-description-correction-review.md)；不等於 authenticated host 通過 |
| Claude router／session state | 原 Ticket 2 已完成 provisional implementation | [第十輪修正後 Review](../evidence/claude-code-adapter-1.4.0-ticket-2-review-after-tenth-corrections.md)；真實 host 若不符仍須修正 |
| exact Claude Code 2.1.251 | 已有 binary provenance、strict validation 與測試工具 | [Ticket 3 Review](../evidence/claude-code-adapter-1.4.0-ticket-3-review.md)仍要求 live observations |
| General 與 Claude 5 profiles | 靜態修正 accepted，完整 Ticket 4／5 未完成 | [General Review](../evidence/claude-code-adapter-1.4.0-ticket-4-review-after-third-correction.md)、[Claude 5 Review](../evidence/claude-code-adapter-1.4.0-ticket-5-review-after-third-correction.md) |
| Behavior／context 工具及 templates | 離線準備完成 | 本機 behavior ledger 為 unexecuted／pending、context capture 為 unobserved，未取得正式模型結果 |
| 三語指南與三套件封裝 | 2026-09-10 對齊工作已完成離線整合 | [整合 Review](../evidence/documentation-and-version-alignment-1.4.0-ticket-3-review.md)；原紀錄為 394 tests、393 passed、1 Windows symlink skip |
| 1.4.0-preview.1 對外發布 | 有 2026-09-09 published/publicly-verified 收據 | [發布收據](../evidence/claude-preview-publication-1.4.0-preview.1-receipt.md)；不把當時遠端狀態稱為本次重新查核 |
| 正式 1.4.0 完整驗收／對外發布 | 未證明完成 | 來源升版與離線 ZIP 不是完整 release；不因指南的下載 URL 存在就推論遠端資產存在 |
| 正式 1.4.1 完整驗收／對外發布 | 2026-09-18 查得歷史 stable tag 與 GitHub Release；完整 Claude live gates 未證明 | `v1.4.1` annotated tag object `b4c91a3ea623c0931f8459ce3f46b638f4cfdc2e` 指向 commit `ebf465c54f44a4c2d1a8e17692161c0d5d38f72e`；stable Release ID `386983777` 有四個 assets。公開存在不等於當時完整驗收通過 |
| 正式 1.4.3 | 已發布 | GitHub 提供三套 ZIP 與校驗檔。[發布資訊](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/tag/v1.4.3)。1.4.2 的 required ledger 與 evidence 保留為歷史紀錄 |

## 文件生命週期整理

2026-09-16 已完成一個代表性 Full workflow migration：Codex skill runtime
slimming 的三份 provisional drafts 現由一份 [Decision Packet](drafts/codex-skill-runtime-slimming/decision-packet.md)
承接。三個舊路徑只保留 metadata-only pointers；[lifecycle manifest](drafts/codex-skill-runtime-slimming/lifecycle-manifest.json)
與 [source manifest](drafts/codex-skill-runtime-slimming/migration/source-manifest.json) 保留原始 bytes、artifact IDs、SHA-256 與 rollback
資訊。Migration 完成時所有 packet sections 均為 `Draft`；使用者其後於 2026-09-16 共同核准完整 Requirement Decision Record 與 Knowledge Base Change Summary。Working Notes 與 packet envelope 仍為 `Draft`，兩個核准 sections 已保存 approval evidence，unresolved／deferred 狀態未被提升。

本次 migration validator 已在 bundled Python 執行成功；它只驗證，不自動刪除或修復檔案。這次整理沒有新增正式 Knowledge Base fact，沒有改變
Full／Lite routing、approval gates、evidence semantics、test-choice 或 release 行為。Generic／Claude adoption、archive retention
policy 與 live model evidence 仍是 deferred／environment-limited 項目。

Codex-only behavior-equivalent slimming 的 durable facts 已同步至 [Project Knowledge Base](knowledge-base.md)。使用者於 2026-09-16 核准完整 [Specification](../specs/codex-skill-runtime-slimming.md)，於 2026-09-17 選擇 T1-T5 全部加測試（`tdd`），並核准 [Ticket Plan](../plans/codex-skill-runtime-slimming.md)。T1-T5 source implementation、isolated package、before/after proxy、完整回歸與 independent Review 均已完成；逐 Ticket 過程報告在本次 repository 瘦身移除，保留 baseline、正式 Specification／Plan、知識庫事實與 Git 歷史／外部快照作追溯。量測不能被解讀為所有 Full route 總載入量都縮小；GPT-5.x／GPT-6 fresh-session compatibility 仍為 `unverified`。

## 選配 Claude live qualification

Exact-host invocation、General／Claude 5 behavior、86 fresh sessions、50% context checkpoints，以及 clean environment lifecycle smoke 均保留為選配 qualification。未另行明確授權時，不要求登入、不啟動 OAuth／模型呼叫、不匯出 sessions／transcripts；狀態維持 `not run`／`unverified`，不得冒稱 passed 或 `live-verified`。若日後選配實測已揭露重大 correctness、安全、隱私或資料損失 finding，該已知 finding 仍交一般 Review gate 判定。

原 Claude 計畫於 2026-09-05 核准十張 Ticket 全部加測試（`tdd`），其後曾調整排序但未免除當時的 live gates；這些是歷史決策。自 1.4.2 起，使用者已明確把 authenticated host／model／context／lifecycle 改為 optional qualification，但不把任何未執行觀察改寫成 passed。2026-09-10 的版本對齊工作為 Ticket 1／3 加測試、Ticket 2 direct（`tests: skipped-by-user`）；不要把整合 suite 的通過改寫成 direct Ticket 執行了行為測試。

真實 host 若與 provisional matcher、hooks 或 failure semantics 不符，回最早受影響的規格／實作重驗，不悄悄提高 minimum、不依實作方便改需求。未來 optional live 操作仍須依該次請求取得明確授權；本次政策實作沒有執行登入、模型呼叫、session export、安裝、提交或發布。

## 原始本機資料

- `.ticket3-preflight/claude-code-2.1.251/`：指定 binary、manifest 與 signature。原觀察 binary SHA-256 為 `8d1229a281281b98fd2dee72b3253a704be4fce4d45207200cd32a9bb5a6c909`；當時 Authenticode Valid、signer Anthropic, PBC。Detached PGP signature 未驗證，不能把下載 signature 當驗證成功。
- `.claude-offline/verification/`：歷史狀態曾記錄 prepared behavior ledger／prompts，但目前路徑實測不存在；不得把該歷史描述當成 1.5.0 的可用 evidence。若日後另行授權 T4 optional qualification，才建立全新、不可覆寫的實測根目錄。
- `.claude-offline/context/capture.json`：歷史狀態記載的本機 capture template 路徑目前不存在；checked-in template 為 `tests/release/fixtures/claude-context-proxy/capture-template.json`，仍未取得本次 actual capture。
- `.claude-offline/doc-alignment-1.4.0/`：before snapshot、raw Red／Green／integration logs、candidate hashes、build-a。重複 build-b 在清理前逐檔核對；其原始副本保存在[清理快照](../evidence/release-history.md#archive)。
- `.claude-offline/publication/`、`.claude-offline/main-revert/`：發布／復原資料仍保留；不能因 Git 忽略就當成不存在或可任意刪除。歷史記載的 `.claude-offline/vscode-live/` 目前實測不存在，不把舊描述當成可用 observation。
- `dist/` 與 `.claude-offline/`：都是本機建置／驗證輸出，不納入 release commit；最終 candidate 必須從 exact commit 的全新 clean checkouts 重建。

## 可選的後續改善

下列為既有架構診斷的未接受提案，記錄用途是避免刪除舊文件後遺失問題，並非本次新增工作：

- 更細的 rule／scenario 映射與 locale-neutral checklist，降低只核對字串的盲點。
- Release-critical JSON 的 strict duplicate-key／不可縮減 checks 邊界，以及可綁定 executor、exit、raw digest、candidate 的 evidence model。
- 把 pure release composition 與 filesystem transaction 分離，降低 builder／token proxy 耦合；避免產生第二個 schema authority。
- Router 的 state store／lock、hook deadline、RouteDecision／BoundOperation 邊界與獨立 anti-drift 測試。
- 版本宣告 inventory、共用測試 helper 的責任整理；固定 preview 功能是否退役另行決定。

其他平台、universal installer／registry、Claude 非 user scopes、Desktop／web、背景更新與 Community Marketplace 均維持延後。設計理由見[知識庫](knowledge-base.md#important-decisions)。

[回到 README](../../README.md)
