# Ticket 2 Review after third corrections

Review label: `independent`

Verdict: `changes-requested` — 2 actionable findings (`P2`: 2).

## Findings

### [P2] Noncanonical hook model text is persisted instead of canonical-or-null state

Trigger: provide a schema-shaped `SessionStart.model` or `PostModelSwitch.to_model` such as `gateway/模型-α` or another credential/PII-like noncanonical string; a requested switch can likewise supply that text in `PreModelSwitch.from_model`. The generic identifier guard accepts it, `SessionStart`/`PostModelSwitch` persist it as `model_id`, and `PreModelSwitch` persists it as `pending_switch.from_model`. Impact: this violates the approved state schema, which permits a canonical model ID or `null`, and allows untrusted noncanonical text to remain in persistent Plugin data for up to 30 days despite the secret/PII exclusion. The existing positive test at `tests/claude/test_router_security.py:259` demonstrates the trigger by accepting `gateway/模型-α` and checking only that its classification is `unknown`, so the current suite would not catch the persistence defect. Tight locations: `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:986`, `:1213`, `:1243`, `:1339`, `:1353`, `:1387`, and `:1421`. Remediation direction: introduce a distinct canonical-model-ID validation/normalization boundary; convert noncanonical host values to `null`/`unknown` without copying the raw value into state or pending transition data, or fail closed where transition ownership cannot then be proved. Add SessionStart, PreModelSwitch, and PostModelSwitch tests using noncanonical and secret-marker values that assert the marker is absent from every persisted byte and model-visible output.

### [P2] A valid `node-too-old` envelope bypasses the Claude Code minimum-version gate

Trigger: invoke the explicit `-5` entry on a Claude Code version below `2.1.251` in an environment where the provisional `UserPromptExpansion` hook still runs and Node is below 22. The router produces a valid `node-too-old` failure envelope, and the explicit Skill immediately directs Claude to use the manual optimized fallback; its separate Claude Code version proof is required only for the missing-envelope branch. Impact: the workflow can start on a known unsupported Claude Code host, contrary to the route table and the rule that explicit manual fallback is permitted only after Claude Code `2.1.251+` has been independently proved. This is material while Ticket 3's exact host semantics remain unverified. Tight location: `adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it-5/SKILL.md:18` (contrast the missing-envelope-only proof at `:20`). Remediation direction: require and describe independent Claude Code `2.1.251+` proof before following *either* manual fallback branch, and add a negative contract test showing that a valid `node-too-old` envelope plus known old/unprovable Claude Code stops rather than loading the optimized profile.

## Artifact metadata

- `artifact_type`: Review Report
- `artifact_id`: `claude-code-adapter-1.4.0-ticket-2-review-after-third-corrections`
- `workflow_id`: `claude-code-adapter`
- `core_version`: `1.3.0`
- `status`: `changes-requested`
- `ticket_mode`: `tdd`
- `review_label`: `independent`
- `reviewed_at`: `2026-09-07` (`Asia/Taipei`)

## Inputs

- Approved Specification: `docs/specs/claude-code-adapter-1.4.0.md`.
- Approved Ticket Plan: Ticket 2 in `docs/plans/claude-code-adapter-1.4.0.md`, including acceptance criteria 6–10 and the automated portion of criterion 22.
- Final production and surrounding files: `hooks/hooks.json`, `scripts/router.mjs`, `config/model-classifications.json`, both public Skill `SKILL.md` files, `scripts/validate_claude_plugin.py`, and `scripts/validate_claude_model_evidence.py`.
- Test changes and surrounding tests: the seven named Claude test modules plus `tests/claude/fixtures/model-classifications/`.
- Supplied raw Red evidence: generation-exhaustion batch (`Ran 2 tests`, three failing subcases) and explicit invalid-UTF-8 identity (`Ran 1 test`, one failure).
- Supplied raw current evidence: focused corrected tests, hook identity, Claude suite, full repository suite, syntax/validator/diff checks, exact Claude Code `2.1.251` version, and strict Plugin/Marketplace validation results described in the review request.
- No prior Ticket 2 Review Report was read or used.

## Assumptions

- The parent workflow proved top-level mode `full`; Ticket 2's approved implementation mode is `tdd`.
- This reviewer context did not implement Ticket 2 and received raw artifacts/results rather than implementer defenses or a proposed verdict, so `independent` is warranted.
- Exact Claude Code command identity, `additionalContext`, and runtime failure semantics remain provisional until the authenticated Ticket 3 host gate; native strict validation does not substitute for that session evidence.
- The review is scoped to Ticket 2 final state and relevant surrounding validation, not later profile implementations or release integration.

## Verification performed

