# Ask Then Do It — Claude Code guide

This guide describes the Claude Adapter public preview `1.4.0-preview.1`. Codex and Generic retain stable `1.3.1`. For the shared Full/Lite workflow, read the [beginner guide](getting-started-simple.en.md).

<a id="versions"></a>
## Preview status and three versions

**Release instructions for the opt-in public preview 1.4.0-preview.1.** The stable release remains **1.3.1** and its Codex/Generic packages do not contain this Claude Adapter. The installation commands and [versioned preview ZIP](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0-preview.1/ask-then-do-it-claude-1.4.0-preview.1.zip) apply once the preview tag, ZIP, and `claude-preview` Marketplace branch have been published. If an artifact is unavailable, wait for publication; do not substitute a different source.

| Requirement | Meaning |
| --- | --- |
| Claude model `4.6+` | The model support baseline; a valid but unlisted model remains unverified. |
| Claude Code `2.1.251+` | The host minimum, checked separately from the model. |
| Node.js `22+` | Required for automatic profile routing, independently of the native Claude Code installation. |

Preview verification covers native `strict` validation and `local automated tests`. Real official Claude Code session verification is **deferred**, including command/hook behavior, model scenario compliance, paired equivalence, context reduction, and clean live smoke. Those checks are not a preview publication gate, and no passing result is claimed. Exact Claude Code 2.1.251 schema validation does not establish live behavior or guarantee later host versions.

<a id="entries"></a>
## Two public entries

After a verified installation and reload, invoke one of these yourself:

```text
/ask-then-do-it:ask-then-do-it Help me build...
/ask-then-do-it:ask-then-do-it-5 Help me build...
```

The first selects the profile automatically; the second explicitly requests the Claude 5 path subject to the routing rules below. Both use `model: inherit`: they preserve your active model, and do not switch or pin it. The Plugin exposes exactly these two supported namespaced entries. Internal stages are not extra commands. Host-provided bare aliases may vary; their presence or absence is not promised.

<a id="routing"></a>
## Routing and session continuity

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
## Full/Lite Config

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
## Review capability

Full Review uses an isolated Plugin reviewer when it is actually available. Its allowed tools are exactly `Read`, `Grep`, and `Glob`; it has no write, shell, or network tools. The workflow waits for its report and checks its findings. A file declaring a reviewer does not prove that the host executed it independently.

With proven repository tools but no usable independent reviewer, the same context reviews and reports `non-independent`. Conversation-only or excerpt-only evidence is `limited-evidence`, with unavailable checks and a handoff; it cannot claim a completed repository Review. Use `independent` only with demonstrated isolation and raw evidence. Lite always keeps its compact same-context Review. Review findings do not themselves authorize fixes.

<a id="status"></a>
## Read-only status

These `read-only` checks do not install, refresh, update, enable, disable, remove, or change Config:

```sh
claude --version
node --version
claude plugin marketplace list --json
claude plugin list --json
claude plugin details ask-then-do-it@ask-then-do-it
```

Report Claude Code and Node separately, Marketplace name/source/scope, qualified Plugin identity, installation scope, version, enabled state, and availability of both entries. If listing output omits a required fact, report it as unknown and inspect the appropriate read-only host state; do not invent ownership or assume a safe write. Component discovery and projected token cost are not model behavior or billing evidence.

<a id="install-update"></a>
## User-scope installation and updates

