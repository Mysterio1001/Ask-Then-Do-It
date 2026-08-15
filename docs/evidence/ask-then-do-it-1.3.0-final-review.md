# Ask Then Do It 1.3.0 Final Independent Review

Artifact type: Review Report

Artifact ID: `ask-then-do-it-1-3-final-review`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Status: Completed - Changes Requested

Review label: `independent`

Reviewed inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), complete current working-tree diff and surrounding Core/Codex/Generic source and tests, current `dist/`, pending [validation ledger](ask-then-do-it-release-1.3.0.json), pending [release evidence](ask-then-do-it-release-1.3.0.md), [release architecture diagnosis after fix](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-fix.md), and raw verification rerun results.

Approved implementation mode: `tdd` for Tickets 1-8. Ticket 8 remains `In Progress` in the Approved Ticket Plan.

Independence: This fresh reviewer did not participate in implementation. `docs/evidence/lite-workflow-mode-1.3.0-ticket-8.md`, package-link implementation evidence, and other implementer conclusions were intentionally not read. A separate fresh runtime-contract audit was used as a second search path; every retained finding was then independently rechecked against the Approved Specification, current source, packaged output, tests, and surrounding guards.

Assumptions: The Specification's phrases "for each operation" and the user-defaults-to-Lite scenario apply to Codex operations that should be selected through normal Skill discovery, not only to requests that explicitly type `$ask-then-do-it`. Generated-file instructions are user-visible package contracts; documentation that tells a user to edit a generated file does not erase a contradictory `DO NOT EDIT` instruction inside that file. This is a local pre-publication review; canonical source remains authoritative and `dist/` is generated output.

Deferred: Source or test correction; package rebuild; evidence status changes; acceptance of architecture proposals F2-F4; external CI; additional operating systems; installed-Plugin and live third-party-model execution; remote guide-URL dereference; Git tag, GitHub Release, push, upload, installation, publication, and announcement.

Handoff: Return P1 to the Codex resolver/dispatch ownership of Ticket 2 and P2 to the Generic composition ownership of Ticket 3, using their Approved `tdd` mode. After focused independent Review, reintegrate and rebuild through Ticket 7 ownership, rerun Ticket 8's complete validation and architecture closure as applicable, then repeat a fresh final independent Review. The pending release evidence must remain `Review Pending`; no external publication is authorized.

## Findings

### [P1] Codex Config defaults do not reach the small operations Lite is intended to govern

Trigger: the Plugin is installed, a project or user Config selects `lite` (or relies on Full fallback), the user makes a trivial, fully specified, formatting-only, or single-line software change, and the user does not explicitly invoke `$ask-then-do-it`. The only Config resolver is inside `adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md:22`, but that Skill's discovery description at line 3 explicitly says not to invoke it implicitly for exactly those requests. There is no Plugin manifest hook, second resolver, or other always-on Config reader, and the packaged Skill is byte-identical. Even after loading, the legacy instruction at line 69 can send a resolved Full small change to an unnamed "lightweight path" instead of one of the two approved modes. The start guides' recommendation to type `$ask-then-do-it` mitigates only explicit use; it does not satisfy the approved persistent-default behavior. Consequently, a normal low-risk operation can bypass mode precedence, risk evaluation, the Lite Change Brief approval, no-new-test boundary, minimum validation, compact Review, and completion disclosure while all focused tests remain green because `tests/codex/test_lite_workflow.py:88` begins inside the already-loaded resolver. Broaden the dispatch contract or add an always-on resolver, remove or reconcile the legacy third path, and add a discovery-level regression that proves Config-selected Lite and Full fallback govern the excluded small-request classes.

### [P2] Generic's only editable default is shipped under a `DO NOT EDIT` instruction

Trigger: a Generic user follows `docs/guides/generic.en.md:42` (or either localized equivalent) and opens the extracted `generic-workflow.md` to set its embedded default. `scripts/build_release.py:572` emits `<!-- GENERATED FILE — DO NOT EDIT -->` as the first instruction, then emits the only `Default workflow mode: full` declaration at line 579 and calls it editable at line 584. The current packaged file reproduces the conflict at `dist/generic/ask-then-do-it-generic-1.3.0/generic-workflow.md:1` and line 8. A user who follows the file's first instruction cannot use the promised easily editable Generic default and is left with per-operation overrides; a rebuild also discards a direct edit. Existing coverage preserves rather than catches the contradiction: `tests/release/test_generic_release.py:147` requires the prohibition, while the Generic tests separately require the declaration. Qualify the generated banner with an explicit declaration exception or move the editable value to a user-owned input that composition preserves, then add a package-level test for the complete edit instruction rather than the two strings in isolation.

