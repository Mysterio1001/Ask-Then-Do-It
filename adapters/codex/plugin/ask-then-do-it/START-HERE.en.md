# Ask Then Do It Codex Plugin 1.2.0 Guide

This Plugin includes nine Skills that guide a project from requirements discovery through implementation, review, and architecture improvement.

This independent project was inspired by Matt Pocock's skills repository. It is not affiliated with or endorsed by Matt Pocock. See `LICENSE` and `THIRD_PARTY_NOTICES.md` in this package for license and attribution information.

## Download and extract

After extracting `ask-then-do-it-1.2.0.zip`, the outermost folder should be `ask-then-do-it/`. Keep the complete folder together; do not copy only `skills/`.

## Install or update with AI

The primary interface is a natural-language request to AI in a Codex task:

```text
Install or update Ask Then Do It from the official marketplace.
```

AI must inspect state before any write:

```powershell
codex plugin marketplace list
codex plugin list
```

For a missing official marketplace, AI may add it and then add the Plugin:

```powershell
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
```

If the official marketplace is present and a newer formal release exists, AI must upgrade the marketplace before running the same Plugin command:

```powershell
codex plugin marketplace upgrade ask-then-do-it
codex plugin add ask-then-do-it@ask-then-do-it
```

If the installed Plugin is already current, AI reports that state and performs no write. If the source, version, CLI support, or result cannot be determined, AI stops and reports the uncertainty. A failed write stops all later writes; AI must not remove the current Plugin first, choose an alternate source, or automatically downgrade. Use only the documented `add` installation subcommand; an install alias is not supported here.

After a successful install or update, start a new Codex task so the new Plugin contents load. If marketplace installation cannot proceed, use the matching `1.2.0` ZIP as the manual fallback.

## Manual installation

This installation method requires an existing local marketplace that you can edit, with an entry pointing to `plugins/ask-then-do-it/`.

1. Place the complete `ask-then-do-it/` folder inside the marketplace's `plugins/` folder.
2. Install or enable `ask-then-do-it` from that marketplace.
3. Open a new Codex task so Codex can load the installed content.

If you have not created a marketplace yet, follow the Codex Plugin documentation to set one up, then return here.

## First use

Enter this in a new Codex task:

```text
Use $ask-then-do-it to help me build this feature: ...
```

The AI will identify the current stage and ask one important question first. You must explicitly approve the requirements, specification, and Ticket plan. After all Tickets are listed, the AI gives each Ticket a test recommendation and warns that adding tests may increase work time while declining them lowers verification confidence. In one response, you decide whether to add tests to every Ticket: add them to all, add them to none, or name only the Tickets that should have tests. You then approve the complete plan. Formal implementation must not begin before those approvals.

Internally, "Add tests" is recorded as `tdd` and "Do not add tests" as `direct`; you do not need to answer with those names.

## Nine Skill entry points

Start with `$ask-then-do-it` in most cases. To select a specific stage, use one of these Skills directly:

| Skill | Purpose |
| --- | --- |
| `$ask-then-do-it` | Identify the current stage and guide the complete workflow |
| `$ask-requirements` | Ask one question at a time to clarify requirements |
| `$ask-with-docs` | Clarify requirements while maintaining long-term project knowledge |
| `$write-spec` | Turn approved requirements into a specification |
| `$plan-tickets` | Split the specification into vertical Tickets and collect every add-tests choice in one response |
| `$implement-direct` | Implement an approved `direct` Ticket without creating or running behavioral tests |
| `$implement-tdd` | Implement a Ticket through Red, Green, and Refactor |
| `$review-code` | Review the code and preserve `tests: skipped-by-user` when a `direct` Ticket has no behavioral-test evidence |
| `$improve-architecture` | Analyze architecture problems and propose improvements |

## Manual update

1. Download and extract the matching ZIP.
2. Back up the existing `ask-then-do-it/` folder in the marketplace.
3. Replace it with the complete new folder.
4. Reinstall or enable the Plugin, then open a new Codex task and confirm that `$ask-then-do-it` is available.

Do not downgrade automatically; use an older version only after explicitly choosing that version.

## Manual removal

Remove or disable `ask-then-do-it` in Codex first. Before deleting its Plugin folder or marketplace entry, make sure no other environment still uses that marketplace.
