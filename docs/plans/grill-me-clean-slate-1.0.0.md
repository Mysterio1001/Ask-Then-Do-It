# Grill Me Clean-slate 1.0.0 Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `grill-me-clean-slate-1-0-plan`

Workflow ID: `grill-me-clean-slate-1-0`

Target Core version: `1.0.0`

Status: Approved

Approval: Explicitly approved by the user on 2026-07-29 with the response `核准`.

## Inputs

- Approved [Grill Me Clean-slate 1.0.0 Specification](../specs/grill-me-clean-slate-1.0.0.md).
- Approved [Clean-slate Requirement Decision Record](../requirements/grill-me-clean-slate-1.0.0.md).
- Current locally validated eight-Skill and nine-prompt implementation.

## Planned outcome

Deliver the first truthful public source release identity `1.0.0`, remove all unpublished legacy version and migration material, provide one self-explanatory Codex package and one self-explanatory Generic package, make first use obvious, and prove the result with deterministic validation evidence without installing or publishing anything.

## Delivery strategy

Each Ticket delivers an observable capability across all necessary source, documentation, build, and test boundaries. Historical deletion is coupled to replacement validation in Ticket 1 so the project never treats removal alone as progress. Consumer documentation follows only after the final output paths exist. Provider packages then become independently understandable before final integration evidence is created.

All Tickets are sequential. Tickets 3 and 4 primarily own different provider areas, but both consume the same release configuration, generated checksum contract, root navigation, and package inventory assumptions. Sequential execution avoids accepting one provider package against a stale shared output set.

## Ticket 1 - Produce one clean 1.0.0 maintainer release base

Status: Completed — evidence: [Ticket 1 evidence](../evidence/grill-me-1.0.0-ticket-1.md).

### Outcome

A maintainer can inspect the active project, see one `1.0.0` contract with no obsolete migration or historical release line, and run one local command that produces current Codex and Generic package bases under the approved provider directories with one checksum file.

### Approved acceptance criteria covered

- Active Core, adapters, Plugin, release configuration, generated manifests, Specification, Plan, and new evidence use `1.0.0` where applicable.
- Obsolete releases, unpacked old packages, old checksums, old migration behavior, old snapshot protection, legacy output recognition, and superseded version artifacts are absent.
- `MIGRATE-V2-001` is absent from Core and both adapters while all non-migration workflow behavior remains.
- Stable canonical Specification and Plan locations replace v2/v3 naming.
- The build produces only the approved `dist/codex/`, `dist/generic/`, and current checksum layout.
- Unknown content and failed builds remain protected.

### In scope

- Add clean-slate inventory and stale-active-identity tests before removing old material.
- Add replacement regression coverage for every non-migration behavior currently protected by migration or historical snapshot suites.
- Rebase Core, both adapters, Plugin, release configuration, generated identities, and active artifact envelopes to `1.0.0`.
- Remove `MIGRATE-V2-001`, migration instructions, migration mappings, migration inventories, migration tests, and legacy release-overlap behavior.
- Remove unpublished old archives, old unpacked output, historical checksum snapshots, superseded Specifications, Plans, evidence, and version-specific fixtures from the approved active inventory.
- Establish final canonical Specification and Plan paths without v2 or v3 naming and repair all active links.
- Change managed release paths to the provider directories approved by the Specification.
- Preserve deterministic staging, collision protection, atomic replacement or rollback, ZIP generation, and current checksums.
- Record Ticket 1 evidence using actual `1.0.0` commands and outcomes.

### Out of scope

- Root consumer onboarding.
- Package-specific start guides.
- Codex manual-installation content.
- Generic immediate-start behavior.
- Final `1.0.0` release evidence or publication.
- Personal installation, marketplace work, Git initialization, or network operations.

### Dependencies

The Approved Clean-slate `1.0.0` Specification. This is the first implementation Ticket.

### Likely ownership areas

- `core/`
- `adapters/codex/` shared conformance and rule mappings
- `adapters/generic-prompts/manifest.yaml` and migration-related prompt content
- `release/release.json`
- `scripts/build_release.py`
- `scripts/validate_release_evidence.py`
- Canonical `docs/specs/`, `docs/plans/`, and replacement `docs/evidence/`
- Migration, conformance, adapter, release-contract, and release-safety tests
- Generated `dist/` outputs

