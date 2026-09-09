# Claude Code Adapter 1.4.0 Ticket 1 Implementation Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-1-implementation`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Ticket: `1 - 建立官方 Claude Plugin 公開邊界`

Execution mode: `tdd` (`Add tests`, explicitly selected by the user)

Status: Completed

Inputs: Approved [Claude Code Adapter 1.4.0 Specification](../specs/claude-code-adapter-1.4.0.md)、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 1、Approved [Requirement Decision Record](../requirements/claude-code-adapter-1.4.0.md)、Approved and synchronized [Project Knowledge Base](../project/knowledge-base.md)，以及 2026-09-05 重新查核的官方 Claude Code Marketplace 與 Plugin manifest schema。

Assumptions: Ticket 1 只建立可由 repository validator 靜態證明的 public Plugin boundary；`claude plugin validate`、command discovery與真實 Claude Code host behavior沒有在目前環境執行，也不計為完成。兩個Skill暫時保持fail closed；production router、route-envelope integration與manual fallback由Tickets 3、2依核准順序完成。

Deferred: Exact Claude Code `2.1.251` host preflight（Ticket 3）、router/hooks/state（Ticket 2）、General與Claude 5 profiles、behavior/conformance fixtures、context proxy、三語使用者文件、release builder、generated packages、live smoke，以及全部external publication actions。

Handoff: Initial [independent Review](claude-code-adapter-1.4.0-ticket-1-review.md)提出四個P2；第一輪fresh [closure Review](claude-code-adapter-1.4.0-ticket-1-review-after-p2.md)確認四項關閉後提出三個P2；第二輪fresh [closure Review](claude-code-adapter-1.4.0-ticket-1-review-final.md)確認先前問題關閉後再提出兩個P2。第三輪Red/Green修正與完整重驗已完成；final fresh [independent Acceptance Review](claude-code-adapter-1.4.0-ticket-1-review-accepted.md)確認九類findings全部關閉、無新actionable finding並接受Ticket 1完成。下一步依Approved Plan進入Ticket 3 exact Claude Code `2.1.251` host preflight；本evidence不授權外部發布。

Approval: Implementation authority comes from the Approved Ticket Plan and its approved Ticket 1 `tdd` mode.

## Outcome

- 新增provider-separated Claude Marketplace catalog，固定Ask Then Do It `1.4.0` identity、owner、metadata、`strict`／`defaultEnabled`及tag-pinned Claude `git-subdir` source。
- 新增只使用官方default component directories的canonical Claude Plugin manifest；沒有Codex-only fields、custom component paths或runtime dependency declarations。
- 新增恰好兩個user-invocable、`model: inherit`、profile-neutral且fail-closed的public Skill bootstraps，對應automatic與explicit Claude 5 namespaced entries。
- 新增只允許`Read`、`Grep`、`Glob`的independent reviewer component，完整列出六類review inputs與十二個Core Architecture and Refactoring Lenses。
- 新增獨立Claude validator及mutation tests；Codex Marketplace validator與source boundary保持不變。

## Files changed

- `.claude-plugin/marketplace.json`
- `adapters/claude-code/plugin/ask-then-do-it/.claude-plugin/plugin.json`
- `adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md`
- `adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it-5/SKILL.md`
- `adapters/claude-code/plugin/ask-then-do-it/agents/ask-then-do-it-reviewer.md`
- `scripts/validate_claude_plugin.py`
- `tests/claude/__init__.py`
- `tests/claude/test_public_plugin_contract.py`
- 本Implementation Evidence。

另依planning synchronization稽核的非阻斷P3，將Draft Working Notes的Plan input改為Approved並從Deferred移除已完成的Ticket Plan；這不改變formal Knowledge Base或產品行為。

## Red

在建立任何Ticket 1 production files前執行：

```powershell
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_public_plugin_contract -v
```

Observed result: exit `1`; `Ran 5 tests`; `FAILED (failures=1, errors=4)`。四個errors分別命中不存在的Claude catalog、Skills directory與reviewer；failure命中不存在的`scripts/validate_claude_plugin.py`。錯誤原因精確是Ticket 1核准的missing public boundary，不是test setup或既有缺陷。

