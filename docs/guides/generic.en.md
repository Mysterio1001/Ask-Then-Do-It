# Ask Then Do It Generic guide

For Claude Desktop Skills and other AI services that accept long text. Upload the ZIP as a Skill in Claude Desktop, or paste the workflow when using a text-only host.

These are the 1.4.1 installation/download targets. If remote artifacts are unavailable, wait for publication.

## Installation and preparation

Download the package. In Claude Desktop, upload the ZIP through the Skills interface. It contains one package folder with `SKILL.md` at that folder's root, starting with YAML `name` and `description` fields. For a text-only host, extract the package and keep `SKILL.md` and `prompts/`.

[Download ask-then-do-it-generic-1.4.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.1/ask-then-do-it-generic-1.4.1.zip)

## Getting started

In Claude Desktop, wait for the upload and security scan to complete, enable the Skill, and ask to use Ask Then Do It. Claude loads the instructions when the Skill is selected. For a text-only host, paste the **entire** `SKILL.md` into every new conversation, then describe your task, for example:

```text
Use Ask Then Do It to help me plan a booking website. Please use English.
```

## Full / Lite modes

**Full** keeps requirements, specification, and a Ticket Plan, with three approvals before implementation. **Lite** suits clearly scoped changes and uses a short Change Brief with one approval.

Say “Use Full for this operation” or “Use Lite for this operation.” This affects only the current operation.

Keep one declaration in `SKILL.md`, `Default workflow mode: full`, or change it to `Default workflow mode: lite`. For an installed Skill, repackage and re-upload the edited copy. This setting belongs to the workflow text; it does not read Codex or Claude Config. Missing or invalid declarations select Full.

For the full workflow, test choices, and saving progress, see the [beginner guide](getting-started-simple.en.md)。

## Available commands

Normally use the uploaded Skill or the complete `SKILL.md`. Advanced users can paste one module from `prompts/`; this does not bypass mode resolution or approvals.

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

Get the newer ZIP and upload it as a Skill, or paste its `SKILL.md` in a new text-only conversation. To stop using it, disable or remove the Skill, or stop pasting it; optionally delete the downloaded copy. Keep your project documents separately.

## Common questions

- Missing progress in a new conversation: use the enabled Skill, or paste the workflow again on a text-only host. To continue Full, provide saved requirements, specification, and Ticket Plan. Installing the Skill does not save project progress; Lite does not persist state across conversations.
- AI cannot edit files or run tests: available capabilities depend on the service and tools. With chat only, apply the output yourself and supply the results.

Report remaining issues through [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues). Include the project version, AI service/host, platform, and reproduction steps.

## License and attribution

This independent project is inspired by Matt Pocock’s skills repository and is not affiliated with or endorsed by him. See `LICENSE` and `THIRD_PARTY_NOTICES.md` for license and attribution.

[Back to README](../../README.md)
