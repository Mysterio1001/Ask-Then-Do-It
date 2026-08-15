# Ask Then Do It 1.3.0 Package-Link Correction Review

Artifact type: Review Report

Artifact ID: `lite-workflow-mode-1-3-package-link-correction-review`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Status: Complete - No Actionable Findings

Review label: `independent`

Approved implementation mode: `tdd`

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md); Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), limited to Tickets 5, 7, and 8; original F1 in the Draft [release architecture diagnosis](ask-then-do-it-1.3.0-release-architecture-diagnosis.md); the user-approved correction target; current relevant final diff and surrounding code; the six Codex/Generic package `START-HERE` sources; `tests/release/test_documentation.py`; `tests/release/test_release_1_3_contract.py`; current expanded `dist/` trees, ZIPs, and `dist/checksums.sha256`; and raw verification executed by this reviewer.

Assumptions: The inspected worktree is the final correction candidate. The approved link root is exactly `https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides/`. Filesystem modification times are used only as local chronology evidence, not as a cryptographic before/after record.

Deferred: Remote URL dereference, Git tag existence, push, GitHub Release publication, upload, installation, and announcement remain deferred. This is the F1 correction Review, not the Ticket 8 final release Review.

Handoff: Return this independent no-finding result to the parent workflow so the F1 correction can close and Tickets 5 and 7 can complete their required revalidation before Ticket 8 resumes.

## Findings

No actionable findings at P0, P1, P2, or P3.

## Requirement and Artifact Verification

All 12 repository-root guide links in the six package entry sources have been replaced by exact, tag-pinned URLs. Each source contains exactly two applicable guide links and no source, expanded package entry, or corresponding ZIP entry retains a Markdown destination beginning `/docs/guides`.

| Host | Locale | Host guide | Complete workflow guide | Result |
| --- | --- | --- | --- | --- |
| Codex | `en` | `.../blob/v1.3.0/docs/guides/codex.en.md` | `.../blob/v1.3.0/docs/guides/getting-started-simple.en.md` | Exact |
| Codex | `ja` | `.../blob/v1.3.0/docs/guides/codex.ja.md` | `.../blob/v1.3.0/docs/guides/getting-started-simple.ja.md` | Exact |
| Codex | `zh-TW` | `.../blob/v1.3.0/docs/guides/codex.zh-TW.md` | `.../blob/v1.3.0/docs/guides/getting-started-simple.zh-TW.md` | Exact |
| Generic | `en` | `.../blob/v1.3.0/docs/guides/generic.en.md` | `.../blob/v1.3.0/docs/guides/getting-started-simple.en.md` | Exact |
| Generic | `ja` | `.../blob/v1.3.0/docs/guides/generic.ja.md` | `.../blob/v1.3.0/docs/guides/getting-started-simple.ja.md` | Exact |
| Generic | `zh-TW` | `.../blob/v1.3.0/docs/guides/generic.zh-TW.md` | `.../blob/v1.3.0/docs/guides/getting-started-simple.zh-TW.md` | Exact |

The Codex links are at lines 40 and 54 of each localized Plugin source. The Generic links are at lines 15 and 19 of each localized release source. This preserves the Specification's concise-entry ownership while resolving F1 without adding canonical guides to either package.

The six source files are byte-identical to their expanded `dist/` copies. The Codex expanded tree has 27 files and its ZIP has the same 27 files with zero byte mismatches; the Generic expanded tree and ZIP likewise agree on 18 files with zero byte mismatches. Builder validation accepted the current managed output set as `['codex', 'generic', 'checksums.sha256']`.

Recorded and observed archive hashes agree:

- Codex: `f3c5ce1e7f48baf5ac619d1719313ca3d91cc1c96af38b67ba4b23aba16bfbd3`
- Generic: `df66b786a8ef855cea9d709f350e5abf3fa943fc61cbe8b903712c7e4e240f6b`

