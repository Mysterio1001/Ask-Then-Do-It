# Architecture Improvement Report Artifact

## Required sections

1. Analysis scope and limitations.
2. System architecture summary.
3. Deletion-analysis results, labeled simulated or explicitly authorized actual analysis.
4. Twelve-lens results.
5. Finding evidence, impact, and confidence.
6. Prioritized improvement proposals.
7. Potentially affected modules.
8. Unresolved items.
9. Artifact links.
10. Knowledge Base Change Summary when durable project knowledge changed.

Every required section MUST appear. Use `not-applicable` with a reason when a section genuinely does not apply.

## States

- `draft`: analysis is proposed and not yet accepted.
- `accepted`: the user accepts the diagnosis and permits Specification work.
- `rejected`: the user declines the diagnosis or proposal.
- `superseded`: a later report replaces this report while preserving traceability.

Changing `draft` to `accepted` requires explicit approval evidence. An accepted report MUST NOT authorize production edits, deletion, refactoring, Ticket implementation, or bypass of the Specification and Ticket Plan gates (`ARCH-REPORT-001`, `ARCH-REFLOW-001`).

The report uses the shared artifact envelope and links its evidence, reviewed scope, limitations, and intended Specification handoff.
