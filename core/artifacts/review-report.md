# Review Report Artifact

## Required content

- Reviewed Specification, Ticket, Approved implementation mode, diff, and verification references.
- Review label: `independent`, `non-independent`, or `limited-evidence`.
- Findings ordered by severity, each with trigger, impact, evidence, and location when available.
- Results for all twelve Architecture and Refactoring Lenses, each labeled `finding`, `no-finding`, `not-applicable`, or `unverified` with the required evidence or reason.
- Verification performed and unavailable evidence.
- Residual risks and untested areas.
- Completion assessment against the approved ticket.
- For a `direct` Ticket: `tests: skipped-by-user`, unavailable behavioral evidence, untested areas, external test constraints, and residual risk without passing-test, automatic declined-test prescriptions, or TDD-complete claims.

If no actionable findings exist, state that explicitly without implying unavailable evidence was checked.

Project-specific lenses MAY follow the core results but MUST NOT replace, rename incompatibly, or silently omit any core lens.
