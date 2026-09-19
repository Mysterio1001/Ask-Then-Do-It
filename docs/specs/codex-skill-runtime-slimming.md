# Codex Skill Runtime Slimming Specification

Artifact type: Specification

Artifact ID: `codex-skill-runtime-slimming-spec`

Workflow ID: `codex-skill-runtime-slimming-2026-09-15`

Core version: `1.4.1`

Status: Approved

Inputs: Approved `codex-skill-runtime-slimming-rdr` and `codex-skill-runtime-slimming-kb-change-summary` in the [Decision Packet](../project/drafts/codex-skill-runtime-slimming/decision-packet.md); [Project Knowledge Base](../project/knowledge-base.md); current Core 1.4.1, Codex adapter sources, rule mapping, conformance manifest, tests, and package contracts.

Assumptions: 第一版只改變 Codex adapter 指令的責任歸屬、按需載入邊界與測試表達方式。相同輸入、設定、證據與使用者決策必須維持相同 route、gate、artifact state、failure behavior 與 completion boundary。GPT-5.x 與 GPT-6 使用同一份 package 與行為契約。

Deferred: Universal trigger 收窄、Review 十二 lenses 條件化、Review 自動修復、model-specific variants、Generic／Claude／Core 語意變更、exact live-model matrix、升版、candidate build、release 與 publication。

Handoff: 建立 Draft Ticket Plan 並逐 Ticket 收集測試選擇；只有完整 Ticket Plan 與全部測試選擇另行核准後，才可修改 runtime 或 tests。

Approval: 使用者於 2026-09-16 在本完整 Draft Specification 已呈現、且明示核准只授權 Ticket Planning、不授權 runtime／tests implementation、升版、candidate build、release 或 publication 後回覆「核准」。

## Problem

Codex adapter 的九個 public skills 已能表達 Core 1.4.1 契約，但目前 root skill 同時承擔 resolver 與大量只在 Full route 才需要的流程細節；八個 stage skills 重複完整 direct-entry mode guard；多個 artifact producers 重複 portable envelope；Review 與 Architecture 重複同一組十二 lenses。這些重複增加每次載入的 context、同步修改成本與政策漂移風險，而部分 tests 又把非契約性的完整文句固定成逐字介面。

## Goals

- 將 Codex runtime 分成清楚的 root router、stage skills 與 package-contained shared contracts。
- 只在 route 或 stage 確實需要時載入條件式細節，避免小任務預載完整 Full workflow。
- 讓共用契約只有一個 runtime canonical owner，同時保留 direct entry 可獨立 fail closed 的必要 guard。
- 讓 GPT-6 受益於較短、語意導向的指令，且讓 GPT-5.x 不必猜測 mode、reference、approval 或 failure outcome。
- 以 semantic contracts、可達性與 package evidence 驗證行為等價，而不是凍結一般說明文字。

## Non-goals

- 不收窄所有 software-changing operations 的 universal trigger，也不增減九個 public skill IDs、plugin identity 或 UI entry metadata。
- 不改 Full／Lite mode、precedence、Config paths、invalid Config fail-closed、direct-stage routing、任何 approval gate 或 artifact semantics。
- 不改 Ticket 的 `tdd`／`direct` 選擇與執行、Lite Change Brief／compact Review、Full Review labels、十二 lenses、architecture diagnosis 或 evidence honesty。
- 不改 Core mandatory rule meaning、Generic 或 Claude runtime，也不新增大型 `AGENTS.md`。
- 不安裝 dependency、不進行 network／live-model 呼叫、不升版、不建立 candidate、不發布。
- 不以硬性縮減百分比凌駕安全、核准、失敗或證據契約。

## Users and scenarios

### 一般軟體修改

不論 substantial feature、單行修正、格式調整或 fully specified change，Codex 仍先由 root resolver 決定本次 operation 的 Full／Lite mode。描述可以更短，但可觸發集合不能縮小。

### Lite operation

Root 在 proven Lite 後只載入 Lite lifecycle。Lite 不載入 Full route 或 Full shared contracts，不建立 Requirement Decision Record、Specification、Ticket Plan 或 Full evidence artifact，也不把 `tdd`／`direct` 當頂層 mode。

### Full operation

Root 在 proven Full 後讀取 Full routing contract，找出第一個未滿足 gate，再載入目前 stage 與該 stage 明確要求的 shared contract。未選中的 stages 不應因本次 route 被預載。

### 直接選擇 stage

