# Grill Me v3 Release Architecture Diagnosis

Artifact type: Architecture Improvement Report

Artifact ID: `grill-me-v3-release-architecture-diagnosis`

Workflow ID: `grill-me-core-v3`

Core version: `3.0.0`

Status: draft

Inputs:

- `release/release.json`
- `scripts/build_release.py`
- `scripts/validate_release_evidence.py`
- `tests/release/`
- Generated `dist/` inventories and checksums
- Ticket 6 validation outcomes recorded on 2026-07-29

Assumptions:

- The declared scope is the local release-building and release-evidence subsystem, not the model-neutral workflow behavior inside packaged prompts and Skills.
- Existing runtime packages are generated output; canonical source remains under `core/`, `adapters/`, `release/`, and `scripts/`.
- This is a non-independent, tool-assisted diagnosis by the implementation agent.

Deferred:

- Any refactoring proposal requires a separate Approved Specification, vertical Ticket Plan, and TDD evidence.
- Release signing and remote publication remain outside the approved v3 scope.

Handoff:

- Treat the release as unblocked by this diagnosis.
- If maintainers choose to reduce release-builder change concentration, begin a new Specification from the proposals below; do not refactor directly from this report.

Approval:

- Not applicable. This initial report is `draft` and has not been accepted by the user.

## 1. Analysis scope and limitations

The analysis covered release identity, source/package validation, deterministic composition, preservation of the validated `2.1.0` artifacts, atomic output replacement, evidence gating, release tests, and generated v3 inventories. Evidence came from read-only source inspection, dependency searches, file metrics, 72 passing automated tests, official validation of eight packaged Skills, Plugin validation, both adapter conformance checks, two clean builds, byte comparison, ZIP equivalence, and SHA-256 verification.

No version history was available because the workspace is not a Git repository. No actual deletion experiment was authorized or performed. Marketplace, personal installation, network publication, and external-provider behavior were not inspected.

## 2. System architecture summary

`release/release.json` is the declarative release contract. `scripts/build_release.py` validates the contract and canonical adapter declarations, composes two minimal packages in staging, validates inventories and ZIP equivalence, writes checksums, and atomically replaces only recognized managed outputs. It recognizes a validated legacy overlap through the old Plugin manifest plus a versioned checksum snapshot, allowing `3.0.0` to replace unversioned pointers while preserving versioned `2.1.0` artifacts.

`scripts/validate_release_evidence.py` is a separate fail-closed gate. It accepts a completed evidence record only when every check configured by `required_validation_checks` appears exactly once with status `passed`, a command, and an outcome. `tests/release/` independently exercises identity, inventory, composition, collision safety, prior-release preservation, reproducibility, checksums, documentation, and evidence-gate behavior.

The primary release builder is a 667-line standard-library module with 25 internal functions. Its public interface remains one command and a small set of flags, so it is operationally deep even though its internal change surface is concentrated.

## 3. Deletion-analysis results

Analysis type: simulated deletion only. No file was removed, renamed, moved, or rewritten for this analysis.

- If `release/release.json` disappeared, the builder would stop at configuration loading, version and inventory ownership would become undefined, and no new release could be proven. Existing archives would remain usable.
- If `scripts/build_release.py` disappeared, README and guide commands plus release tests would fail, and packages could no longer be reproduced from canonical source. Existing `dist/` output would remain readable but would no longer be trustworthy as reproducible output.
- If `scripts/validate_release_evidence.py` disappeared, its tests and the fail-closed evidence check would fail. Package creation would still work, but a completed release status would lack the configured machine-checkable gate.
- If `dist/checksums-2.1.0.sha256` disappeared from a v2-to-v3 workspace, the v2 preservation contract would fail and the builder could not safely classify the legacy unversioned overlap. The validated v2 archives themselves would remain, but migration would stop rather than overwrite uncertain content.
- If either adapter source disappeared, source validation would fail before commit and the prior valid release would remain intact.

## 4. Twelve-lens results

