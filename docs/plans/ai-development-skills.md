# Portable AI Development Workflow - v2 Plan

Status: Approved

Specification: [Portable AI Development Workflow - v2 Specification](../specs/ai-development-skills.md)

Specification status: Approved

## Planned outcome

Deliver a model-neutral workflow core, a generic prompt adapter, and a fully validated Codex adapter. Preserve the former Codex-only v1 plan as historical evidence, remove duplicate runtime sources after migration, and separate portable human documentation from provider-specific instructions.

No personal skill installation is authorized by this plan. Installation remains a separate user-approved action after source validation.

## Tickets

### Ticket 1 - Deliver the portable core with executable conformance validation

#### Outcome

Adapter authors and validators can consume one provider-neutral core containing six workflow modules, logical artifact contracts, a versioned mandatory rule catalog, and a deterministic validator that proves manifest coverage.

#### Acceptance criteria covered

- `core/` contains six normative modules, artifact contracts, and a versioned rule catalog.
- Mandatory rules use stable IDs and validator input.
- The validator rejects missing rules, unknown rules, incompatible core versions, and unsupported capability claims.
- Core requirements contain no provider-specific dependency.

#### In scope

- Core overview and version contract.
- Six normative workflow module documents.
- Five logical artifact contracts and shared artifact fields.
- Machine-readable mandatory rule catalog.
- Shared adapter manifest schema or validation contract.
- Deterministic conformance validator.
- Valid and invalid test fixtures covering mandatory failure modes.

#### Out of scope

- Provider-specific prompt wording.
- Moving existing Codex skills.
- Human usage guides.
- Personal installation.

#### Dependencies

None. This is the minimal enabling slice consumed first by Tickets 2 and 3.

#### Likely ownership areas

- `core/`
- `scripts/`
- Validator tests and fixtures in the repository's selected test convention.

#### Test-first approach

1. Add fixtures for one valid manifest and invalid manifests with a missing mandatory rule, unknown rule, incompatible version, and unjustified capability claim.
2. Add a focused test that expects the future validator to accept only the valid fixture.
3. Observe the expected failure because the validator or catalog is absent.
4. Implement the smallest rule catalog and validator that satisfy the cases.
5. Add provider-name scanning for model-neutral core content.

#### Verification

- Run focused validator tests.
- Validate all fixtures and assert expected exit results.
- Check that every mandatory ID in the approved Specification exists exactly once in the catalog.
- Scan `core/` for Codex paths, invocation syntax, provider metadata, and unsupported provider assumptions.

#### Completion criteria

- The validator gives deterministic, actionable failures.
- The valid fixture passes and every invalid fixture fails for its intended reason.
- Core module and artifact contracts are internally linked and versioned.
- No adapter implementation is required to understand the normative workflow.

#### Parallel safety

`No`. This ticket establishes shared rule IDs, versions, schemas, and validator behavior used by all downstream adapters.

### Ticket 2 - Deliver the generic conversation adapter end to end

#### Outcome

A user can copy modular English prompts into a general language model, declare capabilities, resume from supplied artifacts, complete conversation-safe stages, and receive explicit limitations instead of fabricated execution evidence.

#### Acceptance criteria covered

- The generic adapter provides one bootstrap and six independently usable workflow prompts.
- It defaults to the Conversation profile.
- It never claims repository changes, persistence, tests, completed TDD, or independent review without declared evidence-producing capabilities.
- Its manifest maps all applicable mandatory core rules.

#### In scope

- Generic adapter conformance manifest.
- Bootstrap prompt.
- Orchestration, requirement, specification, planning, implementation-guidance, and review prompts.
- Prompt headers for version, capabilities, required inputs, outputs, and stop conditions.
- Conversation-mode artifact handoff instructions.
- Limited-evidence review labeling.
- Forward-test cases for fresh and resumed workflows.

#### Out of scope

- Provider-native installation formats.
- Claiming official support for named third-party hosts.
- Repository modification or command execution by the default profile.

#### Dependencies

Ticket 1.

#### Likely ownership areas

- `adapters/generic-prompts/`
- Generic adapter fixtures that do not change core contracts.

