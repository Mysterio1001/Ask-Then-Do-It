# Ask Then Do It 1.4.0 Claude Code Adapter Planning Knowledge Base Change Summary

Artifact type: Knowledge Base Change Summary

Artifact ID: `claude-code-adapter-1-4-0-planning-kb-change-summary`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Status: Approved

Inputs: Approved [Claude Code Adapter 1.4.0 Ticket Plan](../../plans/claude-code-adapter-1.4.0.md)、Approved [Specification](../../specs/claude-code-adapter-1.4.0.md)、同步前的 Approved [Project Knowledge Base](../knowledge-base.md)，以及使用者於2026-09-05對十張Ticket全部Add tests／`tdd`的選擇與Plan核准。

Assumptions: 本摘要只同步已核准Ticket Plan的索引、test-mode與handoff狀態；不宣稱任何Ticket implementation、exact Claude Code `2.1.251` host validation、live smoke、local `1.4.0` candidate或external publication已開始或完成。

Deferred: Tickets 1–10 implementation、逐Ticket evidence與Reviews、release architecture diagnosis、Completed `1.4.0` release evidence，以及全部external publication actions。

Handoff: 以下明示變更已同步至Project Knowledge Base，並從Approved Ticket 1的`tdd`模式交由`$implement-tdd`；本摘要的核准不授權external publication。

Approval: 使用者於2026-09-05在本Planning Knowledge Base Change Summary的完整精確內容展示後明確回覆「核准」；該核准只涵蓋本摘要明示的Project Knowledge Base changes，不授權external publication。

## Additions

- 在Project Knowledge Base的`Inputs`加入Approved `claude-code-adapter-1-4-0-plan`。
- 在`Important decisions`新增：十張Tickets全部由使用者選擇Add tests並映射為`tdd`；穩定Ticket ID的實際foundation順序是Ticket 1 → Ticket 3 exact-host preflight → Ticket 2 production router，之後才進profiles。
- 在`Artifact links`新增本Planning Knowledge Base Change Summary；只在本摘要Approved後以Approved標籤與link加入，讓核准與同步來源可追溯。

## Modifications

- 從Project Knowledge Base的`Deferred`移除已完成的`1.4.0 Ticket Plan`，保留implementation、evidence與external publication。
- 將`Handoff`從`$plan-tickets`改為：依Approved Ticket Plan從Ticket 1的`tdd`模式交由`$implement-tdd`；每張Ticket完成後交由獨立`$review-code`，且Ticket 3的exact `2.1.251` hard gate未通過前不得進入profiles。
- 在`Approval`追加：使用者於2026-09-05核准完整Plan與全部`tdd` mapping；同日，使用者在本Planning Knowledge Base Change Summary的完整精確內容展示後明確回覆「核准」，核准本次planning knowledge同步。
- 將`Artifact links`中的`1.4.0 Ticket Plan: pending Ticket Planning and approval`改為Approved [Claude Code Adapter 1.4.0 Ticket Plan](../../plans/claude-code-adapter-1.4.0.md)；正式Project Knowledge Base中的相對target使用`../plans/claude-code-adapter-1.4.0.md`。

## Removals

- 除`Deferred`中已完成的Ticket Plan項目與過時的pending link外，不移除任何正式knowledge。
