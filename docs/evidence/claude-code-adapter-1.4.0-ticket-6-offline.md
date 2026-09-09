# Claude Code Adapter 1.4.0 Ticket 6 Offline Preparation Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-6-offline`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Approved Ticket mode: `tdd`

Status: Offline tooling and two Review corrections accepted by independent re-review. Actual behavior, Ticket 6 completion and release remain pending.

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md) section 11; Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 6 and its 2026-09-09 offline-first sequencing authority; reviewed Ticket 4/5 profile sources; Core `1.3.1` rule inventory; existing fixed Claude5 scenario/matrix references. The user authorized offline tool preparation without changing acceptance criteria or permitting login/model calls.

Assumptions: The coordinating agent established current-operation Full fallback, multi_agent capability and Approved `tdd`. Existing profile references are authored expected outcomes, not observed behavior. Shared model-response recipes may describe hypothetical task states; these are not trusted host envelopes or proof of Ticket 3. Positive execution-dependent cases additionally need concrete cited tool results. The validator can check provenance declarations, hashes and structural boundaries but cannot authenticate an export/human or determine semantic truth by itself.

Deferred: All actual Claude model runs, 60 profile/scenario observations, 24 paired observations, two public authority sequences, authenticated host contracts, formal context measurements, canonical conformance activation, release integration and final live smoke. No login, paid model call, installation/removal, model switch, Marketplace activation, publication or full repository suite was performed.

Handoff: The [independent re-review](claude-code-adapter-1.4.0-ticket-6-offline-review.md) accepted the fixed catalog/staged map, public validation API, pending preparation flow, synthetic separation, transcript/citation/phase checks and paired-input/operation-span corrections. Central integration owns broader regressions. Offline Green validates this tool only; actual evidence remains unavailable and the normal release behavior gate rejects the prepared/synthetic output.

Approval: The user's explicit 2026-09-09 offline-first approval authorizes this bounded preparation. It does not approve fabricated model results or a completed Ticket/release claim.

## Delivered preparation and validation

- `scripts/validate_claude_behavior.py` provides `prepare`, actual `validate`, and distinctly labeled `check-synthetic`. Public `validate_behavior_evidence(path: Path, plugin_root: Path | None = None) -> list[str]` is the integration boundary. An empty list means all checkable **actual-evidence** boundaries passed, not authenticated truth or overall release completion.
- A fixed shared catalog covers all 30 scenario IDs, the twelve paired cases and both authority directions. It carries 131 authored subcases: 66 original static references plus 65 explicit architecture/lifecycle matrix situations. None is an execution record. The staged `1.4.0` conformance map fixes 30 Core rules and three cumulative capabilities without creating the canonical manifest or changing current `1.3.1` declarations.
- `prepare` refuses overwrite and writes 86 pending run records, operator prompts, the disposable repository fixture description and an empty transcript directory. Every outcome is unverified; no response or result is synthesized.
- Actual validation requires exact run/outcome inventories; current frozen Plugin source and catalog/staged/fixture hashes; chronological UTC times; unique isolated session hashes and transcripts; identical supported model/effort/tools/fixture/environment across all twelve pairs; complete scrubbed export provenance and explicit human semantic review; exact per-subcase assistant/tool quotations with valid offsets; required ordered raw execution phases; and operation/profile/resource boundaries for both public authority directions.
- The tool-dependent cases require raw inspection, Red/Green/validation, direct non-test validation, or success/known-failure output as applicable. Expected result labels alone do not satisfy these checks. Human review must still judge relevant Red, appropriate commands, artifact content, completeness and prohibited-action absence.
- `synthetic.py` creates clearly marked fabricated test data in temporary directories only. The normal actual gate rejects it. A deliberately invalid test mutation relabels metadata but retains known synthetic markers; a second Red demonstrated that weakness, and the corrected actual gate now rejects the candidate.
- [Operator guide](../claude_sys/behavior-verification.md) explains preparation, real-run prerequisites, test-only profile selection versus real public authority entries, copying only task inputs, preserving actual complete exports, recording normalized transcript fields/citations and mandatory human authenticity/semantic review.

## Changed files

- `scripts/validate_claude_behavior.py`
- `tests/claude/test_behavior_evidence.py`
- `tests/claude/fixtures/behavior/catalog.json`
- `tests/claude/fixtures/behavior/staged-conformance.json`
- `tests/claude/fixtures/behavior/repository-fixture.json`
- `tests/claude/fixtures/behavior/synthetic.py`
- `docs/claude_sys/behavior-verification.md`
- This evidence.

Profiles, router, public Skills, shared conformance, current versions, default `dist/` and other agents' files were not edited by this Ticket.

## Observed Red — missing preparation boundary

Command:

```text
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_behavior_evidence -v
```

Raw output excerpt:

```text
test_prepare_produces_only_unexecuted_ledger_and_release_gate_rejects_it (tests.claude.test_behavior_evidence.BehaviorPreparationTests.test_prepare_produces_only_unexecuted_ledger_and_release_gate_rejects_it) ... FAIL
AssertionError: 2 != 0
Ran 1 test in 0.076s
FAILED (failures=1)
```

Exit `1`. The Python subprocess could not open the not-yet-implemented `scripts/validate_claude_behavior.py`; this was the intended missing public preparation implementation, not an unrelated dependency failure. The raw absolute machine paths in that subprocess diagnostic are not reproduced in this scrubbed evidence.

After implementing pending preparation and actual rejection, the same focused command produced:

