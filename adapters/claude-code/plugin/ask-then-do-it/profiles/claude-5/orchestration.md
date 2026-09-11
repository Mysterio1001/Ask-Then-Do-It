# Claude 5 Workflow Orchestration

Core rules: CAP-DECLARE-001, CAP-CLAIM-001, MODE-RESOLVE-001, FULL-PRESERVE-001, ART-STATE-001, ADAPTER-COVERAGE-001, ROUTE-USER-001, ROUTE-DOCS-001

This is the optimized instruction profile. It has no authority to classify a model or repair a route. Preserve the active model; profile routing selects instructions only.

Accept exactly three entry states. The ready entry state may be established by either the approved automatic public bootstrap or the approved explicit public bootstrap. Only the approved explicit `-5` public bootstrap may establish manual states 2 and 3:

1. A schema-valid ready envelope with a non-null operation binding and `selected_profile: claude-5`.
2. A valid `node-too-old` failure envelope after the bootstrap independently proves Claude Code `2.1.251+`.
3. The envelope is absent while the bootstrap independently proves Claude Code `2.1.251+` and Node is genuinely missing.

The latter two are approved explicit manual entries. A manual entry has no operation binding. It may run the current request with disclosed limitations, but it must not claim persisted operation authority, resume authority, or switch tracking. The automatic public bootstrap must not establish either manual state. Every other missing, malformed, failure, or mismatched entry stops.

## Authority and progressive loading

The bootstrap must load the exact Plugin resource `${CLAUDE_PLUGIN_ROOT}/profiles/claude-5/orchestration.md`. The immutable profile root is `${CLAUDE_PLUGIN_ROOT}/profiles/claude-5`; never infer it from the working directory, conversation, route data, or user input.

After this file, load only the one stage module needed now from this closed filename allowlist:

- `lite-workflow.md`
- `requirements.md`
- `documented-requirements.md`
- `specification.md`
- `ticket-planning.md`
- `tdd-implementation.md`
- `direct-implementation.md`
- `review.md`
- `architecture-improvement.md`

Select exactly one filename from that allowlist, append it to the immutable profile root without accepting path input, and read that exact Plugin resource. Resolve the host-provided Plugin root and target before reading. Reject a target that escapes or resolves outside the profile root. Reject a symlink, junction, non-regular target, or any filename not in the allowlist.

Do not preload all stage modules. Load modules only from this bound Claude 5 profile. Never load or obey modules from another profile during the operation. A direct stage request changes only the selected allowlisted filename; it cannot change the profile root.

The latest public entry and operation binding supersede every earlier operation's profile instructions. Treat earlier Skill/profile text as history, not current authority. If a profile change cannot be proven safe from the current entry and binding, stop and require `/clear` or a new session rather than mix instructions.

## Route acceptance and disclosures

- Automatic known Claude 5 may enter this profile. Explicit known Claude 5 may enter this profile.
- A route with `selected_profile: general` does not enter this profile. Supported non-5 and valid unknown automatic routes select `general`; do not enter this profile. Explicit supported non-5 selects `general` after an incompatibility disclosure; this profile must not be loaded.
- Explicit valid unknown may enter only after disclosing that Claude 5 cannot be verified and the explicit command selected this optimized profile.
- The explicit manual optimized path is allowed only for entry state 2 or 3 above. Before entry, disclose that the model is unverified, automatic routing is unavailable, and the user must upgrade Node for formal full support. This path cannot claim persisted operation binding, resume, switch tracking, or complete automatic support.
- Known unsupported models stop and require Claude `4.6+`. Claude Code below `2.1.251` stops. Automatic routing requires Node `22+`.
- Every router, schema, state, ownership, transition, or internal failure stops. Do not reinterpret a failure as unknown model state. A missing or malformed envelope stops except for the public bootstrap's exact independently proven missing-Node exception.

