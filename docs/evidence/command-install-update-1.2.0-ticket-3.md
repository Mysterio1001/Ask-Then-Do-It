# Ask Then Do It 1.2.0 Ticket 3 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `command-install-update-1-2-ticket-3-evidence`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Status: Completed

Inputs: Approved [1.2.0 Specification](../specs/command-install-update-1.2.0.md), Approved [Ticket Plan](../plans/command-install-update-1.2.0.md), Tickets 1-2 output, and Ticket 3 (approved `tdd` mode).

Assumptions: README's existing absolute `/START-HERE.*` links and historical documentation assertions are outside the approved README change boundary; this Ticket validates the six changed guides and the exact README whitelist independently.

Deferred: Lockstep release version migration, generated packages/checksums, final release evidence, independent Review, and architecture diagnosis.

Handoff: Ticket 4 after Ticket 3 Review.

## Outcome

Added equivalent English, Traditional Chinese, and Japanese AI-first installation/update instructions to the canonical Plugin start guides and Codex guides. The flow inspects marketplace and Plugin state, writes only for an explicit install/update request, stops on uncertainty or failure, avoids automatic downgrade and alternate sources, supports ZIP fallback, and starts a new Codex task after success. README changes are limited to the approved six download entries and three localized insertions before the existing More information markers.

## Changed files

- `README.md`
- `adapters/codex/plugin/ask-then-do-it/START-HERE.en.md`
- `adapters/codex/plugin/ask-then-do-it/START-HERE.zh-TW.md`
- `adapters/codex/plugin/ask-then-do-it/START-HERE.ja.md`
- `docs/guides/codex.en.md`
- `docs/guides/codex.zh-TW.md`
- `docs/guides/codex.ja.md`
- `tests/release/test_command_install_docs.py`

## Red evidence

Command:

`C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest tests.release.test_command_install_docs`

Observed before documentation changes: `Ran 3 tests`; `FAILED (failures=10)`. The expected missing behaviors were absent marketplace add/upgrade and Plugin add command coverage, missing localized README sections, and the README whitelist mismatch.

## Focused Green evidence

After the localized guides, README sections, version links, and the relative-link assertion were added, the command observed: `Ran 4 tests`; `OK`.

## Refactor and broader verification

The same command was rerun after removing the literal unsupported install alias from user-facing documentation while retaining the validator's forbidden-command assertion; it observed `Ran 4 tests`; `OK`.

The existing `tests.release.test_documentation` module was also run. It remains non-green because it contains pre-existing historical/mojibake expectations for old localized text and `1.1.0` README links, plus an existing absolute `/START-HERE.*` link resolution assumption. Those unrelated assertions were not changed because the approved README boundary forbids rewriting existing content.

`git diff --check` passed with no whitespace errors.

## Residual risks

The target Codex CLI was unavailable for live command execution. Full release documentation tests need a later test-contract migration for historical expectations; Ticket 4 owns current-version test updates while preserving historical artifacts.
