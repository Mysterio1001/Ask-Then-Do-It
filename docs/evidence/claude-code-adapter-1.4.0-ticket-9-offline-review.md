# Claude Code Adapter 1.4.0 Ticket 9 Offline Review

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-9-offline-review`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Approved Ticket mode: `tdd`

Review label: `independent`

Status: Accepted after focused correction re-review — no unresolved actionable offline finding. Full Ticket 9 remains pending.

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md) package/inventory requirements; Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 9 and 2026-09-09 offline-first authority; final `scripts/build_release.py` diff and surrounding transaction code; `scripts/validate_claude_package.py`; `tests/claude/test_release_preview.py`; current release declarations; raw command/result portions of [Ticket 9 offline evidence](claude-code-adapter-1.4.0-ticket-9-offline.md); independent probes below.

Assumptions: This reviewer did not implement Ticket 9 and inspected code/tests/specification before deriving findings. Review is limited to offline package preparation and the shared builder's affected boundaries; it does not approve activation or full Ticket 9 completion. Current-operation Full fallback, multi_agent capability and Approved `tdd` mode were supplied by the coordinator.

Deferred: Formal three-family lockstep activation; canonical Claude conformance; behavior/context/host/live-smoke gates; final package documentation acceptance; complete repository rerun. No default `dist/`, source, test, release configuration, installation or publication mutation was performed in this Review. Probe writes were limited to temporary synthetic fixtures.

Handoff: The single ZIP finding is closed by the focused re-review below. Central integration may use the corrected offline builder. Actual release activation and full Ticket 9 completion remain pending their required gates.

## Finding

### Closed [P2] ZIP equivalence ignored directory entries and non-regular/deterministic metadata

At `scripts/build_release.py:505-519`, `verify_zip_equivalence` removes every member whose name ends in `/` before comparing the ZIP to the expanded tree, then checks only each expected member's decompressed bytes. Starting from a correct synthetic Claude preview, appending either `unexpected-empty-directory/` or `../outside/` and updating its checksum passes `validate_output_set(... require_source_equivalence=True)`; the ordinary extra directory also passes `validate_existing_output_set`. Changing an existing entry's Unix file mode to symlink (`0o120777`) or its timestamp to 2020 also passes with unchanged path/content. The generator at `:482-490` emits only regular files with fixed timestamp, creator and compression, but the validator does not enforce those guarantees. Consequently a nonconforming extraction inventory or non-regular archive can be accepted as source-equivalent/managed output, contradicting the Specification's exact extraction inventory and deterministic ZIP contract. Compare the complete `ZipInfo` inventory, reject ungenerated directory/unsafe entries, and enforce the package's regular-file and deterministic metadata policy while preserving valid prior-release compatibility. The existing duplicate-member, expanded-tree link, source parity and checksum guards do not catch these probes.

## Independent verification

Read-only current declaration check:

```text
git diff --exit-code -- release/release.json core adapters/codex/conformance.yaml adapters/generic-prompts/manifest.yaml dist
```

Exit `0`, no diff output. Current release/Core/Codex/Generic identities remain `1.3.1`; canonical Claude conformance remains unactivated. The new preview mode requires an explicit test-output flag and rejects output in or around default `dist/`, tracked source/config trees and link ancestors. No review probe invoked a build against default `dist/`.

The reviewer used the existing temporary synthetic preview fixture to make ZIP-only mutations, recalculate the checksum and call the public validation functions. Raw observed outcomes:

```text
unexpected ZIP directory: ACCEPTED
unexpected ZIP directory prior-output ownership: ACCEPTED
symlink-mode: ACCEPTED
noncanonical-timestamp: ACCEPTED
unsafe-directory: ACCEPTED
```

The directory probes appended `unexpected-empty-directory/` and `../outside/`. The metadata probes changed only the first existing entry to Unix symlink mode or timestamp `(2020,1,1,0,0,0)`. Runtime and legal source bytes remained the synthetic fixture's exact bytes. Both Python probe invocations exited `0`, confirming the missing rejection without any live Claude or external action.

An additional independent probe injected a candidate marker placement failure followed by prior Claude-family restoration failure, through the shared `replace_managed_path` boundary. Raw result:

```text
incomplete recovery exit: 1
incomplete recovery disclosure: True
preserved staging: 1
prior Claude backup preserved: True
```

The outer probe exited `0` after checking those observations. This confirms that the preview path retains the existing incomplete-recovery behavior rather than deleting the remaining backup. Temporary fixture cleanup occurred only after observing the preserved transaction data.

The implementer's raw evidence records the initial preview-option Red, a later duplicate-member/provider-inventory Red and a 43-test focused/current-release Green. This reviewer inspected those raw summaries and did not redundantly rerun that full set. The exact-runtime/legal inventory, source byte parity, deterministic build routine, explicit preview marker, current configuration boundary, transaction reuse and existing tests were reviewed in source.

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — finding.** ZIP generation defines deterministic regular-file metadata while validation separately omits those constraints; this contributes to the finding above.
2. **Long Function — no-finding.** The changed builder branches are bounded dispatch/validation additions; existing transaction flow remains localized.
3. **Large Module or Class — no-finding.** Builder remains the existing package transaction owner, with Claude inventory/parity extracted into a focused helper.
4. **Long Parameter List — no-finding.** Added helpers take existing configuration/root concepts and do not expose an unstable coordination interface.
5. **Data Clumps — no-finding.** Claude source/runtime/legal inventory is grouped in one helper; preview marker binds its bytes as a single manifest.
6. **Primitive Obsession — finding.** ZIP members are reduced to filename strings, dropping entry type and deterministic metadata needed by the package contract; the same P2 finding covers it.
7. **Feature Envy — no-finding.** The builder delegates Claude payload inventory/parity to its provider helper and retains shared transaction ownership.
8. **Divergent Change — no-finding.** Changes add one provider and isolated preview behavior without unrelated release policy edits.
9. **Shotgun Surgery — no-finding.** Claude runtime inventory has one production owner; the independent test inventory intentionally supplies an external expectation.
10. **Message Chains — not-applicable.** The reviewed code uses local file/config helpers, not a chain of nested domain-object navigation.
11. **Leaky Abstraction — finding.** The equivalence helper's name/consumers imply package equivalence, but directory/type/metadata changes pass; the single P2 finding is the actionable boundary repair.
12. **Shallow Module — no-finding.** The provider helper hides real exact-tree, source identity and parity checks. ZIP validation has the specific missing boundary above, not a reason for a broad architectural refactor.

## Completion assessment and residual limits

Offline preview preparation largely follows the approved scope: current identities and default outputs remain unchanged; synthetic preview packaging is labeled non-release; runtime/legal bytes and shared rollback are covered. One actionable ZIP validation gap remains, so this correction is not yet accepted. Even after correction, no actual host/model/context/live-smoke evidence has been reviewed here, and full Ticket 9 activation/completion must remain pending.

## Focused correction re-review

The preceding finding and assessment describe the initial reviewed bytes. After the implementer observed Red for extra directory, traversal directory, symlink, timestamp and compression mutations, this reviewer inspected the corrected `verify_zip_equivalence` and its two callers. It now requires an exact sorted complete member inventory, rejects duplicate/directory/special-file/encrypted entries, and validates canonical timestamps, creator, regular-file mode, compression, flags, attributes, comments and extras for newly staged packages and all Claude packages. Existing Codex/Generic prior releases use the explicit `canonical_metadata=False` path, retaining legacy timestamps/compression while still rejecting unsafe types and wrong inventory.

Independent rerun of five mutations, each at both candidate validation and prior-preview ownership validation, produced:

```text
extra-directory candidate: REJECTED ZIP inventory differs from directory for ask-then-do-it-claude-1.4.0-preview.zip
extra-directory prior-preview: REJECTED ZIP inventory differs from directory for ask-then-do-it-claude-1.4.0-preview.zip
unsafe-directory candidate: REJECTED ZIP inventory differs from directory for ask-then-do-it-claude-1.4.0-preview.zip
unsafe-directory prior-preview: REJECTED ZIP inventory differs from directory for ask-then-do-it-claude-1.4.0-preview.zip
symlink-mode candidate: REJECTED ZIP member is not a safe regular file
symlink-mode prior-preview: REJECTED ZIP member is not a safe regular file
noncanonical-timestamp candidate: REJECTED ZIP member metadata is not canonical
noncanonical-timestamp prior-preview: REJECTED ZIP member metadata is not canonical
noncanonical-compression candidate: REJECTED ZIP member metadata is not canonical
noncanonical-compression prior-preview: REJECTED ZIP member metadata is not canonical
```

Probe exit `0`; every candidate began with a successfully built synthetic preview, and checksums were recomputed so the rejection tested the intended inventory/metadata boundary. Source/test code was not changed by this reviewer.

The reviewer also loaded the current release configuration and called `validate_existing_output_set` read-only against the existing default `dist/` (no build or write):

```text
Existing default dist validated read-only: ['codex', 'generic', 'checksums.sha256']
Current release identity: 1.3.1 1.3.1
```

Exit `0`. This provides direct compatibility evidence for the existing current managed outputs. The implementer's final 44-test Green is additional raw evidence; it was not redundantly rerun here.

The initial architecture lens findings (Duplicated Code or Policy, Primitive Obsession and Leaky Abstraction) are resolved by this same explicit ZIP boundary and have no remaining actionable finding in this focused scope. Other lens assessments remain unchanged. Verdict: **Accepted for offline preparation**, with no unresolved actionable finding. This does not approve actual behavior/context/host/live smoke or full Ticket 9 release activation/completion.
