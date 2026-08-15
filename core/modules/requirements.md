# Requirement Interrogation

This module defines Full-mode requirement interrogation. Lite requirement questions are governed separately by the Lite workflow module.

## Purpose

Turn ambiguous intent into explicit, human-owned decisions before specification or implementation.

## Contract

- Use available read-only project evidence before asking for facts.
- Ask exactly one question per turn (`GRILL-ONE-001`).
- Include a concrete recommended answer and its principal consequence or tradeoff.
- Prioritize the unresolved decision with the highest impact and uncertainty.
- Trace decisions through goals, users, scope, non-goals, behavior, failures, data, dependencies, security, operations, and acceptance criteria.
- Make only low-impact, reversible assumptions and disclose them.
- Finish with a consolidated Requirement Decision Record and one explicit consensus question.
- Require explicit human consensus (`GATE-REQ-001`).
- Do not authorize production implementation from this module.

## Stop conditions

Stop and wait after every question. Finish only when high-impact items are confirmed, intentionally deferred with clear ownership, or proven irrelevant.

## Documented mode

When durable project context is in scope, compose this module with [Project Knowledge](project-knowledge.md). Preserve the one-question rule and all requirement gates while maintaining Draft Working Notes and proposing evidence-backed Project Knowledge Base changes.
