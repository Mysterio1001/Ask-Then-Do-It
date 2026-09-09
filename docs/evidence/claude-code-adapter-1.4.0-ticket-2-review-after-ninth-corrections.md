# Claude Code Adapter 1.4.0 Ticket 2 Review after Ninth Corrections

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-2-review-after-ninth-corrections`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Status: Changes requested — 2 actionable P2 findings

Review label: `independent`

Ticket execution mode: `tdd`

Review capability: `multi_agent`

## Findings

### [P2] Persisting a post-failure sidecar bypasses the approved single-file state contract

**Location:** `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:667` (construction and lifecycle at lines 672–735, route authority at lines 1397–1399, and creation at line 1609). **Trigger:** every locatable `PostModelSwitch` creates `.<session-key>.json.post-failure`; any later Post failure intentionally retains it. **Impact:** this regular file is durable routing authority outside the Specification's sole approved `${CLAUDE_PLUGIN_DATA}/routing/v1/sessions/<session-key>.json` path and exact state schema. If Post fails before a canonical JSON state exists, cleanup at lines 1188–1213 never discovers the orphan because it enumerates only `<64-hex>.json`, so the sidecar can remain indefinitely and block both public entries for that session until a qualifying `SessionStart` repairs it. **Existing guard:** the fence correctly fails closed, rejects non-regular fence objects, is cleared by a successful Post or qualifying SessionStart, and is removed alongside an expired discoverable JSON state; those guards protect the new behavior but do not authorize the second persistent state representation or clean an orphan without a JSON peer. **Remediation:** represent the failure state through an approved canonical, schema-valid state design with bounded cleanup, or return to the Specification approval gate to explicitly authorize, version, validate, and clean this persistent sidecar before reimplementing it.

### [P2] `PostModelSwitch` writes routing data before the Node 22 eligibility gate

**Location:** `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1603` (write at line 1609; Node gate at line 1619) and `scripts/validate_claude_plugin.py:744`. **Trigger:** run a locatable `PostModelSwitch` on Node `<22`. `main()` derives a state path and establishes the post-failure fence before `checkNodeVersion(process.versions.node)` runs. **Impact:** an unsupported runtime mutates persistent routing data before eligibility is established; the retained fence can later stop both entries after Node is upgraded. The validator nevertheless reports that the Node gate precedes state access because its textual ordering check compares the gate only with the later exact declaration at router line 1620, missing the direct environment access and write at lines 1603–1610. **Existing guard:** the catch path returns a bounded fail-closed Post warning and does not change the active model, while old-Node expansion tests prove no write only for `UserPromptExpansion`; neither prevents the pre-gate Post write. A reviewer probe with simulated Node `21.9.0` reproduced exit `0` plus a newly created `.post-failure` file. **Remediation:** perform the Node gate before every state/path/fence operation while preserving the explicit entry's bounded `node-too-old` envelope; strengthen validation so all pre-gate state access is covered, and add Node `<22` no-write cases for Post and the other hook actions.

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — `finding`.** The Node-before-state policy is duplicated between runtime control flow, validator string matching, and focused tests; the validator and tests certify only a later marker and miss the earlier Post write described in P2 finding 2.
2. **Long Function — `no-finding`.** The longer parser, state validator, lock, and hook-dispatch functions remain internally cohesive, and no observed defect depended on a single function mixing unrelated decisions.
3. **Large Module or Class — `no-finding`.** Although `router.mjs` is large, the reviewed responsibilities form one zero-dependency, fail-closed session-routing boundary; the evidence did not show module size itself causing an additional actionable defect.
4. **Long Parameter List — `no-finding`.** Public helpers use bounded positional inputs plus option objects; no unstable coordination interface or call-site error was found.
5. **Data Clumps — `no-finding`.** Hook events, state, operations, pending switches, envelopes, and lock records are represented as validated cohesive records rather than repeated loose argument groups.
6. **Primitive Obsession — `no-finding`.** Domain strings and numbers are constrained by exact-key schemas, closed sets, regular expressions, byte limits, and transition checks; no additional primitive-value defect was found.
7. **Feature Envy — `not-applicable`.** The changed runtime is a procedural module without object ownership boundaries, and the reviewed functions operate on router-owned records rather than another component's encapsulated data.
8. **Divergent Change — `no-finding`.** All reviewed production changes concern the single route/state/security contract; no unrelated change axis was identified in this Ticket scope.
9. **Shotgun Surgery — `no-finding`.** Correcting behavior normally requires the owning runtime plus its validator and focused tests; no broader multi-module edit fan-out beyond those contract owners was demonstrated.
10. **Message Chains — `no-finding`.** Filesystem and event access are shallow and localized; no fragile navigation chain exposed hidden structure to callers.
11. **Leaky Abstraction — `finding`.** The `.post-failure` sentinel makes callers and cleanup logic depend on an undeclared second persistent state representation, as described in P2 finding 1.
12. **Shallow Module — `no-finding`.** The four hook actions expose a small interface over substantial validation, ownership, atomicity, locking, transition, and failure-envelope behavior.

## Verification performed

Reviewer-executed checks on 2026-09-08:

- `test_nonregular_post_failure_fence_blocks_both_public_entries` plus `test_compact_with_present_unmapped_model_recovers_nonready_state_as_unknown`: `Ran 2 tests in 1.476s`, `OK`.
- `test_ready_routes_prove_supported_claude_code_before_profile_loading`: `Ran 1 test in 0.001s`, `OK`.
- `scripts/validate_claude_plugin.py`: exit `0`, validation passed.
- `scripts/validate_claude_model_evidence.py` against the canonical mapping and fixture trace: exit `0`, evidence valid.
- `node --check adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs`: exit `0`.
- Read-only temporary probe of `PostModelSwitch` with simulated Node `21.9.0`: exit `0`; `CLAUDE_PLUGIN_DATA` was created and contained `routing/v1/sessions/.<session-key>.json.post-failure`, confirming finding 2 and the orphan form in finding 1.

Supplied raw verification, distinguished from reviewer execution:

- Ninth Red before correction: combined 2-test run exited `1`, `Ran 2 in 1.399s`, with 4 failures; the non-regular fence routes were incorrectly ready and present-unmapped compact did not recover `pending`/`indeterminate`.
- Focused Green after stronger assertions: `Ran 2 in 1.970s`, `OK`.
- Narrow adjacent audit: 5 tests, `Ran 5 in 14.101s`, `OK`; this is not claimed as product restricted-tool reviewer evidence.
- Six adjacent modules: `Ran 79 in 75.772s`, `OK`, `skipped=1`.
- Claude suite: `Ran 106 in 92.210s`, `OK`, `skipped=1`.
- Full repository suite: `Ran 322 in 122.464s`, `OK`, `skipped=1`; the skip was the same Windows file-symlink privilege limitation, while the directory-junction guard passed.
- Node syntax, Plugin validator, model-evidence validator, and exact Claude Code `2.1.251` canonical Plugin/Marketplace strict validations were supplied as exit `0`; strict validation passed without warning. `git diff --check` was supplied as exit `0` apart from the pre-existing Knowledge Base LF-to-CRLF warning.
- Supplied router identity: 1,699 lines, 51,290 bytes, SHA-256 `d79905452072206bf02cdaf7788b34cd013e96f3e2527d0280a53464b2f20cd8`.

## Evidence unavailable

- No authenticated Claude Code session was available. Exact `2.1.251` namespaced invocation, same-invocation `UserPromptExpansion.additionalContext`, hook timing, Post failure behavior, resume/compact behavior, and bare-alias observation remain unavailable as live evidence.
- The reviewer did not independently rerun the 106-test Claude suite or 322-test repository suite; their raw outcomes above were supplied.
- File-symlink execution evidence is unavailable on this Windows host because of the reported privilege limitation; directory-junction rejection evidence is available.
- No prior Ticket 2 review, architecture diagnosis, implementation-evidence artifact, or implementer conclusion was inspected or used.

## Reviewed inputs and assumptions

Reviewed inputs: Approved `docs/specs/claude-code-adapter-1.4.0.md`; Approved Ticket 2 in `docs/plans/claude-code-adapter-1.4.0.md`; only the necessary routing/version portions of `docs/requirements/claude-code-adapter-1.4.0.md`; final `hooks/hooks.json`, `config/model-classifications.json`, `scripts/router.mjs`, and both public `SKILL.md` files; `scripts/validate_claude_plugin.py`; `scripts/validate_claude_model_evidence.py`; and final `tests/claude/` fixtures and focused tests.

Assumptions: the current-operation top-level mode was already proven as Full by absent Project and User Config; Ticket mode is the Approved `tdd`; this reviewer context did not implement the change and was not given implementer defenses or a proposed verdict; the supplied raw command outcomes are accurate but are not substituted for unavailable authenticated-host evidence.

Deferred checks: Ticket 3's authenticated exact-host ledger and all downstream profile, conformance, packaging, documentation, context-proxy, release, and publication gates remain outside this Ticket review.

## Residual risk, completion, and handoff

Ticket 3 remains a hard gate: exact Claude Code `2.1.251` strict validation alone does not establish authenticated namespaced command identity, route-envelope delivery, hook/failure semantics, race timing, or bare-alias behavior. The documented automatic `PostModelSwitch` commit race remains best effort and must not be represented as a first-invocation guarantee.

Ticket 2 does **not** appear complete while the two P2 findings remain unresolved. Passing tests and validators do not override the approved persistent-state boundary or the reproduced pre-gate write.

Next handoff: return both findings to the Ticket 2 `tdd` implementation owner for a new failing test and correction. Finding 1 must return to the Specification approval gate if the sidecar design is retained. After corrections, rerun focused router/state/security tests, both validators, the Claude and full repository suites, then obtain another fresh independent Review. Ticket 3's authenticated host ledger must still pass before local `1.4.0` completion.
