---
name: plan-tickets
description: Split an approved software specification into small, dependency-aware, vertically testable implementation tickets and manage the plan approval gate. Use when the user asks to plan an approved feature, create tickets from a spec, identify safe parallel work, or resume planning from an existing approved specification. Do not plan against an unapproved or contradictory spec.
---

# Plan Tickets

Create independently understandable slices that produce verifiable behavior instead of horizontal layers that remain untestable until the end.

<!-- Maintainer note: Vertical slices shorten the feedback loop and expose wrong foundational decisions before they infect the whole implementation. -->

Match user-facing communication and generated artifacts to the user's language when discoverable.

## Check prerequisites

- Require a relevant specification marked `Approved` and confirm it still matches the user's request.
- Read applicable repository instructions, architecture, tests, and current changes.
- Return to `$write-spec` when the plan would require new behavior or contradict the approved contract.
- Do not modify implementation code while planning.

## Choose the artifact

Follow the repository's existing planning convention. If none exists, use `docs/plans/<feature-name>.md`, matching the specification's feature name.

## Use the portable artifact envelope

Include or unambiguously convey `artifact_type` as Ticket Plan, a stable `artifact_id`, the Specification's `workflow_id`, `core_version` `1.0.0`, `status`, upstream `inputs`, `assumptions`, `deferred` decisions, the next-stage `handoff`, and `approval` evidence. Preserve these values when revising an existing artifact.

## Slice vertically

Make each ticket deliver a behavior that can be demonstrated or verified through a public boundary. Include necessary data, backend, frontend, migration, and test work in the same ticket when they jointly deliver that slice.

Avoid plans such as "build all database tables," then "build all APIs," then "build all screens." If a shared enabling change is unavoidable, keep it minimal, name its first consumer, and make its verification explicit.

## Define every ticket

Include:

- Outcome and approved acceptance criteria covered.
- In-scope and explicitly out-of-scope behavior.
- Dependencies and ordering constraints.
- Likely files or architectural areas, without prescribing speculative code.
- First failing test or other test-first verification approach.
- Focused and broader verification commands or signals.
- Completion criteria.
- Parallel safety: `Yes` or `No`, with a concrete reason and ownership boundary.

Keep tickets small enough for one agent to complete with the relevant context, but do not split a coherent behavior merely to make the list longer.

## Analyze parallel work

Mark tickets parallel-safe only when:

- Their shared contracts are already approved.
- They have no unresolved dependency between them.
- They will not modify the same files or core abstraction.
- Their test fixtures and migrations cannot conflict.
- Each result can be integrated and verified independently.

When any condition is uncertain, mark the tickets sequential.

## Run the plan gate

1. Save the plan with `Status: Draft` and link the approved specification.
2. Present the dependency order, vertical outcomes, and proposed parallel groups.
3. Ask the user to approve or revise the plan.
4. After explicit approval, set `Status: Approved`.

Do not invoke `$implement-tdd` before the plan is approved.
