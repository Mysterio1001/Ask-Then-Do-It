# Claude Code General profile Lite workflow

This General profile module applies only after orchestration has proven `lite` for the current operation. Lite is not Full `direct` mode and creates no Full workflow artifacts.

Core rules: LITE-QUESTIONS-001, LITE-BRIEF-001, LITE-RISK-001, LITE-VALIDATE-001, LITE-REVIEW-001, LITE-SESSION-001

## Read-only requests and small edits

For a standalone read-only review or diagnosis, inspect the requested evidence and return findings, examples, and limitations in the same response. Skip implementation planning, Change Brief approval, and file writes. Ask only for genuinely missing inputs. Keep the requested review depth and independence; a formal Ticket Review still follows its evidence contract. A later request to fix findings is a new change request.

After checking the target and risk, use the original instruction as authorization for one exact, local, reversible edit, such as replacing a named button label or correcting a specified internal default. Its target and expected result must be unambiguous and directly verifiable. New features, unresolved decisions, material risk, public contract changes, and external effects use the standard flow. With tools, apply only that edit without a Change Brief or repeat approval, inspect the diff, verify the result, and report it. With conversation capability, provide the proposed edit and validation instructions only. Honor an explicit request for a preview or approval first. If the target, scope, or risk fails these conditions, follow the standard Lite flow below.

The remaining sections describe the standard Lite change flow.

## Reconnaissance, questions, and risk

Inspect only evidence available to the declared capability. Preserve unrelated changes. Before or during implementation, pause on material risk involving authentication/authorization, payments, migrations, destructive data actions, public contracts, cross-module structure, concurrency, or external side effects. Explain the evidence and ask whether to switch to Full for the current operation only; the user may choose to remain in Lite. Never persist that choice.

Ask only blocking questions. Each round contains no more than three questions, ranks them by impact and uncertainty, targets about 500 tokens total, and keeps each question within three short sentences. Each asks one decision and includes one concrete recommendation with its main tradeoff. Use repository evidence instead of asking discoverable facts.

[CORE: LITE-RISK-001]
[CORE: LITE-QUESTIONS-001]
[SCENARIO: LITE-RISK]
[SCENARIO: LITE-QUESTIONS]

## One Change Brief gate

When blockers are resolved, present one conversation-only Change Brief with objective, in-scope behavior, non-goals, three to five observable scenarios, material risks, and intended validation. Target about 800 tokens without omitting material behavior or failure handling. Lite has exactly one formal approval before implementation.

The workflow must not create or update workflow artifacts: no Requirement Decision Record, Draft Working Notes, Project Knowledge Base, Specification, Ticket Plan, Implementation Evidence, Review Report, or Architecture Improvement Report. Production changes start only after explicit approval of the entire brief.

[CORE: LITE-BRIEF-001]
[SCENARIO: LITE-BRIEF]

## Implementation and validation

Implement only the approved brief. Lite must not create or modify behavioral tests, execute new behavioral tests for the operation, or claim Red/Green/Refactor or TDD-equivalent evidence. Stop if material new scope appears.

When relevant and available, inspect the final diff/status; run existing static, syntax, lint, type, build, or schema checks; exercise one principal success path and one important failure or boundary path using an existing check or manual smoke; and retain raw outcomes. Report unavailable evidence and unresolved failure honestly. Do not run a complete behavioral suite by default unless an external delivery contract requires it.

[CORE: LITE-VALIDATE-001]
[SCENARIO: LITE-VALIDATION]

## Compact Review and completion

Perform one compact same-context Review covering brief scope, diff, failure boundaries, security, secrets, observed/unavailable checks, and residual risk. Collect the complete findings batch and do not fix it until the user explicitly approves it. Approved corrections stay within scope and rerun relevant validation. When no finding exists, state that without inventing an empty approval gate. The Plugin reviewer must not upgrade Lite to an independent Full Review.

The completion report targets about 500 tokens and states delivery, changed areas, observed validation, unavailable checks, unresolved findings, and risks. Lite conversation state is not durable across sessions. A new session must resolve mode again and may reconstruct a new brief, but cannot claim to resume unpersisted Lite state.

[CORE: LITE-REVIEW-001]
[CORE: LITE-SESSION-001]
[SCENARIO: LITE-REVIEW]
[SCENARIO: LITE-SESSION]
