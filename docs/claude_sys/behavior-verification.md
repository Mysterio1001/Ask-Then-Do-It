# Claude profile behavior verification — offline preparation

This procedure prepares Ticket 6 evidence. It does not run Claude, log in, change
a model, install a Plugin, or establish a release pass. The current source uses
provisional host contracts until Ticket 3 is verified. Actual Claude calls and
final acceptance remain deferred until separately authorized.

## Prepare

From the repository root, choose a new output directory outside the Plugin:

```text
python scripts/validate_claude_behavior.py prepare --output <new-evidence-directory>
```

The tool refuses to overwrite an existing directory. It writes an unexecuted
`behavior-evidence.json`, 86 operator prompt files and a repository fixture
description. The transcript directory is empty. There are exactly 60 profile
scenario runs (30 per profile), 24 runs for the 12 paired cases and two authority
direction runs. Every observation starts `unverified`; no response or result is
generated. The fixture's file map describes a small local total calculator.
Materialize those files into a **new disposable directory per run** and record
the fixture identity. Keep this evidence output separate from that directory.

The staged conformance fixture maps all 30 Core rules and cumulative
conversation/tools/multi_agent capabilities. Its `staged-unverified` status is
intentional. Do not copy it to canonical `adapters/claude-code/conformance.yaml`
or change current versions; Ticket 9 owns later lockstep activation.

## Run after real Claude verification is authorized

1. Keep the exact prepared profile/bootstrap/reviewer/router/config/manifest
   bytes. If any source or fixed recipe changes, prepare and execute a new set;
   do not edit hashes to reuse old observations. Record OS, supported surface,
   exact Claude Code version (`2.1.251+`), Node (`22+`), exact supported canonical
   model ID, effort and sorted exact tool inventory. All 12 paired cases use the
   same model, effort, tools, fixture, input and OS/surface versions. Each pair
   must also have identical complete ordered user messages, including every
   extra clarification, approval and instruction before/between/after fixed
   inputs. If different interaction is needed, record a failed comparison and
   rerun both members with the same agreed interaction; do not edit transcripts.
2. Use a genuinely new isolated Claude session for each of the 86 runs, with no
   earlier test transcript. Hash each raw session identifier locally and retain
   only its SHA-256. Never record raw session IDs or credentials. A two-entry
   authority case intentionally keeps both operations inside its one fresh
   session; no other run may reuse that session.
3. Scenario and paired comparisons may directly select a profile **only as the
   Specification's test-only comparison**. Load the selected orchestration and
   required same-profile modules from the frozen Plugin resource tree. This
   does not create a public command, switch the active model, or prove public
   bootstrap routing. Give both paired members the same task messages. Record
   `entry: test-only-profile-selection` and the actual loaded resource names.
4. Copy only each numbered user message from its prompt file. The operator-only
   checklist must not be sent as the model's answer or presented as observed
   behavior. The given states are explicit hypothetical task fixtures for
   testing model responses; they are **not** trusted hook signals, real install
   state, evidence of an executed command, or permission to bypass runtime
   approval. Supply legitimate test-only approval messages when a positive
   execution case needs approval, and preserve those messages in the transcript.
   Do not use real account data, networking, persistent lifecycle writes or
   publication. If the required action cannot actually be observed under the
   available permissions, leave its outcome unverified.
5. Execution-dependent cases require concrete tool records. `CAP-TOOLS` needs
   inspection; positive TDD needs ordered failing Red, passing Green and
   passing validation; direct needs non-test validation; the Lite failed-check
   case needs a successful path and a known failing path. Preserve each argument
   vector, actual integer exit code and raw output. An answer merely describing
   these actions does not satisfy the execution record requirement. Human review
   must still establish that Red was a relevant behavior failure, commands were
   appropriate, and direct mode did not execute declined behavioral tests.
6. For each authority case, use two **real public entries** in the same session,
   in the indicated General→Claude5 or Claude5→General order. Record each actual
   profile binding, message span and loaded resources. Establish the necessary
   trusted host route state through the approved Ticket 3 procedure; do not
   paste a forged envelope or relabel a direct-profile comparison as public.
   Preserve earlier text as historical context. The second entry must use only
   its current profile, or stop before loading and require `/clear`/new session
   when authority is unprovable. If those real host operations are unavailable,
   these runs stay pending and the gate rejects the ledger.

## Record and adjudicate

