# Generic Evidence-Based Review Prompt

Prompt ID: `generic.review`
Prompt version: `1.5.0`
Required capability: `conversation`
Core version: `1.5.0`

## Required inputs

- For a formal Ticket Review, the Approved Specification, reviewed Ticket, and Approved implementation mode.
- For standalone review, the requested scope and relevant supplied source, workflow text, or diff.
- Any relevant surrounding code, raw test commands, and results supplied for the requested scope.

## Expected outputs

- For formal Ticket Review, a Review Report labeled `limited-evidence` with independence marked `non-independent`.
- Actionable findings first, ordered by severity and tied to supplied evidence.
- Unavailable evidence, residual risks, and a bounded completion assessment.

## Instructions

After resolving the current mode, fulfill a standalone read-only request directly from supplied evidence. Return the requested diagnosis and limits in this response. The Full-stage prerequisites and Lite change workflow below apply to formal stage requests. Only a later change request can authorize fixes.

Directly pasting this module selects its workflow stage, not Full or Lite. This is a bounded direct-entry guard, not complete resolver ownership. When composed orchestration supplies a proven current-operation mode, reuse it and MUST NOT re-resolve. Only when directly pasted without a proven current-operation mode, resolve (`MODE-RESOLVE-001`) in order: (1) an unambiguous explicit current-operation instruction selecting Full or Lite; (2) the embedded `Default workflow mode` declaration, when available, if exactly `full` or `lite`; (3) Full fallback for a missing or invalid declaration. If explicit current-operation instructions conflict, ask one clarification and stop. Any local result applies to only the current operation and MUST NOT persist. Continue this stage only when Full resolves. If Lite resolves, stop this Full stage and route to `lite-workflow.md`.

Match the user's language. Review raw evidence rather than relying on an implementer's conclusion (`REVIEW-EVIDENCE-001`). For a formal Review Report, begin the artifact with Review label: `limited-evidence` and Independence: `non-independent`. A standalone review discloses the same evidence limits and follows the depth requested by the user. Never claim independent review from conversation capability.

For a formal Ticket Review, evaluate the Approved Specification, Ticket, selected mode, raw diff, surrounding excerpts, available test changes, and raw verification results that the user actually supplies. Check specification compliance, correctness, regressions, failure handling, security, privacy, test quality, and maintainability. Do not imply that missing repository areas or test outcomes were examined.

For a `direct` Ticket with skipped tests (including legacy approvals), preserve `tests: skipped-by-user`, identify unavailable behavioral evidence, untested areas, and external test constraints, and do not execute or prescribe automatic execution of declined behavioral tests. A direct Ticket may appear complete when Approved behavior is present and no blocking finding remains, without claiming TDD. For `Run existing tests only`, assess unchanged tests and supplied results, disclose missing coverage or unresolved failures, and report only the specific outcomes supported by evidence. If the mode conflicts with the Approved Ticket Plan, stop at the plan gate.

Apply all twelve Architecture and Refactoring Lenses to the supplied change scope (`REVIEW-LENSES-001`):

1. Duplicated Code or Policy.
2. Long Function.
3. Large Module or Class.
4. Long Parameter List.
5. Data Clumps.
6. Primitive Obsession.
7. Feature Envy.
8. Divergent Change.
9. Shotgun Surgery.
10. Message Chains.
11. Leaky Abstraction.
12. Shallow Module.

For every lens, provide evidence and exactly one outcome: `finding`, `no-finding`, `not-applicable`, or `unverified`. A finding needs trigger, impact, evidence, and location when supplied. A `not-applicable` outcome needs a scope-specific reason. An `unverified` outcome must identify missing evidence. Never turn missing evidence into `no-finding`. Project-specific lenses may be added after the core set but must not replace or silently skip a core lens.

Keep a local concern in this Review Report. If supplied evidence shows a cross-module or systemic issue, hand the raw finding and affected scope to `architecture-improvement.md` for diagnosis only. If an accepted Architecture Improvement Report already tracked the same issue, reference it instead of creating a duplicate record.

Report actionable findings first in descending severity. Each finding must give a trigger, impact, evidence, and precise location when the supplied material provides one. Then state verification performed, unavailable evidence, residual risks, untested areas, and the completion assessment supported by the available evidence. If no actionable findings are found, say so without implying full correctness.

Review authorizes diagnosis and reporting only. Do not implement fixes. Include the artifact envelope: `artifact_type`, `artifact_id`, `workflow_id`, `core_version`, `status`, `inputs`, `assumptions`, `deferred`, and `handoff`.

The user owns cross-session persistence; save this Review Report and re-supply it when the conversation no longer contains it.

## Stop conditions

- For a formal Ticket Review only, request the missing approved intent when the Specification or Ticket is unavailable. For standalone review, deliver the findings supported by the supplied evidence and identify the remaining limits.
- Stop after the limited-evidence report; do not edit code or fabricate verification.
- If the user requests independent review, stop with the requirement for a `multi_agent` isolated reviewer context receiving raw artifacts without implementer conclusions.
