# 目前狀態與後續工作

整理日期：2026-09-10。此頁以當前來源、已保留的 Review、發布收據及原始離線證據彙整進度；歷史結果不當成本次重跑結果。文件合併與刪除已由使用者明確核准，整理本身不代表新的功能或 Claude 實測完成。

## 已交付與證據邊界

| 項目 | 狀態 | 可支持的結論 |
| --- | --- | --- |
| Core、Codex、Generic、Claude 來源版本 | 1.4.0 | 當前 manifests、runtime 與 release config 已對齊 |
| Claude Plugin 公開邊界／Marketplace | 原 Ticket 1 已完成 correction | [最新接受的 Review](../evidence/claude-code-adapter-1.4.0-ticket-1-marketplace-description-correction-review.md)；不等於 authenticated host 通過 |
| Claude router／session state | 原 Ticket 2 已完成 provisional implementation | [第十輪修正後 Review](../evidence/claude-code-adapter-1.4.0-ticket-2-review-after-tenth-corrections.md)；真實 host 若不符仍須修正 |
| exact Claude Code 2.1.251 | 已有 binary provenance、strict validation 與測試工具 | [Ticket 3 Review](../evidence/claude-code-adapter-1.4.0-ticket-3-review.md)仍要求 live observations |
| General 與 Claude 5 profiles | 靜態修正 accepted，完整 Ticket 4／5 未完成 | [General Review](../evidence/claude-code-adapter-1.4.0-ticket-4-review-after-third-correction.md)、[Claude 5 Review](../evidence/claude-code-adapter-1.4.0-ticket-5-review-after-third-correction.md) |
| Behavior／context 工具及 templates | 離線準備完成 | 本機 behavior ledger 為 unexecuted／pending、context capture 為 unobserved，未取得正式模型結果 |
| 三語指南與三套件封裝 | 2026-09-10 對齊工作已完成離線整合 | [整合 Review](../evidence/documentation-and-version-alignment-1.4.0-ticket-3-review.md)；原紀錄為 394 tests、393 passed、1 Windows symlink skip |
| 1.4.0-preview.1 對外發布 | 有 2026-09-09 published/publicly-verified 收據 | [發布收據](../evidence/claude-preview-publication-1.4.0-preview.1-receipt.md)；不把當時遠端狀態稱為本次重新查核 |
| 正式 1.4.0 完整驗收／對外發布 | 未證明完成 | 來源升版與離線 ZIP 不是完整 release；不因指南的下載 URL 存在就推論遠端資產存在 |

## 必須接續的驗證

| 次序 | 工作與完成條件 | 依據／相依 |
| --- | --- | --- |
| 1 | exact 2.1.251 authenticated namespaced invocation、command identity、additionalContext，以及 Node missing／nonzero／exit 2／timeout 的實際 expansion 行為 | 原 Ticket 3；[host 程序](../maintainer/validation.md#指定-claude-host-驗證)。保持最低版本，不靠新版通過代替 |
| 2 | General／Claude 5 各 30 mandatory scenarios 實際執行，逐一判讀結果 | 原 Tickets 4／5；來源已凍結、host 契約不矛盾，任何 skip／partial 不算 pass |
| 3 | 12 paired cases 的等價結果及 general→Claude 5／反向的同 session authority，共 86 個 fresh-session runs | 原 Ticket 6；相同 model／effort／tools／完整 user messages，不能把 source snapshot 當 model observation |
| 4 | 十情境各 stage-ready 及 Full Review reviewer-ready 的 50% loaded-context reduction | 原 Ticket 7；先通過 actual behavior，逐 checkpoint 判斷，不平均抵銷失敗 |
| 5 | 依實際觀察核對文件，凍結三平台 candidate，完成 parity、checksum、reproducibility 與相關套件驗證 | 原 Tickets 8／9；離線文件／版本／封裝已完成，剩下正式整合與觀測對齊 |
| 6 | 至少一個乾淨真實環境跑完整 install、兩入口、route／switch、session、update、remove、reinstall／ZIP recovery，再做 final Review／release evidence | 原 Ticket 10；前述正式 gates 通過後才宣告完整 local 1.4.0 完成 |

原 Claude 計畫於 2026-09-05 核准十張 Ticket 全部加測試（`tdd`）。2026-09-07 允許 Ticket 3 暫未完成時先做 Ticket 2／profiles；2026-09-09 又允許 Tickets 6–9 的離線準備。這些是排序調整，不免除 live、behavior、context 或最終驗收。2026-09-10 的版本對齊工作為 Ticket 1／3 加測試、Ticket 2 direct（`tests: skipped-by-user`）；不要把整合 suite 的通過改寫成 direct Ticket 執行了行為測試。

真實 host 若與 provisional matcher、hooks 或 failure semantics 不符，回最早受影響的規格／實作重驗，不悄悄提高 minimum、不依實作方便改需求。未來操作的授權仍依該次請求；本次清理沒有執行模型呼叫、安裝、提交或發布。

## 原始本機資料

- `.ticket3-preflight/claude-code-2.1.251/`：指定 binary、manifest 與 signature。原觀察 binary SHA-256 為 `8d1229a281281b98fd2dee72b3253a704be4fce4d45207200cd32a9bb5a6c909`；當時 Authenticode Valid、signer Anthropic, PBC。Detached PGP signature 未驗證，不能把下載 signature 當驗證成功。
- `.claude-offline/verification/`：prepared behavior ledger／prompts，整理前 transcripts 目錄沒有檔案。
- `.claude-offline/context/capture.json`：尚未觀察的 capture template。
- `.claude-offline/doc-alignment-1.4.0/`：before snapshot、raw Red／Green／integration logs、candidate hashes、build-a。重複 build-b 在清理前逐檔核對；其原始副本保存在[清理快照](../evidence/release-history.md#archive)。
- `.claude-offline/publication/`、`main-revert/`、`vscode-live/`：發布／復原及觀察資料保留；不能因 Git 忽略就當成不存在或可任意刪除。
- `dist/`：舊 candidate 保留；當前 source 測試使用新建的隔離輸出，不把此資料夾當成最新結果。

## 可選的後續改善

下列為既有架構診斷的未接受提案，記錄用途是避免刪除舊文件後遺失問題，並非本次新增工作：

- 更細的 rule／scenario 映射與 locale-neutral checklist，降低只核對字串的盲點。
- Release-critical JSON 的 strict duplicate-key／不可縮減 checks 邊界，以及可綁定 executor、exit、raw digest、candidate 的 evidence model。
- 把 pure release composition 與 filesystem transaction 分離，降低 builder／token proxy 耦合；避免產生第二個 schema authority。
- Router 的 state store／lock、hook deadline、RouteDecision／BoundOperation 邊界與獨立 anti-drift 測試。
- 版本宣告 inventory、共用測試 helper 的責任整理；固定 preview 功能是否退役另行決定。

其他平台、universal installer／registry、Claude 非 user scopes、Desktop／web、背景更新與 Community Marketplace 均維持延後。設計理由見[知識庫](knowledge-base.md#important-decisions)。

[回到 README](../../README.md)
