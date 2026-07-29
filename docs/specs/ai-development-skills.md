# Portable AI Development Workflow - v2 Specification

Status: Approved

## Problem

The current workflow encodes a generally useful AI-assisted development method inside Codex-specific skill packaging, invocation syntax, metadata, installation paths, and agent behavior. This makes the method appear model-independent while its executable form is tied to one host.

The project needs one normative, model-neutral workflow core plus adapters that translate the same contract into host-specific instructions without weakening approval gates, evidence requirements, or capability limits.

## Goals

- Define one provider-neutral workflow contract for requirement interrogation, specification, ticket planning, test-driven implementation, and review.
- Keep consequential product decisions under explicit human control.
- Support conversation-only models without allowing them to fabricate repository changes, test results, persistence, or reviewer independence.
- Support tool-capable and multi-agent hosts through declared capability profiles.
- Provide a generic prompt adapter that can be copied into any sufficiently capable language model.
- Preserve a fully validated Codex adapter as the first provider-specific implementation.
- Detect adapter drift through stable rule identifiers, conformance manifests, and deterministic validation.
- Keep internal contracts and prompts in English while matching user-facing output to the user's language.

## Non-goals

- Claim first-class support for Claude Code, Gemini CLI, or any other provider before a dedicated adapter is implemented and tested.
- Pretend that all models have equivalent filesystem, terminal, testing, persistence, context-isolation, or delegation capabilities.
- Generate all adapter prose automatically from the core contract.
- Define application-framework-specific implementation patterns.
- Replace host security, permission, sandbox, or confirmation policies.
- Allow a lower-capability adapter to report stronger evidence than it can actually produce.

## Users and scenarios

- A user pastes generic prompts into a chat model to clarify a requirement and draft portable artifacts.
- A coding agent with repository and command access persists artifacts, implements an approved ticket, and runs tests.
- A multi-agent host delegates demonstrably independent tickets and performs review in an isolated context.
- A Codex user invokes the existing modular workflow through provider-native skills.
- An adapter maintainer maps a new host to the core rules and proves conformance before marking it supported.

## Required behavior

### 1. Model-neutral core

The project MUST maintain a `core/` source of truth that contains no provider-specific invocation syntax, metadata schema, installation path, product name, or assumed tool API.

The core MUST define six independently addressable modules:

1. Workflow orchestration.
2. Requirement interrogation.
3. Specification authoring and approval.
4. Vertical ticket planning and approval.
5. Test-driven implementation.
6. Evidence-based review.

The core MUST use the normative terms `MUST`, `SHOULD`, and `MAY`. Mandatory rules MUST have stable identifiers. The initial rule catalog MUST cover at least these invariants:

- `CAP-DECLARE-001`: declare host capabilities before selecting executable stages.
- `CAP-CLAIM-001`: never claim an action or evidence that the declared capabilities cannot produce.
- `GATE-REQ-001`: require explicit requirement consensus.
- `GATE-SPEC-001`: require explicit specification approval.
- `GATE-PLAN-001`: require explicit ticket-plan approval.
- `GRILL-ONE-001`: ask exactly one requirement question per turn and include a recommendation.
- `SPEC-NOCODE-001`: keep production implementation code out of behavioral specifications.
- `PLAN-VERTICAL-001`: plan vertically testable behavior instead of horizontal technical layers.
- `TDD-RED-001`: observe the expected failing test before production implementation when automated testing is reasonable.
- `REVIEW-EVIDENCE-001`: review raw evidence rather than an implementer's conclusion.
- `ART-STATE-001`: preserve explicit Draft and Approved artifact states.
- `ADAPTER-COVERAGE-001`: map every mandatory core rule in each conforming adapter.

Rule identifiers MUST remain stable across compatible core revisions. Removed or semantically changed rules require a new core version and migration notes.

### 2. Capability profiles

Every adapter MUST declare one or more of these cumulative profiles:

#### Conversation profile

The host can exchange text but cannot be assumed to inspect or modify a repository, persist files, run commands, or isolate another reviewer context.