Opt in to the preview with the exact Marketplace source `https://github.com/Mysterio1001/Ask-Then-Do-It.git#claude-preview` and qualified Plugin `ask-then-do-it@ask-then-do-it`, at `--scope user`. The fragment selects the moving `claude-preview` branch; refreshing it follows that branch, so later previews can be installed without changing the URL. It does not promote the stable 1.3.1 release. The [official Marketplace reference](https://code.claude.com/docs/en/plugin-marketplaces) documents this `#ref` syntax.

Immediately before every write, recheck complete ownership, source, scope, and current state. Earlier status is insufficient. If both expected Marketplace and Plugin are absent and unambiguous:

```sh
claude plugin marketplace add "https://github.com/Mysterio1001/Ask-Then-Do-It.git#claude-preview" --scope user
claude plugin install ask-then-do-it@ask-then-do-it --scope user
```

Inside Claude Code, the equivalent Marketplace command is `/plugin marketplace add https://github.com/Mysterio1001/Ask-Then-Do-It.git#claude-preview`. If only the Plugin is absent and the Marketplace source/ref is correct, run only the install command. For an older expected preview installation, an explicit update may refresh that Marketplace and update that qualified Plugin:

```sh
claude plugin marketplace update ask-then-do-it
claude plugin update ask-then-do-it@ask-then-do-it --scope user
```

The Marketplace refresh command has no scope option; verify its source and scope before and after. Recheck state again before the next write. A current version is a no-op, whether enabled or `disabled`; preserve the disabled choice. Enabling needs a separate user action. A `newer` installed version stops rather than downgrades. Never update by removing first.

Source mismatch, same-name other sources, project/local/managed or multiple scopes, changed or unreadable state, and unsupported Claude Code stop without writes. Missing Node does not prevent an otherwise authorized lifecycle action, but automatic routing remains unavailable. On partial failure stop subsequent writes, reread state, and report actual successes/failures without destructive rollback. After success use `/reload-plugins` or start a new session before claiming new bytes are active. Do not enable background auto-update as part of this workflow.

<a id="remove"></a>
## Remove and preserve data

On an explicit removal request, perform a fresh ownership/source/user-scope/state check immediately before:

```sh
claude plugin uninstall ask-then-do-it@ask-then-do-it --scope user
```

Before removing the last scope, disclose that the Plugin's data directory contains only rebuildable routing state and is deleted by default. Add `--keep-data` only if you explicitly request preservation. Normal removal leaves the Marketplace, both workflow Config files, and other scopes intact. Removing those is a separate purge request. Verify the actual result; failure is not proof of removal.

<a id="zip"></a>
## Session-only ZIP recovery

Download [ask-then-do-it-claude-1.4.0-preview.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0-preview.1/ask-then-do-it-claude-1.4.0-preview.1.zip) from the [versioned preview release](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/tag/v1.4.0-preview.1), verify its SHA-256 against that release's checksums, and extract it while keeping the complete Plugin folder. This immutable tag stays on this preview even when the Marketplace branch advances. Start each test/recovery session with the extracted path as one quoted argument:

```sh
claude --plugin-dir "/path with spaces/ask-then-do-it"
```

This is `session-only`, not a `persistent` Marketplace install or update. Repeat `--plugin-dir` for each session. A bare `claude plugin list` cannot establish this session's ZIP load; check with the same flag or inside that session. Do not create a local Marketplace, copy files into `~/.claude/skills`, or treat ZIP recovery as a personal-Skill installation. The short Plugin START-HERE points to the immutable same-version guide.

<a id="platforms"></a>
## Platforms and observed limits

Windows, macOS, and Linux across local `terminal CLI`, `VS Code`, and `JetBrains` are a **compatibility target**, not nine `live-verified` combinations. No complete live environment is claimed for this Adapter yet. Record the exact OS, surface, Claude Code, Node, active model, and date before making a live claim.

Official documentation was read on **2026-09-09**:

| Surface | Officially documented support and difference |
| --- | --- |
| terminal CLI | Local Plugins can contain Skills, Agents, and hooks. The CLI exposes the complete commands/skills interface. This is documentation support, not proof of this Adapter's exact host hooks. |
| VS Code | Graphical Plugin management is documented, and host settings/hooks are shared with the CLI. The chat panel bundles its own CLI, but its commands/skills are a subset; use `/` to inspect availability. Running `claude` in the integrated terminal requires a separate standalone CLI installation. Plugin reviewer invocation/isolation and both exact namespaced entries still need surface-specific verification. |
| JetBrains | Official usage runs `claude` in the IDE's integrated terminal; external terminals can connect through `/ide`. Plugin features are those of that CLI runtime, with the JetBrains integration adding IDE features. This does not establish a separate graphical command interface or this Adapter's exact runtime behavior. |

Sources: [Plugin components](https://code.claude.com/docs/en/plugins-reference), [VS Code](https://code.claude.com/docs/en/vs-code), [JetBrains](https://code.claude.com/docs/en/jetbrains), [Skills](https://code.claude.com/docs/en/skills), [Subagents](https://code.claude.com/docs/en/sub-agents), and [hooks](https://code.claude.com/docs/en/hooks). Current official documentation does not replace exact 2.1.251 behavior testing. Claude Desktop and web/cloud are outside this compatibility target.

<a id="troubleshooting"></a>
## Troubleshooting

- Missing entries: check actual installation, source, scope, enabled state, and reload/new-session status. A host bare alias is not the supported entry contract; VS Code may expose a subset.
- Route stopped: distinguish unsupported Claude Code/model, missing or old Node, `UserPromptExpansion` envelope failure, and invalid or pending routing state. Do not guess another model/profile or reuse another session. Use only the bounded explicit fallback described above.
- Update failed: report the partial state and stop; do not remove first, choose another source, or silently enable a disabled Plugin.
- Built-in `/doctor` is optional **installation/configuration health** checking for Claude Code. It does not convert, optimize, or validate Ask Then Do It Skills; there is no custom Plugin doctor command.
- A native `strict` validation pass on Claude Code `2.1.251` is schema evidence only. Official-session entry behavior, actual model outcomes, and live lifecycle smoke are deferred beyond this preview. No context-reduction or billing savings result is claimed.

<a id="feedback"></a>
## Preview feedback

Report reproducible issues through [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues). Include preview `1.4.0-preview.1`, OS and surface, Claude Code and Node versions, active model, entry used, and the expected/observed result. Remove credentials and private conversation content before sharing logs.

[Back to README](../../README.md)
