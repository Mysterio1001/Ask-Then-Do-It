# Claude Code General profile orchestration

This is the General profile's internal orchestration module. It is not a public command.

Core rules: CAP-DECLARE-001, CAP-CLAIM-001, MODE-RESOLVE-001, FULL-PRESERVE-001, ADAPTER-COVERAGE-001, ROUTE-USER-001, ROUTE-DOCS-001

## Profile and routing boundary

Enter this module only after the public bootstrap has validated one same-invocation ready route envelope whose `selected_profile` is `general`. A missing or failure envelope must stop before profile loading; never recover inside this module. Treat the ready route envelope and its operation ID as already established authority, but do not request, reconstruct, retain, or expose a raw session ID or hook input.

The router may select this General profile for an automatic entry on a supported non-Claude-5 model, for automatic unknown-model compatibility, or as the General binding produced for an explicit Claude 5 entry on a supported non-Claude-5 model. Honor the bootstrap's disclosure. This profile must not classify a model, must not reroute, and must not infer model identity from text, self-report, environment, or substring matching.

Load only General profile modules required by the current stage. Never load or follow the other profile's modules during this operation. The latest public entry and its operation-bound profile supersede profile instructions retained as historical conversation context. This profile must not pin, switch, or override the active model.

If a model-switch notice arrives, say that the current operation profile remains unchanged. Continue under the operation-bound profile without injecting other instructions; the next permitted public entry may reroute from committed state. If the notice says the new model is unsupported, also disclose that the current operation has left formal model support. Treat a commit-before-notice race as best-effort and never promise that the first invocation after a switch will reroute.

[SCENARIO: ROUTE-AUTO]
[SCENARIO: ROUTE-EXPLICIT-5]
[SCENARIO: ROUTE-FAILURE]
[SCENARIO: ROUTE-SWITCH]

## Declare capability

At the beginning of every operation, declare the strongest capability actually proven now:

- `conversation`: exchange text and produce user-managed artifacts only. Do not claim repository access, persistence, commands, tests, or isolation; give a safe handoff when the requested stage requires them.
- `tools`: includes conversation plus proven repository read/write access and the ability to execute commands. Claim only actions and raw evidence actually observed.
- `multi_agent`: includes tools plus a genuinely isolated worker or reviewer context. Availability of a reviewer file alone does not prove this capability.

Downgrade whenever a required ability is unavailable. Never claim completed implementation or Review from unobserved evidence.

[CORE: CAP-DECLARE-001]
[CORE: CAP-CLAIM-001]
[SCENARIO: CAP-CONVERSATION]
[SCENARIO: CAP-TOOLS]

## Portable artifact envelope

Every General profile stage that produces a Full workflow artifact must use the `portable artifact envelope` defined in `orchestration.md`. The fixed fields are:

1. `artifact_type`: the artifact kind.
2. `artifact_id`: a stable artifact identifier; `artifact_id` must be stable across revisions of the same logical artifact.
3. `workflow_id`: the shared workflow identifier.
4. `core_version`: the Core contract version used by the artifact.
5. `status`: an allowed explicit lifecycle state for that artifact.
6. `inputs`: the upstream evidence and artifacts actually used.
7. `assumptions`: assumptions distinguished from observed evidence.
8. `deferred`: intentionally incomplete work and its owner or later gate.
9. `handoff`: the bounded next workflow stage or safe action.

Also include `approval` when the artifact has an approval or acceptance gate. Approval evidence must identify the explicit human decision; silence, an unrelated reply, or approval of a different artifact does not count. A stage may add artifact-specific fields, but it must not omit, rename, contradict, or invent values for these common fields.

## Resolve exactly one top-level mode

Resolve `full` or `lite` once for every operation. This is separate from the Full Ticket modes `tdd` and `direct`. A stage selection does not imply Full, and the current result applies only to this operation.

Use this precedence, stopping as soon as a source controls the result:

1. A valid explicit current-operation instruction selecting exactly `full` or `lite`.
2. `<project>/.claude/ask-then-do-it.toml`, only when it is inside the active project root.
3. `~/.claude/ask-then-do-it.toml`.
4. `full` fallback.

Conflicting explicit `full` and `lite` instructions remain unresolved: ask one clarification and stop. A valid explicit instruction wins without reading lower sources. A stage module must reuse the mode proven for this operation and must not resolve it again.

For either Config, accept only one top-level quoted assignment exactly equivalent to `mode = "full"` or `mode = "lite"`. Aliases, other capitalization, unquoted or nested values, duplicate or missing `mode`, unsupported values, and malformed TOML are invalid. An absent project Config continues to the user Config. A present but unreadable, malformed, missing-mode, duplicate-mode, or unsupported project Config must fail closed to `full` and must not read the user Config. An absent user Config uses the Full fallback; a present invalid user Config must fail closed to `full`. Disclose a fail-closed outcome when it changes the route the user expected.

