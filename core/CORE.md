# Portable AI Development Workflow Core

Core version: `1.3.1`

This directory is the normative, host-neutral contract for an AI-assisted software development workflow. Adapter wording may vary, but mapped rule semantics must remain compatible with this core.

## Normative language

- `MUST` and `MUST NOT` define conformance requirements.
- `SHOULD` and `SHOULD NOT` define defaults that require a stated reason to override.
- `MAY` defines optional behavior.

## Modules

1. [Workflow orchestration](modules/orchestration.md)
2. [Lite workflow](modules/lite-workflow.md)
3. [Requirement interrogation](modules/requirements.md)
4. [Project knowledge](modules/project-knowledge.md)
5. [Specification](modules/specification.md)
6. [Ticket planning](modules/ticket-planning.md)
7. [Test-driven implementation](modules/tdd-implementation.md)
8. [Direct implementation](modules/direct-implementation.md)
9. [Evidence-based review](modules/review.md)
10. [Architecture improvement](modules/architecture-improvement.md)

## Shared contracts

- [Artifact envelope](artifacts/common.md)
- [Requirement Decision Record](artifacts/requirement-decision-record.md)
- [Project Knowledge Base](artifacts/project-knowledge-base.md)
- [Draft Working Notes](artifacts/draft-working-notes.md)
- [Specification artifact](artifacts/specification.md)
- [Ticket Plan](artifacts/ticket-plan.md)
- [Implementation Evidence](artifacts/implementation-evidence.md)
- [Direct Implementation Evidence](artifacts/direct-implementation-evidence.md)
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

## Top-level workflow modes

- `full`: the assurance-oriented workflow that preserves every existing requirement, Specification, Ticket Plan, implementation, Review, evidence, and architecture gate.
- `lite`: the lower-traceability workflow defined by the Lite module. It uses one conversation-only Change Brief approval and does not create workflow artifacts for the operation.

Top-level workflow mode is separate from the Full Ticket implementation modes `tdd` and `direct`.
