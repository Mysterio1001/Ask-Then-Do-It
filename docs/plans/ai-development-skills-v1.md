# AI Development Skills Suite - v1 Plan

Status: Historical (Previously Approved)

## Approved scope

Implement the six skills defined by the former Codex-only v1 specification. The user approved the requirements, modular architecture, human gates, TDD policy, independent review, safe parallelism, localization, maintainer comments, and distribution approach.

This plan is preserved for project history. It does not authorize v2 implementation.

## Tickets

### Ticket 1 - Initialize the six discoverable skills

Deliverable: six valid skill directories with generated UI metadata.

- Initialize each directory with the official skill-creator initializer.
- Use concise, distinct display names, short descriptions, and default prompts.
- Do not create unused scripts, references, assets, examples, or per-skill README files.

Verification: all expected directories and generated metadata files exist.

Dependencies: none.

Parallel safety: initialization is independent per directory, but run sequentially to keep failure diagnosis simple.

### Ticket 2 - Implement requirement discovery and orchestration

Deliverable: `ai-dev-workflow` and `grill-requirements` behavior.

- Encode stage detection, three approval gates, resume behavior, read-only reconnaissance, one-question grilling, recommendations, decision tracking, and escalation back to earlier gates.
- Keep the umbrella thin; delegate stage-specific procedures instead of duplicating them.

Verification: inspect both skills against the triggering examples and acceptance criteria.

Dependencies: Ticket 1.

Parallel safety: these two skills share the stage contract and should be authored together.

### Ticket 3 - Implement specification and vertical planning

Deliverable: `write-spec` and `plan-tickets` behavior.

- Encode repository-aware artifact paths and stable behavioral specification content.
- Encode vertical slices, dependencies, completion criteria, verification, and safe-parallelism analysis.

Verification: walk a sample feature from confirmed decisions to a spec and independently executable tickets.

Dependencies: Ticket 1 and the gate contract from Ticket 2.

Parallel safety: may be drafted independently after the shared artifact contract is fixed; final consistency review is required.

### Ticket 4 - Implement test-driven execution and independent review

Deliverable: `implement-tdd` and `review-code` behavior.

- Encode red-green-refactor evidence, exception handling, focused and broader verification, scope control, and return-to-spec behavior.
- Encode independent subagent review, raw-evidence isolation, severity ordering, precise locations, and no-findings reporting.

Verification: inspect the TDD invariant and review fallback against the specification.

Dependencies: Tickets 1-3.

Parallel safety: the skills can be drafted independently after artifact contracts are settled; verify their handoff fields together.

### Ticket 5 - Validate the suite and prepare installation

Deliverable: a locally validated, internally consistent skill suite.

- Run the official validator on all six skill directories.
- Check frontmatter trigger coverage and UI metadata consistency.
- Search for placeholders, stale names, unused resources, accidental implementation code in spec instructions, and missing approval gates.
- Forward-test representative invocations if it can be done without contaminating results or changing external systems.
- Install the validated skills into the personal Codex skills directory after obtaining any required filesystem approval.

Verification: all validators pass; the final file inventory contains only intended artifacts; installed copies match the validated source.

Dependencies: Tickets 1-4.

Parallel safety: final validation and installation are sequential integration work.
