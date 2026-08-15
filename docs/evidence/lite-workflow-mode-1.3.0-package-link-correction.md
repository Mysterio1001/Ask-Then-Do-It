# Ask Then Do It 1.3.0 Package Guide Link Correction Evidence

Artifact type: Implementation Evidence

Artifact ID: `lite-workflow-mode-1-3-package-link-correction-evidence`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Release version: `1.3.0`

Status: Completed

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), Ticket 5 and Ticket 7 implementation/Review handoffs, Draft [1.3.0 Release Architecture Diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis.md) Finding F1, and the user's explicit approval to correct F1 on 2026-08-15.

Approved implementation mode: `tdd` from Tickets 5 and 7.

Assumptions: Package entry pages may depend on the release repository's version-pinned online guides. The `v1.3.0` targets are pre-publication contracts and become externally resolvable only after the separately controlled tag/publication step. The correction must not change README structure, guide prose, runtime behavior, Config, package inventory, or historical `1.2.0` artifacts.

Deferred: External URL reachability before the `v1.3.0` tag exists, Git tag, GitHub Release, push, upload, installation, publication, announcement, and the non-blocking architecture proposals F2-F4.

Handoff: A fresh independent `$review-code` context must inspect the approved F1 correction, final source and package diff, strengthened tests, rebuilt archives, checksums, and raw verification below. No source correction finding may be fixed without a new user approval.

## Outcome

- Replaced all twelve repository-root `/docs/guides/...` links in the six Codex/Generic package `START-HERE` sources with version-pinned `https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides/...` targets.
- Preserved the existing three-language text, headings, concise entry-page scope, runtime inventories, README, canonical complete guides, and package file sets.
- Strengthened documentation and isolated-package tests so a future package cannot silently restore repository-root guide links or lose the host/full-flow handoff.
- Rebuilt the default `dist/` only through `scripts/build_release.py`.

## Files and ownership

Correction source:

- `adapters/codex/plugin/ask-then-do-it/START-HERE.{en,zh-TW,ja}.md`
- `release/generic/START-HERE.{en,zh-TW,ja}.md`

Regression coverage:

- `tests/release/test_documentation.py`
- `tests/release/test_release_1_3_contract.py`

Workflow and generated outputs:

- `docs/plans/lite-workflow-mode-1.3.0.md`
- generated `dist/` directories, ZIPs, and `checksums.sha256`
- this evidence file

No README, canonical guide, Core, adapter runtime policy, release configuration, user Config, or historical `1.2.0` artifact was changed by this correction.

## TDD evidence

### Red

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_release_1_3_contract.ReleaseOneThreeContractTests.test_builder_emits_exact_1_3_runtime_packages_and_reference_inventory tests.release.test_documentation.ReleaseDocumentationTests.test_all_nine_start_pages_are_concise_full_lite_handoffs -v
```

Observed before editing the six source pages:

```text
Ran 2 tests in 0.894s
FAILED (failures=18)
```

Six isolated package subtests detected `](/docs/guides/` in generated Codex and Generic entry pages. Twelve localized documentation subtests detected that the expected `v1.3.0` host and Full/Lite guide URLs were absent. There was no setup or unrelated failure.

### Focused Green

Command:

```text
.\.venv\Scripts\python.exe -m unittest tests.release.test_release_1_3_contract.ReleaseOneThreeContractTests.test_builder_emits_exact_1_3_runtime_packages_and_reference_inventory tests.release.test_documentation.ReleaseDocumentationTests.test_all_nine_start_pages_are_concise_full_lite_handoffs tests.release.test_documentation.ReleaseDocumentationTests.test_localized_user_documents_keep_commands_and_avoid_internal_material -v
```

Observed after replacing only the twelve targets:

```text
Ran 3 tests in 0.870s
OK
```

## Build and package evidence

Default rebuild:

```text
.\.venv\Scripts\python.exe scripts\build_release.py
Built codex, generic release 1.3.0 in C:\Users\Ian\Desktop\Grill Me\dist
```

Final archive hashes:

```text
f3c5ce1e7f48baf5ac619d1719313ca3d91cc1c96af38b67ba4b23aba16bfbd3  codex/ask-then-do-it-1.3.0.zip
df66b786a8ef855cea9d709f350e5abf3fa943fc61cbe8b903712c7e4e240f6b  generic/ask-then-do-it-generic-1.3.0.zip
```

A source/default-package scan found zero `](/docs/guides/` matches. All twelve expected version-pinned links were present in the six generated entry pages. The focused documentation, isolated build, package inventory, ZIP equivalence, reproducibility, checksum, and historical-preservation group passed:

```text
Ran 38 tests in 2.362s
OK
```

## Broader verification

Release suite with the existing read-only Pillow dependency path:

```text
Ran 104 tests in 13.263s
OK
```

The first concurrent full-discovery run executed 177 tests and hit one Windows `WinError 5` while the atomic-upgrade test moved its own temporary `codex` directory. In the same validation round, that test passed inside the complete 104-test release suite. No source assertion failed. The affected test was then rerun alone:

```text
Ran 1 test in 0.610s
OK
```

The final full discovery was rerun serially:

```text
Ran 177 tests in 14.781s
OK
```

Other observed results:

- Canonical and packaged Codex Plugin validation: `2/2` passed.
- Canonical and packaged Skill validation: `18/18` returned `Skill is valid!`.
- Codex conformance: passed against Core `1.3.0`.
- Generic conformance: passed against Core `1.3.0`.
- Marketplace validation: passed.
- Token proxy: Full `13,768`, Lite `5,356`, reduction `61.09%`; no API billing guarantee and no Generic 60% claim.
- Generic composed prompt: `13,313` proxy tokens; SHA-256 `b022c1260ca81fd95c12d8e55e6f0e9b7d651b01bab6ebcbb330ce76c3a72acc`.
- Fixture SHA-256: `0c7f08879883f04f85ba10cb2553e49e7cda83559c068d3e3df8ead155f4413f`.
- `git diff --check`: exit `0`; only configured LF-to-CRLF warnings.

## Residual risk

- The version-pinned GitHub guide URLs cannot resolve externally until the separately deferred `v1.3.0` tag exists. Tests verify the exact versioned targets and package content without claiming publication or live network reachability.
- `dist/` remains generated and Git-ignored; the default bytes and checksums must be preserved or rebuilt and revalidated before publication.
- The Draft architecture report's F2-F4 proposals remain unaccepted and authorize no refactor.
