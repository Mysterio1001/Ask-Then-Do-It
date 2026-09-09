# Claude Code Adapter 1.4.0 Ticket 1 Independent Review Report

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-1-review`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Ticket: `1 - 建立官方 Claude Plugin 公開邊界`

Approved implementation mode: `tdd`

Review label: `independent`

Status: Changes requested (four `P2` findings open)

Inputs: Approved [Requirement Decision Record](../requirements/claude-code-adapter-1.4.0.md)、Approved [Specification](../specs/claude-code-adapter-1.4.0.md)、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 1、Approved [Project Knowledge Base](../project/knowledge-base.md)、Ticket-owned source/tests 的完整 working-tree snapshot、相關 Codex Marketplace／adapter contracts，以及 [Ticket 1 raw implementation evidence](claude-code-adapter-1.4.0-ticket-1.md) 中的 Red／Green／74-test 原始結果。Review 未採納 implementation evidence 的結論。

Assumptions: 目前 working tree 是待審 Ticket 1 candidate；Ticket-owned files 皆為 untracked，因此沒有可由 Git 顯示的新增檔 diff，但本 Review 已逐檔閱讀其完整內容並檢查 surrounding contracts。Approved Ticket 2 明確擁有兩個 bootstrap 的最小 route-envelope integration 與 explicit `-5` manual fallback，故 Ticket 1 現階段對 failure envelope 一律 fail closed 不另列 finding。

Deferred: Exact Claude Code `2.1.251` native strict validation、namespaced discovery與真實 host behavior依 Approved Plan 留給 Ticket 3；router/state、完整 route allowlists、兩條 explicit `-5` manual fallback依 Plan 留給 Ticket 2；profiles、behavior equivalence、context proxy、三語文件、release/package integration與live smoke均不在 Ticket 1 範圍。

Handoff: 將下列 findings 返回 Ticket 1 的 `$implement-tdd` 修正；先新增會失敗的 forbidden-component、path-containment、typed/duplicate-key與語意反轉 mutations，再修 validator並重跑 focused、broader與本 Review。四項 finding 未解前不得把 Ticket 1 評為完成或進入 Ticket 3。

## Findings

### P2 — Exact metadata parsing accepts numeric booleans and duplicate keys

Trigger: 將 Plugin manifest 的 `defaultEnabled`，或任一 public Skill 的 `disable-model-invocation`／`user-invocable`，由 JSON/YAML boolean `true` 改為數值 `1`；或在同一 JSON/YAML mapping 先放不安全值、再以相同 key 覆寫 approved 值。Impact: repository validator仍回報合法，雖然Approved Specification要求exact、無歧義的authored fields與boolean值；這會讓deterministic gate與Claude native parser／invocation authority分歧，直到Ticket 3才可能被host validator擋下。Evidence: `load_json`與`load_frontmatter`在`scripts/validate_claude_plugin.py:111-133`使用預設last-wins loaders；本Review實跑確認duplicate JSON解析為最後一個`defaultEnabled: true`、duplicate YAML解析為最後一個`model: inherit`。`validate_manifest`在`:203-205`只用`!=`，`validate_skills`在`:231-240`比較整個dict；Python中`1 == True`。In-memory mutation另得到`ACCEPTED manifest defaultEnabled=1`，並確認兩個Skill numeric booleans與expected dict相等。Catalog path在`:177-180`已有bool type guard，反證manifest／Skill path缺少同等檢查；現有tests沒有integer或duplicate-key mutations。Remediation direction: 使用拒絕duplicate mapping keys的JSON/YAML loaders，對三個boolean欄位使用`type(value) is bool`（或等價strict schema validation），並加入integer `0`／`1`與conflicting duplicate-key的CLI-level rejection tests。

### P2 — Forbidden Claude components are outside the validated inventory

Trigger: 在 otherwise-valid Plugin root加入`.mcp.json`或`.lsp.json`。Impact: `load_and_validate`仍成功，但Claude Code可把這些官方default components當成額外MCP／LSP能力載入，違反Specification禁止MCP/LSP與Ticket 1 excluded-component boundary；只檢查manifest未宣告custom path不足以證明runtime tree沒有該component。Evidence: `scripts/validate_claude_plugin.py:285-290`只驗manifest、`skills/`與`agents/`；`validate_skills`在`:215-216`只特判`commands`，沒有檢查`.mcp.json`、`.lsp.json`或完整allowed root inventory。`tests/claude/test_public_plugin_contract.py:304-375`也只mutate extra Skill、Skill tools與reviewer。Current canonical tree沒有這兩個檔案，但validator／TDD gate對此approved prohibition是false negative。Remediation direction: 驗證Ticket階段允許的Plugin root/default-component inventory並明確拒絕MCP/LSP及其他未核准component，加入兩個file-level mutations；未來Tickets加入hooks/profiles/scripts/config時以版本化allowlist擴充。

### P2 — Component resolution can escape the Plugin root through symlinks

Trigger: 將任一approved Skill directory／`SKILL.md`或reviewer path改成指向Plugin root外的symlink，但外部target保留expected name、frontmatter與body。Impact: validator會follow link並回報通過，使tag-pinned canonical source依賴或讀取source boundary外內容；在另一checkout/package中可能遺失或解析成不同bytes，破壞Ticket Plan明列的relative component resolution與supply-chain isolation。Evidence: `scripts/validate_claude_plugin.py:208-214`、`:227-229`及`:245-253`只使用`is_dir`／`is_file`／`read_text`，沒有對child做`resolve()`後確認`is_relative_to(plugin.resolve())`；現有tests也沒有path-containment mutation。Current component files已確認不是symlink，因此finding針對validator保證而非聲稱canonical tree已逃逸。Remediation direction: 對每個discovered directory/file解析real path、拒絕任何不在resolved Plugin root內的target及unsafe link，並在symlink-capable環境加入escape mutation；Windows無symlink權限時保留deterministic path-policy unit test。

### P2 — Fail-closed Skill behavior is protected only by token presence

Trigger: 保留字串 `Stop` 與所有 required tokens，但把 canonical clause 從 `Stop before beginning ... when [envelope invalid]` 改成 `Do not Stop before beginning ... when ...`。Impact: validator與現有 tests仍可全綠，卻會把 Ticket 1 最重要的 route-envelope trust boundary反轉為 fail open；錯誤或缺失 envelope 可能開始 operation。Evidence: `scripts/validate_claude_plugin.py:136-139` 的 `require_text` 只檢查 substring，兩個 Skills 在 `:221-242` 共用同一組 tokens；`tests/claude/test_public_plugin_contract.py:279-302` 也只做 `assertIn`。本 Review 以 canonical automatic Skill body做不落盤的語意反轉後，對同一組 validator requirements實跑得到 `ACCEPTED semantically inverted missing/invalid-envelope rule`。目前 canonical Skill 在 `adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md:12-18` 與 `skills/ask-then-do-it-5/SKILL.md:12-18` 的文字本身是 fail closed；finding 是 `tdd` gate 無法證明或保護該行為。Remediation direction: 為 bootstrap contract建立可確定驗證的 canonical clauses／結構化規則，並加入至少 missing、duplicated、unknown-field、failure-status及否定／反轉 stop rule 的 mutations；不能只以關鍵字存在作行為證據。

## Specification and Ticket assessment

| Review area | Outcome | Evidence |
| --- | --- | --- |
| Claude catalog identity與provider source | `passed` | `.claude-plugin/marketplace.json:1-40` 具有 exact top-level fields、單一 Plugin、approved owner/metadata、`strict: true`、`defaultEnabled: true`及 `v1.4.0` Claude `git-subdir` source；canonical validator與provider-boundary test通過。 |
| Canonical Plugin manifest | `passed-with-finding` | `plugin.json:1-23` 的 current bytes使用exact approved fields與boolean `true`，且與catalog相符；P2 finding指出validator未拒絕numeric boolean drift。 |
| 恰好兩個 public Skills | `passed-with-finding` | `skills/` current inventory恰為兩個 approved names，frontmatter是 user-only、`model: inherit`、無額外工具／commands；兩個 current bodies明文fail closed。P2 finding指出behavior mutation gate只做token matching。 |
| Reviewer static boundary | `passed` | `agents/ask-then-do-it-reviewer.md:1-44` 只允許 `Read, Grep, Glob`，包含六類 required inputs、finding fields、四種 lens outcomes與十二 lenses；逐項 removal及side-effect-tool mutations均被拒絕。 |
| Claude／Codex provider separation | `passed` | Claude validator未修改Codex validator；兩catalog互不指向對方source；Codex Marketplace regression通過。 |
| Excluded public components與relative resolution | `passed-with-findings` | current Plugin無`commands/`、第三個Skill、額外agent、MCP/LSP或custom manifest component paths，且current files不是symlink；但validator不拒絕`.mcp.json`／`.lsp.json`或root外symlink。Router/hooks/profiles缺席符合Ticket 1 partition。 |
| TDD mode與Red evidence | `partially verified` | supplied raw evidence記錄production files不存在時`Ran 5 tests`、`FAILED (failures=1, errors=4)`，失敗形狀與五個test methods的missing-file paths一致；為避免修改candidate未重演歷史Red。Final focused與broader Green已獨立重跑。四個P2顯示negative mutation coverage仍不足。 |
| Native Claude validation | `deferred` | 此環境找不到`claude` executable；依Approved Plan這是Ticket 3 hard gate，不以Python validator冒充。 |

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — `no-finding`.** Catalog／manifest identity及test oracle有刻意重複，但它們分別是consumer metadata、repository gate與獨立regression assertion；在Ticket 1範圍未發現造成錯誤authority的額外副本，Claude與Codex policy亦保持分離。
2. **Long Function — `no-finding`.** Production validator以`validate_marketplace`、`validate_manifest`、`validate_skills`、`validate_reviewer`分工；最長production routine仍是單一邊界驗證責任，沒有因長度隱藏控制流程。
3. **Large Module or Class — `no-finding`.** `validate_claude_plugin.py`雖同時涵蓋catalog、manifest、Skills與reviewer，但這些共同構成Ticket 1的一個public Plugin boundary；沒有不相關runtime/router責任混入。
4. **Long Parameter List — `no-finding`.** Helpers最多接受三個具名概念，沒有不穩定coordination interface。
5. **Data Clumps — `no-finding`.** Metadata與envelope field groups已集中為constants；未觀察到同一批鬆散參數跨函式反覆傳遞。
6. **Primitive Obsession — `finding`.** Exact boolean與unique-key domains靠寬鬆primitive loaders/equality判定，使integer `1`冒充`true`且duplicate key被last-wins折疊；對應第一項P2，位置`validate_claude_plugin.py:111-133`、`:203-205`、`:231-240`。
7. **Feature Envy — `no-finding`.** 各validation routine主要操作自己所擁有的catalog／manifest／component資料，沒有反覆伸入另一模組內部狀態。
8. **Divergent Change — `no-finding`.** 本Ticket的validator只因同一public-boundary contract變更；router、profiles、release integration由後續Tickets擁有。
9. **Shotgun Surgery — `no-finding`.** Exact identity本來就必須在catalog與manifest各自宣告；validator constants與tests可在同一Ticket一併更新，未見額外跨模組行為散落。
10. **Message Chains — `not-applicable`.** Reviewed production code是淺層dict與filesystem boundary validation，沒有長物件導航或call chain。
11. **Leaky Abstraction — `finding`.** Validator的success surface沒有揭露它忽略未核准default components、會follow root外symlink，並把「字串出現」當成「fail-closed語意成立」；caller必須理解這三項未受保護的implementation details。對應第二至第四項P2，位置`validate_claude_plugin.py:136-139`、`:208-253`、`:285-290`。
12. **Shallow Module — `no-finding`.** CLI以單一入口隱藏JSON/YAML parsing、exact field、inventory、provider及reviewer checks，介面相對其功能仍有足夠價值。

本次沒有跨模組或systemic architecture finding，因此不需要路由至Architecture Improvement Report。

## Verification performed

- `.\.venv\Scripts\python.exe -B scripts\validate_claude_plugin.py` → exit `0`，canonical Claude Plugin validation passed。
- `.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_public_plugin_contract -v` → exit `0`，`Ran 5 tests in 4.642s`，`OK`。
- Approved broader command（Claude public contract、Codex Marketplace/assets/docs、Core conformance/Lite、Codex adapter）→ exit `0`，`Ran 74 tests in 6.580s`，`OK`。
- 額外完整discovery `.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v` → exit `1`，`Ran 221 tests in 27.302s`，唯一failure為既有`release.test_release_safety...test_clean_builds_are_byte_reproducible_and_zips_match_directories`在temporary release replacement遇到Windows `WinError 5`；同一test立即隔離重跑→exit `0`，`Ran 1 test in 1.081s`，`OK`。另一個fresh independent audit的完整discovery亦為`221/221` pass，因此未把此瞬時非Ticket-owned failure升為Ticket 1 finding，但保留為flaky evidence。
- `.\.venv\Scripts\python.exe -B -m py_compile scripts\validate_claude_plugin.py tests\claude\test_public_plugin_contract.py` → exit `0`。
- `git diff --check` → exit `0`；只有既有`docs/project/knowledge-base.md`的LF→CRLF working-copy warning。
- Ticket-owned source/test的credential與machine-local absolute-path scan → exit `0`，no matches。
- Node availability → `v24.19.0`；符合後續automatic-router最低版本，但Ticket 1沒有router。
- In-memory negative probes：manifest numeric boolean被接受、Skill numeric booleans與expected mapping比較相等、JSON/YAML duplicate keys被last-wins折疊、語意反轉的invalid-envelope rule仍通過`require_text`。Static control-flow audit確認MCP/LSP files未被enumerate且component reads未做resolved-root containment。
- Current component files均為一般檔案，未觀察到symlink target。

## Evidence unavailable, residual risks, and untested areas

- `claude` CLI不可用，故未執行兩個`claude plugin validate <path> --strict`、實際namespaced discovery、bare-alias observation或host schema parsing；這是Approved Ticket 3的明確hard gate。
- Historical Red chronology只能由supplied raw evidence核對，無法在不移除current production files的前提下獨立重演；該raw failure shape與test source一致，但沒有獨立timestamp／transcript hash。
- Full-suite單次執行曾在unrelated release-safety temporary replacement遇到`WinError 5`；隔離重跑與另一個fresh run均通過，但本Review不把第一次nonzero隱藏，也不宣稱full suite每次穩定通過。
- Ticket-owned新增檔仍是untracked，Git無法提供與base逐行比較的final diff；本Review改以逐檔完整內容、inventory及working-tree status檢查。
- Current authored files沒有duplicate keys、MCP/LSP components或symlinks；缺口在validator與negative gates。Native strict validation可能補抓部分schema問題，但不能取代Ticket 1的deterministic mutations。
- Router、route enum、manual fallback、profile module、package exclusion、context及live behavior均尚未存在；依Approved Plan不是Ticket 1未完成證據，但後續Tickets仍須各自建立behavior gates。

## Completion assessment

Approved Ticket 1 **尚不應評為完成**。Current canonical catalog、manifest、兩個fail-closed Skills與read-only reviewer本身符合大部分static boundary，且focused與74-test regression均綠；然而四個P2證明repository validator／TDD suite會對forbidden components、root外component resolution、ambiguous/non-boolean metadata及反轉fail-closed語意的candidate產生false green。修正並以新增Red mutations重驗、再由independent Review確認前，completion gate維持未通過。
