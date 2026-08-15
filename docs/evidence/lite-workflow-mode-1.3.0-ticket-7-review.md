# Ticket 7 Independent Review Report

artifact_type: `review-report`

artifact_id: `lite-workflow-mode-1-3-ticket-7-review`

workflow_id: `lite-workflow-mode`

core_version: `1.1.0`

Reviewed release target: `1.3.0`

review_label: `independent`

Approved implementation mode: `tdd`

status: `passed-with-verification-gaps`

## Findings

No actionable findings. No P0, P1, P2, or P3 defect was identified in the reviewed Ticket 7 scope.

The active `1.3.0` identities, release configuration, Plugin and adapter manifests, marketplace reference, generated `dist/` packages, archive names, checksums, runtime inventories, historical `1.2.0` preservation guard, and required workflow-token-proxy gate agree in the reviewed snapshot.

## Inputs

- Approved Specification: `docs/specs/lite-workflow-mode-1.3.0.md`, especially packaging and release identity requirement 15 and acceptance criterion 22.
- Approved Ticket Plan: Ticket 7 in `docs/plans/lite-workflow-mode-1.3.0.md`, including its approved `tdd` mode, scope, boundaries, and completion conditions.
- Current Git diff/status and relevant surrounding source, configuration, generated output, and tests.
- `release/release.json`, `scripts/build_release.py`, active Core/adapter declarations, `.agents/plugins/marketplace.json`, the Codex Plugin manifest, the Generic manifest, and current ignored `dist/` output.
- `tests/release/test_release_1_3_contract.py`, the replaced `tests/release/test_release_1_2_contract.py` from `HEAD`, related release/token-proxy/conformance tests, and reviewer-executed raw results below.
- No Ticket 7 implementation evidence or prior reviewer conclusion was read. In particular, `docs/evidence/lite-workflow-mode-1.3.0-ticket-7.md` was excluded.

## Assumptions

- The reviewed working-tree snapshot is the intended Ticket 7 candidate; unrelated earlier Ticket changes are context only where they feed the package contract.
- `dist/` is intentionally Git-ignored but is an in-scope generated deliverable. Its bytes were inspected and compared with canonical source without rebuilding or modifying the checked-in workspace output.
- The SHA-256 inventory in `tests/release/test_release_1_3_contract.py` identifies the approved `1.2.0` artifacts that Ticket 7 must preserve.
- External publication state is not evidence of local package correctness and remains outside Ticket 7.

## Acceptance Review

- Active identity: `release/release.json:5-6`, Core, both adapter declarations, Plugin `version`, and marketplace `ref` identify `1.3.0`. A search of active Core/adapter/release surfaces found no active `1.2.0` declaration; remaining matches are deliberate historical assertions in the new contract test.
- Release configuration: Codex archive, Generic directory/archive, `lite-workflow.md` inventory, and required `workflow-token-proxy` check are declared at `release/release.json:10`, `release/release.json:24-32`, and `release/release.json:45`.
- Marketplace and manifests: `.agents/plugins/marketplace.json:13`, `adapters/codex/plugin/ask-then-do-it/.codex-plugin/plugin.json:3`, `adapters/codex/conformance.yaml:2-4`, and `adapters/generic-prompts/manifest.yaml:2-4` are aligned.
- Builder contract: `scripts/build_release.py:181-189` rejects marketplace/version drift; `scripts/build_release.py:570-624` composes the editable Generic mode declaration and routing header; the existing atomic staging, exact inventory, reproducible ZIP, ZIP-equivalence, and checksum paths remain covered by passing tests.
- Generated output: current `dist/` exactly matches canonical Codex source and Generic builder composition. The Codex package contains 27 files and the Generic package 18 files; both ZIPs equal their directories.
- Checksums: Codex archive SHA-256 is `e393194a6496544dd9a389960d68cbe55132e54918d9549d2f3d7e4764b6d195`; Generic archive SHA-256 is `0708afb2626d6cb981ab179d3583ae3d0ab845e5e4c97ee374afc02cd6e5a1f7`. Both match `dist/checksums.sha256` exactly.
- Historical preservation: no Git diff/status entry exists for the approved `1.2.0` requirement, Specification, plan, or evidence files. The fixed hash guard at `tests/release/test_release_1_3_contract.py:57-74` passed for every listed artifact.
- Token proxy: the required check is present in release configuration and its independent executable gate passed at 61.09%, above the 60.00% minimum.

## Verification

Raw reviewer results:

1. `python -B -m unittest tests.release.test_release_1_3_contract -v`
   - Environment result: command not found; zero tests executed because bare `python` is not on this shell's PATH.
2. `.\.venv\Scripts\python.exe -B -m unittest tests.release.test_release_1_3_contract -v`
   - `Ran 7 tests in 1.530s`
   - `OK`
3. `.\.venv\Scripts\python.exe -B -m unittest tests.release.test_workflow_token_proxy tests.release.test_release_contract tests.release.test_release_safety tests.release.test_clean_slate tests.release.test_codex_release tests.release.test_generic_release tests.release.test_marketplace_contract -v`
   - `Ran 50 tests in 10.008s`
   - `OK`
4. `.\.venv\Scripts\python.exe -B -m unittest discover -s tests\conformance -p "test_*.py" -v`
   - `Ran 18 tests in 0.562s`
   - `OK`
5. `.\.venv\Scripts\python.exe -B scripts\validate_conformance.py --catalog core\rules\rules.yaml --manifest adapters\codex\conformance.yaml`
   - `Conformance passed: codex against core 1.3.0`
6. `.\.venv\Scripts\python.exe -B scripts\validate_conformance.py --catalog core\rules\rules.yaml --manifest adapters\generic-prompts\manifest.yaml`
   - `Conformance passed: generic-prompts against core 1.3.0`
