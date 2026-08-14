# Generic Direct Implementation Prompt

Prompt ID: `generic.direct-implementation`
Prompt version: `1.2.0`
Required capability: `conversation`
Core version: `1.2.0`

## Required inputs

- An Approved Specification with explicit approval evidence.
- An Approved Ticket Plan with explicit approval evidence.
- One eligible Ticket whose Approved implementation mode is `direct`.
- Repository excerpts and non-test validation information the user chooses to supply.

## Expected outputs

- An `UNEXECUTED DIRECT IMPLEMENTATION GUIDANCE` proposal bounded to one Approved `direct` Ticket.
- A no-behavioral-test change sequence and the non-test evidence a tools-capable host may collect.
- A safe handoff containing the Approved artifacts, selected Ticket, proposal, skipped-test disclosure, and capability limitations.

## Instructions

Match the user's language. Verify both approval gates, completed dependencies, and the selected Ticket's Approved `direct` mode. Never infer direct mode from silence, repository conventions, risk, or another Ticket.

This adapter has conversation capability. Therefore:

- do not modify or claim to modify repository files;
- do not create or modify behavioral tests;
- do not run or claim to run commands or tests;
- do not claim durable persistence;
- do not emit completed Direct Implementation Evidence;
- do not call the Ticket implemented, validated, passing, or complete.

Provide only clearly labeled `UNEXECUTED DIRECT IMPLEMENTATION GUIDANCE`. Keep it within the Approved Ticket, distinguish supplied facts from assumptions, describe the smallest coherent production change, and identify relevant lint, type-check, build, static validation, or equivalent non-behavioral checks for a tools-capable host. Do not fabricate raw output.

If an external CI, hosting, or release system independently requires or executes behavioral tests, disclose the constraint and any delivery block. The workflow must not claim that `direct` bypasses the external system, and must not instruct the tools-capable host to silently run the declined tests.

The tools-capable host receiving the handoff must preserve unrelated changes, must not create, modify, or execute behavioral tests, and must record raw non-test results, final-diff inspection, `tests: skipped-by-user`, unavailable behavioral evidence, and residual risks. It must not use Red, Green, passing-test, test-verified, or TDD-complete claims.

End with:

- the capability limitation;
- supplied evidence used;
- the unexecuted direct change proposal;
- Approved artifact, Ticket, and mode references;
- permitted non-test validation;
- `tests: skipped-by-user` and unavailable behavioral evidence;
- external test constraints, delivery blocks, and residual risks;
- a Review handoff for a tools-capable host.

The user owns cross-session persistence; save this handoff and re-supply it when the conversation no longer contains it.

## Stop conditions

- Stop at the earliest missing, disputed, or conflicting approval or mode gate.
- Stop after the unexecuted handoff. Do not continue into simulated editing, execution, test results, or completed evidence.
- If supplied evidence contradicts an Approved artifact, stop and return to the earliest affected gate.
