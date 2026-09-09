# Claude Code Adapter 1.4.0 Ticket 1 Marketplace Description Correction Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-1-marketplace-description-correction`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Target release version: `1.4.0`

Ticket: `1 - 建立官方 Claude Plugin 公開邊界`

Execution mode: `tdd` (`Add tests`, explicitly selected by the user)

Status: Completed

Inputs: Approved corrected [Claude Code Adapter 1.4.0 Specification](../specs/claude-code-adapter-1.4.0.md)、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 1、Approved [Marketplace Description Knowledge Base Change Summary](../project/drafts/claude-code-adapter-marketplace-description-kb-change-summary.md)、prior [Ticket 1 Implementation Evidence](claude-code-adapter-1.4.0-ticket-1.md)與[accepted independent Review](claude-code-adapter-1.4.0-ticket-1-review-accepted.md)，以及exact Claude Code `2.1.251` [native preflight blocker evidence](claude-code-adapter-1.4.0-ticket-3-preflight-blocker.md)。

Assumptions: Exact-host finding只重開Ticket 1的Marketplace top-level `description` contract。先前accepted Review是當時repository-level bytes的歷史證據，不被改寫；其他catalog、Plugin、Skills、reviewer與provider-boundary contracts均保持不變。

Deferred: Fresh independent correction Review；通過後從頭重跑Ticket 3 namespaced discovery、`UserPromptExpansion`、bare alias與failure-semantics observations。Ticket 2、profiles、packages、live smoke及全部external publication actions仍未授權或未到順序。

Handoff: Fresh [independent correction Review](claude-code-adapter-1.4.0-ticket-1-marketplace-description-correction-review.md)已Accepted且無actionable finding；Ticket 1再次標為Completed，現在從頭重跑Ticket 3。本evidence不授權external publication。

Approval: 使用者於2026-09-06在Draft Specification correction、Knowledge Base Change Summary與exact-host blocker evidence完整展示後明確回覆「核准」，授權本次最小Ticket 1 TDD correction。

## Outcome

- Claude Marketplace authored top-level fields現在恰為`name`、`description`、`owner`、`plugins`。
- Top-level `description`精確重用唯一Plugin entry已核准的independent-project description，沒有引入第二份文案或新產品承諾。
- Claude validator要求欄位存在且值精確相同；missing、drifted或其他unknown field均fail closed。
- Exact Claude Code `2.1.251`現在對canonical Plugin與repository Marketplace兩個targets都以`--strict` exit `0`且沒有warning。

## Files changed

- `.claude-plugin/marketplace.json`
- `scripts/validate_claude_plugin.py`
- `tests/claude/test_public_plugin_contract.py`
- 本correction evidence；另依核准同步Specification、Project Knowledge Base、Knowledge Base Change Summary、Ticket Plan progress與Draft Working Notes。

## Red

先新增canonical top-level exact-key/value assertion，以及missing與drifted `description` negative cases，再執行：

```powershell
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_public_plugin_contract -v
```

Observed Red: exit `1`; `Ran 7 tests in 9.697s`; `FAILED (failures=3)`。三項failure分別證明canonical catalog缺少top-level `description`、舊validator錯誤接受missing mutation，以及drifted description只有unknown-field rejection而未實作exact-value diagnostic。沒有setup或無關failure。

## Green and refactor

- Catalog新增單一top-level `description`，bytes與唯一Plugin entry description相同。
- Validator的Claude catalog exact-key set加入`description`，並以既有單一`DESCRIPTION`常數驗證exact value。
- Focused test以同一`DESCRIPTION` oracle驗證canonical、missing與drifted cases，沒有複製第二份approved文案。

Focused Green: exit `0`; `Ran 7 tests in 8.741s`; `OK`。中央整合重跑同一command：exit `0`; `Ran 7 tests in 7.919s`; `OK`。

Static validator：

```text
Claude Plugin validation passed: <canonical-plugin-root>
```

Python `py_compile`對validator與focused test exit `0`。JSON parse確認top-level keys為`name,description,owner,plugins`且top-level與entry description exact equality為`True`。

## Exact Claude Code 2.1.251 native correction gate

Binary version、official manifest SHA-256與有效Anthropic Authenticode維持[preflight blocker evidence](claude-code-adapter-1.4.0-ticket-3-preflight-blocker.md)記錄的同一隔離binary。沒有安裝、修改PATH或使用較新版本替代。

```text
claude plugin validate <canonical-plugin-root> --strict
```

Observed: exit `0`; `√ Validation passed`; no warning。

```text
claude plugin validate <repository-root> --strict
```

Observed: exit `0`; `√ Validation passed`; no warning。原本唯一的missing-description warning已解除。

## Broader verification

- Affected broader command：Claude public contract、Codex Marketplace/assets/docs、Core conformance/Lite與Codex adapter；exit `0`; `Ran 76 tests in 10.744s`; `OK`。
- 第一次full discovery發現被中止的Ticket 3 worker留下未配對validator的半成品Red tests，exit `1`; `Ran 230 tests`; `FAILED (failures=10)`。這兩個未核准、未到順序的test-only files已移除，未改production behavior或弱化Ticket 1 tests。
- Fresh full discovery：exit `0`; `Ran 223 tests in 24.659s`; `OK`。
- `git diff --check` exit `0`；只有既有Project Knowledge Base LF→CRLF working-copy warning。

## Residual risk

- Marketplace strict validation問題已在exact `2.1.251`解除，但Ticket 3其餘host observations尚未執行，不能把本correction稱為Ticket 3完成。
- Detached PGP manifest signature尚未用release-signing key獨立驗證；binary SHA-256與official manifest一致，Windows Authenticode有效且signer為Anthropic, PBC。此provenance gap須在Ticket 3 evidence中誠實保留或補足。
- Ticket-owned source仍是working-tree/untracked candidate，沒有commit-level provenance；後續整合需由版本控制保存accepted bytes。
