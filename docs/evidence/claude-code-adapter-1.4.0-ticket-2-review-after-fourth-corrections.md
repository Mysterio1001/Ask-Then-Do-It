# Claude Code Adapter 1.4.0 Ticket 2 Review after Fourth Corrections

artifact_type: Review Report

artifact_id: `claude-code-adapter-1.4.0-ticket-2-review-after-fourth-corrections`

workflow_id: `claude-code-adapter`

core_version: `1.3.0`

status: Changes Requested

ticket_mode: `tdd`

review_label: `independent`

## Findings

### P1 — Regex-shaped unknown model IDs can persist secrets or PII

Trigger: an otherwise valid `SessionStart.model`, `PreModelSwitch.from_model`, or `PostModelSwitch.to_model` value such as `claude-tenant-secretmarker-9f23d1` matches the router's permissive canonical-looking regex but is absent from the release-owned exact mapping. Impact: the untrusted value is classified as `unknown` yet is retained verbatim as `model_id` or `pending_switch.from_model` under `${CLAUDE_PLUGIN_DATA}`, violating the approved prohibition on persisting credentials, secrets, tokens, or personal data. The tight production locations are `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:238`, `:1223`, `:1254`, `:1350`, `:1366`, `:1402`, and `:1436`. There is no existing guard: the secret-scrubbing tests use syntactically noncanonical `custom-gateway/...` inputs, while `tests/claude/test_router_security.py:408` explicitly asserts that an unmapped regex-shaped value is preserved. A fresh adversarial probe confirmed the marker in the persisted state. Remediation direction: retain exact IDs only when they are allowlisted by the release-owned mapping; represent every other syntactically valid/unmapped value as `model_id: null` plus `unknown`, and avoid retaining an unallowlisted `from_model` in pending state. Add SessionStart, Pre, and Post regression cases whose secret marker also matches the current regex.

### P2 — A canonical PreModelSwitch mismatch leaves stale state routable

Trigger: ready state records one model, but a requested `PreModelSwitch` supplies a different regex-valid `from_model`; if Claude applies the switch and the next request arrives before the delayed Post hook commits, `handlePreModelSwitch` throws at `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1356` without marking the writable state `indeterminate`. The outer handler at `:1540` emits a nonblocking warning but leaves `routing_status: ready`, so an immediate automatic entry can use the stale classification and may even begin an operation on a now-unsupported active model. This violates the approved impossible-transition fail-closed rule while still correctly avoiding denial of the user's model switch. There is no guard: noncanonical Pre values are made indeterminate and Post mismatches are tested, but `tests/claude/test_router_state.py:400` covers only a missing-state Pre failure. A fresh probe reproduced a successful stale `general` route after the mismatch warning. Remediation direction: when ready, same-session state is writable but its known model disagrees with a canonical Pre `from_model`, atomically mark it `indeterminate`, preserve the operation binding, emit the nonblocking warning, and add a next-entry failure regression.

### P2 — Ready-route disclosure codes are not converted into user-facing disclosure instructions

Trigger: automatic routing receives a valid unknown model, explicit `-5` receives a valid unknown model, or explicit `-5` receives a known supported non-5 model. The router emits `unknown-model-general-compatibility`, `unknown-model-explicit-claude-5`, or `non-claude-5-explicit-general`, but the bootstraps only validate those tuple literals and then direct Claude to load the selected profile. Impact: the workflow may enter general or optimized instructions without telling the user that it is in compatibility mode, cannot verify Claude 5, or is falling back from an incompatible explicit request, contrary to the approved route table and acceptance criteria 6–7. The tight locations are `adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md:16` and `:20`, plus `skills/ask-then-do-it-5/SKILL.md:16` and `:22`. There is no later guard: repository search finds these codes only in router emission and literal contract validation; `scripts/validate_claude_plugin.py:343` and `:356` lock in the incomplete bodies, while `tests/claude/test_router_contract.py:349` checks code presence rather than observable disclosure. Remediation direction: assign mandatory, explicit user-facing wording/behavior to every non-`none` ready disclosure code before loading the selected profile, update the canonical validator body, and test observable instructions for all three routes.

### P2 — Successful PostModelSwitch does not instruct Claude to notify the user of the switch and synchronization

Trigger: an operation exists and a requested or automatic `PostModelSwitch` commits successfully to a supported or unknown model. `continuationContext` says only to retain the bound profile and defer rerouting; it mentions the support change only for an unsupported model. Impact: Claude is not instructed to tell the user that the model changed and routing state synchronized, so the required notification and next-permitted-entry boundary can be silent on ordinary successful switches. The tight location is `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1195`, invoked by the successful path at `:1443`. There is no system-message or bootstrap guard on this path; `tests/claude/test_router_state.py:242` asserts only the operation ID, profile, and next-entry phrase. Remediation direction: make successful Post context explicitly instruct Claude to notify the user that the active model changed, state synchronization completed, the current operation keeps its profile, and only the next permitted public entry reroutes; add requested/automatic and supported/unknown assertions.

### P2 — Same-session clear resets model generation instead of preserving monotonic order