- Personally ran the Claude discovery suite with the repository virtual environment and bundled Node: `Ran 88 tests in 72.059s; OK (skipped=1)`. The only skip was state-file symlink creation because this Windows account lacks symlink privilege; the directory-junction rejection test passed.
- Personally ran `tests.claude.test_public_plugin_contract`: `Ran 8 tests in 13.850s; OK`.
- Personally ran Node syntax validation for `router.mjs`: exit `0`.
- Personally ran the Claude Plugin validator and model-evidence validator: both exit `0`.
- Personally ran `git diff --check`: exit `0`, with only the supplied user-owned Knowledge Base LF-to-CRLF warning.
- Inspected the complete route table, lifecycle and generation transitions, lock/recovery and atomic-replacement paths, failure-envelope construction, exact mapping/trace linkage, public bootstrap envelope unions, schema mutation tests, cleanup, cross-session isolation, and symlink/junction guards.
- An initial focused invocation used the bundled Python without repository dependencies and stopped at import with missing `yaml`; the same affected public-plugin tests passed under the repository `.venv`, so this was an interpreter-selection issue rather than product evidence.

## Twelve architecture and refactoring lenses

1. **Duplicated Code or Policy** — `finding`. The minimum-version/manual-fallback policy spans the Specification, router failure enum, and explicit Skill prose; the drift identified in finding 2 shows that the valid-envelope branch lost the Claude Code proof required by the shared policy.
2. **Long Function** — `no-finding`. The longer parser, lock, and action handlers remain single-purpose, and no actionable defect was attributable to function length.
3. **Large Module or Class** — `no-finding`. `router.mjs` is large, but it is the deliberately dependency-free runtime boundary and separates parsing, mapping, locking, state validation, and hook handlers with narrow internal functions; this review found no safe extraction requirement.
4. **Long Parameter List** — `no-finding`. Public/internal functions use short parameter sets or explicit option objects; no unstable coordination interface was found.
5. **Data Clumps** — `no-finding`. State, pending transition, operation, lock, and envelope fields are represented and validated as coherent records rather than repeated loose argument groups.
6. **Primitive Obsession** — `finding`. Finding 1 arises because domain-specific canonical model identity is represented by the same unconstrained string guard used for generic identifiers.
7. **Feature Envy** — `not-applicable`. The reviewed code is procedural and has no module/class method whose behavior predominantly manipulates another object's responsibilities.
8. **Divergent Change** — `no-finding`. Although the router covers four hook actions, all changes are driven by the single session-routing/state contract and share the same ownership and failure boundary.
9. **Shotgun Surgery** — `no-finding`. Hook wiring, runtime behavior, and human-consumed bootstrap validation necessarily occupy separate artifacts, but the release-owned constants and validator tests constrain coordinated changes; no additional actionable multi-location edit pattern was demonstrated beyond finding 2's policy correction.
10. **Message Chains** — `not-applicable`. There are no deep caller navigation chains or chained object access interfaces in the changed runtime.
11. **Leaky Abstraction** — `no-finding`. Apart from the explicit, specified manual host-version check, Skills consume a bounded route envelope and do not need session, filesystem, lock, or mapping internals.
12. **Shallow Module** — `no-finding`. The small public hook/action interface hides substantial schema validation, ownership, synchronization, routing, and failure handling.

Each fixed lens has exactly one outcome; this is a change-focused review, not a system-wide architecture diagnosis.

## Acceptance and regression assessment

- The four synchronous argument-vector hooks, exact route outcomes, ready/pending/indeterminate lifecycle, generation exhaustion handling, operation binding, same-session resume/compact behavior, clear/fork isolation, PostModelSwitch notices, bounded exit-0 failure envelopes, state cleanup, locking, exact mapping integrity, and no-model-switch behavior are otherwise supported by code and passing tests.
- Acceptance criterion 10 and the canonical-or-null portion of criterion 9 are not satisfied because noncanonical model text is persisted.
- Acceptance criteria 6–7 are not satisfied for the explicit old-Claude-Code plus `node-too-old` branch.
- The provided Red/Green evidence is directionally valid for the third-correction targets, and both corrected regression groups pass in the current Claude suite; it does not cover the two findings above.

## Deferred checks and residual risks

- `deferred`: authenticated exact Claude Code `2.1.251` namespaced invocations, `additionalContext`, command identity, timeout/nonzero/exit-2 semantics, and model-switch race observations remain Ticket 3 work and are `unverified`, not failed.
- `deferred`: the full 304-test repository suite and exact native strict validations were accepted as supplied raw evidence rather than rerun in this reviewer context; the 88-test Claude suite was rerun personally.
- `deferred`: state-file symlink rejection remains unexecuted on this Windows account; static `lstat`/ancestor guards and the passing directory-junction test reduce but do not eliminate this platform-specific evidence gap.
- Residual risk: model-source fixtures are manually normalized transcripts. Current validation proves their hashes, row coverage, dates, URLs, and internal consistency, but not authenticated official-page bytes or reproducible normalization; retain this limitation in release evidence.
- Residual risk: Ticket 3 may invalidate provisional hook matcher/identity/failure assumptions and require reopening Ticket 2 and dependent evidence.

## Completion assessment and handoff

Ticket 2 does **not** appear complete against its Approved Specification while the two P2 findings remain. Handoff to the Ticket 2 TDD implementation stage: add failing behavioral/contract tests for both triggers, make the smallest in-scope corrections, rerun focused Claude and broader repository verification, then obtain another fresh independent Review. Do not advance dependent Tickets on an Accepted Ticket 2 claim until that Review has no blocking findings. No production code, tests, Specification, Plan, Knowledge Base, or prior evidence was modified by this review.
