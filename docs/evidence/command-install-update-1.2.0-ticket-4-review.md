# Ask Then Do It 1.2.0 Ticket 4 Review

Artifact type: Review Report

Artifact ID: `command-install-update-1-2-ticket-4-review`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Status: Completed

Review label: `non-independent`

Reviewed inputs: Approved 1.2.0 Specification, Approved Ticket Plan, final Ticket 4 diff, release builder and validators, focused Red/Green evidence, 66-test release result, generated packages, ZIP inventories, and checksums.

Assumptions: The same context implemented and reviewed Ticket 4; no isolated reviewer context is available.

Deferred: Live target-CLI behavior, external publication, and non-Windows verification.

Handoff: Ticket 5 integrated validation.

## Findings

No actionable finding. Marketplace/version drift fails before output, prior generated releases are replaced only after checksum and ZIP-equivalence verification, and the resulting package boundaries match the Approved Specification.

## Twelve lenses

1. Duplicated Code or Policy: `no-finding` - marketplace structure is centralized in `validate_marketplace.py`; builder reuses it with a release-derived ref.
2. Long Function: `no-finding` - the new prior-output validator is bounded to one validation responsibility.
3. Large Module or Class: `no-finding` - no new class or broad subsystem was introduced.
4. Long Parameter List: `no-finding` - new functions accept cohesive path/config/version inputs.
5. Data Clumps: `no-finding` - asset path and size pairs are kept together in one mapping.
6. Primitive Obsession: `no-finding` - semver, paths, hashes, and policies are constrained by validators.
7. Feature Envy: `no-finding` - marketplace validation owns catalog rules; builder owns release coordination.
8. Divergent Change: `no-finding` - the new validator changes only for marketplace contract changes.
9. Shotgun Surgery: `unverified` - active version declarations are intentionally distributed; milestone diagnosis evaluates this system-level concern.
10. Message Chains: `no-finding` - validation calls are direct and shallow.
11. Leaky Abstraction: `no-finding` - builder receives a domain error and converts it to its release error boundary.
12. Shallow Module: `no-finding` - `validate_existing_output_set` hides checksum, inventory, symlink, and ZIP-equivalence checks behind one release operation.

## Verification and completion

Focused and broader release tests passed, the default build completed, checksums match, and `git diff --check` passed. Ticket 4 appears complete. Residual risk is limited to deferred live CLI and external publication behavior.