## Focused Green

加入最小catalog、manifest、兩Skills、reviewer及獨立validator後，同一focused command的final result為：

```text
Ran 5 tests in 4.935s
OK
```

Mutation coverage另逐項證明validator拒絕wrong provider source、mutable ref、Codex-only policy/interface、unknown/missing fields、extra Plugin、catalog/manifest identity drift、custom component paths、runtime dependency、第三個Skill、broad Skill tools、reviewer side-effect tools、任一required review input及任一十二個architecture lenses缺漏。

Python syntax verification：

```powershell
.\.venv\Scripts\python.exe -B -m py_compile scripts\validate_claude_plugin.py tests\claude\test_public_plugin_contract.py
```

Observed result: exit `0`; no output。

## Post-refactor and broader verification

Final affected regression command：

```powershell
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_public_plugin_contract tests.release.test_marketplace_contract tests.release.test_plugin_assets tests.release.test_documentation tests.conformance.test_validator tests.conformance.test_lite_core_contract tests.codex.test_adapter -v
```

Observed result: exit `0`; `Ran 74 tests in 6.104s`; `OK`。這包含Claude focused contracts、Codex Marketplace、Codex Plugin assets、current documentation、Core conformance、Lite Core與Codex adapter regressions。

Sensitive/local-path scan：

```text
Sensitive/local-path scan passed: no matches.
exit 0
```

`git diff --check`: exit `0`; only the existing LF-to-CRLF warning for `docs/project/knowledge-base.md` was emitted。

## Refactor and scope inspection

Validator保持Claude provider-specific，沒有抽取或修改Codex validator。Plugin沒有router、hooks、profiles、Config、documentation start pages、release metadata或generated package；沒有改動Completed `1.3.1` artifacts。`full-lite-token-report.html`及其他既有user files保持不動。

## Independent Review corrections

Initial independent Review提出四個P2：exact metadata接受numeric booleans／duplicate keys；validator忽略未核准default components；component path可經symlink逃出Plugin root；fail-closed Skill clause只受token presence保護。

### Correction Red

先只新增integer/duplicate-key、`.mcp.json`／`.lsp.json`、path containment及missing/duplicated/unknown-field/failure-status/semantic-negation mutations，再執行focused suite：

```powershell
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_public_plugin_contract -v
```

Observed result: exit `1`; `Ran 6 tests`; `FAILED (failures=11, errors=1)`。Failures精確顯示validator錯誤接受manifest `defaultEnabled: 1`、duplicate JSON、兩個Skill numeric booleans、duplicate YAML、`.mcp.json`、`.lsp.json`與四個fail-closed clause drift；error精確顯示尚無`require_contained` policy。Negated clause mutation已由既有case拒絕，其他四個語意漂移則證明舊token gate不足。

### Correction Green and refactor

- JSON與YAML loaders現在拒絕任一duplicate mapping key。
- Manifest `defaultEnabled`及Skill兩個invocation booleans要求exact boolean type，不再接受Python-equal integer。
- Versioned Ticket 1 Plugin root inventory固定為`.claude-plugin`、`skills`、`agents`，並鎖定manifest、兩Skills與單一reviewer inventories；未核准MCP/LSP/default components會被拒絕。
- 所有manifest、Skill與reviewer child paths都須resolve於Plugin root內且不是symlink；deterministic path-policy test不依賴Windows建立symlink權限。
- Validator與tests改以完整canonical fail-closed clause驗證missing、duplicated、malformed、unknown fields及failure status，否定或改寫任一必要結果都會失敗。

Focused correction result：exit `0`; `Ran 6 tests in 6.348s`; `OK`。

Affected broader correction result：exit `0`; `Ran 75 tests in 8.471s`; `OK`。