### Test-first approach

1. Add a failing active-inventory test that identifies every obsolete version artifact, migration path, and historical output still present.
2. Add failing version-consistency tests requiring `1.0.0` across Core, adapters, Plugin, release configuration, and generated manifests.
3. Add failing rule-coverage tests requiring the clean catalog and both adapters to agree after removal of `MIGRATE-V2-001`.
4. Add failing build-contract tests for `dist/codex/`, `dist/generic/`, exact current archives, and a two-entry checksum file.
5. Add replacement non-migration regression tests before deleting old snapshot or migration suites.
6. Observe failures for the expected stale-version, legacy-inventory, migration, and output-layout reasons.
7. Implement the minimum coherent rebase and removal.
8. Refactor shared inventory and version checks without weakening independent assertions.

### Focused verification

- Run clean inventory, version identity, rule catalog, adapter mapping, release contract, and release safety tests.
- Build into an isolated workspace-owned output root and inspect exact provider directory and archive paths.
- Verify only two current archive hashes appear in the checksum file.
- Confirm unknown sentinel content survives and unmanaged collisions fail safely.

### Broader verification

- Run all Core, Codex, Generic, conformance, and retained workflow regression tests.
- Scan active source and documentation for stale supported identities and removed-path links, allowing only clean-slate traceability and negative fixtures.
- Confirm all eight Skills and nine Generic prompt sources remain present.

### Completion criteria

- The maintainer build base is consistently `1.0.0` and uses the approved provider output layout.
- No old release or migration artifact remains in the approved active inventory.
- Every removed test responsibility has current replacement coverage where behavior remains.
- No unknown file, personal environment, or external system was changed.
- Raw Red and Green outcomes appear in Ticket 1 evidence.

### Parallel safety

`No`. This Ticket changes the shared version contract, rule catalog, both adapter manifests, canonical artifact paths, release builder, output layout, and baseline test inventory consumed by every later Ticket.

## Ticket 2 - Let a source visitor choose the correct download immediately

Status: Completed — evidence: [Ticket 2 evidence](../evidence/grill-me-1.0.0-ticket-2.md).

### Outcome

A first-time visitor opening the source project can choose Codex or Generic from one Traditional Chinese start page and reach the correct current package and detailed guide without reading development internals or running Python.

### Approved acceptance criteria covered

- The root contains `START-HERE.zh-TW.md`.
- The first actionable choice distinguishes Codex from Generic use.
- Consumer instructions point to the one current package for each provider.
- README remains Traditional-Chinese-first and moves build instructions into a maintainer section.
- All current documentation links resolve and no removed path is presented as supported.

### In scope

- Create the root start guide with two concise paths and first-use summaries.
- Restructure README information hierarchy around consumer choice first and maintainer build second.
- Link the existing detailed Codex, Generic, beginner, and design guides without duplicating them.
- Update human documentation for the `1.0.0` identity and provider output paths.
- Add first-screen content, direct-path, language-order, maintainer-boundary, and relative-link tests.
- Record Ticket 2 evidence.

### Out of scope

- Adding package-internal start files.
- Changing Skill or Generic prompt behavior.
- Installing or publishing either package.
- Reworking the release builder established by Ticket 1 except for a proven documentation-path defect.

### Dependencies

Ticket 1 supplies stable `1.0.0` output paths and canonical documentation locations.

### Likely ownership areas

- Root `START-HERE.zh-TW.md`
- Root `README.md`
- `docs/guides/`
- `docs/design/` only when a stale identity or path must be corrected
- Documentation and link tests

### Test-first approach

1. Add a failing test requiring the root start file and two first-screen choices.
2. Add failing assertions that consumer steps contain no build prerequisite and resolve to the current package paths.
3. Add failing README-order tests requiring consumer navigation before maintainer build instructions.
4. Observe the expected missing-entry and stale-path failures.
5. Write the smallest complete start page and revise linked guides.
6. Refactor duplicated prose while preserving explicit provider boundaries.

### Focused verification

- Run documentation content and relative-link tests.
- Verify the first actionable instructions without scrolling into maintainer material.
- Verify every displayed package path exists after the Ticket 1 build.