直接叫用 public stage 只選擇 stage，不代表 Full。Stage 在主體內先檢查 current-operation mode proof：缺少 proof 時交回 root；proven Lite 時停止此 Full stage 並回到 Lite route；只有 proven Full 才進入 stage prerequisites。Mode 不跨 operation 保存或沿用。

### 產出 artifact

Artifact-producing stage 在產出前完整讀取 canonical shared artifact contract，再加入自己的 stage-specific fields、status、approval 與 handoff。Shared contract 不可取代 stage 自己的 gate 或輸出責任。

### Review 與 Architecture

Full Review 與 Architecture diagnosis 從同一 canonical contract 取得完整十二 lenses 與順序，但各自保留 scope、labels、simulated deletion、findings 與 handoff。Lite compact Review 不載入或套用 Full fixed-lens pass。

## Required behavior

### Identity and trigger contract

1. Plugin identity、九個 public skill IDs、UI metadata 與 explicit user selection behavior 必須保持不變。
2. Root description 必須繼續明確涵蓋 every software-changing operation，包括 trivial、formatting-only 與 single-line changes；可以精簡表達，不能縮窄適用範圍。
3. 每個 stage description 必須只描述該 stage 的精確使用時機，不能成為第二個 universal entry。

### Root responsibility

1. Root 是 capability declaration 與 current-operation Full／Lite mode resolution 的唯一 canonical owner。
2. Mode resolver 必須保留 explicit current-operation instruction、project Config、user Config、Full fallback 的 precedence，以及 conflict、absent、unreadable、malformed、missing-mode 與 unsupported value 的現行結果。
3. Root 保留所有 routes 共用的決策、安全邊界與短 stage index；只屬於 Full lifecycle 的跨階段細節在 proven Full 後按需載入，Lite lifecycle 只在 proven Lite 後載入。
4. Full 與 Lite 的條件式內容不得互相載入；Ticket-level `tdd`／`direct` 不得成為第三種頂層 mode。

### Stage responsibility

1. 每個 stage skill 只擁有自身 prerequisites、stage behavior、artifact-specific semantics、approval／stopping condition 與 handoff。
2. Specification 的行為結構仍由 Specification stage 擁有；shared artifact contract 只提供跨 artifact 共用的 envelope、status 與 evidence boundary。
3. Direct-entry guard 必須在每個 stage 主體內以 concise、可獨立理解的文字表達五項結果：stage selection 不是 Full proof、proof 缺失交回 root、Lite 停止 Full stage、只有 proven Full 繼續、mode 不跨 operation 保存或沿用。
4. Stage 可以共用 guard 形狀，但不得重複完整 resolver precedence matrix，也不得只留下沒有 outcome 的裸連結。

### Progressive disclosure and shared contracts

1. Substantial conditional detail 可以移至 consumer package 內的 supporting references；runtime 不得依賴 repository-only `core/`、`docs/` 或網路內容。
2. 每個需要 shared detail 的 `SKILL.md` 必須直接連結該 reference，明確說明何時在 action 前完整讀取。從目前載入的 `SKILL.md` 到必要 detail 最多一個 reference hop；reference 不得再要求另一 reference。
3. Required reference 必須進入 consumer package。所有 links、section targets、rule mappings 與 package inventory 都必須可機器驗證，且不能形成 cycle。
4. Shared runtime owners 至少涵蓋 Full cross-stage routing、portable artifact contract 與十二 architecture/refactoring lenses；Lite lifecycle 保持獨立 owner。最終檔名與切票方式由 Ticket Plan 決定，但不得破壞單層、直接載入與 self-contained constraints。
5. Maintainer-only comments、一般能力提醒與不影響決策的 recipe 只有在 canonical replacement 可達且驗證後才可從 model-visible runtime 移除；任何 Core rule、gate、failure outcome、evidence requirement 或 safety boundary 都不得因此消失。

### Artifact and lens contracts

1. Artifact producers 使用單一 canonical runtime envelope contract，但仍須保留每一 artifact 的 required fields、Draft／Approved 狀態、approval evidence、assumptions、deferred work 與 handoff。
2. 無法讀取 artifact contract 時，producer 必須停止，不得憑記憶省略或重建 required fields。
3. Review 與 Architecture 必須使用同一份十二-lens canonical definition、順序及允許的 outcome；兩個 stages 的既有 scope、independence labels、severity、simulated deletion 與 reflow 行為不得改變。
4. Lite Review 保持 same-context compact Review 與 correction approval，不得因共用 lenses 而變成 Full Review。

### Validation and evidence