It MAY:

- Interrogate requirements.
- Produce a Requirement Decision Record.
- Draft a Specification.
- Draft a Ticket Plan.
- Analyze user-supplied diffs or evidence as a limited-evidence review.
- Offer implementation guidance that is explicitly marked unexecuted.

It MUST NOT:

- Report repository files as modified.
- Mark implementation as complete.
- Report tests or commands as executed.
- Claim persistent cross-session state.
- Claim independent review without an isolated context.

#### Tools profile

The host can inspect and modify a repository, persist artifacts, and execute relevant commands.

It MAY additionally:

- Implement approved tickets.
- Produce real red-green-refactor evidence.
- Run focused and broader verification.
- Persist artifacts according to repository conventions.

It MUST preserve unrelated user changes and obey host permissions and confirmation policies.

#### Multi-agent profile

The host can create isolated worker or reviewer contexts and exchange bounded artifacts between them.

It MAY additionally:

- Parallelize tickets proven independent by an approved plan.
- Perform independent review using a context that did not implement the change.

It MUST NOT claim isolation when workers share conclusions or implementation context in a way that materially anchors the reviewer.

An adapter MAY implement a lower profile without implementing higher profiles. Unsupported stages MUST stop with a capability limitation and a safe handoff, not silently degrade the meaning of completion.

### 3. Logical artifacts

The core MUST define five logical artifact types:

1. Requirement Decision Record.
2. Specification.
3. Ticket Plan.
4. Implementation Evidence.
5. Review Report.

Each artifact MUST include or unambiguously convey:

- Artifact type and stable artifact ID.
- Workflow or feature ID.
- Core version.
- Status, including `Draft` or `Approved` when an approval gate applies.
- Inputs or source artifacts.
- Known assumptions, limitations, and deferred decisions.
- Intended next-stage handoff.
- Approval evidence when approved.

Tool-capable adapters SHOULD follow existing repository documentation conventions. When none exist, they SHOULD persist Specifications under `docs/specs/` and Ticket Plans under `docs/plans/`.

Conversation-only adapters MUST emit complete Markdown artifacts that users can save and re-supply. They MUST state that the user owns cross-session persistence and must provide the artifact again when context is unavailable.

### 4. Human approval gates

The workflow MUST require explicit human approval at three points:

1. Requirement consensus.
2. Specification approval.
3. Ticket-plan approval.

Silence, previous approval of another artifact, file status edited without corresponding conversation evidence, or an unrelated response MUST NOT count as approval.

No implementation stage may begin before the relevant Specification and Ticket Plan are approved. If implementation or review reveals a requirement defect, the workflow MUST return to the earliest affected gate and invalidate or revise downstream artifacts.

### 5. Requirement interrogation

The requirement module MUST:

- Use available read-only project evidence before asking questions.
- Ask exactly one question per turn.
- Include a concrete recommended answer and its principal tradeoff.
- Prioritize high-impact uncertainty over a fixed questionnaire.
- Trace decisions through product behavior, architecture, data, security, failure handling, operations, and acceptance criteria.
- End with a consolidated decision summary and one explicit consensus question.
- Prohibit implementation before consensus.

### 6. Specification

The specification module MUST convert confirmed decisions into an implementation-independent behavioral contract. It MUST cover goals, non-goals, users and scenarios, required behavior, edge and failure behavior, data and external contracts, compatibility, constraints, assumptions, deferred decisions, and observable acceptance criteria.

It MUST write or emit a `Draft` first, request explicit approval, and only then mark the artifact `Approved`. It MUST return to requirement interrogation when a material decision is missing.

### 7. Ticket planning

The planning module MUST require an approved Specification and split work into vertically testable behavior. Each ticket MUST define outcome, covered acceptance criteria, scope, dependencies, likely ownership areas, test-first approach, focused and broader verification, completion criteria, and parallel-safety reasoning.

It MUST write or emit a `Draft` plan first and require explicit approval before implementation. Uncertain parallel safety MUST default to sequential execution.

