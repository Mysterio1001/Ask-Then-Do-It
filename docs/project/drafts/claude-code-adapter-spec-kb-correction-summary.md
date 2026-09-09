# Ask Then Do It 1.4.0 Claude Code Adapter Specification Knowledge Base Correction Summary

Artifact type: Knowledge Base Change Summary

Artifact ID: `claude-code-adapter-1-4-0-spec-kb-correction-summary`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Status: Approved

Inputs: Approved [Claude Code Adapter 1.4.0 Specification](../../specs/claude-code-adapter-1.4.0.md)、Approved [Specification Knowledge Base Change Summary](claude-code-adapter-spec-kb-change-summary.md)、同步後的 Approved [Project Knowledge Base](../knowledge-base.md)，以及 2026-09-04 independent knowledge-sync audit。

Assumptions: 本修正只消除一處 route guarantee 歧義及兩處 provenance 歧義；不新增或改變任何產品行為、最低版本、scope、implementation、test 或 release contract。

Deferred: Ticket Plan、implementation、exact Claude Code `2.1.251` compatibility fixture、live smoke、Completed `1.4.0` evidence，以及所有 external publication actions。

Handoff: 以下明示修正已套用，並交由 `$plan-tickets`；本摘要的核准不授權 implementation。

Approval: 使用者於 2026-09-04 在本修正摘要的完整精確內容展示後明確回覆「核准」；該核准只涵蓋本摘要明示的三項修正，不授權 implementation。

## Additions

- 在 Project Knowledge Base 的 `Approval` 追加使用者對本修正摘要精確內容的核准證據。
- 在 Project Knowledge Base 的 `Artifact links` 新增本修正摘要的 Approved link，讓後續讀者可追溯修正來源。

## Modifications

### Project Knowledge Base Glossary

- 將 **Operation-bound profile** 改為：`每次公開 Ask Then Do It command 開始時綁定的 profile；當前 operation 不因 model switch 混用 instructions。只有 PostModelSwitch commit 後的下一個 permitted public entry 保證依新 classification 路由；commit 前 race window 為 best effort。`

### Project Knowledge Base evidence provenance

- 在 Claude `1.4.0` Requirement decisions 的 evidence 說明後補充：`其中 bare-alias、PostModelSwitch race 與 reviewer execution-mode refinements 另以 Approved claude-code-adapter-1-4-0-spec 為 evidence。`

### Approved Specification Knowledge Base Change Summary input provenance

- 將 `Inputs` 中的 `目前 Approved Project Knowledge Base` 改為 `同步前的 Approved Project Knowledge Base`，明確保存真正的 pre-sync input，避免同步後看似循環引用。

## Removals

- 無。
