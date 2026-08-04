# Ask Then Do It 1.1.0 Release Architecture Diagnosis

Artifact type: Architecture Improvement Report

Artifact ID: `ask-then-do-it-1-1-release-architecture`

Workflow ID: `optional-ticket-testing`

Core version: `1.1.0`

Status: Draft

Inputs: Approved [Optional Ticket Testing Specification](../specs/optional-ticket-testing.md), Approved [Ticket Plan](../plans/optional-ticket-testing.md), [Final Review](ask-then-do-it-1.1.0-final-review.md), Core and adapter contracts, conformance manifests and validator, tests, release configuration, and generated packages.

Assumptions: Core is intended to be normative, while adapter wording may vary only when mapped behavior remains compatible. Existing string-fragment tests are evidence of selected clauses, not a complete behavioral model.

Deferred: Actual refactoring, actual deletion experiments, external hosts, additional operating systems, publication, and selection between the proposals below.

Handoff: Explicit user acceptance or rejection. Acceptance authorizes only a return to `$write-spec`; it does not authorize refactoring or implementation.

Approval: None. This first report is `Draft`.

Current disposition: The two immediate Specification gaps that triggered this diagnosis were fixed through the Approved Ticket 4 `tdd` path and verified by the [Final Review after fixes](ask-then-do-it-1.1.0-final-review-after-fixes.md). The broader clause-level conformance proposals remain optional, unaccepted, and non-blocking for `1.1.0`; this Draft authorizes no implementation.

## 1. Analysis scope and limitations

This read-only release-milestone diagnosis covers the mode-selection policy boundary from provider-neutral Core through Codex and Generic adapters, conformance validation, scenario tests, localized guides, and deterministic packages. Capability: `tools`. The same context performed implementation and diagnosis; no independent diagnostic context was used. No source, package, configuration, or authoritative data was deleted or changed by this diagnosis.

## 2. System architecture summary

Ask Then Do It has three primary semantic layers:

1. `core/` defines normative workflow modules, artifact contracts, and mandatory rule IDs.
2. `adapters/codex/` and `adapters/generic-prompts/` manually translate that contract into host-specific Skills and provider-neutral conversation prompts.
3. `scripts/build_release.py` and `release/release.json` deterministically copy the adapter sources into consumer packages.

`scripts/validate_conformance.py` verifies lockstep Core version, exact mandatory rule-ID coverage, capability hierarchy, non-empty evidence paths, and declared validation metadata. It does not inspect whether an adapter's evidence actually implements every behavioral clause inside a rule. Feature tests compensate by searching selected phrases in Core and adapter files, but they do not derive complete scenario coverage from the Approved Specification.

## 3. Deletion-analysis results

Simulated deletion only; no files were removed.

- If `scripts/validate_conformance.py` disappeared, both adapter conformance commands would fail immediately and the release suite would lose version, mandatory-ID, capability, and manifest-shape protection. Package building itself would still have source inventories, so semantic drift would remain a separate concern.
- If the adapter-specific phrase assertions for optional testing disappeared while manifests retained the existing rule IDs, both conformance validations would still pass. The two Final Review findings demonstrate why: a manifest can claim `GATE-PLAN-001` and `REVIEW-EVIDENCE-001` without proving every clause in the expanded `1.1.0` meanings.
- If `core/modules/ticket-planning.md` or `core/modules/direct-implementation.md` disappeared, Core-focused tests and index links would fail, but adapter prompts would remain physically buildable because packaging copies adapter sources rather than compiling them from Core.
- If `dist/` disappeared, consumer outputs would be unavailable until rebuilt, but the deterministic builder could recreate them from adapter sources. This boundary remains intentionally recoverable.

The critical dependency is therefore not file existence alone; it is the manually maintained semantic mapping from a multi-clause Core rule to two independently authored adapters and several test assertions.

## 4. Twelve-lens results

