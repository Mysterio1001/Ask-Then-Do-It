# Implementation Evidence - v2 Ticket 1

Artifact type: Implementation Evidence

Artifact ID: `v2-ticket-1`

Workflow ID: `portable-ai-development-v2`

Core version: `2.0.0`

Status: Completed

## Inputs

- Approved v2 Specification.
- Approved v2 Plan, Ticket 1.

## Outcome

Delivered a provider-neutral core with six workflow modules, five logical artifact contracts, twelve mandatory rule IDs, a capability hierarchy, an adapter manifest contract, and a deterministic conformance validator.

## Expected red evidence

Command:

`python -m unittest discover -s tests/conformance -p test_validator.py`

Observed result before implementation:

- 7 tests failed or errored.
- The validator script and core rule catalog were absent.
- The provider-neutrality check reported zero core contract files.

The failures matched the planned missing behavior.

## Focused green evidence

The same command completed with:

- 7 tests run.
- 7 tests passed.

The cases cover a valid manifest, a missing mandatory rule, an unknown rule, an incompatible core version, a capability without evidence, the approved mandatory rule set, and provider-neutral core content.

## Broader verification

- Direct validation accepted the valid fixture against core `2.0.0`.
- Direct validation rejected the missing-rule fixture for missing `REVIEW-EVIDENCE-001`.
- The core inventory contains 15 contract files.

## Changed areas

- `core/`
- `scripts/validate_conformance.py`
- `tests/conformance/`
- `requirements-dev.txt`

## Exceptions

The Markdown contract content has no meaningful automated behavior test. It is verified through rule-catalog equality, provider-term scanning, file inventory, internal links, and adapter conformance tests.

## Residual risks

- Adapter prose conformance still requires Tickets 2 and 3.
- YAML parsing requires the declared PyYAML development dependency.
- Semantic rule coverage is validated by mappings and forward tests, not by full natural-language equivalence proof.

## Handoff

Tickets 2 and 3 may proceed in parallel against the frozen core `2.0.0` contract.
