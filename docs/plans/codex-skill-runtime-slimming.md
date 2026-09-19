# Codex Skill Runtime Slimming - Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `codex-skill-runtime-slimming-ticket-plan`

Workflow ID: `codex-skill-runtime-slimming-2026-09-15`

Core version: `1.4.1`

Status: Approved

Inputs: Approved [Codex Skill Runtime Slimming Specification](../specs/codex-skill-runtime-slimming.md); Approved Requirement Decision Record and Knowledge Base Change Summary in the [Decision Packet](../project/drafts/codex-skill-runtime-slimming/decision-packet.md); current Codex skills, `rule-mapping.yaml`, `conformance.yaml`, Codex tests, package builder, release checks, and token-proxy tooling.

Assumptions: 第一版只做 Codex adapter 的 behavior-equivalent ownership and loading refactor。Shared references 固定放在 `adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/references/`，使用 `full-routing.md`、`artifact-contract.md`、`architecture-refactoring-lenses.md`，並保留既有 `lite-workflow.md`。每個 consumer `SKILL.md` 直接連結所需 reference，reference 不再連到另一份 reference。GPT-5.x 與 GPT-6 共用同一 package。

Deferred: Universal trigger 收窄、Review lenses 條件化、Review 自動修復、model-specific variants、Generic／Claude／Core 語意變更、exact live-model／host matrix、版本變更、candidate build、release、publication，以及任何大型 `AGENTS.md`。

Handoff: T1-T5 的測試選擇已全部收集並映射為 `tdd`；本 Ticket Plan 已取得明確核准，現在交接至 T1 `tdd` implementation。

Approval: User explicitly approved the complete Ticket Plan on 2026-09-17 with `核准 Ticket Plan` after all T1-T5 choices were mapped to `tdd`.

## Plan summary

五張 Ticket 依序把驗證基礎、root router、stage／artifact contract、十二 lenses 與整合證據分開交付。順序刻意先建立可重複的語意與 reference 驗證，再移動 runtime 責任；每次移除重複文字前，都先確保 canonical replacement 可達且 failure behavior 可驗證。

本計畫決定下列 package-contained ownership：

| Runtime owner | Canonical path | Consumers |
| --- | --- | --- |
| Lite lifecycle | `ask-then-do-it/references/lite-workflow.md` | Root after proven Lite only |
| Full cross-stage routing | `ask-then-do-it/references/full-routing.md` | Root after proven Full only |
| Portable artifact envelope | `ask-then-do-it/references/artifact-contract.md` | Artifact-producing stages before artifact creation |
| Twelve architecture/refactoring lenses | `ask-then-do-it/references/architecture-refactoring-lenses.md` | Full Review and Architecture before lens evaluation |

這些 references 是 runtime canonical owners，不是 repository documentation。Stage-specific schema、gate、label、failure outcome 與 handoff 仍由各 stage 擁有。

## Dependency order

| Order | Ticket | Depends on | Parallel safety |
| --- | --- | --- | --- |
| 1 | T1 - Semantic validation and baseline evidence | None | No; establishes the validator and measurement contract used by every later Ticket |
| 2 | T2 - Root router and on-demand Full routing | T1 | No; fixes the shared reference location and root routing boundary |
| 3 | T3 - Stage guards and canonical artifact envelope | T1, T2 | No; updates all eight stage entrypoints and shared rule mapping |
| 4 | T4 - Canonical twelve-lens contract | T1, T3 | No; revisits Review and Architecture after their T3 stage-contract changes |
| 5 | T5 - Package integration and compatibility evidence | T2, T3, T4 | No; verifies and measures the integrated package |

## Ticket T1 - Semantic validation and baseline evidence

### Outcome

建立一個 fail-closed、可重複執行的 Codex runtime contract boundary，能驗證 reference graph、section mapping、package containment 與 source-level context measurements，並在任何 runtime 文字移動前保存目前 baseline。

### Acceptance criteria covered

`CSRS-AC-004`、`CSRS-AC-008`、`CSRS-AC-010`，以及 `CSRS-AC-009` 的 focused validation foundation。

### In scope

