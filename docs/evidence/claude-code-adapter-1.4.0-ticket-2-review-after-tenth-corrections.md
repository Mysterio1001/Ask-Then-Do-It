# Claude Code Adapter 1.4.0 Ticket 2 Review after tenth corrections

> 歷史紀錄：以下結論及測試數是原審查當時的觀察。本次文件整理只更新導航；原始 inputs／Ticket 檔名與核准證據可從[清理快照](release-history.md#archive)找回。新連結指向現行摘要，不代表 reviewer 當時審閱過新文件；目前進度見[狀態](../project/status.md)。

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-2-review-after-tenth-corrections`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Status: Accepted - no actionable findings

Review label: `independent`

Ticket mode preserved: `tdd`

Inputs: Approved `docs/specs/claude-code-adapter-1.4.0.md`; Approved Ticket 2 in `docs/plans/claude-code-adapter-1.4.0.md`; current final Ticket 2 production files, validators, model-source fixtures, related `tests/claude/` tests, surrounding code, and raw verification output.

Assumptions: The current workspace bytes are the review target. Exact Claude Code `2.1.251` strict manifest validation proves only the exercised static host boundary; it does not substitute for an authenticated live routing session. No applicable repository `AGENTS.md` was found.

Deferred: Authenticated namespaced invocation, live `UserPromptExpansion.additionalContext`, exact handler failure semantics, the first clean end-to-end smoke, and exhaustive adversarial filesystem race testing remain outside this Ticket 2 review.

Handoff: Ticket 2 may proceed to its workflow completion handoff. Ticket 3 and later integration/release gates must retain the live-host and smoke requirements; reopen Ticket 2 if those observations contradict the provisional command or hook assumptions.

## Findings

No actionable P0-P3 findings.

The reviewed router gates Node `22+` before stdin or state access, writes PostModelSwitch failure state only through the canonical locked session JSON, validates exact state and envelope unions, and keeps both bootstraps fail closed. No surrounding guard was found to be bypassed by a deterministic reviewed input or sequence.

## Verification and evidence unavailable

Independently performed on the reviewed bytes:

- Claude suite: `106` tests in `69.395s`, `OK` (`skipped=1`; Windows symlink creation privilege unavailable).
- Full repository suite: `322` tests in `81.024s`, `OK` (`skipped=1`).
- `node --check adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs`: exit `0`.
- Claude Plugin validator: exit `0`.
- Model evidence validator: exit `0`.
- `git diff --check`: exit `0`; only the existing Knowledge Base LF-to-CRLF warning was emitted.
- Isolated Claude Code binary: `2.1.251 (Claude Code)`.
- Exact Claude Code `2.1.251` Plugin and Marketplace `plugin validate --strict`: both exit `0`, no warnings.
- Router identity independently matched `1603` lines, `48572` bytes, SHA-256 `d0383da5c7581c7d643ab68789cbfac907655cba95540ad56a85c378af8baa32`.

Evidence unavailable in this review: authenticated invocation of both namespaced entries, a live observation of injected `additionalContext`, live Node-missing/nonzero/exit-2/timeout behavior, macOS/Linux filesystem execution, and execution of the skipped Windows symlink case on a privilege-enabled host.

## Residual risks and untested areas

- `assertNoLinkedAncestors` plus later file operations fail closed for the tested symlink/junction cases, but an adversary able to mutate directory reparse points concurrently may create a narrow check/use race. No deterministic trigger was established here; platform-specific handle-relative or no-follow guarantees were not verified.
- Model-source snapshots are dated, normalized transcriptions. Their byte hashes, trace relationships, exact-ID inventory, and classification policy validate, but this review did not independently recrawl the remote source pages.
- Router/host identity and failure semantics remain provisional until Ticket 3's authenticated live ledger confirms them.

## Ticket completion assessment

Ticket 2 appears complete against its Approved `tdd` plan and deterministic acceptance scope: route/state/security behaviors are present, relevant tests and validators pass, and no blocking or actionable finding remains. This assessment does not complete Ticket 3 or the local `1.4.0` release hard gates.

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — `no-finding`.** Envelope tuples, disclosure enums, mapping identity, and bootstrap rules are intentionally mirrored across runtime, public boundary, validator, and tests; exact checks detect drift, and no contradictory duplicate was found.
2. **Long Function — `no-finding`.** The longest routines retain one bounded responsibility (strict JSON parsing, state validation, locking, or dispatch), with lifecycle and route behavior split into named handlers.
3. **Large Module or Class — `no-finding`.** `router.mjs` is large at 1603 lines, but it is the zero-dependency, single-file runtime boundary and exposes cohesive internal seams for input, mapping, state, locking, routing, and hook output; no concrete change defect resulted from its size.
4. **Long Parameter List — `no-finding`.** The largest relevant interfaces use five cohesive values or an options object; no unstable positional coordination or call-site error was found.
5. **Data Clumps — `no-finding`.** State, operation, pending-switch, mapping, envelope, and lock records have explicit schemas and validation rather than recurring unrelated primitive bundles.
6. **Primitive Obsession — `no-finding`.** Model IDs, session keys, operation IDs, timestamps, sources, statuses, classifications, and disclosure codes are constrained by exact sets, regexes, schemas, and cross-field invariants.
7. **Feature Envy — `no-finding`.** Hook handlers operate on router-owned mapping/state abstractions; no function chiefly manipulates another module's private representation.
8. **Divergent Change — `no-finding`.** The module's reasons to change remain within the approved router/state/host contract, while model evidence and public validation are separately owned.
9. **Shotgun Surgery — `no-finding`.** Cross-boundary edits are deliberate contract synchronization and are guarded by exact validators/tests; no ordinary router behavior requires unrelated module changes.
10. **Message Chains — `no-finding`.** Path and JSON navigation are shallow and validated at boundaries; no fragile multi-object call or property chain was found.
11. **Leaky Abstraction — `no-finding`.** Public Skills consume only the bounded route envelope, while raw session/event/path details remain inside the router and are excluded from model-visible output.
12. **Shallow Module — `no-finding`.** The small hook and Skill interfaces hide classification, lifecycle, locking, atomic replacement, ownership validation, recovery, and fail-closed routing behavior, providing substantial abstraction depth.
