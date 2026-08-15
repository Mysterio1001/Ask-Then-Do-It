# Lite Workflow Mode 1.3.0 Ticket 2 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `lite-workflow-mode-1-3-ticket-2-evidence`

Workflow ID: `lite-workflow-mode`

Core version: `1.2.0`

Target release version: `1.3.0`

Status: Completed

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), Ticket 2 in approved `tdd` mode, and completed [Ticket 1 evidence](lite-workflow-mode-1.3.0-ticket-1.md) with its accepted Review.

Assumptions: The Codex adapter implements behavior through declarative Skill instructions rather than an executable Config parser. A present invalid project Config therefore fails closed through explicit orchestration policy. Ticket 1's uncommitted Core changes are the approved dependency used by conformance validation.

Deferred: Independent Review; Generic behavior; localized user documentation; token-proxy measurement; version and package integration; generated `dist/`; external publication, installation, and Config mutation.

Handoff: `$review-code` with the approved artifacts, Ticket 2 final diff, surrounding orchestrator and Core Lite contracts, focused test, and raw results below. The reviewer must not rely on this implementer conclusion.

## Outcome

- Added deterministic, read-only Codex mode resolution for explicit current-operation instruction, project Config, user Config, and Full fallback.
- Distinguished absent project Config from present invalid project Config; present invalid, unreadable, malformed, missing-mode, or unsupported Config fails closed to Full, while a valid explicit instruction wins without reading Config.
- Kept the existing Full route and Ticket-level `tdd`/`direct` choices separate from top-level Lite.
- Added one directly linked Lite reference covering risk reconsideration, bounded questions, one approved conversation-only Change Brief, scoped implementation without new tests or TDD claims, proportionate validation, compact same-agent Review with correction approval, and non-durable completion behavior.
- Added truthful Codex conformance and implementation mappings for all eight mandatory Full/Lite Core rules.

## Files changed

- `adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md`
- `adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/references/lite-workflow.md`
- `adapters/codex/conformance.yaml`
- `adapters/codex/rule-mapping.yaml`
- `tests/codex/test_lite_workflow.py`
- `docs/evidence/lite-workflow-mode-1.3.0-ticket-2.md`

No top-level Skill, Plugin manifest, release manifest, generated output, user Config, localized guide, version declaration, or Ticket Plan was changed by Ticket 2.

## TDD evidence

### Valid Red

The focused public-boundary test was added before any Ticket 2 production file changed.

Command:

```text
.venv\Scripts\python.exe -m unittest tests.codex.test_lite_workflow.CodexLiteWorkflowTests.test_orchestrator_links_one_level_lite_reference_without_new_skill
```

Observed result:

```text
F
======================================================================
FAIL: test_orchestrator_links_one_level_lite_reference_without_new_skill (tests.codex.test_lite_workflow.CodexLiteWorkflowTests.test_orchestrator_links_one_level_lite_reference_without_new_skill)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\Ian\Desktop\Grill Me\tests\codex\test_lite_workflow.py", line 77, in test_orchestrator_links_one_level_lite_reference_without_new_skill
    self.assertTrue(
AssertionError: False is not true : the existing orchestrator Skill must own a one-level Lite reference

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

The failure was the approved missing behavior: the existing orchestrator had no directly linked `references/lite-workflow.md`. It was not a setup, import, or unrelated failure.

### First Green attempt

Command:

```text
.venv\Scripts\python.exe -m unittest tests.codex.test_lite_workflow
```

Observed result:

```text
....F.
FAIL: test_mode_resolver_is_read_only_fail_closed_and_deterministic
AssertionError: 'do not repair' not found in '<resolver section>'
Ran 6 tests in 0.010s
FAILED (failures=1)
```

The implementation already prohibited repair inside a combined sentence. The production instruction was made explicit as `Do not repair or normalize invalid Config`; no assertion or acceptance criterion was weakened.

### Focused Green

Command:

```text
.venv\Scripts\python.exe -m unittest tests.codex.test_lite_workflow
```

Observed result:

```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.010s

OK
```

### Post-refactor verification

One grammar-only refactor added the missing subject to the workflow-artifact prohibition. The final focused rerun observed:

```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.013s

OK
```

No test-first exception was used.

## Broader verification

### All Codex tests

Command:

```text
.venv\Scripts\python.exe -m unittest discover -s tests/codex -p "test_*.py"
```

Final observed result:

```text
.......................
----------------------------------------------------------------------
Ran 23 tests in 0.551s

OK
```

### Codex conformance

Command:

```text
.venv\Scripts\python.exe scripts\validate_conformance.py --catalog core\rules\rules.yaml --manifest adapters\codex\conformance.yaml
```

Observed result:

```text
Conformance passed: codex against core 1.2.0
```

### Existing orchestrator Skill validation

Command:

```text
.venv\Scripts\python.exe "C:\Users\Ian\.codex\skills\.system\skill-creator\scripts\quick_validate.py" adapters\codex\plugin\ask-then-do-it\skills\ask-then-do-it
```

Observed result:

```text
Skill is valid!
```

### Diff and whitespace checks

The scoped tracked-file command completed with exit code `0` and only Git's LF-to-CRLF checkout warnings:

```text
git diff --check -- adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md adapters/codex/conformance.yaml adapters/codex/rule-mapping.yaml
```

An explicit trailing-whitespace scan covering the two untracked additions and all tracked Ticket 2 files reported:

```text
No trailing whitespace in Ticket 2 files.
```

`git status --short` and the scoped diff were inspected. They showed only the six files listed above for Ticket 2; unrelated Core, Generic, documentation, release-script, and conformance-fixture changes were preserved.

The repository-wide `git diff --check` was also run and returned exit code `1` only for concurrent, out-of-scope guide edits:

```text
docs/guides/getting-started-simple.en.md:94: new blank line at EOF.
docs/guides/getting-started-simple.ja.md:94: new blank line at EOF.
docs/guides/getting-started-simple.zh-TW.md:94: new blank line at EOF.
```

Ticket 2 did not edit or repair those parallel-owned files.

## Residual risks and incomplete checks

- The Codex runtime contract is declarative. Focused tests prove required instructions, routing outcomes, direct reference structure, and mappings are present, but cannot guarantee perfect model adherence in every future conversation or exact approximate token counts.
- No real user or project Config was read or written during tests. This avoids mutating user state; runtime permission failures are covered by the fail-closed unreadable-Config instruction rather than an external filesystem test.
- Package inventory, isolated packaged Skill validation, generated archives, checksums, and the `1.3.0` version transition belong to Ticket 7.
- Repository-wide whitespace validation is not currently clean because of the three concurrent guide EOF findings above. Ticket 2's scoped files are clean and its required automated checks pass.
- Independent `$review-code` remains required before Ticket 2 can be accepted by the parent workflow.
