# Ask Then Do It: A Model-Neutral AI Development Workflow

Ask Then Do It divides "ask before acting" into two top-level modes: `Full` and `Lite`. Full preserves complete decision, implementation, and Review evidence. Lite uses less workflow material for well-bounded, lower-risk work while retaining user authority, minimum validation, and honest reporting.

Top-level Full/Lite is separate from the test choice inside a Full Ticket. Lite is not an alias for `direct`, and it must not fabricate Full documents to authorize implementation.

## The problem

A single heavyweight workflow is traceable, but it repeatedly generates and reloads requirements, specifications, Tickets, and handoff material for small changes. Removing TDD alone leaves the rest of that workflow cost in place.

The design therefore protects two outcomes:

- Existing Full approvals, documents, test choices, Review, and architecture improvement behavior remain unchanged.
- Lite reduces workflow-controlled material while disclosing its lower verification confidence and traceability.

## Core and host ownership

Core owns the provider-neutral Full/Lite contract: mode identities, Full fallback, Full compatibility, the Lite lifecycle, risk pauses, approval authority, minimum validation, Review correction authority, and session behavior.

| Layer | Responsibility | Capability it must not claim |
| --- | --- | --- |
| Core | Defines model-neutral semantics and safety boundaries shared by both modes | Does not select host-specific Config paths or tool capabilities |
| Codex Plugin | The Codex adapter maps user and project Config, Skills, file access, and command tools to Core | Must not redefine Core semantics or persist a temporary operation choice |
| Generic workflow | The Generic adapter maps a default-mode declaration and conversation modules to Core | Without tool evidence, must not claim file edits, command execution, or observed test results |

The Codex adapter reads Plugin-owned Config, resolves precedence, and performs file and command work within real permissions. The Generic adapter composes a long-form workflow with a default-mode declaration and preserves capability honesty for a conversation-only host.

Documentation also has explicit ownership. The three localized beginner guides are canonical for the complete Full/Lite user flow; the Codex and Generic guides own host configuration; short entry pages only route readers; this design guide owns maintainer contracts and the token-proxy target.

## Adapter equivalence

Hosts do not need identical tools, but the same user decisions must produce equivalent observable outcomes. Equivalence includes at least:

- An explicit current-operation instruction outranks a persistent default, and no valid default means Full.
- Full retains its three approvals; Lite has one Change Brief approval.
- A high-risk switch affects only the current operation, and material risk discovered during implementation pauses work for another decision.
- Lite creates no workflow documents, adds no tests, and discloses both observed and unavailable validation.
- Lite Review presents findings as a batch and requires user approval before corrections.
- A new session resolves mode again and never claims to resume unpersisted Lite state.

Codex can edit and verify directly. A conversation-only Generic host can offer a plan or analyze user-supplied evidence but cannot claim tool outcomes. That is a capability difference, not a difference in workflow outcome or approval authority.

## Full contract

Full is for high-risk, cross-module, still-uncertain, or audit-sensitive work. Its existing lifecycle remains unchanged:

1. Perform repository reconnaissance, then ask one requirements question at a time until requirements consensus.
2. Synchronize approved information to the Project Knowledge Base only after requirements approval.
3. Create and approve a specification that defines behavior and failure handling.
4. Split work into vertical Tickets, recommend a test choice for each, and ask in one response whether to add tests to every Ticket before approving the complete plan.
5. Full maps the test choices internally to `tdd` or `direct`. TDD requires Red, Green, and Refactor; direct runs no behavioral tests and records the untested behavior.
6. Preserve implementation evidence for independent Review through twelve perspectives. A systemic issue enters architecture improvement analysis and returns through specification and Tickets for new implementation authority.

Requirements consensus, specification, and Ticket plan are Full's three formal approval gates. A mode resolver may precede Full, but it cannot remove or shorten these contracts.

## Lite contract and lower traceability

Lite has lower traceability than Full because its Change Brief, approval, progress, and Review remain in the current conversation instead of becoming workflow documents that another session can resume. Documentation and completion reporting must keep this tradeoff visible.

The shared Lite lifecycle is focused reconnaissance and risk evaluation; up to three blocking questions per round; an approximately 800-token Change Brief; one approval; direct implementation; static plus success/failure-path validation; compact Review; approval for finding corrections; and a completion response normally around 500 tokens.

Lite adds or modifies no behavioral tests, does not use TDD, and does not require Full's twelve Review perspectives or an independent reviewer. It still stops scope expansion, preserves user changes, performs available minimum validation, and lets a known failure prevent an unqualified completion claim.

## Risk and authority boundaries

Authentication, authorization, payment, data migration, destructive data operations, public contracts, cross-module structure, concurrency, asynchronous behavior, and external side effects are evaluated before Lite approval. When material risk exists, the host presents evidence and asks whether to switch only the current operation to Full; the user may accept the risk and continue Lite.

New risk during implementation pauses further modification. A switch to Full preserves observable changes and returns to the earliest unmet Full gate. The choice must not rewrite Config or affect another session.

## Reproducible token proxy

The release gate compares Full and Lite through an equivalent representative scenario. The fixture holds the task, decisions, risk, and delivered outcome constant. Both modes use the same normalization and counting method so a failure can be reproduced inside the repository.

The count includes workflow-controlled material: questions, the Change Brief or Full documents, stage instructions, composed prompt content, repeated handoffs, and completion reporting. The same rule applies to both modes, and material that disadvantages Lite is not specially excluded.

The count excludes task-specific source code, necessary tool output, and hidden model reasoning because those are not common costs that the workflow can deterministically control. The fixture, counting rule, raw Full and Lite counts, and formula must be disclosed in tests or release evidence.

Reduction uses one formula: `(Full proxy - Lite proxy) / Full proxy * 100`. Lite must reduce the controlled proxy by at least 60% for the representative scenario or the release gate fails.

This proxy validates only repository-controlled workflow material. It does not guarantee an API bill reduction, total context size, hidden reasoning cost, or cache discount. Maintainers must not describe a passing gate as a billing guarantee.

## Maintenance rules

- A Core mode change requires matching Codex and Generic mappings plus evidence of equivalence.
- Lite must not weaken Full's one-question sequence, three approvals, per-Ticket test choice, TDD/direct evidence, or Review.
- Lite question, Change Brief, and completion budgets are approximate user-visible output targets; they never justify hiding failure, risk, or missing evidence.
- The beginner guides keep the complete user flow; host guides keep configuration; short entry pages do not duplicate the flow, and no separate Lite guide is added.
- The Generic workflow claims only real host capabilities and provides a clear handoff or unverified disclosure when tools are unavailable.
- The 60% proxy uses an equivalent scenario and fixed rules; a fixture or algorithm change must be evaluated for both modes together.

## Read next

- [Beginner's Full/Lite Workflow Guide](../guides/getting-started-simple.en.md)
- [Codex Plugin Guide](../guides/codex.en.md)
- [Generic Guide](../guides/generic.en.md)


[Back to README](../../README.md)
