# Ask Then Do It 1.4.0 Claude Marketplace Description Knowledge Base Change Summary

Artifact type: Knowledge Base Change Summary

Artifact ID: `claude-code-adapter-1-4-0-marketplace-description-kb-change-summary`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Status: Approved

Inputs: Approved [Claude Code Adapter 1.4.0 Requirement Decision Record](../../requirements/claude-code-adapter-1.4.0.md)、Draft-corrected [Claude Code Adapter 1.4.0 Specification](../../specs/claude-code-adapter-1.4.0.md)、Approved [Project Knowledge Base](../knowledge-base.md)，以及 2026-09-06 [exact Claude Code 2.1.251 native preflight blocker evidence](../../evidence/claude-code-adapter-1.4.0-ticket-3-preflight-blocker.md)。

Assumptions: 本修正只讓既有 repository Marketplace 滿足已核准的 strict-zero-warning需求；不改變Marketplace identity、source、Plugin行為、最低版本、Ticket切分或test choice。

Deferred: Ticket 1 correction implementation與Review、Ticket 3剩餘exact-host observations、Ticket 2 router、profiles、packages、live smoke及全部external publication actions。

Handoff: 下列明示Knowledge Base變更已同步；回Ticket 1執行TDD correction與fresh independent Review，再從頭重跑Ticket 3。

Approval: 使用者於2026-09-06在Draft Specification correction、最小修正內容、本摘要完整內容與preflight blocker evidence展示後明確回覆「核准」；該核准只涵蓋本摘要明示變更，不授權external publication。

## Additions

- 在Project Knowledge Base的Repository marketplace說明補充：Claude catalog authored top-level fields恰為`name`、`description`、`owner`、`plugins`；top-level `description`與唯一Plugin entry的approved independent-project description完全一致。這項要求由exact Claude Code `2.1.251` strict validation證明，且不得以忽略warning取代。
- 在Project Knowledge Base的Artifact links新增本Approved correction summary與Ticket 3 preflight blocker evidence，保存外部contract差異的來源。

## Modifications

- 將Claude Adapter handoff由「Ticket 1 → Ticket 3」更新為：Ticket 3已正確fail fast；須先核准Specification correction、回Ticket 1修正與重新Review，再從頭重跑Ticket 3。

## Removals

- 無。
