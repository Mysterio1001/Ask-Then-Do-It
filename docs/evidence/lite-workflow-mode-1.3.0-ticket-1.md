# Lite Workflow Mode 1.3.0 Ticket 1 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `lite-workflow-mode-1-3-ticket-1-evidence`

Workflow ID: `lite-workflow-mode`

Core version: `1.2.0`

Target release version: `1.3.0`

Status: Completed

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), and Ticket 1 in approved `tdd` mode.

Assumptions: Ticket 1 owns the provider-neutral Core contract and conformance fixtures. Codex and Generic implementations of the new mandatory rules are intentionally owned by Tickets 2 and 3; this evidence does not claim those adapters conform before their Tickets complete.

Deferred: Codex mapping, Generic mapping, localized documentation, deterministic token proxy, `1.3.0` version integration, generated packages, and release evidence.

Handoff: `$review-code` with the approved artifacts, Ticket 1 Core/test diff, and the raw results below.

## Outcome

- Added a dedicated provider-neutral Lite workflow module without adding a Lite or Change Brief artifact template.
- Added top-level `full` and `lite` mode resolution before stage routing.
- Preserved the existing Full requirement, Specification, Ticket Planning, `tdd`/`direct`, Review, and architecture path.
- Scoped the existing exactly-one-question rule to Full so it does not conflict with Lite's maximum-three-question batches.
- Added eight mandatory Core rules and adapter mapping obligations for mode resolution, Full preservation, Lite questions, Change Brief approval, risk, validation, Review, and session completion.

## Files changed

- `core/CORE.md`
- `core/modules/orchestration.md`
- `core/modules/requirements.md`
- `core/modules/lite-workflow.md`
- `core/rules/rules.yaml`
- `core/adapters/manifest-contract.md`
- `tests/conformance/test_lite_core_contract.py`
- `tests/conformance/test_validator.py`
- `tests/conformance/fixtures/*.yaml`

## TDD evidence

### Setup attempt

The first command used the bundled Python runtime and failed before test collection because that runtime did not contain the repository's declared `PyYAML` development dependency:

```text
python -m unittest tests.conformance.test_lite_core_contract.LiteCoreContractTests.test_core_exposes_dedicated_lite_module_without_artifact_template

ImportError: Failed to import test module: test_lite_core_contract
ModuleNotFoundError: No module named 'yaml'
FAILED (errors=1)
```

This was not accepted as Red. The new focused test was temporarily changed to use only the standard library so the missing production behavior could be observed independently of setup. A repository-local ignored `.venv` was then created and `requirements-dev.txt` installed. During the final refactor, the test returned to the project's structured PyYAML parser.

### Valid Red

Command:

```text
.venv\Scripts\python.exe -m unittest tests.conformance.test_lite_core_contract.LiteCoreContractTests.test_core_exposes_dedicated_lite_module_without_artifact_template
```

Observed result before production implementation:

```text
FAIL: test_core_exposes_dedicated_lite_module_without_artifact_template
AssertionError: False is not true : Core must expose a dedicated Lite workflow module
Ran 1 test in 0.000s
FAILED (failures=1)
```

The failure was the approved missing behavior: `core/modules/lite-workflow.md` did not exist.

### Focused Green

Command:

```text
.venv\Scripts\python.exe -m unittest tests.conformance.test_lite_core_contract
```

Observed result:

```text
Ran 5 tests in 0.002s
OK
```

### Post-refactor verification

No additional structural refactor was needed after Green. The focused suite was rerun after final inspection:

```text
Ran 5 tests in 0.001s
OK
```

### Broader verification

Command:

```text
.venv\Scripts\python.exe -m unittest discover -s tests/conformance -p "test_*.py"
```

Observed result:

```text
Ran 17 tests in 0.945s
OK
```

Shared validator command:

```text
.venv\Scripts\python.exe scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest tests/conformance/fixtures/valid.yaml
```

Observed result:

```text
Conformance passed: fixture-valid against core 1.2.0
```

Additional checks:

- `git diff --check`: passed; Git reported only the repository's existing LF-to-CRLF checkout warnings.
- Provider-specific Core scan for `codex`, `gemini`, `claude`, `.codex`, and `Default workflow mode`: no matches.
- New-file trailing-whitespace scan: no findings.

## Incomplete checks and residual risk

- Actual Codex and Generic manifests do not yet claim the eight new mandatory rules. Their implementations and truthful mappings belong to Tickets 2 and 3, so adapter conformance is not claimed here.
- The complete repository suite and release builder are intentionally deferred until downstream adapter, documentation, token-proxy, and release integration Tickets complete.
- Markdown contract tests prove required content and composition boundaries; they cannot guarantee that every future model response stays within approximate token budgets.

## Review correction cycle

The first independent Review reported three in-scope findings: contradictory invalid-default fallback, mandatory budgets written as recommendations, and a missing zero-finding Review branch.

New focused assertions were added first. Before correction, the two selected tests produced two expected failures:

```text
Ran 2 tests in 0.001s
FAILED (failures=2)
```

The Core contract was then changed so absent project configuration continues to the user default, present invalid project configuration fails closed to Full, valid explicit instruction still wins, the 800/500 budgets use `MUST`, and a zero-finding Review reports that result without an empty correction gate.

Focused correction Green:

```text
Ran 2 tests in 0.000s
OK
```

Final post-refactor verification:

```text
.venv\Scripts\python.exe -m unittest tests.conformance.test_lite_core_contract
Ran 6 tests in 0.012s
OK

.venv\Scripts\python.exe -m unittest discover -s tests/conformance -p "test_*.py"
Ran 18 tests in 0.596s
OK

.venv\Scripts\python.exe scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest tests/conformance/fixtures/valid.yaml
Conformance passed: fixture-valid against core 1.2.0
```
