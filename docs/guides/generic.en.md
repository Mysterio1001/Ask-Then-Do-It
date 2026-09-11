# Ask Then Do It Generic guide

For Gemini and other AI services that accept long text. Paste the workflow; no Plugin installation is needed.

These are the 1.4.0 installation/download targets. If remote artifacts are unavailable, wait for publication.

## Installation and preparation

Download and extract the package. Keep `generic-workflow.md` and `prompts/`.

[Download ask-then-do-it-generic-1.4.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0/ask-then-do-it-generic-1.4.0.zip)

## Getting started

In every new conversation, paste the **entire** `generic-workflow.md`, then describe your task, for example:

```text
Help me build a booking website. Please use English.
```

## Full / Lite modes

**Full** keeps requirements, specification, and a Ticket Plan, with three approvals before implementation. **Lite** suits clearly scoped changes and uses a short Change Brief with one approval.

Say “Use Full for this operation” or “Use Lite for this operation.” This affects only the current operation.

Keep one declaration, `Default workflow mode: full`, or change it to `Default workflow mode: lite`. This setting belongs to the pasted text; it does not read Codex or Claude Config. Missing or invalid declarations select Full.

For the full workflow, test choices, and saving progress, see the [beginner guide](getting-started-simple.en.md)。

## Available commands

Normally use `generic-workflow.md`. Advanced users can paste one module from `prompts/`; this does not bypass mode resolution or approvals.

<details>
<summary>Show advanced entries</summary>

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

</details>

## Updating and removal

Get the newer ZIP and paste its workflow in a new conversation. To stop using it, stop pasting it; optionally delete the downloaded copy. Keep your project documents separately.

## Common questions

- Missing progress in a new conversation: paste the workflow again. To continue Full, also provide saved requirements, specification, and Ticket Plan. Lite does not persist state across conversations.
- AI cannot edit files or run tests: available capabilities depend on the service and tools. With chat only, apply the output yourself and supply the results.

Report remaining issues through [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues). Include the project version, AI service/host, platform, and reproduction steps.

## License and attribution

This independent project is inspired by Matt Pocock’s skills repository and is not affiliated with or endorsed by him. See `LICENSE` and `THIRD_PARTY_NOTICES.md` for license and attribution.

[Back to README](../../README.md)
