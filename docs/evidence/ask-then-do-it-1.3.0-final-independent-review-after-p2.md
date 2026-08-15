# Ask Then Do It 1.3.0 Final Independent Review After P2

Artifact type: Review Report

Artifact ID: `ask-then-do-it-1-3-final-independent-review-after-p2`

Workflow ID: `lite-workflow-mode`

Core version: `1.3.0`

Status: `complete - no actionable findings`

Review label: `independent`

Approved implementation mode: Ticket 8 `tdd` (the user selected Add tests for all Tickets).

Reviewed inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md); Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md); the complete current working-tree diff and relevant surrounding Core, Codex, Generic, documentation, tests, release configuration, builders, validators, expanded packages, ZIPs, checksums, and architecture closure; [Ticket 8 evidence](lite-workflow-mode-1.3.0-ticket-8.md); pending [validation ledger](ask-then-do-it-release-1.3.0.json); pending [release evidence](ask-then-do-it-release-1.3.0.md); and raw verification rerun in this reviewer context.

Independence: This reviewer context did not implement the reviewed source, tests, packages, or corrections. Prior reports were used only as repository history and input links; the verdict below was derived from the approved artifacts, current files, current generated output, and independently rerun checks.

Assumptions: Canonical source is authoritative and `dist/` is generated only through `scripts/build_release.py`. `bootstrap.md` and `orchestration.md` are the complete Generic resolver owners; the other nine Generic modules use the approved bounded standalone-entry guard. The local worktree is a cumulative, uncommitted candidate, so ownership is inferred from the Approved Ticket Plan rather than commit boundaries.

Deferred: Live installed-Codex dispatch and Config unreadability behavior; live third-party Generic model adherence; remote `v1.3.0` URL dereference; external CI and other operating systems; installation, tag, push, upload, publication, and announcement; and the unaccepted Draft architecture proposals F2-F4.

Handoff: Return this blocker-free Review to Ticket 8. Refresh the validation ledger, Ticket 8 evidence, and release evidence from the current observed proxy output and archive hashes, run the release-evidence validator, then perform the evidence-only closure review. No source correction is requested by this Review.

## Findings

No actionable P0, P1, P2, or P3 correctness, security, compatibility, scope, validation, or packaging finding was identified in the current candidate. The earlier Codex discovery issue, Generic edit-banner issue, and package-link issue remain structurally closed under the current source, tests, generated output, ZIPs, and checksums.

The current pending evidence is not a source finding: `docs/evidence/ask-then-do-it-release-1.3.0.md` and `docs/evidence/lite-workflow-mode-1.3.0-ticket-8.md` still contain older candidate values and intentionally remain `Review Pending`. They must be refreshed before a completion claim. The current validator correctly rejects that pending status.

## Acceptance coverage

| Criteria | Result | Review evidence |
| --- | --- | --- |
| 1-5 | `passed structurally` | Codex precedence and fail-closed rules are explicit in the canonical orchestrator; Generic declaration, override, and fallback are explicit in the two resolver modules and the composed entrypoint. Direct-entry guards cover the nine standalone Generic modules and eight Codex stage Skills. Live host/model adherence remains unverified. |
| 6 | `passed structurally` | Full remains a separate route with its existing artifacts, gates, Ticket `tdd`/`direct` choices, Review, capability, and architecture contracts; Core, adapter, and regression suites pass. |
| 7-17 | `passed` | Lite question, Change Brief, risk pause, one approval, no-artifact/no-new-test boundary, proportionate validation, correction approval, compact Review, completion budget, and session reset are present in Core, Codex, Generic, and the three-language guides and are covered by focused tests. |
| 18 | `passed` | The deterministic Codex proxy reports Full `14,771`, Lite `5,480`, difference `9,291`, reduction `62.90%` (`6,290` basis points) against the fixed `6,000`-basis-point gate. Generic reports a fixed composed cost of `15,376` and makes no reduction or billing claim. |
| 19-21 | `passed` | README heading/order boundaries, complete localized Full/Lite guides, host ownership, source/package semantic parity, versioned links, and package entrypoints pass the release documentation and package tests. |
| 22 | `passed mechanically; evidence refresh pending` | Active `1.3.0` identity, conformance, inventories, reproducible builds, ZIP equivalence, checksums, historical hashes, and architecture closure pass. Ticket 8 cannot be marked complete until the pending ledger/evidence is rewritten from the current observations and accepted by the evidence gate. |

## Twelve architecture and refactoring lenses

This is a change-focused Review, not a new system-wide architecture diagnosis. Existing non-blocking proposals are recorded and referenced rather than treated as release blockers.

