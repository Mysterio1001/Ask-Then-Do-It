# Ask Then Do It 1.0.0 Release Architecture Diagnosis

Artifact type: Architecture Improvement Report

Artifact ID: `ask-then-do-it-1-0-release-architecture`

Workflow ID: `ask-then-do-it-1-0`

Status: Draft

## Analysis scope and limitations

Read-only release-milestone diagnosis covering Core, Codex and Generic adapters, release builder, tests, and generated packages. No production code or architecture was changed by this diagnosis.

## System architecture summary

The project retains three clear boundaries: model-neutral contracts in `core/`, provider translations in `adapters/`, and deterministic consumer packaging in `scripts/build_release.py` plus `release/release.json`.

## Deletion-analysis results

Simulated deletion of Core would remove the shared semantic contract; deletion of either adapter would remove only that provider surface; deletion of generated `dist/` remains recoverable through the deterministic builder. The two legal files are canonical repository sources consumed by both packages.

## Twelve-lens results

Duplicated Code or Policy, Long Function, Large Module or Class, Long Parameter List, Data Clumps, Primitive Obsession, Feature Envy, Divergent Change, Shotgun Surgery, Message Chains, Leaky Abstraction, and Shallow Module were reviewed. No release-blocking finding was identified. The release builder remains the largest coordination module, but its validation and safety boundaries are cohesive and covered by rollback, collision, reproducibility, inventory, and ZIP-equivalence tests.

## Finding evidence, impact, and confidence

No blocking finding. Confidence is moderate because the diagnosis is non-independent and local; live third-party model execution and additional operating systems were not tested.

## Prioritized improvement proposals

No change is required for `1.0.0`. A future Specification may consider separating release inventory helpers if builder growth makes tests or review materially harder.

## Potentially affected modules

Future-only: `scripts/build_release.py` and release tests.

## Unresolved items

Publication hosting, signing, provenance, external-model automation, and formal legal review remain deferred.

## Artifact links

- [Specification](../specs/ask-then-do-it-1.0.0.md)
- [Ticket Plan](../plans/ask-then-do-it-1.0.0.md)

## Knowledge Base Change Summary

No durable project-knowledge change is proposed.
