# Ticket 5 Independent Review Report

Artifact type: Review Report

Artifact ID: `lite-workflow-mode-1-3-ticket-5-review`

Workflow ID: `lite-workflow-mode`

Review workflow core version: `1.1.0`

Product core version: `1.2.0`

Ticket: `5 - Align host guides, short entry points, and README`

Implementation mode: `tdd`

Review label: `independent`

Status: `changes-requested`

Independence: This fresh reviewer context did not implement Ticket 5 and rebuilt its view from approved artifacts, runtime and documentation contracts, the final Ticket-owned diff, surrounding documents and tests, and raw verification results. The Ticket 5 Implementation Evidence was deliberately not read.

## Findings

### P2 - Mode-enabled entry instructions still present Full-only startup behavior as universal

Trigger: a user starts an operation resolved to Lite, especially one with no blocking question or one that first requires a high-risk mode decision. The three Codex guides still say, in an unqualified `First use` section, that the AI asks one question at a time and uses three approval gates (`docs/guides/codex.en.md:103-121`, `docs/guides/codex.zh-TW.md:103-121`, and `docs/guides/codex.ja.md:92-102`). The three Generic guides make the same unqualified first-question promise before their mode section (`docs/guides/generic.en.md:16-32`, `docs/guides/generic.zh-TW.md:16-32`, and `docs/guides/generic.ja.md:16-32`), and all three packaged Generic short entry pages repeat it at line 13 (`release/generic/START-HERE.en.md`, `.zh-TW.md`, and `.ja.md`). Lite may instead ask up to three blockers, present a Change Brief immediately, or pause for the high-risk Full/Lite decision, and it has one formal pre-implementation approval. The current text therefore gives Lite users an incorrect startup and approval contract and undermines the approved Full/Lite separation. Scope the one-question/three-gate material explicitly to Full or replace the general startup sentence with mode-neutral routing text; keep the Generic START pages short, and add a regression assertion that Full-only startup claims cannot appear outside a Full-scoped section. The passing focused and full documentation suites demonstrate that current tests do not detect this defect.

Affected locations:

- `docs/guides/codex.en.md:103`
- `docs/guides/codex.zh-TW.md:103`
- `docs/guides/codex.ja.md:92`
- `docs/guides/generic.en.md:16`
- `docs/guides/generic.zh-TW.md:16`
- `docs/guides/generic.ja.md:16`
- `release/generic/START-HERE.en.md:13`
- `release/generic/START-HERE.zh-TW.md:13`
- `release/generic/START-HERE.ja.md:13`
- `tests/release/test_documentation.py:95`
- `tests/release/test_documentation.py:486`
- `tests/release/test_documentation.py:579`

## Completion Assessment

The Approved Ticket does not yet appear complete because the P2 finding leaves nine user-facing documents inconsistent with the selected Lite lifecycle. No other actionable finding was identified in the reviewed Ticket 5 scope.

README satisfies the approved three-language structure and preservation boundary: each locale is ordered Introduction, Quick Start, exact Automatic installation heading, nested `#### Codex CLI`, Manual installation, then Read more. The Traditional Chinese heading is exactly `### 自動安裝 ( CLI )`. The preserved commands, links, manual installation text, and Read more blocks are unchanged apart from version-normalization allowance, and all Ticket 5 user-facing version references remain at `1.2.0` for Ticket 7 ownership.

The Codex mode sections correctly document both Config paths and Full/Lite TOML examples; explicit instruction over project Config over user Config over Full; absent-project continuation versus present-invalid-project fail-closed behavior; explicit override over invalid Config; read-only resolution with no repair or persistence; new-session resolution; and the canonical high-risk guide link. The Generic mode sections correctly document the declaration, explicit override, Full fallback, no Codex Config access, host capability limits, new-session declaration behavior, and the canonical guide link. Apart from the finding, the nine START pages remain concise, retain usable installation or startup steps, and hand off detail to the owned guides rather than duplicating the full flow.

## Verification

Observed checks:

