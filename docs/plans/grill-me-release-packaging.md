# Grill Me Release Packaging - Implementation Plan

Artifact type: Ticket Plan

Artifact ID: `grill-me-release-packaging-plan`

Workflow ID: `grill-me-release-2-1`

Core version: `2.0.0`

Status: Approved

Specification: [Grill Me Release Packaging Specification](../specs/grill-me-release-packaging.md)

Specification status: Approved

## Inputs

- Approved Grill Me Release Packaging Specification and its recorded approval evidence.
- Approved Portable AI Development Workflow v2 Specification.
- Existing validated Generic prompts and Codex adapter sources.
- Existing 27-test core and adapter baseline.

## Assumptions

- `adapters/` remains the only editable adapter source, with the Codex Plugin rooted at `adapters/codex/plugin/grill-me/`.
- Release-focused tests may build into isolated workspace-owned temporary output before the final `dist/` integration build.
- Codex Plugin scaffolding and validation will follow the installed `plugin-creator` instructions applicable at implementation time.
- Existing Skill trigger descriptions and `agents/openai.yaml` metadata remain compatible unless Plugin validation proves a required change.

## Deferred

- Personal installation, automatic installers, marketplace publication, external uploads, signing, public licensing, and new provider adapters.

## Handoff

Begin Ticket 1 with the `tools` profile and TDD. Implement all Tickets in the approved dependency order.

## Approval

Re-approved by the user on 2026-07-28 through the explicit response `OK`. This approval applies to the corrected `grill-me` Plugin root, sequential Ticket dependency order, and stated implementation boundaries.

## Ticket 1 - Build one validated Codex Plugin release slice

### Outcome

A maintainer can run the release builder against canonical source and obtain one minimal, versioned Codex Plugin directory, matching reproducible ZIP, and checksum entry containing exactly the six approved Skills.

### Acceptance criteria covered

- `release/release.json` is the single editable release configuration and declares package ID `grill-me`, display name `Grill Me — AI Development Workflow`, release `2.1.0`, and core `2.0.0`.
- `adapters/codex/plugin/grill-me/.codex-plugin/plugin.json` is valid for the supported Codex Plugin format, and both outer folder and manifest name equal `grill-me`.
- The six canonical Skill directories move to `adapters/codex/plugin/grill-me/skills/`, all references resolve, and `adapters/codex/skills/` no longer remains.
- One Codex Plugin contains exactly six Skills and preserves their direct invocation names.
- The generated Codex runtime package excludes development-only content.
- The Codex directory, ZIP, manifest identities, and checksum entry agree.
- The builder uses only the Python standard library and stays within a caller-selected output root.

### In scope

- Initial versioned release configuration and schema validation.
- Codex Plugin source root and manifest.
- Atomic canonical Skill-source migration into the `grill-me` Plugin root, including conformance, rule-mapping, migration-inventory, test, and internal path updates.
- The smallest release-builder path required to build the Codex package end to end.
- Deterministic file ordering and normalized ZIP metadata for the Codex archive.
- Codex package inventory, ZIP-equivalence, identity, and checksum tests.
- Safe resolution of the selected output root and Codex managed targets.

### Out of scope

- Generic combined prompt and Generic package.
- Cross-package collision, interrupted-build, and final reproducibility hardening beyond the Codex slice.
- Root README and usage-guide changes.
- Personal installation or publication.

### Dependencies

None beyond the Approved Specification and current validated Codex adapter.

### Likely ownership areas

- `release/release.json`
- `adapters/codex/plugin/grill-me/.codex-plugin/plugin.json`
- `adapters/codex/plugin/grill-me/skills/`
- Former `adapters/codex/skills/` migration source
- `adapters/codex/conformance.yaml`
- `adapters/codex/rule-mapping.yaml`
- `adapters/codex/migration-inventory.yaml`
- `scripts/build_release.py`
- New release-focused tests and fixtures under `tests/release/`

### Test-first approach

1. Add contract tests for the required release identity, matching `grill-me` folder and manifest names, the sole new canonical six-Skill path, minimal package content, ZIP root and equivalence, and checksum entry.
2. Add a public build-command scenario that targets an isolated workspace-owned output directory.
3. Run the focused suite and observe the expected red because release configuration, Plugin manifest, builder, and artifacts are absent.
4. Use `plugin-creator` guidance to create the minimal valid Plugin source and implement the smallest Codex build path that satisfies the tests.
5. Refactor only after the focused suite is green, then rerun it.

