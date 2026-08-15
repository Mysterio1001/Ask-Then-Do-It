# Lite Workflow Mode 1.3.0 Ticket 6 Closure Review Report

Artifact type: Review Report

Artifact ID: `lite-workflow-mode-1-3-ticket-6-review-closure`

Workflow ID: `lite-workflow-mode`

Review core version: `1.1.0`

Product core version: `1.2.0`

Implementation mode: `tdd`

Status: Complete

Review label: `independent`

Inputs: Approved `lite-workflow-mode-1-3-spec`; Approved Ticket Plan Ticket 6; final `scripts/measure_workflow_token_proxy.py`; focused `tests/release/test_workflow_token_proxy.py`; complete structured benchmark and Full/Lite fixture sources under `tests/release/fixtures/workflow-token-proxy/`; actual Generic composer in `scripts/build_release.py`; final relevant worktree status and diff; independently observed command results listed below.

Assumptions: The worktree contains concurrent changes from other approved Tickets. Ticket 6 ownership is limited to the measurement script, structured benchmark fixtures, focused release tests, and its consumption of the settled Generic composer and adapter sources. New Ticket 6 files are untracked, so their complete contents were inspected directly in addition to status and tracked-diff inspection.

Deferred: Historical Red/Green execution order was not replayed because this review was explicitly isolated from implementation evidence. External CI, package integration, release inventory, generated distributions, checksums, and final release evidence belong to Tickets 7 and 8.

Handoff: Close Ticket 6 and provide its passing deterministic benchmark as input to Ticket 7 integration and Ticket 8 release evidence.

## Findings

No actionable findings.

The fixed Codex benchmark, failure behavior, Generic fixed-cost disclosure, exact canonical source constraint, arithmetic, budgets, exclusions, and report semantics satisfy Ticket 6 and Specification acceptance criterion 18. No blocking correctness, security, compatibility, test-strength, or architecture concern was found in the reviewed scope.

## Contract Assessment

- The benchmark uses one fixed English, tools-capable Codex scenario with one Ticket, no Review finding, and no architecture diagnosis. Full and Lite share the same task facts and the same normalization/counting function.
- `normalized-utf8-quarter-v1` performs NFC normalization, collapses Unicode whitespace, joins ordered events with one LF, and counts `ceil(UTF-8 bytes / 4)` for both modes (`scripts/measure_workflow_token_proxy.py:310-324`).
- All 20 events are pinned by ordered `(id, category, source, budget)` contracts (`scripts/measure_workflow_token_proxy.py:82-206`, `443-513`). An independent 82-case mutation pass changed every field of every event and changed each mode's order; all 82 variants exited with code 2.
- Lite budgets are bound to `lite-questions`, `lite-change-brief`, and `lite-completion`, not merely to compatible categories. Observed proxies were 117/500, 405/800, and 112/500.
- The fixed result is Full `13768`, Lite `5356`, difference `8412`, reduction `61.09%`. The gate uses the exact integer condition `lite * 100 <= full * 40`; 60.00% passed and 59.99% failed in independent boundary checks (`scripts/measure_workflow_token_proxy.py:637-691`).
- Signed percentages preserve negative values, including `-0.01`, rather than displaying an unsigned magnitude (`tests/release/test_workflow_token_proxy.py:304`).
- The three exclusions are shared top-level fixture policy, exact-key validation rejects mode-specific exclusions, and changing excluded task text leaves both mode counts unchanged.
- Generic source must equal the exact canonical directory `adapters/generic-prompts`; a complete filler redirect was rejected with exit code 2 before composition (`scripts/measure_workflow_token_proxy.py:559-570`).
- Generic uses the actual `compose_generic_workflow` implementation (`scripts/build_release.py:570`) and the fixed final module order. The reported raw composition SHA-256 `90431d413c2909e4ed90909349ea4307570ab3d10abfbd329bf084a886f9fefa` independently matched the composer output.
- Generic reports `13313` proxy tokens as a fixed cost applying equally to Full and Lite, applies no Generic reduction gate, and explicitly claims neither a Generic 60% guarantee nor a billing guarantee.
- The fixture fingerprint covers raw fixture bytes, every event ID/path/source byte stream, and actual composed Generic bytes (`scripts/measure_workflow_token_proxy.py:619-634`).

## Verification

