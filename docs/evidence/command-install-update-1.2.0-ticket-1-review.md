# Ask Then Do It 1.2.0 Ticket 1 Review

Artifact type: Review Report

Artifact ID: `command-install-update-1-2-ticket-1-review`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Status: Completed

Review label: `non-independent`

Reviewed inputs: Approved 1.2.0 Specification, Approved Ticket Plan, Ticket 1 implementation diff, focused test output, and repository conventions.

## Findings

No actionable finding for Ticket 1. The catalog has one official entry, the approved source URL and subdirectory, a formal `v1.2.0` ref, the required policies, and the required category. The focused validator rejects mutable refs, alternate sources, wrong paths or policies, and duplicate entries. It does not modify personal marketplace state.

## Twelve lenses

1. Duplicated Code or Policy: `no-finding` - one repository catalog owns the marketplace entry.
2. Long Function: `not-applicable` - metadata-only change.
3. Large Module or Class: `not-applicable` - metadata-only change.
4. Long Parameter List: `not-applicable` - no callable interface added.
5. Data Clumps: `no-finding` - source fields are grouped by the marketplace schema.
6. Primitive Obsession: `no-finding` - externally required catalog values are explicit and test-covered.
7. Feature Envy: `not-applicable` - no runtime behavior.
8. Divergent Change: `no-finding` - ownership is limited to marketplace metadata and its contract test.
9. Shotgun Surgery: `no-finding` - no consumer package files were touched.
10. Message Chains: `not-applicable` - no runtime call chain.
11. Leaky Abstraction: `unverified` - live Codex marketplace schema parsing is unavailable because `codex.exe` could not be executed.
12. Shallow Module: `not-applicable` - no module or abstraction added.

## Verification and residual risk

The focused marketplace contract and relevant release-contract tests passed; the validator command and `git diff --check` passed. Live CLI installation, release-builder enforcement, and package exclusion remain unverified and are owned by later Tickets.

## Completion assessment

Ticket 1 appears complete within its approved boundary. Handoff is to Ticket 2.
