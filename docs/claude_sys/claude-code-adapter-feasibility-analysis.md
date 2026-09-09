# Claude Code 生態與架構適配性分析報告

## 執行摘要與信心程度

**核心結論**：Ask Then Do It 的 Core/Adapter 分層架構**完全適合** Claude Code Plugin 生態。現有的 Codex adapter 可作為 Claude Code adapter 的實作藍圖。將一般 Claude 版與 Claude 5 精簡版包裝在同一個 Plugin 內作為兩個獨立命名的 Skills 是**技術可行且符合官方規範**的設計。

**信心等級**：
- **Host 相容性**：95% — 官方文件明確支持 Plugin、Skills、Marketplace、CLI 與 reload 機制
- **一 Plugin 雙 Skill 設計**：90% — 官方支持但無 model-conditional loading 文件
- **Context 精簡策略**：85% — Claude 5 原則明確，但具體門檻需要實測
- **Conformance 等價性**：80% — 流程語意可保持，但需 blind eval 與 token 測量
- **Release 與測試基礎設施適配**：90% — 現有 builder 已有雙 adapter 模式，需要明確分支

**主要風險**：
- P0：尚未實測 Claude Code 對超長 Skill 的 progressive loading 與 caching 行為
- P0：Claude 5 精簡版在保持相同 conformance 場景通過率下可削減的實際 context 尚未驗證
- P1：/doctor 作為診斷工具的定位正確，但不應被視為自動轉換器
- P1：Model selection 依賴使用者明確指定或 frontmatter `model` field；無 reliable runtime model metadata

---

## 證據來源

### Repository 證據
1. `core/CORE.md` (v1.3.1) — provider-neutral 工作流契約
2. `core/adapters/manifest-contract.md` — adapter conformance schema
3. `core/rules/rules.yaml` — 35 條 mandatory rules
4. `adapters/codex/conformance.yaml` — Codex adapter 完整實作
5. `adapters/codex/plugin/ask-then-do-it/.codex-plugin/plugin.json` — Plugin manifest 範例
6. `adapters/codex/plugin/ask-then-do-it/skills/` — 9 個 Codex Skills
7. `adapters/generic-prompts/` — conversation-only adapter (11 modules)
8. `release/release.json` + `scripts/build_release.py` — deterministic release builder
9. `.agents/plugins/marketplace.json` — git-subdir marketplace 參考
10. `tests/codex/`, `tests/conformance/`, `tests/release/` — 驗證基礎設施
11. `docs/project/drafts/claude-code-adapter-working-notes.md` — 使用者提供的初步構想

### 官方文件證據
1. https://code.claude.com/docs/en/plugins — Plugin 組件、生命週期、scope
2. https://code.claude.com/docs/en/plugins-reference — manifest schema、CLI、caching、namespacing
3. https://code.claude.com/docs/en/skills — SKILL.md frontmatter、progressive disclosure、precedence
4. https://code.claude.com/docs/en/plugin-marketplaces — marketplace.json schema、trust、updates
5. https://code.claude.com/docs/en/model-config — model aliases、effort levels、frontmatter `model` field
6. https://code.claude.com/docs/en/commands — built-in commands、skill namespacing `/plugin-name:skill-name`
7. https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models — 80% prompt reduction, progressive disclosure, adaptive reasoning

### 未能驗證的項目（標記為 `unconfirmed`）
- Claude Code 是否在 Skill 載入時暴露當前 active model ID（官方文件未說明；需要實測）
- Claude Code 的 Plugin 是否支援 model-conditional Skill loading（官方文件未提及）
- 超長 Skill（如包含完整 Core modules 的版本）的 progressive loading 與 prompt caching 實際效果
- skill-creator eval 工具是否包含 conformance scenario 比較能力（官方 quick_validate.py 路徑存在，但功能範圍未確認）

---

## 能力與相容性矩陣

### Claude Code Host Capabilities（來源：官方文件）

