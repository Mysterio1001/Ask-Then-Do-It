# Ask Then Do It Claude Code guide

One Claude Code Plugin provides both general Claude and Claude 5 workflow profiles.

These are the 1.4.0 installation/download targets. If remote artifacts are unavailable, wait for publication.

## Installation and preparation

Requires Claude model **4.6+** and Claude Code **2.1.251+**. Automatic model routing also needs Node.js **22+**. Enter these commands inside Claude Code:

This version supports user scope; the first-install commands below use the default user scope.

```text
/plugin marketplace add Mysterio1001/Ask-Then-Do-It
/plugin install ask-then-do-it@ask-then-do-it
```

<a id="zip"></a>
<details>
<summary>ZIP fallback</summary>

After downloading, compare SHA-256 with the Release checksums file.

[Download ask-then-do-it-claude-1.4.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0/ask-then-do-it-claude-1.4.0.zip)

Download and extract the complete Plugin. Add this flag each time you launch from a terminal:

```bash
claude --plugin-dir "/path with spaces/ask-then-do-it"
```

This is session-only. Every later session also needs `--plugin-dir`; it does not create a persistent Marketplace installation.

</details>

## Getting started

After installation, run `/reload-plugins` or open a new session, then enter:

```text
/ask-then-do-it:ask-then-do-it Help me build a booking website. Please use English.
```

## Full / Lite modes

**Full** keeps requirements, specification, and a Ticket Plan, with three approvals before implementation. **Lite** suits clearly scoped changes and uses a short Change Brief with one approval.

Say “Use Full for this operation” or “Use Lite for this operation.” This affects only the current operation.

To set a default, put `mode = "full"` or `mode = "lite"` in either file:

- `<project>/.claude/ask-then-do-it.toml`
- `~/.claude/ask-then-do-it.toml`

Precedence: current explicit instruction, project Config, user Config, then Full. Invalid Config selects Full; invalid project Config does not fall through to user Config. Resolution does not edit either file.

For the full workflow, test choices, and saving progress, see the [beginner guide](getting-started-simple.en.md)。

## Available commands

Use the first entry in most cases. Both preserve your current model; neither switches models.

| Entry | Purpose |
| --- | --- |
| `/ask-then-do-it:ask-then-do-it` | Select general Claude or Claude 5 automatically; disclose an unknown model and use general compatibility mode. |
| `/ask-then-do-it:ask-then-do-it-5` | Request the Claude 5 profile. A known supported non-5 model still uses general; an unknown model uses the requested profile with an unverified-path disclosure. |

## Updating and removal

For an existing installation, enter inside Claude Code:

```text
/plugin marketplace update ask-then-do-it
/plugin update ask-then-do-it@ask-then-do-it
/reload-plugins
```

Remove the Plugin:

```text
/plugin uninstall ask-then-do-it@ask-then-do-it --scope user
```

Removal keeps the Marketplace and workflow Config. Removing the last scope deletes disposable routing data by default; use `--keep-data` only when you explicitly want to retain it.

Stop and inspect unknown versions or sources and update failures. Do not remove first, downgrade automatically, or switch sources. Current installations need no reinstall, and disabled state should be preserved.

## Common questions

- Entry missing: check that the Plugin is enabled, run `/reload-plugins`, or start a new session. In VS Code, use `/` to inspect available commands.
- Automatic routing stopped: check `claude --version` and `node --version`. The `-5` entry is not a general repair command.
- `/doctor` checks Claude Code installation/configuration health; it does not convert or optimize these Skills.

