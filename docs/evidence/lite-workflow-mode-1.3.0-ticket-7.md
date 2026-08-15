# Lite Workflow Mode 1.3.0 Ticket 7 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `lite-workflow-mode-1-3-ticket-7-evidence`

Workflow ID: `lite-workflow-mode`

Workflow core version: `1.1.0`

Repository Core version: `1.3.0`

Target release version: `1.3.0`

Status: Completed

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), completed Tickets 1-6 and their required Review handoffs, and Ticket 7 in approved `tdd` mode.

Assumptions: Canonical Core, Codex, Generic, documentation, and release sources are authoritative. Generated `dist/` content is replaced only through `scripts/build_release.py`. References to `1.2.0` in approved historical artifacts, compatibility text, project history, and deliberate negative-test mutations are not active release declarations.

Deferred: The `1.3.0` validation ledger, evidence-gate integration, release-milestone architecture diagnosis, final independent Review, and completed release evidence belong to Ticket 8. External installation, Config mutation, Git tag, publication, upload, push, and announcement were not performed.

Handoff: A fresh independent `$review-code` context should receive the Approved Specification and Ticket, the complete Ticket 7 diff, `tests/release/test_release_1_3_contract.py`, this evidence, the default `dist/` inventory and checksums, and the raw results below. No Ticket 7 Review was performed during implementation.

## Outcome

- Moved every active release and Core identity to `1.3.0`, including the Codex Plugin manifest, marketplace tag, Core catalog, adapter manifests, Generic prompt declarations, release configuration, current download references, and package entry headings.
- Added `lite-workflow.md` to the ordered Generic runtime inventory immediately after `orchestration.md`.
- Preserved exactly nine Codex Skill roots and packaged the Lite runtime reference recursively at `skills/ask-then-do-it/references/lite-workflow.md`.
- Added `workflow-token-proxy` to the required release checks.
- Updated current conformance fixtures and active tests explicitly; no blind repository-wide version replacement was used.
- Replaced the old current-release contract test with a `1.3.0` contract covering active identities, package boundaries, exact runtime inventories, marketplace drift rejection, isolated reproducibility, ZIP equivalence, checksums, and historical-byte preservation.
- Rebuilt the default `dist/` atomically through the release builder. Codex packages contain both approved image assets; Generic packages contain no assets; neither package contains marketplace metadata.
- Preserved the approved `1.2.0` requirement, specification, plan, release evidence, and ticket evidence bytes verified by pinned SHA-256 values.

## Ticket 7 files and outputs

The integration changed active version declarations and release contracts in these ownership areas:

- `.agents/plugins/marketplace.json`
- `core/CORE.md`, `core/rules/rules.yaml`
- `adapters/codex/conformance.yaml`, `adapters/codex/rule-mapping.yaml`
- `adapters/codex/plugin/ask-then-do-it/.codex-plugin/plugin.json`
- artifact-emitting Codex `SKILL.md` files and the three packaged START-HERE sources
- `adapters/generic-prompts/manifest.yaml` and all eleven Generic prompt sources
- `release/release.json` and the three Generic package START-HERE sources
- current README, root START-HERE, Codex guide, and Generic guide release references
- `scripts/validate_marketplace.py`
- active Codex, Generic, conformance, documentation, release, and token-proxy tests and fixtures
- `tests/release/test_release_1_3_contract.py` replacing `tests/release/test_release_1_2_contract.py`
- generated default `dist/`
- this evidence file

No existing Requirement Decision Record, Specification, Ticket Plan, Ticket 1-6 evidence, historical release evidence, user Config, or external state was modified by Ticket 7.

## TDD evidence

### Initial valid Red

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_release_1_3_contract -v
```

Observed before the lockstep source and release changes:

```text
Ran 7 tests
FAILED (failures=24)
```

The historical `1.2.0` hash-control test passed. The 24 assertion and subtest failures were the expected missing Ticket 7 behavior: active `1.3.0` declarations, the required token-proxy gate, the Generic Lite inventory, new package paths, package contents, and deterministic `1.3.0` archives were absent or still declared as `1.2.0`. There was no setup or unrelated failure.

### First focused Green

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_release_1_3_contract -v
```

Observed result:

```text
Ran 7 tests in 2.293s
OK
```

### Active-guide stale-version Red and Green

The final stale-version scan found that the three current Codex guides linked to `1.3.0` but still described the matching fallback ZIP as `1.2.0`. A regression assertion was added before correcting the three localized guide sentences.

Red command and result:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_release_1_3_contract.ReleaseOneThreeContractTests.test_active_identity_and_current_document_downloads_are_1_3_0 -v
Ran 1 test in 0.004s
FAILED (failures=3)
```

The three failures were exactly `docs/guides/codex.en.md`, `docs/guides/codex.zh-TW.md`, and `docs/guides/codex.ja.md` containing the stale `1.2.0` fallback sentence.

Green result after the localized correction:

```text
Ran 1 test in 0.003s
OK
```

### Final focused Green

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_release_1_3_contract -v
Ran 7 tests in 1.413s
OK
```

## Release build and package verification

The pre-build default `dist/` was a complete verified `1.2.0` output containing exactly `codex`, `generic`, and `checksums.sha256`. It was then replaced through the only approved builder entrypoint:

```text
.\.venv\Scripts\python.exe scripts\build_release.py
Built codex, generic release 1.3.0 in C:\Users\Ian\Desktop\Grill Me\dist
```

Final default archive checksums:

