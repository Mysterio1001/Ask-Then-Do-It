# Implementation Evidence - v3 Ticket 4

Artifact type: Implementation Evidence

Artifact ID: `v3-ticket-4`

Workflow ID: `grill-me-core-v3`

Core version: `3.0.0`

Status: Completed

## Inputs

- Approved [Core v3 Specification](../specs/ai-development-skills-v3.md).
- Approved [Core v3 Ticket Plan](../plans/ai-development-skills-v3.md), Ticket 4.
- Completed evidence for [Ticket 1](v3-ticket-1.md), [Ticket 2](v3-ticket-2.md), and [Ticket 3](v3-ticket-3.md).

## Outcome

Integrated direct and natural-language routing across documented requirements, normal requirements, review, and architecture diagnosis. Explicit user selection now overrides automatic routing while preserving safety and approval gates. Automatic routes state a reason, architecture diagnosis does not run after every Ticket, and accepted architecture reports return to Specification.

## Expected red evidence

Command:

`python -m unittest tests.conformance.test_validator tests.codex.test_adapter tests.generic.test_generic_prompts`

Observed result before implementation:

- 41 tests ran.
- 6 tests failed for the intended missing routing behavior.
- `ROUTE-USER-001` and `ROUTE-DOCS-001` were absent.
- Core, Codex, and Generic orchestrators lacked the approved documented-requirements conditions and architecture triggers.
- Review did not hand systemic findings to architecture diagnosis or suppress duplicate tracking.

## Focused green evidence

The same suite completed with:

- 41 tests run.
- 41 tests passed.

Direct validations passed:

```text
Skill is valid!  # ai-dev-workflow
Skill is valid!  # review-code
Plugin validation passed: adapters/codex/plugin/grill-me
Conformance passed: codex against core 3.0.0
Conformance passed: generic-prompts against core 3.0.0
```

## Changed areas

- Core orchestration module and two mandatory routing rules.
- Codex `ai-dev-workflow` and `review-code` Skills.
- Generic bootstrap, orchestration, and review prompts.
- Knowledge synchronization handoff rules.
- Both adapter manifests, Codex rule mapping, conformance fixtures, and routing tests.
- Current Codex migration hashes for the two changed legacy Skills; original v1 hashes remain preserved.

## Test-first exceptions

Routing is implemented as model instructions, not an executable router library. Deterministic tests assert every trigger phrase, precedence rule, handoff, non-trigger, and adapter mapping. Separate model forward tests are not run because this execution has no user authorization to create subagents or tasks.

## Residual risks and deferred work

- Model interpretation may vary on whether evidence is truly systemic; every automatic route must still state its reason.
- v2 first-use migration and human documentation remain Ticket 5.
- Combined Generic release composition and packaged inventories remain Ticket 6.
- Direct selection cannot bypass capability, safety, or approval gates.

## Handoff

Ticket 4 is complete. Ticket 5 may implement non-destructive first-use migration and update human-facing documentation against the integrated v3 behavior.