### Focused verification

- Run the release configuration and Codex package tests.
- Validate the Plugin manifest with the applicable Codex-native check.
- Run the official Skill validator for all six packaged Skills.
- Compare packaged Skill content byte-for-byte with canonical source under `adapters/codex/plugin/grill-me/skills/`.
- Confirm every conformance, rule-mapping, migration, test, and documentation reference resolves after the source move.

### Broader verification

- Run existing Codex adapter tests and shared conformance validation.
- Run existing core conformance tests.
- Inspect the generated Codex directory and archive for forbidden development files.

### Completion criteria

- Expected missing-release red is recorded.
- Codex-focused release tests are green.
- One command builds valid, minimal `grill-me/`, `grill-me-2.1.0.zip`, and checksum output from canonical source.
- The old `adapters/codex/skills/` directory is absent and no Skill source is duplicated.
- No personal installation path or external system is read or modified.
- All changes remain inside Ticket 1 ownership.

### Parallel safety

`No`. This Ticket establishes the shared release configuration, builder interface, output-root safety contract, and first package implementation consumed by all later Tickets.

## Ticket 2 - Add the self-contained Generic release slice

### Outcome

A general chat-model user can copy one generated Conversation-only workflow prompt that routes stages internally, while advanced users receive source-equivalent bootstrap and modular prompts in the same versioned package.

### Acceptance criteria covered

- The Generic package contains generated `generic-workflow.md`, `manifest.yaml`, and a `prompts/` directory with exactly one bootstrap plus six modules.
- The combined prompt is generated from canonical prompts in the approved fixed order and is not maintained as another hand-authored source.
- Internal routing, approval gates, Artifact requirements, stop conditions, user-language behavior, and Conversation-only claim limits remain intact.
- Generic directory, ZIP, manifest identities, and checksum entry agree.
- Development-only content is absent.

### In scope

- Extend release configuration and builder behavior for the Generic package.
- Generate the combined prompt from the canonical bootstrap and six modules with a minimal generated router wrapper.
- Generate or package the Generic release manifest with release, core, adapter, capability, and source-module identity.
- Copy modular prompts without semantic rewriting.
- Generic composition, module-order, claim-boundary, inventory, ZIP-equivalence, and checksum tests.

### Out of scope

- Tools or multi-agent capability for Generic prompts.
- A separately maintained eighth prompt source.
- Final cross-package safety and reproducibility hardening.
- Consumer documentation.

### Dependencies

Ticket 1. This Ticket extends the release configuration and builder interface established by the Codex slice.

### Likely ownership areas

- `release/release.json`
- `scripts/build_release.py`
- `adapters/generic-prompts/` only if a source-neutral composition marker is proven necessary
- Generic release tests and fixtures under `tests/release/`

### Test-first approach

1. Add tests for exact source-module inventory, declared composition order, generated-only output, internal routing, approval gates, Conversation-only restrictions, manifest identity, ZIP equivalence, and checksum coverage.
2. Run the focused Generic release scenarios and observe red because the combined prompt and Generic build path are absent.
3. Implement the smallest deterministic composition and packaging extension.
4. Run focused green, inspect the generated prompt, and refactor without changing module semantics.

### Focused verification

- Run Generic release composition and package tests.
- Compare all packaged modular prompts byte-for-byte with canonical source.
- Scan the combined prompt for required stage headers, core version, gates, handoff behavior, and forbidden capability claims.
- Verify Generic manifest identity and Conversation-only declaration.

### Broader verification

- Run existing Generic adapter tests and shared conformance validation.
- Rebuild and revalidate the Codex package to detect shared-builder regressions.
- Run core provider-neutrality checks.

### Completion criteria

- Expected missing-Generic-release red is recorded.
- Generic release tests are green.
- One build produces both package directories, both ZIPs, and checksum entries.
- The combined prompt routes without requesting another prompt paste and never overclaims Conversation capability.
- Canonical modular prompt source remains single and unchanged unless an approved semantic defect is found.

### Parallel safety

`No`. It modifies the same release configuration, builder, checksum output, and release tests as Ticket 1.

## Ticket 3 - Harden safe replacement and reproducible releases

### Outcome

Repeated builds are byte-reproducible, preserve unknown `dist/` content, reject unmanaged collisions, and never expose incomplete staging output as a valid release.