#### Test-first approach

1. Add adapter contract checks for the required seven prompt files and mandatory prompt headers.
2. Add a scenario asserting that a conversation-only implementation request stops with an unexecuted handoff.
3. Add a scenario asserting that a supplied diff receives a limited-evidence, non-independent review label.
4. Observe failures against the absent adapter.
5. Write the minimal prompts and manifest that pass conformance and scenario checks.

#### Verification

- Run shared conformance validation.
- Run prompt structure checks.
- Forward-test requirement grilling, Draft artifact output, artifact import, capability downgrade, unexecuted implementation guidance, and limited-evidence review.
- Confirm user-facing responses follow the supplied user language while prompt sources remain English.

#### Completion criteria

- Each prompt works independently with explicit inputs and stop conditions.
- Bootstrap selects the first unmet workflow stage from supplied evidence.
- Cross-session persistence responsibility is stated whenever artifacts are emitted in conversation mode.
- No generic prompt contains Codex-only syntax, paths, metadata, or unsupported capability claims.

#### Parallel safety

`Yes`, after Ticket 1 is complete. It owns `adapters/generic-prompts/` and does not modify Codex adapter files. It may run in parallel with Ticket 3 while the approved core contract remains frozen.

### Ticket 3 - Migrate and conform the Codex adapter

#### Outcome

The existing six Codex skills live under the sole provider-specific source path, retain their current behavior, declare their real capabilities, and pass both Codex-native and shared conformance validation.

#### Acceptance criteria covered

- Six Codex skills exist under `adapters/codex/skills/`.
- No duplicate root `skills/` source remains after migration.
- Codex-specific metadata, invocation syntax, installation paths, and subagent behavior stay inside the adapter or Codex guide.
- Every skill passes the official skill validator and the shared validator.

#### In scope

- Pre-migration inventory and rollback mapping.
- Atomic source migration from `skills/` to `adapters/codex/skills/`.
- Codex conformance manifest and capability declaration.
- Rule-ID mapping from each skill to the portable core.
- Minimal skill wording changes required for semantic conformance.
- Codex-native metadata validation.
- Link and path updates owned by the adapter.

#### Out of scope

- Personal Codex installation.
- Claude Code, Gemini CLI, or other adapters.
- Duplicating source files at the root for compatibility.
- Rewriting portable human documentation.

#### Dependencies

Ticket 1.

#### Likely ownership areas

- Existing `skills/`
- `adapters/codex/`
- Codex-specific adapter fixtures.

#### Test-first approach

1. Capture the expected six-skill inventory and metadata before migration.
2. Add a structural test requiring the six directories under `adapters/codex/skills/` and forbidding a duplicate root `skills/` directory.
3. Add conformance expectations for rule coverage and declared capabilities.
4. Observe failure against the v1 layout.
5. Move the source atomically, add the manifest, and make only required contract updates.

#### Verification

- Run the official validator for all six skills.
- Run shared conformance validation.
- Compare pre- and post-migration skill inventories and provider metadata.
- Forward-test full orchestration, one-question grilling, approval gates, real TDD evidence on a safe fixture, and independent review where Codex supports isolation.
- Verify rollback mapping can restore the former workspace layout without data loss.

#### Completion criteria

- Exactly one source copy of each Codex skill exists.
- Existing trigger descriptions and UI metadata remain valid or are intentionally updated.
- Capability claims match demonstrated Codex behavior.
- Root source duplication and stale internal links are absent.

#### Parallel safety

`Yes`, after Ticket 1 is complete. It owns `adapters/codex/` and the root `skills/` migration. It may run in parallel with Ticket 2 while neither ticket changes core contracts.

### Ticket 4 - Separate portable and Codex-specific human documentation

#### Outcome

Readers receive a provider-neutral design explanation and primary generic usage guide, while Codex installation and invocation details live only in a dedicated Codex guide.

#### Acceptance criteria covered

- Portable design and generic usage documents contain no Codex-specific operating instructions.
- The Codex guide contains provider-specific installation, invocation, and capability details.
- All human documents identify the approved English Specification as canonical.

