# Claude Code Adapter 1.4.0 Ticket 5 Implementation Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-5-implementation`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Ticket: `5 - 交付 Claude 5-optimized profile 的完整工作流程`

Execution mode: `tdd` (`Add tests`, explicitly selected by the user)

Status: Correction accepted - mandatory model-behavior evidence pending

Inputs: Approved [Claude Code Adapter 1.4.0 Specification](../specs/claude-code-adapter-1.4.0.md)、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 5、Approved [Requirement Decision Record](../requirements/claude-code-adapter-1.4.0.md)、Completed Ticket 2 router/public bootstrap contracts、Core `1.3.1` rules/modules/artifact contracts，以及repository中的 [Claude Code feasibility analysis](../claude_sys/claude-code-adapter-feasibility-analysis.md) 與其Anthropic Claude 5 context-engineering引用。

Assumptions: Current evidence is superseded by [Ticket 5 third-correction evidence](claude-code-adapter-1.4.0-ticket-5-third-correction.md). The replacement gate proves fixed whole-source instruction integrity and evaluation of closed declared decision tables only. The 30-scenario catalog now includes 66 structured static reference cases; they are not executed Claude traces. Authenticated Ticket 3 and mandatory model behavior under Ticket 6 remain pending. This evidence does not establish Ticket completion.

Deferred: Ticket 6 paired equivalence與fresh-session harness、Ticket 7每情境50% context proxy、authenticated Ticket 3/live smoke gates，以及所有tag、push、GitHub Release、Marketplace activation/submission/announcement。

Handoff: The [fresh independent Review](claude-code-adapter-1.4.0-ticket-5-review-after-third-correction.md) accepted the final third-correction modules and direct-architecture lens follow-up with no unresolved actionable finding. [Central integration](claude-code-adapter-1.4.0-profile-correction-integration.md) records the final 349-test regression, native validation and both profile Reviews. Obtain the missing model-behavior evidence before marking this Ticket Completed; static/table passes do not authorize a context-reduction claim.

Approval: Implementation authority comes from the Approved Ticket Plan、其Ticket 5 `Add tests`／`tdd` mode，以及使用者核准繼續Claude Adapter實作的明確指示。

## Historical implementation and earlier correction record

The following outcome descriptions and raw results record earlier implementation states. The third-correction evidence linked above supersedes prior descriptions of the regex oracle, fixture shape and completion strength; historical raw command results are preserved.

## Outcome

- 新增`profiles/claude-5/`恰好十個internal Markdown modules；沒有子目錄、frontmatter、hidden public command或額外Skill component。
- Public bootstrap與optimized orchestration使用exact`${CLAUDE_PLUGIN_ROOT}/profiles/claude-5`資源協定；closed filename allowlist每次只選一個stage module，並要求contained、regular、non-link target，禁止路徑輸入、預載全部modules、跨profile載入/服從與active-model override。
- 十個modules以`Core rules:` trace覆蓋`core/rules/rules.yaml`全部30條mandatory IDs，沒有未知ID或profile exemption。
- 固定30-scenario fixture只保存scenario ID與module inputs；test-owned independent oracle逐項驗證conversation/tools/multi-agent capability、Full/Lite lifecycle、requirements/knowledge/spec/plan/TDD/direct/Review/architecture gates、automatic/explicit/failure/switch routing、session lifecycle、install/status/update/remove/ZIP、docs/package與release integrity。Core rule labels只作supplementary trace。
- Entry invariant明確接受ready Claude 5 operation binding，以及兩個public-bootstrap-controlled manual states：valid`node-too-old` failure envelope與受支援Claude Code下的genuinely-missing Node。Manual entry明示model未驗證、automatic unavailable與Node升級需求，且不得虛構operation binding、resume authority或switch tracking；其他failure停止。
- Claude `.claude/ask-then-do-it.toml` precedence、invalid fail-closed、read-only/no-persistence、operation-bound profile、next-permitted-entry reroute與`/clear`/new-session安全fallback均明示。
- Full Review在可用時使用Plugin的independent read-only reviewer；不可用時明示`non-independent`，conversation-only則`limited-evidence`。Lite保持same-context compact Review，不被升級。
- 保留user-scope lifecycle、disabled/no-op/newer/source/scope/partial-failure矩陣、reload/new-session、session-only ZIP、三語與三family release/publication邊界；未宣告paired equivalence或正式context reduction。
- Full orchestrator明列四個architecture diagnosis triggers、automatic-route announcement、focused-local finding留在Review、accepted report只回Specification；Approved/accepted artifact的durable-knowledge changes必須揭露additions/modifications/removals並取得精確approval，無durable fact不得製造更新或延誤gate。

