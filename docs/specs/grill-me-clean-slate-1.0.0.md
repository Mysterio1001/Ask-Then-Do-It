# Grill Me Clean-slate 1.0.0 Specification

Artifact type: Specification

Artifact ID: `grill-me-clean-slate-1-0-spec`

Workflow ID: `grill-me-clean-slate-1-0`

Target Core version: `1.0.0`

Status: Approved

Approval: Explicitly approved by the user on 2026-07-29 with the response `核准`.

## Inputs

- Approved [Clean-slate 1.0.0 Requirement Decision Record](../requirements/grill-me-clean-slate-1.0.0.md).
- Current locally validated repository behavior as of 2026-07-29.
- Explicit user confirmation that the project has never been published and has no users or compatibility commitments.

## Problem

The active repository represents an unpublished product as though it has multiple released generations. Old Specifications, Plans, evidence, migration behavior, release archives, unpacked packages, checksum snapshots, and v2/v3 version labels increase repository size and create false compatibility obligations. The root experience also leads with a maintainer build command before the two consumer choices, while the downloadable packages do not carry an immediately visible human start guide.

The first public release needs one truthful identity, two obvious downloads, self-contained onboarding, and a smaller active contract without losing the current validated development workflow.

## Goals

- Define the current complete product as the first stable release `1.0.0`.
- Give every active component and generated package one consistent `1.0.0` identity.
- Remove obsolete version history and migration behavior from the active project.
- Present one Codex download and one Generic download as the only consumer choices.
- Make each package understandable after offline extraction.
- Make Generic start productive work immediately after one paste.
- Preserve all current non-migration workflow gates, artifacts, routing, TDD, review, project-knowledge, and architecture-diagnosis behavior.
- Keep release construction deterministic, minimal, safe, and independently verifiable.

## Non-goals

- Preserve pre-release binaries, version histories, migration support, or rollback copies in the active repository.
- Add an automatic installer, updater, marketplace entry, or personal-environment mutation.
- Publish, upload, sign, or host the release.
- Initialize Git or create tags.
- Add provider-native support beyond Codex and Generic.
- Redesign the model-neutral development workflow beyond removal of migration behavior and the Generic first-response requirement.
- Translate canonical model- or machine-consumed contracts.

## Users and scenarios

### New Codex user

The user obtains one `grill-me-1.0.0.zip`, extracts it, sees a Traditional Chinese start file at the Plugin root, follows manual installation instructions, and begins with `$ai-dev-workflow`. The user may invoke any of the eight Skills directly when desired.

### New Generic user

The user obtains one `generic-prompts-1.0.0.zip`, extracts it, sees a Traditional Chinese start file beside `generic-workflow.md`, pastes the complete workflow once, supplies a request, and receives the first high-impact requirement question without another start command.

### Source visitor

The visitor opens the root Traditional Chinese start file, chooses a supported runtime path, and does not need to inspect Core, adapter, test, release, or evidence internals.

### Maintainer

The maintainer edits canonical source, runs one documented local build, obtains exactly two current release packages plus checksums, runs validation, and records completed evidence only after every required check passes.

### Release reviewer

The reviewer can prove exact package inventory, source traceability, version consistency, prompt composition, native validity, conformance, reproducibility, ZIP equivalence, checksums, documentation links, and absence of obsolete active artifacts.

## Terminology

- **Clean-slate**: the deliberate removal of unpublished historical version identities and compatibility behavior so the existing product becomes the first public release.
- **Active project**: canonical source, tests, human documentation, current plans and evidence, release configuration, and generated current output maintained after the clean-slate change.
- **Consumer package**: one runtime ZIP intended for a Codex or Generic user, distinct from the maintainer source repository.
- **Start guide**: a human-facing `START-HERE.zh-TW.md` that explains the shortest safe path to first use.
- **Current behavior**: the validated eight-Skill, nine-prompt workflow excluding v2 migration and including the new Generic immediate-start requirement.

## Required behavior

### 1. Clean version identity