### 8. Test-driven implementation

Formal implementation completion requires the Tools profile.

For each reasonably testable behavior change, the implementation module MUST:

1. Add or identify the smallest meaningful test for approved behavior.
2. Execute it and observe failure for the expected missing-behavior reason.
3. Make the smallest coherent production change that passes.
4. Execute the focused test.
5. Refactor without changing behavior.
6. Execute broader relevant verification in proportion to risk.
7. Record raw results in Implementation Evidence.

It MUST NOT weaken acceptance criteria or tests to accommodate an incorrect implementation. A test-first exception MAY be used only when an automated failing test is not meaningful; the exception and alternative verification MUST be declared before editing.

Conversation-profile adapters MAY provide an unexecuted implementation proposal but MUST NOT label it Implementation Evidence or completed TDD.

### 9. Review

The review module MUST evaluate specification compliance, correctness, regressions, failure behavior, security, privacy, test quality, and maintainability. It MUST report actionable findings first, ordered by severity and linked to precise evidence when locations exist.

A Multi-agent adapter MAY claim independent review only when the reviewer context did not implement the change and receives raw artifacts without the implementer's conclusions or defenses.

A Conversation or Tools adapter without isolation MAY analyze supplied evidence, but MUST label the result as non-independent or limited-evidence review. A review request authorizes diagnosis and reporting, not implementation of fixes.

### 10. Adapter contract

Every adapter MUST include a machine-readable conformance manifest containing:

- Adapter ID and version.
- Target host or usage mode.
- Required core version or compatible range.
- Declared capability profiles.
- Artifact persistence behavior.
- Implemented mandatory rule IDs.
- Provider-specific validation commands or checks.
- Tested environment and validation status.

Adapter prose MAY be optimized for the host, but its semantics MUST remain compatible with mapped core rules. A deterministic validator MUST fail when:

- A mandatory core rule is unmapped.
- The manifest references an unknown or incompatible rule.
- The adapter claims a capability without required behavior or validation evidence.
- The adapter core version is incompatible.

Full adapter prompt text SHOULD remain hand-authored for the host. The validator checks contractual coverage rather than generating all prose.

### 11. Generic prompts adapter

The generic adapter MUST support the Conversation profile and MAY expose additional profiles only when the user explicitly declares the required tools and evidence channel.

It MUST provide:

- One bootstrap prompt that declares capabilities, imports existing artifacts, and determines the next stage.
- One orchestration prompt.
- One requirement-interrogation prompt.
- One specification prompt.
- One ticket-planning prompt.
- One TDD implementation prompt.
- One review prompt.

Each prompt MUST identify its prompt version, required capability profile, required inputs, expected outputs, and stop conditions. Each prompt MUST be independently usable without forcing a restart of completed stages.

### 12. Codex adapter

The current Codex skills MUST move from the root `skills/` directory to `adapters/codex/skills/`. The project MUST NOT retain a duplicate root copy.

The Codex adapter MAY use `SKILL.md`, `agents/openai.yaml`, `$skill-name` invocation, Codex subagents, and Codex installation paths only inside the adapter or its provider-specific guide.

All Codex skills MUST continue to pass the official skill validator and the shared conformance validator.

### 13. Language

The core contract, rule catalog, manifests, adapter instructions, and generic prompts MUST be maintained in English. Adapters MUST instruct models to match user-facing output to the user's language when discoverable.

The project MUST NOT maintain duplicated translated core contracts or prompt sets. Human-facing design and usage documentation MAY be translated.

### 14. Human documentation

Human documentation MUST separate portable concepts from provider-specific operation:

- `docs/design/` explains model-neutral architecture and rationale.
- `docs/guides/generic.zh-TW.md` explains the portable workflow for Traditional Chinese readers.
- `docs/guides/codex.zh-TW.md` explains Codex installation, invocation, and provider capabilities.
- Future officially supported adapters receive corresponding provider guides.