1. Tests 必須驗證 public inventory、universal trigger、mode outcome matrix、direct-entry guard outcomes、Lite isolation、artifact field coverage、lens completeness、mandatory rule mappings、reference reachability／cycle、package inclusion 與 release reproducibility。
2. Exact prose assertion 只保留於 literal 本身是 identity、external contract、path、status、rule ID 或 security boundary 的情況；一般說明改以結構化契約或 normalized semantic markers 驗證。
3. Rule mapping 的每個 source path 與 section 必須在實際 package 中存在且可達；conformance manifest 不得只因宣告 rule ID 就視為 coverage。
4. Before／after source bytes、word count 與 loaded-context proxy 必須使用相同量測方法。這些數值只描述量測結果，不代表 billing 或 total-context 保證，也不設定會誘發刪除必要契約的最低縮減百分比。
5. 靜態 tests、package checks 與 proxy 不能替代 exact-model／host fresh-session evidence。未取得 live evidence 的 GPT-5.x 或 GPT-6 target 必須標記 `unverified`，不得宣稱 live regression-free。

## Edge cases and failure behavior

- Explicit Full 與 Lite 指示衝突時仍暫停並釐清；present invalid Config 仍依現行 precedence fail closed，不因精簡而猜測或 fall through。
- Current-operation mode proof 缺失時，direct stage 必須回到 root resolver；不能沿用先前 operation 或 session 的未記錄結果。
- Required reference 缺檔、不可讀、斷鏈、形成 cycle、超過一 hop、未進 package 或 mapping 指向不存在 section 時，validation 與受影響 route／stage 必須 fail closed。
- Artifact producer 無法取得 canonical contract 時不得省略 fields；Review／Architecture 無法取得 lens contract 時不得宣稱完成十二-lens pass。
- Full route 載入 Lite-only detail、Lite route 載入 Full-only detail，或 Lite 產生 Full artifacts，均視為 regression。
- 任何 route、gate、artifact state、Review outcome、failure result 或 completion boundary 與 refactor 前不同，均視為 behavior regression；token reduction 不得抵銷該失敗。
- Static checks 通過但 live evidence unavailable 時，可以完成 source-level refactor，結論必須保留 `unverified`，不能改寫成 model compatibility 已實證。

## Data, permissions, and external contracts

- 本變更不新增 runtime state、telemetry、credential、個資、network request、dependency 或外部 write。
- Codex project/user mode Config 的路徑、read-only 行為、accepted values 與 precedence 都保持不變；本變更不建立、修復、正規化或保存 Config。
- Consumer package 必須自足，不能把 repository 開發文件當 runtime dependency。
- Core 1.4.1 mandatory rules、Codex conformance schema、plugin identity、public inventory 與 package contract 是既有外部或跨模組契約。
- 本 Specification 的核准只授權後續 Ticket Planning；實作、測試選擇、版本、candidate、release 與 publication 各自仍受後續 gate 或明確授權約束。

## Compatibility, rollout, and recovery

第一版使用單一 Codex package 支援 GPT-5.x 與 GPT-6，不建立 model-specific variants。GPT-5.x 的相容形狀包括 direct-entry local guard、明確 imperative read-before-action、最多一層 reference，以及不依賴隱含 Core knowledge；GPT-6 使用相同安全與 approval invariants，但受益於較短 router 與 route／stage-based loading。

Rollout 先完成 source、semantic contracts、reference reachability、package inventory、rule mapping 與 before／after proxy 驗證。Exact model IDs、host versions 與 live case 數量尚未核准；可用時至少應涵蓋 tiny Full change、Lite change、direct-stage entry without proof、invalid project Config、artifact-producing Full stage 與 Review lens coverage。不可用時，相關 target 保持 `unverified`。

任何 behavior regression、broken package reference 或 mapping inconsistency 都必須阻止完成。Recovery 是恢復重構前可驗證的 Codex adapter source 與 tests，不修改 Core semantics、其他 adapters、版本或 published artifacts。是否升版、建立 candidate 或發布由後續獨立決策處理。

## Constraints and assumptions

- [現行工作流程規格](workflow.md)與 Core 1.4.1 繼續擁有 provider-neutral Full／Lite、artifact、Review 與 architecture semantics；本文件只規範 Codex 的 ownership、loading、compatibility 與 validation behavior。
- 第一版是 behavior-equivalent refactor。相同 evidence 必須得到相同 route 與 gate outcome。
- Package builder 會遞迴包含核准範圍內的 plugin-local references；實作仍須以 package inventory test 證明，而不能只依賴這項假設。
- Source bytes、words 與 proxy reduction 是 optimization evidence，不是成功的替代定義。
- Working tree 內既有使用者變更必須保留；Ticket scope 外的 runtime、documentation、version 或 distribution 變更不得混入。

