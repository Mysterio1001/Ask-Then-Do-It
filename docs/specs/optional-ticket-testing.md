# Optional Ticket Testing Specification

Artifact type: Specification

Artifact ID: `optional-ticket-testing-spec`

Workflow ID: `optional-ticket-testing`

Core version: `1.0.1`

Target release version: `1.1.0`

Status: Approved

Inputs: [Approved Optional Ticket Testing Requirement Decision Record](../requirements/optional-ticket-testing.md), existing Core `1.0.1` workflow contracts, and current Codex and Generic adapter contracts.

Assumptions: `tdd` and `direct` are stable internal behavioral mode names and serialized routing values. User-facing selection must instead ask whether tests should be added. Behavioral tests include unit, integration, end-to-end, and equivalent executable behavior checks; lint, type-check, and build are non-test verification.

Deferred: Exact surrounding prompt prose, optional effort-estimation format, exact serialized mode field name, and migration wording for generated packages.

Handoff: After explicit approval, `$plan-tickets`.

Approval: The earlier Specification and plain-language localized-documentation revision were explicitly approved by the user on 2026-08-04. The user explicitly approved this batch-selection revision on 2026-08-04 after confirming that any number of Ticket test choices can be supplied in one response. Target release version `1.1.0` remains unchanged.

## Problem

The current workflow requires each planned Ticket to define a test-first approach and routes every approved Ticket to TDD implementation. This makes test runtime unavoidable even when a user knowingly prefers faster delivery with lower verification confidence.

The workflow needs an explicit per-Ticket test choice stated in language that first-time users understand. That choice must preserve the existing TDD and direct implementation paths without exposing their internal names as the initial decision.

## Goals

- Give the user final authority over whether behavioral tests are added for every Ticket.
- Ask for that authority using localized add-tests language instead of unexplained implementation-mode terminology.
- Collect all Ticket test choices in one batch so interaction count does not grow linearly with Ticket count.
- Make the time and risk tradeoff visible before Ticket Plan approval.
- Route tested and untested Tickets through distinct, honest implementation contracts.
- Preserve traceability from the approved selection through implementation and Review.
- Keep provider-neutral Core, Codex, and Generic behavior aligned.

## Non-goals

- Rename `$implement-tdd` or make tests optional inside that Skill.
- Force tests based on repository policy, CI, release, security, privacy, or migration risk.
- Represent lint, type-check, or build as behavioral test evidence.
- Treat direct implementation as having TDD-equivalent confidence.
- Bypass requirements, Specification, Ticket Plan, Review, capability, or evidence gates.
- Override an external system that independently requires tests.

## Users and scenarios

### Mixed test-choice plan

The user receives a Draft Ticket Plan, chooses to add tests to higher-risk Tickets and not add tests to lower-risk Tickets, approves the complete plan, and sees each choice routed through the matching internal implementation stage.

### All-direct plan

The user reviews the recommendation, chooses not to add tests to every Ticket, approves the plan, and receives Review-backed completion evidence that explicitly states tests were skipped.

### All-TDD plan

The user chooses to add tests to every Ticket and receives the existing Red, Green, refactor, and broader-verification behavior without semantic weakening.

### Conversation-only Generic user

The user receives a portable plan and implementation guidance that describes the selected route without claiming repository changes, command execution, test results, persistence, or completed implementation.

## Required behavior

### Ticket planning and selection

1. A Draft Ticket Plan MUST list every Ticket before requesting test choices.
2. For each Ticket, the workflow MUST recommend whether behavioral tests should run, MUST give a scope-specific risk reason, and MUST warn that adding tests may increase work time.
3. After presenting all recommendations and warnings, the workflow MUST request all Ticket test choices in one batch. It MUST NOT require one conversational round trip per Ticket, present "choose `tdd` or `direct`" as the user-facing question, or assume that the user knows those terms.
4. The question and answer labels MUST match the user's language. The required semantic choices are "add tests" and "do not add tests"; every localized `START-HERE` copy and all affected Traditional Chinese, English, and Japanese README, guide, design, release, and adapter Markdown MUST express those meanings consistently.
5. The batch request MUST accept: tests for all Tickets, tests for no Tickets, or an explicit mixed selection that resolves every Ticket. An explicit construction such as "add tests to Tickets 1 and 3; do not add tests to the rest" is valid.
6. The workflow MUST map "add tests" to internal mode `tdd` and "do not add tests" to internal mode `direct`. It MUST NOT infer a default from silence, repository conventions, risk, prior Tickets, or an incomplete mixed response.
7. The user MUST be allowed to decline tests for every Ticket.
8. The plan MUST remain Draft while any Ticket lacks a user test choice and mapped mode. When a mixed response does not explicitly resolve the remaining Tickets, the workflow MUST request only the unresolved choices.
9. The plan approval request MUST display the complete Ticket list and each plain-language test choice. It MAY also show the mapped internal mode for traceability, but MUST NOT make knowledge of that mode necessary for approval. One explicit approval MUST approve both the Ticket definitions and their test choices.
10. A test-choice or mapped-mode change after approval MUST return the Ticket Plan to Draft and MUST block affected implementation until the revised plan is explicitly reapproved.