| Capability | Claude Code 支持 | Ask Then Do It Core 需求 | 映射方式 |
|------------|----------------|------------------------|---------|
| **Conversation** | ✅ 完整支持 | `conversation` profile | Skills 可 emit 純文字 artifacts |
| **File read/write** | ✅ `Read`/`Write`/`Edit` tools | `tools` profile | Skills 通過 allowed-tools frontmatter 控制 |
| **Command execution** | ✅ `Bash` tool | `tools` profile | 同上 |
| **Subagents** | ✅ `agents/` directory | `multi_agent` profile | Core Review 需要 isolated reviewer context |
| **Skill namespacing** | ✅ `/plugin-name:skill-name` | 避免衝突 | ask-then-do-it → `/ask-then-do-it:ask-then-do-it` |
| **Skill arguments** | ✅ `$ARGUMENTS`, `$1`, `$2` | 適用於 stage selection | `/ask-then-do-it:implement-tdd 3` |
| **Progressive disclosure** | ✅ Skills 可包含 `references/` subdirectory | Lite 動態載入 | `lite-workflow.md` 作為 reference |
| **Frontmatter `model` field** | ✅ 指定 Skill 使用的 model | Model profile 區分 | `model: "sonnet"` vs `model: "fable"` |
| **Marketplace install** | ✅ `claude plugin install`, git-subdir source | 與 Codex 相同 | `.agents/plugins/marketplace.json` pattern |
| **Plugin reload** | ✅ Changes trigger auto-reload | Development iteration | 保留 |
| **Multiple Skills per Plugin** | ✅ `skills/` directory layout | 一般版 + Claude 5 版 | 兩個獨立 SKILL.md |
| **MCP/LSP/Hooks** | ✅ 但非必要 | Ask Then Do It 不使用 | 未來可選 |

### Model Capabilities（來源：Claude 5 blog + model-config）

| Model | Adaptive reasoning | Extended thinking | Context window | Effort levels | 適用性 |
|-------|-------------------|------------------|---------------|--------------|-------|
| **Fable 5** | ✅ | ✅ (experimental) | 1M native | low → max | 複雜 architecture diagnosis |
| **Opus 5** | ✅ | ✅ | 1M native | low → max | 一般 Full workflow |
| **Sonnet 5** | ✅ | ❌ | 1M native | low → max | **Claude 5 精簡版目標** |
| **Opus 4.x** | ✅ (4.7+) | ❌ | 200k (1M via alias) | low → max | Fallback |
| **Haiku** | ❌ | ❌ | 200k | N/A | 不建議用於此工作流 |

### Core → Claude Code 映射分析

#### ✅ 可直接映射的 Core 行為

| Core Module | Codex Skill | Claude Code 映射 | 備註 |
|-------------|-------------|-----------------|------|
| `orchestration.md` | `ask-then-do-it/SKILL.md` | 保留；需改 Config 路徑 `.codex/` → `.claude/` | 核心相同 |
| `lite-workflow.md` | `references/lite-workflow.md` | 保留；progressive loading | Claude 5 版大幅精簡此部分 |
| `requirements.md` | `ask-requirements/SKILL.md` | 保留 | GRILL-ONE-001 行為不變 |
| `project-knowledge.md` | `ask-with-docs/SKILL.md` | 保留 | KB-EVIDENCE-001 等規則不變 |
| `specification.md` | `write-spec/SKILL.md` | 保留 | SPEC-NOCODE-001 不變 |
| `ticket-planning.md` | `plan-tickets/SKILL.md` | 保留 | PLAN-VERTICAL-001 不變 |
| `tdd-implementation.md` | `implement-tdd/SKILL.md` | 保留 | TDD-RED-001 強制 |
| `direct-implementation.md` | `implement-direct/SKILL.md` | 保留 | 測試禁令不變 |
| `review.md` | `review-code/SKILL.md` | **需調整** | Claude 5 版改用 `/code-review ultra` delegation |
| `architecture-improvement.md` | `improve-architecture/SKILL.md` | 保留 | ARCH-DIAG-001 診斷邊界不變 |