- 保存目前九個 public `SKILL.md` 的 raw UTF-8 bytes、whitespace-delimited words、SHA-256，以及代表性 route load sets 的 normalized loaded-context proxy baseline。
- Proxy 使用一致且可重複的方法：各載入檔案先做 Unicode normalization 與 whitespace normalization，再依載入順序組合，以 `ceil(normalized UTF-8 bytes / 4)` 表示 source-level proxy；明確標示它不是 billing 或 total context。
- 驗證 consumer 到 required reference 是直接 link、最多一 hop、路徑留在 Codex package、target 存在且可讀、reference 不再要求另一 reference、graph 無 cycle。
- 驗證 `rule-mapping.yaml` 的 source path 與 Markdown section 真實存在；不再只因宣告 rule ID 就視為 coverage。
- 以 structured markers、parsed frontmatter、headings、links、closed inventories 與 outcome sets 取代適合移除的非契約 exact-prose assertions；identity、path、status、rule ID 與 security literals 仍可逐字驗證。
- 讓 validator 可對隔離 fixture 驗證 missing target、escaping path、second hop、cycle、missing section 與 package omission 等失敗分支。
- 這是最小 shared enabling Ticket；第一個 runtime consumer 是 T2。

### Out of scope

- 不移動或刪除任何 Codex runtime instructions。
- 不建立三個新 shared runtime references，也不改 Full／Lite routing。
- 不宣稱 source proxy 等於 host 實際載入或模型相容證據。

### Dependencies and likely ownership areas

無前置 Ticket。Likely areas: `tests/codex/`、小型 fixtures、現有 validation／measurement tooling 或一個聚焦的 Codex context measurement helper；不得修改 Generic／Claude fixtures 或 release version。

### Recommended verification

建議加測試。這個 Ticket 定義後續所有文字移動的安全網；若 missing reference、cycle 或虛假 mapping 的負向分支沒有測試，後續瘦身可能在 package 中靜默斷鏈。加測試會增加工時；不加測試會明顯降低 reference failure 與 measurement reproducibility 的驗證信心。

### If tests are added

使用 TDD。第一個 Red 是讓隔離 contract fixture 的 missing／cycle／second-hop 或 missing-section case 未被現有 validator 拒絕；Green 只加入最小 parser、diagnostic 與 baseline measurement；之後執行 focused Codex contract tests 和既有 conformance checks。

### If tests are declined

使用 direct mode，只執行 read-only source inventory、hash／bytes／words／proxy measurement、link resolution 與現有 non-test validators。記錄 `tests: skipped-by-user`，並揭露 malformed graph、cycle、path escape、missing-section 與 measurement drift 未獲 behavioral verification。

### Completion criteria

Baseline 有可重複的 input paths、hashes、公式與 route load sets；validator 對每個指定 invalid fixture fail closed、對現行合法 package 通過，且沒有 Codex runtime 行為改動。

### Parallel safety

No。T1 建立所有後續 Ticket 共用的測量與 validation contract，必須先穩定。

## Ticket T2 - Root router and on-demand Full routing

### Outcome

把 root `SKILL.md` 收斂成 capability declaration、唯一 Full／Lite resolver、共通安全邊界與短 routing index；只有 proven Full 才讀取 canonical `full-routing.md`，proven Lite 仍只讀既有 `lite-workflow.md`。

### Acceptance criteria covered

`CSRS-AC-001`、`CSRS-AC-002`、`CSRS-AC-004`、`CSRS-AC-007`、`CSRS-AC-008`。

### In scope

- 新增 package-contained `full-routing.md`，承接只屬於 Full 的 stage discovery、requirement-mode selection、Ticket implementation routing、architecture routing、knowledge synchronization、gates、coordination 與 completion boundary。
- Root 保留完整且唯一的 mode precedence／failure matrix、Config paths、read-only behavior、universal software-change trigger、capability claim 與 Full／Lite separation。
- Root frontmatter description 可以縮短，但仍須明確涵蓋 every software-changing operation，包括 trivial、fully specified、formatting-only 與 single-line changes；stage descriptions 不得變成第二個 universal entry。
- Root 在 proven Full 後明確要求 action 前完整讀取 `full-routing.md`；proven Lite 只完整讀取 `lite-workflow.md`。兩條 route 不互相載入。
- 保留 direct stage 無 current-operation proof 時返回 root 的 canonical outcome；Ticket-level `tdd`／`direct` 不成為第三種 top-level mode。
- 更新相關 rule mappings 與 semantic tests，移除只凍結一般敘述文句的 assertions。

### Out of scope

- 不改八個 stage bodies、artifact envelope 或十二 lenses。
- 不改 mode precedence、Config semantics、legacy resolved-Full lightweight subpath、approval gates 或 completion result。
- 不調整 universal trigger 範圍。

### Dependencies and likely ownership areas

Depends on T1。Likely areas: root `SKILL.md`、`references/full-routing.md`、`tests/codex/test_lite_workflow.py`、semantic contract tests、`adapters/codex/rule-mapping.yaml`。