The correction-specific local chronology is consistent with the approved boundary. F1 was written at `2026-08-15T13:54:05Z`; the two test files were written at approximately `13:59Z`, the six package sources at approximately `14:01Z`, and the rebuilt checksum at `14:01:31Z`. `README.md` predates F1 at `13:12:17Z`, while all three canonical `getting-started-simple` guides predate it at approximately `02:50Z`. No correction-era write to those four documents was observed.

The historical preservation test recalculated and accepted the fixed SHA-256 values for all 16 named `1.2.0` requirement, specification, plan, Ticket, Review, and release evidence artifacts.

## Test Evaluation

Raw command:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.release.test_documentation tests.release.test_release_1_3_contract -v
```

Observed result: `32` tests ran in `1.683s`; all passed.

`test_documentation.py` defines the exact versioned root and checks the expected host and locale pair in every package source. `test_release_1_3_contract.py` repeats that contract against clean built packages, rejects the original `](/docs/guides/` failure form, performs two byte-reproducible builds, compares expanded trees with ZIP inventories and bytes, validates checksums, and protects historical `1.2.0` hashes. A direct replacement with the wrong tag, host, or locale therefore fails focused coverage, and a stale original F1 link fails package coverage.

The approved `tdd` mode is preserved. Current Green and test-before-source file chronology were observed. Raw Red output was not among the authorized independent-review inputs, so valid Red remains an evidence gap rather than a code finding.

## Twelve-Lens Review

This is a change-focused pass, not a system-wide architecture diagnosis.

| Lens | Outcome | Evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `no-finding` | The 12 literals form the required two-host, three-locale projection. Shared expected roots in the two focused test modules and exact matrix checks keep the duplication bounded and observable. |
| 2. Long Function | `no-finding` | The affected documentation test remains a single matrix-oriented contract; the correction adds no mixed production behavior. |
| 3. Large Module or Class | `no-finding` | The correction adds only package-link assertions to the existing release-documentation responsibility and does not introduce a new responsibility boundary. |
| 4. Long Parameter List | `not-applicable` | The correction introduces no callable production interface or parameter list. |
| 5. Data Clumps | `no-finding` | Host, locale, and guide path are represented together in explicit mappings where that relationship is the tested domain contract. |
| 6. Primitive Obsession | `no-finding` | Exact URL strings are the user-visible artifact under test; constraining them as literal values is appropriate here. |
| 7. Feature Envy | `not-applicable` | No behavior was moved across object or module ownership; release tests inspect the documents and packages they own. |
| 8. Divergent Change | `no-finding` | The correction remains within package entry navigation and its focused release contracts. |
| 9. Shotgun Surgery | `no-finding` | Six localized host sources are an approved ownership matrix, while expanded trees, ZIPs, and checksums are generated deterministically rather than hand-maintained. |
| 10. Message Chains | `not-applicable` | No navigation or call chain was added by this static-document correction. |
| 11. Leaky Abstraction | `no-finding` | The former package-to-repository-root leak is removed; distributed entry pages now expose explicit version-bound external targets. |
| 12. Shallow Module | `not-applicable` | The correction adds no new module or abstraction. |

## Verification Gaps and Residual Risks

- The cumulative worktree diff starts before this correction. There is no correction-start content snapshot or hash for `README.md` and the canonical guides, so their byte-for-byte before/after identity cannot be cryptographically proven from the authorized inputs. The observed timestamps strongly support that the correction did not write them.
- The focused tests assert every required URL and reject the exact original root-relative form, but they do not assert the complete set or count of all absolute guide links. The independent artifact audit closes that gap for the current candidate by confirming exactly two expected links in each of all 18 source, expanded, and ZIP entry documents. A future added extra absolute guide link is a low residual regression risk.
- The version-pinned URLs were intentionally not dereferenced. They become user-valid only when the `v1.3.0` tag and repository content are externally available; that publication state remains deferred.
- Raw TDD Red output was unavailable to this isolated reviewer.

## Completion Assessment

The approved F1 package-link correction appears complete. The exact 12-link mapping, both generated package trees, both ZIPs, checksums, focused regression coverage, and historical `1.2.0` preservation all pass with no unresolved correction finding. This assessment does not claim Ticket 8 release completion or external publication.