### Acceptance criteria covered

- Two unchanged builds produce byte-identical ZIP archives and checksum content.
- Unknown `dist/` content is never silently removed or overwritten.
- A collision with an unmanaged configured target stops safely with an actionable path.
- Existing valid output survives a failed replacement attempt or is replaced only after successful validation.
- Directory and ZIP content remain equivalent for both packages.

### In scope

- Failure-first safety tests using isolated output roots and explicit sentinel content.
- Managed-target recognition and resolved-path containment checks.
- Staging, validation, and replacement behavior for both packages.
- Reproducible ZIP timestamps, ordering, permissions, and checksum formatting.
- Failure diagnostics and cleanup of builder-owned staging content.

### Out of scope

- Personal installation rollback.
- Operating-system package managers.
- Signing, provenance services, publishing, or network behavior.
- Documentation prose except help text emitted by the build command.

### Dependencies

Tickets 1 and 2, because hardening operates over both complete release slices.

### Likely ownership areas

- `scripts/build_release.py`
- `release/release.json` only if managed-output metadata requires a compatible extension
- Safety, reproducibility, and failure fixtures under `tests/release/`

### Test-first approach

1. Add failing scenarios for unknown sentinel preservation, unmanaged-name collision, path escape, simulated pre-commit failure, two-build archive equality, checksum equality, and ZIP-directory equivalence.
2. Confirm each failure exposes the missing safety or reproducibility behavior rather than a test setup problem.
3. Implement the smallest coherent staging and managed-replacement behavior.
4. Reach focused green, refactor shared build boundaries, and rerun both package suites.

### Focused verification

- Run all safety and reproducibility release tests.
- Hash both archives and `checksums.sha256` across two unchanged builds.
- Inspect sentinel files before and after success and failure cases.
- Confirm all resolved mutation targets remain below the selected output root.

### Broader verification

- Run the complete release test suite.
- Revalidate both package inventories and manifests.
- Run existing core and adapter suites to detect packaging-source regressions.

### Completion criteria

- Every declared safety scenario has observed red and final green evidence.
- Two unchanged builds are byte-identical for distributable archives and checksums.
- Unknown content and existing valid output obey the Approved Specification's preservation rules.
- No mutation occurs outside builder-owned staging and managed release targets.

### Parallel safety

`No`. It changes the shared builder implementation and tests consumed by both release packages.

## Ticket 4 - Provide the consumer-first entry and manual lifecycle guides

### Outcome

A new reader can choose Codex or Generic from the repository root, understand source versus generated versus installed content, and follow manual build, validation, installation, update, removal, and resume instructions without an automatic environment change.

### Acceptance criteria covered

- Root `README.md` presents Traditional Chinese first and an equivalent English Quick Start.
- Codex documentation explains one-Plugin installation, `$ai-dev-workflow` as the primary entry, direct Skill shortcuts, validation, manual update, and removal.
- Generic documentation explains one-file entry, modular alternatives, Conversation-only limits, user-managed persistence, and resumption.
- Documentation does not perform, imply, or authorize installation or publication.
- All relative links and documented commands resolve to final source or generated paths.

### In scope

- Root bilingual navigation and quick start.
- Update the Traditional Chinese Codex and Generic guides against the final package layout and commands.
- Clearly label canonical source, generated `dist/`, and personal installation as different locations.
- Manual lifecycle and integrity-verification instructions.
- Required-section, link, command-path, language, and provider-operation scans.

### Out of scope

- Full duplicated English design or usage manuals.
- Automatic installation scripts.
- Marketplace instructions or publication credentials.
- Changes to runtime behavior or release generation.

### Dependencies

Ticket 3, so documentation references a stable package inventory, command, safety behavior, and checksum format.

### Likely ownership areas

- Root `README.md`
- `docs/guides/generic.zh-TW.md`
- `docs/guides/codex.zh-TW.md`
- Documentation checks under `tests/release/` when deterministic assertions are useful

### Test-first approach

Documentation prose has no meaningful automated red behavior test. Before editing, declare the test-first exception and use these alternative checks:

- Required entry and lifecycle section inventory.
- Relative-link resolution.
- Documented path and command validation against actual release output.
- Provider-operation isolation in the Generic path.
- Human comparison with the Approved Specification and final package manifests.

Add an automated failing check first when a missing deterministic path, heading, identity, or command can be asserted meaningfully.

