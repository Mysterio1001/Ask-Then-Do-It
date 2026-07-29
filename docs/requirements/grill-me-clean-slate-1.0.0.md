# Grill Me Clean-slate 1.0.0 Requirement Decision Record

Artifact type: Requirement Decision Record

Artifact ID: `grill-me-clean-slate-1-0-requirements`

Workflow ID: `grill-me-clean-slate-1-0`

Target Core version: `1.0.0`

Status: Approved

## Problem and desired outcome

The project has never been published and has no users, external consumers, or compatibility commitments, but the active repository presents internal v1, v2, v3, and release `2.1.0` history. A person downloading the source can see development structure, multiple generated versions, historical evidence, and maintainer-oriented build instructions before finding the correct entry point.

The desired outcome is a clean first public release named `1.0.0`. The active project must expose one current Codex package, one current Generic package, clear Traditional Chinese start instructions, and no obsolete distribution or migration history.

## Users and success signals

### First-time Codex user

- Sees one Codex download.
- Finds `START-HERE.zh-TW.md` after extraction.
- Understands that installation is manual and begins with `$ai-dev-workflow`.

### First-time Generic model user

- Sees one Generic download.
- Finds `START-HERE.zh-TW.md` and `generic-workflow.md` after extraction.
- Pastes the workflow once and receives the first requirement question in the model's first effective response.

### Maintainer

- Edits canonical source rather than generated output.
- Produces both `1.0.0` packages with one deterministic build.
- Sees no legacy `current/`, `archive/`, v2, v3, or `2.1.0` distribution path in the active project.

### Reviewer

- Can verify versions, package inventories, checksums, conformance, native validation, reproducibility, and successful release evidence.

## Scope

- Treat the current complete product behavior as the first stable release `1.0.0`.
- Set Core, Codex adapter, Generic adapter, Plugin, release, generated manifests, and current artifacts to `1.0.0`.
- Remove old release binaries, unpacked outputs, checksum snapshots, historical version artifacts, snapshot tests, migration rules, migration tests, and legacy release migration logic.
- Remove `MIGRATE-V2-001` while retaining all non-migration current workflow behavior.
- Replace active v2/v3 naming with stable canonical names or `1.0.0` release-evidence names.
- Add a root `START-HERE.zh-TW.md` and one package-specific `START-HERE.zh-TW.md` to each downloadable ZIP.
- Make the source repository maintainer-facing and the two release ZIPs consumer-facing.
- Use only `dist/codex/`, `dist/generic/`, and `dist/checksums.sha256` for generated distribution output.
- Make a fresh Generic workflow start interrogation immediately rather than ending after status declaration.
- Re-run and recreate trustworthy `1.0.0` validation and release evidence.

## Non-goals

- Publish or upload a release.
- Create a Git repository, tag, or remote release.
- Install, update, or remove a personal Codex Plugin.
- Create or mutate a marketplace.
- Add an automatic installer or updater.
- Add another provider-native adapter.
- Add product behavior unrelated to distribution clarity, clean version identity, or Generic startup.
- Preserve an in-repository rollback copy of pre-release versions.

## Primary behavior and user flow

### Source visitor

1. Open `START-HERE.zh-TW.md` at the repository root.
2. Choose Codex or Generic without learning the internal source layout.
3. Follow a direct link to the matching current package or detailed guide.

### Codex consumer

1. Download `grill-me-1.0.0.zip`.
2. Extract one `grill-me/` Plugin root.
3. Read the included Traditional Chinese start file.
4. Follow manual Plugin and marketplace instructions under explicit user control.
5. Begin a new task with `$ai-dev-workflow`; retain direct access to all eight Skills.

### Generic consumer

1. Download `generic-prompts-1.0.0.zip`.
2. Read the included Traditional Chinese start file.
3. Paste the complete `generic-workflow.md` once and provide the request.
4. Receive a concise capability and stage declaration plus exactly one high-impact requirement question, its recommended answer, and its principal tradeoff.

### Maintainer

