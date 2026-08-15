# Ask Then Do It Generic Guide

This guide explains how to use Ask Then Do It with Gemini or another AI service that accepts long text. The Generic package does not require a Plugin; you paste the workflow into a conversation.

## Download and extract

[Download ask-then-do-it-generic-1.3.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-generic-1.3.0.zip) and extract it.

The main files in the package are:

- `START-HERE.en.md`: quick usage instructions.
- `generic-workflow.md`: the complete workflow for normal use.
- `prompts/`: eleven stage-specific modules.
- `LICENSE` and `THIRD_PARTY_NOTICES.md`: license and attribution information.

## Quick start

Begin every new conversation this way:

1. Open `generic-workflow.md`.
2. Copy the entire file and paste it into a new AI conversation.
3. Describe what you want to accomplish and your preferred language.
4. To continue earlier Full work, also paste the important Full documents you saved.

For example:

```text
I want to build an appointment website.
Please respond in English.
```

The AI's first effective response resolves the workflow mode and follows that mode's question and approval rules; you do not need to enter a separate start command.

## Workflow mode configuration

For each operation, the pasted workflow resolves its mode in this order:

1. An explicit instruction for the current operation, such as "use Full this time" or "use Lite this time."
2. The embedded default-mode declaration.
3. Full fallback.

Near the beginning of `generic-workflow.md`, edit the single declaration to exactly one of these lines:

- `Default workflow mode: full`
- `Default workflow mode: lite`

A missing or unsupported declaration selects Full. An explicit override affects only the current operation and does not modify the declaration. A new session starts from the declaration pasted into that conversation unless you give another explicit instruction. The Generic package does not read either Codex Config file. See the [Full and Lite workflow guide](getting-started-simple.en.md) for both mode lifecycles.

Generic remains honest about host capabilities. On a conversation-only host, it cannot inspect a repository, edit files, run commands or tests, persist state, report observed validation, or perform an independent Review. A service with additional tools may act only within the capabilities it actually provides.

## Full mode approval points

In Full mode, the AI asks exactly one requirement question at a time. The first requirements question and each later question include a recommended answer and the main tradeoff. Full uses three approval gates:

1. The requirements are clear.
2. The specification correctly describes the expected result.
3. The Ticket plan is ready to execute.

Before the third approval, the AI first lists every Ticket and gives each one a test recommendation. For every Ticket, it warns that adding tests may increase work time while declining them lowers behavioral-verification confidence. In one response, you decide whether to add tests to every Ticket: add them to all, add them to none, or name only the Tickets that should have tests. There is no default. If a partial answer does not resolve the rest, the AI asks only about the unresolved Tickets.

After approval, a Ticket with tests is internally recorded as `tdd` and follows the TDD module. A Ticket without tests is recorded as `direct` and follows `direct-implementation.md`, which provides implementation guidance without creating or running behavioral tests. Review must retain `tests: skipped-by-user` for the direct path. The workflow moves to implementation only after the third approval. If you request changes, the AI remains at the current stage and revises the material.

## Lite mode questions and approval

Lite may ask no questions when the supplied evidence resolves every blocker. Otherwise, each round asks at most three blocking questions. It then presents one Change Brief and waits for one approval before implementation.

## Capability limits

The Generic package guides the workflow through conversation. It cannot directly edit your files or run tests. It may provide suggestions, documents, or implementation content, but actual file operations depend on the tools offered by your AI service.

Review is based only on the code, documents, and test results you provide in the conversation. If information is missing, the AI should state what cannot currently be verified.

## Save your progress

A new conversation may not remember earlier messages. Continuation works differently in each mode.

### Full

Full creates durable workflow documents. Save the important documents created at each Full stage, including:

- Requirements record.
- Project Knowledge Base.
- Specification.
- Ticket plan, including whether to add tests to each Ticket and its internal route.
- Review or architecture improvement report.

To continue Full in a new conversation:

1. Paste `generic-workflow.md` again.
2. Paste the complete saved documents.
3. Explain what you want to continue or change.

The AI checks the supplied material and proceeds to the first unfinished Full stage.

### Lite

A new Lite session resolves the workflow mode again from the current instruction and the declaration pasted into that conversation. Lite does not persist its Change Brief, approval, progress, or Review, so it cannot resume that unpersisted workflow state. It reconstructs a new Change Brief from available repository state and user input.

## Eleven advanced modules

Use `generic-workflow.md` in most cases. Once you know the workflow, you can paste a specific module from `prompts/`:

Generic is not always Lite. Pasting a module selects a stage, not a workflow mode; the established mode precedence and outcomes do not change. `bootstrap.md` and `orchestration.md` own the complete mode resolver.

The other nine standalone modules include the same bounded, minimal direct-entry guard only because each can be pasted without that resolver; this does not transfer complete resolver ownership. A mode already proven by composed orchestration is reused. Only an unproven direct paste applies `explicit operation instruction > available embedded declaration > Full fallback`. Conflicting instructions pause for clarification. An invalid declaration selects Full; the result is not persisted. Resolved Lite routes to `lite-workflow.md`. Direct entry to `lite-workflow.md` with resolved Full routes to `orchestration.md`.

| Prompt | Purpose |
| --- | --- |
| `bootstrap.md` | Identify current progress and the next stage |
| `orchestration.md` | Coordinate the complete workflow |
| `lite-workflow.md` | Guide the complete Lite lifecycle after mode resolution |
| `requirements.md` | Ask one requirements question at a time |
| `documented-requirements.md` | Clarify requirements and maintain long-term project knowledge |
| `specification.md` | Turn approved requirements into a specification |
| `ticket-planning.md` | Split the specification into vertical Tickets and collect all add-tests choices in one response |
| `direct-implementation.md` | Provide direct implementation guidance without behavioral tests |
| `tdd-implementation.md` | Prepare tests and implementation for each Ticket |
| `review.md` | Review the material supplied in the conversation |
| `architecture-improvement.md` | Analyze architecture problems and improvement options |

## License and attribution

Ask Then Do It is an independent project inspired by Matt Pocock's skills repository. It is not affiliated with or endorsed by Matt Pocock. See `LICENSE` and `THIRD_PARTY_NOTICES.md` in the repository or package for complete information.


[Back to README](../../README.md)