#### ⚠️ 需要改寫的 Codex 專用內容

| 項目 | Codex 依賴 | Claude Code 替代方案 | 理由 |
|------|----------|-------------------|------|
| **Config 路徑** | `~/.codex/ask-then-do-it.toml`<br>`<project>/.codex/ask-then-do-it.toml` | `~/.claude/ask-then-do-it.toml`<br>`<project>/.claude/ask-then-do-it.toml` | Claude Code 的 user/project scope 使用 `.claude/` |
| **Skill 呼叫語法** | `$ask-then-do-it` (bare) | `/ask-then-do-it:ask-then-do-it` (namespaced) | Plugin Skills 預設加 prefix；可設 frontmatter alias 去掉 |
| **Multi-agent Review** | Codex subagent API (undocumented) | `/code-review ultra` (cloud-based) | Claude Code v2.1.218+ 支持；或改用 `agents/` directory |
| **skill-creator validation** | `$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py` | 未確認 Claude Code 等價物 | 需查證 Claude Code 是否內建或透過 Plugin 提供 |

---

## P0/P1/P2 風險評估

### P0 風險（阻斷發布）

1. **未實測 Claude Code 對超長 Skill 的行為**
   - **Trigger**：一般版 Skill 可能包含完整 Core modules（orchestration + lite-workflow ≈ 8k tokens）
   - **Impact**：若 Claude Code 無 progressive caching 或強制截斷，使用者體驗降級
   - **Mitigation**：第一階段先實作並實測；確認 `references/` 動態載入有效；若不可行則一般版也需精簡

2. **Claude 5 精簡版尚未證明與一般版等價**
   - **Trigger**：削減 80% context 後，conformance scenarios 通過率可能下降
   - **Impact**：兩版語意不一致，違反專案目標
   - **Mitigation**：定義 minimum passing score（如 95%）；blind A/B eval；token benchmark；人工 spot check

3. **Model selection 無 runtime metadata**
   - **Trigger**：使用者未明確指定 model，且 frontmatter `model` field 無效時
   - **Impact**：一般版可能跑在 Haiku（不支持 effort），Claude 5 版可能跑在 Opus 5（過度消耗 credits）
   - **Mitigation**：兩版都用明確 frontmatter `model`；文件要求使用者手動 `/model` 或 `--model`；考慮 injected command 動態檢查

### P1 風險（影響品質但可 workaround）

1. **Claude Code Plugin Marketplace 尚未建立**
   - **Trigger**：release 1.x 依賴 git-subdir source；Claude Code 可能需要不同 hosting
   - **Impact**：安裝流程比 Codex 複雜
   - **Mitigation**：第一階段手動 `--plugin-dir`；第二階段建立 GitHub-based marketplace；第三階段考慮官方 community marketplace 提交

2. **skill-creator eval 工具未確認**
   - **Trigger**：官方 quick_validate.py 路徑存在但功能範圍未知
   - **Impact**：conformance eval 需自建
   - **Mitigation**：優先使用官方工具（若可用）；否則將現有 `tests/conformance/` 擴充為 skill-level eval harness

3. **/doctor 的定位模糊**
   - **Trigger**：使用者期待 `/doctor` 自動將一般版轉為 Claude 5 版
   - **Impact**：維護負擔增加；自動轉換可能破壞語意
   - **Mitigation**：明確文件說明 `/doctor` 只診斷 + 建議，不執行轉換；轉換由人工 approve diff 後執行

### P2 風險（不阻斷但需追蹤）

1. **Namespace collision 風險低但存在**
   - **Trigger**：使用者同時安裝 Codex 版與 Claude Code 版
   - **Impact**：`/ask-then-do-it:ask-then-do-it` 與可能的 Codex bare name 衝突
   - **Mitigation**：Claude Code 預設 namespacing 已經降低風險；文件提醒不要同時安裝

