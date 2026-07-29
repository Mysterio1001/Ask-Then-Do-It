# Grill Me Release Packaging Specification

Artifact type: Specification

Artifact ID: `grill-me-release-packaging-spec`

Workflow ID: `grill-me-release-2-1`

Core version: `2.0.0`

Status: Approved

## Inputs

- Approved [Portable AI Development Workflow - v2 Specification](ai-development-skills.md).
- Explicit requirement consensus reached with the user on 2026-07-28.
- Validated Generic prompts adapter and Codex adapter currently maintained under `adapters/`.

## Assumptions

- The repository remains the authoring and validation source rather than an installed runtime location.
- Python is available for repository development and release building.
- The existing Generic and Codex adapter behavior remains compatible with core `2.0.0`.
- Generated release artifacts are disposable and reproducible from source.

## Deferred

- Automated modification of a user's personal Skill installation.
- Marketplace or remote publication.
- Provider-specific adapters other than Generic prompts and Codex.
- Cryptographic signing beyond SHA-256 checksums.
- External-publication licensing and distribution policy.

## Handoff

Hand this revised Approved Specification to Ticket Planning. Implementation remains prohibited until the revised Ticket Plan is explicitly approved.

## Approval

Approved by the user on 2026-07-28 through the explicit response `OK` to the revised Specification approval request. This approval includes the corrected `grill-me` Plugin root and release names.

## Problem

The repository contains a validated portable workflow, Generic prompts adapter, and six Codex Skills, but it exposes development internals before it exposes a clear consumer entry point. A user must understand `core/`, adapter layout, and source-versus-installation boundaries before discovering how to begin. The project also lacks a deterministic release builder, a Codex Plugin package, a self-contained Generic prompt, versioned runtime bundles, and checksums.

The result is technically validated source that still resembles an internal development repository rather than an installable or directly consumable AI Agent workflow product.

## Goals

- Provide one obvious repository entry point that routes users to either Codex or Generic usage.
- Package all six Codex Skills as one installable Codex Plugin while preserving independent Skill invocation.
- Provide one self-contained Generic workflow prompt as the primary conversation-only entry point while preserving modular prompts.
- Keep `core/` and `adapters/` as the only editable workflow and adapter sources.
- Produce minimal, versioned, reproducible runtime bundles from a deterministic build.
- Separate release versioning from core contract versioning.
- Verify package structure, source traceability, checksums, adapter conformance, and native Skill validity before a release is considered valid.
- Document manual installation, update, removal, and source-versus-generated boundaries without changing a user's environment.

## Non-goals

- Change the semantics of core `2.0.0`.
- Replace or merge the six modular workflow stages.
- Remove direct invocation of individual Codex Skills or direct use of modular Generic prompts.
- Install, update, or remove files in a user's personal Codex environment.
- Publish to a marketplace, remote repository, or other external service.
- Add or claim support for additional provider-specific adapters.
- Include development tests, evidence, full design documentation, or validation tooling inside runtime packages.
- Treat generated `dist/` content as editable source.

## Users and scenarios

### New Codex user

The user opens the repository, selects Codex from the root entry point, builds or obtains the Codex package, validates it, and follows manual installation instructions. The user installs one Plugin and normally begins with `$ai-dev-workflow`, while retaining access to all six individual Skills.

### General chat-model user

The user selects Generic usage, copies one self-contained prompt into a conversation, and lets the model route among requirement, Specification, Ticket Planning, unexecuted implementation guidance, and limited-evidence Review stages. The user may instead select an individual modular prompt.

### Maintainer

The maintainer edits only canonical source, runs one release command, inspects unpacked output, verifies ZIP and checksum artifacts, and confirms that rebuilding unchanged source produces equivalent release content.

### Security-conscious user

The user can build and inspect release packages without the build process modifying personal installation directories, invoking an installer, or contacting an external service.

## Required behavior

### 1. Repository entry point

The repository MUST provide a root `README.md` that presents two primary paths: Codex Plugin and Generic prompts.

The README MUST place the Traditional Chinese entry first and provide an English Quick Start covering the same two choices. It MUST link to the detailed Traditional Chinese design and usage guides rather than duplicating those documents.

The README MUST clearly distinguish canonical source, generated release output, and personal installation locations.

### 2. Product and version identity

The release product MUST use:

- Package ID `grill-me`.
- Display name `Grill Me — AI Development Workflow`.
- Release version `2.1.0`.
- Required core version `2.0.0`.

Release and core versions MUST remain independently represented. Packaging-only changes MUST NOT imply a core contract change.

### 3. Release configuration

`release/release.json` MUST be the single editable source for release identity, version, package names, source inputs, and managed outputs.

The release configuration MUST use a documented, versioned schema. Invalid, missing, unknown, or internally contradictory required values MUST stop the build with an actionable error.