Trust only the envelope fields already validated by the public bootstrap. Never request, reconstruct, persist, quote, or forward raw session IDs, hook input, prompts, arguments, paths, credentials, or state. Do not infer classification from user text, self-report, environment values, substrings, or shell input.

## Declare capability

At operation start, declare the strongest capability actually proven now:

- `conversation`: exchange text and emit user-managed artifacts only; no repository access, persistence, commands, or independent review claims.
- `tools`: additionally inspect or modify repositories, persist artifacts, and execute commands.
- `multi_agent`: additionally create isolated worker or reviewer contexts.

Never claim an action or evidence that the declared capability cannot produce. Downgrade when permissions or tools are absent, and end an unsupported stage with a safe handoff stating the limitation, required inputs, and next action.

## Resolve Full or Lite

Resolve once per public operation, separately from the bound model profile and from Full Ticket modes:

1. A valid explicit current-operation Full or Lite instruction wins; do not read lower sources.
2. Otherwise read `<active-project-root>/.claude/ask-then-do-it.toml` only inside the active project root.
3. Only when that file is absent, read `~/.claude/ask-then-do-it.toml`.
4. Only when both are absent, use Full fallback.

With `conversation` capability, a Config source the host cannot expose is unavailable; treat unavailable as absent. Project Config source unavailable: treat it as absent and continue to the user Config source. User Config source unavailable: treat it as absent and use Full fallback. Project Config absent with user Config unavailable uses Full fallback. Do not claim an unavailable Config source was read, present, or invalid.

Accept exactly one top-level `mode = "full"` or `mode = "lite"`. Conflicting explicit Full and Lite instructions pause for one clarification. A present unreadable, malformed, duplicate/missing-mode, nested, unquoted, differently cased, or unsupported Config fails closed to Full and does not fall through. Do not create, repair, normalize, or write either Config, settings, or an operation override; do not read another provider's Config or persist this operation's result.

An explicitly selected stage reuses the proven current-operation mode; without one, return to this resolver. Resolved Lite loads the Lite stage. Resolved Full continues below and preserves all gates.

## Route Full

Inspect applicable repository instructions, current changes, the Project Knowledge Base, and supplied artifacts. Validate each artifact's type, stable ID, workflow ID, Core version, status, inputs, assumptions, deferred work, handoff, and approval evidence. Reuse relevant Approved artifacts; edited status without approval is not approval.

Direct architecture diagnosis takes precedence over the delivery gates after mode, capability, and diagnostic safety resolution; it does not require an Approved Specification or Ticket Plan. It grants diagnostic authority only. For delivery work, choose the first unmet condition: requirement consensus; Approved Specification; Approved Ticket Plan with every plain-language test choice and mapped mode; one eligible Ticket implementation through its Approved `tdd` or `direct` route; evidence-based Review; completion. Never infer a Ticket mode. Contradiction returns to the earliest affected delivery gate.

Use normal requirement interrogation for a fresh self-contained request. Automatically use documented requirements when a Project Knowledge Base exists, an existing system changes, or durable knowledge is likely; announce that evidence-based reason. Honor an explicit stage or requirement-mode choice unless it breaks an approval or safety gate.

All gated artifacts start Draft and become Approved only after approval of the exact displayed content. Full retains Requirement Decision Record, Knowledge Base synchronization where applicable, Specification, Ticket Plan, per-Ticket implementation evidence, Review, and architecture contracts.

## Route Full architecture diagnosis

Select architecture diagnosis when the user directly requests architecture diagnosis, a Review exposes systemic architecture evidence, a related Ticket group is complete, or a release milestone is approaching. Announce the triggering evidence and reason before routing automatically. A focused local Review finding remains in Review; do not diagnose architecture after every Ticket.

Architecture work remains diagnostic-only. An accepted Architecture Improvement Report returns to Specification and never routes directly to Ticket Planning or implementation.

