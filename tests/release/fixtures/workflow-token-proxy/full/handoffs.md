## Requirement gate

The complete Requirement Decision Record and Knowledge Base Change Summary are ready. Do you approve exactly this requirement and these displayed knowledge changes so Specification work may begin?

## Specification gate

The approved requirement is represented by the complete Specification above without prescribing production code. Do you approve it for Ticket Planning?

## Test-choice and plan gate

The plan contains one Ticket. I recommend Add tests because the change affects an existing command branch and backward compatibility; this adds focused test work, while declining leaves the success and boundary paths without behavioral evidence. After recording your Add tests choice as `tdd`, do you approve the complete Ticket definition and mapped mode?

## Implementation handoff

Ticket 1 is approved in `tdd` mode. Hand off the approved Specification, Ticket Plan, repository instructions, relevant code and tests, and current diff to `implement-tdd`.

## Review handoff

Implementation Evidence is complete. Hand the approved artifacts, final diff, surrounding code, focused test changes, and raw verification results to a fresh `review-code` context.
