# Ask Then Do It Generic prompts 使用說明

本指南說明如何在 Gemini 或其他一般語言模型使用 Ask Then Do It。它不要求 Codex，也不把 Codex 的 Plugin、工具或 multi-agent 能力套到別的模型。正式規則以 [Ask Then Do It Clean-slate 1.0.0 Specification](../specs/ask-then-do-it-1.0.0.md) 為準；設計理由請見 [繁體中文設計說明](../design/ai-development-skills.zh-TW.md)。

## 目前版本

Repository 內的 canonical prompts 與 `dist/generic/ask-then-do-it-generic-1.0.0/` release 都已包含 Knowledge Base 與架構診斷。`1.0.0` 是第一個公開版本。

## 建置與檔案

在 repository 根目錄執行：

```powershell
python scripts/build_release.py
```

目前已驗證的 Generic 套件包含：

主要入口是 `dist/generic/ask-then-do-it-generic-1.0.0/generic-workflow.md`；模組化檔案位於 `dist/generic/ask-then-do-it-generic-1.0.0/prompts/`。

```text
dist/generic/ask-then-do-it-generic-1.0.0/
├─ START-HERE.zh-TW.md
├─ generic-workflow.md
├─ manifest.yaml
└─ prompts/
   ├─ bootstrap.md
   ├─ orchestration.md
   ├─ requirements.md
   ├─ documented-requirements.md
   ├─ specification.md
   ├─ ticket-planning.md
   ├─ tdd-implementation.md
   ├─ review.md
   └─ architecture-improvement.md
```

Canonical source 位於 `adapters/generic-prompts/`，其中包含：

- `documented-requirements.md`
- `architecture-improvement.md`

這兩個模組已進入 `1.0.0` 的 all-in-one 與 `prompts/` 套件。

## 一份檔案快速開始：貼上一次

建議使用 all-in-one `generic-workflow.md`：

1. 複製全文到新對話的 system、developer 或第一則 user prompt；位置取決於模型介面。
2. 提供需求、偏好語言、能力證據及目前擁有的完整 Artifacts。
3. 新工作流會在第一個有效回應中簡短說明能力與階段，然後立刻提出第一個需求問題，並附上建議答案與主要取捨；不需要再說「開始」。
4. 恢復工作流會先驗證 Artifact 與核准證據，再前往第一個未完成階段，不會無故重新開始需求審問。
5. 每次只處理一個階段或一個需求問題，並在 stop condition 停下。

範例：

```text
User request:
<你的需求>

Preferred language:
Traditional Chinese

Existing artifacts:
<none，或貼上完整 Artifact 與 approval evidence>
```

## Conversation-only 能力邊界

Generic adapter 唯一經驗證的 profile 是 `conversation`。模型不得聲稱：

- 已讀取或修改 repository。
- 已執行命令、測試、lint、build 或部署。
- 已替使用者保存跨 session 狀態。
- 已完成真實 TDD 或產生 Implementation Evidence。
- 已完成具隔離條件的獨立 Review。
- 已做真正的刪除實驗。

實作階段只能產生 `UNEXECUTED IMPLEMENTATION GUIDANCE`。Review 必須標示 `limited-evidence` 與 `non-independent`。

證據不足要標記 `unverified`；Conversation 模式做不到的檢查要標記 `unavailable`。AI 不能把「沒有資料」寫成 `no-finding`。

## 核准點不會自動跨越

工作流有三個主要人類決策：

1. Requirement Decision Record 是否代表需求共識。
2. Draft Specification 是否核准為 `Approved`。
3. Draft Ticket Plan 是否核准為 `Approved`。

模型不能把沉默、無關回覆、另一份文件的核准，或只改過的 `Status: Approved` 當成有效核准證據。

## 模組化 Prompts

| Prompt | 用途 |
| --- | --- |
| `bootstrap.md` | 宣告能力、盤點 Artifacts，fresh workflow 立刻進入第一個需求問題 |
| `orchestration.md` | 判斷第一個未完成階段與自動路由 |
| `requirements.md` | 一次問一個高影響問題 |
| `documented-requirements.md` | 一次問一題，同時維護 Draft Working Notes 與 Project Knowledge Base 提案 |
| `specification.md` | 產生並核准行為 Specification |
| `ticket-planning.md` | 產生並核准垂直 Ticket Plan |
| `tdd-implementation.md` | 產生尚未執行的 TDD 交接 |
| `review.md` | 對使用者提供的證據做有限、非獨立 Review，檢查 12 項視角 |
| `architecture-improvement.md` | 做唯讀架構診斷、依賴追蹤與模擬刪除 |

進階使用者可直接選擇模組；all-in-one 會依 Artifacts、意圖與第一個未完成 gate 自動判斷。

## 自動路由怎麼判斷

AI 會在三種情況選擇文件化需求模式：

- Project Knowledge Base 已存在。
- 需求正在修改既有系統。
- 討論會產生值得長期保存的專案知識。

AI 必須先說明原因。你明確指定一般或文件化模式時，以你的選擇為準。

架構診斷只在直接要求、Review 發現系統性證據、完成一組相關 Tickets，或接近 release milestone 時啟動，不會每張 Ticket 都跑。

## Project Knowledge Base 與 Draft Working Notes

正式 Project Knowledge Base 的邏輯位置是 `docs/project/knowledge-base.md`。在 Conversation-only 模式中，AI 只能輸出完整 Markdown，由使用者保存。

審問內容先放 Draft Working Notes，標記：

- `proposed`：還沒確認。
- `confirmed`：對話中已確認，但還沒正式核准。
- `unresolved`：缺少證據或互相衝突。

AI 必須一起展示 Requirement Decision Record 及 Knowledge Base 的 `additions`、`modifications`、`removals`。只有你明確核准後，內容才可視為正式知識。

## 12 項 Review 與架構診斷

`review.md` 針對本次變更檢查全部 12 項架構與重構視角。`architecture-improvement.md` 會在模組或系統範圍做更深入分析，再加入依賴追蹤和模擬刪除。

模擬刪除只分析「拿掉它會壞什麼」，不真的刪除、移動或改寫檔案。Architecture Improvement Report 即使變成 `accepted`，也只能回到 Specification；仍要核准 Specification、Ticket Plan，再由有工具的主機執行 TDD。

## 保存 Artifact 與恢復工作流

Conversation-only 模型沒有可靠的跨 session 記憶。請保存：

- Requirement Decision Record。
- Specification。
- Ticket Plan。
- Implementation Evidence 或未執行交接。
- Review Report。
- Project Knowledge Base 與 Draft Working Notes。
- Architecture Improvement Report。

新對話中重新貼上完整內容，包括 `artifact_type`、ID、`workflow_id`、`core_version`、狀態、輸入、假設、延後項目、handoff 與 approval evidence。不要只說「上一個 AI 已經核准」。

## 驗證與完整性

目前的 `1.0.0` 套件驗證命令是：

```powershell
python -m unittest discover -s tests/generic -p "test_*.py" -v
python -m unittest discover -s tests/release -p "test_*.py" -v
Get-FileHash dist/generic/ask-then-do-it-generic-1.0.0.zip -Algorithm SHA256
```

雜湊必須等於 `dist/checksums.sha256`。`dist/` 是 generated output；修改 Prompt 要編輯 canonical source，再重新建置。

Generic prompts 不需要安裝，也不會自動變更模型帳號或個人環境。
