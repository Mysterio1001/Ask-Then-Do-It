# Ask Then Do It 1.2.0 Ticket 4 Implementation Evidence

Artifact type: Implementation Evidence

Artifact ID: `command-install-update-1-2-ticket-4-evidence`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Status: Completed

Inputs: Approved [1.2.0 Specification](../specs/command-install-update-1.2.0.md), Approved [Ticket Plan](../plans/command-install-update-1.2.0.md), completed Tickets 1-3, and Ticket 4 with Approved mode `tdd`.

Assumptions: `dist/` is generated output. A complete, checksum-verified prior release is safe for the builder to replace atomically; unmanaged or incomplete output remains a hard failure.

Deferred: Git tag, GitHub Release, push, upload, Plugin installation, personal marketplace mutation, announcement, and live target-CLI verification.

Handoff: Ticket 4 Review, then Ticket 5 integrated validation.

## Outcome

Moved all active Core, Codex, Generic, Plugin, release, current-guide, package, test, and archive declarations to `1.2.0`. The release builder now validates the repository marketplace against `v{release_version}`, validates and packages both transparent assets, excludes marketplace metadata from consumer packages, and can atomically replace a complete verified prior release. Codex and Generic packages were rebuilt in `dist/` with matching checksums.

## Red evidence

1. `...python.exe -m unittest tests.release.test_release_1_2_contract` observed `Ran 2 tests` and `FAILED (failures=2)`: `release/release.json` still declared `1.1.0`, and the `1.2.0` archives did not exist.
2. The new marketplace drift case observed `ERROR`: `build_release.py` had no `MARKETPLACE_CATALOG` integration point.
3. `...python.exe -m unittest tests.release.test_release_safety.ReleaseSafetyTests.test_complete_verified_prior_release_can_be_upgraded_atomically` observed `FAILED (failures=1)`: a verified `1.1.0` output was rejected because its checksum inventory did not name `1.2.0` archives.

All failures were for the intended missing behavior, not setup errors.

## Green and refactor evidence

- `...python.exe -m unittest tests.release.test_release_1_2_contract`: `Ran 3 tests`; `OK`.
- `...python.exe -m unittest tests.release.test_release_safety`: `Ran 6 tests`; `OK`.
- `...python.exe -m unittest discover -s tests\\release -t . -p test_*.py`: `Ran 66 tests`; `OK`.
- `...python.exe scripts\\build_release.py`: `Built codex, generic release 1.2.0`.
- `git diff --check`: exit code `0`; only Windows line-ending notices were emitted.

The existing-output refactor verifies exact managed roots, one directory and ZIP per provider, SHA-256 inventory, ZIP/directory byte equivalence, and absence of symlinks before replacement. Existing unmanaged-collision and failed-rebuild preservation tests remain green.

## Package evidence

`dist/checksums.sha256` contains exactly:

```text
c5b19837336ba1ac54407a1d0878a1d552921ba45e4e9adafcf0c1a2013048f2  codex/ask-then-do-it-1.2.0.zip
b9b27fafddd80f60b4e2818f3d61757146973d41bee345a65d00ef1b18e99af0  generic/ask-then-do-it-generic-1.2.0.zip
```

Automated inventory checks prove the Codex directory and ZIP contain `assets/icon.png` and `assets/logo.png`; Codex excludes `.agents/plugins/marketplace.json`; Generic excludes both Plugin assets and marketplace metadata. Two isolated builds are byte-identical and both ZIPs match their unpacked directories.

## Residual risk

The target Codex CLI could not be executed live. Local package and marketplace contracts are fully validated, but actual GitHub tag publication and target-CLI installation remain maintainer-controlled work.