### Routing

1. An eligible `tdd` Ticket MUST route to `$implement-tdd` in Codex and to the equivalent TDD module in other adapters.
2. An eligible `direct` Ticket MUST route to `$implement-direct` in Codex and to the equivalent direct implementation module in other adapters.
3. A missing, unknown, conflicting, or unapproved mode MUST stop before implementation. The workflow MUST NOT fall back to either path.
4. Completion of dependencies MUST NOT change a Ticket's approved mode.

### TDD implementation

1. `$implement-tdd` MUST retain its existing readiness, Red, Green, refactor, risk-proportional verification, evidence, and exception contracts.
2. The new selection mechanism MUST NOT permit a Ticket routed to `$implement-tdd` to skip its required behavioral test evidence except for the existing declared test-first exception contract.
3. TDD evidence MUST continue to distinguish observed commands and results from unavailable checks.

### Direct implementation

1. `$implement-direct` MUST require an Approved Specification, an Approved Ticket Plan, an eligible `direct` Ticket, and completed dependencies.
2. It MUST inspect applicable repository instructions, relevant code, current changes, and approved boundaries before editing when the host has tools.
3. It MUST implement only the approved Ticket behavior and MUST preserve unrelated user changes.
4. It MUST NOT create, modify, or execute unit, integration, end-to-end, or equivalent behavioral tests for the Ticket.
5. It MAY execute lint, type-check, build, static validation, or equivalent non-behavioral checks when the host supports tools.
6. It MUST inspect the final change for scope drift and unintended files.
7. Its evidence MUST include changed areas, available non-test commands and raw results, `tests: skipped-by-user`, unavailable behavioral evidence, residual risks, and the Ticket outcome.
8. It MUST NOT emit Red, Green, passing-test, or behavior-verified claims.
9. It MUST hand the Approved artifacts, selected Ticket, final diff or supplied change evidence, available validation results, and skipped-test disclosure to Review.
10. A conversation-only adapter MUST label its output as unexecuted direct implementation guidance and MUST NOT claim edits, execution, persistence, or completed Implementation Evidence.

### Review and completion

1. Review MUST accept evidence from either implementation path and MUST retain the approved Ticket mode.
2. For a `direct` Ticket, Review MUST NOT execute or prescribe automatic execution of the behavioral tests declined by the user.
3. Review of a `direct` Ticket MUST state `tests: skipped-by-user`, unavailable behavioral evidence, untested areas, and risk appropriate to the changed behavior.
4. Existing Review independence labels and the twelve Architecture and Refactoring Lenses MUST remain unchanged.
5. A `direct` Ticket MAY be assessed complete when the approved behavior appears implemented and Review has no blocking finding, but the report MUST NOT claim behavioral test success or TDD completion.
6. A finding that requires implementation MUST follow the approved workflow again; changing the Ticket mode requires a revised and reapproved Ticket Plan.

### Recommendations and external constraints

1. Recommendations MUST consider available evidence about correctness, regression, security, privacy, migration, integration, destructive behavior, and release risk.
2. A strong recommendation MUST remain advisory. No risk category or repository instruction may remove the user's `direct` option inside this workflow.
3. When an external CI, hosting, or release system independently requires tests, the workflow MUST disclose that constraint and MUST NOT claim that selecting `direct` can bypass it.

### Cross-adapter consistency

1. Provider-neutral Core MUST define planning, routing, direct implementation, evidence, and Review behavior for both modes.
2. The Codex Plugin MUST expose `$implement-direct` while retaining `$implement-tdd`.
3. The Generic workflow MUST include an equivalent direct implementation prompt and route selected modes consistently within its conversation-only capability.
4. Adapter mappings, manifests, generated package inventories, human documentation, and conformance validation MUST agree with the Core contract.
5. Existing generated `1.0.1` artifacts MAY remain immutable release evidence; active outputs for this feature MUST use release version `1.1.0`.

## Edge cases and failure behavior

