# Claude Code Adapter 1.4.0 — Ticket 2 Second-Correction Independent Review Report

Artifact type: `Review Report`

Artifact ID: `claude-code-adapter-1-4-0-ticket-2-review-after-second-corrections-independent`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Review label: `independent`

Status: `changes-requested`

Ticket mode: `tdd`

Reviewer capability: `multi_agent + tools`

Reviewed inputs: Approved `docs/requirements/claude-code-adapter-1.4.0.md`; Approved `docs/specs/claude-code-adapter-1.4.0.md`; Approved Ticket 2 in `docs/plans/claude-code-adapter-1.4.0.md`; complete current `adapters/claude-code/plugin/ask-then-do-it/{scripts/router.mjs,hooks/hooks.json,config/model-classifications.json,skills/*/SKILL.md}` review surface; `scripts/validate_claude_plugin.py`; `scripts/validate_claude_model_evidence.py`; `tests/claude/test_router_*.py`, `tests/claude/test_model_classification_evidence.py`, `tests/claude/test_public_plugin_contract.py` and relevant fixtures. The adapter is untracked and has no usable base diff, so the complete scoped artifacts were reviewed. Only after forming an independent source/test conclusion, the reviewer read `docs/evidence/claude-code-adapter-1.4.0-ticket-2-review-final.md`, the raw chronology in `docs/evidence/claude-code-adapter-1.4.0-ticket-2.md`, and Draft `docs/evidence/claude-code-adapter-1.4.0-ticket-2-architecture-diagnosis.md` for closure and architecture comparison.

Assumptions: top-level mode was already proven `full` because both operation/project/user Config sources are absent and Full fallback applies; there is no repository `AGENTS.md`; the Approved Ticket Plan fixes Ticket 2 to `tdd`; this fresh reviewer did not implement the change and did not read an implementer verdict before independently inspecting the raw artifacts. A narrow reviewer candidate received late in the pass was not adopted on authority: its control flow and raw-byte result were independently reproduced before inclusion. Exact authenticated Claude Code runtime behavior remains provisional under the Approved Ticket 2→3 sequencing exception.

Deferred: authenticated Claude Code `2.1.251` command identity, `command_source`, same-invocation `additionalContext`, required/optional hook-field inventory, Node missing/nonzero/exit-2/timeout behavior and host event ordering remain Ticket 3; profile modules, paired conformance, context proxy, docs, release integration and live smoke remain downstream Tickets. No production, test, Specification, Plan, Knowledge Base, implementation-evidence, prior-review or architecture-report change is authorized by this Review.

Next handoff: return both findings to the Full/TDD implementation stage. Add failing regressions first, make the smallest Ticket 2 corrections, rerun focused and complete validation, then request another fresh independent Review. Do not mark Ticket 2 Completed or use it as a frozen downstream dependency while these findings remain.

## Findings

### [P2] Generation exhaustion reports failure but leaves stale `ready` authority routable

Trigger: a schema-valid same-session state with `model_generation = Number.MAX_SAFE_INTEGER` receives either (a) `SessionStart(source=resume, model=claude-sonnet-5)` while the prior ready state records `claude-sonnet-4-6`, or (b) a no-Pre `PostModelSwitch(source=auto|resume, to_model=claude-sonnet-5)` from that prior state. `incrementGeneration` throws `transition-invalid` before either handler writes. The SessionStart catch emits nothing and the Post catch explicitly says “Stop both public entries until a new valid SessionStart state is established,” but both paths leave the old `ready` 4.6 state intact. A following automatic entry therefore succeeds with `supported-non-5/general` instead of failing closed or using the authoritative new model. Personal probes reproduced both outcomes. The same checked increment also makes a requested Pre emit its required non-blocking warning at this boundary, but Pre alone is not the blocking proof here because it must not prevent the switch and a later Post may repair it; the actionable violation is the stale ready route after failed Resume/automatic Post synchronization. Impact: a state transition that the router itself says is unsafe can still authorize a new operation under the previous model/profile, contradicting the `transition-invalid` failure boundary, resume semantics, Post synchronization warning and acceptance criteria 6, 8 and 9. The boundary is pathological but explicitly admitted by `validateState` and deliberately exercised by the new tests, so it cannot be dismissed as unreachable input. Remediation direction: under the existing session lock, make generation exhaustion on Resume/model-authority synchronization persist a safe non-ready/indeterminate state (while preserving any operation binding) or define another monotonic exhaustion transition that guarantees the next public entry fails until a valid reset; tests must assert the following entry's failure, not merely that no unsafe integer was written. Location: `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1199`, `:1224`–`:1228`, `:1393`–`:1398`, and catch translation at `:1491`–`:1510`; incomplete assertions at `tests/claude/test_router_state.py:331`–`:387`.