The product release, model-neutral Core, Codex adapter, Generic adapter, Codex Plugin, generated Generic manifest, current Specification, current Ticket Plan, and current release evidence MUST identify version `1.0.0` where a version is required.

The active project MUST NOT present `2.0.0`, `2.1.0`, or `3.0.0` as a current or historical supported release. Old version strings MAY appear only in dedicated negative test fixtures or in the Approved clean-slate traceability records whose explicit purpose is to describe their removal; they MUST NOT appear as an active identity or supported path.

The clean-slate change MUST be described as the first public release, not as a public downgrade from v3.

### 2. Historical artifact and migration removal

The active project MUST remove unpublished historical release archives, unpacked historical packages, historical checksum files, superseded versioned Specifications, superseded Plans, superseded implementation and release evidence, old snapshot fixtures, migration inventories, migration tests, legacy release-output recognition, and v2 first-use migration instructions.

`MIGRATE-V2-001` MUST be removed from the Core rule catalog and from every adapter rule mapping and conformance manifest. No adapter may claim automatic v2-to-v1.0.0 migration.

Removal of migration behavior MUST NOT remove Project Knowledge Base, Draft Working Notes, documented requirement interrogation, automatic routing, the twelve lenses, architecture diagnosis, simulated deletion safety, Specification, vertical Ticket Planning, TDD, or Review behavior.

### 3. Source and consumer entry separation

The source repository MUST be described as the maintainer and validation workspace. Consumer documentation MUST direct ordinary users to one of two generated ZIPs rather than requiring them to understand or build the source repository.

The repository root MUST contain `START-HERE.zh-TW.md`. Its first actionable choice MUST distinguish:

- Codex Plugin usage.
- Gemini or another general language model through Generic prompts.

The root `README.md` MUST keep Traditional Chinese first, link to the root start guide, identify the two consumer paths, and move source-building details into a clearly maintainer-oriented section.

### 4. Codex consumer package

The Codex release outputs MUST be:

- Unpacked Plugin at `dist/codex/grill-me/`.
- Archive at `dist/codex/grill-me-1.0.0.zip` with `grill-me/` as its archive root.

The Plugin package MUST contain:

- `.codex-plugin/plugin.json` with package name `grill-me` and version `1.0.0`.
- `START-HERE.zh-TW.md` at the Plugin root.
- Exactly these eight Skill directories: `ai-dev-workflow`, `grill-requirements`, `grill-with-docs`, `write-spec`, `plan-tickets`, `implement-tdd`, `review-code`, and `improve-architecture`.
- Each Skill's required instructions and valid UI metadata.

The start guide MUST identify `$ai-dev-workflow` as the primary entry, explain that all eight Skills remain directly callable, and state that installation is manual.

The package MUST NOT contain an installer, marketplace mutation, source tests, Core source, development evidence, Plans, Specifications, caches, or unrelated documentation.

### 5. Generic consumer package

The Generic release outputs MUST be:

- Unpacked package at `dist/generic/generic-prompts-1.0.0/`.
- Archive at `dist/generic/generic-prompts-1.0.0.zip` with `generic-prompts-1.0.0/` as its archive root.

The Generic package MUST contain:

- `START-HERE.zh-TW.md` beside the primary entry.
- Generated `generic-workflow.md`.
- Generated `manifest.yaml` identifying release and Core `1.0.0`, Generic adapter identity, Conversation capability, and all source prompts.
- A `prompts/` directory containing the nine canonical Generic Markdown prompt sources.

The start guide MUST tell the user to paste `generic-workflow.md` once, supply the request and available artifacts, and save emitted Markdown artifacts when cross-session persistence matters.

The package MUST remain Conversation-only and MUST NOT claim repository access, file mutation, command execution, completed TDD, independent Review, actual deletion experiments, or durable persistence without proven host capability.

### 6. Generic immediate startup

For a fresh workflow, the first effective model response after receiving the combined workflow and a user request MUST:

- Declare the proven capability and selected stage concisely.
- Route to the first unmet stage.
- Ask exactly one high-impact requirement question in the user's language.
- Include a recommended answer.
- Include the principal tradeoff.