The build MUST use only the Python standard library and MUST NOT require installation of an additional build dependency.

### 4. Codex Plugin source and package

The Codex Plugin source root MUST be `adapters/codex/plugin/grill-me/`. Its outer folder name and `.codex-plugin/plugin.json` `name` MUST both be `grill-me`, as required by the Codex Plugin contract.

The six canonical Codex Skill directories MUST move from `adapters/codex/skills/` to `adapters/codex/plugin/grill-me/skills/`. After the move validates, the former path MUST NOT remain as a duplicate source. Codex conformance metadata, rule mappings, and migration history remain outside the Plugin root under `adapters/codex/` and MUST resolve the new canonical paths.

The generated Codex runtime package MUST contain only the Plugin manifest and these Skill directories:

- `ai-dev-workflow`
- `grill-requirements`
- `write-spec`
- `plan-tickets`
- `implement-tdd`
- `review-code`

Installing the Plugin MUST preserve direct invocation of every Skill. The documented primary entry point MUST be `$ai-dev-workflow`.

The package MUST NOT contain core source, tests, evidence, release tooling, migration records, conformance fixtures, or full project documentation.

### 5. Generic prompt source and package

The Generic release package MUST contain:

- One generated `generic-workflow.md` primary entry point.
- One manifest identifying release version, core version, capability profile, and source modules.
- A `prompts/` directory containing the existing bootstrap and six modular prompts.

`generic-workflow.md` MUST be generated from the existing bootstrap and modular prompts in a deterministic declared order. It MUST NOT be maintained as an eighth hand-authored prompt source.

The generated prompt MUST route within one conversation without requiring the user to paste another module prompt. It MUST preserve the same approval gates, Artifact contracts, stop conditions, user-language behavior, and Conversation-only evidence limits as the modular adapter.

The Generic package MUST NOT claim repository modification, command execution, durable cross-session persistence, completed TDD, or independent Review.

### 6. Generated release outputs

One documented build command MUST generate these release artifacts under `dist/`:

- An unpacked `grill-me/` Codex Plugin directory whose root name matches its manifest.
- A `grill-me-2.1.0.zip` archive containing the `grill-me/` Plugin root.
- An unpacked `generic-prompts-2.1.0/` directory.
- A `generic-prompts-2.1.0.zip` archive.
- A `checksums.sha256` file covering the distributable archives.

The directory and corresponding ZIP MUST contain equivalent relative files and byte content. Archive metadata that normally varies between runs MUST be normalized sufficiently for unchanged source to produce reproducible archive bytes.

Every generated package MUST carry enough manifest information to trace it to package ID, release version, core version, adapter identity, and source inputs.

### 7. Safe build boundaries

The build MUST write only to managed release targets below the repository `dist/` directory.

Before replacing or removing a managed target, the build MUST resolve and verify that the target is inside the intended `dist/` root and matches the current release configuration.

Unknown files or directories in `dist/` MUST NOT be deleted or overwritten. A collision with an unmanaged target MUST stop the build and identify the path.

A failed build MUST NOT present incomplete output as a valid release. Existing valid output MUST either remain intact or be replaced only after the new output has completed validation.

The build MUST NOT read from or write to a personal Skill installation path, use an installer, publish externally, or require network access.

### 8. Validation

A release MUST be rejected unless all of the following pass:

- Existing core conformance tests.
- Existing Generic adapter tests and shared conformance validation.
- Existing Codex adapter tests and shared conformance validation.
- Official validation of all six Codex Skills.
- Codex Plugin manifest validation applicable to the supported format.
- Generic combined-prompt composition and Conversation-profile checks.
- Package inventory checks that reject missing, duplicate, extra, or stale runtime files.
- ZIP-to-directory content equivalence.
- SHA-256 checksum verification.
- A second unchanged build demonstrating reproducible package contents.
- Relative documentation link checks and provider-operation isolation checks.

Release validation MUST report commands or checks performed and raw outcomes. A failed or blocked required check MUST prevent a successful release status.

### 9. Documentation and installation boundary

The Codex guide MUST explain Plugin contents, build, validation, manual installation, update, removal, and the primary versus advanced Skill entry points.

The Generic guide MUST explain the one-file entry point, modular alternative, Conversation-only capability boundary, Artifact persistence responsibility, and workflow resumption.

Documentation MUST state that build and validation do not authorize or perform personal installation. Any future automated installer requires a separate approved Specification and Plan.

### 10. Language and source ownership

Release configuration, manifests, Skill instructions, generated prompts, checksums, validation contracts, and other machine- or model-consumed artifacts MUST remain in English.

User-facing documentation MAY be translated. The root README follows the approved Traditional-Chinese-first bilingual entry convention.

Canonical source MUST remain outside `dist/`. Generated files MUST state or make clear that they are generated and must not be edited directly.

## Edge cases and failure behavior