Local CLI, VS Code, and JetBrains on Windows, macOS, and Linux are compatibility targets. Real-model, command/hook, independent-review, and full installation/update scenarios still have unverified items. Offline tests do not establish full live verification. [Advanced reference](#advanced-reference)。

Report remaining issues through [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues), including project and host/Node versions, platform, entry, and reproduction steps.

<a id="advanced-reference"></a>
<details>
<summary>Advanced reference</summary>

Detailed routing, Config resolution, review, and platform evidence live here. Use the main guide for installation and everyday operation.

[guide](claude-code.en.md)

<a id="routing"></a>
### Routing and session continuity

| Trusted route result | Automatic entry | Explicit `-5` entry |
| --- | --- | --- |
| Known Claude 5 | Claude 5 profile | Claude 5 profile |
| Known supported non-Claude-5 | General profile | Disclose the mismatch, then General |
| `known unsupported`: known model below 4.6 | Stop | Stop |
| `valid unknown`: valid but unlisted or omitted model | Disclose unverified compatibility, then General | Disclose that your explicit choice is unverified, then Claude 5 |
| `router failure`: invalid state, ownership, transition, or handler failure | Stop | Stop, except the two bounded Node fallbacks below |

Missing or old Node does not mean the model is unknown. The explicit entry alone may use a disclosed manual Claude 5 path after a valid `node-too-old` envelope, or when Node is proven missing and the envelope is unavailable. Both require separately proven Claude Code 2.1.251+; they do not verify the model or provide automatic routing, persisted binding, resume, or switch tracking. Missing/malformed/duplicate envelopes with Node present, unproven versions, and other router failures stop. Never infer model identity from user text or self-report.

One `operation` keeps its selected profile. A model change does not load or obey the other profile mid-operation. After a committed `PostModelSwitch`, the next permitted public entry may select again and supersedes historical profile instructions. Hook timing has a `best-effort` window, so the first invocation after a switch is not guaranteed to reroute. Switching to an unsupported model also discloses that the operation has left formal support.

Startup, fork, and clear do not automatically resume the last operation. Resume/compact need trusted same-session context and current workflow evidence; a stale binding never transfers authority to another session. Full may use saved approved artifacts; Lite conversation state is not durable across sessions.

<a id="config"></a>
### Full/Lite Config

Profile selection and workflow mode are separate. Each operation resolves: explicit `full`/`lite` instruction → project Config inside the active project root → user Config → Full fallback. Conflicting explicit modes pause for one clarification. The trusted active project root determines the project boundary, not a guessed working-directory path.

- Project: `<project>/.claude/ask-then-do-it.toml`
- User: `~/.claude/ask-then-do-it.toml`

The file contains one top-level quoted assignment, either:

```toml
mode = "full"
```

or `mode = "lite"`. Missing project Config continues to user Config. Present but unreadable, malformed, duplicate, missing-mode, or unsupported Config fails closed to Full; an invalid project file does not fall through to the user file. Capitalization, aliases, nested keys, and unquoted values are not accepted. With conversation-only capability, a host-unavailable source counts as absent without pretending it was read or asking you to supply it.

Resolution is read-only: it never creates, repairs, or rewrites either file, persists an operation override, or reads/writes Codex Config. It does not write `settings.json`. This Plugin Config is separate from Claude Code's own host settings and rebuildable routing data. See the [shared workflow guide](getting-started-simple.en.md) for Full approval gates, Ticket test choices, and Lite's one Change Brief.

<a id="review"></a>
### Review capability

Full Review uses an isolated Plugin reviewer when it is actually available. Its allowed tools are exactly `Read`, `Grep`, and `Glob`; it has no write, shell, or network tools. The workflow waits for its report and checks its findings. A file declaring a reviewer does not prove that the host executed it independently.

With proven repository tools but no usable independent reviewer, the same context reviews and reports `non-independent`. Conversation-only or excerpt-only evidence is `limited-evidence`, with unavailable checks and a handoff; it cannot claim a completed repository Review. Use `independent` only with demonstrated isolation and raw evidence. Lite always keeps its compact same-context Review. Review findings do not themselves authorize fixes.

<a id="status"></a>
### Read-only status

These `read-only` checks do not install, refresh, update, enable, disable, remove, or change Config:

```sh
claude --version
node --version
claude plugin marketplace list --json
claude plugin list --json
claude plugin details ask-then-do-it@ask-then-do-it
```

Report Claude Code and Node separately, Marketplace name/source/scope, qualified Plugin identity, installation scope, version, enabled state, and availability of both entries. If listing output omits a required fact, report it as unknown and inspect the appropriate read-only host state; do not invent ownership or assume a safe write. Component discovery and projected token cost are not model behavior or billing evidence.

<a id="platforms"></a>
### Platforms and observed limits

Windows, macOS, and Linux across local `terminal CLI`, `VS Code`, and `JetBrains` are a **compatibility target**, not nine `live-verified` combinations. No complete live environment is claimed for this Adapter yet. Record the exact OS, surface, Claude Code, Node, active model, and date before making a live claim.

Official documentation was read on **2026-09-09**:

| Surface | Officially documented support and difference |
| --- | --- |
| terminal CLI | Local Plugins can contain Skills, Agents, and hooks. The CLI exposes the complete commands/skills interface. This is documentation support, not proof of this Adapter's exact host hooks. |
| VS Code | Graphical Plugin management is documented, and host settings/hooks are shared with the CLI. The chat panel bundles its own CLI, but its commands/skills are a subset; use `/` to inspect availability. Running `claude` in the integrated terminal requires a separate standalone CLI installation. Plugin reviewer invocation/isolation and both exact namespaced entries still need surface-specific verification. |
| JetBrains | Official usage runs `claude` in the IDE's integrated terminal; external terminals can connect through `/ide`. Plugin features are those of that CLI runtime, with the JetBrains integration adding IDE features. This does not establish a separate graphical command interface or this Adapter's exact runtime behavior. |

Sources: [Plugin components](https://code.claude.com/docs/en/plugins-reference), [VS Code](https://code.claude.com/docs/en/vs-code), [JetBrains](https://code.claude.com/docs/en/jetbrains), [Skills](https://code.claude.com/docs/en/skills), [Subagents](https://code.claude.com/docs/en/sub-agents), and [hooks](https://code.claude.com/docs/en/hooks). Current official documentation does not replace exact 2.1.251 behavior testing. Claude Desktop and web/cloud are outside this compatibility target.

<a id="lifecycle"></a>
### Detailed installation, update, and removal rules

The persistent source is `Mysterio1001/Ask-Then-Do-It`, the Plugin is `ask-then-do-it@ask-then-do-it`, and only `user` scope is supported. Recheck source, scope, version, and enabled state immediately before every write. Install only when absent; a current enabled or disabled installation is a no-op. Do not downgrade a newer version. Stop on wrong sources, ambiguous ownership, or unsupported scopes.

An explicit user request authorizes installation, update, or removal. Recheck between writes; after a partial failure, stop, inspect state read-only, and report without destructive rollback. Marketplace refresh has no scope option. Missing Node can still allow safe authorized lifecycle actions, with automatic routing disclosed as unavailable. Reload or start a new session before claiming the new bytes are active. Do not enable background updates implicitly.

Run these in a terminal; installation, update, and removal are separate operations:

```sh
# Install
claude plugin marketplace add Mysterio1001/Ask-Then-Do-It --scope user
claude plugin install ask-then-do-it@ask-then-do-it --scope user

# Update
claude plugin marketplace update ask-then-do-it
claude plugin update ask-then-do-it@ask-then-do-it --scope user

# Remove
claude plugin uninstall ask-then-do-it@ask-then-do-it --scope user
```


</details>

## License and attribution

This independent project is inspired by Matt Pocock’s skills repository and is not affiliated with or endorsed by him. See `LICENSE` and `THIRD_PARTY_NOTICES.md` for license and attribution.

[Back to README](../../README.md)
