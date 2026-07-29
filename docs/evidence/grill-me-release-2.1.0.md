# Implementation Evidence — Grill Me Release 2.1.0

Artifact type: Implementation Evidence

Artifact ID: `grill-me-release-2.1.0-evidence`

Workflow ID: `grill-me-release-2-1`

Core version: `2.0.0`

Status: Completed

## Inputs

- Approved [Grill Me Release Packaging Specification](../specs/grill-me-release-packaging.md).
- Approved [Grill Me Release Packaging Ticket Plan](../plans/grill-me-release-packaging.md).
- Approved Portable AI Development Workflow v2 artifacts and completed [v2 integration evidence](v2-ticket-5.md).
- Canonical Generic and Codex adapter sources.

## Outcome

Release `2.1.0` now provides one validated `grill-me` Codex Plugin and one versioned Generic prompts bundle. The core contract remains `2.0.0`. The build is Python-standard-library-only, deterministic, safe against unmanaged collisions, limited to repository-owned output roots, and performs no personal installation, marketplace mutation, publication, or network operation.

## Ticket red evidence

Each deterministic behavior change began with an observed missing-behavior failure:

| Ticket | Red command | Raw outcome summary |
| --- | --- | --- |
| 1 — Codex Plugin slice | `python -m unittest discover -s tests/release -p "test_codex_release.py" -v` | 3 tests ran; missing `release/release.json`, Plugin manifest, and `scripts/build_release.py` produced 2 errors and 1 failure |
| 2 — Generic slice | `python -m unittest discover -s tests/release -p "test_generic_release.py" -v` | 2 tests ran; missing `generic` config and unsupported `--package generic` produced 1 error and 1 failure |
| 3 — safe replacement | `python -m unittest tests.release.test_release_safety -v` | 4 tests ran; reproducibility, failure preservation, and unmanaged collision checks passed; valid same-directory rebuild failed because existing output was rejected before validation |
| 4 — documentation | `python -m unittest tests.release.test_documentation -v` | 4 checks failed or errored because root README was absent and both guides still described the source-only v2 layout |
| 5 — integration contract | `python -m unittest tests.release.test_release_contract -v` | The initial 4-test pass exposed an unhandled conflicting `core_version`; a later focused boundary test also observed that non-default repository output succeeded without explicit test opt-in |

The newline-only hash changes detected during Ticket 1 were not accepted as a new baseline. All six `agents/openai.yaml` files were restored to their recorded byte-level hashes before migration verification was considered green.

## Focused green evidence

- Ticket 1: 3 Codex release tests and 9 Codex adapter tests passed; Plugin validation passed; all six Skill validators returned `Skill is valid!`.
- Ticket 2: 5 combined Codex and Generic release tests passed.
- Ticket 3: 4 safety tests passed, followed by all 9 then-current release tests.
- Ticket 4: 4 documentation and relative-link checks passed.
- Ticket 5: 5 release-contract checks passed, including explicit test-only opt-in for non-default repository output roots.
- The final Codex package test also compares every packaged Skill file byte-for-byte with `adapters/codex/plugin/grill-me/skills/`.

## Final automated verification

The following suites were executed separately because the original test directories are independent `unittest` discovery roots:

```text
python -m unittest discover -s tests/generic -p "test_*.py" -v
11 tests passed

python -m unittest discover -s tests/codex -p "test_*.py" -v
9 tests passed

python -m unittest discover -s tests/conformance -p "test_*.py" -v
7 tests passed

python -m unittest discover -s tests/release -p "test_*.py" -v
18 tests passed
```

Total: 45 tests passed.

Direct shared conformance results:

```text
Conformance passed: generic-prompts against core 2.0.0
Conformance passed: codex against core 2.0.0
```

Native validation results:

```text
Plugin validation passed: adapters/codex/plugin/grill-me
Plugin validation passed: dist/grill-me
Skill is valid! (6 of 6 packaged Skills)
```

## Reproducibility and checksum evidence

