# Claude profile correction integration — 2026-09-09

Artifact type: Integration Evidence

Artifact ID: `claude-code-adapter-1-4-0-profile-correction-integration`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0` (workflow evidence contract; product authoring baseline `1.3.1`)

Status: Corrections accepted; final local regression verified. Tickets 4/5 remain incomplete pending mandatory model-behavior evidence.

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md), [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Tickets 4/5 with `tdd`, [General evidence](claude-code-adapter-1.4.0-ticket-4.md), [Claude 5 third-correction evidence](claude-code-adapter-1.4.0-ticket-5-third-correction.md), and the user's approval of the four latest findings.

Assumptions: The current-operation resolver observed absent project/user Config and selected Full fallback; tools and isolated reviewers establish `multi_agent`. Frozen prompt equality protects reviewed text, not arbitrary language semantics or actual model compliance. The two profiles retain ten internal modules each and two public namespaced entries.

Deferred: Actual Claude execution of the mandatory scenario outcomes; authenticated Ticket 3 host ledger; Ticket 6 paired/authority evidence; context reduction, release integration and live smoke. These checks do not authorize login, publication or Marketplace mutation and do not complete Tickets 4/5.

Handoff: Both independent correction Reviews are accepted with no unresolved actionable finding. Preserve correction acceptance separately from Ticket completion. Obtain the outstanding model-behavior evidence before claiming the full behavior gates passed.

## Approved corrections

- General's complete-source fixed reference now rejects additions that preserve every old phrase and table while reversing policy. Focused Red: two tests, 34 expected false-pass failures; focused Green: 13 tests. No General production policy changed for this test-gate repair.
- Claude 5 now has complete-source integrity checks, exact Core/module ownership, thirty static reference scenarios and separately evaluated closed decision tables. Its Red reproduced seven unsafe test false-passes and two missing lifecycle/architecture guards; Green: ten tests. Explicit remove requests receive fresh complete pre-write state verification. Direct architecture diagnosis precedes unrelated delivery-artifact gates while retaining diagnostic safety.
- The final independent review exposed a related direct-diagnosis dependency: both architecture modules referred to twelve lenses defined only in the unloaded Review module. The coordinator corrected this within the direct-architecture scope, as recorded below.

## Direct architecture lens dependency: Red / Green

Before adding the canonical list, ran:

```powershell
& '.venv/Scripts/python.exe' -B -m unittest tests.claude.test_general_profile.ClaudeGeneralProfileTests.test_direct_architecture_defines_the_canonical_lenses_without_review tests.claude.test_claude5_profile.Claude5ProfileTests.test_direct_architecture_defines_the_canonical_lenses_without_review
```

Observed exit `1`:

```text
Ran 2 tests in 0.001s
FAILED (failures=2)
```

Both failures reported `Direct diagnosis must not depend on unloaded review.md`. Each test reads only the architecture module and compares the explicit lens names/order to the existing independent public-contract canonical list.

Added one sentence containing the twelve ordered names to each architecture module. Updated only that module in each fixed source reference, with an assertion that removing the new sentence exactly restores the previous reference. All other reference contents were preserved. Both existing independent reviewers were asked to recheck these final bytes.

```powershell
& '.venv/Scripts/python.exe' -B -m unittest tests.claude.test_general_profile tests.claude.test_claude5_profile
```

Observed exit `0`:

```text
Ran 25 tests in 0.290s
OK
```

## Integration checks

Before the lens addition, full repository regression reported `Ran 347 tests in 94.377s; OK (skipped=1)`. That run is historical. After the two lens tests and final source additions, ran:

```powershell
& '.venv/Scripts/python.exe' -B -m unittest discover -s tests -p 'test_*.py'
```

Observed exit `0`:

```text
Ran 349 tests in 95.064s

OK (skipped=1)
```

The skipped case is `ClaudeRouterSecurityTests.test_state_file_symlink_is_not_followed`. A focused verbose rerun confirmed `symlink creation unavailable on this host: [WinError 1314]`; it reported `Ran 1 test in 0.092s; OK (skipped=1)`. This Windows host lacks the required symlink-creation privilege. The skip is unavailable evidence, not a passed symlink-security observation. No privileges or host settings were changed.

The canonical Plugin validator, model-classification evidence validator and `node --check` each exited `0`. `git diff --check` exited `0` with only the pre-existing Knowledge Base LF/CRLF warning; since much of this worktree is untracked, a separate check also inspected all 29 current profile/test/fixture files and found no trailing whitespace.

Exact native validation after the final source changes:

```text
--version exit 0
2.1.251 (Claude Code)
plugin validate adapters/claude-code/plugin/ask-then-do-it --strict exit 0
Validation passed
plugin validate . --strict exit 0
Validation passed
```

Commands ran against the pre-existing exact binary with an isolated temporary `CLAUDE_CONFIG_DIR`, automatic updates/nonessential traffic/telemetry disabled, and no login or installation. The temporary path was checked to be inside `.ticket3-preflight` and removed afterward. These are native schema observations, not authenticated model behavior.

The user's pre-existing `docs/project/knowledge-base.md` SHA-256 remains `D64B538EE04C65FC829891A37F5BB1FD7D6A00E44A18B406E1CDE8A7B130A062`; no Knowledge Base content was edited.

## Independent correction closure

- [General final independent Review](claude-code-adapter-1.4.0-ticket-4-review-after-third-correction.md): correction accepted, no unresolved actionable finding; reviewer independently passed 14 focused tests, rejected four lens mutations, and confirmed the exact baseline change and unchanged other nine modules. Its earlier independent probe rejected 72 text/inventory mutations.
- [Claude 5 final independent Review](claude-code-adapter-1.4.0-ticket-5-review-after-third-correction.md): correction accepted, no unresolved actionable finding; reviewer independently passed 11 focused tests, verified the canonical lens order, and rejected the missing-lens mutation. Its earlier independent probes rejected five source mutations and detected four table-decision inversions.

Both reviewers explicitly reproduced the limitation that a source and reference changed to the same bad instruction can agree. They inspected the actual final instructions and accepted this bounded correction while preserving the missing model-behavior gates. Neither Review nor the 349-test regression establishes actual Claude execution of the thirty scenarios, paired equivalence, context reduction, or release readiness. Tickets 4/5 remain incomplete; the user's earlier decision to skip authenticated testing remains in effect.
