# Lite Workflow

## Purpose

Provide a lower-token, lower-traceability path for a single operation while retaining an approved scope, proportionate validation, honest risk disclosure, and user control over corrections.

Lite is a top-level workflow mode. It is not the Full Ticket implementation mode `direct`, and it MUST NOT fabricate Full artifacts or approval state.

## Entry and capability

- Enter only after orchestration resolves the current operation to `lite`.
- Inspect applicable repository instructions, current changes, and only the code, tests, configuration, documentation, or contracts reasonably related to the request.
- Preserve unrelated user changes and declare capability limitations before relying on unavailable actions or evidence.
- Stop when material behavior or scope cannot be represented honestly in Lite and recommend Full for the current operation.

## Reconnaissance and risk

Before Change Brief approval, evaluate available evidence for authentication or authorization, payments, data migration, destructive data operations, public contracts, cross-module structural change, concurrency or asynchronous behavior, and external side effects (`LITE-RISK-001`).

When material risk is present, explain the evidence and ask whether only the current operation should switch to Full. The user MAY remain in Lite, and either choice MUST NOT alter a persistent default.

If new material risk appears after approval or during implementation, the workflow MUST pause further modification and ask the same current-operation question again. Switching to Full preserves observable current changes and returns to the earliest unmet Full gate. Continuing Lite retains the accepted risk for completion reporting.

## Blocking questions

Ask only unresolved questions whose answers block or materially redirect implementation (`LITE-QUESTIONS-001`). Use repository evidence instead of asking for discoverable facts.

Each round MUST:

- contain no more than three blocking questions and no filler questions;
- rank questions by impact and uncertainty;
- target approximately 500 tokens for the complete batch;
- keep each question to at most three short sentences;
- ask one decision and include one concrete recommendation plus its principal tradeoff.

When more blockers exist, ask the highest-priority three and reassess the rest after the answers.

## Change Brief and approval

After blockers are resolved, display one conversation-only Change Brief containing the objective, in-scope behavior, explicit non-goals, three to five observable acceptance scenarios, material risks, and intended validation (`LITE-BRIEF-001`).

The Change Brief MUST target approximately 800 tokens. Material behavior, failure handling, risk, or validation MUST NOT be omitted to meet the target. If an honest brief cannot fit, recommend Full and ask whether to switch the current operation.

Lite has exactly one formal approval before implementation. Production modification MUST NOT begin until the user explicitly approves the complete Change Brief.

Lite MUST NOT create or update workflow artifacts, including a Requirement Decision Record, Draft Working Notes, Project Knowledge Base, Specification, Ticket Plan, Implementation Evidence, Direct Implementation Evidence, Review Report, or Architecture Improvement Report. Requested production code, configuration, content, and documentation remain valid outputs.

## Implementation boundary

- Implement only the approved Change Brief and stop when material new behavior or scope is required.
- MUST NOT create or modify behavioral test files for the operation.
- MUST NOT require or claim Red, Green, Refactor, TDD-complete, or TDD-equivalent evidence.
- MUST NOT perform speculative cleanup, unrelated refactoring, or broad generated-output replacement outside approved behavior and real delivery contracts.

## Minimum validation

When relevant and available, Lite MUST (`LITE-VALIDATE-001`):

1. inspect final repository status and diff for unintended files and scope drift;
2. run applicable existing syntax, lint, type-check, build, configuration, schema, or equivalent static checks;
3. execute an existing focused test or perform a manual smoke check for one principal success path;
4. execute an existing focused test or perform a manual smoke check for one most important failure or boundary path;
5. retain the observed outcomes needed for the completion report.

Lite MUST NOT run a complete behavioral suite by default solely because it exists. A real external delivery contract MAY require broader checks and MUST be obeyed and disclosed.

Correct implementation or environment problems within the approved Change Brief and rerun relevant checks before Review. Report an unavailable check and its risk. A known unresolved applicable validation failure MUST prevent an unqualified completion claim.

## Compact Review and correction authority

After validation, the implementing AI performs one compact, non-independent Review of Change Brief coverage, diff scope, principal failure and boundary paths, security-sensitive behavior, sensitive information, observed and unavailable validation, and residual risk (`LITE-REVIEW-001`). Lite does not require a separate reviewer, the fixed twelve-lens pass, or a Review artifact.

Collect all actionable in-scope findings and present them in one batch. The workflow MUST NOT fix a finding until the user explicitly approves the batch. After approval, fix only the approved findings and rerun relevant validation. Partial approval limits the fix subset. A fix requiring material scope expansion returns to the user instead of being treated as an in-scope correction.

If correction is declined, leave the finding unchanged and report its impact. Do not claim a clean Review or successful completion that hides an unresolved finding.

When Review finds no actionable findings, state that result and MUST NOT create an empty correction gate.

## Completion and session lifecycle

A normal completion report MUST target approximately 500 tokens and state delivered behavior, changed files or ownership areas, observed validation and outcomes, unavailable checks, unresolved findings, and residual risks (`LITE-SESSION-001`). Failures, blockers, security concerns, and missing evidence MAY exceed the target and MUST NOT be suppressed.

The conversation-only Change Brief, approval, progress, and Review are not durable cross-session state. A new session MUST resolve mode again from its current instruction and available defaults. It MAY reconstruct a new Change Brief from repository state and user input, but it MUST NOT claim to resume unpersisted Lite workflow state.
