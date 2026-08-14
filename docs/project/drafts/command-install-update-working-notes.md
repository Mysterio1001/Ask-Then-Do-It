# 指令安裝與版本更新 Draft Working Notes

Artifact type: Draft Working Notes

Artifact ID: `command-install-update-working-notes`

Workflow ID: `command-install-update`

Target Core version: `1.1.0`

Status: Draft

## Inputs

- 使用者於 2026-08-13 提出的需求：讓 Ask Then Do It 可透過 Codex 指令安裝，並在新版本發布後讓使用者要求 AI 執行安裝或更新。
- 現有 GitHub repository：`Mysterio1001/Ask-Then-Do-It`，預設分支為 `main`。
- 現有 Codex Plugin：`adapters/codex/plugin/ask-then-do-it/`。
- 已核准的 `grill-me-clean-slate-1.0.0` Requirement Decision Record 與 Specification。
- OpenAI 官方 Plugin marketplace 文件（2026-08-13 查核）。

## Requirement decision map

### Confirmed

- `confirmed`：Plugin 必須可由 GitHub marketplace 來源加入 Codex，而不再要求使用者下載 ZIP 並手動複製 Plugin 資料夾。
- `confirmed`：新版本發布後，使用者必須能以自然語言要求 AI 執行對應的 marketplace 更新與 Plugin 重新安裝流程。
- `confirmed`：現有 Plugin 已有 `.codex-plugin/plugin.json` 與九個 Skill，可作為 marketplace 中的安裝來源。
- `confirmed`：目前 repository 尚無 `.agents/plugins/marketplace.json`，所以 `codex plugin marketplace add Mysterio1001/Ask-Then-Do-It` 尚不能形成完整安裝流程。
- `confirmed`：本需求會取代舊規格中「不得新增 marketplace entry」及「僅手動安裝」的現況限制；舊文件仍保留為歷史證據。
- `confirmed`：marketplace catalog 追蹤 repository 的 `main`；marketplace entry 中的 Plugin 來源固定到最新正式 Git tag。每次發布新版時，maintainer 必須同步把 entry 更新到新 tag，避免安裝到尚未正式發布的 `main` 內容。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：第一個支援指令安裝與 AI 輔助更新的產品版本為 `1.2.0`。既有 `v1.1.0` 保持不可變；`1.2.0` 實作必須同步更新 Plugin manifest、marketplace entry、release 設定、使用者文件、下載連結與產物。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：`README.md` 的既有內容、順序、字句與連結原則上不得修改；唯一允許修改的既有內容是把三種語言目前的 `1.1.0` ZIP 顯示文字與下載 URL 更新為 `1.2.0`。除此之外，只能分別以英文、繁體中文與日文插入本次新增的「支援指令更新」說明；各語言內容必須緊接在該語言的 `Read more:`、`更多說明：`、`詳しい説明：` 之前。使用者於 2026-08-13 明確修正此邊界。
- `confirmed`：AI 不得在安裝或更新失敗後自動降版。失敗時必須保留目前已安裝版本（若有）、回報失敗命令與原因，並停止後續步驟；只有使用者明確指定舊 tag 或版本時，AI 才能執行降版。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：使用者文件以自然語言要求 AI 安裝或更新為主要介面，並在其下提供對應的 Codex CLI 命令，供使用者核對、手動執行與除錯。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：GitHub Release ZIP 手動安裝在 `1.2.0` 之後仍是正式備援方式，供 CLI marketplace 無法使用、CLI 版本過舊或環境受限制時使用；每次發布仍須維護 ZIP、checksum 與相關測試。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：AI 必須先以唯讀命令偵測 marketplace、Plugin 與版本狀態，再決定動作。marketplace 不存在時才加入來源並安裝；marketplace 已存在時先升級 catalog 再重新安裝；已是最新正式版本時只回報、不寫入；無法可靠判斷時停止並回報，不猜測執行。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：版本一致性是強制 release gate。marketplace entry 的正式 Plugin tag、Plugin manifest、release 設定、ZIP 名稱、checksum 與正式版本文件任一不一致時，驗證必須失敗並阻止發布。`v1.2.0` tag 所指向的 commit 必須包含固定至 `v1.2.0` 的 marketplace entry。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：使用者明確要求「安裝」或「更新 Ask Then Do It」時，已授權 AI 在完成唯讀狀態偵測後執行該次必要的 marketplace 與 Plugin 寫入，不須重複確認。「檢查版本」或語意不明的要求只授權讀取狀態，不得寫入。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：`.agents/plugins/marketplace.json` 僅屬於 Git repository 的 CLI 安裝來源，不放入消費者 ZIP；ZIP 繼續作為獨立的離線手動備援包。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：marketplace entry 只允許固定的 HTTPS GitHub URL `https://github.com/Mysterio1001/Ask-Then-Do-It.git`，並固定使用 `git-subdir` 與正式 tag；不支援 SSH、HTTP、使用者輸入的替代來源或可變 URL。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：正式文件與測試只採用 `codex plugin add` 作為 Plugin 安裝子命令，不以 `codex plugin install` 作為本專案契約。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：使用者原先指定的燈塔圖片已被後續選擇取代，不得加入 Plugin。
- `confirmed`：最終圖示來源改為 `C:/Users/Ian/AppData/Local/Temp/codex-clipboard-473a2d00-e6c4-415e-a8be-e4cd3548c12d.png`。該檔案為 `1024×956`、24-bit RGB、無 alpha 通道的紅色海馬問號圖。使用者要求將其調整為 Plugin 圖示資產，加入 Plugin，並更新 `plugin.json` 的 `interface.brandColor`、`interface.composerIcon` 與 `interface.logo`。
- `confirmed`：圖示採透明背景。處理時保留紅色海馬問號主體，移除淺灰白背景並清理邊緣暈染，使圖示可用於亮色與深色 Codex 介面。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：最終圖示規格為 512×512 透明背景的 `assets/icon.png`、1024×1024 透明背景的 `assets/logo.png`，主體等比例置中並保留安全留白，不重新設計；`plugin.json` 使用 `brandColor: "#C8262A"`、`composerIcon: "./assets/icon.png"`、`logo: "./assets/logo.png"`。使用者於 2026-08-13 回覆「核准」。
- `confirmed`：最終來源圖片的 SHA-256 為 `C22CF733EBF01ECFEB9C5E9A29AC37496A8B78BBE09F22D5942EC31F0B374EBB`，供後續實作驗證使用。

