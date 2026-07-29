# Implementation Evidence - v2 Ticket 3

Artifact type: Implementation Evidence

Artifact ID: `v2-ticket-3`

Workflow ID: `portable-ai-development-v2`

Core version: `2.0.0`

Status: Completed

## Inputs

- Approved v2 Specification.
- Approved v2 Plan, Ticket 3.
- Frozen core `2.0.0` contract from Ticket 1.
- Approved v1 Codex skill sources under the former root `skills/` path.

## Outcome

Migrated all six Codex skills into the sole provider-specific source at `adapters/codex/skills/`, preserved the v1 source snapshots and UI metadata, added conformance and rule mappings, and recorded a deterministic rollback inventory. Ticket 5 semantic integration then added the minimum v2 instructions for runtime capability declaration, portable Artifact envelopes, evidence labels, and user-language matching.

## Expected red evidence

Command:

`python -m unittest discover -s tests/codex -p test_*.py -v`

Observed result before migration:

- 5 tests ran.
- 2 tests failed and 3 errored.
- The root `skills/` duplicate still existed.
- `conformance.yaml`, `rule-mapping.yaml`, and `migration-inventory.yaml` were absent.
- The expected migrated file inventory was absent.

The failures matched the planned pre-migration layout and missing adapter contracts.

## Focused green evidence

After migration, the same command completed with 5 tests passed. Ticket 5 added four semantic integration cases; the final focused result is:

- 9 tests run.
- 9 tests passed.

The cases verify the sole six-skill source, preserved v1 and current v2 hashes, unchanged provider metadata, safe rollback mappings, capability and rule coverage, resolvable rule implementations, modular language behavior, runtime capability declaration, Artifact envelopes, and evidence labels.

## Broader verification

Shared conformance command:

`python scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest adapters/codex/conformance.yaml`

Observed result:

`Conformance passed: codex against core 2.0.0`

The seven Ticket 1 conformance tests also passed unchanged.

The official `skill-creator` `quick_validate.py` validator produced `Skill is valid!` for each of:

- `ai-dev-workflow`
- `grill-requirements`
- `implement-tdd`
- `plan-tickets`
- `review-code`
- `write-spec`

The root `skills/` path no longer exists. All six `agents/openai.yaml` files match their pre-migration SHA-256 snapshots. `migration-inventory.yaml` records both each original v1 hash and the current v2 hash for the six minimally conformed `SKILL.md` files.

## Changed areas

- `adapters/codex/`
- `tests/codex/`
- Former root `skills/` source moved to `adapters/codex/skills/`

## Refactoring

The atomic move initially left skill prose and provider metadata byte-identical. Semantic integration later added only the v2 contract instructions required by the Approved Specification; provider metadata remained unchanged, and both source generations remain auditable by hash.

## Exceptions

The migration itself has no meaningful behavioral red test beyond the structural, hash, manifest, and rollback assertions declared before the move. Those checks are the alternative verification surface.

## Residual risks

- The rollback mapping is verified structurally but was not executed because the approved outcome requires the migrated layout.
- Installation into a personal Codex skill directory remains outside this ticket and has not occurred.

## Handoff

Ticket 4 may now document the stable generic and Codex adapter paths. Ticket 5 must integrate all validators and exercise approval, TDD evidence, and independent-review behavior.