Documentation MUST identify the approved English Specification as the canonical source.

## Edge cases and failure behavior

- When host capabilities are unknown, default to the Conversation profile until stronger capabilities are proven.
- When an artifact is missing or its approval state cannot be verified, stop at the corresponding gate.
- When a conversation loses earlier context, require the user to re-supply the relevant artifact rather than reconstructing approval from memory.
- When an adapter supports repository tools but not isolated agents, allow implementation but label review as non-independent.
- When tests cannot run because of environment failure, report the raw blocker and do not mark the ticket complete.
- When two artifacts disagree, use the latest explicitly approved upstream artifact and return downstream artifacts to Draft.
- When an adapter fails conformance, mark it experimental or unsupported and prevent official-support claims.
- When a provider changes its native format or capabilities, keep the core stable and update only the adapter unless workflow semantics must change.

## Data, permissions, and external contracts

The workflow artifacts may contain product requirements, repository paths, diffs, test results, and review findings. Adapters MUST obey host policies for sensitive data, external transmission, filesystem writes, command execution, and user confirmation.

The core does not grant permission to upload private artifacts, change external systems, install software, or perform destructive actions. Adapters MUST preserve the host's authorization boundaries.

Conformance manifests and artifact schemas are public project contracts. Provider credentials, private repository contents, secrets, or live environment data MUST NOT be embedded in them.

## Compatibility, rollout, and recovery

- The existing Codex-only implementation is v1 behavior and remains the migration source until the v2 Specification and Ticket Plan are approved.
- The root `skills/` directory MUST remain unchanged while this Specification is Draft.
- After approval, planning MUST define an atomic migration to `adapters/codex/skills/`, link updates, validation, and rollback checks.
- The existing v1 plan remains historical and MUST NOT authorize v2 implementation.
- No personal Codex installation may be overwritten without explicit installation authorization.
- Rollback MUST restore the pre-migration workspace layout without losing the v2 core or documentation work already approved.

## Constraints and assumptions

- Markdown is the portable human- and model-readable format for core contracts and generic prompts.
- YAML is the default machine-readable format for adapter conformance manifests unless implementation evidence justifies another format.
- Provider adapters may require provider-owned metadata in addition to the shared manifest.
- Model quality varies; conformance guarantees workflow instructions and evidence boundaries, not identical output quality.
- Technology-stack neutrality remains required for application development tasks.
- User-facing output follows the user's language; internal normative sources remain English.

## Acceptance criteria

- Core workflow requirements outside adapter-specific and migration sections contain no provider-specific dependency.
- `core/` contains six normative modules, a versioned mandatory rule catalog, and artifact contracts.
- Every mandatory core rule has a stable ID and appears in validator input.
- `adapters/generic-prompts/` contains one bootstrap prompt and six independently usable workflow prompts.
- The generic adapter defaults to the Conversation profile and never claims unexecuted work, tests, persistence, or independent review.
- `adapters/codex/skills/` contains the six migrated Codex skills and no duplicate root `skills/` source remains.
- Generic and Codex adapters contain valid conformance manifests with explicit core versions, rule coverage, capabilities, persistence behavior, and validation status.
- A deterministic conformance validator rejects missing mandatory rules, unknown rules, incompatible core versions, and unsupported capability claims.
- All Codex skills pass the official skill validator after migration.
- Representative forward tests verify requirement grilling, artifact handoff, approval gates, capability downgrade, real TDD evidence on a tool-capable fixture, limited-evidence review, and independent review where supported.
- Portable design and generic usage documents contain no Codex-specific operating instructions.
- The Codex guide contains provider-specific installation and invocation details.
- No adapter other than generic prompts and Codex is labeled officially supported in v2.

## Deferred decisions

- Claude Code adapter format and validation.
- Gemini CLI adapter format and validation.
- Additional provider-specific adapters.
- Automated generation of complete adapter prompt prose.
- A hosted artifact persistence service for conversation-only models.
- Cross-provider benchmark criteria beyond contract conformance and representative forward tests.