Config resolution is read-only. It must not create, repair, normalize, or rewrite either file; must not persist an operation override; must not write `settings.json`; and must not read or write Codex Config. A source unavailable to the proven capability is not evidence that it was read.

[CORE: MODE-RESOLVE-001]
[SCENARIO: MODE-EXPLICIT]
[SCENARIO: MODE-CONFIG]
[SCENARIO: MODE-INVALID]

## Conversation-only unavailable-source transitions

For `conversation` capability with no explicit mode, host-unavailable is absence, not invalid content. Follow these transitions without asking the user to supply a host Config:

| Capability | Explicit mode | Project Config | User Config | Outcome |
| --- | --- | --- | --- | --- |
| conversation | none | host-unavailable | valid Full or Lite | Treat project as absent; select the valid user mode |
| conversation | none | host-unavailable | host-unavailable | Treat both as absent; select Full fallback |
| conversation | none | absent | host-unavailable | Treat user as absent; select Full fallback |

The workflow must not claim that an unavailable Config was read, parsed, absent on disk, valid, or invalid. If a source becomes available through proven tools, use its actual absent/valid/invalid result instead of this host-unavailable branch.

## Route the selected workflow

For `lite`, load `lite-workflow.md` and do not load a Full stage. Lite must not fabricate Full artifacts or modes.

For `full`, preserve every gate, artifact, Ticket test choice, implementation route, Review requirement, and architecture contract. Inspect available repository instructions, relevant sources and tests, current changes, and existing approved artifacts. Apply the Full route precedence below.

Otherwise, select the first unmet delivery condition in this order: requirement consensus, Approved Specification, Approved Ticket Plan with all test choices, eligible implementation, Review, an applicable automatic architecture transition, then completion. Reuse relevant internally consistent approved evidence; return to the earliest affected gate when evidence is missing, disputed, contradictory, or no longer feasible.

Honor an explicit user-selected module, requirement mode, or Approved Ticket implementation mode unless it violates a safety or approval gate. Use normal requirements for a fresh self-contained request. Automatically select documented requirements when a Project Knowledge Base exists, the request changes an existing system, or durable knowledge is likely; announce that evidence-based reason first. An accepted Architecture Improvement Report returns to Specification, never directly to planning or implementation.

Implementation requires proven `tools`. Independent Review and parallel work require proven `multi_agent`. Unsupported stages end with the limitation, unavailable evidence, required handoff, and safe next action.

[CORE: FULL-PRESERVE-001]
[CORE: ROUTE-USER-001]
[CORE: ROUTE-DOCS-001]
[CORE: ADAPTER-COVERAGE-001]

## Full route precedence

Before the delivery first-unmet order, handle an explicit direct architecture-diagnosis request after mode, capability, safety, and the architecture stage's own authorization prerequisites are resolved. It does not require existing Requirements, Specification, Ticket Plan, implementation, or Review. It authorizes diagnosis only and must not bypass the architecture stage's own safety or approval gates.

| Request/trigger | Upstream delivery state | Preconditions | Next stage | Authority |
| --- | --- | --- | --- | --- |
| Direct architecture diagnosis | Any | Mode, capability, safety, and the architecture stage's own authorization prerequisites | `architecture-improvement.md` | Diagnosis only; no implementation |
| Automatic architecture trigger | Relevant Full delivery gates complete and trigger proven | Announce the evidence and reason | `architecture-improvement.md` | Diagnosis only; no implementation |
| Accepted Architecture Improvement Report | Any | Acceptance evidence | `specification.md` | No direct planning or implementation |

## Full architecture transitions

Apply the direct-request row according to the Full route precedence above. Apply automatic routes only after checking the relevant delivery gates. Automatic architecture routing must be evidence-based and announced before loading the architecture stage.

| Trigger | Next stage | Required behavior |
| --- | --- | --- |
| Direct architecture request | `architecture-improvement.md` | Explicit user route; no automatic-route announcement required |
| Systemic Review evidence | `architecture-improvement.md` | Announce the evidence and reason before automatic routing |
| Related Ticket group completes | `architecture-improvement.md` | Announce the evidence and reason before automatic routing |
| Release milestone approaches | `architecture-improvement.md` | Announce the evidence and reason before automatic routing |
| Focused local Review finding | `review.md` | Stay in Review; do not route to architecture improvement |
| Accepted Architecture Improvement Report | `specification.md` | Return to Specification; never route directly to planning or implementation |

Do not run architecture diagnosis after every Ticket. Only cross-module or systemic Review evidence triggers the automatic route; keep a local finding in Review.

## Durable-knowledge synchronization transitions

Check durable knowledge whenever any workflow artifact becomes Approved or accepted, not only after documented requirement interrogation.

| Evidence transition | Required behavior |
| --- | --- |
| Each Approved or accepted artifact changes durable facts | Propose a complete Knowledge Base Change Summary tied to that artifact; display additions, modifications, and removals including none; request joint approval for the exact displayed artifact and knowledge changes before applying them |
| Artifact adds no durable fact | Continue the unrelated gate without a knowledge update or delay |

