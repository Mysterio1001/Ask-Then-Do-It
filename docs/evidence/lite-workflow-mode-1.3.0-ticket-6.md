# Lite Workflow Mode 1.3.0 Ticket 6 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `lite-workflow-mode-1-3-ticket-6-evidence`

Workflow ID: `lite-workflow-mode`

Core version: `1.2.0`

Target release version: `1.3.0`

Status: Completed

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), completed Tickets 1-3 and their accepted Reviews, and Ticket 6 in approved `tdd` mode.

Assumptions: The representative benchmark is an English, tools-capable Codex operation. It deliberately uses one low-risk Ticket, two shared product decisions, no Review correction, and no architecture diagnosis. Raw task-specific source code, necessary tool output, and hidden model reasoning are shared exclusions rather than mode-specific adjustments.

Deferred: Adding `workflow-token-proxy` to `release/release.json`, changing the final Generic runtime inventory and versions, rebuilding `dist/`, creating the `1.3.0` release ledger, and evidence-gate integration belong to Tickets 7 and 8. No external publication or installation was performed.

Handoff: A fresh independent `$review-code` context with the Approved Specification and Ticket, the initial and final Review findings, the corrected Ticket 6 script/test/fixture diff, this evidence, the raw results below, and the disclosed unrelated broader-suite failures. No post-final-fix Review was performed during implementation.

## Outcome

- Added the standard-library `normalized-utf8-quarter-v1` measurement CLI.
- Added one strict, human-readable Full/Lite fixture with identical task facts, decisions, risks, and delivered outcome.
- Counted selected Skill instructions, questions, Full documents or Lite Change Brief, handoffs, implementation/validation records, Review, and completion output.
- Applied Unicode NFC normalization, whitespace-run collapse, ordered LF joining, and `ceil(UTF-8 bytes / 4)` to both modes.
- Fixed the release threshold at `6000` basis points and evaluated it through integer cross multiplication: `lite * 100 <= full * 40`.
- Bound every event to its exact mode, ordered ID, category, canonical source path, and budget; redirected or replayed Full/Lite sources now fail before they can affect the gate.
- Pinned the Generic composed-prompt source to the exact canonical `adapters/generic-prompts` directory before path resolution or composition.
- Rejected unknown schema fields, configurable thresholds, mode-specific exclusions, missing/traversing/absolute/non-UTF-8 sources, duplicate event IDs, event-contract drift, and moved or exceeded Lite budgets.
- Formatted signed basis-point percentages from an explicit sign and absolute magnitude, including comparisons where Lite exceeds Full.
- Reported the complete Generic composed prompt from `build_release.compose_generic_workflow` as a separate fixed cost applying equally to Full and Lite. No Generic reduction percentage or billing guarantee is claimed.

## Files changed

- `scripts/measure_workflow_token_proxy.py`
- `tests/release/test_workflow_token_proxy.py`
- `tests/release/fixtures/workflow-token-proxy/benchmark.json`
- `tests/release/fixtures/workflow-token-proxy/full/*.md`
- `tests/release/fixtures/workflow-token-proxy/lite/*.md`
- `docs/evidence/lite-workflow-mode-1.3.0-ticket-6.md`

No release configuration, builder, version declaration, generated package, checksum, Ticket 4/5 document, approved Plan, installation, Config file, or external state was changed.

## TDD evidence

### Valid Red

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_representative_codex_fixture_passes_sixty_percent_gate -v
```

Observed before the measurement script existed:

```text
test_representative_codex_fixture_passes_sixty_percent_gate ... FAIL
AssertionError: 2 != 0 : ...python.exe: can't open file
'C:\Users\Ian\Desktop\Grill Me\scripts\measure_workflow_token_proxy.py':
[Errno 2] No such file or directory
Ran 1 test in 0.100s
FAILED (failures=1)
```

This was the approved missing behavior: the public deterministic measurement CLI did not exist. The test reached the CLI boundary and did not fail for fixture setup or an unrelated repository defect.

### Secondary strict-schema Red

After initial Green, final inspection found that a budget label could move from the completion event to the Review event while preserving the three budget names. A regression test was added before correcting the validator.

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_lite_budget_labels_cannot_move_to_different_events -v
```

