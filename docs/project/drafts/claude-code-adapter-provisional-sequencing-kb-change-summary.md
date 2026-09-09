# Claude Code Adapter 1.4.0 Provisional Sequencing Knowledge Base Change Summary

Artifact type: Knowledge Base Change Summary

Artifact ID: `claude-code-adapter-1-4-0-provisional-sequencing-kb-change-summary`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Status: Approved

Inputs: 使用者於2026-09-07明確核准的sequencing correction、Approved Claude Code Adapter `1.4.0` Specification與Ticket Plan、Ticket 3 unverified ledger及其preflight／Review evidence。

Assumptions: Exact Claude Code `2.1.251` binary與strict validation已可用，但authenticated model session、兩個namespaced invocations、`additionalContext`、bare alias與failure semantics仍未觀察。Provisional implementation可能因後續host結果而返工。

Deferred: Ticket 2 implementation、General／Claude 5 profiles、Ticket 3 authenticated observations、Ticket 9 integration freeze、Ticket 10 local completion，以及所有external publication actions。

Handoff: 同步下列明示變更後，進入Approved Ticket 2的`tdd` implementation；不得把provisional／simulated evidence冒稱live verified，且Ticket 3未通過前不得進入Ticket 9 integration freeze或完成local `1.4.0`。

Approval: 使用者於2026-09-07在看到「Ticket 3保持未完成但改為local `1.4.0`完成前hard gate，現在先進入Ticket 2」，並被告知可能因exact-host差異返工後，明確回覆「核准」。本核准只涵蓋以下精確sequencing knowledge，不降低產品acceptance criteria，也不授權external publication。

## Additions

- 加入`provisional host evidence`規則：Ticket 3通過前，所有依賴exact host的command identity、hook、route與failure結果只可標為provisional／simulated。
- 加入reconciliation規則：Ticket 3若與provisional implementation不一致，返回最早受影響的Requirement／Specification／Ticket，並使dependent evidence失效後重驗。

## Modifications

- Foundation順序由`Ticket 1 → Ticket 3 → Ticket 2 → profiles`改為`Ticket 1 → Ticket 2 → profiles`的provisional implementation順序。
- Ticket 3由Ticket 2／profiles前置gate移為Ticket 9 integration freeze與local `1.4.0` completion前的hard gate。
- Current handoff由重跑Ticket 3改為進入Ticket 2 `tdd` implementation。

## Removals

- 移除「Ticket 3未通過前不得開始Ticket 2或profiles」的current planning rule。
- 不移除Ticket 3的任何驗收項目、最低版本要求、真實host evidence或release-blocking地位。
