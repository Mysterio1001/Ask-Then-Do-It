# Grill Me Release 1.0.0 Evidence

Artifact type: Implementation Evidence

Artifact ID: `grill-me-release-1.0.0-evidence`

Workflow ID: `grill-me-clean-slate-1-0`

Core version: `1.0.0`

Release version: `1.0.0`

Status: Completed

## Scope

This is the first public source release of Grill Me. It provides exactly two consumer packages: one Codex Plugin and one Generic prompt package. It removes all unpublished historical release output and migration behavior while retaining all other approved workflow behavior.

## Inputs

- Approved [Requirement Decision Record](../requirements/grill-me-clean-slate-1.0.0.md)
- Approved [Specification](../specs/grill-me-clean-slate-1.0.0.md)
- Approved [Ticket Plan](../plans/grill-me-clean-slate-1.0.0.md)
- [Ticket 1 evidence](grill-me-1.0.0-ticket-1.md)
- [Ticket 2 evidence](grill-me-1.0.0-ticket-2.md)
- [Ticket 3 evidence](grill-me-1.0.0-ticket-3.md)
- [Ticket 4 evidence](grill-me-1.0.0-ticket-4.md)
- [Validation ledger](grill-me-release-1.0.0.json)

## Final automated Green

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Observed: `Ran 52 tests in 4.190s`; `OK`.

This includes clean version identity, migration absence, 22-rule coverage, eight-Skill and nine-prompt inventories, immediate Generic startup, both package guides, documentation links, safe collisions, atomic rebuild behavior, reproducibility, ZIP equivalence, checksum verification, and fail-closed release evidence.

## Skill, Plugin, and adapter validation

- Eight source Skills: all valid.
- Eight packaged Skills: all valid.
- Source Codex Plugin: validation passed.
- Packaged Codex Plugin: validation passed.
- Codex adapter: conforms to Core `1.0.0`.
- Generic adapter: conforms to Core `1.0.0` with only `conversation` capability.

The `skill-creator` validation rules influenced the final Skill verification; the `plugin-creator` validation rules confirmed both the canonical and packaged Plugin. No cachebuster, installation, reinstall, or marketplace workflow was executed.

## Final package inventory

```text
dist/
├─ codex/
│  ├─ grill-me/
│  └─ grill-me-1.0.0.zip
├─ generic/
│  ├─ generic-prompts-1.0.0/
│  └─ generic-prompts-1.0.0.zip
└─ checksums.sha256
```

- Codex unpacked package: 18 files — Plugin manifest, Traditional Chinese start guide, eight Skills, and eight UI metadata files.
- Generic unpacked package: 12 files — Traditional Chinese start guide, combined workflow, generated manifest, and nine byte-equivalent source prompts.
- No tests, Core source, Plans, Specifications, evidence, installer, marketplace file, cache, or unrelated documentation appears in either package.

## Reproducibility, ZIP, and checksum evidence

Two isolated complete builds were compared by relative filename and SHA-256. Every generated file was byte-identical.

Both archives were expanded and every relative file was compared with the matching unpacked directory. Both pairs were byte-equivalent.

Current archive hashes:

```text
4bd9733c50224aaeef7f6f0ded125a18c81340a3c31f99bf80396c324583d26e  codex/grill-me-1.0.0.zip
a8f22fcf80d9a0fee1c4cee85c7272f55e81f1bf40d203d55389e49de97af53b  generic/generic-prompts-1.0.0.zip
```

`dist/checksums.sha256` contains exactly these two entries.

## Removed-artifact and safety evidence

- No `MIGRATE-V2-001`, migration inventory, migration test, or first-use migration instruction remains in active runtime areas.
- No stale old release identity remains in active Core, adapter, release, guide, design, or generated output areas.
- No placeholder or forbidden development content appears in either package.
- Unknown or incomplete output content fails closed without replacement.
- A failed rebuild preserves a prior complete valid output set.
- Build code contains no installer, publication, network, personal Codex, or marketplace mutation operation.

## Release milestone architecture diagnosis

The [read-only Architecture Improvement Report](grill-me-1.0.0-release-architecture-diagnosis.md) covers dependency boundaries, simulated deletion, and all twelve Architecture and Refactoring Lenses. It found no release-blocking architecture issue. Its draft status does not authorize implementation.

## Final Review

The [Final Review](grill-me-1.0.0-final-review.md) is labeled `non-independent` because the same agent implemented and reviewed the work. It reports no blocking finding and discloses unavailable live third-party-model execution, unavailable independent review, and untested operating systems.

## Assumptions

- Third-party model wording can vary, but the Generic prompt contract normatively requires one immediate recommended requirement question in the same effective response.
- Manual Codex installation remains under the user's authority and environment-specific marketplace rules.

## Deferred

- Publication, hosting, Git tags, signing, provenance, automatic installation, marketplace creation, additional provider-native adapters, and external-model automation.

## Handoff

The local `1.0.0` release is complete and ready for a maintainer-controlled publication decision. No publication or installation occurred in this workflow.