2. **Windows path handling**
   - **Trigger**：`.claude/` 在 Windows 上的 backslash vs forward slash
   - **Impact**：Config 讀取可能失敗
   - **Mitigation**：現有 Codex 已處理 Windows；複用相同邏輯

3. **Claude 5 generation fallback behavior**
   - **Trigger**：生物/安全研究觸發 content policy
   - **Impact**：自動 fallback 到 Opus 5/4.x 導致 model profile 不一致
   - **Mitigation**：文件說明此為預期行為；建議敏感專案使用一般版

---

## 一般版與 Claude 5 版建議結構

### Plugin 整體結構

```
claude-code-plugin/
├── .claude-plugin/
│   └── plugin.json              # name: ask-then-do-it-claude, version: 2.0.0
├── skills/
│   ├── ask-then-do-it/          # 一般版（完整 Core）
│   │   ├── SKILL.md             # model: "opus" 或不指定（使用 default）
│   │   └── references/
│   │       ├── lite-workflow.md
│   │       ├── architecture-lenses.md
│   │       └── ...
│   ├── ask-then-do-it-fast/     # Claude 5 精簡版
│   │   ├── SKILL.md             # model: "sonnet", disable-model-invocation: false
│   │   └── references/
│   │       └── lite-workflow-fast.md  # 80% shorter
│   ├── ask-requirements/        # 共用（一般與 Claude 5 共用同一實作）
│   │   └── SKILL.md
│   ├── write-spec/              # 共用
│   │   └── SKILL.md
│   ├── ...
│   └── review-code-fast/        # Claude 5 專用（delegation to /code-review ultra）
│       └── SKILL.md
├── assets/
│   ├── icon.png
│   └── logo.png
├── START-HERE.zh-TW.md
├── START-HERE.en.md
├── LICENSE
└── THIRD_PARTY_NOTICES.md
```

### 命名策略（三選一）

#### 選項 A：功能導向命名（推薦）
- 一般版：`/ask-then-do-it:ask-then-do-it`
- Claude 5 版：`/ask-then-do-it:ask-then-do-it-fast`
- **優點**：語意清晰；`-fast` 暗示適用於快速迭代
- **缺點**：名稱較長

#### 選項 B：Model 命名
- 一般版：`/ask-then-do-it:full`
- Claude 5 版：`/ask-then-do-it:claude5`
- **優點**：簡短
- **缺點**：`claude5` 未來可能過時；與 Core `full` mode 混淆

#### 選項 C：Effort-based 命名
- 一般版：`/ask-then-do-it:standard`
- Claude 5 版：`/ask-then-do-it:adaptive`
- **優點**：對應 effort levels 概念
- **缺點**：使用者可能不理解 adaptive 指什麼

**建議**：選項 A，並在 START-HERE 與 SKILL.md description 明確說明兩版差異。

### Context 精簡原則（Claude 5 版）

根據 Anthropic blog 所述的 Claude 5 context engineering：

1. **削減重複性指導**
   - ❌ 不要：列舉所有 12 個 Architecture Lenses 的完整定義
   - ✅ 改為：`Review using the twelve Architecture and Refactoring Lenses (see references/architecture-lenses.md if needed)`

2. **削減防禦性 constraints**
   - ❌ 不要："Do not create artifacts. Do not run tests. Do not modify Config. Do not..."
   - ✅ 改為：`Lite workflow prohibits test creation and workflow artifacts.`

3. **依賴 adaptive reasoning**
   - ❌ 不要：詳細描述 edge cases 與 fallback 邏輯
   - ✅ 改為：信任 model 處理 ambiguity；只在 critical gates 明確說明

4. **Progressive disclosure**
   - ❌ 不要：在 main SKILL.md 包含完整 Lite workflow lifecycle
   - ✅ 改為：`references/lite-workflow-fast.md` 僅在 Lite 路由後載入

