# Ask Then Do It 1.3.0 Direct-Entry Correction Independent Review

Artifact type: Review Report

Artifact ID: `lite-workflow-mode-1-3-direct-entry-correction-review`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Status: `changes-requested`

Review label: `independent`

Approved implementation mode: Ticket 8 `tdd` (user selected Add tests).

Reviewed inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md); Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), especially Ticket 8; the user-approved direct-entry correction contract; the prior changes-requested Review used only as raw trigger evidence; the current Core, Codex, Generic, localized-guide, test, release-configuration, expanded-package, ZIP, and checksum surfaces; and supplied plus independently rerun raw verification results.

Independence: This reviewer context did not implement the correction. Fresh read-only subreviews independently inspected the Codex and Generic entry matrices. Implementer defenses and correction evidence were not used to determine the verdict.

Assumptions: Core is normative; `bootstrap.md` and `orchestration.md` retaining mode-resolution ownership is a behavioral ownership contract; an inlined resolver in a non-owner stage is not delegation unless Core explicitly permits that projection; canonical source remains authoritative and `dist/` is generated release output.

Deferred: A product decision between canonical delegation and an explicitly permitted inlined Generic guard; correction implementation; release-ledger and existing-evidence updates; live installed-Plugin and third-party-model adherence; external CI and other operating systems; Git tag, push, GitHub Release, upload, installation, and announcement.

Handoff: Keep Ticket 8 and release `1.3.0` at Review Pending. Reconcile Generic resolver ownership, add a regression that rejects the disallowed ownership shape, rebuild generated packages, rerun affected and integrated verification, and request another fresh independent Review. This report authorizes diagnosis only.

## Findings

### [P2] Generic stage modules bypass the canonical resolver required by Core

Trigger: Directly paste any non-resolver Generic stage without a previously proven current-operation mode, such as `requirements.md` or `lite-workflow.md`. Core requires that entry to delegate to the adapter's canonical mode resolver before stage behavior (`core/modules/orchestration.md:25-30`; `core/adapters/manifest-contract.md:22`). Instead, all eight Full-stage modules independently execute a copied explicit-instruction/declaration/fallback resolver, for example `adapters/generic-prompts/requirements.md:22`, and `lite-workflow.md:27` does the same for the Lite stage. This conflicts with `bootstrap.md:29-38`, `orchestration.md:28-47`, and all three localized Generic guides (`docs/guides/generic.en.md:103-105`, with equivalent text in `generic.zh-TW.md:103-105` and `generic.ja.md:103-105`), which retain resolver ownership in bootstrap/orchestration. The tests at `tests/generic/test_generic_lite_workflow.py:183-210` require both copied local resolution and retained canonical ownership but never require delegation, so both contradictory contracts pass together.

Impact: The current copied rules happen to produce the approved immediate Full/Lite outcomes, but the Generic adapter cannot truthfully satisfy its claimed `MODE-RESOLVE-001` mapping while Core makes canonical delegation mandatory. A future precedence, conflict, fallback, or lifecycle change can diverge between the two declared resolver owners and nine stage-local copies, and a model receives conflicting ownership instructions at the public direct-entry boundary. The same inconsistency is shipped byte-for-byte in the expanded package, composed workflow, and ZIP. Reconcile the contract in one of two explicit ways: make non-owner stages delegate unresolved entry to bootstrap/orchestration while preserving the approved outcome matrix, or obtain approval to amend Core, the manifest contract, and localized ownership guidance to permit a standardized inlined guard. Then make tests reject the non-selected design rather than asserting both.

No other actionable P0-P3 finding was identified.

## Correction Coverage

| Surface | Result | Evidence |
| --- | --- | --- |
| Nine Codex Skills | Pass | `$ask-then-do-it` owns fresh resolution at `SKILL.md:22-56`; all eight stage Skills place the no-proof, Lite, and proven-Full guard before stage behavior; `adapters/codex/rule-mapping.yaml:20-47` traces all nine entries. |
| Codex conflicts, invalid Config, and lifecycle | Pass | The canonical resolver pauses conflicting explicit modes, fails present invalid Config closed to Full, preserves absence precedence, and forbids persistence or reuse. |
| Eleven Generic immediate route outcomes | Pass with contract defect | Explicit instruction, declaration, fallback, conflict, Full-stage-to-Lite, and Lite-stage-to-Full outcomes are stated in all modules, but P2 violates the normative resolver-ownership boundary. |
| Localized Codex and Generic guides | Pass for semantic parity | English, Traditional Chinese, and Japanese describe the same stage-not-mode behavior and route outcomes. Generic guide parity also reproduces the ownership conflict in P2. |
| Core and mapping traceability | Fail | Core clearly mandates delegation, while Generic claims `MODE-RESOLVE-001` without a mapping that reconciles copied local resolution with canonical ownership. |
| Generated packages and ZIPs | Pass for parity | Canonical sources, expanded outputs, composed Generic workflow, ZIP entries, inventories, and declared hashes agree. Parity propagates P2 unchanged. |

## Architecture and Refactoring Lenses

This is a change-focused pass, not a system-wide architecture diagnosis.

