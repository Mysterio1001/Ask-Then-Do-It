# Ask Then Do It Codex Plugin Guide

This guide explains how to download, install, and use Ask Then Do It. The Plugin provides a set of Skills, with each Skill handling part of the development workflow.

## Download and extract

[Download ask-then-do-it-1.3.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-1.3.0.zip) and extract it.

The outermost extracted folder should be `ask-then-do-it/`, containing:

- `.codex-plugin/`
- `skills/`
- usage, license, and attribution documents

Install the complete folder. Do not copy only `skills/`, and do not add another version-named folder around it.

## Install or update with AI

Use natural language as the primary interface:

```text
Install or update Ask Then Do It from the official marketplace.
```

AI must inspect configured marketplaces and installed Plugins before writing:

```powershell
codex plugin marketplace list
codex plugin list
```

When the official marketplace is absent, add it and then add the Plugin:

```powershell
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
```

When it is present and a newer formal release is available, upgrade it first and then add the Plugin again:

```powershell
codex plugin marketplace upgrade ask-then-do-it
codex plugin add ask-then-do-it@ask-then-do-it
```

If the installed version is current, report it and do not write. If source, version, CLI support, or command results are uncertain, stop and report the uncertainty. A failed write stops subsequent writes. Never remove the current Plugin first, use an alternate source, or automatically downgrade. Use only the documented `add` installation subcommand; an install alias is unsupported.

After success, start a new Codex task. If the marketplace flow fails, use the matching `1.3.0` ZIP fallback. An older version is allowed only after the user explicitly chooses that version.

## Manual installation fallback

The current installation method requires an existing local marketplace that you can edit. The marketplace must have a name and an entry pointing to `<local-marketplace-root>/plugins/ask-then-do-it`.

1. Back up the existing `plugins/ask-then-do-it/` folder in the marketplace. Skip this step for a first installation.
2. Copy the complete extracted `ask-then-do-it/` folder to `<local-marketplace-root>/plugins/ask-then-do-it/`.
3. Confirm that Codex can see the marketplace:

```powershell
codex plugin marketplace list
```

4. Install the Plugin and check its status:

```powershell
codex plugin add ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

5. Open a new Codex task.

If you do not yet have a marketplace and entry, create them by following the [official Codex Plugin guide](https://developers.openai.com/plugins/build/plugins), then return to step 1.

## Workflow mode configuration

For each operation, Codex resolves the workflow mode in this order:

1. An explicit instruction for the current operation, such as "use Full this time" or "use Lite this time."
2. Project Config.
3. User Config.
4. Full fallback.

The Plugin-owned configuration files are:

- Project: `<project>/.codex/ask-then-do-it.toml`.
- User: `~/.codex/ask-then-do-it.toml`.

Each file accepts only a top-level `mode = "full"` or `mode = "lite"` value:

```toml
mode = "full"
```

```toml
mode = "lite"
```

For example, `mode = lite` is malformed and `mode = "fast"` is unsupported. An absent Project Config continues to User Config. A present invalid Project Config falls back to Full and does not continue to User Config. A file that exists but is unreadable, malformed, has no top-level `mode`, or uses an unsupported value is invalid. An explicit instruction wins without reading Config.

Mode resolution is read-only: it does not create, write, repair, or normalize either file. An explicit override affects only the current operation and never changes Config. Project Config affects only its project. A new session resolves the mode again from its own operation instruction and Config state.

High-risk work may prompt you to switch only the current operation to Full or explicitly accept the risk and continue Lite. This choice is not saved to Config. See the [Full and Lite workflow guide](getting-started-simple.en.md) for both lifecycles and the high-risk categories.

## First use

Enter this in a new Codex task:

```text
Use $ask-then-do-it to help me build this feature: ...
```

The resolved mode determines which lifecycle follows.

### Full mode

In Full mode, the AI asks exactly one requirement question at a time. Each question includes a recommended answer and the main tradeoff.

Full uses three approval gates:

1. Requirements consensus.
2. Specification.
3. Ticket plan.

Before the third approval, the AI first lists every Ticket and gives each one a test recommendation. For every Ticket, it warns that adding tests may increase work time while declining them lowers behavioral-verification confidence. In one response, you decide whether to add tests to every Ticket: add them to all, add them to none, or name only the Tickets that should have tests. There is no default. If a partial answer does not resolve the rest, the AI asks only about the unresolved Tickets.

After approval, a Ticket with tests is internally recorded as `tdd` and uses `$implement-tdd`. A Ticket without tests is recorded as `direct` and uses `$implement-direct`, which does not create or run behavioral tests but may run lint, type-check, or build checks. Its Review retains `tests: skipped-by-user` and states the untested risk. Formal implementation begins only after the third approval.

### Lite mode

Lite may ask no questions when repository evidence resolves every blocker. Otherwise, each round asks at most three blocking questions. It then presents one Change Brief and waits for one approval before implementation.

## Nine Skill entry points

| Skill | Best used for |
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

You may invoke any Skill directly. Direct Skill invocation selects a stage, not a workflow mode. `$ask-then-do-it` remains the canonical mode resolver and the usual starting point.

An unresolved mode delegates to `$ask-then-do-it` before stage work begins. Resolved Lite routes to the Lite lifecycle. Resolved Full may continue to the selected stage only after its normal prerequisites are satisfied. Conflicting mode signals pause for clarification. Invalid Config falls back to Full. Direct entry does not persist mode state.

## Manual update

1. Download and extract the new ZIP.
2. Back up the existing `plugins/ask-then-do-it/` folder in the marketplace.
3. Replace it with the complete new `ask-then-do-it/` folder.
4. Run the installation command again and check the version with `codex plugin list`.
5. Open a new Codex task and try `$ask-then-do-it`.

If the new version does not load, restore the backup and reinstall the earlier version.

## Manual removal

Run:

```powershell
codex plugin remove ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

These commands remove the installation from Codex. Before deleting `plugins/ask-then-do-it/` or its entry from the marketplace, make sure no other environment still uses it.

## License and attribution

Ask Then Do It is an independent project inspired by Matt Pocock's skills repository. It is not affiliated with or endorsed by Matt Pocock. See `LICENSE` and `THIRD_PARTY_NOTICES.md` in the repository or package for complete information.


[Back to README](../../README.md)
