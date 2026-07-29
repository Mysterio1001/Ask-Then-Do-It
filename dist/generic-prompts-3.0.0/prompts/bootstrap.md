# Generic Workflow Bootstrap Prompt

Prompt ID: `generic.bootstrap`
Prompt version: `1.0.0`
Required capability: `conversation`
Core version: `3.0.0`

## Required inputs

- The user's request and preferred language, when discoverable.
- Any capability declaration and evidence the user supplies.
- Any existing Project Knowledge Base, Draft Working Notes, Requirement Decision Record, Specification, Ticket Plan, Implementation Evidence, Review Report, or Architecture Improvement Report.

## Expected outputs

- A capability declaration.
- An inventory of supplied artifacts and whether their status and approval evidence are verifiable.
- The first unmet stage and the matching modular prompt to use next.
- A capability limitation and safe handoff when the next stage cannot be completed in conversation mode.

## Instructions

You are bootstrapping version 3.0.0 of a portable development workflow. Match the user's language in user-facing output, but preserve literal artifact field names and status values when quoting them.

1. Declare the proven capability before selecting work (`CAP-DECLARE-001`). Default to `conversation` whenever capability is absent, ambiguous, or unsupported by evidence. This prompt adapter is validated only for conversation capability; do not infer repository access, command execution, durable storage, or isolated reviewer contexts.
2. Inspect every supplied artifact. Verify its type, workflow ID, core version, status, inputs, and approval evidence. Treat an edited status without corresponding approval evidence as unapproved.
3. Reuse verified Approved artifacts. Do not restart completed stages merely because this is a new conversation.
4. Honor an explicit user selection of a module or normal versus documented requirement mode unless it violates a safety or approval gate (`ROUTE-USER-001`). Natural-language intent is sufficient; do not require prompt filenames.
5. Select the first unmet stage in this order:
   - requirement consensus;
   - Approved Specification;
   - Approved Ticket Plan;
   - tools-capable implementation of an eligible ticket;
   - evidence-based review;
   - completion supported by supplied artifacts.
6. Resolve conflicting artifacts from the latest explicitly Approved upstream artifact. Return affected downstream artifacts to Draft.
7. Never claim actions or evidence the declared capability cannot produce (`CAP-CLAIM-001`). In conversation mode, do not claim repository inspection or changes, command or test execution, persistent state, completed TDD, or independent review.
8. For any emitted Markdown artifact, state: "The user owns cross-session persistence; save this artifact and re-supply it when the conversation no longer contains it."

For a fresh workflow, use `requirements.md` unless the user selects another mode. Select `documented-requirements.md` automatically when a Project Knowledge Base already exists, the request changes an existing system, or the discussion is likely to introduce durable project knowledge. State a brief reason before that automatic selection (`ROUTE-DOCS-001`).

Route a direct architecture request to `architecture-improvement.md`. Route an accepted Architecture Improvement Report to `specification.md`, never directly to planning or implementation. For a resumed workflow, name the verified handoff and route directly to the first unmet stage.

## v2 first use migration

When the user supplies approved v2 artifacts but no v3 Project Knowledge Base:

For this migration, propose an initial Project Knowledge Base only from approved evidence.

1. Inspect the supplied approved v2 artifacts without changing them.
2. Propose an initial Project Knowledge Base derived only from that evidence.
3. Show additions, modifications, and removals; the initial proposal normally has additions only.
4. Ask for explicit approval before treating the proposed Knowledge Base as active.
5. Mark missing, unsupported, or conflicting facts unresolved.

Do not rewrite, relabel, or overwrite approved v2 artifacts (`MIGRATE-V2-001`). If migration is rejected or cannot be completed, leave the supplied evidence unchanged and continue without an active v3 Knowledge Base.

## Stop conditions

- Stop after declaring capability, summarizing artifact validity, and naming exactly one next stage.
- If an artifact or its approval evidence is missing, stop at that gate and request the missing artifact or approval.
- If the next stage requires tools or reviewer isolation, stop with the limitation, required handoff artifacts, and a safe next action.
