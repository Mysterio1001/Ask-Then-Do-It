# Grill Me 1.0.0 — Ticket 4 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `grill-me-1-0-ticket-4-evidence`

Workflow ID: `grill-me-clean-slate-1-0`

Core version: `1.0.0`

Status: Completed

## Inputs

- Approved [Clean-slate 1.0.0 Specification](../specs/grill-me-clean-slate-1.0.0.md).
- Approved [Clean-slate 1.0.0 Ticket Plan](../plans/grill-me-clean-slate-1.0.0.md).
- Completed [Ticket 3 evidence](grill-me-1.0.0-ticket-3.md).

## Outcome

The Generic source contract and generated combined workflow now require fresh requirement work to begin in the same effective response as bootstrap. After a concise capability and stage declaration, the model asks exactly one high-impact question in the user's language and includes a recommended answer and principal tradeoff. It must not stop after status, promise to ask later, or ask the user to say "start".

The Generic package now includes `START-HERE.zh-TW.md` beside `generic-workflow.md`. The guide explains one-paste use, the expected first response, Conversation-only limits, user-owned Markdown persistence, and resumed workflow behavior.

## Expected Red evidence

Command:

```powershell
python -m unittest tests.generic.test_generic_prompts tests.release.test_generic_release tests.release.test_documentation -v
```

Observed before implementation: `Ran 26 tests`; three failures and one error. They identified the deferred fresh bootstrap, missing start-guide declaration and package file, and missing first-response human documentation.

## Green evidence

The same focused command observed: `Ran 26 tests`; `OK`.

The default builder then observed: `Built codex, generic release 1.0.0`.

## Preserved boundaries

- Resumed workflow artifacts remain validated and completed stages are not restarted.
- Explicit user module selection remains authoritative within safety and approval gates.
- Conversation-only mode still cannot claim repository access, mutation, command execution, completed TDD, independent Review, actual deletion experiments, or durable persistence.
- All nine canonical prompt sources remain English and provider-neutral; the human package guide is Traditional Chinese.

## Assumptions

- Model responses can vary stylistically, but the required content and stop boundary are normative in the combined and modular prompt contracts.

## Deferred

- Final complete suite, reproducibility, ZIP equivalence, checksum, architecture diagnosis, Review, and release evidence: Ticket 5.

## Handoff

Proceed to Ticket 5 and validate the two final consumer packages as one release set.
