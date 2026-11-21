# Generic Direct Implementation Prompt

Prompt ID: `generic.direct-implementation`
Prompt version: `1.5.0`
Required capability: `conversation`
Core version: `1.5.0`

## Required inputs

- An Approved Specification with explicit approval evidence.
- An Approved Ticket Plan with explicit approval evidence.
- One eligible Ticket whose Approved implementation mode is `direct`.
- Repository excerpts and validation information the user chooses to supply.

## Expected outputs

- An `UNEXECUTED DIRECT IMPLEMENTATION GUIDANCE` proposal bounded to one Approved `direct` Ticket.
- A change sequence and the checks a tools-capable host can perform under the Approved test choice.
- A safe handoff containing the Approved artifacts, selected Ticket, proposal, Approved test choice, and capability limitations.

## Instructions

Directly pasting this module selects its workflow stage, not Full or Lite. This is a bounded direct-entry guard, not complete resolver ownership. When composed orchestration supplies a proven current-operation mode, reuse it and MUST NOT re-resolve. Only when directly pasted without a proven current-operation mode, resolve (`MODE-RESOLVE-001`) in order: (1) an unambiguous explicit current-operation instruction selecting Full or Lite; (2) the embedded `Default workflow mode` declaration, when available, if exactly `full` or `lite`; (3) Full fallback for a missing or invalid declaration. If explicit current-operation instructions conflict, ask one clarification and stop. Any local result applies to only the current operation and MUST NOT persist. Continue this stage only when Full resolves. If Lite resolves, stop this Full stage and route to `lite-workflow.md`.

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

The tools-capable host must preserve unrelated changes and inspect the final diff. For `Run existing tests only`, run relevant existing behavioral tests without adding or modifying tests. Record actual commands and outcomes, including failures or unavailable coverage. An unresolved failure prevents an unqualified success claim. For `Skip behavioral tests` and legacy Approved direct Tickets without explicit existing-test permission, do not run behavioral tests. Record `tests: skipped-by-user` only for the skip choice or legacy direct approvals. Report only observed existing-test outcomes; never claim TDD.

End with:

- the capability limitation;
- supplied evidence used;
- the unexecuted direct change proposal;
- Approved artifact, Ticket, and mode references;
- permitted validation;
- the Approved test choice and any unavailable behavioral evidence;
- external test constraints, delivery blocks, and residual risks;
- a Review handoff for a tools-capable host.

The user owns cross-session persistence; save this handoff and re-supply it when the conversation no longer contains it.

## Stop conditions

- Stop at the earliest missing, disputed, or conflicting approval or mode gate.
- Stop after the unexecuted handoff. Do not continue into simulated editing, execution, test results, or completed evidence.
- If supplied evidence contradicts an Approved artifact, stop and return to the earliest affected gate.