- Focused Ticket 5 documentation contract run: 6 tests, passed.
- `python -m unittest tests.release.test_documentation`: 22 tests, passed.
- `python -m unittest tests.release.test_command_install_docs`: 5 tests, passed.
- Focused relative-link run from both documentation modules: 2 tests, passed.
- `git diff --check HEAD -- <18 Ticket 5 paths>`: passed; Git emitted only expected LF-to-CRLF working-copy warnings.
- Ticket-owned diff inspection: 18 changed paths, all within README, the six host guides, nine START pages, and the two approved documentation test modules.
- README preservation audit: independently derived all ten normalized preamble/Automatic/Manual/Read-more SHA-256 values from `HEAD:README.md`; every value matches `README_PRESERVED_DIGESTS`. The guard is HEAD-independent at runtime and the constants were not changed to accept unrelated README churn.
- Version audit over Ticket 5 documents: no `1.3.0` declaration; current public references remain `1.2.0`.
- Manual three-language semantic comparison against the Ticket 2 Codex runtime, Ticket 3 Generic runtime, and Ticket 4 canonical guide: completed; the finding above is the only divergence found.

Evidence unavailable or deferred:

- Ticket 5 Implementation Evidence was intentionally unavailable to this review.
- External HTTP availability of release downloads and external documentation was not exercised; local relative links were resolved.
- Generated `dist/`, checksums, and the `1.3.0` release identity are Ticket 7 ownership and were not reviewed as Ticket 5 outputs.
- Model behavior outside the reviewed written contracts remains unverified.

Residual risk after the finding is corrected is primarily localization drift: exact-token tests prove required phrases, but they cannot prove every future translation is semantically equivalent without another human semantic pass.

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy - `finding`.** The Full startup policy is repeated across the six host guides and three Generic entry pages and has drifted from the new mode resolver. Trigger, impact, evidence, and affected locations are recorded in the P2 finding.
2. **Long Function - `no-finding`.** Ticket 5-specific test behavior is expressed as bounded locale maps and loops. The longer canonical-guide matrices belong to the already completed Ticket 4 dependency and do not obscure the reviewed host/entry assertions.
3. **Large Module or Class - `no-finding`.** `test_documentation.py` is large, but its changed surface has one cohesive responsibility: localized release-document contracts. No separate state or unrelated runtime responsibility was added by Ticket 5.
4. **Long Parameter List - `not-applicable`.** The reviewed change adds Markdown content and zero-argument `unittest` cases; it introduces no production or helper interface with a parameter list.
5. **Data Clumps - `no-finding`.** Locale-specific paths, headings, and semantic markers are grouped in explicit dictionaries instead of repeatedly traveling through ad hoc call sites.
6. **Primitive Obsession - `no-finding`.** Literal headings, commands, paths, and mode declarations are the public documentation contract and appropriately require exact string assertions.
7. **Feature Envy - `not-applicable`.** The reviewed Markdown and standalone assertion functions do not define collaborating objects or modules that reach into another owner's internal state.
8. **Divergent Change - `no-finding`.** Codex configuration, Generic configuration, canonical flow, short entry, and README responsibilities remain separated by document ownership; Ticket 5 does not add runtime or release-generation reasons to those files.
9. **Shotgun Surgery - `finding`.** The P2 finding shows that one mode-routing clarification must be corrected consistently in nine localized documents because the Full startup sentence was copied across host and package entry surfaces. The canonical-guide links reduce, but did not eliminate, this policy duplication.
10. **Message Chains - `not-applicable`.** No navigation, object, or call chain is introduced; links are direct and were resolved by the link checks.
11. **Leaky Abstraction - `no-finding`.** Host-specific guides intentionally expose only their owned configuration and capability contracts, while START pages hand complete lifecycle detail to the canonical guide. The finding is incorrect scoping, not hidden implementation leakage.
12. **Shallow Module - `not-applicable`.** The change introduces no new module API; documentation tests directly enforce user-visible contracts without an abstraction layer whose interface exceeds its value.

## Assumptions

- `git diff HEAD --` restricted to the Ticket 5 ownership list is the final review diff because the worktree contains changes from multiple Tickets.
- The Approved Specification and Approved Ticket Plan are authoritative when wording differs from historical `1.2.0` documents.
- Ticket 2, Ticket 3, and Ticket 4 current repository content is the dependency contract consumed by Ticket 5.

## Handoff

Return to the Ticket 5 implementer to correct the nine affected Full-only startup claims and add focused regression coverage without changing runtime behavior, README preserved content, versions, generated output, or other Ticket ownership. Rerun the focused cases, both complete documentation modules, relative-link checks, and Ticket-scoped `git diff --check`, then request a fresh independent review of the corrected final diff.
