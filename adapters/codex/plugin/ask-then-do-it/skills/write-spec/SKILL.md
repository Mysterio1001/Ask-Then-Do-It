---
name: write-spec
description: Convert confirmed software decisions into a durable, implementation-independent behavioral specification and manage its approval gate. Use after requirement consensus, when the user asks to document agreed behavior, or when an existing spec must be revised because requirements changed. Do not invent missing product decisions or begin implementation.
---

# Write Spec

Preserve agreed intent in a document that remains useful after code changes and across AI sessions.

<!-- Maintainer note: Excluding production code keeps the specification stable when implementation details evolve. -->

Match user-facing communication and generated artifacts to the user's language when discoverable.

## Resolve the top-level mode before this stage

Direct selection of this Skill chooses this Full-workflow stage, not top-level `full`. Before stage behavior, require a current-operation mode proof from `$ask-then-do-it`; never persist or reuse mode.

- Missing proof: stop and delegate to `$ask-then-do-it`.
- Proven `lite`: stop this Full stage and route to the Lite workflow.
- Proven `full`: continue with this stage's prerequisites and gates.

## Check prerequisites

- Require explicit requirement consensus or an existing approved source of truth.
- Compare the decision summary with repository evidence and call out contradictions.
- If a material decision is missing, return to `$ask-requirements` and ask only the blocking question.
- Do not infer approval from the request to draft a specification.

## Choose the artifact

Follow the repository's existing documentation convention. If none exists, use `docs/specs/<feature-name>.md` with a short lowercase hyphenated feature name. Update the relevant existing spec instead of creating a duplicate.

## Use the portable artifact contract

Before creating or emitting a Specification, read the [portable artifact contract](../ask-then-do-it/references/artifact-contract.md) completely. Use it for the common envelope, `approval` evidence, and status transition; preserve those values when revising an existing artifact. If it is missing or unreadable, stop before artifact creation and leave the handoff pending.

## Write the behavioral contract

Use this structure when the repository has no stronger template:

```markdown
# <Feature> Specification

Status: Draft

## Problem
## Goals
## Non-goals
## Users and scenarios
## Required behavior
## Edge cases and failure behavior
## Data, permissions, and external contracts
## Compatibility, rollout, and recovery
## Constraints and assumptions
## Acceptance criteria
## Deferred decisions
```

Write acceptance criteria as observable, testable outcomes. Record data lifecycle, permissions, compatibility, and failure behavior when relevant. Preserve traceability from each accepted decision to at least one behavior, constraint, or acceptance criterion.

Do not include production implementation code, proposed patches, or code blocks that prescribe internal structure. Mention a technology, interface, or file only when it is an approved constraint or an existing external contract.

## Run the specification gate

1. Save the document with `Status: Draft`.
2. Summarize the behavior, boundaries, and consequential assumptions.
3. Ask the user to approve or revise the specification.
4. If revised, update the document and request approval again.
5. After explicit approval, change the status to `Approved` and record the approval date if the repository convention supports it.

Do not call `$plan-tickets` while the specification remains draft or disputed.
