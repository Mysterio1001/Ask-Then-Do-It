# Ask Then Do It 1.2.0 Ticket 5 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `command-install-update-1-2-ticket-5-evidence`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Status: Completed

Inputs: Approved [1.2.0 Specification](../specs/command-install-update-1.2.0.md), completed [Ticket Plan](../plans/command-install-update-1.2.0.md), completed Tickets 1-4, and Ticket 5 with Approved mode `tdd`.

Assumptions: Existing release-evidence tests already provide meaningful Red coverage for missing checks, failed/blocked checks, version mismatch, and unauthorized skipped tests, so no new evidence-validator behavior was needed.

Deferred: Git tag, GitHub Release, push, upload, Plugin installation, personal marketplace mutation, announcement, external CI, additional operating systems, and live target-CLI verification.

Handoff: Ticket 5 Review and maintainer-controlled publication decision.

## Evidence-gate coverage

`tests.release.test_release_evidence` already rejects incomplete or inconsistent completed evidence and accepts only the configured current release version. During Ticket 4 its old synthetic `1.1.0` ledger failed against current `1.2.0`, demonstrating the version gate; the test fixture was then made release-config-driven without weakening any negative case.

## Integrated verification

- Final full discovery with the declared PyYAML development dependency: `Ran 113 tests in 7.758s`; `OK`.
- Marketplace validator: passed for `.agents/plugins/marketplace.json`.
- Native Plugin validator: canonical and packaged Plugin both passed.
- Native Skill validator: all nine canonical and all nine packaged Skills passed (`18/18`).
- Conformance validator: Codex and Generic both passed against Core `1.2.0`.
- Release builder: default `dist/` build completed after all source/document changes.
- Asset inspection: 512x512 icon and 1024x1024 logo have transparent backgrounds, visible padding, centered nonempty subject, and no clipping.
- Release package tests: deterministic double build, ZIP/directory equivalence, SHA-256 verification, asset inclusion, marketplace exclusion, Generic exclusion, localized documentation, README whitelist, and historical-boundary checks all passed.
- `git diff --check`: exit code `0` with no whitespace error.

PyYAML `6.0.3` was installed only into a temporary workspace test directory to satisfy `requirements-dev.txt`; it is not part of source or release packages.

## Completion

All required local checks have accepted evidence. No external release, installation, marketplace mutation, or publication occurred.