### Recommended verification

建議加測試。Root 是所有 software-changing operations 的入口，mode precedence、invalid Config 或 Lite isolation 的退化會影響整個 adapter。加測試會增加工時；不加測試會降低對 route equivalence、trigger preservation 與 conditional loading 的信心。

### If tests are added

使用 TDD。第一個 Red 驗證 Full conditional detail 仍留在 root 或 Full／Lite reference loading 不互斥；接著以最小 root／reference 移動達成 Green，再跑完整 mode outcome matrix、universal trigger、Lite isolation、reference graph 與 mapping tests。

### If tests are declined

使用 direct mode，只做 frontmatter／section parser、mode matrix 對照表、reference validator、rule mapping validator、diff inspection 與 skill quick validation。記錄 `tests: skipped-by-user`；不得宣稱真實 route behavior 或 GPT-5.x／GPT-6 adherence 已驗證。

### Completion criteria

Root 對每個 baseline mode input 保持相同 route／failure result；Full-only detail 只有一個 canonical owner，Lite route 不載入 Full reference，所有 public identity 與 trigger contracts 不變。

### Parallel safety

No。T2 決定 shared-reference path 與 root routing boundary，T3 必須使用這個已驗證結構。

## Ticket T3 - Stage guards and canonical artifact envelope

### Outcome

讓八個 public stages 各自只保留 stage prerequisites、行為、artifact-specific semantics、gate 與 handoff，同時以短 local guard 保持 direct-entry fail-closed，並讓所有 artifact producers 在產出前讀取同一份 canonical artifact contract。

### Acceptance criteria covered

`CSRS-AC-003`、`CSRS-AC-004`、`CSRS-AC-005`、`CSRS-AC-007`、`CSRS-AC-008`。

### In scope

- 新增 package-contained `artifact-contract.md`，集中 portable envelope、Draft／Approved state honesty、approval evidence、assumptions、deferred work、handoff 與 required-reference failure behavior。
- 八個 stage bodies 都保留可獨立理解的 concise guard：直接選 stage 不是 Full proof、無 proof 回 root、proven Lite 停止 Full stage、只有 proven Full 繼續、mode 不跨 operation 保存或沿用。
- 從八個 guards 移除完整 resolver precedence matrix；canonical resolver 仍只在 root。
- 每個 artifact-producing stage 直接連結 `artifact-contract.md`，並在建立 artifact 前要求完整讀取；讀不到時停止，不能靠記憶補欄位。
- 各 stage 繼續擁有自己的 required fields、status transitions、approval／stopping condition、evidence labels 與 handoff；Specification shape 留在 `write-spec`。
- 精準化 stage descriptions，只描述各 stage 的使用時機與重要排除，不擴張觸發範圍。
- 在 canonical replacement 可達且 tests／validators 已覆蓋後，移除重複 portable field lists、maintainer-only comments 與不影響決策的 recipe。
- 更新 rule mapping、semantic markers 與 package reference expectations。

### Out of scope

- 不改 root resolver 或 Full routing reference。
- 不集中 stage-specific schemas、Requirement／Specification／Plan gates、test-choice mapping、TDD／Direct behavior 或 Review labels。
- Review／Architecture 的十二 lens definitions 留到 T4；Lite workflow 不讀 artifact contract。

### Dependencies and likely ownership areas

Depends on T1 and T2。Likely areas: all eight stage `SKILL.md` files、`references/artifact-contract.md`、Codex semantic tests、`rule-mapping.yaml`。

### Recommended verification

建議加測試。這個 Ticket 同時保護 direct entry 與所有 Full artifacts，任何遺漏都可能繞過 mode proof、approval state 或 required fields。加測試會增加工時；不加測試會降低對八個 guards、fail-closed reference loading 與 artifact completeness 的信心。

### If tests are added

使用 TDD。第一個 Red 驗證每個 stage 的五項 guard outcomes、禁止完整 resolver duplication，以及每個 producer 的 direct artifact-reference link／read-before-action；再加入 missing-reference、required-field coverage 與 Draft／Approved state checks，最後以最小 stage edits 達成 Green。

### If tests are declined

使用 direct mode，只執行 parsed section／link inspection、artifact field crosswalk、rule mapping validation 與九個 skill quick validation。記錄 `tests: skipped-by-user`；揭露 direct-entry outcome、missing-reference failure 與 artifact state regression 未獲 behavioral verification。

### Completion criteria

八個 stage guards 都獨立表達五項 outcome 且不重複 resolver matrix；所有 producers 使用同一 canonical envelope，baseline stage-specific fields／gates／handoffs 無缺漏，broken contract link 會 fail closed。

