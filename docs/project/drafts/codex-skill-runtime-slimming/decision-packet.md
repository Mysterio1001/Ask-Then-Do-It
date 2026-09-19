# Codex Skill Runtime Slimming - Decision Packet

Artifact type: Decision Packet

Artifact ID: `codex-skill-runtime-slimming-decision-packet`

Workflow ID: `codex-skill-runtime-slimming-2026-09-15`

Core version: `1.4.1`

Status: Draft

Inputs: 使用者提供的 GPT-6 Astra skills／AGENTS.md 優化原則、Codex runtime 唯讀稽核、現行 Core／Codex sources、tests、release contracts，以及使用者於 2026-09-16 確認的 Codex-only 行為等價邊界。

Assumptions: Project Config 與 user Config 均不存在，因此本次文件工作依 Full fallback 進行；第一版只重構 Codex adapter 的指令結構，不改變任何可觀察的 workflow 行為。

Deferred: Universal trigger 收窄、Review 十二 lenses 條件化、Review 自動修復、model-specific variants、Generic／Claude／Core 語意變更、exact live-model matrix、升版、candidate build 與外部發布。

Handoff: 完整 Requirement Decision Record、Knowledge Base Change Summary 與 [Specification](../../../specs/codex-skill-runtime-slimming.md) 已核准；T1-T5 測試選擇已於 2026-09-17 全部選擇加測試並映射為 `tdd`，使用者已核准 [Ticket Plan](../../../plans/codex-skill-runtime-slimming.md)，目前交接至 T1 `tdd` implementation。

Approval:

Knowledge change: `summary_required: true`。使用者於 2026-09-16 共同核准完整 Requirement Decision Record 與 Knowledge Base Change Summary；已只依核准摘要同步 [Project Knowledge Base](../../knowledge-base.md)。

本文件是 workflow `codex-skill-runtime-slimming-2026-09-15` 唯一的 provisional substantive owner。舊三份草稿路徑只保留 pointer；原始 bytes 與 SHA-256 由 [source manifest](migration/source-manifest.json) 指向 migration backup。Backup 是復原資料，不是目前需求來源。

## Draft Working Notes

```json
{
  "artifact_type": "Draft Working Notes",
  "artifact_id": "codex-skill-runtime-slimming-working-notes",
  "workflow_id": "codex-skill-runtime-slimming-2026-09-15",
  "core_version": "1.4.1",
  "status": "Draft",
  "inputs": ["user-guidance", "codex-source-and-test-audit", "core-1.4.1", "project-knowledge-base"],
  "assumptions": ["Runtime source is current evidence; unavailable exact-model live evidence is not replaced by static checks."],
  "deferred": ["Exact live-model matrix", "Release versioning", "Candidate build", "Publication"],
  "handoff": "Requirement Decision Record and Knowledge Base Change Summary approval",
  "approval": null
}
```

### Confirmed

- `confirmed`：只處理 Codex adapter；Generic 與 Claude 不在本輪範圍。
- `confirmed`：第一版採行為等價的瘦化、優化與分責化，不改 universal trigger、Full／Lite、approval、stage routing 或 artifact semantics。
- `confirmed`：九個公開 skill 名稱、plugin identity、Full／Lite mode precedence、invalid Config fail-closed、TDD／Direct、Review、architecture 與 evidence honesty 契約均須保留。
- `confirmed`：GPT-5.x 仍是相容目標；progressive disclosure 必須使用明確的 read-before-action 指令、單層 reference 與可在 direct entry 看見的短 guard，不能只依賴 GPT-6 的推理能力。
- `confirmed`：本專案目前沒有 `AGENTS.md`；本輪不新增大型 `AGENTS.md`。
- `confirmed`：使用者於 2026-09-16 先回覆「核准」確認行為等價第一版，之後再確認「專注回到 codex」；兩次回覆是需求邊界共識，不等同於尚未完整展示的 RDR／Knowledge Base 正式核准。

### Repository evidence

- 現行九份 Codex `SKILL.md` 合計約 55,581 bytes、7,630 words；root orchestrator 約 11,426 bytes、1,589 words。
- 八個 stage skills 重複完整 direct-entry mode guard。
- Artifact producers 重複 portable envelope 欄位；Review 與 Architecture skills 重複十二 lenses。
- `tests/codex/test_adapter.py` 與 `tests/codex/test_lite_workflow.py` 多處以 exact prose 驗證契約，讓等價改寫產生不必要維護成本。
- Codex package builder 已遞迴複製 plugin source，且 root skill 已有 `references/lite-workflow.md`，可作為 progressive disclosure 的既有包裝先例。

