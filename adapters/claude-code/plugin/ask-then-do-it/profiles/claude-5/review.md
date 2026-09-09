# Claude 5 Evidence-Based Review

Core rules: REVIEW-EVIDENCE-001, REVIEW-LENSES-001, CAP-CLAIM-001

Review the Approved requirements/Specification/Ticket and Approved Ticket mode, final diff, surrounding code, test changes, and raw verification evidence. Missing inputs are unavailable evidence, never assumed success. For `direct`, preserve `tests: skipped-by-user`, do not run/prescribe declined tests, and disclose untested areas.

With proven multi-agent capability, delegate to the Plugin's independent read-only reviewer, give it the raw inputs rather than the implementer's verdict, wait for completion, then verify and integrate its output. Independence exists only if that reviewer did not implement the change and was not anchored by conclusions. If the reviewer is unavailable, perform the Full Review in the main context and label it `non-independent`; this alone is not blocking. With conversation/user excerpts only, label the result `limited-evidence`, identify unread repository and unexecuted tests, and provide a safe handoff.

Check specification compliance, correctness/regression, failures, security/privacy, test quality, maintainability, and scope. Apply all twelve Architecture and Refactoring Lenses in canonical order: Duplicated Code or Policy; Long Function; Large Module or Class; Long Parameter List; Data Clumps; Primitive Obsession; Feature Envy; Divergent Change; Shotgun Surgery; Message Chains; Leaky Abstraction; Shallow Module. Give every lens exactly one evidence-backed result: `finding`, `no-finding`, `not-applicable` with reason, or `unverified` with missing evidence.

Validate each finding's trigger, impact, evidence, guard, and tight location; rank P0, P1, P2, or P3 and report findings first. Treat Review as diagnosis, not fix authority. Emit the common Review Report envelope, independence label, lens results, verification/unavailable evidence, risks/untested areas, and completion assessment. Route systemic evidence to diagnostic architecture analysis only.

Lite never uses this Full reviewer path; its stage retains same-context compact Review and correction approval.

A conversation-only result must not claim a completed repository Review.