Observed result:

```text
test_lite_budget_labels_cannot_move_to_different_events ... FAIL
AssertionError: 0 != 2
Ran 1 test in 0.206s
FAILED (failures=1)
```

The emitted report incorrectly associated the completion limit with `lite-review`. The validator was then tightened so each fixed budget belongs to its exact intended event and duplicate budget declarations fail closed.

### Approved Review correction Red

The initial independent Review found that non-instruction sources could be redirected or replayed to manufacture a passing gate and that negative basis points were disclosed one percentage point too low. The user approved both corrections before these tests or fixes were added.

Source-contract command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_event_contract_rejects_redirected_sources_for_both_modes tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_event_contract_rejects_category_redirection tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_replayed_full_output_cannot_manufacture_a_passing_gate -v
```

Observed before the source-contract fix:

```text
test_event_contract_rejects_redirected_sources_for_both_modes ... FAIL (2 subtests)
test_event_contract_rejects_category_redirection ... FAIL
test_replayed_full_output_cannot_manufacture_a_passing_gate ... FAIL

Full output replay report:
Full proxy tokens: 173852
Lite proxy tokens: 25356
Reduction: 85.41%
Codex gate: passed

Ran 3 tests in 0.725s
FAILED (failures=4)
```

The replay case first enlarged Lite's unbudgeted implementation/validation output, then redirected all six Full output events to the same unrelated large source. The old validator accepted both source changes and repetition, turning that comparison into a false `85.41%` pass.

Signed-percentage command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_signed_reduction_percentage_when_lite_exceeds_full -v
```

Observed before the percentage-format fix:

```text
basis_points=-6109: '-62.09' != '-61.09'
basis_points=-101: '-2.01' != '-1.01'
basis_points=-1: '-1.01' != '-0.01'
Ran 1 test in 0.011s
FAILED (failures=3)
```

The same test also covers `0 -> 0.00` and `6109 -> 61.09`, which already passed.

### Approved Review correction Green

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_event_contract_rejects_redirected_sources_for_both_modes tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_event_contract_rejects_category_redirection tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_replayed_full_output_cannot_manufacture_a_passing_gate tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_signed_reduction_percentage_when_lite_exceeds_full -v
```

Observed after both fixes:

```text
Ran 4 tests in 0.550s
OK
```

### Approved final Review P2 Red

The final independent Review found that `generic_composed_prompt.source` could be redirected to another repository-owned directory containing the eleven expected filenames. The user explicitly approved this correction before the regression test or production fix was added.

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_generic_source_must_be_the_canonical_prompt_directory -v
```

Observed before the canonical Generic source fix:

```text
test_generic_source_must_be_the_canonical_prompt_directory ... FAIL
AssertionError: 0 != 2
Generic composed prompt normalized bytes: 2881
Generic composed prompt proxy tokens: 721
Codex gate: passed
Ran 1 test in 0.229s
FAILED (failures=1)
```

The mutation created a repository-owned alternate directory with all eleven expected module filenames and filler content, then redirected only the fixture's Generic source. The old validator successfully composed it, reducing the disclosed fixed cost from canonical `13313` to unrelated `721` while leaving the Codex gate passed.

### Approved final Review P2 Green

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_generic_source_must_be_the_canonical_prompt_directory -v
```

Observed after pinning the exact source string before path resolution:

```text
test_generic_source_must_be_the_canonical_prompt_directory ... ok
Ran 1 test in 0.159s
OK
```

### Focused Green

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy -v
```

Final observed result:

```text
Ran 19 tests in 2.736s
OK
```