### Proposed

- `proposed`：在 repository 新增 `.agents/plugins/marketplace.json`，marketplace 名稱與 Plugin 名稱皆使用 `ask-then-do-it`。
- `proposed`：使用者第一次安裝時執行 `codex plugin marketplace add Mysterio1001/Ask-Then-Do-It`，再從該 marketplace 安裝 `ask-then-do-it`。
- `proposed`：更新時由 AI 執行 marketplace refresh/upgrade、重新安裝 Plugin，並要求使用者開啟新 Codex 任務載入新版。
- `proposed`：同步修改三種語言的 Plugin start guide 與 Codex guide，將 GitHub 指令流程設為主要安裝方式，ZIP 手動流程降為復原或備援方式；README 僅按已確認邊界插入三種語言的支援指令更新說明。
- `proposed`：以自動化測試驗證 marketplace schema、來源路徑、版本一致性、文件指令及 release package 邊界。
- `proposed`：保留紅色海馬問號圖形，不重新設計；先將非正方形來源調整為適合 Plugin 的正方形視覺，再產生 512×512 的 `assets/icon.png` 與 1024×1024 的 `assets/logo.png`。

### Unresolved

None. All material product decisions are confirmed or intentionally deferred.

## Assumptions

- Codex CLI 的實際可用命令以 OpenAI 官方文件與目標使用者安裝版本為準；目前工作環境的 `codex.exe` 因作業系統拒絕存取而無法執行唯讀 help 驗證。
- 「用 AI 指令去安裝」指使用者以自然語言授權 AI 執行 Codex CLI 更新流程，不代表 repository 在背景自動修改使用者環境。
- GitHub Release 發布與 marketplace 檔案更新會由 maintainer 控制，不在需求詢問階段執行外部發布。

## Deferred

- 發布到 OpenAI universal public Plugins Directory。
- 背景自動檢查、推播或無人值守自動更新。
- GitHub Release 建立、tag、push 與外部公告的實際執行。

## Next decision

產生完整 Requirement Decision Record 與 Project Knowledge Base Change Summary，請求單一明確核准。

## Handoff

Requirement Decision Record 與 Project Knowledge Base Change Summary 已核准；handoff 至 `$write-spec`。

## Approval

Draft Working Notes 本身維持 Draft 且不構成實作授權。其衍生的完整 Requirement Decision Record 與 Knowledge Base changes 已由使用者於 2026-08-13 明確核准。