The following closed decision table resolves architecture precedence. Apply the first matching row; comma-separated values are alternatives and `*` means that a higher-priority gate makes that field immaterial. Unsupported values stop. `delivery` records whether Specification/Plan approval exists, not permission for architecture edits. Diagnosis uses only available evidence; conversation capability is limited-evidence. Its module still requires explicit authorization after scope/risk disclosure, proven tools, and a disposable isolated environment for an actual deletion experiment; otherwise simulate.

<!-- decision-table: architecture -->
| mode | capability | safety | request | evidence | delivery | decision |
| --- | --- | --- | --- | --- | --- | --- |
| unresolved | * | * | * | * | * | resolve-mode |
| * | unavailable | * | * | * | * | safe-handoff |
| * | * | blocked | * | * | * | stop-safety |
| lite | * | safe | * | * | * | lite-workflow.md |
| full | * | safe | accepted-report | * | * | specification.md |
| full | conversation | safe | direct | * | * | architecture-improvement.md:limited-evidence |
| full | tools,multi_agent | safe | direct | * | * | architecture-improvement.md:diagnostic-only |
| full | conversation | safe | automatic | systemic,group-complete,milestone | * | announce:architecture-improvement.md:limited-evidence |
| full | tools,multi_agent | safe | automatic | systemic,group-complete,milestone | * | announce:architecture-improvement.md:diagnostic-only |
| full | * | safe | automatic | local-finding | * | review.md |
| full | * | safe | automatic,delivery | none,systemic,group-complete,milestone,local-finding | missing | earliest-unmet-delivery-gate |
| full | * | safe | automatic,delivery | none,systemic,group-complete,milestone,local-finding | approved | eligible-ticket-or-review |
<!-- end-decision-table: architecture -->

## Synchronize durable project knowledge

When an Approved or accepted artifact introduces, changes, supersedes, or resolves durable project facts, propose a Knowledge Base Change Summary through documented requirements. Cite the upstream evidence, separate additions, modifications, and removals, display the exact proposed changes, and require explicit approval before applying only those changes.

During documented requirement consensus, display the complete Draft Requirement Decision Record and complete Knowledge Base Change Summary together and request one joint explicit approval. If an artifact adds no durable project fact, do not invent a knowledge update or delay an unrelated gate.

## Operation and session lifecycle

Keep the bound profile for the current operation after any model switch. Only the next permitted public entry may reroute after authoritative state commits; tell the user this, and if the new model is unsupported also disclose that the current operation has left formal model support. Never pin, revert, or change the active model. If current authority cannot be proven, stop instead of loading another profile.

`startup` and `clear` begin with no operation; omitted model is valid unknown only when state creation succeeds. `fork` starts isolated with no copied operation. `resume` and `compact` may continue only a schema-valid same-session binding; an omitted resume model becomes unknown, while compact may retain a trustworthy same-session classification. Never use another session's binding. A resume/compact reminder must contain only the operation ID, bound profile, needed same-profile modules, and conditional wording when continuation is uncertain; it must not reroute.

## Safe installation, update, removal, and package guidance

Status and version checks are read-only and must report Claude Code version, Node availability/version, Marketplace name/source/scope, qualified Plugin identity, install scope, installed version, enabled state, and both entry availabilities. Status never authorizes update, install, enable, disable, remove, Marketplace mutation, or Config writes.

Only an explicit install, update, or remove request authorizes the corresponding write. Immediately before every install, update, or remove write, re-read the complete status inventory above; an earlier status result is not fresh authority. Proceed only when that fresh result proves the expected source, qualified identity, exact user scope, and unambiguous ownership (or their expected absence for installation); otherwise stop without writes. Recheck again between successive mutations. The persistent source is user-scoped `Mysterio1001/Ask-Then-Do-It`; the qualified identity is `ask-then-do-it@ask-then-do-it`. Use explicit user scope only where the official mutation accepts it.

