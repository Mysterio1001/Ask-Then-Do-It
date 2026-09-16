# Codex Skill Runtime Slimming — Draft Working Notes

Artifact type: Draft Working Notes

Artifact ID: `codex-skill-runtime-slimming-working-notes`

Workflow ID: `codex-skill-runtime-slimming-2026-09-15`

Core version: `1.4.1`

Status: Draft

Inputs: 使用者提供的 GPT-6 Astra skills／AGENTS.md 優化原則、2026-09-15 Codex runtime 唯讀稽核、現行 Core／Codex adapter／tests／release contracts。

Assumptions: 本次操作依 project Config、user Config 均不存在而採 Full fallback；第一階段尚未獲准修改 runtime；官方頁面於本環境無法驗證，官方原則暫以使用者提供內容及 bundled migration guidance 為準。

Deferred: 跨模型 live eval 的 exact model／host matrix、是否調整其他 adapters、正式 release 與遠端發布。

Handoff: 先確認第一版是否只做行為等價的結構瘦身，再完成 Requirement Decision Record 與 Knowledge Base Change Summary。

Approval: Requirement boundary confirmed by user on 2026-09-16; formal RDR and Knowledge Base Change Summary approval pending.

## Confirmed

- `confirmed`：目標是瘦化、優化與分責 Codex runtime skills。
- `confirmed`：主要問題是廣泛觸發、主 router 過重、八份 mode guard 重複、artifact envelope 與 architecture lenses 重複，以及測試過度綁定 prompt 原句。
- `confirmed`：關鍵安全與流程不變量不能因 Astra 最佳化而被隱含化，包括 mode precedence、approval state、TDD Red、Direct 禁止行為測試及 evidence honesty。
- `confirmed`：progressive disclosure 應維持單層、在動作點明確要求讀取，降低 GPT-6 以前模型漏讀風險。
- `confirmed`：本專案目前沒有 `AGENTS.md`，不把新增大型 `AGENTS.md` 納入預設範圍。
- `confirmed`：使用者於 2026-09-16 回覆「核准」，確認第一版採行為等價的結構瘦身邊界。

## Proposed

- `proposed`：第一版只做行為等價重構：縮短 descriptions、將 orchestrator 改為 router、集中 mode resolver／artifact envelope／lenses references、以短 local guard 取代重複段落，並將逐字測試改為契約測試。
- `proposed`：第一版保留 universal software-change trigger、Full/Lite semantics、所有 approval gates、Review 十二 lenses 要求及 Lite findings correction approval。
- `proposed`：第二版才個別評估收窄 universal trigger、條件式十二 lenses、以及已核准範圍內 Review 自動修復。
- `proposed`：只優化 Codex adapter；Core 只有在修正 mapping／可達性契約所必需時才改，Generic 與 Claude runtime 行為不變。

## Unresolved

- `confirmed`：第一版明確採「行為等價」範圍，將三項產品行為調整全部延後。
- `unresolved`：跨模型驗收要使用哪些可用 GPT-5.x／GPT-6 模型與何種 fresh-session cases。
- `unresolved`：本次成果是否升版、建置 candidate 或只完成來源與離線驗證。
