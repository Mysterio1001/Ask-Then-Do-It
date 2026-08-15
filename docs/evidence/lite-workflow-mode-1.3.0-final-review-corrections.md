# Lite Workflow Mode 1.3.0 Final Review Corrections

Artifact type: Implementation Evidence

Artifact ID: `lite-workflow-mode-1-3-final-review-corrections`

Workflow ID: `lite-workflow-mode`

Core version: `1.1.0`

Release version: `1.3.0`

Status: Completed

Inputs: Approved [Specification](../specs/lite-workflow-mode-1.3.0.md), Approved [Ticket Plan](../plans/lite-workflow-mode-1.3.0.md), [Final Independent Review](ask-then-do-it-1.3.0-final-review.md), and the user's explicit approval on 2026-08-15 to correct the complete P1/P2 finding batch.

Approved implementation mode: `tdd` from Tickets 2 and 3. Ticket 7 owns generated release integration, and Ticket 8 owns final validation and evidence closure.

Assumptions: Skill frontmatter is the public Codex discovery boundary. `scripts/build_release.py` is the only permitted writer for managed `dist/` output. Existing point-in-time Review, architecture, and Ticket evidence remains historical and is not rewritten when current measurements change.

Deferred: Fresh final independent Full Review, completed release evidence, Ticket 8 completion, and every external publication, installation, Config mutation, tag, push, upload, and announcement action.

Handoff: The [Independent Correction Review](lite-workflow-mode-1.3.0-final-review-corrections-review.md) found no actionable issue, and the [release architecture closure](ask-then-do-it-1.3.0-release-architecture-diagnosis-after-review-fixes.md) found no release correctness blocker. A fresh independent `$review-code` context must now review the complete `1.3.0` candidate. Any new actionable finding returns to the user before correction.

## Outcome

The approved P1 correction makes the Codex orchestrator discoverable for every software-changing operation, including trivial, fully specified, formatting-only, and single-line changes. Mode resolution therefore occurs before routing. Trivial non-software questions remain excluded, and the legacy small-change behavior is now explicitly a resolved-Full subpath that never applies after Lite is selected.

The approved P2 correction replaces Generic's unqualified generated-file prohibition with one explicit permission: users may edit only the `Default workflow mode` declaration. The permission precedes the declaration in the composed workflow and is enforced in both fresh-build and tracked-package tests.

## P1 discovery and Full-subpath TDD

Red command:

```text
.\.venv\Scripts\python.exe -m unittest tests.codex.test_lite_workflow.CodexLiteWorkflowTests.test_implicit_discovery_resolves_mode_for_every_software_change_size
```

Observed before the source correction:

```text
Ran 1 test in 0.001s
FAILED (failures=1)
AssertionError: 'every software-changing operation' not found
```

The test reads the actual YAML frontmatter discovery description, covers all four excluded software-change classes, and verifies that the legacy small path is a resolved-Full subpath rather than a third top-level mode.

Focused Green after the smallest Skill correction:

```text
Ran 1 test in 0.001s
OK
```

The complete Codex suite then passed `24/24`. The canonical Skill also passed official `quick_validate.py` validation before package integration.

## P2 generated edit-contract TDD

Red command covered the in-memory composer, a fresh isolated package, and the tracked package boundary:

```text
.\.venv\Scripts\python.exe -m unittest -v tests.generic.test_generic_lite_workflow.GenericLiteCompositionTests.test_generated_workflow_allows_only_default_mode_declaration_edits tests.release.test_generic_release.GenericReleaseTests.test_built_workflow_allows_only_default_mode_declaration_edits tests.release.test_generic_release.GenericReleaseTests.test_builder_emits_self_contained_conversation_only_package
```

Observed before the source correction:

```text
Ran 3 tests in 0.321s
FAILED (failures=3)
```

All failures were the expected missing qualified edit permission while the unqualified `GENERATED FILE - DO NOT EDIT` contract remained.

After changing only the generated banner, in-memory composition passed `4/4`, the fresh isolated package passed `1/1`, and the complete Generic suite passed `33/33`. The tracked-package test remained at its expected single failure until central release integration rebuilt `dist/`.

## Release integration

The first approved builder invocation encountered a temporary Windows atomic-replacement failure while moving `dist/generic`:

```text
Release build failed: Atomic release replacement failed: [WinError 5] Access is denied.
```

The builder restored the previous output and removed its staging directory. Read-only inspection confirmed that both package directories and the previous checksum manifest remained present and unchanged. No source correction was made for the environment-only failure.

The immediate serial retry succeeded:

```text
Built codex, generic release 1.3.0 in C:\Users\Ian\Desktop\Grill Me\dist
```

The combined post-build correction group passed `4/4`. The complete release suite passed `105/105`. Canonical and packaged validation passed for all 18 Skill instances and both Plugin instances.

Current archive SHA-256 values are:

```text
f4448e20e2654ed5837cbddd5d0713c79b933a1410f4d13e91ac2ef84a775995  codex/ask-then-do-it-1.3.0.zip
b399c9de509acf65d2ed277ed9d86d29926fd756947b1dff68c434f5ffa059c1  generic/ask-then-do-it-generic-1.3.0.zip
```

## Deterministic proxy contract refresh

The approved Skill discovery text adds the same 60 proxy tokens to the shared orchestrator event in both Full and Lite. The semantic output-event difference remains `8,412`, but the denominator changes the percentage. The existing exact-value contract correctly failed against the changed authoritative source:

```text
Ran 19 tests in 2.919s
FAILED (failures=1)

actual:   (13828, 5416, 8412, 6083)
expected: (13768, 5356, 8412, 6109)
```

After checking the unchanged integer gate and refreshing only the exact current-source tuple, the complete proxy suite passed `19/19`.

The current deterministic result is:

- Codex Full: `13,828` proxy tokens.
- Codex Lite: `5,416` proxy tokens.
- Difference: `8,412` proxy tokens.
- Reduction: `60.83%`; the fixed `60.00%` gate passes.
- Fixture SHA-256: `03211645237dabb53d43458f9e10203d33c10be9f782cd8a13cb1dbef05d5277`.
- Generic fixed composed cost: `13,326` proxy tokens.
- Generic composed SHA-256: `97f489969d250fe24479d155bccccc6f8e04442efc77ffafb8938c82b141734a`.
- No API billing guarantee or Generic 60% claim is made.

## Additional observed validation

- Codex: `24/24` passed.
- Generic: `33/33` passed.
- Conformance: `18/18` passed.
- Release: `105/105` passed.
- Final serial discovery after integration: `180/180` passed.
- Skill validation: `18/18` passed.
- Plugin validation: `2/2` passed.
- A fresh no-context forward test selected Lite for a Config-selected single-line software change, Full's named legacy subpath for a no-Config formatting edit, and no workflow Skill for a trivial non-software question.
- The fresh independent correction Review found no actionable findings and independently confirmed source, expanded-package, ZIP, checksum, and proxy boundaries.
- The read-only architecture closure found P1/P2 structurally resolved, prior F1 still resolved, and no new release correctness blocker. F2-F4 remain unaccepted non-blocking Draft proposals.
- Scoped syntax and `git diff --check` validation passed with only configured Windows LF-to-CRLF warnings.

This correction evidence is complete. The local release and Ticket 8 remain pending their separate fresh final Full Review and evidence gate.