### Broader verification

- Run release documentation and package-path tests.
- Scan Generic onboarding for Codex-only installation claims and scan Codex onboarding for unsupported automatic-install claims.

### Completion criteria

- A new visitor can choose a path in one page and reach an existing current package.
- No consumer path asks the user to understand source layout or run the builder.
- Maintainer build and validation remain discoverable but clearly separate.
- All relevant links and deterministic documentation checks pass.

### Parallel safety

`No`. This Ticket establishes shared root navigation and final public path terminology consumed by both package-specific start guides.

## Ticket 3 - Let a Codex user download and start one safe Plugin

Status: Completed — evidence: [Ticket 3 evidence](../evidence/grill-me-1.0.0-ticket-3.md).

### Outcome

A Codex user can download the only current Plugin ZIP, extract it, see a package-root Traditional Chinese start guide, follow safe manual installation boundaries, and begin with `$ai-dev-workflow` while retaining direct access to all eight Skills.

### Approved acceptance criteria covered

- Codex output uses the approved unpacked and archive paths with `grill-me/` as Plugin root.
- The package root contains `START-HERE.zh-TW.md`, a valid `1.0.0` Plugin manifest, and exactly eight Skills with valid UI metadata.
- The guide identifies the primary and advanced entry points and manual installation boundary.
- No installer, marketplace mutation, development-only file, or unrelated documentation appears in the package.
- The Plugin and all eight packaged Skills pass official validation.

### In scope

- Add the maintained Codex package start-guide source and deterministic packaging rule.
- Update Codex package inventory contracts to permit exactly the approved human guide in addition to runtime Plugin content.
- Update the detailed Codex guide for download, integrity verification, manual installation, first test, update boundary, and removal boundary.
- Add package/source equivalence, ZIP root, start-guide content, eight-Skill inventory, Plugin identity, and forbidden-file tests.
- Run official validation against the packaged Plugin and each packaged Skill.
- Record Ticket 3 evidence.

### Out of scope

- Automatic installation or updater scripts.
- Marketplace creation, mutation, cachebuster, or reinstall.
- Generic package behavior.
- Publication or external upload.

### Dependencies

Ticket 1 supplies the `1.0.0` package and builder contract. Ticket 2 supplies the public Codex route and terminology.

### Likely ownership areas

- Codex package start-guide source
- `adapters/codex/plugin/grill-me/`
- Codex section of release configuration or builder composition when required by the approved inventory
- `docs/guides/codex.zh-TW.md`
- Codex release, documentation, and validator integration tests
- Generated `dist/codex/`

### Test-first approach

1. Add a failing package inventory expectation for `START-HERE.zh-TW.md` at the Plugin root.
2. Add failing guide-content tests for the download, checksum, manual boundary, `$ai-dev-workflow`, and eight direct entries.
3. Add failing minimal-package tests for installers, marketplace files, evidence, tests, caches, and source-only material.
4. Observe the expected missing-guide failures.
5. Add the guide and the minimum deterministic builder support.
6. Refactor package-guide wording without adding runtime workflow instructions that belong in Skills.

### Focused verification

- Build only into an isolated output and compare the packaged guide with its canonical source.
- Validate the Plugin and all eight Skills with official validators.
- Verify the ZIP root and exact file inventory.
- Follow the start guide without executing installation commands.

### Broader verification

- Run Codex adapter, shared conformance, release safety, checksum, and documentation suites.
- Confirm no personal Codex or marketplace path was read or changed.

### Completion criteria

- One self-explanatory Codex ZIP passes all native and deterministic checks.
- The guide is sufficient to reach a manual first-use step without implying automatic installation.
- Package contents remain minimal and contain no unauthorized operation.
- Raw validation outcomes appear in Ticket 3 evidence.

### Parallel safety

`No`. Although provider-specific, this Ticket updates the combined release inventory and checksum-producing build consumed by the Generic package Ticket.

## Ticket 4 - Let a Generic user paste once and receive the first question

Status: Completed — evidence: [Ticket 4 evidence](../evidence/grill-me-1.0.0-ticket-4.md).

### Outcome

A Gemini or other general-language-model user can download the only current Generic ZIP, see a Traditional Chinese start guide beside `generic-workflow.md`, paste the workflow once with a request, and receive the first recommended high-impact requirement question immediately.