#### In scope

- Rewrite the existing design explanation around the portable architecture.
- Replace the current combined guide with `docs/guides/generic.zh-TW.md`.
- Add `docs/guides/codex.zh-TW.md`.
- Update document cross-links and terminology.
- Explain capability profiles, artifact handoff, gates, adapter support status, and honest downgrade behavior.

#### Out of scope

- Translating the canonical core or generic prompts.
- Provider guides for unsupported adapters.
- Changing workflow semantics through documentation edits.

#### Dependencies

Tickets 2 and 3, so the guides describe validated behavior and final paths.

#### Likely ownership areas

- `docs/design/`
- `docs/guides/`
- Cross-links in approved project documents where necessary.

#### Test-first approach

Automated behavior tests are not meaningful for prose quality. Before editing, use the approved documentation exception and define alternative checks:

- Link-target validation.
- Required-section checks.
- Provider-term scanning in portable documents.
- Human comparison against the approved Specification and adapter manifests.

#### Verification

- Confirm every relative link resolves.
- Scan generic documents for `.codex`, `$skill-name`, `agents/openai.yaml`, Codex installation paths, and unsupported host instructions.
- Confirm the Codex guide contains the required installation and invocation details.
- Check that the documents do not duplicate a translated core contract.

#### Completion criteria

- A new user can choose generic or Codex instructions without conflating them.
- Portable documentation explains what is guaranteed at each capability profile.
- Provider-specific details appear only in the Codex guide or adapter source.

#### Parallel safety

`No`. This ticket consumes the validated outputs and final paths of Tickets 2 and 3 and updates shared documentation links.

### Ticket 5 - Integrate, forward-test, and prepare the v2 source release

#### Outcome

The repository is internally consistent, all declared support claims are backed by validation evidence, and the source is ready for a separately authorized installation or future adapter work.

#### Acceptance criteria covered

- Generic and Codex manifests pass deterministic conformance validation.
- Official Codex validation passes.
- Representative tests cover gates, artifacts, capability downgrade, TDD evidence, limited review, and independent review where supported.
- Only generic prompts and Codex are labeled officially supported.
- No personal installation or unsupported provider claim occurs.

#### In scope

- Full validator and test execution.
- File inventory, placeholder, duplicate-source, stale-link, and provider-leak checks.
- Independent forward tests using raw artifacts and minimal context.
- Core-to-adapter rule coverage report.
- Final source handoff with residual risks and deferred adapters.

#### Out of scope

- Installing into a personal or external host directory.
- Publishing to a marketplace or remote repository.
- Adding deferred provider adapters.

#### Dependencies

Tickets 1-4.

#### Likely ownership areas

- Validation fixtures and reports that belong in the repository.
- Small fixes across completed tickets when validation exposes a contract defect.

#### Test-first approach

Use the approved acceptance criteria as the integration test matrix. Add failing integration checks for any uncovered criterion before fixing the corresponding source artifact.

#### Verification

- Run all shared validator tests and adapter conformance checks.
- Run all official Codex skill validations.
- Execute representative generic and Codex forward tests from clean contexts.
- Verify required directory layout, document links, rule coverage, support labels, and absence of duplicate sources.
- Confirm the workspace can be rolled back using the recorded migration mapping if necessary.

#### Completion criteria

- Every acceptance criterion has direct validation evidence or an explicitly documented manual check.
- No blocking finding remains.
- Residual risks and deferred provider adapters are accurately reported.
- Installation remains pending explicit user authorization.

#### Parallel safety

`No`. This is sequential integration work over all prior tickets.

## Dependency order and parallel groups

```text
Ticket 1: Portable core and validator
    |-- Ticket 2: Generic prompts adapter --|
    |-- Ticket 3: Codex adapter migration --|--> Ticket 4: Human documentation --> Ticket 5: Integration
```

Tickets 2 and 3 form the only proposed parallel group. All other work is sequential.

## Plan approval gate

This plan does not authorize implementation while its status is `Draft`. After explicit approval, change the status to `Approved` and begin with Ticket 1.
