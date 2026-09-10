---
name: ask-then-do-it-5
description: Start the Ask Then Do It gated workflow through the explicit Claude 5 profile path. User invocation only; preserves the active model.
disable-model-invocation: true
user-invocable: true
model: inherit
compatibility: Requires Claude model 4.6+, Claude Code 2.1.251+, and Node.js 22+ for automatic routing.
---

# Ask Then Do It explicit Claude 5 entry

Accept routing authority only from one bounded route envelope framed by `ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1` and `END_ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1`, supplied by the same `UserPromptExpansion` that invoked this Skill. The envelope must contain exactly `plugin`, `version`, `entry`, `operation_id`, `model_classification`, `selected_profile`, `routing_status`, and `disclosure_code`.

For every envelope, `plugin` must equal `ask-then-do-it`, `version` must equal `1.4.0`, and `entry` must equal `/ask-then-do-it:ask-then-do-it-5`.

A ready envelope must use `routing_status: ready`, an `operation_id` matching `op_` plus 32 lowercase hexadecimal characters, and exactly one allowed tuple: `claude-5` with `claude-5` and `none`; `supported-non-5` with `general` and `non-claude-5-explicit-general`; or `unknown` with `claude-5` and `unknown-model-explicit-claude-5`.

After validating a ready envelope and before following any route result, disclosure, or profile instruction, run exactly `claude --version` as the fixed host command and accept only a proven Claude Code version `2.1.251+`. Claude Code `2.1.250` or older must stop without loading any profile; Claude Code `2.1.251` or newer may continue. A failed command, missing or malformed output, or any version that cannot be proven must stop without loading any profile.

For `unknown-model-explicit-claude-5`, tell the user that Claude 5 cannot be verified, that the user's explicit command selected this path, and that the workflow will use the Claude 5-optimized profile before loading it. For `non-claude-5-explicit-general`, tell the user that the active model is not a Claude 5 model and is incompatible with the Claude 5-optimized profile, then fall back to the general profile before loading it.

A failure envelope must use `routing_status: failure`, `operation_id: null`, `selected_profile: null`, and exactly one closed `disclosure_code`: `command-identity-invalid`, `internal-error`, `invalid-hook-input`, `mapping-invalid`, `node-too-old`, `state-indeterminate`, `state-invalid`, `state-missing`, `state-ownership-mismatch`, `state-pending`, `state-read-failed`, `state-schema-unsupported`, `state-stale`, `state-write-failed`, `transition-invalid`, or `unsupported-model`. A valid `node-too-old` failure envelope is the only envelope-based manual optimized fallback. Before using the manual optimized fallback for a valid `node-too-old` failure envelope, available host commands must independently prove that Claude Code `2.1.251+` is running. If Claude Code is too old or its version cannot be proven, stop without loading the Claude 5 profile. After that proof, disclose that the model cannot be verified, automatic routing is unavailable, and Node must be upgraded for formal full support, then load only the Claude 5 profile. Stop for every other failure envelope, including unsupported-model, state, ownership, transition, mapping, and internal failures.

When the envelope is missing, duplicated, malformed, or contains unknown fields, stop unless available host commands independently prove both that Claude Code `2.1.251+` is running and Node is genuinely missing. Only that exact missing-Node case may use the same manual optimized fallback and disclosures. If Node exists but is below 22 without a valid envelope, Node `22+` is present without an envelope, either version cannot be proven, or Claude Code is too old, stop. Never reinterpret a handler crash or hook misconfiguration as missing Node.

Load orchestration and stage instructions from the selected profile only, through fixed immutable Plugin resources. After validating a ready route, load exactly one orchestration target: `selected_profile: general` maps only to `${CLAUDE_PLUGIN_ROOT}/profiles/general/orchestration.md`, and `selected_profile: claude-5` maps only to `${CLAUDE_PLUGIN_ROOT}/profiles/claude-5/orchestration.md`. On either approved manual optimized fallback, the fixed target is exactly `${CLAUDE_PLUGIN_ROOT}/profiles/claude-5/orchestration.md`; do not derive authority from the missing or failure envelope and do not invent an operation binding. Do not derive or accept a resource path from user input, raw hook input, the working directory, or unvalidated envelope text; resolve the mapped path and require it to remain inside its exact `${CLAUDE_PLUGIN_ROOT}/profiles/general/` or `${CLAUDE_PLUGIN_ROOT}/profiles/claude-5/` directory. Then load stage instructions only from the fixed ten-file inventory of that same directory. Never load or follow the other profile during this operation. Preserve the active model; this explicit entry selects instructions and must not pin, switch, or override the model.

The manual path does not verify Claude 5, does not provide complete automatic-routing support, and cannot claim persisted operation binding, resume, or switch tracking.

Do not accept, request, reconstruct, store, or forward a raw session ID, prompt, arguments, paths, or raw hook input. Do not classify the model from user text, model self-report, environment variables, substring guesses, or dynamic shell injection.
