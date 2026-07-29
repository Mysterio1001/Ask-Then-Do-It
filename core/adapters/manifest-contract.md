# Adapter Conformance Manifest

Every adapter MUST provide a machine-readable manifest with:

- `adapter_id`: stable adapter identifier.
- `adapter_version`: adapter semantic version.
- `target`: host or usage mode.
- `core_version`: compatible core version.
- `capabilities`: declared capability profiles.
- `artifact_persistence`: how artifacts are retained.
- `implemented_rules`: every mandatory core rule ID (`ADAPTER-COVERAGE-001`).
- `capability_evidence`: non-empty validation evidence for every declared profile.
- `validation.status`: current validation claim.
- `validation.environment`: tested environment.
- `validation.commands`: reproducible checks.

Capability profiles are cumulative: `tools` includes `conversation`; `multi_agent` includes `conversation` and `tools`.

The shared validator MUST reject missing mandatory rules, unknown rules, incompatible core versions, unknown capabilities, incomplete capability hierarchy, and a declared capability without evidence.