Coverage includes deterministic output, the exact per-mode event contract, Full and Lite source-redirection rejection, repeated Full-source gate fabrication, shared exclusions, normalization, signed percentage boundaries, integer threshold arithmetic, prompt-growth failure, non-configurable threshold, path and UTF-8 defense, duplicate IDs, exact budget ownership and limits, canonical Generic source enforcement, actual Generic composition, and prohibited Generic reduction/billing claims.

## Observed benchmark

Command:

```text
.\.venv\Scripts\python.exe scripts\measure_workflow_token_proxy.py --fixture tests\release\fixtures\workflow-token-proxy\benchmark.json
```

Observed result:

```text
Algorithm: normalized-utf8-quarter-v1
Fixture: tests/release/fixtures/workflow-token-proxy/benchmark.json (a33269fee015b43f0b47a64b7c3a45d172def664c202a79f48ab5a1572dca415)
Full proxy tokens: 13768
Lite proxy tokens: 5356
Difference: 8412
Reduction: 61.09% (minimum 60.00%)
Codex gate: passed
Generic composed prompt fixed cost: 13313 proxy tokens
```

Full contains `55,069` normalized UTF-8 bytes and Lite contains `21,422`. The exact integer result is `6109` basis points, and `5356 * 100 <= 13768 * 40` is true.

Lite budget observations:

- Questions: `117 / 500` proxy tokens.
- Change Brief: `405 / 800` proxy tokens.
- Completion: `112 / 500` proxy tokens.

The complete Generic composition contains `53,251` normalized bytes, or `13,313` proxy tokens. Its raw composed SHA-256 is `90431d413c2909e4ed90909349ea4307570ab3d10abfbd329bf084a886f9fefa`. Its source is fixed to `adapters/generic-prompts`; it is reported as a fixed cost for both Generic modes and is not part of the tools-capable Codex 60% gate.

The focused determinism check invoked the JSON CLI twice and observed byte-identical stdout. A separate in-memory comparison also observed `ByteIdentical: True` for the `9,021`-character JSON report with SHA-256 `e6ddc06847fa77bb6da9e567ad653b66923000c3eeef9bb90f2b73b0a06647bd`.

## Broader verification

### Relevant release contracts

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_release_contract tests.release.test_generic_release -v
```

Observed result:

```text
Ran 11 tests in 1.399s
OK
```

### Codex adapter suite

```text
.\.venv\Scripts\python.exe -m unittest discover -s tests\codex -t . -v
Ran 23 tests in 0.531s
OK
```

### Core conformance suite

```text
.\.venv\Scripts\python.exe -m unittest discover -s tests\conformance -t . -v
Ran 18 tests in 0.595s
OK
```

### Generic adapter suite

```text
.\.venv\Scripts\python.exe -m unittest discover -s tests\generic -t . -v
Ran 32 tests in 0.395s
OK
```

### Python syntax

```text
.\.venv\Scripts\python.exe -m py_compile scripts\measure_workflow_token_proxy.py tests\release\test_workflow_token_proxy.py
Exit code: 0
```

### Generic actual-composer hash

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy.WorkflowTokenProxyTests.test_generic_report_hashes_the_actual_builder_composition -v
test_generic_report_hashes_the_actual_builder_composition ... ok
Ran 1 test in 0.126s
OK
```

### Event-contract mutation matrix

An inline standard-library runner reversed each Full and Lite event order once, then independently mutated every one of the 20 events' `id`, `category`, `source`, and `budget` fields. Each mutation invoked the public JSON CLI against a temporary repository-owned fixture.

