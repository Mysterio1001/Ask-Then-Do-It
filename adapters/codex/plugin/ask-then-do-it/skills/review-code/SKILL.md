---
name: review-code
description: Independently review software changes against approved requirements, specifications, tickets, tests, and repository conventions, with actionable findings prioritized by severity. Use for current diffs, completed tickets, pull requests, explicit code-review requests, or the final review stage of the AI development workflow. A review request authorizes diagnosis and reporting, not implementation of fixes.
---

# Review Code

Review from evidence rather than the implementer's narrative. Optimize for defects the author would act on, not for commentary volume.

<!-- Maintainer note: Withholding the implementer's conclusions reduces anchoring and preserves the value of an independent pass. -->

Match user-facing communication and generated artifacts to the user's language when discoverable.

## Resolve the top-level mode before this stage

Direct selection of this Skill chooses this Full-workflow stage, not top-level `full`. Before stage behavior, require a current-operation mode proof from `$ask-then-do-it`; never persist or reuse mode.

- Missing proof: stop and delegate to `$ask-then-do-it`.
- Proven `lite`: stop this Full stage and route to the Lite workflow.
- Proven `full`: continue with this stage's prerequisites and gates.

## Create an independent view

When the runtime permits, delegate the review to a fresh subagent that did not implement the change. Provide only:

- Applicable repository instructions.
- Approved specification and ticket.
- Final diff and relevant surrounding code.
- Test changes and raw verification results.

Do not provide the implementer's defenses, expected findings, or a proposed verdict. Ask the reviewer to inspect the artifacts as a normal review task. If independent execution is unavailable, deliberately rebuild context from the same raw artifacts before reviewing.

## Label evidence and independence

Choose and state the Review label before findings:

- Use `independent` only when a fresh reviewer context did not implement the change and was not anchored by implementer conclusions.
- Use `non-independent` when the same context implemented the change or isolation cannot be demonstrated.
- Use `limited-evidence` when only user-supplied excerpts or incomplete raw artifacts are available; also state whether the reviewer context is independent.

Never use a stronger label than the available evidence and runtime isolation can prove.

## Preserve the implementation mode

- Read and retain the Ticket's Approved `tdd` or `direct` mode.
- For a `direct` Ticket, retain `tests: skipped-by-user`, identify unavailable behavioral evidence, untested areas, and external test constraints. Do not execute or prescribe automatic execution of declined behavioral tests.
- A `direct` Ticket may appear complete when approved behavior is present and no blocking finding remains, but never describe it as passing tests or TDD-complete.
- If the supplied mode conflicts with the Approved Ticket Plan, stop at the plan gate rather than choosing a route.

## Review in priority order

1. Verify every changed behavior against the approved specification and acceptance criteria.
2. Trace correctness, state transitions, failure paths, compatibility, and regressions.
3. Examine trust boundaries, authorization, validation, secrets, privacy, and destructive behavior.
4. Evaluate whether available tests would fail for likely defects and identify important untested paths without running tests declined by an Approved `direct` mode.
5. Apply all twelve Architecture and Refactoring Lenses to the changed code and its relevant impact area (`REVIEW-LENSES-001`). Read the [canonical architecture and refactoring lens contract](../ask-then-do-it/references/architecture-refactoring-lenses.md) completely immediately before the lens pass. If it is missing or unreadable, stop and do not claim a completed twelve-lens pass.

Ignore purely stylistic preferences unless they create a material maintenance, correctness, or repository-convention problem.

## Apply the twelve lenses

After reading the canonical contract, apply every lens in its fixed order. Record exactly one contract outcome per lens with evidence, while keeping this Review focused on the changed code and relevant impact area; do not imply a system-wide architecture diagnosis. Project-specific lenses may follow but must not replace, rename incompatibly, or silently skip a core lens. Preserve this stage's change-focused scope, independence labels, severity, finding validation, and systemic handoff.

For any `finding`, include its trigger, impact, evidence, and tightest location when available. Treat missing evidence as missing evidence, not as `no-finding`.

## Route systemic findings

Keep a local concern in this Review Report. When evidence shows a cross-module or systemic issue, hand the raw finding and affected scope to `$improve-architecture` for diagnosis only. If an accepted Architecture Improvement Report already tracked the same issue, reference it instead of creating a duplicate record.

## Validate each finding

For every proposed finding:

- Confirm it is introduced or exposed by the reviewed change.
- Identify the concrete input, state, or sequence that triggers it.
- Check surrounding code for an existing guard or invariant.
- State the user or system impact.
- Point to the tightest relevant file and line location.
- Assign severity: `P0` catastrophic, `P1` urgent, `P2` normal, or `P3` minor.

Each finding must state its trigger, impact, and evidence; do not report a concern without those three anchors.

Do not report speculation as fact. State uncertainty and the missing evidence when verification is impossible.

## Use the portable artifact contract

Before creating or emitting a Review Report, read the [portable artifact contract](../ask-then-do-it/references/artifact-contract.md) completely. If it is missing or unreadable, stop before artifact creation and leave the handoff pending.

## Report findings first

List actionable findings in descending severity. Use a short title followed by one concise paragraph explaining trigger, impact, and remediation direction. Keep locations precise.

After findings, state:

- Verification performed and evidence unavailable.
- Residual risks and untested areas.
- Whether the approved ticket appears complete.

If no actionable findings exist, say so explicitly and still identify residual risks or verification gaps. Do not modify code unless the user separately asks for fixes.

Emit a Review Report using the portable artifact contract for the common envelope. Preserve the stated Review label, evidence unavailable, residual risks, untested areas, and completion assessment in the artifact.
