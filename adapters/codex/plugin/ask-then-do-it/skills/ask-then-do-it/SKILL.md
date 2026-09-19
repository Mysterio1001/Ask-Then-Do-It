---
name: ask-then-do-it
description: Route every software-changing operation through implicit Config-driven Full or Lite mode discovery, including trivial, fully specified, formatting-only, and single-line changes. Also use for explicit structured development workflows; do not use for non-software questions.
---

# AI Dev Workflow

Resolve the top-level mode, then load only the selected lifecycle.

## Declare capabilities

Before selecting or invoking a workflow stage, state the strongest capability profile proven in the current runtime:

- `conversation` can exchange text and produce user-managed artifacts.
- `tools` additionally requires actual repository read/write access, artifact persistence, and command execution.
- `multi_agent` additionally requires isolated worker or reviewer contexts.

If a required tool or isolation mechanism is unavailable, downgrade to the strongest proven profile. Never claim repository changes, test execution, persistence, parallel independence, or completed review evidence outside the declared profile. End an unsupported stage with the limitation, required handoff, and safe next action.

## Resolve the top-level mode

Resolve one top-level mode for every current operation before selecting a workflow stage. The only supported modes are `full` and `lite`.

Use this precedence: explicit current-operation instruction, project Config, user Config, then Full fallback.

- User Config: `~/.codex/ask-then-do-it.toml`.
- Project Config: `<project>/.codex/ask-then-do-it.toml` inside the active project root. A Config outside the active project root is not that project's override.
- The only recognized setting is a top-level `mode` whose value is exactly `mode = "full"` or `mode = "lite"`. Do not treat aliases, different capitalization, nested values, or workflow-policy settings as a supported mode.

Apply the sources deterministically:

- A valid explicit instruction wins without reading Config, even when a Config would be malformed, unreadable, missing-mode, or unsupported.
- Conflicting explicit full and lite instructions pause routing and require one clarification; do not select by word order.
- With no explicit instruction, a valid project Config wins over user Config.
- An absent project Config continues to user Config.
- A present invalid project Config fails closed to Full; do not continue to user Config.
- With no controlling project Config, a valid user Config selects its mode.
- An absent user Config falls back to Full.
- A present invalid user Config fails closed to Full.

A present Config is invalid when it is unreadable, malformed TOML, missing-mode, or contains an unsupported mode value. Disclose a fail-closed result when it changes the route the user expected.

Mode resolution is read-only. Do not write or create either Config. Do not repair or normalize invalid Config, and do not persist a current-operation override. Do not reuse a previous operation's or session's mode as an undocumented fallback.

Direct selection of any public stage Skill selects a stage, not top-level Full. When that stage has no current-operation mode proof, it must delegate here before stage behavior. Resolve the mode afresh; never treat direct Skill selection as Full fallback.

## Route the selected mode

The top-level `full` and `lite` modes are distinct from the Full Ticket-level `tdd` and `direct` implementation choices.

- For proven `full`, read the [Full routing workflow](references/full-routing.md) completely before acting and follow that lifecycle.
- For proven `lite`, read the [Lite workflow](references/lite-workflow.md) completely before acting and follow that lifecycle.

Lite MUST NOT fabricate an Approved Full Specification, Ticket Plan, Ticket implementation mode, or Full evidence artifact. A selection or override applies only to the current operation and never mutates either Config.

## Operating rules

- Match user-facing communication and generated documents to the user's language. Default to Traditional Chinese only when no preference is discoverable.
- Read applicable repository instructions before acting. Preserve user changes and follow existing project conventions.
- Answer questions from repository evidence instead of asking the user. Ask only for product decisions, unavailable context, or choices with material tradeoffs.
- Treat requirement consensus, specification approval, and ticket-plan approval as separate human gates.
- Never modify implementation code, install dependencies, or cause external side effects before all applicable gates pass.
- If implementation evidence contradicts an approved artifact, return to the earliest affected gate. Never silently redefine the requirement.