- If the user does not answer whether to add tests for every Ticket, the workflow stops at the Ticket Plan gate.
- If a batch answer names only some Tickets without stating what happens to the rest, the named choices are retained and the workflow asks only for the unresolved Tickets.
- If the plan text and a handoff disagree about a Ticket's mode, the Approved Ticket Plan controls and the conflicting downstream artifact is invalid.
- If a direct implementation attempt creates or executes a behavioral test, it violates the direct contract and cannot be reported as conforming direct evidence.
- If non-test validation fails, direct implementation cannot claim successful completion while that known failure remains unresolved or honestly deferred through a revised upstream decision.
- If an external system blocks delivery for missing tests, the workflow reports the external block; it does not silently run tests or misreport delivery.
- If new evidence changes the recommended mode, the workflow explains the new risk. Only the user may approve a mode revision.

## Data, permissions, and external contracts

- Every Ticket owns one approved plain-language test choice and its mapped internal execution mode for the current plan revision.
- The test choice, mapped mode, user approval evidence, recommendations, skipped-test disclosure, validation results, and residual risks travel through durable workflow artifacts.
- No new personal data, credential, permission, network service, or external mutation is required.
- Repository instructions and external CI or release contracts remain evidence and operational constraints, but do not become workflow-enforced mandatory tests.

## Compatibility, rollout, and recovery

- `$implement-tdd` remains a compatible public Skill with unchanged meaning for `tdd` Tickets.
- `$implement-direct` is an additional public Skill, so active Codex and Generic package inventories and user guides must expose the new path consistently.
- Existing Approved plans without an execution mode cannot enter the new implementation contract until revised and explicitly reapproved.
- Existing `1.0.1` release packages and evidence remain historical; the new active packages and evidence use `1.1.0`.
- Recovery from a wrong selection is a Ticket Plan revision followed by explicit reapproval; the workflow does not silently rewrite modes.

## Constraints and assumptions

- The workflow can warn about likely additional time but is not required to produce an exact duration estimate.
- Risk recommendations use repository and approved-artifact evidence available to the host and state limitations when evidence is incomplete.
- Non-test validation may consume time and may be executed by `$implement-direct` without converting the Ticket to TDD.
- Review remains diagnostic and does not authorize fixes or a mode change.

## Acceptance criteria

1. Given a Draft Ticket Plan, the user sees every Ticket, a reasoned test recommendation, and a warning that adding tests may increase work time before being asked whether to add tests.
2. One batch request can collect the choices for all Tickets, whether the plan contains two Tickets or fifty.
3. The batch request accepts all-add, all-decline, and explicit mixed choices that resolve every Ticket.
4. The user-facing question and answers are expressed as "add tests" or "do not add tests" in the user's language, not as an unexplained choice between `tdd` and `direct`.
5. A Ticket Plan with any unanswered test choice or missing mapped mode cannot become Approved or route to implementation.
6. The user can approve any mixture of added and declined tests, including declining tests for every Ticket; these choices map deterministically to `tdd` and `direct`.
7. An Approved `tdd` Ticket routes only to the unchanged TDD implementation contract.
8. An Approved `direct` Ticket routes only to the new direct implementation contract.
9. No repository, CI, release, security, privacy, migration, or risk classification makes a workflow test mandatory.
10. Direct implementation creates and executes no behavioral tests while allowing non-test validation.
11. Direct evidence contains `tests: skipped-by-user`, raw available validation, unavailable behavioral evidence, and residual risks without TDD claims.
12. Review preserves the selected mode, does not run declined tests, and reports the missing evidence and risk.
13. A direct Ticket can be marked complete after a non-blocking Review without being described as tested or TDD-complete.
14. Changing a test choice or mapped mode after approval returns the plan to Draft and blocks affected implementation until reapproval.
15. Core, Codex Plugin, Generic workflow, documentation, package inventories, and conformance results describe and enforce the same behavior within their capabilities.
16. Every localized `START-HERE` copy and all affected Traditional Chinese, English, and Japanese README, guide, design, release, and adapter Markdown consistently ask whether tests should be added and do not use `tdd` or `direct` as the initial user-facing choice.
17. Active Codex and Generic release outputs, manifests, checksums, and evidence for this feature consistently identify version `1.1.0` while existing `1.0.1` evidence remains historical.

## Deferred decisions

- Exact surrounding prose outside the required localized "add tests" or "do not add tests" meanings.
- Whether adapters display qualitative effort only or an optional estimate when reliable evidence exists.
- Exact serialized field names beyond the stable `tdd` and `direct` semantics.
- Exact release-note and migration wording.
