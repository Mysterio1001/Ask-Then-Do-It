# Ask Then Do It Codex Plugin 使用說明

本指南供人類使用者與維護者閱讀，說明 Codex Plugin 的工作流、建置、驗證、手動安裝、手動更新與手動移除。模型中立的架構理由請見 [繁體中文設計說明](../design/ai-development-skills.zh-TW.md)；正式工作流規則以 [Ask Then Do It 1.0.0 Specification](../specs/ask-then-do-it-1.0.0.md) 為準。

Repository 內的 source 與 release 都已包含八個 Skills。`1.0.0` 是第一個公開版本。

## Plugin 是 Codex adapter，不是整個核心

通用工作流規則屬於 `core/`。Codex 專用的 canonical source 位於：

```text
adapters/codex/plugin/ask-then-do-it/
├─ .codex-plugin/
│  └─ plugin.json
└─ skills/
   ├─ ask-then-do-it/
   ├─ ask-requirements/
   ├─ ask-with-docs/
   ├─ write-spec/
   ├─ plan-tickets/
   ├─ implement-tdd/
   ├─ review-code/
   └─ improve-architecture/
```

Plugin 外層資料夾與 manifest 的 `name` 都必須是 `ask-then-do-it`。八個 Skills 都可獨立呼叫；一般情況建議從 `$ask-then-do-it` 開始，由 AI 根據意圖、Artifacts 與第一個未完成 gate 選擇下一階段。

## 建置 release

在 repository 根目錄執行：

```powershell
python scripts/build_release.py
```

Codex 成品是：

- `dist/codex/ask-then-do-it/`：未壓縮 Plugin。
- `dist/codex/ask-then-do-it-1.0.0.zip`：內容以 `ask-then-do-it/` 為根的可重現 ZIP。
- `dist/checksums.sha256`：兩個 release archives 的 SHA-256。

Builder 只寫入設定中受管理的 `dist/` 目標，不會自動安裝、不會修改 personal installation、不會建立 marketplace，也不會對外發布。

`release/release.json` 指向 `1.0.0`。Builder 會安全替換完整且已驗證的 `dist/codex/`、`dist/generic/` 與目前 checksum。

## 建置後驗證

先執行 release tests：

```powershell
python -m unittest discover -s tests/release -p "test_*.py" -v
```

若本機 Codex 內含 `plugin-creator`，驗證 Plugin manifest 與 package shape：

```powershell
python "$env:CODEX_HOME/skills/.system/plugin-creator/scripts/validate_plugin.py" `
  dist/codex/ask-then-do-it
```

逐一驗證 release 內的八個 Skills：

```powershell
$validator = "$env:CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py"
Get-ChildItem dist/codex/ask-then-do-it/skills -Directory | ForEach-Object {
  python $validator $_.FullName
}
```

也應執行 Codex adapter conformance：

```powershell
python scripts/validate_conformance.py `
  --catalog core/rules/rules.yaml `
  --manifest adapters/codex/conformance.yaml
```

`Get-FileHash dist/codex/ask-then-do-it-1.0.0.zip -Algorithm SHA256` 的結果必須等於 `dist/checksums.sha256` 中對應項目。

## 安裝邊界

Codex 目前從已設定的 marketplace 安裝 Plugin，而不是直接安裝任意 ZIP。官方結構與 marketplace 語意可參考 [Package your plugin](https://developers.openai.com/plugins/build/plugins)。本 release 故意不包含 marketplace entry，也不修改任何 marketplace；第一次建立或註冊 marketplace 是另一個需要明確授權的操作。

下面命令都是給使用者自行執行的手動生命週期範例。本專案的建置與驗證不會執行它們。

## 手動安裝

前提是你已擁有一個可信任且允許修改的本機 marketplace，其 entry 名稱為 `ask-then-do-it`，並指向 `<local-marketplace-root>/plugins/ask-then-do-it`。

1. 先建置並通過上一節的驗證。
2. 備份 marketplace 中既有的 `plugins/ask-then-do-it/`；若不存在，確認 marketplace entry 已由你或管理者建立。
3. 將完整的 `dist/codex/ask-then-do-it/` 複製為 `<local-marketplace-root>/plugins/ask-then-do-it/`。不要只複製 `skills/`，也不要多包一層版本資料夾。
4. 確認 Codex 已能看到該 marketplace：

```powershell
codex plugin marketplace list
```

5. 從該 marketplace 安裝並確認狀態：

```powershell
codex plugin add ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

