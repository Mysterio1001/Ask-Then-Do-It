# Evidence-Based Review

## Purpose

Evaluate delivered changes against approved intent and raw evidence, prioritizing defects the author should act on.

## Contract

- Review the approved Specification, ticket, diff, surrounding code, test changes, and raw verification results (`REVIEW-EVIDENCE-001`).
- Check specification compliance, correctness, regressions, failure handling, security, privacy, test quality, and maintainability.
- Apply [all twelve Architecture and Refactoring Lenses](../references/architecture-refactoring-lenses.md) to the changed code and its relevant impact area (`REVIEW-LENSES-001`).
- Record evidence and one permitted outcome for every lens. Never use `no-finding` when evidence is missing.
- Treat this lens pass as a focused change review rather than a system-wide architecture diagnosis.
- Validate each finding with a trigger, impact, evidence, and precise location when available.
- Report actionable findings first in descending severity.
- State residual risks and unavailable evidence even when no findings exist.
- Treat review as diagnosis, not authorization to implement fixes.

## Independence labels

- Claim `independent` only when a `multi_agent` reviewer context did not implement the change and was not anchored by the implementer's conclusions.
- Label review `non-independent` when the same context implemented the change.
- Label review `limited-evidence` when only user-supplied excerpts or artifacts are available.
