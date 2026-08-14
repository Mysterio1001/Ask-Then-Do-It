# Ask Then Do It: Ask First, Then Build

Ask Then Do It guides an AI to clarify your needs first, then move through specification, work planning, implementation, and review in order.

This independent project was inspired by the [Matt Pocock skills repository](https://github.com/mattpocock/skills). It is not affiliated with or endorsed by Matt Pocock. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for license and attribution information.

## 1. Use with Codex

[Download ask-then-do-it-1.2.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.2.0/ask-then-do-it-1.2.0.zip) and extract it. After installing the complete `ask-then-do-it/` Plugin folder, open a new Codex task and enter:

```text
$ask-then-do-it I want to build...
```

The AI will ask one important question first. It will not move to the next stage until you confirm the requirements. After the Tickets are drafted, it gives a test recommendation for each Ticket, then asks you in one response whether to add tests to each Ticket before you approve the complete plan. For installation, updates, and all nine Skill entry points, see the [Codex Plugin Guide](docs/guides/codex.en.md).

## 2. Use with Gemini or another AI

[Download ask-then-do-it-generic-1.2.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.2.0/ask-then-do-it-generic-1.2.0.zip) and extract it. Open `generic-workflow.md`, paste the entire file into a new AI conversation, and then describe what you want to do.

The AI will begin with one requirements question. Save the important documents created during the workflow. When you start another conversation, paste the workflow and your saved documents again. See the [Generic Guide](docs/guides/generic.en.md) for complete instructions.

## Learn about the workflow

- [Beginner's Workflow Guide](docs/guides/getting-started-simple.en.md)
- [Design Guide](docs/design/ai-development-skills.en.md)
