# 驗證手冊

適用來源版本：1.4.1。此文件集合既有工具操作、Claude 實測程序及重要回歸測試對照；來源／已知缺口見[工作狀態](../project/status.md)。**離線測試、來源 integrity、simulated hook 結果與真實 Claude 行為是不同證據。** 不以其中一項代替全部驗收。

## 開發環境與一般檢查

使用[發布手冊](releasing.md#開發環境)指定的 CPython 3.12／PyYAML／Pillow，Claude 測試另需 Node.js 22+。以下 `python` 指已選定的開發環境 Python；Windows 本機可用 `.venv/Scripts/python.exe`。

```text
python -m unittest discover -s tests -v
python scripts/validate_marketplace.py
python scripts/validate_claude_plugin.py
python scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest adapters/codex/conformance.yaml
python scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest adapters/generic-prompts/manifest.yaml
python scripts/validate_conformance.py --catalog core/rules/rules.yaml --manifest adapters/claude-code/conformance.yaml
python scripts/measure_workflow_token_proxy.py --json
python scripts/validate_claude_model_evidence.py --mapping adapters/claude-code/plugin/ask-then-do-it/config/model-classifications.json --trace tests/claude/fixtures/model-classifications/source-trace.json
```

完整 suite 會建立並清理隔離 fixtures，不直接更新根目錄 dist。針對性套件可使用 `python -m unittest discover -s tests/claude -p test_documentation.py -v` 等既有 discovery 方式。Windows 無 symlink 權限時如實記錄 skip，不把未執行的分支記為已驗證。

## 工具責任與證據強度

| 工具（scripts/） | 用途與限制 |
| --- | --- |
| build_release.py | 三平台來源、inventory、ZIP、parity、checksum 與復原；不是 host／model 實測 |
| validate_marketplace.py | Codex catalog schema、identity、tag／source |
| validate_conformance.py | Core rule／capability declaration；不以檔案存在證明語意等價 |
| validate_release_evidence.py | required-check ledger 與 Completed 宣告；不自行執行或認證原始命令 |
| measure_workflow_token_proxy.py | Codex tools 固定 Full／Lite benchmark，Lite proxy 至少降低 60%；Generic composed prompt 是兩模式共同固定成本，單列且 `gate_applied: false`，不宣稱 Generic 60% 縮減或帳單保證 |
| validate_claude_plugin.py | Claude manifest、catalog、public components、router／profile 契約 |
| validate_claude_package.py | Python API：validate_source／source_payload／validate_parity；builder 呼叫，沒有獨立 CLI |
| validate_claude_model_evidence.py | exact model mapping 與 dated official snapshots、metadata／hash 連結 |
| validate_claude_host_contract.py | 指定 host ledger、來源與實測輸出結構；不能產生 authenticated observations |
| validate_claude_behavior.py | prepare 未執行的 recipes；validate 實際 scrubbed transcripts；check-synthetic 只測工具 |
| measure_claude_context.py | 通過 behavior gate 後計算實際載入的 Plugin-owned text，不是總 context／billing |

Plugin Skills 是 Markdown 產品指令；source-contract／reviewed-instructions fixtures 可拒絕漂移或語意反轉，但固定文字一致不代表模型已遵循指令。更新 prompt 需重做相關觀測，不能只更新預期字串宣布通過。

## 指定 Claude host 驗證

最低 Claude Code 2.1.251 的 exact executable 需驗證來源／hash、兩次 native `claude plugin validate <plugin-or-repository> --strict` 皆 exit 0 且無 warning、兩個 namespaced entries 的 command identity、UserPromptExpansion additionalContext、bare alias 的觀察，以及 Node missing／nonzero／exit 2／timeout 的 expansion 結果。驗證 version floor 不能只拿新版 binary 代替。

```text
python scripts/validate_claude_host_contract.py --ledger <host-ledger.json> --evidence-root <raw-host-evidence-directory>
```

參考 [host fixture](../../tests/claude/fixtures/host-contract/contract.json) 與 [host preflight tests](../../tests/claude/test_host_contract_preflight.py)。實測需隔離 session/config、停用自動更新並保留 exact binary provenance。Fixture marker 只供測試，不是 consumer Plugin。若 host 實際契約不符，回到規格修正，不悄悄提高最低版本或把 simulated 結果當真實結果。

## Claude behavior 證據

本程序承接原 behavior-verification.md 的完整操作與資料格式。prepare 不登入、不呼叫模型、不安裝外掛，也不會產生成功回答。來源改變後需重新 prepare，未驗證結果保留 unverified。實際模型呼叫與安裝等外部操作依該次明確授權執行。

### 準備


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
intentional. It is a test recipe, not the current canonical conformance
declaration. Current 1.4.1 declarations already exist; do not overwrite them
with staged-unverified fixture data.

### 執行實測

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

### 記錄與判讀

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

### 合成資料與離線工具測試

`tests/claude/fixtures/behavior/synthetic.py` explicitly fabricates data only for
validator tests. All records, response markers and review provenance are labeled
synthetic; it invokes neither Claude nor commands. Its separate
`validate_synthetic_evidence` API / `check-synthetic` CLI exercise the same
structural checks but never return an actual release pass. The normal `validate`
command rejects those fixtures. The checked-in catalog and source-derived
expected outcomes are authored recipes, never raw execution evidence.

## Claude loaded-context 量測

先完成兩 profiles 各 30 scenarios、12 paired cases 與雙向 authority（共 86 runs）的實際 behavior evidence，再準備 context capture：

```text
python scripts/measure_claude_context.py --prepare <new-capture.json>
python scripts/measure_claude_context.py --fixture <observed-capture.json> --behavior-evidence <directory>/behavior-evidence.json --json
```

十個固定 scenarios 的每個 stage-ready checkpoint，及 Full Review 的 reviewer-ready，各自需達到 `optimized * 100 <= general * 50`。不取平均抵銷失敗。計數保存 actual load order、每次注入的重複文字、raw hashes、NFC／whitespace normalization 後 bytes、`ceil(bytes / 4)` proxy 與來源；reviewer prompt 也計入。`--synthetic` 只提供診斷，不是 release pass。完整 counted／excluded material 定義見 [Claude 規格](../specs/claude-code-adapter.md)。

## 真實使用流程與發布驗收

至少一個乾淨真實本機環境須記錄 exact OS／surface／Claude Code／Node／canonical model／日期，完成 Marketplace add/install、兩入口、可用模型 route、model switch、session isolation、resume 或 compact、test-only older candidate update、remove、reinstall/recovery、release ZIP 的 session-only 載入。Unavailable branches 另用明示 simulated events 測試，不能冒充九組 OS／IDE 全部通過。

正式 release ledger 的完整性與三套件建置程序見[發布手冊](releasing.md)。真實 transcripts 的語意、人工作業與外部來源真偽不能只靠 JSON schema／hash 自動證明。

## 重要修正與回歸測試對照

歷次 Review 原文在[歷史快照](../evidence/release-history.md#archive)；下表保留維護時需要的問題類型與對應測試，而非逐輪審查流水帳。測試檔存在不代表本次已執行。

| 重要問題／邊界 | 回歸依據 |
| --- | --- |
| Codex／Claude schema 混用、YAML boolean／tag、未知欄位、精確公開元件、保留關鍵字的反向指令 | [public Plugin](../../tests/claude/test_public_plugin_contract.py)、[marketplace](../../tests/release/test_marketplace_contract.py) |
| Model mapping exact IDs、來源日期／URL／path、bool 冒充 integer、snapshot trace 漂移 | [model evidence](../../tests/claude/test_model_classification_evidence.py) |
| Node gate、bounded/fatal UTF-8 input、state/envelope union、不能把 state failure 當 unknown | [router contract](../../tests/claude/test_router_contract.py)、[schema validation](../../tests/claude/test_router_schema_validation.py) |
| cross-session、unsafe paths／symlink、lock ownership、最後重試與 stale-lock recovery、atomic state | [state](../../tests/claude/test_router_state.py)、[security](../../tests/claude/test_router_security.py)、[Review regressions](../../tests/claude/test_router_review_regressions.py) |
| 同一 operation profile authority、按需載入、Direct／Architecture prerequisites、指令缺失或反轉 | [General](../../tests/claude/test_general_profile.py)、[Claude 5](../../tests/claude/test_claude5_profile.py)，另需真實 behavior observations |
| synthetic evidence 冒充 actual、引用跨度、fresh session、paired inputs、執行階段證據 | [behavior evidence](../../tests/claude/test_behavior_evidence.py)、[context proxy](../../tests/claude/test_context_proxy.py) |
| incomplete／duplicate checks、錯誤 Completed、unverified Claude gates | [release evidence](../../tests/release/test_release_evidence.py) |
| Windows transient error、替換失敗、復原再失敗與保留 backup、二套件升級三套件 | [transaction](../../tests/release/test_release_transaction.py)、[safety](../../tests/release/test_release_safety.py) |
| ZIP duplicate／traversal／metadata、source parity、舊 preview 邊界 | [release contract](../../tests/release/test_release_contract.py)、[preview tests](../../tests/claude/test_release_preview.py) |
| same-version guide URL、三語命令、relative links、必需限制 | [release documentation](../../tests/release/test_documentation.py)、[Claude documentation](../../tests/claude/test_documentation.py) |

[回到 README](../../README.md)
