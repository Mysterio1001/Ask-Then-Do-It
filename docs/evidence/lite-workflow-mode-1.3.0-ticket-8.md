# Lite Workflow Mode 1.3.0 Ticket 8 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `lite-workflow-mode-1-3-ticket-8-evidence`

Workflow ID: `lite-workflow-mode`

Workflow core version: `1.1.0`

Repository Core version: `1.3.0`

Release version: `1.3.0`

Status: Completed

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), completed Tickets 1-7 and their Review/correction handoffs, completed [final-review corrections](lite-workflow-mode-1.3.0-final-review-corrections.md), [direct-entry correction Review after P2](lite-workflow-mode-1.3.0-direct-entry-correction-review-after-p2.md), [post-P2 architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-p2-fix.md), [final independent Review](ask-then-do-it-1.3.0-final-independent-review-after-p2.md), completed [user-document footer independent Review](ask-then-do-it-1.3.0-user-document-footer-independent-review.md), [validation ledger](ask-then-do-it-release-1.3.0.json), completed [release evidence](ask-then-do-it-release-1.3.0.md), prior [evidence closure Review](ask-then-do-it-1.3.0-evidence-closure-review.md), and final [evidence-only closure Review](ask-then-do-it-1.3.0-evidence-closure-after-footer.md).

Approved implementation mode: `tdd`.

Assumptions: `release/release.json` is the authoritative required-check inventory. Final evidence may trust only checks actually observed in this workflow. A Draft architecture proposal does not authorize implementation. Generated `dist/` may be changed only through the release builder.

Deferred: External publication/tag/push/upload, installation, Config mutation, additional operating systems, external CI, live installed-Codex dispatch, and live third-party model behavior.

Handoff: Local pre-publication validation and evidence closure are complete. External release actions remain separately controlled and are not authorized by this artifact.

## Evidence-gate TDD

The focused tests added explicit protection for three proxy-gate failure paths: removing the mandatory proxy gate from release configuration, omitting the proxy result from the ledger, and recording the proxy result as failed.

Red command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_release_evidence -v
```

Observed before the validator correction:

```text
Ran 9 tests in 1.053s
FAILED (failures=1)
```

The missing-ledger and failed-result cases already failed closed. The one valid missing behavior was that a self-consistent release configuration and ledger could both omit `workflow-token-proxy` and still validate.

The smallest production change added `workflow-token-proxy` to the validator's non-removable mandatory check set.

Focused Green:

```text
Ran 9 tests in 0.874s
OK
```

## Integrated validation

- Final serial discovery: `Ran 193 tests in 19.174s`; `OK`.
- Final release suite: `Ran 108 tests in 15.746s`; `OK`.
- Codex, Generic, and conformance suites: `27/27`, `39/39`, and `19/19` passed.
- All 18 canonical/packaged Skills and both canonical/packaged Plugins passed official validators.
- Marketplace and both conformance CLIs passed.
- Token proxy remained above the fixed gate at Full `14,771`, Lite `5,480`, difference `9,291`, reduction `62.90%`, fixture SHA-256 `90384287b87d8f58be4c3ce458c3b215199667c3301f3a668399bbbcda884fe3`; Generic fixed cost is `15,376` with no Generic reduction or billing claim.
- The focused token-proxy and evidence-gate suites passed `19/19` and `9/9`.
- Two clean builds, exact inventories, ZIP equivalence, checksums, atomic replacement, and historical hashes passed.
- `git diff --check` exited `0` with only configured Windows LF-to-CRLF warnings.

An earlier concurrent full-discovery attempt hit a temporary Windows `WinError 5` in the atomic prior-release upgrade test. The same test passed inside the complete release suite, passed alone (`1/1`), and serial discovery passed. After the P1/P2 corrections, the first production rebuild encountered another temporary `WinError 5` while moving `dist/generic`; the builder restored the prior output and removed staging, and the immediate serial retry succeeded. No production correction was made for either environment-only transient.

## Review and architecture corrections

The first read-only architecture diagnosis found one package-link blocker. Work stopped, the finding was presented to the user, and correction proceeded only after explicit approval. The correction used TDD, rebuilt `dist/`, and passed an independent no-finding Review. The after-fix architecture closure verified source/expanded/ZIP/checksum parity and found F1 resolved.

The first final independent Full Review then found two blockers: Codex Skill discovery excluded small software changes before Config mode resolution, and Generic's editable declaration was shipped under an unqualified `DO NOT EDIT` banner. Both findings were presented together and corrected only after explicit user approval. Their TDD regressions, rebuilt packages, deterministic proxy refresh, and independent correction Review passed.

A later final Review found that direct public stage entrypoints could bypass top-level mode resolution. After user approval, Codex stage Skills were routed through the canonical resolver and Generic standalone stages received the approved bounded direct-entry guard while `bootstrap.md` and `orchestration.md` retained complete resolver ownership. The correction passed independent Review, and the post-P2 architecture diagnosis found all release blockers structurally closed. The final independent Review found no actionable P0-P3 finding.

F2-F4 remain unaccepted, non-blocking Draft maintainability proposals. They authorize no refactor and are excluded from this Ticket's implementation scope.

## Release candidate state

- Codex archive SHA-256: `7f80461578791c25d07f81bbddebf6ec5ca30ae7f1f816335c77330d7045d19d`.
- Generic archive SHA-256: `511ecccadb39ced89182ce55c4dd96f2571a59928fdb374829b0c5d6e4f0bebd`.
- Validation ledger contains exactly every configured required check with `passed` status and observed command/outcome text.
- Release evidence is `Completed` after the footer Review, evidence validator, and final evidence-only closure accepted the regenerated package hashes and footer links.