## Files changed

- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/orchestration.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/lite-workflow.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/requirements.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/documented-requirements.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/specification.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/ticket-planning.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/tdd-implementation.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/direct-implementation.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/review.md`
- `adapters/claude-code/plugin/ask-then-do-it/profiles/claude-5/architecture-improvement.md`
- `tests/claude/fixtures/claude-5-profile/scenarios.json`
- `tests/claude/test_claude5_profile.py`
- 本Implementation Evidence。

## Red evidence

Command after adding only the optimized-only tests/fixture and before any profile production file:

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_claude5_profile
```

Observed raw summary:

```text
Ran 5 tests in 0.011s

FAILED (failures=34)
```

The failures were the expected missing behavior: `profiles/claude-5/` did not exist, so the exact ten-module inventory, all 30 scenario clauses, all 30 Core rule traces, progressive loading, routing/Config/lifecycle/reviewer branches, and no-cross-profile/no-model-override contracts were absent. The helper reported each missing required module as an assertion rather than an environment/setup error.

## Focused Green evidence

Command after the ten optimized modules and small wording/refactor corrections:

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_claude5_profile -v
```

Observed raw summary:

```text
Ran 5 tests in 0.012s

OK
```

All five methods passed: exact progressive-disclosure inventory; exact 30-rule trace; exact 30-scenario inventory/outcomes; no cross-profile path/model override; and explicit routing/Config/lifecycle/reviewer downgrade.

## Refactor and adjacent verification

The original fixture-owned substring matcher was replaced after Review with a test-owned, branch-oriented contract oracle. The fixture now contains no expected phrases, while production mutations exercise reversed explicit-user routing, removed manual-entry guards, removed architecture/knowledge routes, and injected cross-profile/model-override instructions. Production instructions remain stage-specific and avoid copying detailed Core explanations into every module.

Adjacent router regression command:

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_router_contract tests.claude.test_router_state tests.claude.test_router_security -q
```

Observed raw result:

```text
Ran 45 tests in 26.180s

OK (skipped=1)
```

The skip is the existing Windows symlink-permission case, not a Ticket 5 behavior skip. A scoped `git diff --check` over the Ticket-owned profile/test files exited `0` with no output.

### Central shared-validator TDD closure

Profiles加入後，中央先執行shared validator focused Red；canonical validator仍使用pre-profile root inventory，因而拒絕規格要求的`profiles`目錄：

```text
Ran 2 tests in 0.282s

FAILED (failures=2)
```

中央更新後，canonical validator要求Plugin root包含`profiles`、該目錄恰有`general`與`claude-5`，且每個profile恰有規格固定的十個modules。Mutation tests另證明missing／extra profile、missing／extra module及profile path-guard drift都會被拒絕。Focused Green raw result：

```text
Ran 3 tests in 7.391s

OK
```

### Central combined and repository verification

Combined profile/public verification：

```text
Ran 23 tests in 13.869s

OK
```

Claude-focused suite：

```text
Ran 118 tests in 73.059s

OK (skipped=1)
```

Full repository suite：

```text
Ran 334 tests in 91.245s

OK (skipped=1)
```

唯一skip仍是既有Windows symlink-permission case。Canonical Claude Plugin validator、model-evidence validator、Node router syntax與`git diff --check`皆exit `0`；diff check只有既有Project Knowledge Base line-ending warning。Exact Claude Code `2.1.251`對Plugin與repository Marketplace執行strict validation皆exit `0`且無warning。這些結果關閉shared validator/profile inventory整合，不取代Ticket 3 authenticated behavior ledger。

## Approved Review corrections

[Ticket 5 Independent Review](claude-code-adapter-1.4.0-ticket-5-review.md)提出3×P2，使用者明確核准修正：F1 deterministic profile loading/manual entry contradiction、F2 mandatory Full architecture/durable-knowledge routes、F3 self-referential substring oracle。

### Correction Red

在修改production profile前，先移除fixture的`required`文字、建立test-owned 30-scenario oracle與四個adversarial production mutations，然後執行：

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_claude5_profile -v
```

Observed raw summary:

```text
Ran 6 tests in 0.089s