| Lens | Outcome | Evidence and classification |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `finding` | F2 remains an unaccepted Draft proposal: mode precedence, risk categories, budgets, approvals, validation, Review, and session behavior are projected across Core, both adapters, three locales, fixtures, and tests. The current direct-entry projections are standardized and tested; no new correctness defect is introduced. |
| 2. Long Function | `no-finding` | Reviewed changed executable paths (`compose_generic_workflow`, release validation, token proxy, and evidence validation) are linear, cohesive pipelines. No current failure is attributable to individual function length. |
| 3. Large Module or Class | `finding` | F4 remains an unaccepted Draft proposal: `scripts/build_release.py` owns source/schema validation, composition, package/archive generation, checksums, and filesystem replacement. Current outputs and failure handling are correct, so this is non-blocking maintainability evidence. |
| 4. Long Parameter List | `no-finding` | No changed public callable exposes an unstable coordination list; builder and composer interfaces retain cohesive config/path inputs. |
| 5. Data Clumps | `no-finding` | Mode sources, proxy events, package inventories, and evidence checks are represented by explicit configuration objects/collections rather than new loose argument bundles. |
| 6. Primitive Obsession | `finding` | F3 remains an unaccepted Draft proposal: release-check IDs, statuses, commands, and outcomes are primitive self-declared strings in `scripts/validate_release_evidence.py`. It is an assurance-design limitation, not a current candidate correctness finding. |
| 7. Feature Envy | `no-finding` | The token proxy reuses the builder-owned Generic composer; package tests inspect their owned outputs; adapter mappings remain on their own surfaces. No changed path reaches through an unrelated unit's internals. |
| 8. Divergent Change | `finding` | F2/F4 remain: policy projections and the release builder change for multiple reasons. They are already routed to the Draft architecture report and are outside Ticket 8's approved implementation scope. |
| 9. Shotgun Surgery | `finding` | A future mode-policy change still spans Core, adapters, localized docs, fixtures, package inventories, archives, checksums, and evidence (the F2 proposal). Current deterministic builder and parity tests contain the release fan-out and no new drift was found. |
| 10. Message Chains | `not-applicable` | The scoped implementation is declarative Markdown/YAML/JSON plus direct filesystem, ZIP, and hash operations; there is no meaningful object-navigation chain to assess. |
| 11. Leaky Abstraction | `finding` | P1/P2 ownership and dispatch leaks are closed. F3 remains a non-blocking boundary leak because the evidence validator checks declared status/text but does not bind executor identity, exit status, raw result artifacts, or package digests. |
| 12. Shallow Module | `finding` | F3 remains: the evidence validator presents a completion gate while encapsulating only declaration/status checks. The resolver owners and bounded stage guards are proportional to their documented interfaces. |

The `finding` outcomes above are existing, non-blocking Draft architecture proposals already routed to [the post-P2 architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-p2-fix.md); they do not request a correction to this release candidate.

## Verification performed

- Full serial discovery: `192/192` passed in `14.956s` with the bundled Pillow site-packages exposed through `PYTHONPATH`.
- Release discovery: `107/107` passed in `13.709s`.
- Codex, Generic, and Core conformance suites: `27/27`, `39/39`, and `19/19` passed.
- Canonical and packaged Skill validation: `18/18` returned `Skill is valid!`; canonical and packaged Plugin validation: `2/2` passed.
- Codex and Generic conformance CLIs passed against Core `1.3.0`; marketplace validation passed through the release suite.
- Deterministic proxy execution passed: Full `14,771`, Lite `5,480`, reduction `62.90%`; fixture SHA-256 `90384287b87d8f58be4c3ce458c3b215199667c3301f3a668399bbbcda884fe3`; Generic fixed cost `15,376`.
- Release contract, documentation, source inventory, two-clean-build reproducibility, atomic replacement, ZIP equivalence, checksum, historical-hash, and evidence-gate tests passed. Current expanded inventories are Codex `27` files and Generic `18` files.
- Current archive SHA-256 recalculation matches `dist/checksums.sha256`: Codex `e2838c830ca56b3c8dc901783e8c773127a65cd0096ddef63f2e919c615bb73e`; Generic `7751999bb2fc01a6ddae0717ddfbd7dc213796d7c2f79d0b7bfe6556eaf39e9d`.
- `git diff --check` passed; only configured Windows LF-to-CRLF informational warnings were emitted.
- Running `scripts/validate_release_evidence.py` against the current candidate failed only on the expected `Status: Review Pending` gate. It must be rerun after evidence refresh.
- One initial full-discovery attempt encountered the known transient Windows `WinError 5` atomic-rename failure. The affected test passed alone (`1/1`), and the immediate complete rerun passed `192/192`; the release suite also passed `107/107`.

## Evidence unavailable and residual risks

- No live installed Codex Plugin operation exercised every implicit/direct-entry and Config precedence combination. Static Skill contracts, focused regressions, package parity, and conformance are the strongest available evidence.
- No live third-party Generic model was run through all resolver and standalone-module paths; text and composition tests cannot prove model adherence.
- The six version-pinned guide URLs cannot be dereferenced until separately authorized publication creates the `v1.3.0` tag.
- The pending ledger and Ticket 8/release evidence still report the prior proxy values (`13,828`/`5,416`) and prior archive hashes (`f4448e...`/`b399c9...`), while the current raw run reports `14,771`/`5,480` and `e2838c...`/`775199...`. This is an explicit evidence-refresh handoff, not an implementation defect.
- Release evidence provenance remains declaration-based rather than execution-bound, as tracked by F3.
- The proxy clears the fixed gate by `2.90` percentage points; future controlled workflow-text growth could reduce that margin.
- External CI, non-Windows environments, installation, sustained concurrent build stress, and publication remain unverified or deferred.

## Completion assessment

This independent Review is complete with no actionable findings. The approved P1/P2 corrections and prior package-link correction remain closed, and current source, tests, documentation, packages, ZIPs, checksums, and raw validation agree. Ticket 8 and the local release are not yet administratively complete solely because the pending ledger/evidence must be refreshed to this current candidate and then accepted by the evidence validator. No source fix, publication, or external release action is authorized by this Review.
