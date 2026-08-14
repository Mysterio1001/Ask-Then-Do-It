# Ask Then Do It 1.2.0 Release Architecture Diagnosis

Artifact type: Architecture Improvement Report

Artifact ID: `ask-then-do-it-1-2-release-architecture`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Status: Draft

Inputs: Approved 1.2.0 Specification and Ticket Plan, final diff, Core and adapter declarations, marketplace and Plugin manifests, release builder and validators, tests, generated packages, and Ticket 5 Review.

Assumptions: Current textual consumer surfaces remain intentionally standalone. A future architecture change must preserve readable independent packages and localized documentation.

Deferred: Refactoring, actual deletion experiments, clause/schema redesign, other operating systems, live target CLI, and external publication.

Handoff: Optional user acceptance or rejection. Acceptance authorizes only a return to Specification work, not refactoring or implementation.

Approval: None. This first report is `Draft`.

## 1. Analysis scope and limitations

Capability: `tools`. This read-only milestone diagnosis covers release identity and distribution from `release/release.json` through Core/adapters, repository marketplace, Plugin manifest/assets, builder/validators, tests, and `dist/`. The same context implemented the release; no isolated diagnostic context or actual deletion experiment was used.

## 2. System architecture summary

Core and adapter sources define workflow behavior; `.agents/plugins/marketplace.json` defines repository discovery; `release/release.json` coordinates package identity and inventory; `scripts/build_release.py` validates canonical sources and atomically generates deterministic Codex and Generic packages. Dedicated marketplace, conformance, evidence, Plugin, Skill, image, documentation, and package tests close contracts that the standard-library builder does not parse itself.

## 3. Deletion-analysis results

Simulated deletion only; no file was removed.

- Without `release/release.json`, the builder and release-evidence validator fail closed and no current packages can be produced.
- Without `scripts/validate_marketplace.py`, the builder import fails and marketplace validation cannot pass; release generation is blocked rather than silently omitting the supply-chain check.
- Without `.agents/plugins/marketplace.json`, both the marketplace validator and builder fail before committed output.
- Without the focused `1.2.0` release/document/image tests, active localized references, transparent-corner behavior, README preservation, and package exclusion could drift beyond the builder's intentionally narrow structured checks.
- Without `dist/`, no consumer archive remains, but the canonical sources can deterministically recreate it.

## 4. Twelve-lens results

| Lens | Outcome | Evidence |
| --- | --- | --- |
| Duplicated Code or Policy | `finding` | Current release identity and command-flow wording are repeated across Core, adapters, manifests, localized guides, tests, and generated metadata. |
| Long Function | `no-finding` | New marketplace, PNG, and prior-output checks are separated into named functions. |
| Large Module or Class | `no-finding` | `build_release.py` is large but remains one cohesive deterministic release boundary with no class growth. |
| Long Parameter List | `no-finding` | Changed interfaces pass cohesive config/path/selection inputs. |
| Data Clumps | `no-finding` | Marketplace source fields and Plugin asset contracts are validated as structured groups. |
| Primitive Obsession | `no-finding` | Semver, URL, ref, policy, path, PNG header, and digest primitives are explicitly constrained. |
| Feature Envy | `no-finding` | Marketplace rules stay in the marketplace validator while release coordination stays in the builder. |
| Divergent Change | `no-finding` | Each added validator changes for one contract family. |
| Shotgun Surgery | `finding` | A version advance requires coordinated changes across many current declarations and tests, even though drift is detected. |
| Message Chains | `no-finding` | Direct validator calls and filesystem boundaries avoid deep navigation chains. |
| Leaky Abstraction | `no-finding` | Consumer ZIPs exclude repository marketplace metadata and temporary source-image details. |
| Shallow Module | `no-finding` | Builder and validators provide substantial fail-closed behavior behind small command interfaces. |

## 5. Finding evidence, impact, and confidence

The two findings share one cause: standalone consumer text and explicit release declarations are intentionally duplicated. Impact is maintainer effort and the risk of missing one declaration during a later release. Confidence is high because this release required coordinated active-version changes across Core, both adapters, Plugin, guides, tests, and generated output. Current impact is mitigated: builder and test gates reject mismatched catalog refs, manifests, package names, docs, assets, checksums, and evidence.

## 6. Prioritized improvement proposals

1. Add a structured current-release declaration inventory consumed by a validator, while keeping generated consumer packages readable and self-contained.
2. Parameterize standalone marketplace validation from the release configuration instead of changing its default expected tag each release.
3. Keep localized prose editorial, but centralize the exact command/state checklist used by parity tests so future wording changes do not duplicate contract literals unnecessarily.

These are optional proposals. None is required to release `1.2.0`, and this Draft authorizes no implementation.

## 7. Potentially affected modules

`release/release.json`, `scripts/build_release.py`, `scripts/validate_marketplace.py`, Core/adapter version headers, localized guides, release tests, and release evidence validation.

## 8. Unresolved items

Whether future release identity should be generated into canonical text, validated through a structured inventory, or continue as explicit declarations; and whether non-Windows and live target-CLI validation should become mandatory publication checks.

## 9. Artifact links

- [Approved Specification](../specs/command-install-update-1.2.0.md)
- [Approved Ticket Plan](../plans/command-install-update-1.2.0.md)
- [Ticket 5 Review](command-install-update-1.2.0-ticket-5-review.md)
- [Release evidence](ask-then-do-it-release-1.2.0.md)

## 10. Knowledge Base Change Summary

No durable Project Knowledge Base change is proposed. The existing Knowledge Base already records the marketplace, release builder, consumer package, and command-installation boundaries. The optional architecture proposals remain unaccepted.
