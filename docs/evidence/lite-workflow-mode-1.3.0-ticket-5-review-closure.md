# Ticket 5 Closure Review - Host Guides, Entry Points, and README

Artifact type: Review Report

Artifact ID: `lite-workflow-mode-1-3-ticket-5-review-closure`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Product version: `1.2.0`

Implementation mode: `tdd`

Review label: `independent`

Status: Changes Requested

Reviewed inputs: Approved `lite-workflow-mode-1-3-spec`; Approved Ticket 5 in `docs/plans/lite-workflow-mode-1.3.0.md`; settled Ticket 2 Codex runtime; settled Ticket 3 Generic runtime; Ticket 4 canonical localized getting-started guides; the final scoped diff for the 16 Ticket 5 documents and two focused test modules; raw focused and dependency verification results.

Assumptions: The working tree inspected on 2026-08-15 is the final Ticket 5 candidate. Product `1.2.0` references remain current until Ticket 7 performs the separately planned lockstep `1.3.0` integration. Other Tickets' files and existing evidence artifacts are outside this Review except where the Approved Ticket names them as settled inputs.

Deferred: Generated `dist/` output, package inventories, checksums, external publication, external URL reachability, Ticket 7 version integration, and external CI.

Next handoff: Return the two findings to `$implement-tdd`; after focused Red/Green evidence and the relevant documentation suites pass, hand the final diff and raw results to a fresh `$review-code` context.

## Findings

### P2 - Generic continuation instructions still present Full-only persistence as mode-neutral

When a Lite user reaches `Save your progress` (or its localized equivalent), all three Generic guides instruct the user to save stage documents, paste them into a new conversation, and let the AI proceed to the first unfinished stage. That sequence is valid only for Full: Lite creates no workflow artifacts and a new session must reconstruct a new Change Brief rather than claim to resume approval, progress, or Review. The unscoped instructions therefore contradict the approved Lite session lifecycle and can cause users or hosts to treat non-durable Lite state as resumable. Scope this section explicitly to Full and state the corresponding Lite new-session behavior in all three locales. Add a regression assertion that checks this mode distinction rather than only the old first-question phrases. Evidence: `docs/guides/generic.en.md:73`, `docs/guides/generic.zh-TW.md:73`, `docs/guides/generic.ja.md:73`, and the incomplete guards in `tests/release/test_documentation.py:579` and `tests/release/test_documentation.py:665`.

### P2 - The Japanese Codex guide no longer identifies Full's three approval gates

The changed Japanese First Use section says only that Full has three approval points, then refers to the third approval; unlike the English and Traditional Chinese versions, it does not identify requirements consensus, Specification, and Ticket Plan. A Japanese Codex user therefore receives a materially weaker gate contract, and the locale is no longer semantically equivalent. Restore the three gate identities under the Full heading and strengthen the localized host-guide test to assert those identities in every locale, not merely the count phrase. Evidence: `docs/guides/codex.ja.md:104`; comparison locations `docs/guides/codex.en.md:117` and `docs/guides/codex.zh-TW.md:117`; permissive assertion at `tests/release/test_documentation.py:665`.

## Verification

- `python -m unittest tests.release.test_documentation tests.release.test_command_install_docs`: PASS, 29 tests (`24 + 5`). This includes the repository-wide relative-document-link check and focused Codex-guide link checks.
- `python -m unittest tests.codex.test_lite_workflow tests.generic.test_generic_lite_workflow tests.generic.test_generic_prompts`: PASS, 37 tests against the settled Ticket 2 and Ticket 3 runtime contracts.
- Scoped `git diff --check` for all 16 Ticket 5 documents and both test modules: PASS. Git emitted only its configured LF-to-CRLF working-copy warnings.
- README preservation audit against `HEAD`: PASS. The fixed preamble digest and all English, Traditional Chinese, and Japanese Automatic installation, Manual installation, and Read more digests match the historical baseline after release-version normalization.
- Final scoped status and diff inspection: the Ticket 5 candidate is limited to README, the nine START-HERE documents, six host guides, and the two approved documentation test modules. The README heading order is Introduction, Quick Start, Automatic installation (CLI), Codex CLI, Manual installation, then Read more in every locale.

Unavailable evidence: external CI and external HTTP-link availability were not observed. Generated packages and `1.3.0` release identity are intentionally unavailable at this Ticket because Ticket 7 owns them.

## Residual Risk and Completion Assessment

The passing suites prove the currently asserted literals, structure, links, and README-preservation hashes, but they do not reject the two semantic regressions above. No security, secret, authorization, privacy, or destructive-operation concern was found in this documentation-only change. Ticket 5 does not yet appear complete against the Approved Specification and Plan because both P2 findings affect required localized user behavior and their regression coverage.

## Twelve-Lens Review

1. **Duplicated Code or Policy**: `finding` - Full/Lite policy is repeated across localized host documents; the unscoped Generic continuation text and missing Japanese gate identities demonstrate two concrete divergence failures. Trigger, impact, evidence, and locations are Findings 1 and 2.
2. **Long Function**: `no-finding` - the changed test methods contain sizable locale tables, but each method exercises one named documentation contract and the failure scope remains traceable.
3. **Large Module or Class**: `no-finding` - `test_documentation.py` is large, but its reviewed additions remain cohesive around localized public-document contracts; no defect requires a module split.
4. **Long Parameter List**: `not-applicable` - the reviewed documentation and tests introduce no public or unstable multi-parameter interface.
5. **Data Clumps**: `no-finding` - locale markers are grouped in explicit per-contract dictionaries; no repeated loose value group caused a separate defect beyond the policy-divergence findings.
6. **Primitive Obsession**: `no-finding` - literal markers and SHA-256 digests are appropriate deterministic representations for documentation contracts and preserved README blocks.
7. **Feature Envy**: `not-applicable` - no changed behavior reaches through another module's state or ownership.
8. **Divergent Change**: `finding` - one mode-contract change requires coordinated edits across host, locale, entry-point, and test surfaces, and the two findings show that the coordination is incomplete. The affected scope is the localized Generic and Codex guide contracts cited above.
9. **Shotgun Surgery**: `finding` - the approved localization surface necessarily spans many documents; missing one locale detail and retaining one old cross-session paragraph changes user-visible semantics. Findings 1 and 2 are the actionable manifestations; no broader refactor is authorized by this Review.
10. **Message Chains**: `not-applicable` - no object navigation, call chain, or chained state access exists in the reviewed change.
11. **Leaky Abstraction**: `no-finding` - host-specific configuration remains in the Codex and Generic guides, while START-HERE files hand off to canonical guides without exposing runtime internals.
12. **Shallow Module**: `not-applicable` - the change adds no module interface whose coordination cost exceeds the behavior it hides.