FAILED (failures=15)
```

Ten F1 subtest failures精確指出missing Plugin-relative orchestration path、immutable profile root、closed allowlist、containment/non-link guards、ready binding與兩個manual states/no-authority contract。其餘failures命中`FULL-ARCH`、`FULL-KNOWLEDGE`與`ROUTE-EXPLICIT-5`分支；不是test setup failure。Red run中的mutation method已成功拒絕反轉explicit-user selection、刪除manual guard、刪除architecture/knowledge routes與加入cross-profile/model override，證明新oracle不再接受Review展示的false-pass mutation。

### Correction Green and focused integration

最小production change只修改Claude 5`orchestration.md`，加入exact contained load protocol、三種合法entry states、四個architecture triggers與durable-knowledge handoff。Focused rerun：

```text
Ran 6 tests in 0.086s

OK
```

與中央更新的public bootstrap/shared Plugin contract合併後執行：

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_claude5_profile tests.claude.test_public_plugin_contract -v
```

Observed raw summary:

```text
Ran 19 tests in 14.790s

OK
```

`scripts/validate_claude_plugin.py`亦exit`0`並回報canonical Plugin validation passed。Ticket-owned scoped`git diff --check`exit`0`無輸出；production profile搜尋`profiles/general`、parent/general paths、model frontmatter/CLI override及active-model switch/override/pin文字均零命中。完整Claude/full repository重驗交由中央整合執行，不在平行Ticket ownership內重跑。

## Fresh Review after-correction findings and second correction

[Ticket 5 Fresh Independent Review After Correction](claude-code-adapter-1.4.0-ticket-5-review-after-correction.md)提出2×P2，使用者明確核准修正：ready entry的automatic／explicit bootstrap authority矛盾，以及`conversation` capability下Config source unavailable時缺少deterministic transition。

### Second correction Red

在修改production profile前，先加入ready-entry authority interaction test、explicit-only ready wording mutation、conversation Config unavailable interaction test，以及wrong stop-and-ask／fabricated-read mutations，然後執行：

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_claude5_profile -v
```

Observed raw summary:

```text
Ran 8 tests in 0.109s

FAILED (failures=4)
```

Failures精確命中兩個Review finding：既有ready entry gate排除automatic public bootstrap，以及`conversation` capability沒有project/user Config unavailable的fallthrough與capability-honest disclosure。這不是test setup failure；新增mutation亦證明explicit-only ready authority、錯誤stop-and-ask與虛構Config read不會被oracle接受。

### Second correction Green and focused integration

最小production change仍只修改Claude 5`orchestration.md`：ready state可由approved automatic或explicit public bootstrap建立；兩個manual states維持只能由explicit `-5` bootstrap建立，且不得虛構operation binding、resume authority或switch tracking。Host無法提供Config時明確視為`unavailable`並依Core當作absent；project unavailable繼續user Config，user unavailable使用Full fallback，且不得聲稱unavailable source已被讀取、存在或invalid。Focused rerun：

```text
Ran 8 tests in 0.105s

OK
```

與public Plugin contract合併後執行：

```powershell
& '.\.venv\Scripts\python.exe' -B -m unittest tests.claude.test_claude5_profile tests.claude.test_public_plugin_contract -v
```

Observed raw summary:

```text
Ran 21 tests in 16.517s

OK
```

Canonical `scripts/validate_claude_plugin.py` exit`0`；Ticket-owned scoped`git diff --check` exit`0`無輸出；cross-profile與active-model override搜尋零命中。完整Claude/full repository驗證仍由中央整合執行。

## Residual risks and evidence limits

- The 30 optimized scenario checks now use an independent branch-oriented static oracle and adversarial mutations; Ticket 6 still owns true fresh-session outcomes, paired equivalence, same-session bidirectional authority tests, and shared conformance integration.
- Ticket 7 still owns formal per-scenario context measurement. Module compactness here is an implementation technique, not a 50% reduction claim.
- Shared Plugin validator已以exact two-profile／ten-module inventory、mutation rejection與path guards完成中央整合；Ticket 1 public boundary未被弱化。
- Ticket 3 authenticated host ledger remains provisional/unverified. Native strict schema or static tests cannot substitute for authenticated `additionalContext`, command identity, loading, resume/switch, and failure observations.
- No General profile, shared validator, router, public Skill, reviewer, documentation, release file, README, historical artifact, Project Knowledge Base, external installation, or publication state was modified by this Ticket.
- A fresh independent Review is required before Ticket 5 may be marked Completed.