Trigger: after one or more committed model transitions, Claude emits `SessionStart` with source `clear` while reusing the same session ID. `handleSessionStart` excludes `clear` from prior-state reads at `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1227`, then initializes generation to `0` at `:1235`–`:1253`. Impact: one session key can observe generation `1` followed by `0`, creating duplicate/order-ambiguous generations and violating the approved monotonic-generation state contract. There is no guard: the lifecycle test clears only at generation zero, and `tests/claude/test_router_security.py:226`–`:233` currently codifies the reset. A fresh probe reproduced `1 -> 0`. Remediation direction: for a same-key clear, validate/read prior state solely to advance the generation while still clearing model and operation; if a reset is intentionally an epoch boundary, the state schema and approved specification must first represent that epoch explicitly. Add a clear-after-switch regression.

## Inputs

- Applicable repository instructions: no workspace `AGENTS.md`, `CLAUDE.md`, project workflow Config, or user workflow Config was present; the top-level resolver therefore proved Full fallback for this operation.
- Approved Requirement: `docs/requirements/claude-code-adapter-1.4.0.md`.
- Approved Specification: `docs/specs/claude-code-adapter-1.4.0.md`.
- Approved Ticket: Ticket 2 in `docs/plans/claude-code-adapter-1.4.0.md`; its Approved execution mode is `tdd`, matching the supplied mode.
- Final production and surrounding files: `hooks/hooks.json`, `scripts/router.mjs`, `config/model-classifications.json`, both public Skill `SKILL.md` files, `scripts/validate_claude_plugin.py`, and `scripts/validate_claude_model_evidence.py`.
- Tests and fixtures: the seven named Ticket 2 test modules and `tests/claude/fixtures/model-classifications/`.
- Supplied raw verification: focused canonical persistence/control `Ran 4 tests in 1.214s; OK`; explicit fallback version gate `Ran 1 test in 0.001s; OK`; adjacent router/state/security/public suite `Ran 44 tests in 32.479s; OK (skipped=1)`; Claude suite `Ran 93 tests in 59.178s; OK (skipped=1)`; full repository `Ran 309 tests in 84.825s; OK (skipped=1)`; Node syntax, both repository validators, and `git diff --check` exit `0` except the existing user-owned Knowledge Base LF-to-CRLF warning.
- Supplied exact-host boundary evidence: exact Claude Code `2.1.251`, canonical Plugin strict validation, and repository Marketplace strict validation exited `0` without warnings. This is validation evidence, not an authenticated interactive host-session observation.
- Existing Ticket 2 Review Reports and implementer verdicts were deliberately not read.

## Assumptions

- The supplied approvals and raw test summaries are authentic records of the named commands; reviewer-run commands below were used as independent confirmation where the environment permitted.
- Ticket 3 remains the approved owner of authenticated namespaced invocation, live `additionalContext`, bare-alias observation, and exact failure-semantics evidence. Its incompleteness does not excuse deterministic Ticket 2 defects but prevents calling host-dependent behavior live verified.
- The review scope is the complete final Ticket 2 state, not only the most recent corrections. Later profile, conformance, documentation, lifecycle, packaging, and release tickets remain outside this Ticket's completion claim except where their current files form a direct regression boundary.

## Verification

Reviewer-run verification:

- `.venv\\Scripts\\python.exe -m unittest discover -s tests/claude -p 'test_*.py'` → `Ran 93 tests in 60.349s`; `OK (skipped=1)`.
- The sole skip was `test_state_file_symlink_is_not_followed`, because this Windows account lacks file-symlink creation privilege (`WinError 1314`). The directory-junction protection test passed.
- The first attempt with the bundled Python ran 85 discovered tests but could not import `test_public_plugin_contract.py` because that runtime lacked the repository-declared PyYAML dependency. Re-running with the repository `.venv` loaded PyYAML `6.0.3`; the public-contract module passed 9/9 and the complete Claude suite then passed as above. This setup failure is not treated as a product-test failure.
- Bundled Node `--check adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs` → exit `0`.
- `.venv\\Scripts\\python.exe scripts/validate_claude_plugin.py` → exit `0`.
- `.venv\\Scripts\\python.exe scripts/validate_claude_model_evidence.py --mapping ... --trace ...` → exit `0`.
- `git diff --check` → exit `0`; only the pre-existing user-owned `docs/project/knowledge-base.md` LF-to-CRLF warning was emitted.
- A reviewer-run temporary adversarial probe produced `persisted_unknown_model_id: claude-tenant-secretmarker-9f23d1`, routed `ready/general/none` immediately after a canonical Pre mismatch warning, and observed generation `[1, 0]` across a same-key clear. The temporary directory was removed after the probe.
- Two fresh, non-implementing, read-only reviewer contexts independently inspected state/security and model/public-contract boundaries. Their isolated probes reproduced findings 1, 2, and 5; static production/test tracing established findings 3 and 4. Their broader checks also reported Codex 27/27, Generic 39/39, Conformance 19/19, and Release 131/131 passing.

Coverage assessment:

