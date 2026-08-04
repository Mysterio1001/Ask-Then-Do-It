# Ask Then Do It 1.1.0 Final Review

Artifact type: Review Report

Artifact ID: `ask-then-do-it-1-1-final-review`

Workflow ID: `optional-ticket-testing`

Core version: `1.1.0`

Status: Superseded by [Final Review after fixes](ask-then-do-it-1.1.0-final-review-after-fixes.md)

Review label: `non-independent`

Reviewed inputs: Approved [Specification](../specs/optional-ticket-testing.md), Approved [Ticket Plan](../plans/optional-ticket-testing.md), Tickets 1-4 Implementation Evidence, complete working-tree diff and surrounding source, generated packages, tests, and raw verification results.

Approved implementation mode: `tdd` for Tickets 1-4.

Assumptions: The Approved Specification is authoritative over condensed Core and adapter wording. A required behavior is incomplete when no normative contract or executable scenario prevents an adapter from omitting it.

Deferred: Independent reviewer execution, external CI and hosting behavior, additional operating systems, Plugin installation, marketplace behavior, publication, and live third-party model execution.

Handoff: `$improve-architecture` for read-only diagnosis of the cross-adapter semantic drift. Any accepted improvement returns to Specification before implementation.

## Findings

### [P2] Show the complete Ticket definitions before collecting modes and require the approved risk dimensions

Trigger: a user receives a multi-Ticket plan whose scope details or security, privacy, migration, integration, destructive-operation, or release exposure affects the test decision. The Codex plan gate currently presents only dependency order, vertical outcomes, and parallel groups before collecting modes ([plan-tickets/SKILL.md](../../adapters/codex/plugin/ask-then-do-it/skills/plan-tickets/SKILL.md#L74)); the Core and Generic contracts say only `risk-based` without requiring the complete Ticket definitions to be displayed first or the Specification's enumerated risk dimensions ([ticket-planning.md](../../core/modules/ticket-planning.md#L16), [generic ticket-planning.md](../../adapters/generic-prompts/ticket-planning.md#L41)). The user can therefore be asked to choose `tdd` or `direct` without all Approved decision context, and a recommendation can omit required high-impact evidence while still passing current tests. Require the complete Ticket list and definitions before mode selection, enumerate the approved recommendation dimensions, and add sequence plus omission-negative tests across Core, Codex, and Generic.

### [P2] Preserve external test constraints and prohibit Review from automatically prescribing declined tests

Trigger: a `direct` Ticket targets a repository whose CI, host, or release system independently requires or executes behavioral tests. Direct implementation currently forbids the workflow from running tests but never requires disclosure that an external system can still block or test delivery ([direct-implementation.md](../../core/modules/direct-implementation.md#L8), [implement-direct/SKILL.md](../../adapters/codex/plugin/ask-then-do-it/skills/implement-direct/SKILL.md#L20), [Generic direct implementation](../../adapters/generic-prompts/direct-implementation.md#L23)). Review prohibits executing declined tests but does not prohibit prescribing their automatic execution ([core review.md](../../core/modules/review.md#L11), [review-code/SKILL.md](../../adapters/codex/plugin/ask-then-do-it/skills/review-code/SKILL.md#L38), [Generic review.md](../../adapters/generic-prompts/review.md#L26)). This can mislead a user about deliverability or reintroduce the declined work through Review, contrary to the Approved Specification. Require external-constraint disclosure and blocked-delivery handling, explicitly prohibit automatic test prescriptions, and cover both behaviors in all three contract layers.

## Twelve Architecture and Refactoring Lenses

| Lens | Outcome | Evidence |
| --- | --- | --- |
| Duplicated Code or Policy | `finding` | Mode-selection policy is manually restated across Core, Codex, Generic, localized documentation, and string-fragment tests; the two findings show clauses already drifted. |
| Long Function | `no-finding` | The only executable production change, `validate_release_evidence.validate`, remains a short single-purpose validation routine. |
| Large Module or Class | `no-finding` | New direct implementation contracts remain separate modules; no changed class or module gained unrelated runtime responsibilities. |
| Long Parameter List | `no-finding` | No changed public function introduced an excessive parameter list; the release validator still takes three cohesive artifact paths. |
| Data Clumps | `no-finding` | Ticket mode, approval, skipped-test disclosure, and evidence are intentionally grouped in durable workflow artifacts rather than repeatedly passed as loose runtime parameters. |
| Primitive Obsession | `no-finding` | `tdd` and `direct` are intentionally closed, stable serialized values with explicit invalid-state handling. |
| Feature Envy | `not-applicable` | Most changed units are declarative contracts; the release validator operates only on its owned configuration and evidence data. |
| Divergent Change | `no-finding` | Direct implementation, TDD, Review, and planning remain separate reasons-to-change at module level. |
| Shotgun Surgery | `finding` | One policy change touched 72 tracked files plus new modules, evidence, and generated outputs; semantic omissions occurred despite the broad edit and green suite. |
| Message Chains | `not-applicable` | No changed runtime object navigation or chained call interface exists in this documentation-first workflow layer. |
| Leaky Abstraction | `finding` | Conformance validates version, rule IDs, capabilities, and evidence paths but not rule semantics, so every adapter test must know and restate selected Core phrases to compensate. |
| Shallow Module | `no-finding` | `$implement-direct` and `direct-implementation.md` expose a small interface while hiding a meaningful readiness, no-test, evidence, and handoff contract. |

## Verification performed

- Full regression: `Ran 66 tests`; `OK`.
- Focused release suite: `Ran 43 tests`; `OK`, including two isolated byte-identical builds, ZIP/directory parity, current archive hashes, exact inventories, and documentation links.
- Official validation: canonical and packaged Plugins passed; all eighteen Skill validations passed.
- `git diff --check`: no whitespace errors; only informational LF-to-CRLF checkout warnings.
- Active-source scan found no remaining `1.0.1` declarations in Core, adapters, release configuration, root entry files, or active guides.

## Evidence unavailable and residual risks

- The same context implemented and reviewed the change, so this is not an independent Review.
- Existing tests verify selected phrases and inventories but do not model the two missing behavior sequences above.
- External CI, hosting, installation, publication URLs, additional operating systems, and live third-party model behavior were not exercised.
- Generated package integrity is verified locally, but release readiness remains blocked by the two P2 Specification gaps.

## Completion assessment

The four implementation Tickets produced the intended two routes and integrated `1.1.0` packages, but the Approved Specification is not yet completely represented across Core, Codex, and Generic. The release does not appear complete until both findings are resolved through the gated workflow and the final Review is repeated.
