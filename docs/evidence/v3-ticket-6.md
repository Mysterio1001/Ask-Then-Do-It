# Portable AI Development Workflow v3 - Ticket 6 Evidence

Artifact type: Implementation Evidence

Artifact ID: `portable-ai-development-workflow-v3-ticket-6-evidence`

Workflow ID: `grill-me-core-v3`

Core version: `3.0.0`

Status: Completed

## Outcome

Ticket 6 produced and proved the local `3.0.0` Codex and Generic release without installing, publishing, uploading, or mutating a marketplace or personal AI environment.

## TDD evidence

- Red: 25 release tests against the old release state produced 17 failures and 5 errors for the expected missing v3 identity, package inventory, documentation, preservation snapshot, and evidence-gate behavior.
- Green: the final integrated command ran 73 tests in 4.595 seconds with `OK`.
- Refactor: release validation data was centralized in schema version 2, the evidence gate was separated from package construction, and legacy overlap recognition was isolated behind a validated checksum snapshot.

## Acceptance evidence

- Core, both adapters, Plugin manifest, generated Generic manifest, and release identity are `3.0.0`.
- The Codex package contains exactly eight Skills and all pass official validation.
- The Generic package contains nine source prompts, a generated combined entry, and a generated manifest.
- Both adapters pass conformance against all 23 mandatory Core rules.
- Versioned `2.1.0` archives and evidence retain approved hashes.
- Two clean builds produce byte-identical archives and checksum content.
- Both ZIPs match their unpacked directories byte-for-byte and both hashes match `dist/checksums.sha256`.
- Failed, blocked, missing, duplicate, and unknown evidence checks cannot validate a completed release.
- Documentation points to v3 while explaining source, generated output, preserved v2 artifacts, and personal-installation boundaries.
- The release milestone architecture diagnosis completed without mutation and found no release blocker.

## Evidence links

- [Full 3.0.0 release evidence](grill-me-release-3.0.0.md)
- [Machine-readable validation ledger](grill-me-release-3.0.0.json)
- [Release architecture diagnosis](v3-release-architecture-diagnosis.md)
- [Approved v3 Specification](../specs/ai-development-skills-v3.md)
- [Approved v3 Ticket Plan](../plans/ai-development-skills-v3.md)

## Limitations

- Final review was non-independent.
- Cross-platform reproducibility beyond the validated Windows environment remains unverified.
- Installation, cachebuster, marketplace configuration, publication, external upload, dedicated provider adapters, and signing remain outside this Ticket.
