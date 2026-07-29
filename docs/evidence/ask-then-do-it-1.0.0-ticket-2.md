# Ask Then Do It 1.0.0 Ticket 2 Evidence

Artifact type: Implementation Evidence

Artifact ID: `ask-then-do-it-1-0-ticket-2`

Workflow ID: `ask-then-do-it-1-0`

Ticket: 2 — Let a Codex user install and invoke the renamed Plugin

Status: Completed

Date: 2026-07-29

## Scope completed

- Renamed the Codex Plugin root to `ask-then-do-it`.
- Renamed the primary and two requirement Skills to `ask-then-do-it`, `ask-requirements`, and `ask-with-docs`.
- Updated Skill folders, frontmatter, UI metadata, default prompts, Core/Codex routing references, conformance evidence, rule mapping, release contract, and Codex guide.
- Updated the Plugin manifest to the approved product and author identity, with an independent-project and non-endorsement disclosure.
- Added the concise independent-project notice to the packaged Codex start guide.
- Updated the deterministic Codex builder to copy canonical `LICENSE` and `THIRD_PARTY_NOTICES.md` into the package and ZIP root.
- Added focused identity, routing, package inventory, guide, and legal byte-equivalence tests.

## Red evidence

Command:

```powershell
& 'C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.codex.test_ask_then_do_it_codex_identity -v
```

Result before implementation: `FAILED (failures=4, errors=1)`.

- The `adapters/codex/plugin/ask-then-do-it/` root did not exist.
- The three renamed Skill folders and metadata did not exist.
- The orchestrator could not be read at the approved new location.
- The old Plugin inventory did not satisfy the new identity contract.

During implementation, an isolated build also failed with `Plugin displayName must match release display_name`; the release display name and manifest display name were then made identical.

## Green evidence

Focused tests:

```powershell
& 'C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.codex.test_ask_then_do_it_codex_identity -v
```

Result: `Ran 4 tests ... OK`.

Official validation after the user approved installing `PyYAML 6.0.3` into the bundled validation runtime:

```powershell
python scripts/build_release.py --package codex --output-root ticket2-validation --allow-test-output-root
python quick_validate.py <each canonical Skill>
python quick_validate.py <each packaged Skill>
python validate_plugin.py adapters/codex/plugin/ask-then-do-it
python validate_plugin.py ticket2-validation/codex/ask-then-do-it
```

Results:

- Isolated Codex release build succeeded.
- All 8 canonical Skills reported `Skill is valid!`.
- All 8 packaged Skills reported `Skill is valid!`.
- Canonical Plugin validation passed.
- Packaged Plugin validation passed.
- Focused package test proved both legal files are byte-identical in the package directory and ZIP.

## Boundary confirmation

The isolated `ticket2-validation/` build output was removed after verification. No personal Plugin installation, marketplace change, publication, upload, or external release was performed.
