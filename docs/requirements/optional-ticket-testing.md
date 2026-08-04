# Optional Ticket Testing Requirement Decision Record

Artifact type: Requirement Decision Record

Artifact ID: `optional-ticket-testing-requirements`

Workflow ID: `optional-ticket-testing`

Core version: `1.0.1`

Target release version: `1.1.0`

Status: Approved

Inputs: User feedback about TDD test runtime, first-time-user terminology, and excessive interaction when a plan contains many Tickets; the existing Ticket Planning, TDD Implementation, Review, orchestration, adapter, and release contracts.

Assumptions: In this requirement, tests are automated behavioral checks such as unit, integration, and end-to-end tests. Lint, type-check, and build checks are non-test verification. `tdd` and `direct` remain stable internal routing values, but are not the choices shown in the initial per-Ticket question.

Deferred: Exact surrounding prompt prose, serialized Ticket Plan field names, and effort-estimation format.

Handoff: `$write-spec`

Approval: The earlier execution-mode contract was explicitly approved by the user on 2026-08-04. The user explicitly approved the plain-language test-choice revision and its full localized-documentation scope on 2026-08-04. The user then explicitly approved batch collection of all Ticket test choices on 2026-08-04 so a plan with many Tickets does not require one conversational round trip per Ticket. Target release version `1.1.0` remains unchanged.

## Problem and desired outcome

Users report that executing tests during TDD increases the time required to complete implementation. The current workflow sends every approved Ticket to `$implement-tdd` and does not let the user choose whether that additional time is warranted.

The desired outcome is a user-owned choice for every Ticket. The workflow recommends which Tickets should have tests, then asks in the user's language whether to add tests to each Ticket. It maps that plain-language answer to either TDD or direct implementation without requiring the user to understand those internal names and without imposing any mandatory test.

## Users and success signals

### Workflow user

- Sees all planned Tickets before implementation begins.
- Sees a risk-based test recommendation and a warning that tests may increase work time before each test choice.
- Is asked whether to add tests to each Ticket, using plain language instead of being asked to choose `tdd` or `direct`.
- Can add tests to any subset of Tickets or decline tests for every Ticket.
- Can submit all Ticket choices in one response instead of answering once per Ticket.
- Can identify which Tickets were tested and which were deliberately left behaviorally unverified.

### Implementer and reviewer

- Receives one explicitly approved implementation mode for every Ticket.
- Routes a Ticket without guessing or silently defaulting.
- Preserves honest evidence when tests were skipped by user choice.
- Can complete a directly implemented Ticket after Review without claiming that tests passed.

## Scope

- Add the test-selection decision to Draft Ticket Planning.
- Ask whether to add tests to every Ticket before Ticket Plan approval, then record the answer internally as `tdd` when tests are added or `direct` when tests are not added.
- Collect the complete set of choices in one batch after all recommendations are visible, accepting all-add, all-decline, or explicit mixed selections.
- Do not require one conversational round trip per Ticket; a 50-Ticket plan can be classified in one response.
- Update every localized `START-HERE` copy and all affected Traditional Chinese, English, and Japanese Markdown documentation and adapter prompts, keeping the user-facing test-choice meaning consistent everywhere.
- Keep `$implement-tdd` for Tickets whose mode is `tdd`.
- Add `$implement-direct` for Tickets whose mode is `direct`.
- Permit `$implement-direct` to run lint, type-check, and build checks while prohibiting behavioral test creation and execution.
- Carry `tests: skipped-by-user`, unavailable behavioral evidence, and residual risk into implementation and Review evidence.
- Apply equivalent behavior to the provider-neutral Core, Codex Plugin, and Generic workflow.
- Update routing, artifacts, documentation, package inventories, and conformance expectations affected by the additional path.

## Non-goals

- Rename or weaken `$implement-tdd` for Tickets that select TDD.
- Retain any workflow-level test that the user cannot skip.
- Claim that direct implementation provides the same confidence as TDD.
- Let Review silently run the behavioral tests that the user declined.
- Override enforcement performed by an external CI, hosting, or release system outside this workflow's control.

## Primary behavior and user flow

