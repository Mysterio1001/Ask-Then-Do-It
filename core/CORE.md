# Portable AI Development Workflow Core

Core version: `3.0.0`

This directory is the normative, host-neutral contract for an AI-assisted software development workflow. Adapter wording may vary, but mapped rule semantics must remain compatible with this core.

## Normative language

- `MUST` and `MUST NOT` define conformance requirements.
- `SHOULD` and `SHOULD NOT` define defaults that require a stated reason to override.
- `MAY` defines optional behavior.

## Modules

1. [Workflow orchestration](modules/orchestration.md)
2. [Requirement interrogation](modules/requirements.md)
3. [Project knowledge](modules/project-knowledge.md)
4. [Specification](modules/specification.md)
5. [Ticket planning](modules/ticket-planning.md)
6. [Test-driven implementation](modules/tdd-implementation.md)
7. [Evidence-based review](modules/review.md)
8. [Architecture improvement](modules/architecture-improvement.md)

## Shared contracts

- [Artifact envelope](artifacts/common.md)
- [Requirement Decision Record](artifacts/requirement-decision-record.md)
- [Project Knowledge Base](artifacts/project-knowledge-base.md)
- [Draft Working Notes](artifacts/draft-working-notes.md)
- [Specification artifact](artifacts/specification.md)
- [Ticket Plan](artifacts/ticket-plan.md)
- [Implementation Evidence](artifacts/implementation-evidence.md)
- [Review Report](artifacts/review-report.md)
- [Architecture Improvement Report](artifacts/architecture-improvement-report.md)
- [Adapter manifest contract](adapters/manifest-contract.md)
- [Mandatory rule catalog](rules/rules.yaml)
- [Architecture and Refactoring Lenses](references/architecture-refactoring-lenses.md)

## Capability profiles

Adapters MUST declare cumulative capability profiles before selecting stages:

- `conversation`: exchange text and emit user-managed artifacts.
- `tools`: inspect and modify a repository, persist artifacts, and execute commands.
- `multi_agent`: create isolated worker or reviewer contexts in addition to tool capabilities.

Unknown capability is not evidence. Default to `conversation` until stronger capabilities are demonstrated.
