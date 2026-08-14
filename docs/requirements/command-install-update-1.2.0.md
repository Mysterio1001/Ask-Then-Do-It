# Ask Then Do It 1.2.0 指令安裝、更新與 Plugin 圖示 Requirement Decision Record

Artifact type: Requirement Decision Record

Artifact ID: `command-install-update-1-2-requirements`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Target release version: `1.2.0`

Status: Approved

Inputs: 使用者於 2026-08-13 確認的指令安裝、AI 輔助更新、版本安全、README 邊界與 Plugin 圖示決策；現有 `1.1.0` Plugin、release 與文件契約；OpenAI 官方 Plugin marketplace 文件；最終圖示來源 SHA-256 `C22CF733EBF01ECFEB9C5E9A29AC37496A8B78BBE09F22D5942EC31F0B374EBB`。

Assumptions: 目標 Codex 版本支援官方文件中的 GitHub marketplace、`marketplace upgrade` 與 `plugin add`；目前工作環境的 `codex.exe` 因系統拒絕存取而無法執行 help 實測。自然語言「安裝／更新」是該次必要寫入的明確授權，不是背景自動更新。

Deferred: OpenAI universal public Plugins Directory、背景檢查或推播、無人值守更新、實際 GitHub tag／Release／push／公告、私人 fork marketplace。

Handoff: `$write-spec` after approval.

Approval: 使用者於 2026-08-13 在完整 Requirement Decision Record 與 Knowledge Base Change Summary 展示後明確回覆「核准」。

## Problem and desired outcome

目前 Plugin 雖可由 ZIP 手動安裝，但 repository 缺少 GitHub marketplace catalog，使用者無法用簡單的 Codex 指令安裝，也無法在正式新版本發布後要求 AI 安全地檢查並更新。Plugin 同時缺少安裝介面使用的品牌色與圖示。

目標是發布 `1.2.0`：提供固定官方來源、只安裝正式 tag 的 GitHub marketplace；讓使用者以自然語言要求 AI 完成首次安裝或更新；保留 ZIP 作為正式備援；並加入由指定紅色海馬問號圖處理出的透明 Plugin icon 與 logo。

## Users and success signals

- 新使用者可要求 AI 安裝 Ask Then Do It；AI 先檢查狀態，只在 marketplace 不存在時加入官方來源，再用 `codex plugin add` 安裝。
- 既有使用者可在新版本發布後要求 AI 更新；AI 先檢查狀態，升級 catalog、重新安裝，並指示開啟新 Codex 任務。
- 只要求檢查版本的使用者不會觸發任何寫入。
- 受限制或舊版 CLI 環境仍可使用正式 GitHub Release ZIP。
- 維護者無法發布版本宣告、marketplace tag、Plugin、ZIP、checksum 或正式文件彼此不一致的 release。
- Plugin 在亮色與深色介面均能顯示清晰、透明背景的紅色海馬問號圖示。

## Scope

- 將 active product、Core、adapters、Plugin、release 設定、產物與正式版本文件同步提升至 `1.2.0`；已發布的 `v1.1.0` 不變。
- 在 `.agents/plugins/marketplace.json` 建立 repository marketplace；catalog 由 `main` 提供，但 Plugin entry 固定到 `v1.2.0` 正式 tag。
- Plugin entry 必須使用 `git-subdir`、固定 URL `https://github.com/Mysterio1001/Ask-Then-Do-It.git` 與 `adapters/codex/plugin/ask-then-do-it` 子目錄。
- 文件以自然語言 AI 指令為主、CLI 命令為輔，正式安裝子命令只使用 `codex plugin add`。
- AI 必須先唯讀檢查 marketplace、Plugin 與版本狀態，再選擇首次安裝、更新或不變更。
- 保留 ZIP、checksum 與手動安裝文件作為正式備援；marketplace catalog 不得進入消費者 ZIP。
- 將指定來源圖處理為 `assets/icon.png` 與 `assets/logo.png`，並更新 Plugin interface。
- 新增自動化 release、marketplace、資產、manifest、文件與 README 邊界測試。

## Non-goals

- 背景自動更新、版本推播、未經使用者要求的寫入或自動降版。
- 從 HTTP、SSH、替代 repository、私人 fork 或使用者輸入 URL 安裝。
- 使用 `codex plugin install` 作為本專案正式契約。
- 把 marketplace catalog 放入 ZIP，或取消 ZIP 備援。
- 重新設計海馬問號圖形、使用已被取代的燈塔圖片，或新增 `logoDark`。
- 在本工作流中建立 Git tag、GitHub Release、push 或外部公告。

## Required behavior