## Decision traceability

| Approved decision | Normative sections | Acceptance criteria |
| --- | --- | --- |
| Codex-only、行為等價、universal trigger 不變 | Non-goals；Identity and trigger contract | `CSRS-AC-001`、`CSRS-AC-002`、`CSRS-AC-012` |
| Root／stage／shared-reference 分責 | Root responsibility；Stage responsibility；Progressive disclosure | `CSRS-AC-003`、`CSRS-AC-004`、`CSRS-AC-005` |
| GPT-5.x 與 GPT-6 使用同一 package | Progressive disclosure；Compatibility, rollout, and recovery | `CSRS-AC-004`、`CSRS-AC-011` |
| Artifact 與十二 lenses 集中但行為不變 | Artifact and lens contracts | `CSRS-AC-005`、`CSRS-AC-006` |
| Semantic tests 與證據誠實性 | Validation and evidence | `CSRS-AC-008`、`CSRS-AC-009`、`CSRS-AC-010`、`CSRS-AC-011` |

## Acceptance criteria

1. `CSRS-AC-001`：九個 public skill IDs、plugin identity、UI metadata、universal software-change trigger 與 explicit user selection contract 與 baseline 相同。
2. `CSRS-AC-002`：對 mode precedence matrix 的每個 baseline input，root 產生相同 observable route 與 failure result；Full／Lite 不交叉載入 conditional detail。
3. `CSRS-AC-003`：八個 public stages 的 direct-entry guard 各自可從 stage 主體驗證五項必要 outcome，且不包含完整 resolver precedence matrix。
4. `CSRS-AC-004`：每個 conditional contract 都由 consumer `SKILL.md` 直接連結並要求 action 前完整讀取；最長一個 reference hop，無 cycle、缺檔、repository-only dependency 或 package omission。
5. `CSRS-AC-005`：所有 artifact producers 使用一個 canonical runtime envelope contract，且 baseline 的 artifact-specific required fields、states、approval gates 與 handoffs 全數保留。
6. `CSRS-AC-006`：Full Review 與 Architecture 使用同一完整十二-lens contract；兩者 baseline scope、labels、outcomes、simulated deletion 與 handoff 保持不變，Lite Review 不套用 Full pass。
7. `CSRS-AC-007`：只有在 replacement 可達且驗證後，model-visible runtime 才移除重複 resolver prose、重複 envelope lists、第二份 lens definition、maintainer-only comments 與無決策 recipe；安全、approval、failure 與 evidence boundaries 無缺漏。
8. `CSRS-AC-008`：Core 1.4.1 mandatory rule IDs 全部映射至實際存在、可達且進入 package 的 Codex sections；conformance 與 reference validation 對斷鏈或虛報 fail closed。
9. `CSRS-AC-009`：適用的 Codex unit、skill validation、conformance、mode matrix、Lite isolation、package inventory、reproducible build 與 release contract checks 通過；所有 unavailable 或 skipped checks 明確揭露。
10. `CSRS-AC-010`：使用同一方法保存 baseline／after bytes、words 與 loaded-context proxy；報告不把 proxy 稱為 billing／total context，也不以硬性縮減比例掩蓋 regression。
11. `CSRS-AC-011`：GPT-5.x 與 GPT-6 package inventory 沒有未核准 variant，兩者共用行為契約；沒有 exact model／host fresh-session evidence 的 target 明確標記 `unverified`。
12. `CSRS-AC-012`：最終 diff 不包含 Generic、Claude runtime、Core rule semantics、`AGENTS.md`、release version、candidate 或 generated distribution 變更，除非後續另經對應 gate 核准。

## Deferred decisions

- Exact supporting-reference filenames 與 Ticket ownership；必須在 package-contained、consumer direct link、單層載入及 validator 可達性約束內決定。
- Exact GPT-5.x／GPT-6 model IDs、host versions、fresh-session case 數量與執行環境。
- Universal trigger 是否在未來收窄、Review lenses 是否條件化，以及 Review 是否可在額外核准下自動修復。
- 是否升 patch version、建立 candidate ZIP、執行 release gates 或 publication。
- Generic、Claude、Core semantics 與 `AGENTS.md` 的任何後續調整。

## Approval scope

本文件已由使用者明確核准並可進入 Ticket Planning。這次核准只授權建立 Draft Ticket Plan 與收集逐 Ticket 測試選擇；不授權 runtime／tests implementation、Ticket execution、升版、candidate build、release 或 publication。完整 Ticket Plan 與全部測試選擇仍須另行明確核准。