7. `.\.venv\Scripts\python.exe -B scripts\validate_marketplace.py --catalog .agents\plugins\marketplace.json`
   - `Marketplace validation passed: .agents\plugins\marketplace.json`
8. `.\.venv\Scripts\python.exe -B scripts\measure_workflow_token_proxy.py`
   - Algorithm: `normalized-utf8-quarter-v1`
   - Fixture SHA-256: `0c7f08879883f04f85ba10cb2553e49e7cda83559c068d3e3df8ead155f4413f`
   - Full: `13768`; Lite: `5356`; difference: `8412`; reduction: `61.09%`; gate: `passed`
   - Generic fixed cost: `13313` proxy tokens, explicitly without a Generic 60% or billing guarantee.
9. Read-only canonical-source-to-`dist/` comparison using the builder's own validation, composition, ZIP-equivalence, and checksum readers:
   - `Codex package exact: 27 files`
   - `Generic package exact: 18 files`
   - `ZIP equivalence and checksum inventory: passed`
10. `git diff --check`
    - Exit code `0`; no whitespace error. Git emitted only existing Windows LF-to-CRLF conversion warnings.

## Twelve Lenses

| # | Lens | Outcome | Evidence |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `no-finding` | Release identity and runtime inventories are centralized in `release/release.json`; necessarily repeated package/manifest declarations are locked by `tests/release/test_release_1_3_contract.py:135-248` and conformance validation. No independently maintained equivalent policy diverged. |
| 2 | Long Function | `no-finding` | Ticket 7 adds bounded marketplace validation in `load_config` and a bounded Generic header change in `compose_generic_workflow`; it does not introduce a new mixed-responsibility long function. |
| 3 | Large Module or Class | `no-finding` | `scripts/build_release.py` remains cohesive around one deterministic release-build boundary. The reviewed change adds no class or unrelated module responsibility. |
| 4 | Long Parameter List | `not-applicable` | No changed Ticket 7 interface introduces a long parameter list; the changed helpers consume the existing release config/source abstractions. |
| 5 | Data Clumps | `no-finding` | Version, provider paths, archives, inventories, and required gates travel as the structured release configuration rather than repeated loose argument groups. |
| 6 | Primitive Obsession | `no-finding` | Strict semver, relative output paths, exact configuration keys, PNG headers, SHA-256 entries, inventories, and marketplace refs are validated before output; raw strings are not accepted without domain checks. |
| 7 | Feature Envy | `not-applicable` | The changed procedural builder functions operate on release configuration and package sources that they own; no object reaches through another object's internal state. |
| 8 | Divergent Change | `no-finding` | The builder's validation, composition, and packaging edits all serve the same `1.3.0` release-integration reason. No unrelated reason to change was added. |
| 9 | Shotgun Surgery | `no-finding` | Version edits span mandated user-visible declarations, but one release config plus lockstep contract tests and generated `dist/` prevent silent drift. The fan-out is the approved release surface, not an avoidable new dependency. |
| 10 | Message Chains | `not-applicable` | No changed call or object-navigation chain exposes nested runtime internals; configuration access remains local to the builder boundary. |
| 11 | Leaky Abstraction | `no-finding` | Callers select package/output through the builder interface; atomic staging, source validation, ZIP layout, checksums, and marketplace lockstep remain internal and independently verified. |
| 12 | Shallow Module | `no-finding` | Builder helpers hide substantial deterministic filesystem, inventory, archive, and validation behavior behind narrow functions; their interfaces are justified by the behavior they encapsulate. |

This lens pass is scoped to Ticket 7 and does not claim a system-wide architecture diagnosis. No systemic finding requires routing to architecture diagnosis.

## Evidence Unavailable And Deferred

- Pre-implementation Red evidence was not among the permitted independent-review inputs, so the reviewer cannot independently confirm the TDD event sequence. The final test changes and Green results are present; the workflow coordinator must retain the original Red evidence separately.
- The complete repository-wide suite and completed release-evidence validation were not run here. Those are intentionally deferred to Ticket 8 rather than expanding this Ticket 7 review.
- External Git tag creation, GitHub Release state, push, upload, installation, and publication were not checked and remain out of scope. Until publication, the marketplace `v1.3.0` ref is a local contract rather than a remotely resolvable release.
- The default builder was not rerun against the workspace `dist/` because this review was authorized to write only this report. Isolated builder tests passed, and a read-only exact comparison proved the existing `dist/` bytes equal current canonical output.

## Residual Risk

- `dist/` is Git-ignored, so its verified bytes are not represented by the normal source diff; release handling must preserve the reviewed output and checksums.
- The historical preservation test uses an explicit approved-artifact hash inventory. A future historical artifact addition would need an intentional inventory update; the current approved `1.2.0` set passed.
- Full combined validation and final evidence completeness remain dependent on Ticket 8.

## Ticket Completion Assessment

Ticket 7 appears complete against its approved behavioral and packaging acceptance surface. Current identities agree on `1.3.0`; both adapters conform to Core `1.3.0`; configured and generated inventories are exact; packages, ZIPs, and checksums are reproducible and mutually consistent; the token-proxy required gate passes; and approved historical `1.2.0` artifacts are unchanged.

The assessment is qualified only by the unavailable independent TDD Red sequence and explicitly deferred Ticket 8/external-release checks. No blocking or actionable Review finding remains in Ticket 7.

## Handoff

Return to the workflow coordinator to retain the implementation's original TDD Red evidence and accept or reject this independent Review. If accepted, proceed to the separately approved Ticket 8 integrated-validation and release-evidence gate; do not treat this report as external publication approval.
