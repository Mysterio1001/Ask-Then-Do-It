# Ask Then Do It 1.3.0 Evidence Closure Review

Artifact type: Review Report

Artifact ID: `ask-then-do-it-1-3-evidence-closure-review`

Workflow ID: `lite-workflow-mode`

Workflow core version: `1.1.0`

Repository Core version: `1.3.0`

Status: `complete - no actionable findings`

Review label: `independent`

Approved implementation mode: Ticket 8 `tdd` (the user selected Add tests).

Reviewed inputs: Current [validation ledger](ask-then-do-it-release-1.3.0.json), [release evidence](ask-then-do-it-release-1.3.0.md), [Ticket 8 evidence](lite-workflow-mode-1.3.0-ticket-8.md), and [Approved Ticket Plan](../plans/lite-workflow-mode-1.3.0.md); their links to the [final independent Review](ask-then-do-it-1.3.0-final-independent-review-after-p2.md), [post-P2 architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-p2-fix.md), current `release/release.json`, `dist/checksums.sha256`, the two current archives, deterministic proxy output, and release-evidence validator result.

Independence: This reviewer context did not implement the feature, corrections, packages, tests, or evidence refresh. The verdict was rebuilt from the current files and read-only checks.

Assumptions: The final Review and architecture diagnosis are historical pre-refresh handoffs; their statements that evidence was pending are superseded only by the current refreshed artifacts and successful evidence validation. `dist/` remains builder-generated output.

Deferred: Git tag, GitHub Release, push, upload, installation, publication, announcement, external CI, additional operating systems, live installed-Codex dispatch, live third-party model execution, remote `v1.3.0` URL availability, and unaccepted Draft proposals F2-F4.

Handoff: Ticket 8 and the local pre-publication evidence closure are complete. This Review authorizes no source correction, Config mutation, installation, publication, or external release action.

## Findings

No actionable P0, P1, P2, or P3 finding was identified in the evidence-only administrative delta.

## Closure checks

| Check | Result | Evidence |
| --- | --- | --- |
| Status and handoff | `passed` | Release evidence, Ticket 8, and Ticket 8 in the Approved Plan are `Completed`; their handoffs limit completion to the local pre-publication candidate and keep external release actions separately controlled. |
| Required-check inventory | `passed` | `release/release.json` and the ledger contain the same ordered 13 IDs, including mandatory `workflow-token-proxy`; there are no missing, extra, duplicate, failed, or empty command/outcome entries. |
| Validator | `passed` | `scripts/validate_release_evidence.py` returned `Release evidence 1.3.0 validated: all required checks passed`. |
| Proxy | `passed` | A fresh deterministic run reported Full `14,771`, Lite `5,480`, difference `9,291`, reduction `62.90%`, composite fixture fingerprint `90384287b87d8f58be4c3ce458c3b215199667c3301f3a668399bbbcda884fe3`, and Generic fixed cost `15,376`. The evidence makes no API-billing or Generic-reduction claim. |
| Archives and checksums | `passed` | Direct SHA-256 recalculation matched `dist/checksums.sha256`: Codex `e2838c830ca56b3c8dc901783e8c773127a65cd0096ddef63f2e919c615bb73e`; Generic `7751999bb2fc01a6ddae0717ddfbd7dc213796d7c2f79d0b7bfe6556eaf39e9d`. |
| Counts and links | `passed` | The evidence consistently records `192/192`, `107/107`, `27/27`, `39/39`, `19/19`, `18/18`, and `2/2`; every local Markdown input link resolves. |
| Review and architecture gates | `passed` | The final independent Review is complete with no actionable finding. The post-P2 Draft diagnosis reports no release correctness blocker and explicitly leaves F2-F4 unaccepted and nonblocking. |
| Premature-claim boundary | `passed` | No current scoped artifact retains the old proxy/hash values or `Review Pending`. Completion is explicitly local and pre-publication; live host/model behavior and all external actions remain deferred. |

## Twelve architecture and refactoring lenses

| Lens | Outcome | Evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `no-finding` | The administrative values agree across the scoped ledger, evidence, Ticket, and Plan; broader policy projection remains deferred F2. |
| 2. Long Function | `not-applicable` | The delta is Markdown/JSON evidence and status metadata, not executable function logic. |
| 3. Large Module or Class | `not-applicable` | No module or class changed in this administrative scope; builder breadth remains deferred F4. |
| 4. Long Parameter List | `not-applicable` | No callable interface changed. |
| 5. Data Clumps | `no-finding` | Counts, hashes, statuses, and check records remain grouped in the ledger/evidence surfaces that own them. |
| 6. Primitive Obsession | `no-finding` | The scoped IDs and statuses conform to the current validator contract; its declaration-based limitation remains deferred F3. |
| 7. Feature Envy | `not-applicable` | No executable ownership or cross-module data access changed. |
| 8. Divergent Change | `no-finding` | Each scoped edit serves the single release-evidence closure responsibility. |
| 9. Shotgun Surgery | `no-finding` | The required evidence projections are synchronized and independently cross-checked; broader policy fan-out remains deferred F2. |
| 10. Message Chains | `not-applicable` | The scope contains direct artifact links and declarative records, not object-navigation chains. |
| 11. Leaky Abstraction | `no-finding` | Local completion, external publication, proxy limitations, and Draft architecture status remain explicit; validator provenance limits remain deferred F3. |
| 12. Shallow Module | `not-applicable` | No module interface was introduced or changed by the administrative delta. |

## Verification performed

- Ran the release-evidence validator with the current config, ledger, and release evidence; it exited `0`.
- Compared required-check and ledger inventories programmatically: `13/13`, exact order, unique IDs, all `passed`, and all command/outcome fields populated.
- Re-ran the deterministic token proxy and matched every current ledger value and limitation.
- Recalculated both archive SHA-256 values and matched the checksum manifest and both Markdown evidence files.
- Resolved every local Markdown link from release and Ticket 8 evidence.
- Searched the four scoped administrative artifacts for prior proxy values, prior archive hashes, and `Review Pending`; none remain.

The earlier `192/192`, `107/107`, adapter, validator, package, reproducibility, ZIP-equivalence, and historical-hash executions were not repeated in this evidence-only pass; their raw results are carried by the current ledger and final independent Review.

## Residual risks

The evidence validator proves inventory, status, and required text shape, not execution provenance; this remains the unaccepted, nonblocking Draft F3 proposal. Live Codex/Generic behavior, remote tag-pinned URLs, external CI, other operating systems, installation, publication, and sustained concurrent build behavior remain unverified or deferred. The known Windows atomic-rename transients remain disclosed in the completed evidence and were followed by successful serial reruns.

## Completion assessment

The evidence-only closure is complete with no actionable findings. Current status, counts, required checks, proxy output, hashes, links, Review result, architecture boundary, and deferred external actions agree, so the local pre-publication `1.3.0` completion claim is supported without broadening into publication or live-host claims.
