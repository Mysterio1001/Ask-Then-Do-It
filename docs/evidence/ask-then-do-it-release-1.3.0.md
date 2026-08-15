# Ask Then Do It Release 1.3.0 Evidence

Artifact type: Release Evidence

Artifact ID: `ask-then-do-it-release-1.3.0-evidence`

Workflow ID: `lite-workflow-mode`

Workflow core version: `1.1.0`

Repository Core version: `1.3.0`

Release version: `1.3.0`

Status: Completed

Inputs: Approved [1.3.0 Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), completed [Ticket 8](lite-workflow-mode-1.3.0-ticket-8.md), Tickets 1-7 implementation and Review handoffs, [package-link correction Review](lite-workflow-mode-1.3.0-package-link-correction-review.md), [direct-entry correction Review after P2](lite-workflow-mode-1.3.0-direct-entry-correction-review-after-p2.md), [post-P2 architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-p2-fix.md), [final independent Review](ask-then-do-it-1.3.0-final-independent-review-after-p2.md), completed [user-document footer independent Review](ask-then-do-it-1.3.0-user-document-footer-independent-review.md), [validation ledger](ask-then-do-it-release-1.3.0.json), prior [evidence closure Review](ask-then-do-it-1.3.0-evidence-closure-review.md), and final [evidence-only closure Review](ask-then-do-it-1.3.0-evidence-closure-after-footer.md).

Assumptions: This is local pre-publication evidence. Version-pinned documentation and download targets are release contracts that become externally resolvable only after the separately controlled `v1.3.0` tag and publication steps.

Deferred: Git tag, GitHub Release, push, upload, installation, publication, announcement, external CI, additional operating systems, live installed-Codex dispatch, and live third-party model execution.

Handoff: Local pre-publication validation and evidence closure are complete. External release actions remain separately controlled and are not authorized by this artifact.

## Outcome

Ask Then Do It `1.3.0` adds Config-selected Full and Lite workflows across provider-neutral Core, Codex, Generic prompts, and three-language documentation. Full preserves the existing assurance-oriented gates. Lite uses one conversation-only Change Brief approval, no workflow artifact or new behavioral-test files, proportionate minimum validation, user-approved Review corrections, and fresh mode resolution in each session.

The deterministic Codex proxy reports Full `14,771` and Lite `5,480` workflow-controlled proxy tokens, a difference of `9,291` and a `62.90%` reduction. This is not an API billing guarantee. Generic discloses a fixed composed-prompt cost of `15,376` proxy tokens and makes no 60% claim.

## Validation

- Final serial automated discovery: `193/193` passed.
- Release suite: `108/108` passed.
- Codex, Generic, and conformance suites: `27/27`, `39/39`, and `19/19` passed.
- Canonical and packaged Plugin validation: `2/2` passed.
- Canonical and packaged Skill validation: `18/18` passed.
- Marketplace and both adapter conformance CLIs passed against Core `1.3.0`.
- Two isolated builds were byte-reproducible; expanded directories and ZIP entries were equivalent.
- All twelve packaged host/locale guide links are pinned to `v1.3.0`; no packaged repository-root `/docs/guides/` link remains.
- Sixteen approved historical `1.2.0` artifacts retained their pinned SHA-256 values.
- The evidence gate rejects removal, absence, or failure of `workflow-token-proxy`.
- The completed ledger and release evidence passed `scripts/validate_release_evidence.py`: every configured required check is present and passed.
- The first final Full Review's two findings were corrected with user approval and passed an independent no-finding correction Review.
- The approved direct-entry corrections passed independent Review; Generic retains two complete resolver owners and nine bounded standalone projections rather than defaulting every Generic use to Lite.
- The post-P2 read-only architecture diagnosis found all release blockers structurally closed and no remaining release correctness blocker. Its non-blocking Draft proposals authorize no refactor.
- The final independent Review found no actionable P0-P3 finding.
- The user-document footer independent Review found no actionable finding across the approved 22-file navigation set and regenerated package outputs.
- The final evidence-only closure Review found no actionable finding after independently matching statuses, required checks, proxy values, archive hashes, and local links.

One concurrent full-discovery attempt encountered a Windows temporary-directory `WinError 5` in an atomic-upgrade test. That test passed alone and in the complete release suite, and serial discovery passed. The first post-correction production rebuild later encountered a separate temporary atomic-move `WinError 5`; rollback preserved the previous output and the immediate serial retry succeeded. No source assertion remained failed.

## Package layout

```text
dist/
|- codex/
|  |- ask-then-do-it/
|  `- ask-then-do-it-1.3.0.zip
|- generic/
|  |- ask-then-do-it-generic-1.3.0/
|  `- ask-then-do-it-generic-1.3.0.zip
`- checksums.sha256
```

## Archive hashes

```text
7f80461578791c25d07f81bbddebf6ec5ca30ae7f1f816335c77330d7045d19d  codex/ask-then-do-it-1.3.0.zip
511ecccadb39ced89182ce55c4dd96f2571a59928fdb374829b0c5d6e4f0bebd  generic/ask-then-do-it-generic-1.3.0.zip
```

## Publication boundary

No Plugin installation, user Config mutation, personal marketplace change, Git tag, GitHub Release, push, upload, announcement, automatic downgrade, or external publication occurred.