## Acceptance Review 1-22

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1 | `blocked` | Resolver fallback is correct once loaded, but P1 permits an implicit small Codex operation to run without selecting Full. |
| 2 | `blocked` | Project-over-user precedence is represented and tested inside the resolver; P1 leaves that resolver unreachable for excluded requests. |
| 3 | `passed` | An explicit current-operation selection makes the workflow applicable, wins without reading lower-priority Config, and performs no Config write. |
| 4 | `blocked` | Invalid Config fail-closed wording is complete when routed; the dispatch gap prevents a mode result for excluded operations. |
| 5 | `blocked` | Generic selection, explicit override, and invalid fallback are present, but P2 contradicts the required easily editable default declaration. |
| 6 | `passed within routed Full` | Core, Codex, and Generic retain the Full gates, artifacts, Ticket test choice, `tdd`/`direct` routes, Review lenses, and architecture route; Full regression passed. |
| 7 | `passed` | All three Lite contracts bound questions to three blockers, the approximate 500-token batch, three short sentences, one decision, recommendation, and tradeoff. |
| 8 | `passed` | Required Change Brief sections, three-to-five scenarios, approximate 800-token target, and honest-over-budget Full recommendation are present. |
| 9 | `passed` | Exactly one explicit complete-Brief approval precedes production modification. |
| 10 | `passed` | No Lite artifact type exists; all adapters prohibit workflow artifacts and cross-session resume claims. |
| 11 | `passed` | Pre-approval and mid-implementation risk pauses cover every required category and keep the decision current-operation-only. |
| 12 | `passed` | Lite scope, no behavioral-test edits, no TDD claim, and no speculative cleanup are explicit. |
| 13 | `passed` | Status/diff, applicable static checks, one success path, and one failure/boundary path are required with observed outcomes. |
| 14 | `passed` | Known applicable failures block an unqualified completion claim. |
| 15 | `passed` | Lite uses one compact same-agent, non-independent Review without a Full twelve-lens or Review-artifact requirement. |
| 16 | `passed` | Findings are batched, correction waits for approval, partial approval limits the subset, and material expansion returns to the user. |
| 17 | `passed` | Approximate 500-token completion includes delivery, changed areas, observed/unavailable validation, unresolved findings, and residual risk. |
| 18 | `passed` | The fixed Codex fixture and symmetric algorithm reran at Full `13,768`, Lite `5,356`, reduction `61.09%`; Generic fixed cost `13,313` is disclosed without a 60% or billing claim. |
| 19 | `passed` | README preserved the bounded three-language Introduction/Quick Start and installation/manual/read-more structure; preservation hashes and documentation tests passed. |
| 20 | `passed` | Canonical complete guides, host-specific guides, design ownership, and concise START-HERE entry points remain within their approved responsibilities. |
| 21 | `passed` | Traditional Chinese, English, and Japanese sources and packaged documents retain equivalent behavior and exact source/package copies; P2 is language-neutral and separately recorded. |
| 22 | `passed mechanically; release still blocked` | Identity, inventories, reproducibility, ZIP parity, checksums, conformance, historical hashes, and pending evidence agree on `1.3.0`; open P1/P2 prevent release completion. |

## Twelve Architecture and Refactoring Lenses

| Lens | Outcome | Evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `finding` | The after-fix architecture report already tracks F2: Full/Lite policy is manually projected across Core, both adapters, locales, fixtures, and tests. P2 is a concrete local drift between the builder banner and three localized Generic editing instructions. |
| 2. Long Function | `no-finding` | Changed executable paths are linear validation/composition routines with focused negative tests; no reviewed defect is triggered by function length. |
| 3. Large Module or Class | `finding` | Tracked architecture proposal F4 remains: `scripts/build_release.py` owns configuration, source validation, composition, archives, checksums, and output transactions, and the proxy imports its composer. The current package results are correct, so this remains non-blocking and unaccepted. |
| 4. Long Parameter List | `no-finding` | No changed public interface exposes excessive coordination parameters; builder, proxy, validator, and test helpers retain cohesive inputs. |
| 5. Data Clumps | `no-finding` | Mode sources, event contracts, package inventories, and evidence checks are grouped in explicit configuration structures rather than repeatedly travelling as loose values. |
| 6. Primitive Obsession | `finding` | Tracked proposal F3 remains: evidence IDs, statuses, commands, and outcomes are primitive self-declared strings in `scripts/validate_release_evidence.py`. Direct raw reruns support this candidate, but the validator itself is not execution-bound. |
| 7. Feature Envy | `no-finding` | Package tests inspect owned build outputs and the proxy delegates Generic composition to the owning builder; no changed behavior improperly reaches through another unit's data. |
| 8. Divergent Change | `finding` | Tracked F2/F4 remain: policy projections change for several reasons, and the builder changes for validation, composition, archive, and transaction concerns. No additional correctness finding beyond P1/P2 was found. |
| 9. Shotgun Surgery | `finding` | Tracked F2 remains: one mode change requires coordinated Core, Codex, Generic, locale, fixture, package, and evidence edits. Deterministic tests caught current byte drift but did not catch P1's discovery boundary or P2's contradictory instructions. |
| 10. Message Chains | `not-applicable` | The reviewed runtime is declarative Markdown, direct file/config reads, builder calls, ZIP entries, and checksums; no meaningful object-navigation chain exists in this scope. |
| 11. Leaky Abstraction | `finding` | P1 is a concrete leak: callers are promised a Config-selected mode but must know to invoke the resolver Skill explicitly to avoid its discovery exclusion. Tracked F3 separately leaves ledger provenance to external producers. |
| 12. Shallow Module | `finding` | Tracked F3 remains: the evidence validator exposes a completion gate but only validates declaration shape and status strings. P1 also shows the top-level resolver's broad interface is not backed by an equally broad dispatch boundary. |