```text
e393194a6496544dd9a389960d68cbe55132e54918d9549d2f3d7e4764b6d195  codex/ask-then-do-it-1.3.0.zip
0708afb2626d6cb981ab179d3583ae3d0ab845e5e4c97ee374afc02cd6e5a1f7  generic/ask-then-do-it-generic-1.3.0.zip
```

The focused contract built two additional isolated output roots and observed identical relative-file sets and bytes. It also compared every non-directory ZIP entry and byte payload to its unpacked package, recalculated every SHA-256 value, checked the exact nine-Skill and eleven-prompt inventories, required the nested Lite reference and Codex assets, and rejected assets or marketplace metadata in Generic.

## Native validators

The repository-used system Skill validator ran once for each of the nine canonical Skills and once for each of the nine default packaged Skills:

```text
.\.venv\Scripts\python.exe C:\Users\Ian\.codex\skills\.system\skill-creator\scripts\quick_validate.py <skill-root>
18 validations: Skill is valid!
```

Canonical and default packaged Plugin roots passed the system Plugin validator:

```text
Plugin validation passed: C:\Users\Ian\Desktop\Grill Me\adapters\codex\plugin\ask-then-do-it
Plugin validation passed: C:\Users\Ian\Desktop\Grill Me\dist\codex\ask-then-do-it
```

Adapter and marketplace CLIs:

```text
Conformance passed: codex against core 1.3.0
Conformance passed: generic-prompts against core 1.3.0
Marketplace validation passed: .agents\plugins\marketplace.json
```

## Token-proxy gate

Command:

```text
.\.venv\Scripts\python.exe scripts\measure_workflow_token_proxy.py --fixture tests\release\fixtures\workflow-token-proxy\benchmark.json --json
```

Observed Codex result:

- Full: `13,768` proxy tokens from `55,069` normalized bytes.
- Lite: `5,356` proxy tokens from `21,422` normalized bytes.
- Difference: `8,412` proxy tokens.
- Reduction: `61.09%` (`6109` basis points), above the fixed `60.00%` gate.
- Lite questions: `117 / 500`; Change Brief: `405 / 800`; completion: `112 / 500`.
- Fixture SHA-256: `0c7f08879883f04f85ba10cb2553e49e7cda83559c068d3e3df8ead155f4413f`.

Observed Generic disclosure:

- Complete composed prompt fixed cost: `13,313` proxy tokens from `53,251` normalized bytes.
- Composed SHA-256: `b022c1260ca81fd95c12d8e55e6f0e9b7d651b01bab6ebcbb330ce76c3a72acc`.
- The fixed cost applies equally to Full and Lite; no Generic 60% guarantee or billing guarantee is claimed.

The dedicated token-proxy suite remained Green after the active Full fixture Core declarations changed to `1.3.0`:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_workflow_token_proxy -v
Ran 19 tests in 2.931s
OK
```

## Broader verification

### Adapter and conformance suites

```text
.\.venv\Scripts\python.exe -m unittest discover -s tests\codex -t . -v
Ran 23 tests in 0.470s
OK

.\.venv\Scripts\python.exe -m unittest discover -s tests\generic -t . -v
Ran 32 tests in 0.470s
OK

.\.venv\Scripts\python.exe -m unittest discover -s tests\conformance -t . -v
Ran 18 tests in 0.624s
OK
```

The first Generic run produced 11 expected current-test failures because one shared interface assertion still required prompt and Core version `1.2.0`. Updating that active test to `1.3.0` made all 32 tests pass; no prompt behavior was weakened.

### Release suite

The pre-rebuild run executed 99 tests. It had exactly one expected assertion failure because default `dist/` still contained the inspected `1.2.0` archives and one environment import error because Pillow was not installed in the project venv. After the atomic build and use of the existing read-only workspace runtime dependencies:

```text
$env:PYTHONPATH='C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages'
.\.venv\Scripts\python.exe -m unittest discover -s tests\release -t . -v
Ran 101 tests in 13.204s
OK
```

No dependency was installed or modified.

### Full discovery

The first attempted full command used `-s tests -t .`; unittest rejected it before executing tests because the `tests/` root is intentionally not importable. The corrected repository discovery command omitted `-t .`:

```text
$env:PYTHONPATH='C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages'
.\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py'
Ran 174 tests in 14.000s
OK
```

### Version and diff inspection

The active scan covered `core`, `adapters`, `release`, `scripts`, root README and START-HERE files, `tests`, and unpacked `dist/`. It found no stale `1.2.0` or `v1.2.0` declaration outside `tests/release/test_release_1_3_contract.py`. That test retains only:

- pinned historical artifact paths and SHA-256 values;
- assertions that active documents and emitted Skill envelopes do not retain `1.2.0`;
- a deliberate `v1.2.0` marketplace mutation proving drift rejection.

Remaining repository matches are historical or provenance context under approved requirements, specifications, plans, evidence, and project knowledge/drafts. They were intentionally preserved. `git diff --check` exited `0`.

## Environment, gaps, and residual risk

- Environment: Windows, PowerShell, Python `3.12.13` from `.venv`.
- Existing read-only Pillow and PyYAML runtime packages were exposed only through `PYTHONPATH` for full image-asset discovery. No package installation occurred.
- Generated default `dist/` is present and verified locally; no claim is made that it was committed, installed, tagged, uploaded, or published.
- Ticket 8 release evidence and independent Review remain required before any final release-complete claim.
- No known Ticket 7 test, validator, conformance, inventory, reproducibility, ZIP-equivalence, checksum, historical-hash, or active-version failure remains.