### [P3] Pre-parse failures for the explicit entry are mislabeled as the automatic entry

Trigger: invoke the explicit `ask-then-do-it:ask-then-do-it-5` expansion with stdin that fails before JSON has been returned, such as an otherwise valid payload whose `session_id` contains raw byte `0xFF`, malformed JSON, or truncated UTF-8. `main` initializes `entry` to the automatic entry, awaits fatal decode/strict parse in `readStdin`, and only afterward inspects `rawEvent.command_name`; the catch therefore emits a valid `invalid-hook-input` failure envelope whose `entry` is `/ask-then-do-it:ask-then-do-it`. The personal raw-byte probe reproduced this exact envelope. Impact: the explicit Skill safely stops because the envelope identity does not match, so this is not a profile-selection bypass; however, the handler-started failure is not a deterministic envelope for the entry whose hook actually ran, and the explicit bootstrap cannot consume the declared failure/disclosure as its own. The current invalid-UTF-8 regression covers SessionStart collision rejection, not either UserPromptExpansion identity. Remediation direction: provide the matcher-selected entry to the router as fixed trusted invocation metadata before stdin decoding (subject to Ticket 3's exact-host validation), or use separate fixed actions with the same property; add explicit-entry invalid UTF-8, malformed and truncated-input regressions. Do not recover identity by partially parsing untrusted invalid bytes. Location: `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs:1446`–`:1455` and `:1491`–`:1495`; missing coverage near `tests/claude/test_router_review_regressions.py:613`.

## Prior `3×P2 + 2×P3` closure audit

- Prior P2, last-attempt stale-lock ownership: `closed`. After stale recovery, current `withSessionLock` must successfully publish a new owner-token record before setting `ownerToken` and entering the callback; reacquisition loss fails closed. The last-attempt/contender, owner replacement, dead-lock recovery and concurrent-reclaimer tests passed.
- Prior P2, replacement-decoding collision for raw invalid UTF-8 session IDs: `closed for the exact cross-session collision`. Stdin now uses `TextDecoder(..., { fatal: true })` before parse/hash, and the `0xFF`/`0xFE` collision regression passed without a state write. The explicit-entry identity P3 above is a distinct failure-envelope defect exposed at the same pre-parse boundary.
- Prior P2, Node 18/19 API surface before the Node gate: `closed`. Portable UTF-16 well-formedness checking no longer calls the unavailable prototype API; the simulated Node 18/19 and Node 21 tests preserve explicit identity and return `node-too-old`.
- Prior P3, source-trace metadata/schema binding: `closed`. The validator now fixes the canonical mapping path, exact integer schema version, date, source inventory, URLs and per-source dates to the runtime mapping; all new drift mutations passed.
- Prior P3, unsafe `model_generation` increment: `partially closed`. Current code no longer writes `9007199254740992`, so the exact unsafe-integer corruption is closed. The correction does not satisfy its claimed fail-closed outcome: the old valid `ready` state remains authoritative and a next entry routes successfully, which is the P2 above.

## Verification performed

- Independently read the Approved requirements, full Approved Specification and Approved Ticket 2 before reading prior implementation/review conclusions; retained `tdd` mode.
- Read the complete current 1,520-line, 45,218-byte router (SHA-256 `0BCD51F3E6529BFEEC6D835CC18CF45B7C12C4B8706D3E13ACEE232791AC82AE`), hooks, exact mapping, both bootstraps, validators and scoped tests/fixtures.
- Ran `\.venv\Scripts\python.exe -m unittest discover -s tests/claude`: exit `0`; `Ran 87 tests in 61.230s`; `OK (skipped=1)`. The skip was Windows regular-file symlink privilege; the directory-junction test passed.
- Ran `\.venv\Scripts\python.exe -B -m unittest discover -s tests -p 'test_*.py'`: exit `0`; `Ran 303 tests in 89.438s`; `OK (skipped=1)`.
- Ran `node --check adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs`: exit `0`, no output.
- Ran the repository-venv Claude Plugin validator: exit `0`, `Claude Plugin validation passed`.
- Ran the model-classification evidence validator against the canonical mapping/trace: exit `0`, `Claude model classification evidence is valid.`
- Ran `git diff --check`: exit `0`; only the pre-existing `docs/project/knowledge-base.md` LF→CRLF warning was printed.
- Ran exact local `\.ticket3-preflight\claude-code-2.1.251\claude.exe --version`: exit `0`, `2.1.251 (Claude Code)`. Ran Plugin and repository Marketplace `plugin validate --strict`: each exit `0`, `Validation passed`, no warning. These are schema observations only, not authenticated command/session evidence.
- Generation Resume probe: after a valid maximum-generation 4.6 state, `resume` with model 5 returned exit `0` and empty stdout; persisted state remained `ready`, generation `9007199254740991`, model `claude-sonnet-4-6`, source `startup`; the next automatic envelope was `ready`, `supported-non-5`, `general`.
- Generation automatic-Post probe: synchronization output said to stop both entries, but persisted state remained the same old `ready` 4.6 state; the next automatic envelope was again `ready`, `supported-non-5`, `general`.
- Explicit invalid-UTF-8 probe: an explicit expansion whose session ID contained raw `0xFF` returned exit `0` and `invalid-hook-input`, but the envelope `entry` was `/ask-then-do-it:ask-then-do-it` rather than the explicit `-5` entry.
- An initial attempt with the bundled standalone Python was not counted because that environment lacked PyYAML and could not load `test_public_plugin_contract`; all reported Python results above use the repository's working `.venv`.

## Evidence unavailable / unverified

- No authenticated exact Claude Code `2.1.251` session has yet proved runtime `command_name`, `command_source`, same-invocation `additionalContext`, Node failure semantics, or ordering. Ticket 3 remains a hard gate; native strict validation does not prove these behaviors.
- Exact required/optional hook fields and any closed `permission_mode` values remain unverified. Current Approved artifacts do not establish that omitted `transcript_path`/`cwd`/`permission_mode` must be rejected or that an unknown bounded permission mode affects routing, so this review does not expand the freeze into a finding.
- `claude-mythos-5` appears in none of the four Approved dated local source snapshots. This review found no evidence that it belonged in the 2026-09-07 exact freeze and therefore records omission as `unverified`, not a defect. Later official evidence must reopen the mapping/evidence gate rather than silently extend it.
- The four source snapshots were not re-fetched or independently authenticated against the network. The review verified local consistency, bindings and mutation behavior, not the historical truth of remote pages.
- For `PostModelSwitch(source=auto|resume)`, current code intentionally trusts authoritative `to_model` without comparing `from_model`. An out-of-order pair could theoretically overwrite a newer ready model, but authenticated host evidence available to this review does not prove such delivery can occur. This remains a Ticket 3 ordering risk, not a finding.
- Windows regular-file symlink creation remained unavailable; directory-junction protection passed. macOS/Linux filesystem/link behavior was not live-tested.
- Profile module execution, disclosure rendering, same-session cross-profile precedence and profile equivalence are outside Ticket 2 and remain downstream evidence.

## Twelve Architecture and Refactoring Lenses

The Draft architecture snapshot predates the second corrections, but the router grew from 1,482 to 1,520 lines and none of the corrections changed its responsibility boundaries. Its A1–A5 concerns therefore still apply diagnostically. They remain Draft, do not authorize refactoring, and are not additional immediate Ticket 2 correction requests.

| # | Lens | Outcome | Evidence |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `no-finding` | Hook, mapping, disclosure and Skill policy is repeated across JS/JSON/Python/tests, but current values agree and the independent validators/mutation tests intentionally provide defense in depth. No current drift was found. |
| 2 | Long Function | `no-finding` | `parseJsonStrict`, `validateState` and `main` are substantial but each retains a coherent role; the two findings are boundary/state-postcondition defects, not evidence that one mixed function is presently unreviewable. |
| 3 | Large Module or Class | `finding` | Current `router.mjs:1` is 1,520 lines/45,218 bytes and owns parser, event schemas, mapping, filesystem/lock protocol, state machine, handlers and output. A local change triggers whole-module review and broad regression exposure. This confirms Draft A1; severity is non-blocking architecture P3, with no refactor authorized here. |
| 4 | Long Parameter List | `no-finding` | Handler, lock and envelope interfaces remain short; no defect arose from an unstable long parameter list. |
| 5 | Data Clumps | `finding` | `entry/classification/profile` still travel through tuple strings, persisted operation and parallel `successEnvelope` inputs at `router.mjs:148`–`:155`, `:1112`–`:1137`. Adding a route can diverge projections. This confirms Draft A4, a non-blocking architecture P3. |
| 6 | Primitive Obsession | `finding` | Route/status/error/generation concepts remain unconstrained strings/numbers spread across sets and helpers. The maximum-safe integer being schema-valid but lacking a safe exhausted-state transition is the concrete P2 trigger above (`router.mjs:962`–`:1045`, `:1199`–`:1203`). Draft A4's wider maintainability concern also remains. |
| 7 | Feature Envy | `not-applicable` | This is a functional/procedural runtime, not an object model whose methods primarily manipulate another object's internals. |
| 8 | Divergent Change | `finding` | Host schema, model freeze, JSON parsing, filesystem safety, lock recovery, lifecycle and envelope behavior independently modify one file; the second corrections added code without separating these change reasons. This confirms Draft A1, non-blocking architecture P3. |
| 9 | Shotgun Surgery | `finding` | A hook/mapping/envelope change still requires coordinated edits across JSON, JS, Python validators, Skills, fixtures and tests. Current values agree, so this is Draft A3's maintainability risk rather than a current behavior defect. |
| 10 | Message Chains | `not-applicable` | Callers use direct functions/plain records; no long navigation chain exposes nested implementation structure. |
| 11 | Leaky Abstraction | `finding` | Host timeout policy remains in `hooks.json` while lock wait/reclaim choices remain in router call sites; validator/tests also depend on source-text/helper structure. The explicit pre-parse finding further shows that matcher-known entry identity is not represented at the router boundary. Draft A2/A5 remain applicable; no refactor is authorized here. |
| 12 | Shallow Module | `no-finding` | The four CLI actions hide substantive routing, security, concurrency and state behavior; the interface is materially simpler than its implementation. |

## Residual risk

- Green tests do not cover the post-failure next-entry behavior at generation exhaustion; the existing boundary tests prove only that an unsafe integer is not written.
- Green fatal-UTF-8 coverage does not invoke either UserPromptExpansion matcher and therefore cannot detect failure-envelope entry drift.
- Ticket 3 may still invalidate provisional hook field, matcher, visibility or timing assumptions; exact binary schema validation alone is insufficient.
- The Draft architecture risks increase review cost around further Ticket 2 corrections. They should remain diagnostic until a separate approved Specification/Plan authorizes architectural work.
- The same-user filesystem can still change between link/path checks and file operations; current tests establish fail-closed behavior for stable symlink/junction fixtures, not a formal adversarial TOCTOU proof.

## Completion assessment

Ticket 2 is **not complete**. The three prior P2s and the source-metadata P3 are closed, while the previous generation P3 is only partially closed: unsafe integer persistence is gone, but the transition now fails open by retaining stale `ready` routing authority. The separate explicit pre-parse identity P3 also remains. Because the Approved mode is `tdd`, both corrections require new Red evidence before implementation and another fresh independent Review afterward.