The systemic F2-F4 concerns are already routed to the Draft after-fix Architecture Improvement Report and are not duplicated here as new refactor authority. P1 and P2 are bounded release-contract defects that should return to their owning Tickets.

## Verification Performed

- Final serial discovery with the candidate's Pillow dependency on `PYTHONPATH`: `177/177` passed in `14.379s`; `OK`.
- Release discovery: `104/104` passed in `13.548s`; Codex `23/23`, Generic `32/32`, and conformance `18/18` passed independently.
- Canonical and packaged validation: Skills `18/18`, Plugins `2/2`, marketplace CLI passed, and both conformance CLIs passed against Core `1.3.0`.
- Deterministic proxy rerun: Full `13,768`, Lite `5,356`, difference `8,412`, reduction `61.09%`; fixture fingerprint `0c7f08879883f04f85ba10cb2553e49e7cda83559c068d3e3df8ead155f4413f`; Generic fixed cost `13,313` with no applied gate.
- Current `dist/` audit: Codex directory/ZIP `27/27`, Generic `18/18`, zero duplicate, missing, extra, or byte-mismatched entries; canonical/package copies had zero byte mismatches.
- Independent SHA-256 recalculation matched `dist/checksums.sha256`: Codex `f3c5ce1e7f48baf5ac619d1719313ca3d91cc1c96af38b67ba4b23aba16bfbd3`; Generic `df66b786a8ef855cea9d709f350e5abf3fa943fc61cbe8b903712c7e4e240f6b`.
- Release tests exercised two clean byte-reproducible builds, exact inventories, ZIP equivalence, atomic replacement, evidence-gate missing/failed proxy rejection, documentation links, and all sixteen pinned historical `1.2.0` hashes.
- Active identity scan found no stale `1.2.0` declaration in active Core, adapters, release configuration, root entry files, active guides, or scripts outside deliberate historical/mutation assertions.
- `git diff --check` exited `0`; only informational LF-to-CRLF warnings were emitted. Review validation left the pre-report source/test/config/`dist/` diff unchanged.
- Running the evidence validator against the current candidate correctly failed only because the Markdown evidence is still `Status: Review Pending`; the gate must not be rerun as passing until fixes and a blocker-free repeated Review allow `Completed`.
- No local `v1.3.0` tag exists. No external publication action was executed or inferred.

## Candidate Ledger Accuracy

The observed counts, proxy fingerprint and arithmetic, Skill/Plugin/conformance results, inventories, reproducibility coverage, ZIP parity, archive hashes, historical preservation, and final serial result agree with the pending JSON/Markdown evidence. The disclosed concurrent Windows `WinError 5` was not reproduced in serial execution; the affected release behavior passed in the `104/104` release suite and final `177/177` run, so the candidate describes that event honestly rather than hiding a current assertion failure. The ledger does not claim final Review success, and the Markdown correctly remains `Review Pending`.

## Verification Gaps and Residual Risk

- Live installed-Plugin dispatch was not executed. P1 does not depend on that unavailable run: the packaged discovery description normatively excludes the triggering requests and no alternative resolver exists. A live regression remains necessary after correction.
- Ticket 8's original Red chronology was intentionally unavailable because its implementation evidence was excluded from this independent Review. Final Green behavior and the evidence-gate negative cases were rerun; any correction must establish fresh Red/Green evidence under the Approved `tdd` mode.
- Remote `v1.3.0` guide targets cannot be dereferenced until separately authorized publication creates the tag. Their local URL mapping is structurally correct; availability remains deferred.
- External CI, additional operating systems, installed marketplace behavior, live Codex/Generic model adherence, and sustained concurrent Windows stress were not exercised.
- Architecture proposals F2-F4 remain Draft, unaccepted, and non-blocking for the observed candidate. They authorize no refactor.
- No source, test, config, package, plan, candidate evidence, external system, or publication state was changed by this diagnostic Review.

## Completion Assessment

Ticket 8 and the local `1.3.0` release do not appear complete while P1 and P2 remain open. The mechanical validation matrix and pending ledger are internally accurate, but acceptance criteria 1, 2, 4, and 5 are not fully represented at the user-visible dispatch/configuration boundaries. Keep Ticket 8 `In Progress` and release evidence `Review Pending`; return the defects through their owning `tdd` Tickets, rebuild and revalidate generated packages and checksums, repeat architecture closure as applicable, and obtain a fresh blocker-free independent Review before any completion or publication claim.