### Parallel safety

No。八個 stage 與共用 rule mapping 是同一 ownership boundary，且 T4 會再次修改其中 Review／Architecture 兩個 consumers。

## Ticket T4 - Canonical twelve-lens contract

### Outcome

建立單一十二-lens runtime definition，讓 Full Review 與 Architecture 各自按需讀取同一順序與 outcome contract，同時保留兩個 stages 不同的 scope、labels、simulated deletion、report 與 handoff。

### Acceptance criteria covered

`CSRS-AC-004`、`CSRS-AC-006`、`CSRS-AC-007`、`CSRS-AC-008`。

### In scope

- 新增 package-contained `architecture-refactoring-lenses.md`，集中十二 lenses 的名稱、固定順序、定義，以及 `finding`／`no-finding`／`not-applicable`／`unverified` outcome honesty。
- `review-code` 與 `improve-architecture` 都直接連結該 reference，並在 lens pass 前完整讀取；讀不到時不得宣稱完成十二-lens pass。
- Review 保留 change-focused priority、independence labels、severity、finding validation 與 systemic handoff。
- Architecture 保留 diagnostic-only boundary、dependency tracing、simulated deletion、report state 與 accepted-proposal reflow。
- 移除兩個 stage bodies 中重複的 lens definition，只保留 stage-specific application rules。
- 確認 Lite compact Review 沒有連結或套用 Full fixed-lens pass。
- 更新 `REVIEW-LENSES-001` 與 architecture rule mappings、semantic tests 和 package expectations。

### Out of scope

- 不更名、重排、條件化或增減十二 lenses。
- 不讓 Review 自動修復，也不改 Architecture diagnosis 的授權邊界。
- 不修改 Lite compact Review behavior。

### Dependencies and likely ownership areas

Depends on T1 and T3。Likely areas: `review-code/SKILL.md`、`improve-architecture/SKILL.md`、`references/architecture-refactoring-lenses.md`、Codex semantic tests、`rule-mapping.yaml`。

### Recommended verification

建議加測試。Lens completeness 與順序是 mandatory Core contract，且 Lite isolation 不能靠人工記憶。加測試會增加工時；不加測試會降低對 lens omission、outcome drift、missing-reference failure 與 Lite contamination 的信心。

### If tests are added

使用 TDD。第一個 Red 驗證 Review／Architecture 尚未共同解析同一 canonical list，或 Lite 錯誤取得 Full lens contract；Green 建立單一 reference 與兩個 direct consumers，再驗證完整順序、closed outcomes、stage-specific behavior 與 broken-link failure。

### If tests are declined

使用 direct mode，只做 reference list／order diff、consumer link inspection、Lite isolation scan、rule mapping validation 與 quick validation。記錄 `tests: skipped-by-user`；不得宣稱兩個 stages 的實際 lens application 或 missing-reference behavior 已驗證。

### Completion criteria

十二 lenses 只有一個 runtime definition；兩個 Full consumers 可直接取得完整 contract，原有各自 semantics 不變，Lite route 不載入該 reference。

### Parallel safety

No。T4 修改 T3 已整理過的 Review／Architecture files 及同一 rule mapping，必須在 T3 Green 後進行。

## Ticket T5 - Package integration and compatibility evidence

### Outcome

從乾淨、隔離的 Codex package boundary 驗證整合結果，產出 before／after slimming evidence 與 compatibility honesty，並把完成的 source candidate 交給獨立 Review；不升版、不建立正式 candidate、不發布。

### Acceptance criteria covered

`CSRS-AC-009`、`CSRS-AC-010`、`CSRS-AC-011`、`CSRS-AC-012`，以及 `CSRS-AC-001` 至 `CSRS-AC-008` 的 integrated verification。

### In scope

- 從隔離 temporary output 建立 Codex package，驗證四份 references 都在 package、所有 consumer links 在 package 內解析、ZIP 與展開目錄一致、兩次 isolated build bytes 可重現。
- 執行九個 skill quick validation、Codex unit／semantic tests、mode matrix、Lite isolation、conformance、rule mapping、package inventory、applicable release contract checks 與 `git diff --check`。
- 用 T1 相同方法記錄 after bytes、words 與每個代表 route 的 loaded-context proxy，和 baseline 並列；不設定硬性縮減百分比，不用總 source 變小掩蓋某 route 變大或 contract regression。
- 驗證 package 沒有 GPT-5.x／GPT-6 variants，並以 direct local guard、imperative read-before-action、single-hop reference 與 self-contained package 作為 source-level compatibility evidence。
- Exact model／host fresh-session runs 若未另行核准或環境不可用，GPT-5.x 與 GPT-6 都明確標記 `unverified`；static tests 不得改寫成 live compatibility。
- 確認 final diff 不含 Generic／Claude runtime、Core semantics、`AGENTS.md`、version、正式 candidate、generated distribution 或 publication changes。
- 產出 implementation／integration evidence，附 raw commands、results、skips、unavailable checks、residual risks，交給 `$review-code`；獨立 reviewer unavailable 時如實標記。