```text
test_prepare_produces_only_unexecuted_ledger_and_release_gate_rejects_it (tests.claude.test_behavior_evidence.BehaviorPreparationTests.test_prepare_produces_only_unexecuted_ledger_and_release_gate_rejects_it) ... ok
Ran 1 test in 0.841s
OK
```

Exit `0`.

## Observed Red — metadata relabeling of known synthetic records

Command:

```text
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_relabeling_all_metadata_cannot_promote_known_synthetic_markers -v
```

Raw output excerpt:

```text
test_relabeling_all_metadata_cannot_promote_known_synthetic_markers (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_relabeling_all_metadata_cannot_promote_known_synthetic_markers) ... FAIL
AssertionError: [] is not true : known synthetic records must not become actual evidence by metadata edits
Ran 1 test in 4.782s
FAILED (failures=1)
```

Exit `1`. The adversarial candidate existed only in the temporary test directory and was never delivered or claimed as actual evidence. After adding the known synthetic-marker rejection, this test passed in the full focused result below. The guard catches known self-authored test records; it is not a cryptographic or semantic authentication claim.

## Focused Green and final verification

Before the second Red, the expanded focused suite passed 11 tests in `16.586s`. After the correction and final source-inventory/all-pair environment checks, command:

```text
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_behavior_evidence -v
```

Raw final output:

```text
test_actual_gate_cannot_be_enabled_by_relabeling_only_ledger (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_actual_gate_cannot_be_enabled_by_relabeling_only_ledger) ... ok
test_authority_operations_prohibit_wrong_profile_cross_load_and_overlap (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_authority_operations_prohibit_wrong_profile_cross_load_and_overlap) ... ok
test_citation_must_match_observed_response_and_same_subcase (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_citation_must_match_observed_response_and_same_subcase) ... ok
test_complete_synthetic_structure_cannot_pass_actual_release_gate (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_complete_synthetic_structure_cannot_pass_actual_release_gate) ... ok
test_environment_minimum_tools_model_and_pair_identity (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_environment_minimum_tools_model_and_pair_identity) ... ok
test_exact_inventory_hash_provenance_and_review_rejections (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_exact_inventory_hash_provenance_and_review_rejections) ... ok
test_execution_evidence_requires_real_phases_and_tool_citations (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_execution_evidence_requires_real_phases_and_tool_citations) ... ok
test_fixed_recipe_staged_conformance_and_pair_inputs (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_fixed_recipe_staged_conformance_and_pair_inputs) ... ok
test_raw_transcript_digest_paths_schema_and_scrub_fail_closed (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_raw_transcript_digest_paths_schema_and_scrub_fail_closed) ... ok
test_relabeling_all_metadata_cannot_promote_known_synthetic_markers (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_relabeling_all_metadata_cannot_promote_known_synthetic_markers) ... ok
test_prepare_produces_only_unexecuted_ledger_and_release_gate_rejects_it (tests.claude.test_behavior_evidence.BehaviorPreparationTests.test_prepare_produces_only_unexecuted_ledger_and_release_gate_rejects_it) ... ok
test_prepare_refuses_overwrite_and_preserves_files (tests.claude.test_behavior_evidence.BehaviorPreparationTests.test_prepare_refuses_overwrite_and_preserves_files) ... ok

Ran 12 tests in 20.633s

OK
```

Exit `0`. No broader suite was run here; central integration owns it. No test is skipped and no actual transcript is fabricated as successful evidence. Passing synthetic tool checks and generated pending templates leave the actual behavior gate failed/unavailable.

## Remaining limits

The normalized transcript format is project-owned. Hashes bind recorded bytes, not their truth. Explicit human review and intact exports are required because software cannot prove a reviewer was honest, an action was absent, an output was authentic, or a semantic judgment was correct. Hypothetical fixture responses do not establish actual hook/session/lifecycle behavior; the authority runs additionally require real public entries, and Ticket 3 remains separate. No current observation can complete Ticket 6, count a formal context reduction or justify release activation.

## Independent Review corrections

The independent reviewer identified two checkable gaps: an extra user instruction or approval on only one paired member was ignored by the fixed-input subsequence check; an authority operation span could contain only its task input and omit the cited model response. The approved correction adds exact equality of each pair's complete ordered user-message stream and requires authority spans to contain their assistant/tool responses plus corresponding outcome citations. It preserves the fixed input/outcome catalog, ledger/transcript schema, public API and preparation hashes. Existing **unexecuted** prepared kits remain compatible; no `prepare` regeneration is required for this correction. Any recorded evidence must be revalidated with the corrected validator.

Observed Red command:

```text
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_paired_extra_user_approval_must_be_identical_on_both_sides tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_authority_operation_spans_must_include_observed_response_and_citations -v
```

Raw output excerpts:

```text
test_paired_extra_user_approval_must_be_identical_on_both_sides (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_paired_extra_user_approval_must_be_identical_on_both_sides) ... FAIL
test_authority_operation_spans_must_include_observed_response_and_citations (tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_authority_operation_spans_must_include_observed_response_and_citations) ... FAIL
AssertionError: [] is not true : one-sided extra approval must break paired input equality
AssertionError: [] is not true : an input-only operation cannot establish observed authority
Ran 2 tests in 3.998s
FAILED (failures=2)
```

Exit `1`. Both probes used explicitly synthetic temporary records and failed for the intended missing check before the production validator correction.

After correction, the full focused command above (`-m unittest tests.claude.test_behavior_evidence -v`) produced the raw summary:

```text
Ran 14 tests in 20.139s

OK
```

Exit `0`, with both new regression methods reported `ok`. No broader suite or actual Claude run was executed. The independent reviewer will recheck these final correction bytes; release behavior remains unavailable.