### Marketplace and version policy

- Marketplace 名稱與 Plugin 名稱皆為 `ask-then-do-it`，entry policy 為 `AVAILABLE`／`ON_INSTALL`，category 為 `Developer Tools`。
- `main` 上的 catalog 只可引用最新正式 tag；`v1.2.0` tag 所指 commit 必須包含引用 `v1.2.0` 的 entry。
- 發布 gate 必須比較 marketplace tag、Plugin manifest、release 設定、ZIP 名稱、checksum 與正式版本文件；任一不一致即失敗。

### AI installation and update flow

- 明確的「安裝」或「更新 Ask Then Do It」授權該次必要寫入；「檢查版本」或語意不明只授權讀取。
- Marketplace 不存在：加入 `Mysterio1001/Ask-Then-Do-It`，再執行 `codex plugin add ask-then-do-it@ask-then-do-it`。
- Marketplace 已存在且有新版：執行 marketplace upgrade，再以同一 `plugin add` 命令重新安裝。
- 已是最新正式版：回報版本，不執行寫入。無法可靠判斷：停止並回報，不猜測。
- 失敗時保留目前版本、回報失敗命令與原因並停止；只有使用者明確指定舊 tag 或版本時才可降版。
- 成功安裝或更新後，要求使用者開啟新 Codex 任務載入新版。

### Documentation boundary

- README 只可把三種語言既有 `1.1.0` ZIP 顯示文字與 URL 更新為 `1.2.0`，並在 `Read more:`、`更多說明：`、`詳しい説明：` 前各插入對應語言的「支援指令更新」內容；其他既有文字、順序與連結不得修改。
- 三種語言的 Plugin start guide 與 Codex guide 必須把 marketplace 指令設為主要路徑，把 ZIP 標示為正式備援，並一致說明偵測、授權、失敗停止及新任務載入規則。

### Plugin visual assets

- 唯一來源是已確認 SHA-256 的紅色海馬問號 PNG；燈塔圖不得出現在 Plugin 或 release。
- `assets/icon.png` 必須是 512×512 PNG、透明背景；`assets/logo.png` 必須是 1024×1024 PNG、透明背景。
- 兩者保留原圖主體、等比例置中、安全留白、移除淺灰白背景與邊緣暈染，不重新設計。
- `plugin.json` interface 必須包含 `brandColor: "#C8262A"`、`composerIcon: "./assets/icon.png"`、`logo: "./assets/logo.png"`，且路徑指向實際打包檔案。

## Failures, security, privacy, and operations

- 不得因偵測失敗、網路失敗或 CLI 輸出不明而嘗試替代來源、重複寫入或自動降版。
- Repository 與套件不得包含 credentials、私人 marketplace 狀態、來源圖片的臨時路徑或未核准的外部 URL。
- Release build 維持 deterministic；圖示成品是 canonical Plugin source 的一部分，並必須被複製到 unpacked package 與 ZIP。
- Marketplace catalog 是 repository metadata，不是 consumer package content。

## Acceptance criteria

- `.agents/plugins/marketplace.json` schema、固定 HTTPS URL、`git-subdir`、子目錄、policy、category 與 `v1.2.0` tag 全部通過測試。
- Canonical 與 packaged Plugin validation 通過；兩個圖檔尺寸、PNG 格式、alpha、透明角落、主體覆蓋與 manifest 路徑通過測試。
- `1.2.0` 版本一致性 gate、deterministic build、ZIP equivalence 與 checksum verification 通過。
- 三種語言文件包含正確自然語言提示與 `codex plugin marketplace`／`codex plugin add` 流程，不宣稱背景自動更新或自動降版。
- README diff 僅包含核准的 `1.2.0` ZIP 替換與三個指定位置的新增段落。
- ZIP 不包含 `.agents/plugins/marketplace.json`，但包含 `assets/icon.png`、`assets/logo.png` 與更新後 manifest。
- 全部 automated tests、Codex conformance、Skill validation、Plugin validation 與 release evidence gate 通過後，才可宣告本地 `1.2.0` release 完成。

## Confirmed decisions

以上 marketplace、版本、AI 授權、狀態分流、失敗停止、ZIP 備援、README 邊界、官方來源、`plugin add` 與 icon 規格，皆由使用者在 2026-08-13 逐項明確核准。

## Explicit consensus evidence

Requirement interrogation 的逐項回覆與 Draft Working Notes 位於 `docs/project/drafts/command-install-update-working-notes.md`。使用者於 2026-08-13 在完整 record 與 Knowledge Base Change Summary 展示後明確回覆「核准」，完成本需求 gate。
