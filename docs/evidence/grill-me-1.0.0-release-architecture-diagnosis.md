# Grill Me 1.0.0 Release Architecture Diagnosis

Artifact type: Architecture Improvement Report

Artifact ID: `grill-me-1-0-release-architecture-diagnosis`

Workflow ID: `grill-me-clean-slate-1-0`

Core version: `1.0.0`

Status: draft

Inputs: Approved Specification and Ticket Plan, canonical Core and adapters, release configuration and builder, generated package inventories, 52-test Green result, native validation results, conformance results, and reproducibility evidence.

Assumptions: The repository is a maintainer workspace; Codex and Generic ZIPs are the only consumer packages; no runtime installation or external publication is in scope.

Deferred: Provider-native adapters beyond Codex, public hosting, signing, installers, and long-term archive policy.

Handoff: Retain this report as release evidence. Any accepted structural change must return through Specification, Ticket Plan, and TDD.

Approval: None. This diagnostic report does not authorize implementation.

## 1. Analysis scope and limitations

This is a read-only release-milestone diagnosis. It covers Core ownership, adapter boundaries, release composition, generated outputs, tests, and human entry points. The same agent performed implementation and diagnosis, so this is not an independent architecture assessment. No file was actually deleted, moved, renamed, or rewritten for the deletion analysis.

## 2. System architecture summary

- `core/` is the normative provider-neutral contract.
- `adapters/codex/` maps the contract to one Plugin with eight independently discoverable Skills.
- `adapters/generic-prompts/` maps the contract to nine Conversation-only prompt modules.
- `release/release.json` declares one version and two provider packages.
- `scripts/build_release.py` validates canonical source, creates deterministic packages, verifies inventories and checksums, and replaces only a complete managed output set.
- Root and package start guides are human-facing; canonical workflow contracts remain English.
- Tests independently cover Core conformance, both adapters, documentation, release inventory, collision safety, reproducibility, ZIP equivalence, and evidence gating.

The public surface is small: two ZIPs plus one checksum file. Maintainer internals remain outside both packages.

## 3. Deletion-analysis results

All deletion checks were simulated from references, build guards, and tests:

| Simulated removal | Expected effect | Evidence |
| --- | --- | --- |
| `release/release.json` | No release can be built | Builder requires and strictly validates this configuration |
| One Codex Skill directory | Codex source and package inventory validation fail | Configured eight-Skill equality and Skill tests |
| One Generic prompt module | Generic source validation and exact nine-prompt tests fail | Config module list and prompt inventory tests |
| Either package `START-HERE.zh-TW.md` | Package inventory and onboarding tests fail | Codex and Generic release tests |
| One mandatory Core rule | Adapter conformance fails until both mappings are reconciled | Shared conformance validator and fixtures |
| `checksums.sha256` | Existing output set and release verification fail | Build safety and checksum tests |
| Root `START-HERE.zh-TW.md` | Consumer-choice and relative-link tests fail | Documentation tests |

No candidate appears redundant enough to justify an actual deletion experiment.

## 4. Twelve-lens results

| Lens | Result | Evidence and reason |
| --- | --- | --- |
| Duplicated Code or Policy | `no-finding` | Start guides repeat a small safety boundary for offline use, while normative workflow policy remains in Core and adapter contracts. |
| Long Function | `no-finding` | Builder functions are bounded by validation, composition, verification, and commit responsibilities; tests cover each boundary. |
| Large Module or Class | `no-finding` | `build_release.py` is sizable but forms one deep, standard-library release module with a single CLI surface and cohesive safety contract. |
| Long Parameter List | `no-finding` | Shared helpers take only the path, config, selection, and explicit validation mode needed by their contract. |
| Data Clumps | `no-finding` | Source, directory, archive, entry, and module data are intentionally grouped in the release configuration rather than repeated call arguments. |
| Primitive Obsession | `no-finding` | Paths and versions are strings at the JSON boundary, then receive strict SemVer, containment, provider-prefix, and inventory validation. |
| Feature Envy | `not-applicable` | No object-oriented domain objects exchange responsibilities; modules operate on their owned source and contract data. |
| Divergent Change | `no-finding` | Core, adapter, documentation, and packaging changes have separate ownership paths and focused tests; the builder changes only for release-contract behavior. |
| Shotgun Surgery | `no-finding` | Version appears in required independent artifact envelopes, but release identity is declared once in config and consistency tests detect drift. |
| Message Chains | `not-applicable` | No long runtime object-navigation chain exists; paths are resolved directly from validated configuration. |
| Leaky Abstraction | `no-finding` | Generic never claims Codex capabilities; Codex installation details remain in human guides and do not leak into Core or Generic prompts. |
| Shallow Module | `no-finding` | Eight Skills and nine prompts expose stage-level interfaces required for direct use, while orchestrators remain intentionally thin and the release builder hides substantial validation behind one command. |

## 5. Finding evidence, impact, and confidence

No release-blocking architecture finding was identified. Confidence is high for repository structure and generated inventory because they are covered by deterministic tests and byte comparisons; confidence is moderate for behavior across third-party chat models because no provider-native execution harness is available in this workspace.

## 6. Prioritized improvement proposals

1. Low priority: add provider-specific forward scenarios only when a stable, automatable provider harness and explicit authority are available.
2. Low priority: consider signing or provenance metadata after a public hosting strategy is approved.

Neither proposal is required for `1.0.0`, and this report does not authorize either change.

## 7. Potentially affected modules

- Future scenario harness: `tests/generic/` and potentially a new provider adapter.
- Future provenance: `release/release.json`, `scripts/build_release.py`, release tests, and human guides.

## 8. Unresolved items

- Exact behavior of every third-party model after prompt paste remains host-dependent.
- Public release hosting and signing policy are not selected.

## 9. Artifact links

- [Specification](../specs/grill-me-clean-slate-1.0.0.md)
- [Ticket Plan](../plans/grill-me-clean-slate-1.0.0.md)
- [Ticket 4 evidence](grill-me-1.0.0-ticket-4.md)

## 10. Knowledge Base Change Summary

Additions: none. Modifications: none. Removals: none. This diagnosis confirms the approved release architecture and introduces no durable project decision requiring a Knowledge Base update.
