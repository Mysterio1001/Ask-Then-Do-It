# Ask Then Do It Project Knowledge Base

Artifact type: Project Knowledge Base

Artifact ID: `ask-then-do-it-project-knowledge-base`

Workflow ID: `command-install-update`

Core version: `1.3.0`

Status: Approved

Inputs: Approved historical requirement/specification artifacts, Approved `1.3.0` release evidence, and Approved `release-1-3-1-maintenance-requirements`.

Assumptions: Approved `1.3.0` release evidence describes the current completed local release. `1.3.1` is the approved maintenance target until implementation and release evidence establish completion.

Deferred: Universal public Plugin Directory, unattended update delivery, private fork distribution, external release execution.

Handoff: Keep synchronized with Approved Specifications and Ticket Plans.

Approval: 原始 Knowledge Base 於 2026-08-13 核准；使用者於 2026-08-17 在完整 `1.3.1` Requirement Decision Record 與 Knowledge Base Change Summary 展示後明確核准本次同步。

## Glossary

- **Repository marketplace**: `.agents/plugins/marketplace.json` catalog used to discover the official Plugin through GitHub; it is not part of consumer ZIPs.
- **Official Plugin source**: `https://github.com/Mysterio1001/Ask-Then-Do-It.git`, subdirectory `adapters/codex/plugin/ask-then-do-it`, at a formal Git tag.
- **AI-assisted update**: User-authorized, state-aware execution of Codex marketplace and Plugin commands; not a background updater.
- **ZIP fallback**: Versioned GitHub Release archive maintained as a supported manual installation path.

## Architecture map

- `core/`: Provider-neutral workflow contract.
- `adapters/codex/plugin/ask-then-do-it/`: Canonical Codex Plugin source, including manifest, Skills, start guides, and visual assets.
- `.agents/plugins/marketplace.json`: Repository-only catalog pointing at the tagged canonical Plugin subdirectory.
- `release/release.json` and `scripts/build_release.py`: Versioned deterministic release definition and builder using complete staging validation, managed-output replacement, and rollback to protect local release output.
- `dist/`: Generated Codex and Generic consumer packages plus checksums; excludes marketplace catalog.
- `tests/release/`: Release, inventory, marketplace, documentation, image asset, reproducibility, ZIP, checksum, and evidence gates.

## Important decisions

- `1.2.0` is the first command-installable release; `v1.1.0` stays immutable. Evidence: Approved `command-install-update-1-2-requirements`.
- Catalog follows `main`, while installable Plugin entries pin the latest formal tag. Evidence: Approved `command-install-update-1-2-requirements`.
- Natural-language install/update requests authorize the necessary state-aware writes; version checks remain read-only. Evidence: Approved `command-install-update-1-2-requirements`.
- Failures stop without automatic downgrade; ZIP remains a supported fallback. Evidence: Approved `command-install-update-1-2-requirements`.
- Plugin branding uses transparent red seahorse-question-mark assets and `#C8262A`. Evidence: Approved `command-install-update-1-2-requirements`.
- `1.3.1` is a release-reliability maintenance target limited to declaring the Pillow development/test dependency and improving Windows serial release replacement reliability. Evidence: Approved `release-1-3-1-maintenance-requirements`.
- Same-output concurrent builds, Token fingerprint changes, CI, dependency locking, documentation expansion, and broad builder refactoring are outside `1.3.1`. Evidence: Approved `release-1-3-1-maintenance-requirements`.
- Managed-output replacement and rollback restoration explicitly include Windows `WinError 5` in the bounded-retry allowlist. Because that error code cannot distinguish transient file occupation from a permanent ACL denial, permanent access-denied may wait briefly until the retry limit; other non-allowlisted errors fail immediately. If rollback cannot complete, recovery staging/backup data and both primary and recovery errors must be preserved and reported. Evidence: Approved revised `release-1-3-1-maintenance-requirements`.
- Current release, Core, Codex adapter, Generic adapter, and runtime identities advance together to `1.3.1`; `v1.3.0` and its historical artifacts remain immutable. Evidence: Approved `release-1-3-1-maintenance-requirements`.

## External dependencies

- OpenAI Codex Plugin marketplace and `codex plugin` CLI behavior documented by OpenAI.
- GitHub repository tags and Releases under `Mysterio1001/Ask-Then-Do-It`.
- User-provided source image identified by SHA-256 `C22CF733EBF01ECFEB9C5E9A29AC37496A8B78BBE09F22D5942EC31F0B374EBB` during asset production only.
- CPython 3.12 and `Pillow>=12.3,<13` are the `1.3.1` development and release-validation baseline. Pillow is not a Codex or Generic consumer runtime dependency.

## Unresolved items

- Local `codex.exe` command help could not be executed in the current environment; target compatibility must be verified through official documentation and, when available, a functioning target CLI.
- Actual Git tag, GitHub Release, push, upload, and announcement remain maintainer-controlled external operations.
- The `v1.3.1` tag, push, GitHub Release, asset upload, Marketplace activation, and announcement remain pending explicit approval and observed execution results.

## Artifact links

- Requirement Decision Record: [Command install, update, and icon 1.2.0](../requirements/command-install-update-1.2.0.md).
- Specification: [Command install, update, and icon 1.2.0](../specs/command-install-update-1.2.0.md).
- Historical requirement: [Clean-slate 1.0.0](../requirements/grill-me-clean-slate-1.0.0.md).
- Historical specification: [Clean-slate 1.0.0](../specs/grill-me-clean-slate-1.0.0.md).
- Approved 1.3.0 Requirement Decision Record: [Full/Lite workflow mode 1.3.0](../requirements/lite-workflow-mode-1.3.0.md).
- Approved 1.3.0 Specification: [Full/Lite workflow mode 1.3.0](../specs/lite-workflow-mode-1.3.0.md).
- Approved 1.3.0 Ticket Plan: [Full/Lite workflow mode 1.3.0](../plans/lite-workflow-mode-1.3.0.md).
- Approved 1.3.0 release evidence: [Ask Then Do It release 1.3.0](../evidence/ask-then-do-it-release-1.3.0.md).
- Approved 1.3.1 Requirement Decision Record: [Release reliability maintenance 1.3.1](../requirements/release-1.3.1-maintenance.md).
- Approved 1.3.1 Specification: [Release reliability maintenance 1.3.1](../specs/release-1.3.1-maintenance.md).
- Approved 1.3.1 Ticket Plan: [Release reliability maintenance 1.3.1](../plans/release-1.3.1-maintenance.md).
