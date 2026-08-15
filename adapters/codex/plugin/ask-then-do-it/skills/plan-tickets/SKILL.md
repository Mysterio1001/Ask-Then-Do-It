---
name: plan-tickets
description: Split an approved software specification into small, dependency-aware, vertically testable implementation tickets and manage the plan approval gate. Use when the user asks to plan an approved feature, create tickets from a spec, identify safe parallel work, or resume planning from an existing approved specification. Do not plan against an unapproved or contradictory spec.
---

# Plan Tickets

Create independently understandable slices that produce verifiable behavior and preserve the user's test-time choice.

<!-- Maintainer note: Vertical slices shorten the feedback loop and expose wrong foundational decisions before they infect the whole implementation. -->

Match user-facing communication and generated artifacts to the user's language when discoverable.

## Resolve the top-level mode before this stage

Direct selection of this Skill chooses this Full-workflow stage, not top-level `full`. Before any stage behavior, require `$ask-then-do-it` to have proven the current-operation mode; never persist or reuse mode.

- No proof: stop and delegate to `$ask-then-do-it`. The canonical resolver handles an explicit `lite` instruction and Config `lite`; conflicting explicit modes pause for clarification; invalid Config fails closed to Full; an absent source reaches Full fallback.
- Proven `lite`: stop this Full stage and route through `$ask-then-do-it` to the canonical Lite workflow.
- Proven `full`: continue subject to every existing prerequisite and gate.

## Check prerequisites

- Require a relevant specification marked `Approved` and confirm it still matches the user's request.
- Read applicable repository instructions, architecture, tests, and current changes.
- Return to `$write-spec` when the plan would require new behavior or contradict the approved contract.
- Do not modify implementation code while planning.

## Choose the artifact

Follow the repository's existing planning convention. If none exists, use `docs/plans/<feature-name>.md`, matching the specification's feature name.

## Use the portable artifact envelope

Include or unambiguously convey `artifact_type` as Ticket Plan, a stable `artifact_id`, the Specification's `workflow_id`, `core_version` `1.3.0`, `status`, upstream `inputs`, `assumptions`, `deferred` decisions, the next-stage `handoff`, and `approval` evidence. Preserve these values when revising an existing artifact.

## Slice vertically

Make each ticket deliver a behavior that can be demonstrated or verified through a public boundary. Include necessary data, backend, frontend, migration, and test work in the same ticket when they jointly deliver that slice.

Avoid plans such as "build all database tables," then "build all APIs," then "build all screens." If a shared enabling change is unavoidable, keep it minimal, name its first consumer, and make its verification explicit.

## Define every ticket

Include:

- Outcome and approved acceptance criteria covered.
- In-scope and explicitly out-of-scope behavior.
- Dependencies and ordering constraints.
- Likely files or architectural areas, without prescribing speculative code.
- A TDD approach with the first failing test, focused Green, and broader verification.
- A direct approach with permitted non-test validation and behavioral evidence that would remain unavailable.
- Completion criteria.
- Parallel safety: `Yes` or `No`, with a concrete reason and ownership boundary.

Keep tickets small enough for one agent to complete with the relevant context, but do not split a coherent behavior merely to make the list longer.

## Recommend tests and collect choices in one batch

- Present the complete Ticket definitions and all recommendations before requesting one batch test choice.
- Give every Ticket a risk-based test recommendation and a scope-specific reason. Use available evidence about correctness, regression, security, privacy, migration, integration, destructive behavior, and release risk; state when relevant evidence is unavailable.
- For every Ticket, warn that tests may increase work time and that skipping them lowers behavioral verification confidence.
- Ask in the user's language whether tests should be added, and collect all Ticket choices in a single response. Do not present `tdd` and `direct` as the initial user-facing options.
- Accept `Add tests to all Tickets`, `Do not add tests to all Tickets`, or an explicit mixed selection such as adding tests to named Tickets and declining them for the rest.
- Retain choices from an incomplete mixed selection and ask only about unresolved Tickets.
- There is no default. Do not infer an unresolved test choice from risk, repository conventions, another Ticket, prior history, or silence.
- For every resolved Ticket, map `Add tests` to internal mode `tdd` and map `Do not add tests` to internal mode `direct`.
- Display all plain-language test choices before requesting approval. Internal modes may also be shown for traceability, but the user must not need to understand them. A plan with any unresolved choice or missing mapped mode must remain `Draft`.

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
2. Present the complete Ticket definitions, dependency order, vertical outcomes, and proposed parallel groups.
3. Present every recommendation, then collect all plain-language test choices in one batch. Accept all-add, all-decline, or explicit mixed selection; ask only about unresolved Tickets when necessary.
4. Map each resolved choice to its internal mode, present the complete Ticket definitions and test choices, then ask the user to approve or revise the plan.
5. After explicit approval, set `Status: Approved` and preserve both the test choices and mapped modes.

Do not invoke `$implement-tdd` or `$implement-direct` before the plan is approved. Changing a test choice or mapped mode after approval returns the plan to `Draft` and requires reapproval before affected implementation continues.