1. **Duplicated Code or Policy - no-finding.** Archive names and hashes are repeated in tests and documentation as independent public-contract assertions; no conflicting release policy was found.
2. **Long Function - finding.** `load_config` validates several independent schema areas in one function. Evidence: `scripts/build_release.py:116`. Impact: future schema changes require editing a broad validation block. Confidence: high.
3. **Large Module or Class - finding.** `scripts/build_release.py` owns contract parsing, both package builders, deterministic ZIP behavior, legacy recognition, output validation, and atomic commit in 667 lines. Impact: unrelated release concerns converge on one module. Confidence: high. This is not a release blocker because the CLI is intentionally narrow and tests cover each boundary.
4. **Long Parameter List - no-finding.** Inspected interfaces use small parameter sets; the longest internal calls remain understandable and keyword arguments mark safety-sensitive choices.
5. **Data Clumps - no-finding.** Repeated `root/config/selected` values represent explicit build context rather than an observed domain object whose absence caused defects.
6. **Primitive Obsession - finding.** The strict release contract is represented as nested untyped dictionaries and string identifiers. Impact: internal code relies on repeated string-key access after runtime validation. Confidence: medium; strict validation and tests substantially reduce current risk.
7. **Feature Envy - no-finding.** Package-specific behavior reads its own configuration section and source tree; no function materially manipulates another module's private state.
8. **Divergent Change - finding.** The builder changes for schema evolution, Codex packaging, Generic composition, legacy migration, archive mechanics, and atomic filesystem behavior. Impact: multiple reasons to change are concentrated in one file. Confidence: high.
9. **Shotgun Surgery - finding.** A release-version change intentionally touches release configuration, Plugin identity, generated paths, tests, and human documentation. Impact: omissions can leave stale paths. Confidence: high. Current contract and documentation tests catch this, so it is not a blocking defect.
10. **Message Chains - no-finding.** Nested configuration access is short and local; no long runtime navigation chain or cascading object graph was found.
11. **Leaky Abstraction - finding.** Legacy recognition derives `grill-me-<version>.zip` and `generic-prompts-<version>` conventions inside the builder rather than from explicit legacy metadata. Evidence: `validated_legacy_overlap`. Impact: a future package rename would require coordinated code changes. Confidence: high; current package ID is fixed, so v3 behavior is correct.
12. **Shallow Module - no-finding.** Both CLIs hide substantial validation and safety behavior behind simple commands. Their external interfaces are smaller than the complexity they encapsulate.

## 5. Finding evidence, impact, and confidence

The material architecture pattern is change concentration, not a release correctness failure. `build_release.py` remains a deep command module but combines multiple internal reasons to change. The evidence gate is already separated, which limits further growth. Automated failure cases cover duplicate, missing, stale, and extra inventory; unmanaged collisions; failed rebuild preservation; legacy hashes; two-build reproducibility; ZIP equivalence; and failed or blocked evidence states.

No finding invalidates the observed release outputs. Residual maintainability risk is medium; release integrity risk after the current validation matrix is low. The diagnosis is non-independent because the same agent implemented and inspected the release changes.

## 6. Prioritized improvement proposals

1. **Medium priority:** Specify a future internal separation of release-contract parsing, package composition, and atomic output management while preserving the one-command public interface.
2. **Medium priority:** Specify explicit legacy-release metadata instead of deriving historical package names inside `validated_legacy_overlap`.
3. **Low priority:** Evaluate typed immutable configuration objects after parsing so package builders no longer depend on nested string-key dictionaries.
4. **Low priority:** Keep independent contract strings in tests and documentation; do not deduplicate them into production helpers that would weaken verification independence.

These are diagnosis proposals only. None is authorized for implementation by this report.

## 7. Potentially affected modules

- `release/release.json`
- `scripts/build_release.py`
- `scripts/validate_release_evidence.py`
- `tests/release/test_release_contract.py`
- `tests/release/test_codex_release.py`
- `tests/release/test_generic_release.py`
- `tests/release/test_release_safety.py`
- `tests/release/test_release_evidence.py`
- Root and provider-specific usage documentation

## 8. Unresolved items

- Change-frequency evidence is unavailable without version history.
- Cross-platform reproducibility beyond the validated Windows environment is unverified.
- Filesystem failure behavior on non-Windows platforms is unverified.
- Release signing, provenance, marketplace installation, and external publication are intentionally unavailable in this scope.

## 9. Artifact links

- [v3 Specification](../specs/ai-development-skills-v3.md)
- [v3 Ticket Plan](../plans/ai-development-skills-v3.md)
- [Ticket 5 evidence](v3-ticket-5.md)
- `release/release.json`
- `scripts/build_release.py`
- `scripts/validate_release_evidence.py`
- `dist/checksums.sha256`
- `dist/checksums-2.1.0.sha256`

## 10. Knowledge Base Change Summary

Not applicable. The diagnosis identified release-subsystem implementation details and future refactoring options but introduced no new durable business term, product boundary, or approved architecture decision requiring Project Knowledge Base synchronization.
