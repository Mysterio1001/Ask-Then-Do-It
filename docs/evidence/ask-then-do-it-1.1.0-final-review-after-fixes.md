# Ask Then Do It 1.1.0 Final Review after Fixes

Artifact type: Review Report

Artifact ID: `ask-then-do-it-1-1-final-review-after-fixes`

Workflow ID: `optional-ticket-testing`

Core version: `1.1.0`

Status: Completed

Review label: `non-independent`

Reviewed inputs: Approved [Specification](../specs/optional-ticket-testing.md), Approved [Ticket Plan](../plans/optional-ticket-testing.md), [Ticket 4 Implementation Evidence](optional-ticket-testing-ticket-4.md), superseded [first Final Review](ask-then-do-it-1.1.0-final-review.md), complete final diff and surrounding source, generated packages, tests, and raw verification results.

Approved implementation mode: `tdd` for Tickets 1-4.

Assumptions: The broader conformance architecture proposals remain unaccepted and outside this fix. Release completion requires the current Approved Specification to be represented and verified, not acceptance of optional future refactoring.

Deferred: Independent reviewer execution, external CI and hosting behavior, additional operating systems, Plugin installation, marketplace behavior, publication, live third-party model execution, and the Draft conformance architecture proposals.

Handoff: Final release evidence and maintainer-controlled local handoff. No installation or publication is authorized.

## Findings

No new actionable or release-blocking finding remains. The two P2 findings from the first Review are resolved across Core, Codex, Generic, tests, and rebuilt packages:

- All three planning contracts now require complete Ticket definitions before mode selection and require recommendations to consider correctness, regression, security, privacy, migration, integration, destructive behavior, and release risk, while identifying unavailable evidence.
- All three direct paths now disclose independent external CI, hosting, or release-system test constraints and delivery blocks without claiming `direct` bypasses them. All three Review paths prohibit executing or prescribing automatic execution of declined behavioral tests.

## Twelve Architecture and Refactoring Lenses

| Lens | Outcome | Evidence |
| --- | --- | --- |
| Duplicated Code or Policy | `finding` | The cross-adapter policy remains manually replicated; it is already tracked in the Draft [Architecture Improvement Report](ask-then-do-it-1.1.0-release-architecture-diagnosis.md), and exact Core/Codex/Generic scenario assertions now cover the Approved clauses. |
| Long Function | `no-finding` | Validator routines remain short and cohesive; the fix changed declarative contracts and focused assertions. |
| Large Module or Class | `no-finding` | Planning, direct implementation, TDD, and Review remain separate modules with distinct responsibilities. |
| Long Parameter List | `no-finding` | No public executable interface gained additional parameters. |
| Data Clumps | `no-finding` | Mode, approval, external constraints, skipped-test disclosure, and residual risks are intentionally carried by durable workflow artifacts. |
| Primitive Obsession | `no-finding` | `tdd` and `direct` remain a closed, validated pair with explicit invalid-state behavior. |
| Feature Envy | `not-applicable` | The reviewed scope is primarily declarative policy and owned validation logic, not behavior operating on another object's data. |
| Divergent Change | `no-finding` | The immediate fix stayed within the existing planning, direct implementation, and Review reasons-to-change. |
| Shotgun Surgery | `finding` | Cross-adapter policy still requires coordinated edits; this systemic concern is already tracked by the Draft architecture report and did not produce remaining semantic drift in the reviewed clauses. |
| Message Chains | `not-applicable` | No relevant runtime object-navigation chain exists in the changed scope. |
| Leaky Abstraction | `finding` | Coarse rule-ID conformance still relies on adapter scenario tests for clause-level assurance; the Draft architecture report owns the future proposal. |
| Shallow Module | `finding` | `Conformance passed` remains narrower than full semantic equivalence, but current release behavior is independently covered by the three focused scenario tests and full regression suite. |

## Verification performed

- Review-fix Red: three focused tests failed for the expected missing contract clauses.
- Review-fix Green: the same three tests passed.
- Final full regression after rebuilding and evidence-link validation: `Ran 66 tests in 4.713s`; `OK`.
- Official validation: canonical and packaged Plugins passed; all eighteen Skill instances returned `Skill is valid!`.
- Release safety tests rebuilt two isolated releases, proved byte reproducibility and ZIP/directory parity, and verified current hashes.
- `git diff --check` reported no whitespace errors; only informational LF-to-CRLF checkout warnings.

## Evidence unavailable and residual risks

- Review is non-independent because the same context implemented the changes.
- External systems may still independently require tests; the workflow now discloses rather than bypasses that constraint, but no live external CI or hosting service was exercised.
- One intermediate full run encountered a transient Windows `WinError 5` during temporary-directory replacement. The affected safety test and the subsequent complete suite passed; additional operating systems and sustained stress execution remain unverified.
- The Draft architecture report documents future semantic-conformance improvements; it is not accepted and authorizes no implementation.
- Installation, marketplace behavior, publication URLs, additional operating systems, and live third-party model execution remain unverified.

## Completion assessment

The Approved Specification and all four `tdd` Tickets now appear complete. Core, nine Codex Skills, ten Generic prompt files, localized documentation, generated packages, checksums, and verification evidence consistently represent Ask Then Do It `1.1.0`. No blocking Review finding remains.
