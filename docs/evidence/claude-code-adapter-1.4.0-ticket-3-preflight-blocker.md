# Claude Code Adapter 1.4.0 Ticket 3 Exact-Host Preflight Blocker Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-3-preflight-blocker`

Workflow ID: `claude-code-adapter`

Core version: `1.3.1`

Target release version: `1.4.0`

Ticket: `3 - 驗證 exact Claude Code 2.1.251 host contract`

Execution mode: `tdd` (`Add tests`, explicitly selected by the user)

Status: Blocked - Specification correction required

Inputs: Approved [Requirement Decision Record](../requirements/claude-code-adapter-1.4.0.md)、當時Approved的[Specification](../specs/claude-code-adapter-1.4.0.md)、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md)、Completed Ticket 1與其[accepted independent Review](claude-code-adapter-1.4.0-ticket-1-review-accepted.md)，以及Anthropic official release manifest、detached signature與Windows x64 binary for Claude Code `2.1.251`。

Assumptions: 本次只在隔離workspace temporary boundary使用exact binary；沒有安裝、修改PATH、呼叫`install`／`update`、啟用auto-update或修改既有Claude user state。Native stdout使用scrubbed logical paths呈現，未保存machine-specific absolute path。

Deferred: Marketplace correction核准與Ticket 1 TDD correction後，才可重新執行兩次native strict validation、namespaced discovery／invocation、`UserPromptExpansion.command_name`與`additionalContext`觀察、bare alias及四種failure semantics。Ticket 2與profiles不得開始。

Handoff: Exact-host gate已正確fail fast。返回Draft Specification correction；核准後回Ticket 1最早source owner修正、重驗、重新Review，再從頭重跑Ticket 3。不得忽略warning或把partial Plugin validation冒稱Ticket 3通過。

Approval: 使用者於2026-09-06明確核准下載與隔離驗證exact Claude Code `2.1.251`；該核准不等於Specification correction或後續implementation核准。

## Binary provenance and isolation

- Official version: `2.1.251`; manifest commit `37534ac596d80cefb02d272f036adba4ba055d2c`; build date `2026-08-28T15:09:02Z`。
- Windows x64 binary size: `217360032` bytes，與official manifest完全一致。
- Binary SHA-256: `8d1229a281281b98fd2dee72b3253a704be4fce4d45207200cd32a9bb5a6c909`，與official manifest完全一致。
- Windows Authenticode: `Valid`; signer `Anthropic, PBC`; signer certificate thumbprint `0D7581D2C51C59DF686C3000C70BF543F9F6C6CB`。
- `claude --version`: exit `0`; stdout `2.1.251 (Claude Code)`。
- Manifest與detached PGP signature已下載；本機沒有通用`gpg` command，且額外installer-script下載未獲准，因此未把detached-signature verification冒稱已完成。Manifest hash matching加上有效Anthropic Authenticode支持本次binary identity observation。
- Process-local隔離使用獨立`CLAUDE_CONFIG_DIR`並停用updates；所有invocations使用temporary binary absolute path，未修改PATH。

## Native strict observations

Canonical Plugin command：

```text
claude plugin validate <canonical-plugin-root> --strict
```

Observed: exit `0`。

```text
Validating plugin manifest: <canonical-plugin-root>/.claude-plugin/plugin.json

√ Validation passed
```

Repository Marketplace command：

```text
claude plugin validate <repository-root> --strict
```

Observed: exit `1`。

```text
Validating marketplace manifest: <repository-root>/.claude-plugin/marketplace.json

‼ Found 1 warning:

  > description: No marketplace description provided. Adding a description helps users understand what this marketplace offers

× Validation failed (--strict treats warnings as errors)
```

獨立重跑 repository root 與 manifest file，均重現相同的單一 warning 與 exit `1`。直接傳入 `.claude-plugin` directory 不是合法替代路徑，因為 Claude Code 會在其下尋找 `.claude-plugin/marketplace.json` 或 `.claude-plugin/plugin.json`，所以該形式也會失敗。

## Earliest affected gate

Approved Requirement Decision Record 要求 repository Marketplace strict validation exit `0` 且沒有 warning，但沒有限制 top-level field inventory。只有當時 Approved Specification 要求恰為 `name`、`owner`、`plugins`，使 strict-zero-warning requirement 在 exact `2.1.251` 上無法成立。因此這是 Specification-level external-contract correction，不是使用者意圖或最低版本的變更。

窄幅修正提議加入 exact top-level `description`，並要求它與唯一 Plugin entry 已核准的 independent-project description 完全相同。其他 Marketplace、Plugin、router、profile 與 release behavior 均不變。