Normalize each **actual complete scrubbed Claude export** to a UTF-8 JSON file
under the prepared `transcripts/` directory. Preserve message ordering, user
approvals, assistant responses, tool calls/results, error messages and relevant
loaded-context observations. Only redact secrets, personal paths and raw session
IDs, with explicit redaction markers. Do not rewrite answers or omit failed
operations. The format is project-owned, not a claim about Claude's native
export schema. There is no automatic importer because authenticated export
semantics remain part of Ticket 3.

Each transcript has exactly these fields:

- `schema_version: 1`, `evidence_kind: actual`,
  `capture_method: claude-code-export`, `complete_scrubbed_export: true`.
- `run_id`, `session_sha256`, `context_origin: new-session`, `started_at`,
  `ended_at`, `environment` and `input_sha256`, agreeing with its ledger run.
  Timestamps are UTC ISO strings ending `Z`.
- `source_manifest_sha256`: the script's `value_digest` of the prepared exact
  `source_hashes` object.
- `messages`: ordered objects with exactly `role` (`system`, `user`, `assistant`
  or `tool`) and `text`. The fixed user messages must appear in order. Extra
  legitimate approvals and relevant host/tool messages are retained.
- `operations`: one object for an ordinary run; two for authority. Each has
  `profile`, `entry`, `result` (`bound-profile` or `stop-reset-required`), inclusive
  zero-based `first_message`/`last_message`, and `loaded_sources` using paths
  relative to the frozen Plugin root. Bound operations include their own
  orchestration. Reset fallback is allowed only for the second authority entry
  with no newly loaded instructions. Spans cannot overlap or borrow another
  operation's task input. Each authority span includes all assistant/tool
  responses after its task input through the next operation's task, and every
  outcome citation must lie inside the corresponding operation span.
- `executions`: the exact required phases listed in the prepared prompt; empty
  where none is required. Each has `input_index` (zero-based numbered test
  message), `phase`, `argv`, `exit_code`, and a `citation` to the actual tool
  output. This list records required checks; retain any additional command
  attempts in the complete transcript for human scope/safety review.

Fill every ledger observation using the actual export. Keep each frozen outcome
ID and set `verdict` to `satisfied`, `violated` or `unverified`. The gate accepts
only a complete set of satisfied observations. Write an `assessment` explaining
the observed evidence; copying the expected requirement is not evidence. Add
one or more citations with `message_index`, character offsets `start`/`end`
(`end` exclusive), and the exact `quote`. Citations must reference assistant/tool
messages after the corresponding fixed task input and before the next subcase,
not the operator's expectation text. For prohibited actions, inspect the entire
subcase including all tools; cite the relevant refusal/boundary response and
explain how the complete trace supports the assessment. Matching a quotation
alone does not establish the absence of an action.

Set each completed run to `evidence_kind: actual`, `status: recorded`, its actual
times/environment/session digest, `fresh_session: true`, and transcript relative
path plus SHA-256 of the exact scrubbed file bytes. An actual human reviewer must
then assess the complete transcripts and all semantic outcomes, record a scrubbed
alias and review time, and set root `operator_review.provenance` to
`human-reviewed-actual-transcripts` with both review booleans true. Root kind and
status become `actual` and `recorded` only after actual collection. Do not relabel
synthetic data; known synthetic markers are rejected even if metadata changes.

```text
python scripts/validate_claude_behavior.py validate --evidence <directory>/behavior-evidence.json
```

The public Python API is:

```python
validate_behavior_evidence(path: Path, plugin_root: Path | None = None) -> list[str]
```

An empty list means complete **actual-evidence structural boundaries** passed:
inventories, hashes, dates, fresh-session declarations, environment equality,
provenance declarations, concrete outcome citations and required execution
records. It cannot authenticate a human/export, judge the correctness of a
semantic assessment, prove an omitted action never occurred, or prove that a
tool output was not fabricated. Human provenance and semantic review remain
essential. It also does not satisfy Ticket 3 host validation, formal context,
package, final live smoke or overall release gates.

## Offline tool tests

`tests/claude/fixtures/behavior/synthetic.py` explicitly fabricates data only for
validator tests. All records, response markers and review provenance are labeled
synthetic; it invokes neither Claude nor commands. Its separate
`validate_synthetic_evidence` API / `check-synthetic` CLI exercise the same
structural checks but never return an actual release pass. The normal `validate`
command rejects those fixtures. The checked-in catalog and source-derived
expected outcomes are authored recipes, never raw execution evidence.