The response MUST NOT end after capability inventory, workflow status, a future-tense promise to interrogate, or an instruction for the user to say "start".

For a resumed workflow, the adapter MUST validate supplied artifacts and route to the first unmet stage without restarting requirement interrogation unnecessarily.

### 7. Distribution layout and managed outputs

Generated release output MUST use only these consumer-facing areas:

- `dist/codex/`
- `dist/generic/`
- `dist/checksums.sha256`

The active distribution MUST NOT contain `current/`, `archive/`, multiple release versions, a historical checksum snapshot, or top-level duplicate package copies.

`dist/checksums.sha256` MUST cover exactly the two current distributable archives. Generated directories and archives MUST contain equivalent relative files and byte content.

The build MUST stage and validate complete output before replacement. Unknown content or an unmanaged collision MUST stop the build without deleting or overwriting it.

### 8. Canonical artifact reset

The final active Specification and Ticket Plan MUST use stable canonical documentation locations without v2 or v3 naming. Release-specific evidence MAY include `1.0.0` in its filename.

Current validation evidence MUST be recreated from actual clean-slate commands and outcomes. Historical evidence MUST NOT be mechanically relabeled as `1.0.0` without rerunning the represented checks.

No stale internal link may point to a removed Specification, Plan, evidence record, migration file, package path, or old version.

### 9. Language and documentation ownership

Canonical Core, prompts, Skill instructions, manifests, Specifications, Plans, rule catalogs, validation contracts, and machine-readable evidence MUST remain English.

Human-facing start guides and detailed usage guides MAY use Traditional Chinese. The root entry MUST remain Traditional-Chinese-first.

The package start guides MUST be short consumer instructions, not duplicated design documents. Detailed design, development process, and validation evidence remain outside runtime packages.

### 10. Validation and release evidence

The `1.0.0` release MUST be rejected unless all applicable checks pass:

- Clean active-inventory and stale-version scans.
- Core rule-catalog and both adapter conformance validation.
- Existing non-migration workflow regression tests.
- Generic fresh and resumed startup scenarios.
- Exact Codex and Generic package inventory tests.
- Official validation of all eight packaged Codex Skills.
- Plugin manifest and package validation.
- Generic combined-workflow composition and Conversation-limit tests.
- Documentation content and relative-link checks.
- Collision safety and failed-build preservation.
- Two unchanged clean builds with byte-identical archives and checksum content.
- ZIP-to-directory byte equivalence.
- SHA-256 verification for both current archives.
- Release milestone architecture diagnosis.
- A final Review labeled honestly for its independence level.

A failed, missing, duplicated, unknown, or blocked required check MUST prevent successful completed release evidence.

## Edge cases and failure behavior

- If an old version string remains as an active identity or supported path, reject completion and identify the file. Negative stale-version fixtures and Approved clean-slate traceability records are the only exceptions.
- If an old artifact cannot be classified safely, stop and request review rather than deleting an unrelated file.
- If an old link remains after artifact removal, documentation validation fails.
- If either package contains an unexpected file or omits its start guide, reject that package.
- If the Plugin root, manifest name, and configured package identity differ, stop the build.
- If Generic prompt order changes or the combined entry omits a source, reject the package.
- If a fresh Generic response does not ask one recommended question, the startup scenario fails.
- If current output already exists and validates, replace it only after a new staged output validates completely.
- If current output collides with unmanaged content, preserve it and stop with an actionable path.
- If checksum or ZIP equivalence fails, create no completed release evidence.
- If the host cannot perform a claimed action, downgrade the claim according to the existing capability contract.
- If the user supplies old workflow artifacts, do not claim an automatic compatibility migration that the clean-slate product no longer supports.

## Data, permissions, and external contracts

The project may delete only old-version paths explicitly authorized by an Approved Ticket Plan derived from this Specification. It MUST preserve unknown and unrelated user content.

The build is authorized to read canonical repository source and write only configured generated release targets under `dist/`. It has no authority over personal Codex storage, marketplace configuration, model accounts, external services, or release hosts.

