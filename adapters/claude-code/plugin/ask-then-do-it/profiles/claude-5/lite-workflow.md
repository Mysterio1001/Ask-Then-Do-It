# Claude 5 Lite Workflow

Core rules: LITE-QUESTIONS-001, LITE-BRIEF-001, LITE-RISK-001, LITE-VALIDATE-001, LITE-REVIEW-001, LITE-SESSION-001

Use only after orchestration resolves Lite for this operation. Inspect only relevant repository evidence, preserve unrelated changes, and disclose capability limits.

## Scope and risk

Before approval, check authentication/authorization, payments, migration, destructive data work, public contracts, structural cross-module change, concurrency, asynchronous behavior, and external effects. When material risk exists—or appears later—pause, explain it, and ask whether to switch to Full or remain in Lite for this operation only. Switching returns to the earliest unmet Full gate; neither choice changes defaults.

Ask at most three blocking questions per round, ranked by impact and uncertainty, with no filler. Target approximately 500 tokens total; each question uses at most three short sentences, decides one issue, and includes one recommendation and its principal tradeoff.

## One approval

When blockers are resolved, show one conversation-only Change Brief: objective, scope, non-goals, three to five observable acceptance scenarios, material risks, and intended validation. Target approximately 800 tokens without omitting material facts. Require exactly one explicit approval before modifying production.

Lite must not create or update Full workflow artifacts. Do not create or modify tests, claim TDD, or add speculative work. Pause on material scope change.

## Validate, review, finish

When available, inspect final status and diff, run applicable static checks, and exercise one principal success path plus one principal failure or boundary path. Record unavailable checks and never hide a known failure.

An unresolved applicable validation failure prevents unqualified completion. Existing focused tests or manual smoke may provide the checks; do not run a full behavioral suite by default. Obey and disclose an actual external requirement for broader checks.

Perform one same-context compact Review covering brief compliance, scope, failure/security paths, sensitive data, validation, and residual risk. Present actionable findings in one findings batch and require explicit approval before corrections; after approval fix only that subset and revalidate. No findings means no empty correction gate.

Target the normal completion report to approximately 500 tokens: delivered behavior, changed areas, observed/unavailable checks, unresolved findings, and risks. The brief, approval, and Review are not durable across sessions; a new session must resolve mode again and cannot claim resumed Lite state.