```text
@'
import copy
import tempfile
from pathlib import Path

from tests.release.test_workflow_token_proxy import (
    EXPECTED_CATEGORIES,
    ROOT,
    read_fixture,
    run_proxy,
    write_fixture,
)

failures = []
checked = 0

def verify(label, data):
    global checked
    checked += 1
    with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
        fixture = Path(temporary) / "benchmark.json"
        write_fixture(fixture, data)
        result = run_proxy(fixture)
    if result.returncode != 2:
        failures.append((label, result.returncode, result.stderr, result.stdout[:200]))

for mode in ("full", "lite"):
    data = read_fixture()
    data["modes"][mode]["events"].reverse()
    verify(f"{mode}.order", data)

for mode in ("full", "lite"):
    base = read_fixture()
    events = base["modes"][mode]["events"]
    for index, original in enumerate(events):
        data = copy.deepcopy(base)
        item = data["modes"][mode]["events"][index]
        item["id"] = f"{item['id']}-mutated"
        verify(f"{mode}[{index}].id", data)

        data = copy.deepcopy(base)
        item = data["modes"][mode]["events"][index]
        item["category"] = next(
            category
            for category in EXPECTED_CATEGORIES
            if category != item["category"]
        )
        verify(f"{mode}[{index}].category", data)

        data = copy.deepcopy(base)
        item = data["modes"][mode]["events"][index]
        item["source"] = events[(index + 1) % len(events)]["source"]
        verify(f"{mode}[{index}].source", data)

        data = copy.deepcopy(base)
        item = data["modes"][mode]["events"][index]
        item["budget"] = "questions" if item["budget"] is None else None
        verify(f"{mode}[{index}].budget", data)

print(f"Rejected: {checked - len(failures)}/{checked}")
if failures:
    for failure in failures:
        print(failure)
    raise SystemExit(1)
'@ | .\.venv\Scripts\python.exe -
Rejected: 82/82
Exit code: 0
```

### Diff whitespace validation

```text
git diff --check
Exit code: 0
```

Git emitted only existing LF-to-CRLF working-copy conversion warnings for tracked parallel files; it reported no whitespace error.

## Complete release discovery disclosure

Command:

```text
.\.venv\Scripts\python.exe -m unittest discover -s tests\release -t . -v
```

Observed result:

```text
Ran 86 tests in 10.740s
FAILED (failures=4, errors=1)
```

All 18 Ticket 6 tests present at that discovery passed. The later Generic canonical-source regression passes in the final focused `19/19` result. The complete release discovery is not reported as passing. Its failures are outside Ticket 6 ownership:

1. `test_retained_workflow_inventory_and_rules_are_unchanged` still expects the historical ten-file Generic prompt inventory and rejects the already-added canonical `lite-workflow.md`. Final inventory integration is explicitly Ticket 7 scope.
2. Three localized `test_readme_has_one_localized_section_before_each_more_information_marker` subtests still expect the old README installation headings while Ticket 5 documentation work is active. Ticket 6 did not modify README or those assertions.
3. `tests.release.test_plugin_assets` could not import because the repository-local `.venv` lacks `PIL` (`ModuleNotFoundError: No module named 'PIL'`). No dependency was installed during Ticket 6.

These unrelated results do not invalidate the focused proxy behavior, but they remain unavailable as a clean complete-release-suite result and must not be presented as passing evidence.

## Residual risks and incomplete checks

- The proxy is deterministic repository-controlled evidence, not a tokenizer-specific measurement, API billing prediction, total-context guarantee, hidden-reasoning measurement, or prompt-cache estimate.
- The passing margin is `1.09` percentage points. Future prompt or fixture growth may legitimately fail the gate and require both modes to be re-evaluated; the fixture must not be padded to restore a pass.
- Semantic equivalence of the human-readable Full and Lite fixture remains a Review responsibility in addition to automated inventory checks.
- Ticket 7 must add the final required validation-check ID and Generic module inventory without weakening the benchmark. Ticket 8 must reject missing or failed proxy ledger evidence.
- The complete release discovery remains non-clean for the three disclosed ownership/environment causes above.
- A fresh independent post-final-fix Review remains required before Ticket 6 can hand off to Ticket 7.