The default builder was executed twice against repository `dist/`. The second build first validated the existing managed release, replaced only those managed targets, and produced byte-identical archives and checksum content.

```text
grill-me-2.1.0.zip
SHA-256 10c9b95e9e75c9dac20e570d0f7ed75ef71e4ad0d59e755f53d27ec5a729236d

generic-prompts-2.1.0.zip
SHA-256 5f5d6e86dbde9e2de99f68528c18df1ea1265b59f65d969a4aa9c70bee954254
```

Both values were recalculated from the final archives and matched `dist/checksums.sha256`. Automated checks also compared every ZIP entry with its unpacked directory counterpart.

## Package inventory and forward evidence

The Codex runtime contains only `.codex-plugin/plugin.json` plus the exact six Skill directories. It contains no core source, tests, conformance metadata, migration records, release tooling, or full documentation. Plugin folder name and manifest name both equal `grill-me`, and `$ai-dev-workflow` remains the documented primary entry while all six direct Skill invocations remain available.

The Generic runtime contains generated `generic-workflow.md`, generated `manifest.yaml`, and byte-identical copies of the bootstrap plus six modular prompts. Composition checks verify declared order, internal routing, approval gates, Conversation-only limitations, `UNEXECUTED IMPLEMENTATION GUIDANCE`, `limited-evidence`, and `non-independent` labels.

Release-specific forward confidence is based on:

- the prior clean-context Generic and Codex scenarios recorded in `v2-ticket-5.md`;
- byte-identical packaging of those forward-tested canonical Skills and modular prompts;
- fresh/resumed Generic scenario tests in the final 11-test Generic suite;
- official validation of the unpacked packaged Plugin and every packaged Skill.

No personal Plugin installation or new external model session was performed, because both are outside the Approved release scope. This evidence therefore validates the installable package shape and prompt handoff, not a mutation of a user's Codex environment.

## Documentation verification

- Root `README.md` presents Traditional Chinese first and an equivalent English Quick Start.
- Both Codex Plugin and Generic prompts are reachable without first understanding repository internals.
- Documentation distinguishes canonical source, generated `dist/`, and personal installation.
- Codex lifecycle instructions follow the current official marketplace boundary and clearly state that the builder does not install or create marketplace metadata.
- Generic instructions preserve model neutrality, user-managed Artifact persistence, and Conversation-only claim limits.
- All tested relative Markdown links resolve, and the updated guides contain no stale `adapters/codex/skills/` source path.

## Changed ownership areas

- `README.md`
- `release/release.json`
- `scripts/build_release.py`
- `adapters/codex/plugin/grill-me/`
- `adapters/codex/conformance.yaml`
- `adapters/codex/rule-mapping.yaml`
- `adapters/codex/migration-inventory.yaml`
- `tests/codex/test_adapter.py`
- `tests/release/`
- `docs/guides/codex.zh-TW.md`
- `docs/guides/generic.zh-TW.md`
- `dist/`

## Test-first exceptions

Human documentation prose used the Approved Plan's documentation exception. Deterministic headings, language order, paths, lifecycle terms, provider boundaries, and links received failing automated checks before the documents were changed. Human comparison against the Approved Specification and current official Codex Plugin documentation supplied the alternative verification for prose accuracy.

## Residual risks and deferred work

- Prompt and Skill contracts cannot guarantee identical reasoning quality across every model version.
- Generic users remain responsible for saving and re-supplying cross-session Artifacts.
- A Codex installation still requires an authorized configured marketplace; this release does not create one.
- The final Plugin was validated but not installed into a personal Codex environment.
- SHA-256 verifies integrity but is not publisher signing or provenance.
- Public licensing, signing, marketplace publication, external upload, and additional provider-specific adapters remain deferred.
- The workspace is not a Git repository, so Git diff/status evidence is unavailable.

## Handoff

Release `2.1.0` is complete under `dist/` and ready for local inspection or a separately authorized installation or publication workflow. Generated output may be deleted and rebuilt from canonical source. Any personal installation, marketplace creation or mutation, signing, or publication requires separate explicit authorization.