- Exact mapping, known/unsupported/unknown/custom routing, both entry identities, all five SessionStart sources, requested and automatic switch sources, operation preservation, failure envelopes, bounded reads, stale-state rejection, cross-session hashing, lock reclamation, atomic replacement, cleanup, mapping trace integrity, provider boundaries, and the two approved manual-fallback prerequisites have substantial positive and negative coverage.
- The suite does not currently fail for regex-shaped secret persistence, canonical Pre mismatch followed by an immediate entry, required ready-route user disclosure, ordinary successful Post notification, or clear-after-nonzero generation. The future-ID and clear assertions currently preserve two of those defects, so the green suite is not sufficient acceptance evidence for those clauses.

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — `finding`.** Finding 3 shows the ready-disclosure policy split among router code values, two public Skill bodies, literal validator bodies, and string-presence tests. The duplication allows the enum to remain internally consistent while omitting its user-facing semantic action. Trigger, impact, locations, missing guard, and remediation are recorded in Finding 3.
2. **Long Function — `no-finding`.** The 1,563-line router is decomposed into focused parsing, mapping, locking, state, transition, and output functions; the reviewed defects arise from missing invariants rather than a single unreviewable long function.
3. **Large Module or Class — `no-finding`.** `router.mjs` is large but owns one dependency-free hook/runtime trust boundary, exposes narrow actions, and has focused state/lock tests. Within Ticket 2 evidence, splitting it is not required to remediate the findings.
4. **Long Parameter List — `no-finding`.** Event and state values travel as validated objects, while the longest reviewed helper signatures remain bounded and stable.
5. **Data Clumps — `no-finding`.** Envelope, operation, pending-switch, lock, event, and state fields are represented and validated as coherent records rather than repeated independent parameters.
6. **Primitive Obsession — `no-finding`.** Although strings represent classifications, statuses, actions, sources, and disclosure codes, closed sets, exact tuple validation, schema checks, and tests constrain them. The missing disclosure behavior is captured as Finding 3 rather than an unconstrained-primitive issue.
7. **Feature Envy — `no-finding`.** Mapping, filesystem locking, state transitions, and bootstrap validation each primarily operate on data owned by their local boundary.
8. **Divergent Change — `no-finding`.** Mapping data and evidence are externalized, while host event changes converge on one router boundary; no additional unrelated change axis was shown to require modifying the same internal function.
9. **Shotgun Surgery — `no-finding`.** The intentionally duplicated public/validator contract requires coordinated edits, but validators and mutation tests detect ordinary drift. Finding 3 concerns missing semantics across that contract, not evidence that routine unrelated changes require broad surgery.
10. **Message Chains — `no-finding`.** Hook input is validated at the boundary and handlers receive direct event/state records; no caller chain exposes nested internals or creates a material defect.
11. **Leaky Abstraction — `no-finding`.** Public Skills intentionally know the bounded route-envelope schema as a trust boundary but do not know raw session IDs, paths, hook input, locks, or state-file mechanics.
12. **Shallow Module — `no-finding`.** Four hook actions and two framed route outcomes hide substantial validation, classification, state ownership, locking, atomicity, lifecycle, and failure handling; interface complexity is justified by the hidden behavior.

## Deferred and unavailable evidence

- Authenticated exact-host invocation identity, live `additionalContext` visibility, bare aliases, Node unavailable/nonzero/exit-2/timeout behavior, and real Post ordering remain Ticket 3 evidence and are `unverified` here.
- The state-file symlink runtime branch is `unverified` on this account because Windows denied symlink creation. Static rejection logic and the directory-junction branch were verified.
- No nine-cell OS/surface live matrix or clean release smoke was attempted; those are later approved gates, not Ticket 2 acceptance evidence.
- The review did not modify production, tests, requirements, specification, plan, Knowledge Base, implementation evidence, or prior Reviews.

## Residual risks

- The router's lock protocol is necessarily platform-sensitive. Concurrent route, live-lock, stale-dead-lock, replacement-token, cleanup-lock, atomic-write, path-space, and junction tests passed, but file-symlink behavior is not live proven on this Windows identity.
- Mapping evidence uses checked, hashed normalized snapshots and an exact semantic digest. It protects the release freeze against silent drift, but future/custom model IDs intentionally remain unknown and require a future release to become trusted.
- Claude Code may complete an automatic Post hook after a request; the approved best-effort race remains even after the requested-switch mismatch defect is fixed and must remain disclosed rather than upgraded to a first-invocation guarantee.
- Passing current regression suites cannot compensate for missing behavioral assertions identified in the findings.

## Completion assessment

Ticket 2 does **not** appear complete. Findings 1–5 are actionable violations of the Approved Requirement, Specification, and Ticket acceptance boundaries. The verdict is **Changes Requested** with five findings (`P1: 1`, `P2: 4`). No production correction is authorized by this Review.

## Handoff

Return Ticket 2 to the approved `tdd` implementation path. Add failing tests for all five triggers before production changes, implement the smallest state/bootstrap corrections, rerun focused state/security/public-contract tests, the complete Claude suite, adjacent provider/release regressions, validators, Node syntax, and `git diff --check`, then request a fresh independent Review. Ticket 3's authenticated exact-host gate remains required afterward and any observed contract difference must reopen the earliest affected approved artifact.
