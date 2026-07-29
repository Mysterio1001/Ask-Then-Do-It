# Implementation Evidence - v3 Ticket 1

Artifact type: Implementation Evidence

Artifact ID: `v3-ticket-1`

Workflow ID: `grill-me-core-v3`

Core version: `3.0.0`

Status: Completed

## Inputs

- Approved [Core v3 Specification](../specs/ai-development-skills-v3.md).
- Approved [Core v3 Ticket Plan](../plans/ai-development-skills-v3.md), Ticket 1.
- Existing validated Core `2.0.0` and release `2.1.0` source.

## Outcome

Delivered the first vertical Core v3 behavior: documented requirement interrogation with evidence-backed Project Knowledge Base synchronization, Draft Working Notes, a directly callable Codex `grill-with-docs` Skill, and an independently usable Generic documented-requirements prompt.

## Expected red evidence

The first usable test invocation required the existing PyYAML development dependency. Earlier attempts without an available Python or readable PyYAML installation were environment failures and were not counted as behavioral red evidence.

After loading PyYAML from an isolated workspace test dependency directory, this command was executed:

`python -m unittest tests.conformance.test_validator tests.codex.test_adapter tests.generic.test_generic_prompts`

Observed product result before implementation:

- 30 tests ran.
- 4 tests failed and 6 errored for the intended missing behavior.
- The catalog remained Core `2.0.0` and lacked `KB-EVIDENCE-001`, `KB-DRAFT-001`, and `KB-SYNC-001`.
- The Project Knowledge Base, Draft Working Notes, and project-knowledge module contracts were absent.
- `grill-with-docs` and `documented-requirements.md` were absent.
- Existing unrelated tests remained green.

These failures matched Ticket 1's missing behavior.

## Focused green evidence

The same 30-test command completed with:

- 30 tests run.
- 30 tests passed.

Coverage includes Core `3.0.0`, the three mandatory knowledge rules, canonical Knowledge Base path and sections, provisional note states, Codex Skill inventory and approval behavior, Generic prompt inventory and capability limits, migration snapshot integrity, adapter manifests, and shared conformance validation.

Direct conformance results:

```text
Conformance passed: codex against core 3.0.0
Conformance passed: generic-prompts against core 3.0.0
```

## Skill and Plugin validation

- The official `skill-creator` validator returned `Skill is valid!` for all seven current Codex Skills.
- The official Plugin validator returned `Plugin validation passed` for `adapters/codex/plugin/grill-me`.
- No cachebuster, personal installation, reinstall, marketplace write, or publication was performed.

## Changed areas

- Core version, module index, artifact envelope, requirement handoff, and mandatory rules under `core/`.
- New `core/modules/project-knowledge.md`.
- New Project Knowledge Base and Draft Working Notes artifact contracts.
- New Codex `grill-with-docs` Skill and generated `agents/openai.yaml` metadata.
- New Generic `documented-requirements.md` prompt.
- Core-version and rule mappings in both adapter manifests.
- Existing artifact-producing Skills and Generic prompts updated to emit Core `3.0.0` artifacts.
- Conformance, Codex, and Generic behavior tests and fixtures.
- Codex migration inventory current hashes, while all original v1 hashes remain unchanged.

## Test-first exceptions

Markdown instructions do not execute the workflow themselves. Their semantic contract is verified by exact rule, section, state, capability, approval, and artifact assertions plus shared validators. Model forward testing is deferred because this run is not authorized to create subagents or separate tasks.

## Residual risks and deferred work

- Automatic documented-mode routing is intentionally deferred to Ticket 4; direct invocation is complete.
- The twelve-lens review contract is deferred to Ticket 2.
- Architecture diagnosis is deferred to Ticket 3.
- First-use v2 Knowledge Base migration is deferred to Ticket 5.
- Release configuration and generated packages remain at validated release `2.1.0` until Ticket 6. Existing `dist/` artifacts were not modified.
- Prompt conformance cannot guarantee identical reasoning quality across model versions.

## Handoff

Ticket 1 is complete. Ticket 2 may begin against the approved Core `3.0.0` knowledge contract. Tickets 3-6 remain dependency-blocked.