- Missing source Skill or modular prompt: stop before replacing a valid release.
- Duplicate Skill or unexpected runtime file: reject the package inventory.
- Release configuration version differs from package manifest version: stop with the conflicting fields.
- Core version differs from adapter compatibility declarations: fail conformance before packaging succeeds.
- Existing managed output from the same release: rebuild it safely and deterministically.
- Existing unmanaged output with a colliding name: stop without deleting it.
- Invalid Plugin manifest: reject the Codex package.
- Combined Generic prompt omits or reorders a required module: reject the Generic package.
- Checksum mismatch or ZIP content mismatch: reject the release.
- Interrupted or failed build: do not label partial staging output as a valid release.
- Unknown host capability: Generic behavior remains Conversation-only.
- Personal installation directory is present or discoverable: ignore it; build remains scoped to the repository.
- Unsupported provider name appears as an officially supported package: reject the support claim.

## Data, permissions, and external contracts

Release metadata and checksums are public project artifacts and MUST NOT contain secrets, credentials, private repository content, personal paths, or environment-specific tokens.

The build is authorized to read canonical project sources and to create or replace only configuration-declared outputs below repository `dist/`. It has no authority to modify user installation directories or external systems.

The Plugin manifest follows the Codex Plugin packaging contract. Each contained Skill continues to follow the Codex `SKILL.md` and `agents/openai.yaml` contracts.

ZIP archives and `checksums.sha256` are external release contracts. Consumers MUST be able to verify the archive hash without reading internal development state.

## Compatibility, rollout, and recovery

- Existing `core/`, Generic adapter, documentation conventions, scripts, tests, Skill invocation names, prompt IDs, Artifact formats, and Rule IDs remain compatible.
- The canonical Codex Skill source path changes from `adapters/codex/skills/` to `adapters/codex/plugin/grill-me/skills/`; conformance paths, rule mappings, migration inventory, tests, and documentation MUST move consistently, and no duplicate old source may remain.
- Existing direct source usage remains available during rollout.
- The first `2.1.0` build introduces new release outputs without changing a personal installation.
- Generated `dist/` may be discarded and rebuilt from canonical source at any time.
- If packaging validation fails, recovery is to preserve or restore canonical source and rebuild; generated output is not authoritative.
- Rollback from the release-layer change removes generated output and release-entry additions without changing core `2.0.0` semantics or previously validated adapter behavior.

## Constraints and assumptions

- Markdown remains the prompt and human-document format.
- JSON is the release configuration and Codex Plugin manifest format.
- YAML remains valid for existing adapter conformance manifests.
- SHA-256 is sufficient for integrity verification in this local source-release phase but is not a publisher signature.
- Build and validation must work without network access.
- Runtime package contents remain minimal and host-specific.
- The repository is not required to be a Python application or distributable Python package.
- Exact operating-system installation commands may differ, but documented source and destination semantics remain consistent.

## Acceptance criteria

- A new reader can open root `README.md` and choose Codex or Generic without first understanding repository internals.
- One build command using only Python's standard library produces unpacked `grill-me/`, versioned `generic-prompts-2.1.0/`, both reproducible versioned ZIP archives, and `checksums.sha256`.
- The Codex release is one valid `grill-me/` Plugin containing exactly the six approved Skills, with `$ai-dev-workflow` documented as the primary entry point and all six direct invocations preserved.
- The Plugin outer folder and manifest name both equal `grill-me`; `grill-me-2.1.0.zip` contains that root folder, and the former `adapters/codex/skills/` source no longer exists.
- The Generic release contains one generated self-contained prompt plus the seven source-equivalent modular prompts.
- The generated Generic prompt performs internal stage routing and retains Conversation-only claim limits.
- Package and release manifests consistently identify `grill-me`, display name `Grill Me — AI Development Workflow`, release `2.1.0`, and core `2.0.0`.
- No package contains development-only files.
- ZIP contents match their unpacked directories and both archive hashes match `checksums.sha256`.
- Two builds from unchanged source produce byte-identical ZIP archives and checksum content.
- Unknown `dist/` content survives unchanged or causes a safe collision failure; it is never silently removed.
- Existing 27 automated tests remain green, and new release-focused tests cover configuration, composition, package inventory, safety, reproducibility, and checksums.
- Both adapters pass shared conformance, all six Skills pass official validation, and the Plugin manifest passes its applicable validation.
- Documentation explains build and manual use without performing or implying personal installation.
- No marketplace publication, external upload, personal installation, or unsupported-provider release occurs.

## Deferred decisions

- Installer design and consent model.
- Marketplace metadata, publishing workflow, and release credentials.
- Release signing and provenance beyond checksums.
- Public license selection and third-party distribution terms.
- Additional language-specific detailed guides.
- Dedicated Claude Code, Gemini CLI, or other provider packages.