1. `$plan-tickets` creates a Draft Ticket Plan from an Approved Specification.
2. The workflow presents every Ticket, recommends whether each Ticket should receive tests with a reason, and warns that adding tests may increase work time.
3. After all recommendations are visible, the workflow asks the user to classify all Tickets in one batch. It MUST use clear localized test language and MUST NOT require the user to choose between the unexplained labels `tdd` and `direct`.
4. The batch request accepts three forms: add tests to all Tickets, add tests to no Tickets, or identify the Tickets that should have tests and the disposition of every remaining Ticket.
5. An answer to add tests maps to internal mode `tdd`; an answer not to add tests maps to internal mode `direct`. The user may decline tests for all Tickets.
6. The Ticket Plan cannot become Approved, and implementation cannot start, while any Ticket lacks an explicit selection.
7. One approval covers the complete Ticket Plan, including all test choices and their internal routing values.
8. A `tdd` Ticket routes to `$implement-tdd` and follows its existing Red, Green, refactor, and broader-verification contract.
9. A `direct` Ticket routes to `$implement-direct`, which implements the approved behavior without creating or executing behavioral tests. It may run non-test verification.
10. Both paths hand their raw evidence to `$review-code`.
11. A directly implemented Ticket may be marked complete when Review has no blocking finding, but the evidence must retain `tests: skipped-by-user` and disclose that behavior was not test-verified.

## Edge cases and failure behavior

- There is no default implementation mode. Missing user selection blocks Ticket Plan approval and implementation.
- A repository, CI configuration, release policy, security concern, or migration risk may cause the workflow to recommend tests strongly, but does not make them mandatory within the workflow.
- External systems may still reject untested work; the workflow reports that external constraint honestly rather than claiming it can bypass it.
- Review must not convert a `direct` Ticket to TDD or run declined behavioral tests without a later user-approved plan revision.
- Changing a mode after Ticket Plan approval returns the plan to Draft and requires explicit reapproval before affected implementation continues.
- Evidence from `direct` implementation must not use TDD Red or Green labels or imply an observed passing behavior.

## Data, dependencies, security, privacy, and operations

- The selected mode is durable Ticket Plan data and travels with Ticket handoffs and evidence.
- No new personal data, permission, secret, or external service is introduced.
- Skipping tests may increase correctness, security, privacy, migration, and regression risk; recommendations and Review must disclose the relevant risk rather than hiding it.
- Core, Codex, and Generic adapters must remain semantically consistent within their proven capability profiles.
- Generic conversation-only prompts may propose work but must not claim execution, persistence, test results, or completed implementation.

## Acceptance criteria

- Every Ticket in an approvable plan has an explicit user answer to whether tests should be added.
- All per-Ticket recommendations are displayed before one batch selection request.
- The batch selection accepts all-add, all-decline, and explicit mixed choices without requiring one response per Ticket.
- The selection prompt includes a risk-based recommendation, its reason, and a warning that adding tests may increase work time before asking whether to add tests.
- The selection prompt does not ask first-time users to choose `tdd` or `direct`; those values remain internal routing and serialization details.
- Adding tests maps to `tdd`, declining tests maps to `direct`, and declining tests for every Ticket is valid.
- Every localized `START-HERE` copy and all affected Traditional Chinese, English, and Japanese README, guide, design, release, and adapter Markdown express the same add-tests or do-not-add-tests choice.
- No repository-, CI-, release-, security-, or migration-based test is forced by the workflow.
- A `tdd` Ticket routes only to `$implement-tdd`.
- A `direct` Ticket routes only to `$implement-direct`.
- `$implement-direct` neither creates nor executes behavioral tests and may perform lint, type-check, and build verification.
- Direct Implementation Evidence and Review Report both retain `tests: skipped-by-user`, unavailable test evidence, and residual risk.
- Review does not run declined behavioral tests and may support completion without claiming test success.
- Core, Codex Plugin, Generic workflow, documentation, packaging, and conformance checks describe the same two-path behavior.

## Confirmed decisions

- Test execution is entirely the user's choice; there are no mandatory workflow tests.
- The plain-language test choice is made for all Tickets in the Draft Ticket Plan before one final plan approval.
- Test choices are collected as one batch; the workflow does not require a separate conversational turn for every Ticket.
- The user can choose all-add, all-decline, or an explicit mixed set while retaining an individual result for every Ticket.
- User-facing prompts ask whether tests should be added; they do not require users to understand `tdd` or `direct`.
- Internally, adding tests selects `tdd` and declining tests selects `direct`, preserving deterministic routing and evidence.
- The workflow recommends high-risk Tickets for tests while leaving final authority with the user.
- `$implement-tdd` remains unchanged in identity and handles only selected TDD Tickets.
- `$implement-direct` is a new public Skill or equivalent adapter stage for untested Tickets.
- Direct implementation may perform non-test verification.
- Untested Tickets can complete after non-blocking Review with explicit risk disclosure.
- The feature targets release version `1.1.0`; existing `1.0.1` release artifacts remain historical evidence.