### Focused verification

- Validate every documented relative link and release path.
- Verify README language order and both user paths.
- Verify Codex-only installation and invocation details remain in the Codex path.
- Verify Generic instructions preserve Conversation-only and user-managed persistence language.

### Broader verification

- Build both packages by following only documented commands.
- Compare documented inventories, names, versions, checksums, and entry points with generated output.
- Scan all human documents for stale pre-release paths and unsupported-provider claims.

### Completion criteria

- A reader can select and use either supported release without reading repository architecture first.
- Manual lifecycle instructions match verified package behavior.
- No document suggests that build automatically installs or publishes anything.
- All alternative documentation checks pass.

### Parallel safety

`No`. Although documentation owns separate files, it must describe the stable behavior and final paths established by Ticket 3; drafting earlier risks encoding an unstable command contract.

## Ticket 5 - Integrate, forward-test, and produce the 2.1.0 source release

### Outcome

The repository contains a validated `2.1.0` release output, direct evidence for every acceptance criterion, and no unsupported claim, personal installation, or external publication.

### Acceptance criteria covered

- All existing and new tests pass together.
- Both manifests, all six Skills, both runtime packages, ZIPs, and checksums validate.
- Clean-context forward tests demonstrate the Codex Plugin entry and Generic one-file routing.
- The release is reproducible and minimal.
- Final evidence identifies residual risks and deferred installation or publication work.

### In scope

- Execute the documented build into repository `dist/`.
- Run core, Generic, Codex, release, documentation, manifest, native Skill, checksum, inventory, and reproducibility checks.
- Forward-test the installed-package shape without installing it into a personal directory.
- Forward-test the Generic combined prompt from a clean context using representative fresh and resumed workflows.
- Record raw commands, results, generated inventory, checksums, limitations, and residual risks in Implementation Evidence.
- Remove test-only temporary output and generated bytecode while retaining the final versioned `dist/` release artifacts.

### Out of scope

- Copying the Plugin into a personal Skill directory.
- Marketplace installation or publication.
- Network calls, remote uploads, release signing, or unsupported adapters.
- Fixing unrelated repository work.

### Dependencies

Tickets 1-4.

### Likely ownership areas

- Final generated `dist/` outputs
- `docs/evidence/` release evidence
- Integration checks under `tests/release/`
- Small source fixes within prior Ticket ownership only when a failing approved acceptance criterion proves them necessary

### Test-first approach

Use the Approved Specification acceptance criteria as the integration matrix. Add a focused failing integration check before any source fix for an uncovered deterministic criterion. Forward-test with raw Artifacts and minimal context rather than expected answers or implementation conclusions.

### Focused verification

- Build twice and compare archive and checksum bytes.
- Verify archive hashes from `checksums.sha256`.
- Compare every ZIP entry with its unpacked package file.
- Run all release, documentation, and adapter integration tests.
- Run official Plugin and Skill validation.

### Broader verification

- Run the existing 27-test baseline plus every new release test.
- Run both shared conformance validations.
- Re-run provider-neutrality, duplicate-source, stale-link, placeholder, minimal-package, unsupported-provider, and generated-file scans.
- Inspect the final `dist/` inventory and confirm no personal installation or external state changed.

### Completion criteria

- Every Approved Specification acceptance criterion has direct automated, forward-test, or declared manual evidence.
- No blocking finding or failed required check remains.
- Final archives, checksums, unpacked packages, manifests, and source versions agree.
- Temporary test artifacts and bytecode are absent; final release artifacts remain under `dist/`.
- Installation and publication remain explicitly pending separate authorization.

### Parallel safety

`No`. This Ticket integrates and may diagnose all prior ownership areas; it must run after the complete release and documentation are stable.

## Dependency order and parallel groups

```text
Ticket 1: Codex Plugin release slice
    ↓
Ticket 2: Generic release slice
    ↓
Ticket 3: Safety and reproducibility hardening
    ↓
Ticket 4: Consumer entry and lifecycle documentation
    ↓
Ticket 5: Integration and forward testing
```

No parallel implementation group is approved. The first three Tickets share the release configuration, builder, output, and tests; Ticket 4 consumes their final public contract; Ticket 5 integrates all results.

## Plan approval gate

This Plan is Approved against the corrected Approved Specification and authorizes implementation within the stated Ticket boundaries.
