---
name: review-code
description: Independently review software changes against approved requirements, specifications, tickets, tests, and repository conventions, with actionable findings prioritized by severity. Use for current diffs, completed tickets, pull requests, explicit code-review requests, or the final review stage of the AI development workflow. A review request authorizes diagnosis and reporting, not implementation of fixes.
---

# Review Code

Review from evidence rather than the implementer's narrative. Optimize for defects the author would act on, not for commentary volume.

<!-- Maintainer note: Withholding the implementer's conclusions reduces anchoring and preserves the value of an independent pass. -->

Match user-facing communication and generated artifacts to the user's language when discoverable.

## Resolve the top-level mode before this stage

Direct selection of this Skill chooses this Full-workflow stage, not top-level `full`. Before any stage behavior, require `$ask-then-do-it` to have proven the current-operation mode; never persist or reuse mode.

- No proof: stop and delegate to `$ask-then-do-it`. The canonical resolver handles an explicit `lite` instruction and Config `lite`; conflicting explicit modes pause for clarification; invalid Config fails closed to Full; an absent source reaches Full fallback.
- Proven `lite`: stop this Full stage and route through `$ask-then-do-it` to the canonical Lite workflow.
- Proven `full`: continue subject to every existing prerequisite and gate.

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
5. Apply all twelve Architecture and Refactoring Lenses to the changed code and its relevant impact area (`REVIEW-LENSES-001`).

Ignore purely stylistic preferences unless they create a material maintenance, correctness, or repository-convention problem.

## Apply the twelve lenses

Use this fixed core order:

1. **Duplicated Code or Policy**: equivalent behavior or rules maintained in multiple places.
2. **Long Function**: size or mixed responsibilities obstruct understanding, testing, or change.
3. **Large Module or Class**: one unit owns too many responsibilities or reasons to change.
4. **Long Parameter List**: an interface exposes unstable coordination or missing concepts.
5. **Data Clumps**: related values repeatedly travel together without a coherent abstraction.
6. **Primitive Obsession**: domain meaning relies on unconstrained primitive values.
7. **Feature Envy**: behavior depends more on another unit's data or responsibilities than its own.
8. **Divergent Change**: one unit changes repeatedly for unrelated reasons.
9. **Shotgun Surgery**: one behavior change requires edits across many locations.
10. **Message Chains**: navigation or call chains expose internal structure and amplify coupling.
11. **Leaky Abstraction**: callers must understand or compensate for hidden implementation details.
12. **Shallow Module**: interface complexity is not justified by the functionality it hides.

For every lens, record evidence and exactly one outcome: `finding`, `no-finding`, `not-applicable`, or `unverified`. A finding must include trigger, impact, evidence, and location when available. A `not-applicable` result needs a scope-specific reason. An `unverified` result must identify missing evidence. Never turn missing evidence into `no-finding`.

Project-specific lenses may follow the core set but must not replace, rename incompatibly, or silently skip a core lens. This pass remains focused on the change; do not imply a system-wide architecture diagnosis.

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

Do not report speculation as fact. State uncertainty and the missing evidence when verification is impossible.

## Report findings first

List actionable findings in descending severity. Use a short title followed by one concise paragraph explaining trigger, impact, and remediation direction. Keep locations precise.

After findings, state:

- Verification performed and evidence unavailable.
- Residual risks and untested areas.
- Whether the approved ticket appears complete.

If no actionable findings exist, say so explicitly and still identify residual risks or verification gaps. Do not modify code unless the user separately asks for fixes.

Emit a Review Report that includes or unambiguously conveys `artifact_type`, stable `artifact_id`, shared `workflow_id`, `core_version` `1.3.1`, review `status`, reviewed `inputs`, `assumptions`, `deferred` checks, and the next `handoff`. Preserve the stated Review label, evidence unavailable, residual risks, untested areas, and completion assessment in the artifact.