- `.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy -v`: 19 tests passed.
- Independent event-contract mutation harness: 82 mutations executed; 82 returned exit code 2; zero escaped.
- Independent Generic alternate-directory filler fixture: exit code 2 with `fixture.generic_composed_prompt.source must equal adapters/generic-prompts`.
- `.venv\Scripts\python.exe scripts\measure_workflow_token_proxy.py --json`: exit code 0 with deterministic counts, `61.09%`, fixture SHA-256 `a33269fee015b43f0b47a64b7c3a45d172def664c202a79f48ab5a1572dca415`, and no billing guarantee.
- `.venv\Scripts\python.exe scripts\measure_workflow_token_proxy.py`: exit code 0; the human report disclosed algorithm, fixture, counts, difference, percentage, passed Codex gate, Generic fixed cost, and limitation.
- Independent integer boundaries: Full/Lite `10000/4000` passed at `60.00%`; `10000/4001` failed at `59.99%`; small-integer `3/1` passed and `3/2` failed.
- Independent composer comparison: reported Generic SHA-256 equaled SHA-256 of the bytes returned by `compose_generic_workflow` over the canonical source and fixed module inventory.
- `.venv\Scripts\python.exe -m py_compile scripts\measure_workflow_token_proxy.py tests\release\test_workflow_token_proxy.py scripts\build_release.py`: passed.
- Adjacent Generic and release regression selection: 28 tests passed across `tests.generic.test_generic_prompts`, `tests.release.test_generic_release`, and `tests.release.test_release_contract`.
- `git diff --check`: no whitespace error; only existing LF-to-CRLF worktree warnings were reported.
- Final status, tracked diff, all untracked Ticket 6 files, selected canonical Skill sources, all fixture files, and the Generic composer were inspected for scope and semantic alignment.

Evidence unavailable: external CI and the historical TDD Red/Green chronology were not independently observed. The focused tests clearly exercise the introduced public CLI and mutation boundaries, but this review does not replace the separately retained implementation chronology.

## Twelve Architecture And Refactoring Lenses

1. **Duplicated Code or Policy** - `no-finding`. Event and module contracts are deliberately pinned in executable constants, fixture data, and focused expectations so a benchmark edit cannot silently redefine its own oracle; the duplication serves the approved tamper-resistance boundary.
2. **Long Function** - `no-finding`. `measure_modes` is the largest flow but remains a linear schema-validation, contract-validation, measurement, and report-construction path with focused helpers around parsing, paths, normalization, Generic composition, and reporting.
3. **Large Module or Class** - `no-finding`. The standard-library script owns one cohesive benchmark CLI; the focused test module owns only that CLI's contract and mutations.
4. **Long Parameter List** - `no-finding`. Public and internal functions accept at most the fixture/configuration values required for their single operation; no unstable coordination interface was introduced.
5. **Data Clumps** - `no-finding`. Event ID, category, source, and budget form the explicit event schema and are validated as one contract rather than repeatedly travelling as unrelated loose arguments.
6. **Primitive Obsession** - `no-finding`. String categories, paths, modes, budgets, and exclusion kinds are constrained by exact-key checks, fixed inventories, safe path resolution, and domain-specific validators at the trust boundary.
7. **Feature Envy** - `no-finding`. Generic measurement delegates composition to the owning release builder instead of reproducing its header/module semantics; the dependency is the intended canonical boundary.
8. **Divergent Change** - `no-finding`. The measurement script has one reason to change: the disclosed deterministic benchmark contract or its report schema.
9. **Shotgun Surgery** - `no-finding`. Updating a fixed benchmark intentionally requires coordinated source, fixture, and independent expectation changes; this is a stability control, not accidental cross-module behavior spread.
10. **Message Chains** - `no-finding`. Data navigation is shallow fixture/config access inside validation boundaries, with no caller-visible chain through internal objects.
11. **Leaky Abstraction** - `no-finding`. CLI callers supply only an optional repository-owned fixture and choose JSON or human output; normalization, path safety, composer use, fingerprinting, and integer gating remain internal.
12. **Shallow Module** - `no-finding`. The CLI hides substantial validation, deterministic normalization, exact event enforcement, secure source resolution, Generic composition, hashing, budget checks, arithmetic, and stable reporting behind a small command surface.

## Security And Failure Paths

Fixture and event paths must resolve to repository-owned files, reject traversal and absolute paths, and decode as UTF-8. Exact object keys prevent fixture-controlled threshold changes, mode-specific exclusions, hidden event fields, and alternate Generic roots. Invalid fixtures return exit code 2; a valid benchmark below the gate returns exit code 1; a passing benchmark returns exit code 0. The script performs local reads and deterministic computation only, exposes no secret, executes no fixture content, performs no network or billing operation, and makes no destructive change.

## Residual Risk And Completion

The byte-quarter proxy is intentionally not a tokenizer, API bill, total-context, cache, tool-output, source-code, or hidden-reasoning measurement. Its conclusion is limited to the fixed representative English Codex operation and the disclosed workflow-controlled material. Generic receives only a separately disclosed fixed-cost measurement and no reduction claim. Future legitimate workflow inventory changes must update the deliberately fixed contract and expected counts together, which will require explicit benchmark review.

No known approved branch is untested, no required local check failed, and no actionable finding remains. Ticket 6 appears complete against the Approved Specification and Ticket Plan, subject only to the explicitly deferred release integration/evidence checks and unavailable historical TDD chronology.