### Proposed

- `proposed`：root skill 保留每次操作都需要的 capability、mode selection 與短 routing index；Full-only 詳節移到按需讀取的 reference，Lite reference 維持隔離。
- `proposed`：stage skill 只保留 stage prerequisites、stage-specific behavior 與一段短 direct-entry guard；共用 artifact contract 與十二 lenses 改由明確 reference 承接，Specification-specific shape 仍由 `write-spec` 擁有。
- `proposed`：supporting reference 必須由需要它的 `SKILL.md` 直接連結，不得 reference-to-reference；缺檔或斷鏈 fail closed。
- `proposed`：測試從 exact sentences 改驗證 semantic invariants、reference reachability、package inventory 與 rule mappings；真正有法律、identity 或外部契約意義的 exact literals 繼續保留。

### Unresolved

- `unresolved`：GPT-5.x 與 GPT-6 fresh-session live evaluation 可使用的 exact model IDs、host versions 與 case 數量。
- `unresolved`：source 完成後是否升 patch version、建立 candidate ZIP 或只保留離線驗證。
- `unresolved`：跨 public skill 共用 reference 的最終 plugin-relative 位置，須由 Specification／Ticket 以 self-contained package、單層載入及 validator 可達性共同決定；不得依賴 repository-only docs。

## Requirement Decision Record

```json
{
  "artifact_type": "Requirement Decision Record",
  "artifact_id": "codex-skill-runtime-slimming-rdr",
  "workflow_id": "codex-skill-runtime-slimming-2026-09-15",
  "core_version": "1.4.1",
  "status": "Approved",
  "inputs": ["codex-skill-runtime-slimming-working-notes", "codex-sources-and-tests", "core-1.4.1", "project-knowledge-base", "confirmed-codex-only-boundary"],
  "assumptions": ["The first version changes instruction ownership, loading time, and test expression only; equal inputs and evidence retain equal routes, gates, artifact states, and completion boundaries."],
  "deferred": ["Universal trigger narrowing", "Conditional lenses", "Review auto-correction", "Model-specific variants", "Core, Generic, or Claude changes", "Release versioning", "Publication"],
  "handoff": "Write and obtain approval for the behavioral Specification.",
  "approval": "User explicitly approved the complete Requirement Decision Record and Knowledge Base Change Summary together on 2026-09-16 with `核准`."
}
```

### Problem

Codex adapter 現有 public skills 能表達 Core 契約，但 root orchestrator 承擔過多 Full workflow 細節，八個 stage skills 重複 mode guard，多個 artifact producers 重複 envelope，Review 與 Architecture 重複十二 lenses。這些重複增加每次載入的 context、政策漂移風險與小修改成本；逐字 prompt tests 又讓語意等價的精簡難以進行。

### Desired outcomes

1. Codex runtime 具有清楚的 router、stage 與 shared-reference 責任邊界。
2. 每次操作只載入當下 route／stage 所需細節，不預載不相干流程。
3. Shared contracts 只有一個 runtime canonical owner，stage 仍保留足以 fail closed 的 local guard。
4. GPT-6 Astra 能受益於較短且語意導向的指令；GPT-5.x 不需猜測 mode、approval 或 reference 載入時機。
5. Tests 驗證可達的行為契約，而不是把非契約文句永久凍結。

### Users and scenarios

- 一般 Codex software-changing operation 仍先觸發 root resolver；小型、格式或單行修改不因本輪被移出 universal coverage。
- Lite operation 只讀 Lite lifecycle，不載入 Full stage references，也不建立 Full artifacts。
- Full operation 由 root 判定第一個未滿足 gate，再載入當前 stage；不預載所有 stages。
- 使用者直接選擇 public stage 時，stage 先檢查 current-operation mode proof；無 proof 交回 root，Lite 離開 Full stage，只有 proven Full 繼續。
- Artifact producer 在產出前讀取 canonical artifact contract，並保留自身 stage-specific fields、status、approval 與 handoff。
- Review／Architecture 仍完整套用同一組十二 lenses；Lite compact Review 仍不套用 Full fixed-lens pass。

### Included scope

1. `adapters/codex/plugin/ask-then-do-it/skills/**` 內九個 public skills 及其 package-contained supporting references。
2. `adapters/codex/rule-mapping.yaml` 與 `adapters/codex/conformance.yaml`，但只限 source path／section 可達性與既有 mandatory rule coverage 維護。
3. `tests/codex/**`，以及直接驗證 Codex package inventory、reference reachability、token proxy 或 release contract 的既有 tests／fixtures。
4. 本 workflow 的 Specification、Ticket Plan、implementation evidence 與 Review 文件，依各自 gate 建立。
5. 若現有 validator 無法檢查斷鏈，可在後續 Approved Ticket 內擴充既有 validation boundary；不得順便重寫其他 adapter validator。