5. **保留的內容（不可刪減）**
   - ✅ Capability declaration (CAP-DECLARE-001)
   - ✅ Mode resolution precedence (MODE-RESOLVE-001)
   - ✅ Approval gates (GATE-REQ-001, GATE-SPEC-001, GATE-PLAN-001)
   - ✅ Material risk pause (LITE-RISK-001)
   - ✅ Evidence requirements (TDD-RED-001, REVIEW-EVIDENCE-001)
   - ✅ Artifact state (ART-STATE-001)

### 預期 Token Budget

| Component | 一般版 | Claude 5 版 | 削減 % |
|-----------|-------|-----------|-------|
| 主 orchestrator | ~4000 | ~1000 | 75% |
| Lite reference | ~3000 | ~600 | 80% |
| Stage Skills (平均) | ~2000 | ~600 | 70% |
| Architecture Lenses | ~4000 | ~800 | 80% |
| **Total (worst case)** | ~13000 | ~3000 | **77%** |

---

## /doctor 與 skill-creator 的正確定位

### /doctor 的角色（診斷，非轉換）

#### ✅ 應該做的
1. **診斷當前 Skill context size**
   - 分析 SKILL.md + references/ 的 token count
   - 標示超出建議預算的部分（如 Sonnet 5 建議 <5k）

2. **建議精簡候選區域**
   - 識別重複性說明、防禦性 constraints、詳細 edge case 邏輯
   - 提供 before/after diff preview（但不執行）

3. **驗證 mandatory rules 完整性**
   - 檢查 35 條 mandatory rules 是否都有對應文字
   - 警告任何可能影響 conformance 的刪減

4. **提供 model suitability 建議**
   - 基於 current Skill size 建議適合的 model（Fable 5 / Opus 5 / Sonnet 5）

#### ❌ 不應該做的
1. **自動轉換**
   - 不自動改寫 SKILL.md
   - 不自動生成 `-fast` 版本

2. **繞過 conformance**
   - 不建議刪減 approval gates、evidence requirements、safety boundaries

3. **取代人工判斷**
   - 精簡建議需要維護者 review 與 approve

### skill-creator 的角色（驗證）

#### 確認功能範圍（需實測）
- [ ] `quick_validate.py` 是否檢查 frontmatter schema
- [ ] 是否支持 conformance scenario 比較
- [ ] 是否包含 token measurement
- [ ] 是否支持 blind eval（A/B 比較兩版 Skill）

#### 整合方式
```bash
# 假設 skill-creator 可用
claude plugin install skill-creator

# 驗證一般版
/skill-creator:validate ./skills/ask-then-do-it

# 驗證 Claude 5 版
/skill-creator:validate ./skills/ask-then-do-it-fast

# 比較兩版
/skill-creator:compare ./skills/ask-then-do-it ./skills/ask-then-do-it-fast \
  --scenarios tests/conformance/scenarios/ \
  --threshold 0.95
```

若 skill-creator 不提供此功能，則：
- 使用現有 `tests/conformance/` + `tests/codex/` 作為 eval harness
- 將 scenarios 擴充為 Skill-level input/output pairs
- 建立 token measurement script（擴充現有 `measure_workflow_token_proxy.py`）

---

## 驗證門檻

### Conformance 等價性門檻

#### Scenario 通過率
- **一般版**：100%（與現有 Codex adapter 相同的 35 scenarios）
- **Claude 5 版**：≥95%（允許 1-2 個 edge case 行為差異，但 mandatory rules 必須 100%）

