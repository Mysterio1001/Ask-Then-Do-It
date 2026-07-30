# Ask Then Do It Codex Plugin Guide

This guide explains how to download, install, and use Ask Then Do It. The Plugin provides a set of Skills, with each Skill handling part of the development workflow.

## Download and extract

[Download ask-then-do-it-1.0.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-1.0.1.zip) and extract it.

The outermost extracted folder should be `ask-then-do-it/`, containing:

- `.codex-plugin/`
- `skills/`
- usage, license, and attribution documents

Install the complete folder. Do not copy only `skills/`, and do not add another version-named folder around it.

## Manual installation

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

## First use

Enter this in a new Codex task:

```text
Use $ask-then-do-it to help me build this feature: ...
```

The AI identifies the current stage, then asks the single most important question. Each question includes a recommended answer and the main tradeoff.

The workflow pauses for your explicit approval at three points:

1. Requirements consensus.
2. Specification.
3. Ticket plan.

Formal implementation begins only after the third approval.

## Eight Skill entry points

| Skill | Best used for |
| --- | --- |
| `$ask-then-do-it` | Identify the current stage and guide the whole workflow; start here in most cases |
| `$ask-requirements` | Clarify one high-impact requirement at a time |
| `$ask-with-docs` | Clarify requirements while maintaining a Project Knowledge Base |
| `$write-spec` | Turn approved requirements into a specification |
| `$plan-tickets` | Split a specification into vertical, testable Tickets |
| `$implement-tdd` | Implement a Ticket through Red, Green, and Refactor |
| `$review-code` | Review requirements, code changes, and test results |
| `$improve-architecture` | Analyze architecture and module relationships, then propose improvements |

You may invoke any Skill directly. If you use only `$ask-then-do-it`, the AI selects the next stage from your request and current progress.

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