| Lens | Outcome | Evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `finding` | Trigger: change direct-entry precedence, conflict, or fallback behavior. Impact: the same resolver policy must change in bootstrap, orchestration, eight Full stages, and the Lite stage, and may drift. Evidence: P2 and `adapters/generic-prompts/*.md`. |
| 2. Long Function | `not-applicable` | The reviewed runtime correction is declarative Markdown and mapping data; it adds no production function whose length can be assessed. |
| 3. Large Module or Class | `no-finding` | No changed Core or adapter document acquires unrelated responsibilities beyond routing or its existing stage contract. |
| 4. Long Parameter List | `not-applicable` | No callable interface or parameter list changed in this correction. |
| 5. Data Clumps | `not-applicable` | The correction introduces no recurring loose value group crossing callable interfaces. |
| 6. Primitive Obsession | `no-finding` | Exact `full` and `lite` literals and declaration syntax are approved public contracts constrained by negative tests, not unconstrained substitutes for a missing domain type. |
| 7. Feature Envy | `finding` | Trigger: enter a non-owner Generic stage without mode proof. Impact: that stage performs orchestration's mode-source and conflict responsibilities before its own work. Evidence: `requirements.md:22`, `lite-workflow.md:27`, and the ownership declarations in `bootstrap.md:29` and `orchestration.md:28`. This is part of P2. |
| 8. Divergent Change | `finding` | Trigger: change either a stage contract or mode resolution. Impact: every non-owner stage now has two reasons to change: its own behavior and orchestration policy. Evidence: the copied guards identified in P2. |
| 9. Shotgun Surgery | `finding` | Trigger: correct or extend direct-entry mode semantics. Impact: coordinated edits are required across Core, eleven Generic modules, localized guides, literal tests, composed output, ZIPs, and checksums. The current correction demonstrates that change footprint. |
| 10. Message Chains | `no-finding` | Direct handoffs name one resolver or one next module and expose no multi-hop object-navigation chain. |
| 11. Leaky Abstraction | `finding` | Trigger: maintain or consume a directly pasted Generic stage. Impact: callers and maintainers must reconcile whether the stage resolves mode itself or delegates to the documented canonical owner. Evidence: the Core/stage/guide contradiction in P2. |
| 12. Shallow Module | `no-finding` | Bootstrap, orchestration, Lite, and Full stages each expose substantial workflow behavior; the defect is conflicting ownership, not an interface whose cost exceeds its value. |

The lens findings above are facets of P2 and do not create separate correction findings or authorize a broad refactor.

## Verification Performed

- Focused Codex, Generic, and localized-documentation modules: `56/56`, OK.
- Focused Core Lite contract: `7/7`, OK.
- Full serial discovery with the repository's existing bundled Pillow dependency exposed to the workspace interpreter: `191/191`, OK.
- Release discovery: `107/107`, OK. An initial venv-only attempt loaded and passed 104 tests but could not import Pillow; rerunning with the existing bundled dependency loaded and passed all three asset tests and then the complete suite.
- Codex and Generic conformance CLIs both passed against Core `1.3.0`.
- Marketplace validation passed.
- Direct deterministic proxy execution: Full `14,771`, Lite `5,480`, difference `9,291`, reduction `62.90%`; Generic fixed cost `14,950`; the 60% gate passed without a billing claim.
- Supplied raw validation also recorded focused integrated `39/39`, Codex `27/27`, Generic `38/38`, conformance `19/19`, canonical and packaged Skills `18/18`, Plugins `2/2`, and both conformance CLIs passing.
- Canonical-to-expanded and expanded-to-ZIP audits found no mismatch. Codex ZIP inventory contains all nine Skills; Generic ZIP inventory contains all eleven modules.
- Actual archive SHA-256 values match `dist/checksums.sha256`: Codex `e2838c830ca56b3c8dc901783e8c773127a65cd0096ddef63f2e919c615bb73e`; Generic `3aad0062d3ddc58d97d391e6b28553293d61e509a17c9ddff1058133960cb82e`.
- `git diff --check` exited `0`; output contained only informational LF-to-CRLF working-copy warnings.

## Evidence Unavailable and Residual Risk

- No live installed Codex Plugin run invoked all nine Skills under explicit, project Config, user Config, conflict, invalid, and fallback combinations. Static contracts, mapping, tests, and package parity cover the shipped instructions; host/model adherence remains external.
- No live third-party Generic model executed all eleven direct-paste cases. The supplied forward scenarios and repository tests are structural instruction checks, not a deterministic model-behavior harness.
- The conformance validator verifies declared mandatory rule IDs and versions; it does not prove that a Generic module delegates to the owner named by Core. That gap is why P2 survives passing conformance.
- Raw Red chronology was intentionally excluded from this independent pass. Ticket 8's approved `tdd` mode was preserved, and current Green behavior was independently rerun.
- External CI, non-Windows environments, publication URLs, tag state, installation, and sustained concurrent build stress were not exercised.
- Codex repeats a small direct-entry guard in each standalone Skill. Current mapping and matrix tests keep those projections aligned, but live dispatch remains the residual integration risk.

## Completion Assessment

The Codex direct-entry correction appears complete, and the Generic route matrix, localization, and package projections are mechanically complete. The overall direct-entry correction and Ticket 8 do not appear complete because P2 leaves Generic's normative resolver ownership inconsistent with Core and its public documentation. Existing release evidence should remain Review Pending, and external publication remains out of scope and unauthorized.
