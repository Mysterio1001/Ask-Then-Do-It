# Ask Then Do It Codex Plugin guide

Use the Codex Plugin to guide requirements, implementation, and Review. Start with `$ask-then-do-it`.

These are the 1.4.1 installation/download targets. If remote artifacts are unavailable, wait for publication.

## Installation and preparation

Run these first-install commands in a terminal, or ask your AI to run them:

```bash
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
```

<a id="zip"></a>
<details>
<summary>ZIP fallback</summary>

[Download ask-then-do-it-1.4.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.1/ask-then-do-it-1.4.1.zip)

Keep the complete `ask-then-do-it/` folder, not only `skills/`. Place it in `plugins/ask-then-do-it/` of an existing editable local Marketplace whose entry points there, then run:

```bash
codex plugin add ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

If you have no local Marketplace, create one using the [official guide](https://developers.openai.com/plugins/build/plugins).

</details>

## Getting started

After installation, open a new Codex task and enter:

```text
$ask-then-do-it Help me build a booking website. Please use English.
```

## Full / Lite modes

**Full** keeps requirements, specification, and a Ticket Plan, with three approvals before implementation. **Lite** suits clearly scoped changes and uses a short Change Brief with one approval.

Say “Use Full for this operation” or “Use Lite for this operation.” This affects only the current operation.

To set a default, put `mode = "full"` or `mode = "lite"` in either file:

- `<project>/.codex/ask-then-do-it.toml`
- `~/.codex/ask-then-do-it.toml`

Precedence: current explicit instruction, project Config, user Config, then Full. Invalid Config selects Full; invalid project Config does not fall through to user Config. Resolution does not edit either file.

For the full workflow, test choices, and saving progress, see the [beginner guide](getting-started-simple.en.md)。

## Available commands

Normally use `$ask-then-do-it`. Expand the table to select a particular stage. Direct entry still requires that stage’s prerequisites.

<details>
<summary>Show advanced entries</summary>

| Skill | Purpose |
| --- | --- |
| `$ask-then-do-it` | Identify the current stage and guide the whole workflow; start here in most cases |
| `$ask-requirements` | Clarify one high-impact requirement at a time |
| `$ask-with-docs` | Clarify requirements while maintaining a Project Knowledge Base |
| `$write-spec` | Turn approved requirements into a specification |
| `$plan-tickets` | Split a specification into vertical Tickets and collect all add-tests choices in one response |
| `$implement-direct` | Implement an approved `direct` Ticket without creating or running behavioral tests |
| `$implement-tdd` | Implement a Ticket through Red, Green, and Refactor |
| `$review-code` | Review requirements, changes, and available evidence, including skipped-test risk |
| `$improve-architecture` | Analyze architecture and module relationships, then propose improvements |

</details>

## Updating and removal

For an existing installation, run in a terminal:

```bash
codex plugin marketplace upgrade ask-then-do-it
codex plugin add ask-then-do-it@ask-then-do-it
```

For a manual update, back up the folder, replace it with the complete newer folder, and add the Plugin again. Restore the backup if loading fails.

Open a new Codex task after a successful update.

Remove the Plugin:

```text
codex plugin remove ask-then-do-it --marketplace ask-then-do-it
```

For a local Marketplace installation, replace the removal command’s marketplace name with your `<local-marketplace-name>`.

This removes the installation. Before deleting files from a local Marketplace, check that no other environment shares them.

Stop and inspect unknown versions or sources and update failures. Do not remove first, downgrade automatically, or switch sources. Current installations need no reinstall, and disabled state should be preserved.

## Common questions

- Skill missing: check `codex plugin list`, then open a new task.
- Installation source unclear: inspect `codex plugin marketplace list` first.

Report remaining issues through [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues). Include the project version, AI service/host, platform, and reproduction steps.

## License and attribution

This independent project is inspired by Matt Pocock’s skills repository and is not affiliated with or endorsed by him. See `LICENSE` and `THIRD_PARTY_NOTICES.md` for license and attribution.

[Back to README](../../README.md)