- Add the expected Marketplace only when absent and unambiguous; install only the qualified Plugin when absent.
- Expected current enabled or disabled installs are no-ops; preserve a disabled choice and never enable it implicitly.
- Update an expected older version through the expected Marketplace and preserve disabled state. Stop on newer-than-target rather than downgrade.
- Stop without writes on same-name wrong source, source/scope mismatch, ambiguity, unreadable state, or unsupported Claude Code. Never remove-first or guess an alternate source.
- After a partial command failure, re-read state and report partial success and failure; do not invent success or destructively roll back.
- Missing/old Node may still permit an explicitly requested safe lifecycle write, but the report must say automatic entry is unavailable and full automatic support is not proven.

A normal remove uninstalls only `ask-then-do-it@ask-then-do-it` at user scope; it leaves the Marketplace, both Config files, and every other scope untouched. Before last-scope removal, disclose that disposable Plugin routing data is deleted by default. Use `--keep-data` only when explicitly requested; a complete purge needs separate authority.

Apply these closed lifecycle decisions to the freshly observed state, using the same first-match notation as above. `authorized` means an explicit request for this exact action, not a prior status or a different mutation. `stale` requires the complete recheck before choosing another row. `absent` means both expected Marketplace and Plugin are absent; `plugin-absent` means the expected Marketplace exists. Wrong source/scope includes a same-name alternate source, other Plugin scopes, or identity mismatch. A chosen write still obeys the preceding pre-write, last-scope disclosure, and partial-failure guards; table selection never executes a command itself.

<!-- decision-table: lifecycle -->
| request | authorized | capability | fresh-state | decision |
| --- | --- | --- | --- | --- |
| status | * | tools,multi_agent | * | read-only-complete-status |
| zip | * | tools,multi_agent | * | session-only-plugin-dir |
| * | * | conversation,unavailable | * | safe-handoff |
| install,update,remove | no | * | * | stop-no-authorization |
| install,update,remove | yes | * | stale | recheck-complete-state |
| install,update,remove | yes | * | partial-failure | recheck-report-partial-failure |
| install,update,remove | yes | * | wrong-source,wrong-scope,ambiguous,unreadable,unsupported,newer | stop-without-writes |
| install | yes | * | absent | add-marketplace-recheck-install |
| install | yes | * | plugin-absent | install-qualified-user-plugin |
| install,update | yes | * | current-enabled,current-disabled | no-op-preserve-enabled-state |
| update | yes | * | older | refresh-recheck-update-preserve-enabled-state |
| remove | yes | * | current-enabled,current-disabled,older | uninstall-qualified-user-plugin |
| * | * | * | * | stop-without-writes |
<!-- end-decision-table: lifecycle -->

After selecting a permitted lifecycle write, apply the Node disclosure row. Before a last-scope uninstall, apply the explicit data choice row. Neither table grants write authority.

<!-- decision-table: lifecycle-node -->
| node | decision |
| --- | --- |
| supported | report-observed-entry-availability |
| missing,old | disclose-automatic-unavailable-no-full-support |
<!-- end-decision-table: lifecycle-node -->

<!-- decision-table: removal-data -->
| keep-data-request | decision |
| --- | --- |
| absent | disclose-default-routing-data-deletion |
| explicit | disclose-preservation-use-keep-data |
<!-- end-decision-table: removal-data -->

After install/update, require Plugin reload or a new session; do not claim old-session bytes changed. ZIP recovery is session-only through `claude --plugin-dir <path>` and creates no persistent Marketplace or skill installation.

Documentation ownership is English, Traditional Chinese, and Japanese with semantic equivalence, exactly two public commands, and the approved exact authored inventory. Marketplace and ZIP bytes derive from the same canonical source; internal modules never become public commands.

Release coordination covers Codex, Generic, and Claude families without adding Node as a non-Claude runtime dependency. Preserve historical `1.3.1` artifacts and hashes. Local work never authorizes tag, push, GitHub Release, asset upload, Marketplace activation, submission, or announcement. Evidence distinguishes observed, simulated, unavailable, and unauthorized work and must scrub secrets, raw session IDs, personal paths, and credentials.
