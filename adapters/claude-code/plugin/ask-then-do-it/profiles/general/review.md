# Claude Code General profile evidence-based Review

This General profile Full-stage module requires a proven `full` mode, Approved requirements and Specification, the reviewed Ticket and its Approved Ticket mode, final diff and surrounding code, test changes, and raw implementation and verification evidence. Review authorizes diagnosis and reporting, not fixes.

Core rules: REVIEW-EVIDENCE-001, REVIEW-LENSES-001

## Capability and independence

Declare the evidence label before findings and make an honest downgrade:

- With proven `multi_agent`, an Agent tool, and the Plugin reviewer available, delegate to the independent read-only reviewer with raw artifacts but without implementer conclusions. Wait for the reviewer to finish, then validate and integrate findings rather than blindly accepting them.
- With `tools` but no usable reviewer/Agent, perform the Full Review in the same context, label it `non-independent`, and name the unavailable independent evidence.
- With only `conversation` or user excerpts, label it `limited-evidence`, state what repository and tests were not read/run, provide a safe handoff, and must not claim a completed repository Review.

Reviewer availability alone does not block completion when all other gates pass. This is the required independent reviewer and honest downgrade behavior. Lite remains a compact same-context Review and never uses this independence contract.

[SCENARIO: CAP-MULTI-AGENT]

## Review contract

Review the Approved Specification, Approved Ticket mode, final diff/surrounding code, test changes and raw results, and raw evidence. Preserve `tests: skipped-by-user` for direct Tickets and do not run declined tests. Check behavior, regressions, failure paths, security/privacy, test quality, maintainability, and evidence honesty.

Apply all twelve Architecture and Refactoring Lenses in this order: Duplicated Code or Policy; Long Function; Large Module or Class; Long Parameter List; Data Clumps; Primitive Obsession; Feature Envy; Divergent Change; Shotgun Surgery; Message Chains; Leaky Abstraction; Shallow Module. For each, provide evidence and exactly `finding`, `no-finding`, `not-applicable` with reason, or `unverified` with missing evidence.

List actionable findings first by severity (`P0` through `P3`). Each finding gives trigger, impact, evidence, tight location, and remediation direction. Verify that an existing guard does not already address it. Keep local issues here; route only genuinely systemic evidence to diagnostic architecture analysis.

Emit a Review Report. Use the `portable artifact envelope` defined in `orchestration.md`, then add evidence/independence labels, findings, checks performed/unavailable, residual risks, untested areas, and supported completion assessment. Do not turn missing evidence into no-finding and do not modify code.

[CORE: REVIEW-EVIDENCE-001]
[CORE: REVIEW-LENSES-001]
[SCENARIO: FULL-REVIEW]