### Excluded scope

- Universal software-change trigger 或 public skill inventory 的變更。
- Full／Lite semantics、mode precedence、Config paths、fail-closed behavior 或 direct-stage routing 的變更。
- Requirement、Specification、Ticket Plan、Lite Change Brief 或 correction approval gates 的變更。
- TDD Red、Direct no-behavioral-test、Review labels、十二 lenses、architecture diagnosis 或 evidence claims 的變更。
- Core mandatory rule meaning；Generic／Claude source 或 behavior；新增 `AGENTS.md`。
- Dependency installation、network calls、model-specific instruction forks、release version bump、candidate build 或 publication。

### Required behavior

#### Discovery and identity

- Plugin identity、九個 public skill IDs、UI metadata 與 explicit user selection behavior 保持不變。
- Root frontmatter description 必須繼續明確涵蓋 every software-changing operation，包含 trivial、formatting-only 與 single-line changes；可以縮短文句，但不能收窄觸發集合。
- Stage skill descriptions 必須簡短描述各自精確的 stage 使用時機，不能擴張成第二個 universal entry。

#### Root router

- Root 仍是 capability declaration 與 current-operation Full／Lite mode 的 canonical resolver。
- Resolver 保留 explicit instruction、project Config、user Config、Full fallback 的順序，以及 conflict、absent、unreadable、malformed、missing-mode、unsupported 等現行結果。
- Root 只保留所有 route 都需要的決策與安全邊界；Full-only lifecycle detail 在 proven Full 後才讀取，Lite detail 只在 proven Lite 後讀取。
- Full 與 Lite references 彼此不得互相載入，且不得把 Ticket-level `tdd`／`direct` 當頂層 mode。

#### Stage responsibility and direct entry

- 每個 stage skill 只擁有自身 prerequisite、操作、artifact-specific semantics 與 gate。
- 每個 direct-entry stage 都必須在主體內保留 concise guard，明確表達：stage selection 不是 top-level Full、mode proof 缺失時交回 root、Lite 停止此 Full stage、只有 proven Full 繼續、mode 不跨 operation 保存或沿用。
- Guard 可共用固定短格式，但不能只留下沒有 fail-closed outcome 的裸連結。

#### Progressive disclosure and shared contracts

- `SKILL.md` 可將 substantial conditional detail 移至 package-contained `references/`；每個 reference 必須由需要它的 `SKILL.md` 直接連結並說明何時完整讀取。
- 從目前載入的 `SKILL.md` 到所需 detail 最多一個 reference hop；reference 不得再要求另一 reference，避免 GPT-5.x 漏讀與循環。
- Runtime contract 不得依賴 plugin package 外的 `core/`、`docs/` 或網路內容。
- Broken link、missing reference、package omission 或 rule mapping 指向不存在 section 必須使 validation fail closed。
- Artifact envelope 與十二 lenses 可以集中，但使用它們的 stage 必須保留明確 read-before-action 指令與 stage-specific outcome。

#### Tests and evidence

- Tests 必須保留 semantic invariants、mandatory rule IDs、public inventory、mode outcome matrix、Lite isolation、artifact field coverage、lens completeness、reference reachability、package inclusion 及 release reproducibility。
- Exact prose assertion 只在該 literal 本身是 external contract、identity、path、status、rule ID 或 security boundary 時保留；一般說明文字改以結構化契約或 normalized semantic markers 驗證。
- Token proxy 必須用相同 measurement method 比較 before／after；source bytes、word count 或 proxy reduction 不得被描述成實際 billing 或 total-context 保證。
- 實作完成不得宣稱 GPT-5.x／GPT-6 live-compatible，除非對應 exact model／host fresh-session evidence 已取得；缺少 live evidence 時可完成 source refactor，但須標示 `unverified` 並不得用靜態 tests 取代。

### Failure behavior

- Mode proof 缺失、衝突或 invalid Config 依現行 resolver 行為處理，不因精簡而猜測。
- Required reference 不可讀時停止受影響 route／stage並報告 packaging failure，不從模型記憶補寫規則。
- Artifact producer 無法取得 canonical envelope 時不得省略 required fields。
- Rule mapping 或 package inventory 與 source 不一致時，Codex conformance／release validation 失敗。
- 精簡造成任何 Full／Lite、gate、artifact、Review 或 completion outcome 差異時，視為 regression；返回 Specification／Ticket 修正，不以 token reduction 抵銷。