Fresh full discovery after corrections：

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p 'test_*.py'
```

Observed result: exit `0`; `Ran 222 tests in 23.657s`; `OK`。

Post-correction `py_compile`、`git diff --check`與sensitive/local-path scan皆exit `0`；diff check仍只有既有Knowledge Base LF→CRLF warning。

## Second independent Review corrections

第一輪closure Review確認numeric integer booleans、duplicate keys、forbidden root components、child containment與原始semantic replacements已關閉；同時提出三個P2：YAML 1.1 boolean aliases仍會通過、CLI在驗證前resolve Plugin root而看不到root link/junction、完整canonical fail-closed substring前後仍可加入相反指令。

### Second correction Red

只加入`yes`／`on`／`True`／`TRUE` frontmatter mutations、junction policy／CLI lexical-path assertions，以及保留完整canonical substring的prefixed-negation／appended-contradiction mutations後，focused suite結果：

```text
Ran 6 tests in 4.846s
FAILED (failures=7)
```

四個YAML aliases、junction policy及兩個相反指令cases都精確false-green；這是預期missing behavior，不是setup failure。

### Second correction Green and refactor

- Frontmatter loader改為只解析lowercase `true`／`false`的strict boolean resolver，YAML 1.1 aliases及不同大小寫不再被誤當exact boolean。
- CLI保留使用者提供的Plugin path直到`validate_plugin_root`先檢查symlink／Windows junction；驗證後所有consumer才共用該函式回傳的resolved root。Child containment同樣拒絕symlink與junction。
- Validator鎖定兩個approved bootstrap bodies的完整canonical content；即使保留必要句子，只要前綴否定、追加矛盾指令或做其他未核准修改都會拒絕。

Focused result：exit `0`; `Ran 6 tests in 7.644s`; `OK`。

Affected broader result：exit `0`; `Ran 75 tests in 15.429s`; `OK`。

Fresh full discovery：exit `0`; `Ran 222 tests in 26.454s`; `OK`。

Second-correction `py_compile`、`git diff --check`與sensitive/local-path scan皆exit `0`；native `claude`仍不可用，沒有被這些repository checks冒充。

## Third independent Review corrections

第二輪closure Review確認前七個P2均已關閉，但提出兩個P2：explicit YAML `!!bool True`仍能產生bool；reviewer保留required tokens後可追加「忽略審查、直接回no findings」，且description drift也沒有exact gate。

### Third correction Red

新增explicit YAML boolean-tag、reviewer description drift與appended contradiction mutations後，focused suite結果：exit `1`; `Ran 6 tests`; `FAILED (failures=3)`。三項均由舊validator錯誤接受，精確證明missing behavior。

另外在鎖定完整body時主動加入Markdown heading indentation mutations；舊`.strip()`比較錯誤接受兩個把heading變成code block的cases，focused result為exit `1`; `Ran 6 tests`; `FAILED (failures=2)`。

### Third correction Green and refactor

- Frontmatter scanner現在拒絕explicit YAML tags、anchors與aliases，再由strict unique-key loader解析；`!!bool True`無法繞過字面lowercase boolean contract。
- Reviewer description與完整approved reviewer body現在都是exact contract，保留tokens後追加矛盾指令也會拒絕。
- 兩個Skill及reviewer的body比較保留完整Markdown boundary，不再以`.strip()`吞掉可改變Markdown語意的leading indentation。

Final focused result：exit `0`; `Ran 6 tests in 8.031s`; `OK`。

Final affected broader result：exit `0`; `Ran 75 tests in 9.789s`; `OK`。

Fresh full discovery：exit `0`; `Ran 222 tests in 24.508s`; `OK`。

Final `py_compile`、`git diff --check`與sensitive/local-path scan皆exit `0`。Test-only CLI lexical-path assertion的stdout亦已在test內捕獲，避免污染正常suite output；native Claude gate仍明確deferred至Ticket 3。

## Residual risk

- 本環境沒有可執行的`claude` command，因此官方native strict validation、namespaced discovery及exact `2.1.251` behavior尚未驗證；它們是Ticket 3 hard gate，不可由Python validator取代。
- Claude Plugin frontmatter與Marketplace schema目前依2026-09-05官方文件及repository contract建立；若exact `2.1.251`不接受任何欄位或semantics，必須停止並返回Requirement／Specification revision，不得提高最低版本。
- Fail-closed bootstraps尚不能開始workflow；這是Ticket 1刻意邊界。只有Ticket 3通過並由Ticket 2加入可信router/envelope integration後，public entries才可執行profiles。