| Lens | Outcome | Evidence |
| --- | --- | --- |
| Duplicated Code or Policy | `finding` | Optional-test behavior is manually duplicated in Core, nine Codex Skills or handoffs, ten Generic prompts or composition, three localized document sets, manifests, and tests. |
| Long Function | `no-finding` | `validate_conformance.validate` and `validate_release_evidence.validate` remain readable, linear, and cohesive. |
| Large Module or Class | `no-finding` | Direct implementation was added as separate Core, Codex, and Generic modules instead of expanding TDD into mixed responsibilities. |
| Long Parameter List | `no-finding` | Validator entry points accept cohesive artifact paths and no new coordination-heavy interface was introduced. |
| Data Clumps | `finding` | Mode, selection approval, recommendation, external constraint, skipped-test disclosure, and Review behavior travel together as one policy but are represented as prose fragments across files without one structured contract. |
| Primitive Obsession | `no-finding` | The strings `tdd` and `direct` are a deliberate closed serialization with explicit invalid-mode behavior. |
| Feature Envy | `not-applicable` | Declarative adapter files do not perform runtime behavior against another module's data; the issue is policy replication rather than misplaced computation. |
| Divergent Change | `finding` | `GATE-PLAN-001`, `ROUTE-USER-001`, and `REVIEW-EVIDENCE-001` accumulated multiple independent behavioral clauses while retaining coarse rule identities, so one rule now changes for several distinct reasons. |
| Shotgun Surgery | `finding` | The feature touched 72 tracked files and new generated/evidence artifacts; two Approved clauses were still missed across all layers. |
| Message Chains | `not-applicable` | There is no relevant runtime navigation chain in the declarative workflow contract. |
| Leaky Abstraction | `finding` | Adapter authors and tests must read Core prose and manually know which fragments make a rule conformant because the manifest's rule-ID abstraction does not carry clause-level semantics. |
| Shallow Module | `finding` | The current conformance interface is easy to satisfy with a rule ID but provides less semantic assurance than its `Conformance passed` result implies for multi-clause rules. |

## 5. Finding evidence, impact, and confidence

### Semantic conformance is coarser than the behavior it claims

Evidence: `validate_conformance.py` compares mandatory and implemented rule-ID sets, versions, capabilities, evidence-list shape, and validation metadata. It never associates an individual behavior or scenario with a rule. `GATE-PLAN-001` now covers mode selection, missing-mode blocking, plan display order, and approval; `REVIEW-EVIDENCE-001` now covers raw evidence, mode preservation, skipped-test disclosure, declined-test behavior, and direct completion claims. The full 66-test suite and both conformance commands passed while the Final Review still found missing Approved clauses.

Impact: future Core expansions can produce packages whose manifests truthfully list every rule ID yet omit part of a rule's current meaning. This is a release-quality risk across all adapters and explains the duplicated-policy and shotgun-surgery findings.

Confidence: High for the observed validation gap because it follows directly from validator code and a concrete green-suite counterexample. Moderate for the best long-term remedy because the repository has not yet chosen between finer rule IDs, structured per-rule evidence, or shared executable scenarios.

## 6. Prioritized improvement proposals

1. Split multi-clause optional-testing behavior into stable, independently mappable rule IDs or clause IDs for plan display order, recommendation dimensions, mode completeness, external test constraints, direct no-test behavior, and Review declined-test behavior. This gives conformance a smaller truthful unit.
2. Extend adapter manifests to map each required rule or clause to specific evidence files and scenario IDs, then make conformance reject missing, unknown, or duplicate mappings. File existence alone should not be described as semantic proof.
3. Add shared black-box scenario definitions derived from the Approved Specification and execute equivalent assertions against Core, Codex, and Generic surfaces. Include negative cases for incomplete pre-selection display, omitted risk categories, external CI blocking, and Review automatically prescribing declined tests.
4. Keep localized documentation and package inventory tests downstream; do not make user-facing translations the normative policy source.

## 7. Potentially affected modules

- `core/rules/rules.yaml`, `core/modules/ticket-planning.md`, `core/modules/direct-implementation.md`, `core/modules/review.md`, and `core/adapters/manifest-contract.md`.
- `scripts/validate_conformance.py` and conformance fixtures.
- `adapters/codex/conformance.yaml`, `adapters/codex/rule-mapping.yaml`, relevant Codex Skills, and Codex scenario tests.
- `adapters/generic-prompts/manifest.yaml`, relevant Generic prompts, and Generic scenario tests.
- Release evidence and active packages after any approved contract revision.

## 8. Unresolved items

- Whether clause-level rule IDs or structured scenario IDs provide the better long-term public contract.
- Whether shared scenarios should parse declarative text, use structured companion metadata, or both.
- How much localized documentation consistency should remain exact-test-driven versus editorially reviewed.
- Independent reviewer and non-Windows execution remain unavailable.

## 9. Artifact links

- [Approved Specification](../specs/optional-ticket-testing.md)
- [Approved Ticket Plan](../plans/optional-ticket-testing.md)
- [Ticket 4 Implementation Evidence](optional-ticket-testing-ticket-4.md)
- [Final Review](ask-then-do-it-1.1.0-final-review.md)

## 10. Knowledge Base Change Summary

No durable Project Knowledge Base change is proposed while this report remains Draft. If accepted, the proposed durable modification would be: adapter conformance must prove clause-level behavioral coverage rather than only coarse rule-ID presence. No addition or removal is requested yet.
