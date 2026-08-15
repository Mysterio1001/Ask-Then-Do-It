# Ticket 6 Final Review Report

Artifact type: Review Report

Artifact ID: `lite-workflow-mode-1-3-ticket-6-review-final`

Workflow ID: `lite-workflow-mode`

Review workflow core version: `1.1.0`

Product Core version: `1.2.0`

Target release version: `1.3.0`

Ticket: `6 - Enforce the deterministic 60% token-proxy gate`

Approved implementation mode: `tdd`

Status: Changes requested

Review label: `independent`

Reviewed inputs: Approved Specification `docs/specs/lite-workflow-mode-1.3.0.md`; Approved Ticket Plan and Ticket 6 definition in `docs/plans/lite-workflow-mode-1.3.0.md`; final `scripts/measure_workflow_token_proxy.py`; `tests/release/test_workflow_token_proxy.py`; final Full/Lite benchmark fixture files; related `scripts/build_release.py` diff; Codex orchestrator and Lite workflow source; and the observed focused, CLI, mutation, and diff-check results recorded below. The prior Review and Implementation Evidence artifacts were not used as review evidence.

Assumptions: The current working tree is the revision under review. The benchmark fixture and its source files are intended to be canonical release inputs, and a Generic fixed-cost report must measure the canonical composed Generic prompt rather than an arbitrary repository-owned directory.

Deferred: Full release/conformance suite, package rebuild/checksum verification, external CI, and external publication were not rerun because they are outside this focused Ticket 6 review pass.

Handoff: Return the P2 finding to the Ticket 6 `implement-tdd` owner after explicit correction approval; rerun focused tests and the mutation matrix, then request a fresh independent Review.

## Findings

### [P2] Generic benchmark source can be redirected to fabricate the fixed-cost report

Trigger: Change `fixture.generic_composed_prompt.source` to any repository-owned directory containing the eleven expected module filenames, with otherwise valid module order. Impact: `measure_generic` accepts the alternate directory and composes a successful report from its filler files, so the reported Generic complete composed prompt can be made arbitrarily smaller or otherwise unrelated to the canonical Generic workflow. Reproduction returned exit code 0 and reduced the reported Generic proxy from 13,313 to 721; the Codex gate still passed because Generic is excluded from that gate, but the fixed-cost evidence is no longer trustworthy. Evidence and location: `scripts/measure_workflow_token_proxy.py:561-590` validates only a safe directory and filename inventory, then composes from that directory; `tests/release/test_workflow_token_proxy.py:410-427` hashes whatever fixture source is supplied and has no redirect-rejection case. Pin the Generic source to the canonical release/config source (or a fixed repository-owned constant) and add a negative mutation test for a same-filename alternate directory.

## Verification

- Focused test: `.\\.venv\\Scripts\\python.exe -m unittest tests.release.test_workflow_token_proxy -v` - 18 tests passed.
- CLI JSON and human output both passed. The representative Codex result was Full `13,768`, Lite `5,356`, difference `8,412`, reduction `61.09%`, with the integer gate at `>= 60.00%`.
- The algorithm is disclosed as `normalized-utf8-quarter-v1`, uses UTF-8 bytes with the same normalization and exclusions for both modes, and explicitly reports `billing_guarantee: false`.
- Lite output budgets were verified as questions `117 <= 500`, Change Brief `405 <= 800`, and completion `112 <= 500`; the fixture locks those budget labels to their intended events.
- An independent mutation matrix covered mode/order plus every Full and Lite event `id`, `category`, `source`, and `budget` field: 82/82 mutations were rejected with schema-error exit code 2.
- Boundary mutations for duplicate IDs, unsafe/missing/absolute/non-UTF-8 sources, threshold override, mode-specific exclusions, redirected event sources/categories, and replayed Full output were exercised and rejected.
- Signed reduction display was checked for negative, zero, and positive cases; the exact integer gate and 60% threshold remained unchanged.
- Generic output was checked to have `gate_applied: false`, apply equally to Full/Lite, include the actual builder composition and complete module inventory, and make no billing or Generic 60% claim.
- `git diff --check` reported no whitespace errors for tracked changed files; untracked Ticket 6 files were inspected and no whitespace error was observed. No external CI or complete release suite was run.

## Residual risks and unavailable evidence

The P2 Generic-source redirection remains unresolved and prevents an unqualified completion claim. The benchmark is deterministic for its current canonical Codex event paths and output sources, but broader release/package integration and historical-release preservation remain unverified in this focused pass. Generic hosts therefore have no valid 60% guarantee, as correctly disclosed; the remaining risk is that the separately reported fixed cost can be fixture-gamed until the source is pinned.

## Twelve architecture and refactoring lenses

1. Duplicated Code or Policy: `no-finding` - duplicated event contracts across the script, fixture, and tests are deliberate drift tripwires for this release gate; no conflicting policy was observed.
2. Long Function: `no-finding` - `measure_modes` and `measure_generic` are validation/reporting pipelines, but their responsibilities are coherent and covered by focused tests.
3. Large Module or Class: `no-finding` - the standalone standard-library script owns one measurement boundary; no unrelated ownership area was introduced.
4. Long Parameter List: `no-finding` - public helpers use small, domain-relevant parameter sets; no unstable coordination interface was added.
5. Data Clumps: `no-finding` - event tuples and benchmark metadata travel as explicit schema objects and are validated at the boundary.
6. Primitive Obsession: `no-finding` - JSON primitives are constrained by exact-key, type, category, budget, path, and arithmetic validation appropriate to a fixture boundary.
7. Feature Envy: `no-finding` - Generic composition delegates to the canonical `compose_generic_workflow` builder instead of reproducing its formatting policy.
8. Divergent Change: `no-finding` - the changed script and fixture tests evolve around one deterministic proxy contract rather than unrelated concerns.
9. Shotgun Surgery: `no-finding` - event inventory changes are intentionally localized to the fixed contract, fixture, and focused tests; no hidden cross-module edit pattern was found.
10. Message Chains: `no-finding` - path resolution and composition use short, bounded calls without exposing nested implementation navigation.
11. Leaky Abstraction: `finding` - Generic source ownership leaks through the fixture and lets callers select an arbitrary module directory; this is the P2 finding above.
12. Shallow Module: `no-finding` - the measurement script provides meaningful schema validation, normalization, arithmetic, and report behavior behind its CLI.

## Completion assessment

The Codex deterministic 60% gate, exact event contracts, 500/800/500 Lite budgets, signed percentage display, shared algorithm/scenario/exclusions, replay rejection, and Generic no-gate/no-billing disclosure meet the approved Ticket 6 behavior. The approved Ticket does not appear complete because the Generic fixed-cost evidence is not protected against canonical-source redirection. No source, test, fixture, plan, or implementation file was modified during this review.
