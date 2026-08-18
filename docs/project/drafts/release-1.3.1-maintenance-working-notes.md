# Ask Then Do It 1.3.1 Maintenance Release Draft Working Notes

Artifact type: Draft Working Notes

Artifact ID: `release-1-3-1-maintenance-working-notes`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Status: Draft

Inputs: User decisions in the 2026-08-17 conversation, including explicit approval of the `WinError 5` retry tradeoff; current `dev` repository state; Approved `1.3.0` requirement, specification, plan, and release evidence; current Project Knowledge Base; and read-only architecture findings about development dependencies and Windows release replacement.

Assumptions: `v1.3.0` and its published artifacts remain immutable. The target is a new patch release `1.3.1`, not a rewrite of `1.3.0`.

Deferred: Implementation, dependency installation, Token fingerprint changes, CI, broad builder refactoring, external Git tag creation, GitHub Release publication, Marketplace publication, push, upload, and announcement.

Handoff: Continue one-decision-at-a-time requirement clarification, then prepare a Draft Requirement Decision Record and Project Knowledge Base Change Summary.

Approval: Pending. These notes are provisional and are not formal project knowledge.

## Confirmed

- `confirmed`: The target is an Ask Then Do It `1.3.1` maintenance release.
- `confirmed`: `v1.3.0` and its existing release artifacts must not be overwritten.
- `confirmed`: The maintenance scope includes declaring the Pillow development/test dependency required by `tests/release/test_plugin_assets.py`.
- `confirmed`: The maintenance scope includes improving Windows release replacement reliability after observed transient `WinError 5` failures.
- `confirmed`: Token fingerprint canonicalization is outside this maintenance scope.
- `confirmed`: Basic CI and broad `build_release.py` reorganization are outside this maintenance scope.
- `confirmed`: `1.3.1` supports reliable serial release builds targeting one output directory.
- `confirmed`: Simultaneous builders targeting the same output directory are a non-goal for `1.3.1`.
- `confirmed`: The `1.3.1` development and release-validation baseline is CPython 3.12 with Pillow 12.x.
- `confirmed`: `requirements-dev.txt` declares `Pillow>=12.3,<13`; other Python or Pillow major versions are not compatibility commitments for `1.3.1`.
- `confirmed`: If forward replacement and rollback both fail, the builder preserves the staging and backup data needed for manual recovery and reports their paths instead of deleting them during cleanup.
- `confirmed`: Managed-output replacement and rollback restoration explicitly treat Windows `WinError 5` as retry-eligible and apply bounded retry.
- `confirmed`: Because `WinError 5` cannot distinguish transient file occupation from a permanent ACL denial, a permanent denial with the same code may wait until the bounded retry limit. Other non-allowlisted path, permission, structural, or unknown `OSError` failures are not retried.
- `confirmed`: `1.3.1` does not add or expand README or developer-guide content. Clean-environment installation and full-test commands are recorded in test and release evidence.
- `confirmed`: This workflow stops at a locally complete `1.3.1` candidate with packages, checksums, validation, and release evidence.
- `confirmed`: Creating `v1.3.1`, pushing, creating a GitHub Release, uploading assets, activating the Marketplace ref, and announcing the release each remain external publication actions requiring a later explicit approval.
- `confirmed`: `release_version`, `core_version`, Codex adapter, Generic adapter, and current runtime declarations advance in lockstep to `1.3.1`, following the existing patch-release convention.

## Proposed

- `proposed`: A clean development environment can install the declared development dependencies and import every test module without undeclared packages.
- `proposed`: The release builder retries allowlisted transient errors for a bounded duration and exposes no unbounded wait.
- `proposed`: A failed replacement preserves or restores the previously validated release without mixing old and new managed outputs; an incomplete rollback is reported as requiring manual recovery.
- `proposed`: Tests simulate transient and persistent replacement failures deterministically instead of depending on an intermittent operating-system failure.
- `proposed`: Consumer-facing Full/Lite behavior remains unchanged; active release identity, packages, documentation, Marketplace metadata, checksums, and evidence advance to `1.3.1` only as required by the existing release contract.

## Unresolved

None. All material requirement decisions are confirmed or intentionally deferred to Specification, Ticket Planning, or external publication approval.

## Evidence

- `requirements-dev.txt` declares PyYAML but not Pillow.
- `tests/release/test_plugin_assets.py` imports `PIL.Image` at module import time.
- `scripts/build_release.py::commit` performs multiple `os.replace` operations and rollback without bounded retry.
- `docs/evidence/ask-then-do-it-release-1.3.0.json` records earlier transient Windows `WinError 5` events and a successful manual retry.
- The user explicitly approved bounded retry for managed-output `WinError 5`, accepting that a permanent ACL denial with the same code may wait until the retry limit.
- The repository has formal tags through `v1.3.0`; no `1.3.1` requirement, specification, plan, tag, or release artifact currently exists.