Package manifests, checksums, prompts, and public documentation MUST contain no credentials, private paths, personal identifiers, or environment-specific tokens.

The Plugin manifest, Skill folders, Generic manifest, package inventories, and checksums remain external technical contracts. The package start guides are public human contracts.

## Compatibility, rollout, and recovery

This is an intentionally breaking pre-publication clean reset. No compatibility period, redirect, archive directory, or old binary preservation is required because no user or external consumer exists.

Implementation MUST remove historical active artifacts only after the new Specification and Ticket Plan are approved. Deletion and replacement MUST occur within the repository scope and remain test-first where behavior is reasonably testable.

The new `1.0.0` release becomes authoritative only after every required validation passes. Until then, no completed `1.0.0` release evidence may exist.

Generated output MAY be discarded and rebuilt from canonical source. The active canonical source and Approved `1.0.0` artifacts are the recovery source. There is no in-repository rollback guarantee for removed unpublished versions.

Future published versions SHOULD store historical binaries in a tag, release service, or external archive rather than the active source distribution tree. That future retention mechanism is not part of this Specification.

## Constraints and assumptions

- The project is currently local and is not a Git repository.
- No public release, user installation, external integration, or compatibility promise exists.
- Python and the existing standard-library release builder remain available to maintainers.
- Markdown remains the workflow and human-document format.
- JSON remains the release and Plugin manifest format; YAML remains the shared adapter and rule format.
- SHA-256 remains sufficient for local integrity verification but is not a publisher signature.
- The current eight Skills and nine Generic prompt sources are the intended first public feature set.
- Human onboarding is Traditional-Chinese-first; canonical model contracts remain English.
- Runtime packages remain small even after adding one package-specific human start guide.

## Acceptance criteria

- A source visitor sees `START-HERE.zh-TW.md` at the root and can choose Codex or Generic without reading development internals.
- The active project has one truthful `1.0.0` identity across Core, adapters, Plugin, release, generated manifests, current Specification, current Plan, and current evidence.
- No obsolete binary, unpacked old package, old checksum, old migration rule, migration test, historical version artifact, stale active version label, or legacy release logic remains.
- The current mandatory rule catalog and both adapters agree after removing `MIGRATE-V2-001`.
- One build produces only `dist/codex/grill-me/`, `dist/codex/grill-me-1.0.0.zip`, `dist/generic/generic-prompts-1.0.0/`, `dist/generic/generic-prompts-1.0.0.zip`, and `dist/checksums.sha256` as managed release outputs.
- Both unpacked packages and archives include a visible `START-HERE.zh-TW.md`.
- The Codex Plugin contains exactly eight valid Skills, identifies `1.0.0`, and documents manual use beginning with `$ai-dev-workflow`.
- The Generic package contains its start guide, combined workflow, manifest, and nine modular prompt files, all identifying Core and release `1.0.0` where applicable.
- A fresh Generic request receives capability and stage context plus exactly one recommended high-impact question and its principal tradeoff in the first effective response.
- All required automated, native, conformance, documentation, safety, reproducibility, ZIP, checksum, evidence-gate, architecture, and Review checks pass.
- Completed `1.0.0` evidence contains raw commands and outcomes and is rejected when any configured required check is not passed.
- No personal installation, marketplace mutation, publication, upload, network operation, or unsupported-provider support claim occurs.

## Deferred decisions

- Public release hosting and download-page implementation.
- Git initialization, tags, and historical binary retention after a real public release.
- Automated Codex installation, update, and removal.
- Marketplace publication and cachebuster behavior.
- Additional human-language start guides.
- Dedicated native adapters for Gemini CLI, Claude Code, or other platforms.
- Signing and provenance beyond SHA-256.

## Handoff

After explicit approval, this Specification authorizes creation of a separate Draft vertical Ticket Plan. It does not authorize implementation, deletion, version replacement, release building, installation, or publication.

## Specification approval gate

This complete Specification was explicitly approved by the user on 2026-07-29 with the response `核准`. The approval authorizes creation of a separate Draft vertical Ticket Plan. It does not authorize implementation until that Ticket Plan is explicitly approved.
