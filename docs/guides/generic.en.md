# Ask Then Do It Generic Guide

This guide explains how to use Ask Then Do It with Gemini or another AI service that accepts long text. The Generic package does not require a Plugin; you paste the workflow into a conversation.

## Download and extract

[Download ask-then-do-it-generic-1.1.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.1.0/ask-then-do-it-generic-1.1.0.zip) and extract it.

The main files in the package are:

- `START-HERE.en.md`: quick usage instructions.
- `generic-workflow.md`: the complete workflow for normal use.
- `prompts/`: ten stage-specific modules.
- `LICENSE` and `THIRD_PARTY_NOTICES.md`: license and attribution information.

## Quick start

Begin every new conversation this way:

1. Open `generic-workflow.md`.
2. Copy the entire file and paste it into a new AI conversation.
3. Describe what you want to accomplish and your preferred language.
4. To continue earlier work, also paste the important documents you saved.

For example:

```text
I want to build an appointment website.
Please respond in English.
```

The AI's first effective response states the current stage and then asks the first requirements question. Each question includes a recommended answer and the main tradeoff; you do not need to enter a separate start command.

## Approval points

Ask Then Do It pauses for your explicit approval at three points:

1. The requirements are clear.
2. The specification correctly describes the expected result.
3. The Ticket plan is ready to execute.

Before the third approval, the AI first lists every Ticket and gives each one a test recommendation. For every Ticket, it warns that adding tests may increase work time while declining them lowers behavioral-verification confidence. In one response, you decide whether to add tests to every Ticket: add them to all, add them to none, or name only the Tickets that should have tests. There is no default. If a partial answer does not resolve the rest, the AI asks only about the unresolved Tickets.

After approval, a Ticket with tests is internally recorded as `tdd` and follows the TDD module. A Ticket without tests is recorded as `direct` and follows `direct-implementation.md`, which provides implementation guidance without creating or running behavioral tests. Review must retain `tests: skipped-by-user` for the direct path. The workflow moves to implementation only after the third approval. If you request changes, the AI remains at the current stage and revises the material.

## Capability limits

The Generic package guides the workflow through conversation. It cannot directly edit your files or run tests. It may provide suggestions, documents, or implementation content, but actual file operations depend on the tools offered by your AI service.

Review is based only on the code, documents, and test results you provide in the conversation. If information is missing, the AI should state what cannot currently be verified.

## Save your progress

A new conversation may not remember earlier messages. Save the important documents created at each stage, including:

- Requirements record.
- Project Knowledge Base.
- Specification.
- Ticket plan, including whether to add tests to each Ticket and its internal route.
- Review or architecture improvement report.

To continue in a new conversation:

1. Paste `generic-workflow.md` again.
2. Paste the complete saved documents.
3. Explain what you want to continue or change.

The AI checks the supplied material and proceeds to the first unfinished stage.

## Ten advanced modules

Use `generic-workflow.md` in most cases. Once you know the workflow, you can paste a specific module from `prompts/`:

| Prompt | Purpose |
| --- | --- |
| `bootstrap.md` | Identify current progress and the next stage |
| `orchestration.md` | Coordinate the complete workflow |
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