### Out of scope

- 不執行 network 或付費 model calls。
- 不修改 exact live-model matrix、不升版、不寫入正式 `dist/`、不提交、不建立 tag／Release、不發布。
- Review 發現的新 behavior 或 architecture scope 不在本 Ticket 內直接修復；回到最早受影響 gate。

### Dependencies and likely ownership areas

Depends on T2, T3, and T4。Likely areas: isolated build／test fixtures、Codex package integration tests、measurement evidence under `docs/evidence/`、`conformance.yaml` validation evidence when needed、final Status links。任何 temporary build 必須留在可清理的隔離位置，不更新正式 distributions。

### Recommended verification

建議加測試並執行完整適用 suite。這是跨 Ticket package、mapping、reproducibility 與 scope boundary 的最後防線。加測試會增加工時；不加測試會降低對 consumer package 完整性、兩次建置一致性與整合 regression 的信心。

### If tests are added

使用 TDD。第一個 Red 是隔離 package integration test 尚未證明 shared references、links、mapping sections 與 exact inventory 一致；Green 只補足必要 packaging／test integration，然後跑 focused checks、完整適用 suite、兩次 isolated build、measurement 與 final diff audit。

### If tests are declined

使用 direct mode，不新增、修改或執行 behavioral tests；只允許 skill／conformance validators、read-only package inventory、isolated build、ZIP byte comparison、measurement、diff inspection 與其他非測試 validation。記錄 `tests: skipped-by-user`，並揭露 mode、stage、artifact、lens 與 integration behavior 未獲回歸測試。

### Completion criteria

所有選定 checks 通過或被誠實標為 unavailable／skipped；四份 references 在 consumer package 可達且 build 可重現；before／after evidence 可重算；scope audit 無越界；GPT-5.x／GPT-6 live status 沒有被誇大；沒有 blocking Review finding 時才可宣稱 source-level refactor 完成。

### Parallel safety

No。T5 必須針對 T2-T4 的單一整合結果執行，不能與尚在變動的 runtime 並行。

## Test choice batch

每張 Ticket 都必須由使用者選擇是否加測試；沒有預設值，也不能由風險、repository convention 或其他 Ticket 推定。`Add tests` 會映射為內部 `tdd`；`Do not add tests` 會映射為內部 `direct`。任何未決選擇都使本計畫保持 `Draft`。

| Ticket | Recommendation | Choice | Internal mode |
| --- | --- | --- | --- |
| T1 | Add tests - reference validator、負向 failure branches 與 baseline reproducibility 是後續安全基礎 | 使用者於 2026-09-17 選擇「全部加測試」 | `tdd` |
| T2 | Add tests - root mode matrix、universal trigger 與 Full／Lite isolation 影響全部 operations | 使用者於 2026-09-17 選擇「全部加測試」 | `tdd` |
| T3 | Add tests - 八個 direct-entry guards 與 artifact gates 具有高 regression blast radius | 使用者於 2026-09-17 選擇「全部加測試」 | `tdd` |
| T4 | Add tests - mandatory lens order／outcomes、broken links 與 Lite isolation 需可重複驗證 | 使用者於 2026-09-17 選擇「全部加測試」 | `tdd` |
| T5 | Add tests - package inventory、reproducibility、scope 與 integrated behavior 需要最終回歸證據 | 使用者於 2026-09-17 選擇「全部加測試」 | `tdd` |

所有建議都傾向加測試，原因不是固定要求「改完一定全測」，而是本次會搬動共用 workflow contracts，且主要成功條件就是行為等價與 fail-closed。選擇不加測試仍可走 direct mode，但各 Ticket 所列的 behavioral evidence gap 必須保留，不能用 static inspection 冒充。

## Plan approval boundary

本文件目前為 `Approved`。T1-T5 的一次性 plain-language test choices 已全部選擇「加測試」並映射為 `tdd`。計畫核准後可依序執行已核准 Ticket；Plan approval 不授權升版、正式 candidate、release、publication、Generic／Claude／Core 修改或 live-model calls。