### Approved acceptance criteria covered

- Generic output uses the approved unpacked and archive paths and includes its package-root start guide.
- The package contains generated workflow and manifest plus nine byte-equivalent prompt sources.
- Fresh startup declares capability and stage concisely, then asks exactly one recommended question with its principal tradeoff.
- Fresh startup does not stop after status or ask the user to say "start".
- Resumed workflows route to the first unmet stage without unnecessary restart.
- Conversation-only evidence and persistence boundaries remain intact.

### In scope

- Add the maintained Generic package start-guide source and deterministic packaging rule.
- Update bootstrap, orchestration, or combined-workflow wrapper only as needed to enforce immediate startup.
- Update Generic guide instructions for one-paste use, first response, artifact saving, and resumption.
- Add package inventory, source equivalence, start-guide, fresh response, resumed response, one-question, recommendation, tradeoff, language, and capability-limit scenarios.
- Record Ticket 4 evidence.

### Out of scope

- Repository or Tools capability for Generic prompts.
- Claims of completed implementation, independent Review, persistence, or actual deletion.
- Codex packaging or installation.
- Dedicated provider-native integration.

### Dependencies

Ticket 1 supplies the Generic `1.0.0` package contract. Ticket 2 supplies shared navigation. Ticket 3 stabilizes the combined two-package inventory and checksum behavior.

### Likely ownership areas

- Generic package start-guide source
- `adapters/generic-prompts/bootstrap.md`
- `adapters/generic-prompts/orchestration.md`
- Generic combined-workflow composition
- `docs/guides/generic.zh-TW.md`
- Generic scenario, package, documentation, and release integration tests
- Generated `dist/generic/`

### Test-first approach

1. Add a failing package inventory expectation for the Generic start guide.
2. Add a failing fresh-workflow transcript expectation in which the current behavior only reports status or defers interrogation.
3. Require exactly one question, a recommended answer, principal tradeoff, and user-language response.
4. Add regression cases for resumed artifacts, direct module selection, Conversation-only claims, and user-owned persistence.
5. Observe the expected missing-guide or deferred-start failures.
6. Implement the smallest prompt and composition changes.
7. Refactor repeated startup wording without weakening modular prompt independence.

### Focused verification

- Build and inspect the Generic package and combined source order.
- Compare all nine packaged prompt files byte-for-byte with canonical source.
- Run fresh, resumed, direct-selection, and limited-capability scenarios.
- Verify the first effective fresh response contains exactly one question.

### Broader verification

- Run all Generic adapter, shared conformance, release composition, documentation, checksum, and safety tests.
- Confirm no Generic content instructs automatic external or personal-environment mutation.

### Completion criteria

- One self-explanatory Generic ZIP passes exact inventory and composition checks.
- One paste plus one request starts useful interrogation immediately.
- Existing approval gates, routing, artifacts, and Conversation boundaries remain green.
- Raw scenario outcomes appear in Ticket 4 evidence.

### Parallel safety

`No`. This Ticket changes the final Generic prompt behavior and the same combined release checksum set that must be validated after the Codex package is stable.

## Ticket 5 - Prove the first public-source 1.0.0 release

Status: Completed — evidence: [Release 1.0.0 evidence](../evidence/grill-me-release-1.0.0.md).

### Outcome

A maintainer or reviewer can build twice from unchanged source, verify both self-explanatory packages and their checksums, inspect complete release evidence, and confirm that the project neither retains an obsolete active version nor performs any installation or publication.

### Approved acceptance criteria covered

- Every required automated, native, conformance, documentation, safety, reproducibility, ZIP, checksum, architecture, Review, and evidence-gate check passes.
- Two clean builds are byte-identical.
- Both archives match their unpacked directories.
- The current checksum file covers exactly two archives.
- Completed evidence exists only after all configured checks pass.
- No installation, marketplace mutation, publication, upload, network operation, or unsupported-provider claim occurs.

### In scope

