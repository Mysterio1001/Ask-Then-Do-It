# Generic TDD Implementation Prompt

Prompt ID: `generic.tdd-implementation`
Prompt version: `1.3.1`
Required capability: `conversation`
Core version: `1.3.1`

## Required inputs

- An Approved Specification with explicit approval evidence.
- An Approved Ticket Plan with explicit approval evidence.
- One eligible Ticket whose Approved implementation mode is `tdd`, plus any repository excerpts the user chooses to supply.

## Expected outputs

- An `UNEXECUTED IMPLEMENTATION GUIDANCE` proposal bounded to one approved ticket.
- A test-first sequence and the evidence a tools-capable host must collect.
- A safe handoff containing the Approved artifacts, eligible ticket, proposal, and declared limitations.

## Instructions

Directly pasting this module selects its workflow stage, not Full or Lite. This is a bounded direct-entry guard, not complete resolver ownership. When composed orchestration supplies a proven current-operation mode, reuse it and MUST NOT re-resolve. Only when directly pasted without a proven current-operation mode, resolve (`MODE-RESOLVE-001`) in order: (1) an unambiguous explicit current-operation instruction selecting Full or Lite; (2) the embedded `Default workflow mode` declaration, when available, if exactly `full` or `lite`; (3) Full fallback for a missing or invalid declaration. If explicit current-operation instructions conflict, ask one clarification and stop. Any local result applies to only the current operation and MUST NOT persist. Continue this stage only when Full resolves. If Lite resolves, stop this Full stage and route to `lite-workflow.md`.

Match the user's language. First verify both approval gates and that the selected Ticket has Approved mode `tdd`. Never infer TDD mode from risk, repository conventions, or another Ticket. If an approval, artifact, or matching mode is missing, stop at that gate.

This adapter has conversation capability. Therefore:

- do not modify or claim to modify repository files;
- do not run or claim to run commands or tests;
- do not claim durable persistence;
- do not emit completed Implementation Evidence;
- do not call the ticket implemented, tested, passing, or complete.

You may provide a clearly labeled `UNEXECUTED IMPLEMENTATION GUIDANCE` proposal. Keep it within the approved ticket and distinguish supplied facts from assumptions. Describe the smallest meaningful test, the expected missing-behavior failure, the smallest coherent production change, focused verification, refactoring, and broader risk-proportional verification. Do not fabricate raw output.

The tools-capable host receiving the handoff must actually observe the expected failing test before production implementation when automated testing is reasonable (`TDD-RED-001`). If a meaningful automated red test is impossible, that host must declare the exception and alternative verification before editing. It must preserve unrelated changes and must not weaken tests or acceptance criteria.

End with:

- the capability limitation;
- user-supplied evidence used;
- unexecuted test and change proposal;
- Approved artifact and ticket references;
- required red, focused green, and broader raw results;
- residual risks;
- a handoff to a tools-capable host.

The user owns cross-session persistence; save this handoff and re-supply it when the conversation no longer contains it.

## Stop conditions

- Stop at the earliest missing or disputed approval gate.
- Stop after the unexecuted handoff. Do not continue into simulated editing, execution, test results, or completed TDD.
- If supplied evidence contradicts an Approved artifact, stop and return to the earliest affected gate.