### Compatibility matrix

| Target | Required instruction shape | Required source evidence | Live evidence boundary |
| --- | --- | --- | --- |
| GPT-5.x | Direct-entry local guard、明確 imperative read-before-action、最多一層 reference、不得依賴隱含 Core knowledge | Mode matrix、reference reachability、package inventory、semantic contract tests 全數通過 | Exact model／host 可用時執行 fresh-session cases；不可用時標 `unverified`，不能宣稱 live regression-free |
| GPT-6 Astra | 短 router、按 route／stage 載入、避免鉅細靡遺 recipe；仍保留安全與 approval invariants | 與 GPT-5.x 相同的 shared contract suite，另比較 loaded-context proxy | Exact model／host 可用時執行相同 fresh-session cases；不可用時只宣稱 source-level compatibility |
| Model-specific fork | 第一版禁止；兩類模型使用同一份 package 與行為契約 | Package inventory 不得出現未核准 variant | 後續若需要 variant，須另立 Requirement／Specification |

建議 live cases 至少涵蓋：tiny Full change、Lite change、direct-stage entry without proof、invalid project Config、artifact-producing Full stage、Review lens coverage。Exact model IDs、host versions 與 case 數量仍待後續決策。

### Acceptance criteria

1. `CSRS-AC-001`：九個 public skill IDs、plugin identity、universal software-change trigger 與 explicit user selection contract 不變。
2. `CSRS-AC-002`：Root 對 mode precedence 與全部現行 outcome 產生與 refactor 前相同的可觀察 route，Full／Lite 不交叉預載。
3. `CSRS-AC-003`：八個 public stage 的 direct-entry guard 均可獨立表達五項必要 outcome，且不重複完整 resolver matrix。
4. `CSRS-AC-004`：Conditional detail 從需要它的 `SKILL.md` 最多一個 reference hop；所有 references 存在、package-contained、無循環且由測試驗證可達。
5. `CSRS-AC-005`：Artifact producers 使用一個 canonical runtime envelope contract並保留 stage-specific requirements；任何 required field 都未消失。
6. `CSRS-AC-006`：Review 與 Architecture 使用同一個十二-lens canonical contract，兩者原有 scope、labels、simulated deletion 與 handoff 不變；Lite Review 不被升級為 Full pass。
7. `CSRS-AC-007`：Maintainer-only comments 與無決策價值的重複 recipe 從 model-visible runtime 移除，安全、approval、failure 與 evidence boundaries 仍明示。
8. `CSRS-AC-008`：Core 1.4.1 mandatory rule IDs 仍全部映射到真實可達的 Codex sections；conformance manifest 不虛報 coverage。
9. `CSRS-AC-009`：Codex unit、skill validation、conformance、package inventory、reproducible build 與適用 release tests 通過；環境限制與 skipped checks 完整揭露。
10. `CSRS-AC-010`：使用既有方法留下 before／after bytes、words 與 token-proxy evidence；改善幅度只作量測結果，不設定會誘發刪除安全契約的硬性百分比。
11. `CSRS-AC-011`：GPT-5.x 與 GPT-6 使用同一份行為契約與 package；未取得 live evidence 的 target 明確標示 `unverified`。
12. `CSRS-AC-012`：Git diff 不包含 Generic、Claude runtime、Core rule semantics、`AGENTS.md`、release version 或 generated distribution changes，除非後續另經 gate 核准。

### Confirmed decisions and deferrals

- Confirmed：Codex-only、行為等價、single-package、single-hop progressive disclosure。
- Confirmed：Universal trigger、Full／Lite、approval、stage routing、artifact semantics 與 Review lenses 本輪不改。
- Deferred：Exact shared-reference paths 由後續 Specification／Ticket 在上述 bounded contract 內落定。
- Deferred：Exact live model／host matrix、version bump、candidate build 與 publication。

### Consensus evidence

使用者於 2026-09-16 先以「核准」確認第一版採行為等價，其後以「好 那我們專注回到codex進行瘦化 優化 分責化」再次確認 Codex-only scope。在完整 RDR 與完整 Knowledge Base Change Summary 共同展示，且明示本次核准不授權 runtime implementation、version bump、candidate build、release 或 publication 後，使用者於 2026-09-16 回覆「核准」，正式共同核准兩者並授權 Knowledge Base 同步與 Draft Specification 撰寫。

## Knowledge Base Change Summary