Derive formal Knowledge Base content only from Approved or accepted evidence. Apply only the exact jointly approved changes and preserve unrelated knowledge.

## Session and operation continuity

On `startup`, `fork`, or `clear`, do not claim an operation resumed without current workflow evidence. On `resume` or `compact`, accept only same-session operation context supplied by the trusted bootstrap/hook path. A conditional continuation describing a last binding is historical evidence, not proof that work remains active; verify workflow artifacts or conversation evidence before continuing. Never copy authority across sessions. A new public entry replaces the prior operation binding.

For `resume` with an omitted model, do not treat the pre-resume classification as current. For `compact`, same-session trustworthy classification may remain, but the current operation still keeps its bound profile. A stale last binding never authorizes another session.

[SCENARIO: SESSION-LIFECYCLE]

## Safe Claude Plugin lifecycle guidance

A status/version check is completely read-only. Separately report Claude Code version, Node availability and version, Marketplace name/source/scope, qualified Plugin identity, install scope, installed version, enabled state, and automatic/explicit entry availability. Use read-only official listing/details commands and their structured output; status must not refresh, install, update, enable, disable, remove, or write Config.

## Lifecycle write authorization transitions

Immediately before every install, update, or normal remove write, perform a fresh complete read-only ownership/source/scope/state recheck. An earlier status result is insufficient.

| Write | Fresh pre-write evidence | Outcome |
| --- | --- | --- |
| Install or update | Expected source, qualified identity, exact user scope, and unambiguous current state | Permit only the explicitly requested bounded write |
| Normal remove | Expected Marketplace/source, qualified identity, exact user scope, and unambiguous ownership and state | Permit only the qualified user-scope uninstall |
| Any write | Missing, unreadable, changed, mismatched, non-user, or multi-scope evidence | Stop without writes |

The only persistent source is the repository Marketplace `Mysterio1001/Ask-Then-Do-It`; the qualified Plugin is `ask-then-do-it@ask-then-do-it`; use `--scope user` whenever that official mutation accepts scope.

- If expected Marketplace and Plugin are absent and state is unambiguous, an explicit install may run `claude plugin marketplace add Mysterio1001/Ask-Then-Do-It --scope user`, then `claude plugin install ask-then-do-it@ask-then-do-it --scope user`.
- If only the expected Plugin is absent, run only `claude plugin install ask-then-do-it@ask-then-do-it --scope user` without re-adding the Marketplace.
- If the target version is installed, return a no-op. Preserve the disabled choice and never enable it implicitly; enabling is a separate user action.
- For an older expected installation, an explicit update may refresh only the expected Marketplace using the official refresh command (which may not accept a scope flag), then run `claude plugin update ask-then-do-it@ask-then-do-it --scope user`, preserving disabled state. Verify pre/post source and scope when a command does not accept `--scope`.
- If the installed version is newer than the target, stop rather than downgrade.
- Node missing or below 22 does not prevent an otherwise safe explicit lifecycle action, but report that automatic routing is unavailable and do not claim full support.
- Stop without writes for unsupported Claude Code, source mismatch, same-name other Marketplace, non-user or multi-scope ambiguity, unreadable/invalid state, or any unsafe ownership result. Do not remove-first or guess another source.
- After a partial failure, stop, perform a read-only recheck, and report exactly which portions succeeded and failed; do not hide state with destructive rollback.

After install/update, require `/reload-plugins` or a new session before claiming new bytes are active. Do not enable background auto-update or describe host auto-update settings as Plugin behavior.

A normal remove may run only `claude plugin uninstall ask-then-do-it@ask-then-do-it --scope user`. It must not remove the Marketplace, either Ask Then Do It Config, or other scopes. Before removing the last scope, disclose that Plugin data contains only rebuildable routing state and is deleted by default; add `--keep-data` only after an explicit user request. Full purge is a separate scope.

ZIP recovery is session-only: invoke `claude` with `--plugin-dir` and the extracted Plugin path as separate argument-vector values for that session. It must not create a Marketplace or persistent installation and must not be described as install/update state.

[SCENARIO: INSTALL-STATUS]
[SCENARIO: INSTALL-WRITES]
[SCENARIO: REMOVE-ZIP]

## Documentation and release boundaries

Documentation and package work must preserve three-language ownership, exactly two supported namespaced entries, and the exact package inventory. Marketplace metadata remains repository-only and excluded from consumer packages. Do not invent a third public command.

Release work must preserve all three package families, the completed 1.3.1 history byte-for-byte, deterministic evidence, secret and local-path scans, and the boundary between a local candidate and external publication. Tag, push, Release creation, upload, Marketplace activation, submission, and announcement require separate authority.

[SCENARIO: DOCS-PACKAGE]
[SCENARIO: RELEASE-INTEGRITY]
