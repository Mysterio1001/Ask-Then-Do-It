# Ask Then Do It Release 1.1.0 Evidence

Artifact type: Implementation Evidence

Artifact ID: `ask-then-do-it-release-1.1.0-evidence`

Workflow ID: `optional-ticket-testing`

Core version: `1.1.0`

Release version: `1.1.0`

Status: Completed

Inputs: Approved [Optional Ticket Testing Specification](../specs/optional-ticket-testing.md), completed [Ticket Plan](../plans/optional-ticket-testing.md), Tickets 1-6 Implementation Evidence, [Independent Ticket 5 Review](optional-ticket-testing-ticket-5-review.md), [Independent Ticket 6 Review](optional-ticket-testing-ticket-6-review.md), and [Release Architecture Diagnosis](ask-then-do-it-1.1.0-release-architecture-diagnosis.md).

Assumptions: The local release handoff does not install, publish, upload, or modify a marketplace. The unaccepted architecture proposals are deferred and authorize no changes.

Deferred: Installation, marketplace mutation, publication, upload, external CI and hosting execution, additional operating systems, and live third-party model behavior.

Handoff: Maintainer-controlled inspection and any separate installation or publication decision.

## Outcome

Ask Then Do It `1.1.0` now presents every Ticket with a scope-specific test recommendation and per-Ticket work-time warning, then collects all plain-language add-tests choices in one batch. The user may add tests to all Tickets, add them to none, or identify a mixed subset; incomplete mixed choices leave only unresolved Tickets pending. Adding tests maps internally to `tdd`, while declining tests maps to `direct`, without requiring first-time users to know those names.

Codex routes internally mapped `direct` Tickets to `$implement-direct`; Generic routes them to `direct-implementation.md`. TDD remains test-driven; direct implementation does not create or run behavioral tests and preserves `tests: skipped-by-user` through Review.

External CI, hosting, or release-system test constraints are disclosed without claiming that `direct` bypasses them. Review neither executes nor prescribes automatic execution of declined behavioral tests.

## Validation

- Ticket 5 TDD: three focused Core/Codex/Generic contract tests observed expected Red and Green; two independent Review-fix cycles strengthened per-Ticket warnings, ordering, state retention, and negative prompt coverage. Final focused result: `Ran 3 tests`; `OK`.
- Ticket 6 TDD: two localized-documentation tests observed `69` expected subtest failures before source changes, then `Ran 2 tests`; `OK`. The complete documentation module observed and corrected four integration failures, then `Ran 14 tests`; `OK`.
- Final top-level discovery includes Codex and conformance after adding package markers and a discovery regression guard; the earlier 68-test result was incomplete. One corrected run encountered a transient Windows `WinError 5` during atomic temporary-directory replacement; the affected test passed alone (`Ran 1 test in 0.208s`; `OK`), and the repeated final full regression passed: `Ran 98 tests in 5.134s`; `OK`.
- Canonical and packaged Plugin validation passed; all eighteen Skill instances passed official validation.
- Codex and Generic conformance passed against Core `1.1.0`.
- Exact inventories contain nine Codex Skills and ten Generic prompt files.
- Two isolated complete builds were byte-identical; both ZIPs equal their generated directories.
- `dist/checksums.sha256` contains exactly two verified `1.1.0` entries.
- Ticket 5 and Ticket 6 independent Reviews have no remaining finding. Architecture diagnosis is read-only; broader proposals remain Draft.

## Package layout

```text
dist/
├─ codex/
│  ├─ ask-then-do-it/
│  └─ ask-then-do-it-1.1.0.zip
├─ generic/
│  ├─ ask-then-do-it-generic-1.1.0/
│  └─ ask-then-do-it-generic-1.1.0.zip
└─ checksums.sha256
```

## Archive hashes

```text
bc98595ddde5b06ae2a0d4419c5ef1dc95cc9a495b18047d50ced9f6ce547dc4  codex/ask-then-do-it-1.1.0.zip
0cd6b9dd87c6dd262c67a7def05882c3463210c38296289b5c4b16ac160a7326  generic/ask-then-do-it-generic-1.1.0.zip
```

## Review and architecture

- [Independent Ticket 5 Review](optional-ticket-testing-ticket-5-review.md)
- [Ticket 6 Implementation Evidence](optional-ticket-testing-ticket-6.md)
- [Independent Ticket 6 Review](optional-ticket-testing-ticket-6-review.md)
- [Earlier Final Review after fixes](ask-then-do-it-1.1.0-final-review-after-fixes.md)
- [Superseded first Final Review](ask-then-do-it-1.1.0-final-review.md)
- [Draft Release Architecture Diagnosis](ask-then-do-it-1.1.0-release-architecture-diagnosis.md)
- [Validation ledger](ask-then-do-it-release-1.1.0.json)

## Publication boundary

No Plugin installation, marketplace change, publication, upload, release hosting mutation, or external communication occurred.