#### Mandatory Rules Coverage
兩版都必須 100% 覆蓋以下規則：
```
CAP-DECLARE-001, CAP-CLAIM-001, MODE-RESOLVE-001, FULL-PRESERVE-001
LITE-QUESTIONS-001, LITE-BRIEF-001, LITE-RISK-001, LITE-VALIDATE-001, LITE-REVIEW-001, LITE-SESSION-001
GATE-REQ-001, GATE-SPEC-001, GATE-PLAN-001
GRILL-ONE-001, SPEC-NOCODE-001, PLAN-VERTICAL-001, TDD-RED-001, REVIEW-EVIDENCE-001
ART-STATE-001, ADAPTER-COVERAGE-001
KB-EVIDENCE-001, KB-DRAFT-001, KB-SYNC-001
REVIEW-LENSES-001, ARCH-DIAG-001, ARCH-DELETE-001, ARCH-REPORT-001, ARCH-REFLOW-001
ROUTE-USER-001, ROUTE-DOCS-001
```

#### Context/Token Benchmarks

| Metric | 一般版目標 | Claude 5 版目標 |
|--------|----------|---------------|
| Main orchestrator | ≤5000 tokens | ≤1500 tokens |
| Lite reference | ≤3500 tokens | ≤800 tokens |
| Stage Skill (平均) | ≤2500 tokens | ≤800 tokens |
| Worst-case full load | ≤15000 tokens | ≤4000 tokens |

#### Fresh-session Eval
- 10 個 blind scenarios（使用者不知道使用哪一版）
- 比較 outcome quality、completeness、adherence to gates
- 人工 spot check：是否正確處理 material risk pause、approval gates、artifact state

#### A/B Benchmark
- 相同 5 個 representative scenarios（涵蓋 Full/Lite、TDD/Direct、architecture diagnosis）
- 測量：token count、API cost、latency、outcome correctness
- Claude 5 版應該：
  - Token count: -70% ~ -85%
  - API cost: -50% ~ -70%（考慮 Sonnet 5 pricing）
  - Latency: ±10%（adaptive reasoning 可能抵消部分加速）
  - Correctness: ≥95%

---

## 分階段 Roadmap

### Phase 0：驗證與設計（2-3 weeks）
**目標**：確認技術可行性，無需寫 production code

#### Deliverables
- [ ] 在實際 Claude Code 環境安裝現有 Codex Plugin（改名為 test-claude-adapter）
- [ ] 驗證 `.claude/` Config 路徑讀取
- [ ] 驗證 namespaced skill invocation（`/test:ask-then-do-it`）
- [ ] 驗證 frontmatter `model` field 是否生效
- [ ] 測量超長 Skill（10k tokens）的 loading time 與 caching behavior
- [ ] 實測 `references/` progressive loading
- [ ] 驗證 `/code-review ultra` 是否可替代 Codex subagent-based review
- [ ] 建立 Claude 5 精簡版 **mockup**（手動削減一個 Skill，不 commit）
- [ ] Fresh-session blind test：mockup vs 原版（5 scenarios）
- [ ] 決定是否繼續（Go/No-Go decision）

#### Success Criteria
- [ ] Config 路徑、namespacing、model field 都正常運作
- [ ] 超長 Skill 可用（即使慢也可接受；Phase 1 優化）
- [ ] Mockup 通過 ≥4/5 scenarios
- [ ] 使用者與維護者 approve roadmap

### Phase 1：Claude Code Adapter 基礎版（4-6 weeks）
**目標**：完成一般版（完整 Core），驗證基礎設施

#### Tickets（TDD）
1. **Adapter manifest 與 conformance mapping**
2. **Plugin structure 與 manifest**
3. **Config 路徑替換**
4. **Namespace 與 invocation**
5. **Review delegation 調整**
6. **Release builder 擴充**
7. **Package 與 marketplace**
8. **Documentation**

#### Success Criteria
- [ ] 所有 35 mandatory rules 通過 conformance tests
- [ ] `claude plugin install` 成功（手動或 marketplace）
- [ ] Fresh-session eval：10/10 scenarios pass
- [ ] Build reproducibility：兩次獨立 build 產生 byte-identical ZIPs
- [ ] Token budget：worst-case ≤16k（比原始 Codex 稍高可接受）