```json
{
  "artifact_type": "Knowledge Base Change Summary",
  "artifact_id": "codex-skill-runtime-slimming-kb-change-summary",
  "workflow_id": "codex-skill-runtime-slimming-2026-09-15",
  "core_version": "1.4.1",
  "status": "Approved",
  "inputs": ["codex-skill-runtime-slimming-rdr", "codex-audit", "project-knowledge-base"],
  "assumptions": ["This summary proposes durable maintenance facts only and does not approve implementation, release, or deferred behavior changes."],
  "deferred": ["Trigger narrowing", "Review auto-correction", "Conditional lenses", "Exact cross-model live results", "Version bump", "Candidate build", "Publication"],
  "handoff": "The displayed Knowledge Base changes are synchronized; write and obtain approval for the Specification.",
  "approval": "User explicitly approved this complete Knowledge Base Change Summary together with the complete Requirement Decision Record on 2026-09-16 with `核准`."
}
```

### Additions

- Codex adapter 第一版 skill slimming 採 behavior-equivalent progressive disclosure；GPT-5.x 與 GPT-6 共用同一份 package 與行為契約。
- Codex runtime 的責任分為 root router、stage skills 與 package-contained supporting references；conditional detail 由使用它的 `SKILL.md` 直接載入，最多一個 reference hop。
- Direct-stage entries 保留 concise local mode guard；shared artifact 與 lens contract 即使集中，也不能省略 read-before-action 與 fail-closed 行為。
- Codex validation 新增 reference reachability、cycle／package checks，並以 semantic contracts 取代非契約 exact prose assertions。
- Cross-model 靜態相容與 exact-model live evidence 分開；未執行 live case 時維持 `unverified`。

### Modifications

- Project Knowledge Base 的 Codex architecture map 從「九個 public skills」細分為 root resolver／router、八個 stage skills、Lite／Full／shared references，以及 semantic contract tests。
- Codex 維護原則改為 Core semantics authoritative、adapter runtime self-contained；repository `core/` 與 `docs/` 不可成為 consumer runtime dependency。
- Codex validation guidance 增列 universal trigger preservation、direct-entry guard coverage、one-hop reference reachability、Lite isolation 與 before／after proxy evidence。

### Removals

- 在 canonical replacement 可達且已驗證後，移除 stage bodies 內重複的完整 mode-resolution prose。
- 在 canonical replacement 可達且已驗證後，移除 artifact producers 內重複的完整 portable-envelope field list。
- 在 canonical replacement 可達且已驗證後，移除 Review／Architecture 其中一份重複的十二-lens definition，只保留各 stage 的特有操作與 outcome。
- 移除 model-visible maintainer comments、一般能力提醒與不影響決策的 recipe；不移除任何 Core rule、gate、failure outcome、evidence requirement 或 safety boundary。

### Explicit non-changes

- 不改 universal trigger、public skill inventory、Full／Lite、mode Config、approval、Ticket test choice、TDD／Direct、artifact semantics、Review lenses、architecture flow 或 completion claims。
- 不改 Core mandatory rule semantics、Generic、Claude、`AGENTS.md`、release version 或 published artifacts。

### Approval boundary

正式核准必須同時涵蓋本文件中完整 RDR 及本 additions／modifications／removals。核准只允許後續建立 Draft Specification並套用這些 durable facts；不直接授權 runtime implementation、Ticket execution、release 或 publication。

Section approval state: `Approved`。已同步的 durable facts 見 [Project Knowledge Base](../../knowledge-base.md)；上述 runtime removals 仍受「canonical replacement 可達且已驗證」條件約束，本次核准不直接授權實作。

## Canonical outputs

- [Project Knowledge Base](../../knowledge-base.md)：承接本次已核准且已同步的 durable project facts。
- [Codex Skill Runtime Slimming Specification](../../../specs/codex-skill-runtime-slimming.md)：canonical Approved behavioral contract；其核准只授權 Ticket Planning。
- [Codex Skill Runtime Slimming Ticket Plan](../../../plans/codex-skill-runtime-slimming.md)：目前的 canonical Approved implementation plan；T1-T5 測試選擇已映射為 `tdd`，依序交接至 Ticket implementation。

## Source and recovery links

- [Lifecycle manifest](lifecycle-manifest.json)
- [Source manifest](migration/source-manifest.json)
- [Working Notes backup](migration/backup/working-notes.md)
- [Requirement Decision Record backup](migration/backup/requirement-decision-record.md)
- [Knowledge Base Change Summary backup](migration/backup/knowledge-base-change-summary.md)

Migration backup 只供 recovery；在本 packet 存在期間，不應從 backup 恢復第二份 current substantive owner。
