# Claude Code Adapter 1.4.0 Ticket 1 P2 修正後獨立 Review Report

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-1-review-after-p2`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Ticket: `1 - 建立官方 Claude Plugin 公開邊界`

Approved implementation mode: `tdd`

Review label: `independent`

Status: Changes requested（3 個 `P2` findings open）

Inputs: Approved [Requirement Decision Record](../requirements/claude-code-adapter-1.4.0.md)、Approved [Specification](../specs/claude-code-adapter-1.4.0.md)、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 1、初次 [Independent Review](claude-code-adapter-1.4.0-ticket-1-review.md)、[Ticket 1 raw correction evidence](claude-code-adapter-1.4.0-ticket-1.md)、完整 Ticket-owned source／tests working-tree snapshot、Codex surrounding contracts，以及本次獨立執行的 focused、broader、full-suite 與 mutation probes。Reviewer context 沒有參與實作；raw implementation evidence 只作原始結果來源，未採納其完成 verdict。

Assumptions: 目前 working tree 是 Ticket 1 最終 closure candidate。Ticket-owned新增檔仍是 untracked，Git 無法提供其逐行 base diff，因此本 Review 逐檔閱讀 `.claude-plugin/marketplace.json`、`adapters/claude-code/plugin/ask-then-do-it/**`、`scripts/validate_claude_plugin.py`、`tests/claude/**`，並檢查 Codex／Core／release surrounding regressions。Ticket 2 擁有 production router、route-envelope allowlists 與 explicit `-5` manual fallback；Ticket 1 的兩個 bootstrap 現階段一律 fail closed 是核准切分。

Deferred: Exact Claude Code `2.1.251` 對 Plugin root與Marketplace root的native strict validation、namespaced discovery、frontmatter parsing及真實host behavior依Approved Plan留給Ticket 3；router/state、完整profiles、behavior equivalence、context proxy、三語文件、release/package integration與live smoke均不在Ticket 1範圍。Native Claude unavailable不會被Python validator取代或誤標為passed。

Handoff: 將下列三個findings交回Ticket 1的`$implement-tdd`。先新增YAML 1.1 boolean alias、CLI root symlink／Windows junction及保留canonical substring之否定指令的Red cases，再修正validator並重跑focused、75-test broader、full discovery與fresh independent closure Review。Findings關閉前不應完成Ticket 1或進入依賴其accepted Review的Ticket 3。

## Findings

### P2 — YAML boolean aliases仍繞過exact frontmatter gate

Trigger: 將任一public Skill的`disable-model-invocation: true`或`user-invocable: true`改成YAML 1.1 alias，例如`yes`或`on`。Impact: repository validator把該scalar解析成Python `bool`並回報合法，但Approved Specification要求明確、exact的`true` boolean；不同YAML schema／Claude host parser可能把同一source解讀成string或其他值，使deterministic gate與實際invocation authority分歧。Evidence: `UniqueKeyLoader`在`scripts/validate_claude_plugin.py:98-121`繼承`yaml.SafeLoader`的implicit resolvers，`load_frontmatter`在`:164-176`直接使用它；`:316-320`只比較解析後value與Python type。本Review確認`yes`、`on`、`True`與`TRUE`都被解析為`True`，並以不落盤的完整validator mutation把automatic Skill改為`disable-model-invocation: yes`，結果為`ACCEPTED`。現有tests在`tests/claude/test_public_plugin_contract.py:353-371`只覆蓋numeric `1`與duplicate key，未覆蓋跨YAML schema alias。Remediation direction: 使用與核准authored contract一致的strict YAML scalar schema，或在解析前後確定驗證canonical boolean spelling；加入至少`yes`／`on`及其他非核准boolean spelling的CLI-level rejection cases。Numeric `0`／`1`與JSON／YAML duplicate-key修正本身已確認有效。

### P2 — Plugin root symlink／junction可在root policy執行前被解參照

Trigger: 以指向另一個contract-shaped目錄的POSIX directory symlink或Windows junction作為canonical／`--plugin` root。Impact: validator可替不在lexical Plugin root內、且不一定能由tag-pinned `git-subdir`獨立取得的payload出具pass，破壞relative source containment與installability／supply-chain isolation。Evidence: `main()`在`scripts/validate_claude_plugin.py:378-388`先把`args.plugin.resolve()`傳給`load_and_validate`，所以`:198-200`的`plugin.is_symlink()`對CLI path已失去原始link identity；Windows junction本身另呈現`is_symlink=False`、`is_junction=True`，即使直接呼叫`validate_plugin_root`也被接受。本Review在隔離temporary Windows junction實跑CLI，canonical-shaped target得到`Claude Plugin validation passed`與exit `0`。現有`tests/claude/test_public_plugin_contract.py:407-436`只證明一個普通outside path會被`require_contained`拒絕並記錄canonical child guards，沒有CLI root-link mutation。Remediation direction: 在任何`.resolve()`前驗證原始Plugin root，跨平台拒絕symlink及junction／reparse-point等目錄連結，再一致使用已驗證的resolved root做child containment；新增POSIX symlink與Windows junction可用時的CLI-level negative tests。Manifest、Skill與reviewer child的resolved-root containment，以及current canonical tree沒有link，均已確認；本finding限於root boundary。

### P2 — 保留canonical substring即可加入相反的fail-open指令

Trigger: 保留完整canonical句子，但在前方加上`Do not `，形成`Do not Stop before beginning ...`；或保留該句後另加指示在envelope missing／failure時忽略stop rule並開始operation。Impact: validator與focused suite仍全綠，但bootstrap可收到直接反轉Approved fail-closed trust boundary的指令，使缺失或failure envelope開始operation。Evidence: `require_text()`在`scripts/validate_claude_plugin.py:179-182`只做substring presence；`validate_skills`在`:294-322`只要求`FAIL_CLOSED_CLAUSE`及其他tokens出現。本Review對automatic Skill分別執行preserved-substring prefixed negation及appended contradiction的完整in-memory validation，兩者都得到`ACCEPTED`。現有`tests/claude/test_public_plugin_contract.py:382-405`以replace改寫canonical phrase，五個cases都因移除required substring而失敗，沒有測到保留substring的語意反轉。Remediation direction: 對兩個versioned bootstrap採用可確定驗證的完整normalized body／section template（或等價、不依賴關鍵字存在的結構化契約），並加入保留canonical substring的prefix及additive contradiction mutations。Current兩個authored Skill bodies本身仍是fail closed；finding針對validator／TDD gate的false green。

## 初次四項 P2 closure assessment

| 初次finding | Outcome | 本次證據 |
| --- | --- | --- |
| Strict boolean與duplicate JSON/YAML rejection | `partially-closed` | Manifest numeric `0`／`1`、Skill numeric `1`及conflicting duplicate JSON/YAML均被拒絕；但YAML 1.1 `yes`／`on` aliases仍被完整validator接受，對應第一個新P2。 |
| Forbidden root components | `closed` | `PLUGIN_ROOT_ENTRIES`固定Ticket 1 root inventory為`.claude-plugin`、`skills`、`agents`，manifest／Skills／agent inventories亦鎖定；`.mcp.json`、`.lsp.json`及任一額外root entry都被拒絕，current tree只有核准entries。 |
| Component containment／symlink policy | `partially-closed` | 普通outside path與各manifest／Skill／reviewer child的resolved containment有效，current children均非links；但CLI預先resolve root且Windows junction不屬於`is_symlink()`，對應第二個新P2。 |
| Canonical fail-closed clause mutations | `open` | 會移除canonical substring的missing／duplicated／unknown-field／failure-status／replacement-negation mutations已拒絕；保留substring的prefixed或additive semantic negation仍通過，對應第三個新P2。 |

## Specification and Ticket assessment

| Review area | Outcome | Evidence |
| --- | --- | --- |
| Claude catalog identity與provider source | `passed` | `.claude-plugin/marketplace.json`具有exact top-level fields、單一Plugin、核准owner／metadata、strict booleans及tag-pinned `v1.4.0` Claude `git-subdir` source；Claude validator拒絕Codex catalog，Codex validator維持通過。 |
| Canonical Plugin manifest | `passed` | Current `plugin.json`的fields、identity、metadata及lowercase JSON boolean與catalog一致，沒有custom component paths、runtime dependency或unknown fields。 |
| 恰好兩個public Skills | `passed-with-findings` | Current inventory恰為兩個names，frontmatter是user-only、`model: inherit`且current bodies fail closed；第一及第三個P2指出frontmatter parser與behavior mutation gate仍有false green。 |
| Reviewer static boundary | `passed` | 單一reviewer只允許`Read, Grep, Glob`，包含全部required inputs、finding fields、四種outcomes與十二lenses；side-effect tool及token-removal mutations被拒絕。 |
| Excluded components與relative resolution | `passed-with-finding` | Forbidden root inventory與child containment有效，但root link identity可被消除，對應第二個P2。Router／hooks／profiles缺席符合Ticket 1切分。 |
| TDD mode與regression | `passed-with-findings` | Final focused 6、affected broader 75及full 222 tests均綠；三個獨立negative probes證明現有suite仍能false green。Historical Red chronology只由raw evidence核對，未採納其completion verdict。 |
| Native Claude validation | `deferred` | 本機沒有`claude` executable；依Approved Plan屬Ticket 3 hard gate。 |

## Twelve Architecture and Refactoring Lenses

1. **Duplicated Code or Policy — `no-finding`.** Catalog／manifest identity、兩個bootstrap與test oracle中的必要重複各有consumer、provider或independent regression責任；本Ticket範圍未見因額外policy副本造成authority漂移。
2. **Long Function — `no-finding`.** Production validator按catalog、manifest、Skills、reviewer及path policy分工；新增guards沒有形成會隱藏重要控制流程的單一長函式。Mutation test雖集中多個subtests，仍可由具名cases直接定位失敗。
3. **Large Module or Class — `no-finding`.** `validate_claude_plugin.py`只擁有同一Ticket 1 public Plugin boundary，尚未混入router、profiles或release builder責任。
4. **Long Parameter List — `no-finding`.** Production helpers最多傳遞三個清楚概念，沒有不穩定coordination interface。
5. **Data Clumps — `no-finding`.** Identity、Skill、envelope、review inputs及lenses均以具名constants集中；沒有同一批鬆散values跨函式反覆傳遞。
6. **Primitive Obsession — `finding`.** Skill invocation authority取決於YAML scalar，但domain仍交由`SafeLoader`寬鬆implicit boolean aliases決定；`yes`／`on`因解析成primitive `True`而繞過exact authored contract。對應第一個P2，位置`validate_claude_plugin.py:98-121,164-176,316-320`。
7. **Feature Envy — `no-finding`.** 各validator routine主要操作自己擁有的catalog、manifest或component資料，沒有反覆伸入其他模組內部狀態。
8. **Divergent Change — `no-finding`.** 這個validator的變更原因仍是單一Claude public-boundary contract；後續router、profiles及release integration由其他Tickets擁有。
9. **Shotgun Surgery — `no-finding`.** Exact identity及bootstrap在consumer source、validator與independent tests中同步是核准邊界的必要多方聲明；未見額外、不相關的修改散落。
10. **Message Chains — `not-applicable`.** Reviewed production code是淺層mapping與filesystem boundary validation，沒有物件導航或多層call chain可評估。
11. **Leaky Abstraction — `finding`.** CLI success抹除原始root link identity，且Skill body success只代表required substrings存在、不代表沒有相反指令；caller必須知道這些validator未揭露的例外。對應第二、第三個P2，位置`validate_claude_plugin.py:179-200,294-322,378-388`。
12. **Shallow Module — `no-finding`.** 單一CLI入口隱藏duplicate-key、exact metadata、inventory、provider separation、containment及reviewer checks，介面相對功能仍有足夠價值；findings是可修正的boundary holes，不使整個模組成為淺層轉接。

本次findings均局限於Ticket 1 Claude validator／tests，沒有cross-module systemic architecture evidence，因此不另路由Architecture Improvement Report。

## Verification performed

- `.\.venv\Scripts\python.exe -B scripts\validate_claude_plugin.py` → exit `0`，canonical Claude Plugin validation passed。
- `.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_public_plugin_contract -v` → exit `0`，`Ran 6 tests in 6.615s`，`OK`。
- Approved affected broader command（Claude public contract、Codex Marketplace/assets/docs、Core conformance/Lite、Codex adapter）→ exit `0`，`Ran 75 tests in 9.351s`，`OK`。
- `.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p 'test_*.py'` → exit `0`，`Ran 222 tests in 25.078s`，`OK`；涵蓋全部現有Codex／Generic／Core／release surrounding regressions。
- `.\.venv\Scripts\python.exe -B -m py_compile scripts\validate_claude_plugin.py tests\claude\test_public_plugin_contract.py` → exit `0`，no output。
- Independent strict/duplicate probes：manifest numeric `0`與`1`、conflicting duplicate JSON及YAML mapping keys全數被`ClaudePluginError`拒絕。
- Independent forbidden-component／child-containment evidence：focused suite的`.mcp.json`、`.lsp.json` mutations被拒絕；普通outside path被`require_contained`拒絕；recorded guards涵蓋manifest、Skills及reviewer paths；current canonical inventory沒有symlink或junction。
- Independent adversarial probes：YAML `yes`／`on`解析為`bool True`且`disable-model-invocation: yes`被完整validator接受；保留canonical phrase的prefixed negation與appended contradiction均被接受。
- Windows root-link probe：temporary directory junction呈現`is_symlink=False`、`is_junction=True`；直接`validate_plugin_root`及CLI `--plugin <junction>`均接受，CLI exit `0`。Probe已清理，沒有改動repository candidate。
- `git diff --check` → exit `0`；只有既有`docs/project/knowledge-base.md`的LF→CRLF working-copy warning。Ticket-ownedsource／tests的trailing-whitespace、credential／secret及machine-local absolute-path scans均無matches；UTF-8 files沒有BOM且有final LF。
- `claude` → unavailable；`node --version` → `v24.19.0`。Node只證明後續runtime prerequisite在本機可用，不代表Ticket 1存在router或native host已驗證。

## Evidence unavailable, residual risks, and untested areas

- `claude` CLI不可用，因此兩個`claude plugin validate <path> --strict`、實際namespaced discovery、bare-alias observation、host frontmatter schema與installation behavior均未執行；這是Approved Ticket 3明列的hard gate。
- POSIX directory symlink mutation沒有在本Windows host執行；pre-resolution control flow可由source確定，且等價的Windows directory junction已實際重現。Current canonical root與children本身都是一般directories/files。
- Historical initial／correction Red無法在不回退current candidate的前提下獨立重演；raw evidence記錄的failure shape與test source一致，但本Review只把本次實跑的final及adversarial結果當作completion判斷。
- Ticket-owned新增檔仍為untracked，沒有Git base diff；Review已以完整snapshot、inventory、line-by-line source inspection及surrounding tests補足，但不宣稱有commit-level provenance。
- Current authored metadata使用lowercase`true`、current Skill文字沒有相反指令、current Plugin root／children沒有links；三個findings針對未受保護的future drift與deterministic gate，不是聲稱current bytes已含惡意內容。
- Router、route enum、manual fallback、profiles、package exclusion、context及live behavior尚未存在；依Approved Plan不是Ticket 1額外finding，但後續Tickets仍須各自建立behavior gates。

## Completion assessment

Approved Ticket 1 **尚不可評為完成**。Forbidden root component修正已關閉，numeric boolean、duplicate key及Plugin child containment也已有有效保護；然而exact Skill boolean仍接受YAML 1.1 aliases，Plugin root link policy可被CLI pre-resolution／Windows junction繞過，fail-closed body仍可在保留canonical substring時加入相反指令。這三個`P2`都會讓repository validator／TDD suite對不符合Approved public boundary的candidate產生false green。修正、補Red mutations、重驗並由fresh independent Review確認前，Ticket 1 completion gate維持未通過。
