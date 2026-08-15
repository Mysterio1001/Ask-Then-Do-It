# Lite Workflow

Use this reference only after the orchestrator resolves the current operation to `lite`. Lite reduces workflow text and durable traceability; it does not promise lower API billing or TDD-equivalent assurance.

## Contents

- Reconnaissance and boundaries
- Material-risk reconsideration
- Blocking questions
- Change Brief approval
- Scoped implementation
- Proportionate validation
- Compact Review
- Completion and new-session behavior

## Inspect the relevant scope

Read applicable repository instructions, inspect current repository changes, and inspect only the code, tests, configuration, documentation, and contracts reasonably related to the request. Use repository evidence instead of asking for discoverable facts, preserve unrelated user changes, and state capability or evidence limits before relying on unavailable actions.

Stop and return to the user when implementation would require materially new behavior or scope. When the operation cannot be represented honestly within the Lite budgets or assurance level, recommend Full for only the current operation.

## Reconsider material risk

Evaluate available evidence before Change Brief approval and again during implementation for material authentication, authorization, payment, data migration, destructive data operation, public contract, cross-module structural, concurrency, asynchronous, or external side effect risk.

When material risk exists, explain the specific evidence and ask whether only the current operation should switch to Full or continue in Lite with the risk accepted. The user may remain in Lite. If no mode answer is received, remain paused.

If new evidence appears after approval or during implementation, pause further modification and ask the same current-operation question again. The decision MUST NOT persist or modify Config.

Switching to Full preserves observable current changes and returns to the earliest unmet Full gate before more implementation. Continuing in Lite retains the accepted risk for the completion report.

## Ask blocking questions

Ask only unresolved questions whose answers block or materially redirect implementation. Use repository evidence before asking the user.

For each round:

- ask no more than three questions and omit filler when fewer blockers exist;
- rank questions by impact and uncertainty;
- target approximately 500 tokens for the complete batch;
- keep each question to at most three short sentences;
- ask one decision per question; and
- include one concrete recommendation and its principal tradeoff or consequence.

When more than three blockers remain, ask the highest-priority three and reassess the rest after the answers. Do not repeat a question made irrelevant by an earlier answer.

## Approve the Change Brief

After blockers are resolved, present one conversation-only Change Brief containing:

- the objective;
- in-scope behavior;
- explicit non-goals;
- three to five observable acceptance scenarios;
- material risks; and
- intended validation.

Target approximately 800 tokens. Do not omit material behavior, failure handling, risk, or validation to fit the budget. If an honest brief cannot fit, recommend Full and ask whether only the current operation should switch.

Lite has exactly one formal pre-implementation approval. Do not begin production modification until the user explicitly approves the complete Change Brief.

For this Lite operation, the workflow MUST NOT create or update a Requirement Decision Record, Draft Working Notes, Project Knowledge Base, Specification, Ticket Plan, Implementation Evidence, Direct Implementation Evidence, Review Report, or Architecture Improvement Report. User-requested production code, configuration, content, and documentation remain valid implementation outputs.

## Implement within scope

Implement only the approved Change Brief. Stop when materially new behavior or scope is required.

- MUST NOT create or modify unit, integration, end-to-end, or equivalent behavioral test files.
- MUST NOT require or report Red, Green, Refactor, TDD-complete, or TDD-equivalent evidence.
- Do not perform speculative cleanup, unrelated refactoring, or broad generated-output replacement outside the approved behavior and real delivery contracts.
- Re-run material-risk evaluation whenever implementation reveals new evidence.

## Validate proportionately

When relevant and available:

1. Inspect final repository status and diff for unintended files and scope drift.
2. Run applicable existing syntax, lint, type-check, build, configuration, schema, or equivalent static checks.
3. Execute an existing focused test or perform a manual smoke check for one principal success path.
4. Execute an existing focused test or perform a manual smoke check for one most important failure or boundary path.
5. Retain the observed outcomes for Review and completion.

Do not run a complete behavioral suite by default solely because it exists. Obey and disclose a real external CI, repository, hosting, or release contract that requires broader checks.

Correct an implementation or in-scope environment problem within the approved Change Brief and rerun the relevant check before Review. Report unavailable validation and its risk. A known unresolved applicable failure prevents an unqualified completion claim.

## Run compact Review

After validation, the same implementing AI performs one compact, non-independent Review. Do not require a separate reviewer context, the Full fixed twelve-lens pass, or a Review artifact.

Review Change Brief coverage, diff and file scope, principal failure and boundary paths, security-sensitive behavior and sensitive information, observed and unavailable validation, and residual risk.

Present all actionable in-scope findings in one batch and stop. Do not edit a finding until the user explicitly approves the batch. After approval, fix only the approved subset and rerun relevant validation. A correction requiring material scope expansion returns to the user instead of being treated as in-scope.

If the user declines any correction, leave it unchanged and report the unresolved finding and impact. Do not hide it behind a clean Review or successful-completion claim.

When Review finds no actionable findings, state that result and MUST NOT create an empty correction gate.

## Complete and start new sessions

A normal successful completion response targets approximately 500 tokens and states delivered behavior, changed files or ownership areas, observed validation and outcomes, unavailable checks, unresolved findings, and residual risks. Avoid implementation narration and do not repeat the complete Change Brief.

Failures, blockers, security concerns, missing evidence, and unresolved risk may exceed the target and must not be suppressed.

The conversation-only Change Brief, approval, progress, and Review are not durable cross-session state. A new session must resolve mode again from its current-operation instruction and current Config precedence. It may reconstruct a new Change Brief from repository state and user input, but MUST NOT claim to resume unpersisted Lite state.
