# Grill Me Release 3.0.0 Evidence

Artifact type: Implementation Evidence

Artifact ID: `grill-me-release-3.0.0-evidence`

Workflow ID: `grill-me-core-v3`

Core version: `3.0.0`

Release version: `3.0.0`

Status: Completed

## Scope

This evidence covers the local source release only: Core `3.0.0`, Codex adapter `3.0.0`, Generic adapter `3.0.0`, one eight-Skill Codex Plugin package, one nine-source-prompt Generic package, deterministic archives, checksums, v2 preservation, documentation, and fail-closed release evidence.

It does not cover personal installation, marketplace mutation, publication, remote upload, release signing, or dedicated provider adapters beyond Codex and Generic.

## Red evidence

The Ticket 6 release tests were changed before production release configuration or documentation. The first run against the `2.1.0` release state executed 25 tests and produced 17 failures plus 5 errors. Expected missing behavior included:

- Release and Core identity still declared `2.1.0` and `2.0.0`.
- The Plugin manifest still declared `2.1.0` and six Skills.
- Generic release configuration omitted the two v3 prompts.
- `checksums-2.1.0.sha256` did not exist.
- v3 documentation paths were absent.
- The release evidence validation contract and validator did not exist.

No completed `3.0.0` release evidence existed during this Red state.

## Final automated Green

Command:

```powershell
python -m unittest `
  tests.conformance.test_validator `
  tests.codex.test_adapter `
  tests.generic.test_generic_prompts `
  tests.migration.test_v2_migration `
  tests.release.test_documentation `
  tests.release.test_release_contract `
  tests.release.test_codex_release `
  tests.release.test_generic_release `
  tests.release.test_release_safety `
  tests.release.test_release_evidence -v
```

Raw outcome:

```text
Ran 73 tests in 4.595s

OK
```

An earlier integrated attempt could not read the workspace-local PyYAML directory under sandbox ACL and therefore produced three dependency errors. It was not recorded as successful release evidence. The final command ran with the existing dependency directory readable and passed all checks.

## Skill and Plugin validation

Every packaged directory under `dist/grill-me/skills` was validated with the official `skill-creator` validator:

```text
ai-dev-workflow: Skill is valid!
grill-requirements: Skill is valid!
grill-with-docs: Skill is valid!
implement-tdd: Skill is valid!
improve-architecture: Skill is valid!
plan-tickets: Skill is valid!
review-code: Skill is valid!
write-spec: Skill is valid!
```

Plugin validation outcome:

```text
Plugin validation passed: C:\Users\Ian\Desktop\Grill Me\dist\grill-me
```

No Plugin cachebuster, reinstall, personal Skill copy, or marketplace command was run.

## Adapter conformance

Commands:

```powershell
python scripts/validate_conformance.py `
  --catalog core/rules/rules.yaml `
  --manifest adapters/codex/conformance.yaml

python scripts/validate_conformance.py `
  --catalog core/rules/rules.yaml `
  --manifest adapters/generic-prompts/manifest.yaml
```

Raw outcomes:

```text
Conformance passed: codex against core 3.0.0
Conformance passed: generic-prompts against core 3.0.0
```

Both adapters map all 23 mandatory v3 Rule IDs.

## Reproducibility, inventory, ZIP, and checksum evidence

Two clean builds from unchanged canonical source produced:

```text
grill-me-3.0.0.zip byte_identical=True sha256=ce6c9331e37f13bb1968340a4a122250c5c0044319288d3d5c10e6c3d8c766af
generic-prompts-3.0.0.zip byte_identical=True sha256=54895142a2af1bebe84d413761c1003f38092f62c7382deb61a6982236075c96
checksums.sha256 byte_identical=True sha256=ab5f07957f10c432f136a405c37f323e3e84ddbb46915f218aa6fe0ec0cf3c4a
```

Explicit package comparison produced:

```text
dist\grill-me-3.0.0.zip zip_equivalent=True files=17
dist\generic-prompts-3.0.0.zip zip_equivalent=True files=11
generic-prompts-3.0.0.zip checksum_match=True
grill-me-3.0.0.zip checksum_match=True
```

The Codex count contains the Plugin manifest plus sixteen Skill and UI metadata files. The Generic count contains nine byte-identical modular source prompts plus generated `generic-workflow.md` and `manifest.yaml`. Tests reject duplicate, missing, stale, unlisted, and extra runtime content.

## v2 preservation

Protected v2 artifacts retained these hashes:

```text
10c9b95e9e75c9dac20e570d0f7ed75ef71e4ad0d59e755f53d27ec5a729236d  grill-me-2.1.0.zip
5f5d6e86dbde9e2de99f68528c18df1ea1265b59f65d969a4aa9c70bee954254  generic-prompts-2.1.0.zip
cb740d91041363f15e262c090f20f33e7b5716ac554b61bfaa4b0a50f4589879  docs/evidence/grill-me-release-2.1.0.md
```

`dist/checksums-2.1.0.sha256` preserves the archive hash contract. A dedicated release-safety test reconstructs a valid v2 output, builds v3 over only the recognized legacy overlap, and verifies that both versioned v2 archives, the v2 Generic directory, and the versioned checksum snapshot remain unchanged.

## Fail-closed evidence gate

`release/release.json` declares twelve required validation check IDs. `scripts/validate_release_evidence.py` rejects a completed release record when any check is missing, duplicated, unknown, `failed`, or `blocked`, or lacks a command and outcome. Tests prove passed, failed, blocked, and missing-check paths.

The machine-readable ledger for this release is [grill-me-release-3.0.0.json](grill-me-release-3.0.0.json). It was created only after every required check had passed.

## Release milestone architecture diagnosis

The read-only [v3 Release Architecture Diagnosis](v3-release-architecture-diagnosis.md) applied all twelve lenses and simulated deletion of the release contract, builder, evidence validator, checksum snapshot, and adapter sources without mutating them.

It found non-blocking maintainability concerns: one large builder module, concentrated reasons to change, nested primitive configuration, coordinated version touch points, and convention-based legacy naming. The report is `draft`, non-independent, and does not authorize refactoring. No correctness, integrity, security, or release-blocking architecture finding remains.

## Non-independent final review

The implementation agent reviewed release identity, stale transitional text, runtime inventories, placeholder markers, development-file exclusion, package/source equivalence, legacy replacement behavior, failure rollback, and the evidence gate. No blocking finding remained after the final 73-test run.

This review is explicitly non-independent because no separate clean reviewer was authorized or available under the current execution constraints. Official validators, deterministic conformance checks, independent clean output directories, and byte-level comparisons provide the stronger objective evidence used for release status.

## Final output

- `dist/grill-me/`
- `dist/grill-me-3.0.0.zip`
- `dist/generic-prompts-3.0.0/`
- `dist/generic-prompts-3.0.0.zip`
- `dist/checksums.sha256`
- Preserved `dist/grill-me-2.1.0.zip`
- Preserved `dist/generic-prompts-2.1.0/`
- Preserved `dist/generic-prompts-2.1.0.zip`
- Preserved `dist/checksums-2.1.0.sha256`

The repository is not a Git repository, so Git status and diff evidence are unavailable. No network, installation, marketplace, publication, upload, or personal-environment mutation occurred.