1. Edit canonical Core, adapter, documentation, or release configuration source.
2. Run the documented build.
3. Obtain exactly one current package for each supported path and one checksum file.
4. Run all required validation before creating completed `1.0.0` evidence.

## Edge cases and failure behavior

- A stale active `2.0.0`, `2.1.0`, or `3.0.0` version declaration must fail the clean-slate validation, except when a test fixture explicitly proves stale-version rejection.
- A stale v1, v2, or v3 active Specification, Plan, release artifact, evidence record, migration rule, or migration test must fail the current-project inventory check.
- Unrelated user content must not be deleted merely because its name resembles an old artifact.
- A generated-output collision must stop without presenting partial output as a valid release.
- A package missing its start file, primary entry, manifest, Skill, or declared prompt must fail inventory validation.
- A Generic fresh response that only reports status or asks the user to say "start" must fail the startup scenario.
- A failed or blocked required validation must prevent completed `1.0.0` release evidence.
- User-supplied old workflow artifacts receive no claimed automatic migration after migration support is removed.

## Data, dependencies, security, privacy, and operational constraints

- The build remains local, deterministic, standard-library-only, and network-free.
- Distribution packages contain public workflow instructions and no credentials, private paths, caches, tests, or development evidence.
- Package start guides are human-facing Traditional Chinese documents.
- Canonical Core, Skill, prompt, manifest, Specification, Plan, rule, and validation contracts remain English.
- Personal installations, marketplaces, accounts, external services, and release hosts remain outside repository authority.
- Deletion during implementation is limited to explicitly approved old-version project paths and must not expand to unknown content.

## Acceptance criteria

- The active project identifies the current product, Core, both adapters, and release as `1.0.0`.
- No obsolete release output, checksum snapshot, migration behavior, or old-version artifact remains in the approved active inventory.
- The root start file directs a first-time user to exactly one Codex path or one Generic path.
- Both ZIPs include `START-HERE.zh-TW.md` at an immediately visible package location.
- The Codex package contains exactly the valid Plugin manifest, eight Skills and their UI metadata, and its start guide.
- The Generic package contains its start guide, generated combined workflow, generated manifest, and nine source-equivalent prompt files.
- A fresh Generic workflow asks the first recommended requirement question in its first effective response.
- `dist/` contains only the approved Codex directory and ZIP, Generic directory and ZIP, and current checksum file under the agreed provider directories.
- All automated tests, official Skill checks, Plugin validation, both adapter conformance checks, reproducibility checks, ZIP equivalence, checksums, documentation links, and evidence gate pass.
- No installation, marketplace mutation, publication, upload, or network operation occurs.

## Confirmed decisions

- Complete clean-slate rather than preserving a visible historical version line.
- First public version `1.0.0` for all active components.
- No user or compatibility obligation exists.
- Two consumer downloads; source repository for maintainers.
- Human start file inside both packages.
- Manual Codex installation only.
- Immediate Generic interrogation after one paste.
- No `current/` or `archive/` distribution layer.
- Future historical binaries belong in a tag, release platform, or external archive rather than the active project.

## Assumptions

- The current eight-Skill and nine-prompt behavior is the intended first public product, except for removal of old migration behavior and the strengthened Generic startup response.
- Traditional Chinese remains the primary human onboarding language.
- The absence of Git history is accepted for this local clean-slate change.

## Deferred decisions

- Public hosting and release-page design.
- Git repository initialization, tags, and long-term archive policy.
- Automated installer and update behavior.
- English or additional translated package start guides.
- Dedicated Gemini CLI, Claude Code, or other provider-native packages.
- Signing and provenance beyond SHA-256.

## Explicit consensus evidence

The user explicitly approved this Requirement Decision Record on 2026-07-29 with the response `核准`, after adopting each recommended clean-slate, distribution, package-guide, manual-installation, Generic-startup, and simplified-output decision in separate one-question turns.

## Handoff

This Approved Requirement Decision Record authorizes a Draft behavioral Specification. It does not authorize deletion, version changes, package rebuilding, Ticket Planning, or implementation.
