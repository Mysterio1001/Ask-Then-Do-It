# Ask Then Do It Codex Plugin 1.3.0 Guide

This Plugin guides a project from requirements through implementation and review. For the ZIP fallback, download and extract the archive, then keep the complete `ask-then-do-it/` folder together.

This independent project was inspired by Matt Pocock's skills repository. It is not affiliated with or endorsed by Matt Pocock. See `LICENSE` and `THIRD_PARTY_NOTICES.md` in this package for license and attribution information.

## Install or update

Ask AI in a Codex task:

```text
Install or update Ask Then Do It from the official marketplace.
```

Inspect current state first:

```powershell
codex plugin marketplace list
codex plugin list
```

If the official marketplace is missing, add it:

```powershell
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
```

If it is already present and needs an update, upgrade it instead:

```powershell
codex plugin marketplace upgrade ask-then-do-it
```

Then install or refresh the Plugin:

```powershell
codex plugin add ask-then-do-it@ask-then-do-it
```

After a successful install or update, open a new Codex task. For the decision rules, manual fallback, updates, and removal, see the [detailed Codex Plugin guide](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides/codex.en.md).

## Start

Enter this in a new Codex task:

```text
Use $ask-then-do-it to help me build this feature: ...
```

Stage-specific entries are `$ask-requirements`, `$ask-with-docs`, `$write-spec`, `$plan-tickets`, `$implement-direct`, `$implement-tdd`, `$review-code`, and `$improve-architecture`.

## Choose Full or Lite

Use Full when the work needs the complete documented workflow and stronger assurance. Use Lite for a bounded change when a shorter workflow and proportionate validation are appropriate. See the [complete Full and Lite workflow guide](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides/getting-started-simple.en.md) before choosing.


[Back to README](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/README.md)
