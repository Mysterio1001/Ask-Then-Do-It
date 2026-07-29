# Implementation Evidence - v2 Ticket 5

Artifact type: Implementation Evidence

Artifact ID: `v2-ticket-5`

Workflow ID: `portable-ai-development-v2`

Core version: `2.0.0`

Status: Completed

## Inputs

- Approved v2 Specification.
- Approved v2 Plan, Ticket 5.
- Completed Implementation Evidence for Tickets 1-4.
- Final Generic prompts and Codex adapter sources.

## Outcome

Integrated the portable core, Generic prompts adapter, Codex adapter, and separated human documentation. Added semantic Codex conformance checks discovered by forward testing, completed clean-context representative tests, and verified the source is ready for a separately authorized installation or future adapter work.

## Integration red evidence

The first full pass found that the migrated v1 Codex prose passed format, hash, Rule-ID, and manifest checks but did not explicitly require every v2 Artifact envelope field, runtime capability declaration, evidence label, or modular user-language behavior.

New Codex integration tests were added before changing skill prose. The expected red result was:

- 9 test methods ran.
- Artifact-envelope subtests failed for all five producers.
- Language checks failed for the five directly usable module skills.
- Runtime capability declaration and Review-label checks failed.
- The migration inventory failed the new pre-migration/current dual-hash contract.
- Existing mandatory Rule-ID mapping and manifest coverage remained green.

The failures matched the uncovered v2 semantics rather than an unrelated environment problem.

## Integration green evidence

Minimal additive instructions were added to the six Codex `SKILL.md` files. The v1 hashes remain recorded, current v2 hashes are validated, and all `agents/openai.yaml` metadata remains unchanged.

Final automated suites:

- Core conformance: 7 tests passed.
- Generic prompts: 11 tests passed.
- Codex adapter: 9 tests passed.
- Total: 27 tests passed.

Direct manifest validation:

```text
Conformance passed: generic-prompts against core 2.0.0
Conformance passed: codex against core 2.0.0
```

The official `skill-creator` validator returned `Skill is valid!` for all six Codex skills.

## Forward-test evidence

Forward-test agents received only the selected prompt or Skill, the user scenario, and raw task-local artifacts. They were not given intended fixes or expected verdicts.

| Scenario | Observed behavior | Assessment |
| --- | --- | --- |
| Requirement grilling | Asked exactly one question about named-member versus link sharing, recommended named members, stated the login-friction tradeoff, then stopped | Passed `GRILL-ONE-001` behavior |
| Resume from Approved Specification | Reused the supplied private-notes Specification, produced two vertical Tickets, kept the Plan `Draft`, requested explicit approval, and did not implement | Passed resumption, vertical slicing, and Plan gate; its missing portable envelope exposed the semantic integration red that was then fixed |
| Generic implementation request | Emitted `UNEXECUTED IMPLEMENTATION GUIDANCE`, declared Conversation capability, reported no files or tests as changed or run, and handed off required red/green evidence to a tools-capable host | Passed capability downgrade and honest-claim behavior |
| Generic supplied-diff Review | Labeled output `limited-evidence` and `non-independent`, found the unauthorized administrator bypass, disclosed unavailable repository evidence, and did not edit code | Passed limited-evidence Review behavior |
| Codex real TDD fixture | Added public-function tests, observed two `NotImplementedError` red errors, implemented the approved retry policy, then reported focused and broader 2/2 green with raw commands and result summaries | Passed real red-green evidence and portable Implementation Evidence output |
| Codex isolated raw-artifact Review | A reviewer that did not implement the password-reset change received only approved intent, diff, test excerpts, and raw results; it labeled evidence `limited-evidence`, stated reviewer independence, found reusable reset tokens as P1, emitted the Review Report envelope, and withheld completion | Passed evidence-first Review, isolation, labeling, and Artifact handoff behavior |

The TDD fixtures were bounded to `.forward-test/` and removed after evidence capture.

## Structural and documentation verification

- Exactly six Codex skills exist under `adapters/codex/skills/`.
- No root `skills/` duplicate exists.
- All six skills contain a maintainer comment for developers.
- Exactly seven Generic prompt files exist: one bootstrap plus six modules.
- All relative Markdown links resolve.
- No unresolved `TODO`, `FIXME`, `TBD`, placeholder marker, or stale combined-guide link remains.
- The core and portable operating documentation contain no provider invocation syntax, personal installation path, or provider metadata dependency.
- The Traditional Chinese design, Generic guide, and Codex guide all link to the Approved English Specification as canonical.
- Only Generic prompts and Codex are described as officially supported v2 adapters.

## Changed areas

- `adapters/codex/skills/`
- `adapters/codex/migration-inventory.yaml`
- `adapters/codex/rule-mapping.yaml`
- `tests/codex/test_adapter.py`
- `docs/evidence/v2-ticket-5.md`

## Test-first exceptions

Forward-test fixtures and prose checks use declared alternative verification where a lasting production red test is not meaningful. The semantic Codex contract gap had an automated surface, so failing tests were added and observed before the Skill changes.

## Residual risks and deferred adapters

- Prompt and Skill conformance cannot guarantee identical reasoning quality across model versions.
- Generic Conversation mode still relies on users to persist and re-supply complete Artifacts.
- Claude Code, Gemini CLI, and other provider-specific adapters remain deferred and unsupported until implemented and tested.
- No personal Skill installation, marketplace publication, remote publication, or external-system mutation was performed.

## Handoff

The v2 source is ready for use through copyable Generic prompts and for a separately authorized Codex installation. Any installation or publication remains a distinct user-approved action.