6. 開啟新的 Codex task，使用 `$ask-then-do-it` 測試載入結果。

若尚無 marketplace 或 entry，請停在第 2 步；建立它超出本 release 的自動化範圍，不應假設已獲授權。

## 手動更新

1. 建置並驗證新的 release，確認版本與 checksum。
2. 保留舊 Plugin 備份，再以新的完整 `ask-then-do-it/` 取代 marketplace source。
3. 重新執行安裝命令，然後以 `codex plugin list` 核對版本與來源。
4. 開啟新的 Codex task 測試，避免舊 task context 繼續使用快取內容。
5. 驗證失敗時，還原備份並重新安裝舊版本；不要修改 `dist/` 內的 generated manifest 來偽造版本。

同一版本的本機開發 cachebuster 流程不是 `1.0.0` release contract 的一部分，不能改寫已驗證 archive 後仍沿用原 checksum。

## 手動移除

先從 Codex 的 local config 與 cache 移除已安裝 Plugin：

```powershell
codex plugin remove ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

移除安裝不等於刪除 marketplace source。若還要刪除 `<local-marketplace-root>/plugins/ask-then-do-it/` 或 marketplace entry，應另行確認該 marketplace 是否仍被其他使用者或環境使用，並取得檔案刪除授權。本專案不會代為執行。

## 八個入口

| Skill | 適合用途 |
| --- | --- |
| `$ask-then-do-it` | 重大、模糊、跨模組或完整開發流程；建議的主要入口 |
| `$ask-requirements` | 一次釐清一個高影響需求決策 |
| `$ask-with-docs` | 一次問一題，暫存 Draft Working Notes，核准後同步 Project Knowledge Base |
| `$write-spec` | 把已確認需求寫成行為 Specification |
| `$plan-tickets` | 把 Approved Specification 切成垂直 Tickets |
| `$implement-tdd` | 依 Approved Plan 執行一個 Ticket 的 red-green-refactor |
| `$review-code` | 依核准意圖、diff 與原始驗證結果執行 Review，掃描固定 12 項視角 |
| `$improve-architecture` | 做唯讀架構診斷、依賴追蹤、模擬刪除與 Architecture Improvement Report |

AI 可以自動判斷應使用哪個模組，但 Requirement、Specification 與 Ticket Plan 的人類核准點不能由 AI 自行跨越。

## AI 何時自動選擇新模組

`$ask-then-do-it` 在下列情況選擇 `$ask-with-docs`：

- Project Knowledge Base 已存在。
- 要修改既有系統。
- 討論會產生值得長期保存的術語、架構或決策。

AI 必須先簡短說明原因。使用者直接指定 `$ask-requirements` 或 `$ask-with-docs` 時，以使用者選擇為準，但不能跳過安全或核准 gate。

`$improve-architecture` 只在直接要求、Review 發現系統性問題、完成一組相關 Tickets，或接近 release milestone 時啟動，不會每張 Ticket 都跑。

## Project Knowledge Base

Repository-backed 工作流的正式 Knowledge Base 位於 `docs/project/knowledge-base.md`。審問中的未批准資訊先放 Draft Working Notes，標記 `proposed`、`confirmed` 或 `unresolved`。

## 12 項 Review 與架構安全

`$review-code` 會檢查本次變更的 12 項核心視角，每項都要有 `finding`、`no-finding`、`not-applicable` 或 `unverified` 與對應證據。系統性發現才交給 `$improve-architecture`。

`$improve-architecture` 的模擬刪除只追蹤「拿掉它會壞什麼」，不會真的刪除、移動或改寫。實際刪除實驗還需要獨立的明確授權、`tools` 能力及可丟棄隔離環境。本指南與目前開發流程都沒有授權實際刪除。

Architecture Improvement Report 即使變成 `accepted`，也只能回到 `$write-spec`；仍須核准 Specification、Ticket Plan，最後才可用 TDD 實作。