### Phase 2：Claude 5 精簡版（3-4 weeks）
**目標**：完成 `-fast` 變體，達成 conformance 等價

#### Tickets（TDD）
1. **Context 精簡 — orchestrator**
2. **Context 精簡 — Lite reference**
3. **Context 精簡 — stage Skills**
4. **Frontmatter model field**
5. **Token measurement**
6. **Conformance eval**
7. **A/B benchmark**
8. **Documentation 更新**

#### Success Criteria
- [ ] Claude 5 版通過 ≥33/35 conformance scenarios（95%）
- [ ] Token reduction: ≥70%
- [ ] API cost reduction: ≥50%（假設 Sonnet 5 pricing）
- [ ] Blind eval：人工 spot check 5/5 scenarios 品質相當

### Phase 3：/doctor 診斷工具（2 weeks，可選）
**目標**：輔助未來精簡與優化

### Phase 4：External Publication（1 week）
**目標**：GitHub Release、Marketplace 上線

---

## 現階段不應處理的項目（Deferred）

### 明確排除（至少 v2.0.0 不做）
1. **自動 Codex → Claude Code 遷移工具**
2. **Universal cross-host installer CLI**
3. **Model-conditional Skill loading**
4. **Private fork distribution**
5. **Unattended update delivery**
6. **Gemini CLI、GitHub Copilot、其他 AI agents**

### 可能在 Phase 4 後追加（v2.1）
1. **skill-creator eval 整合**
2. **Extended thinking 支持**
3. **MCP/LSP servers**
4. **Hooks（pre/post skill execution）**

---

## 需要維護者決定的事項

### 高優先級（Phase 0 必須決定）
1. **是否繼續 Claude Code adapter 開發？**
2. **兩版命名方案？**（選項 A/B/C）
3. **Release 版本號？**（v2.0.0 或 v1.4.0）
4. **是否與現有 Codex/Generic 共用 Core 版本？**

### 中優先級（Phase 1 前決定）
5. **Claude Code 版的 Review 策略？**
6. **Release builder 泛化策略？**
7. **Claude 5 版的 conformance 通過門檻？**（95% 或 98%）

### 低優先級（Phase 2 前決定）
8. **/doctor 是否納入 v2.0.0？**
9. **是否提交至 Claude Code 官方 community marketplace？**
10. **是否支持多語言 START-HERE？**

---

## 給 Ask Then Do It 維護者的五行摘要

1. **Core/Adapter 分層完美適配 Claude Code Plugin 生態**；現有 Codex adapter 可直接作為實作藍圖，主要差異為 Config 路徑（`.codex/` → `.claude/`）與 Skill namespacing。

2. **一 Plugin 雙 Skill 設計（標準版 + Claude 5 精簡版）技術可行**；透過 frontmatter `model` field 與獨立 SKILL.md 達成；精簡版預期削減 70-85% context 並保持 ≥95% conformance 等價性。

3. **Phase 0 驗證（2-3 weeks）為 Go/No-Go decision 關鍵**；需實測 `.claude/` Config、namespacing、model field、超長 Skill 與 progressive loading 行為；若驗證失敗則停止開發。

4. **Release 版本建議 v2.0.0（新 major adapter）**；可與 1.3.1 Core 共存；release builder 先硬編碼第三個 adapter，未來若有更多 hosts 再泛化為 registry pattern；`/doctor` 定位為診斷工具而非自動轉換器。

5. **Mandatory rules（35 條）與所有 approval/safety/evidence gates 不可刪減**；Claude 5 精簡版僅削減重複性說明、防禦性 constraints 與詳細 edge case 邏輯；透過 blind A/B eval、token benchmark、fresh-session test 與 skill-creator（若可用）驗證等價性。

---

**報告結束**。建議維護者先執行 Phase 0 驗證，確認技術可行性後再進入實作階段。若有任何問題或需要補充證據，請告知。