- Run the complete clean-slate test suite and both adapter conformance checks.
- Run official validation for all eight packaged Skills and the Plugin.
- Build twice into clean isolated workspace paths and compare archive and checksum bytes.
- Compare every ZIP entry byte-for-byte with its unpacked package file.
- Verify both SHA-256 entries and exact package inventories.
- Run stale-active-identity, removed-artifact, placeholder, cache, and development-file scans.
- Perform a read-only release milestone architecture diagnosis with all twelve lenses and simulated deletion analysis.
- Perform a final Review labeled with its actual independence level.
- Create machine-readable and human-readable `1.0.0` release evidence only after every required result passes.
- Remove test-only dependencies, temporary builds, caches, and bytecode while preserving final release output.

### Out of scope

- Personal installation or installation testing that mutates a user environment.
- Marketplace configuration, cachebuster, publication, upload, remote release, Git tag, or signing.
- Fixing unrelated issues or implementing deferred architecture proposals.

### Dependencies

Tickets 1-4.

### Likely ownership areas

- All validation suites
- Final generated `dist/`
- `docs/evidence/` current Ticket and release evidence
- Release evidence validation ledger and gate
- Root and package documentation only for proven final-path defects

### Test-first approach

Use the Approved Specification acceptance criteria as the integration matrix. Add a focused failing test before any source fix for an uncovered deterministic criterion. Do not create completed release evidence during any failed or blocked state.

### Focused verification

- Run package inventories, start-guide checks, fresh Generic startup, checksums, ZIP equivalence, and evidence-gate tests.
- Validate all packaged Codex Skills and the Plugin.
- Run both shared conformance commands.

### Broader verification

- Run the complete automated suite.
- Build twice and compare raw bytes.
- Inspect the final source and generated inventories for removed history and forbidden files.
- Validate all current documentation links.
- Confirm temporary and cache cleanup without touching final output.

### Completion criteria

- Every Approved acceptance criterion has direct automated, raw-command, or explicitly labeled diagnostic evidence.
- No failed, blocked, missing, duplicate, or unknown required check remains.
- Both consumer packages are current, self-explanatory, reproducible, checksum-verifiable, and minimal.
- The final project contains no obsolete active version or migration contract.
- Final evidence truthfully records limitations and confirms that no external or personal state changed.

### Parallel safety

`No`. This is the final sequential integration and release-proof Ticket across every shared contract and output.

## Dependency order

1. Ticket 1: Clean `1.0.0` maintainer release base.
2. Ticket 2: Root consumer choice.
3. Ticket 3: Self-explanatory Codex package.
4. Ticket 4: Self-explanatory, immediate-start Generic package.
5. Ticket 5: Final validation and release evidence.

No parallel implementation group is proposed.

## Cross-ticket constraints

- Begin every reasonably testable behavior with an observed failing test for the intended missing behavior.
- Do not delete an old test until equivalent retained behavior has replacement coverage.
- Limit deletion to paths explicitly classified by the Approved Specification and this Plan; preserve unknown content.
- Keep canonical model- and machine-consumed artifacts in English and human onboarding Traditional-Chinese-first.
- Treat `dist/` as generated output and canonical source as authoritative.
- Do not create completed `1.0.0` release evidence before every configured required check passes.
- Do not install, update, remove, publish, upload, configure a marketplace, initialize Git, or use the network.
- Do not implement a diagnostic architecture proposal without a separate Approved Specification and Plan.

## Assumptions

- Existing test infrastructure can be replaced incrementally without losing non-migration behavioral coverage.
- The approved clean-slate deletion scope is sufficient; any uncertain file returns to Specification rather than being removed by guesswork.
- Exact internal helper placement may change during implementation when public behavior, safety boundaries, and one-level discoverability remain intact.

## Deferred decisions

- Git and public release infrastructure.
- Historical binary retention after an actual public version exists.
- Automatic installer and update behavior.
- Marketplace publication and cachebuster flow.
- Additional human-language package guides.
- Dedicated provider-native packages and signing beyond SHA-256.

## Handoff

After explicit approval, this Plan authorizes sequential implementation beginning with Ticket 1 under TDD. It does not authorize personal installation, marketplace mutation, publication, upload, Git operations, network access, or work outside the specified Tickets.

## Plan approval gate

This complete Ticket Plan was explicitly approved by the user on 2026-07-29 with the response `核准`. The approval authorizes sequential implementation beginning with Ticket 1 under TDD and does not broaden any external or personal-environment authority.
