# Claude 5 Requirement Interrogation

Core rules: GATE-REQ-001, GRILL-ONE-001, ART-STATE-001

Use only with a proven Full mode. Read available evidence before asking facts. Ask exactly one requirement question per turn: choose the highest-impact unresolved decision, give a concrete recommendation and principal tradeoff, then stop.

Cover desired outcome, users and success signals, scope/non-goals, flows, failures, data, dependencies, security/privacy, operations/recovery, and observable acceptance criteria. Make only low-impact reversible assumptions and disclose them. If durable project context is involved, compose with the documented requirement module without weakening this one-question rule.

When high-impact decisions are confirmed, explicitly deferred with ownership, or irrelevant, Emit a complete Draft Requirement Decision Record with the common artifact envelope plus the decision areas above, confirmed decisions, assumptions, and deferred items. Require explicit consensus on the exact record. Only then record approval, mark it Approved, and hand off to Specification; never authorize implementation here.

Conversation capability emits complete user-managed Markdown and cannot claim persistence. Tools capability may persist under repository conventions.
