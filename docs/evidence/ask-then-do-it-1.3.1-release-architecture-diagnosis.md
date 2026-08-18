# Ask Then Do It 1.3.1 Release Architecture Diagnosis

Artifact type: `Architecture Improvement Report`

Artifact ID: `ask-then-do-it-1-3-1-release-architecture-diagnosis`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Status: `draft`

Inputs: Approved Specification、Approved Ticket Plan、Approved Project Knowledge Base、Tickets 1-3 implementation evidence 與 accepted correction Reviews、三輪 final Review、current git diff/status、release source/tests/config、default `dist` 與 checksums。

Assumptions: 同一 output root 只有一個串行 builder；CPython 3.12/Pillow 12.x 是正式 baseline；canonical source 與 `release/release.json` 是權威來源，`dist/` 是可重建 generated output；最新 raw verification 對應目前 source state。

Deferred: 本報告接受或拒絕、任何 refactor、實際刪除、validation ledger、Completed release evidence、evidence-only closure、tag、push、GitHub Release、asset upload、Marketplace activation與 announcement。

Handoff: 沒有發現未解的 `1.3.1` release-correctness blocker。Ticket 4 可建立 validation ledger、Completed local release evidence 與 evidence-only closure。下列非阻斷改善不得在 Ticket 4 暗中實作。

Approval: `pending`。本 Draft 尚未獲使用者接受；即使接受，也只授權回到 `$write-spec`，不授權直接修改、刪除或 refactor。

## 1. 分析範圍與限制

能力為 `multi_agent`；本診斷由隔離的唯讀 architecture context 執行。範圍限於 `1.3.1` local release chain：

- `requirements-dev.txt`
- `release/release.json`
- release builder、Marketplace/conformance/evidence validators
- Core rules、Codex/Generic adapters、Plugin/Marketplace manifests
- active identity projection
- generated `dist`、ZIP、checksums
- release tests、historical guards 與 evidence boundary

本 context 沒有執行 builder 或測試，也沒有修改、刪除、rename、move、install、publish、tag 或 push。實際檢查限於 source/config/test 閱讀、`rg`、Git diff/status/history、dist inventory、SHA-256 與 `git diff --check`。測試結果採用主執行 context 與最新 independent Review 的 raw observations：focused correction `1/1`、transaction `11/11`、safety `6/6`、full `216/216`、evidence/base/1.3 `36/36`、official default builder passed。

本 context 獨立確認：

- `dist` 為 `48` files，沒有 `.dist-release-*` transaction root。
- 未發現 Pillow/PIL 命名的 consumer artifact。
- Codex ZIP SHA-256 為 `557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209`。
- Generic ZIP SHA-256 為 `6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b`。
- 兩者均與 `dist/checksums.sha256` 相符。
- Working tree 是累積且未提交的 candidate，無法用 commit boundary 精確歸屬每次 correction。

## 2. 系統架構摘要

### 依賴、ownership 與影響半徑

| 元件 | Ownership / reason to change | Inbound | Outbound / impact radius |
| --- | --- | --- | --- |
| `requirements-dev.txt` | 開發與 release-validation 環境 | `pip install -r`、manifest contract test | PyYAML 支援 conformance；Pillow 支援 Plugin PNG tests；不得流入 consumer packages |
| `release/release.json` | release coordination authority | builder、token proxy、evidence validator、release/package tests | 版本、package paths、Skill/module inventory、13 gates、managed outputs；變更會影響 source projections、tests、dist 與 evidence |
| `scripts/build_release.py` | config/source validation、composition、packaging、ZIP/checksum、transaction commit/recovery | CLI、Codex/Generic/release tests、token proxy 對 composer 的 import | canonical sources、Marketplace、legal/assets、temporary staging、default/test outputs |
| `validate_marketplace.py` | repository Marketplace contract | builder、Marketplace CLI/tests | `.agents/plugins/marketplace.json`；其 tag 必須與 current release 一致 |
| `validate_conformance.py` | Core/adapter conformance | Codex/Generic CLI/tests | `core/rules/rules.yaml` 與兩個 adapter manifests；依賴 PyYAML |
| `validate_release_evidence.py` | local completion consistency gate | Ticket 4、evidence tests | config、ledger、Markdown envelope；不參與 package bytes |
| Core/Codex/Generic sources | runtime policy 與 provider projections | conformance、identity、package tests | Codex 27-file package、Generic 18-file package、ZIP、hash |
| `dist/` | generated candidate delivery surface | builder、default parity/tests、hash audit | 兩個 expanded packages、兩個 ZIP、checksum ledger；不是 canonical source |
| Tests/Reviews/evidence | drift rejection 與 release assurance | approved requirements、source/config、generated output | 阻止 identity、inventory、transaction、historical 或 evidence drift |

主要資料流：

```text
requirements-dev.txt
  -> isolated CPython environment
  -> conformance + Plugin asset + full tests

Core rules + Codex/Generic sources + release.json + Marketplace
  -> builder validation/composition
  -> staged expanded packages
  -> deterministic ZIPs + checksums
  -> existing-output validation
  -> bounded transactional replacement/recovery
  -> default dist

release.json required-check inventory
  + observed commands/results
  + architecture diagnosis/final Review
  -> validation ledger + Markdown evidence
  -> evidence validator
  -> Completed local release claim
```

Current correctness defense 是多層的：builder 在 commit 前驗 staging、inventory、ZIP 與 checksum；transaction tests 鎖定 retry/recovery state；default-dist parity 將 persistent candidate 綁到 fresh build；identity/historical tests 防止 current drift 與 `1.3.0` mutation；evidence validator 負責最後的 declared-state consistency。

## 3. 安全模擬刪除結果

全部只做 `ARCH-DELETE-001` 模擬。沒有實際刪除授權，因此 actual-deletion authorization gate 不成立。

| 模擬刪除 | 預期失效與影響 |
| --- | --- |
| `requirements-dev.txt` 的 `Pillow>=12.3,<13` | Manifest contract 立即失敗；fresh CPython 3.12 安裝後缺少 `PIL`，Plugin asset module 無法 import/collect。既有裝有 Pillow 的環境可能遮蔽缺口。Codex/Generic runtime inventory本身不受影響。 |
| `release/release.json.required_validation_checks` 整個欄位 | Builder exact-key validation 失敗；evidence validator 回報缺少 gate contract；release contract test 失敗，candidate 與 Completed evidence 都不能產生。 |
| 只移除一個非 `workflow-token-proxy` check | Builder 仍接受；evidence validator 也可接受同步縮減的 ledger；只有 exact 13-item release contract test 會拒絕。這證明完整 inventory 的 fail-closed ownership 分散於 config、test 與執行流程。 |
| `retry_managed_output_operation()` 或 wrappers 的語意 | Backup、install、candidate removal 與 restore 退回單次 filesystem call；transient `WinError 5` success/parity tests 失敗，真實 Windows build 重新暴露偶發 replacement failure。 |
| `IncompleteRecoveryError`、conditional staging preservation 或 name-keyed supersession classification | 真正不完整 recovery 會遺失 primary/recovery context 或人工復原資料；完整 restore 也可能被誤報為 invalid。Transaction tests 中 incomplete-preservation 與 superseding regression 會直接失敗。 |
| Plugin manifest 的 active `version` owner | `validate_codex_source()` 拒絕 Plugin version mismatch；Plugin/identity tests 失敗；Codex expanded package 與 ZIP 不能建立。 |
| `core/CORE.md` 的 current identity projection | Identity tests 失敗，但 builder 本身不讀該文件，package build 仍可能進行；這顯示部分 lockstep projection 由 tests 而非單一生成 authority 維護。 |
| `scripts/validate_release_evidence.py` | Package build 不受影響，但 evidence tests 與 Ticket 4 CLI gate 消失；沒有機械化方式拒絕 missing/failed checks、ambiguous JSON 或假 Markdown envelope。 |
| 整個 `dist/` | Canonical source 不遺失，可由正式 builder 重建；在重建、parity、ZIP 與 hash 驗證前沒有可交付 candidate。 |
| 只刪 `dist/checksums.sha256` | Current-dist contract 與 hash gate 失敗；existing-output validation 視 `dist` 為 incomplete collision，正式 builder 不會悄悄覆寫部分 output。 |
| `validate_marketplace.py` | Builder top-level import 及 Marketplace tests 失敗；即使只選 Generic package，現有 builder 載入階段仍依賴此 validator。 |
| `core/rules/rules.yaml` | 兩個 conformance commands 失去共同規則 authority；builder core-version check 及 conformance tests 失敗。 |

## 4. 固定十二 lenses

| # | Lens | Outcome | 證據 |
| --- | --- | --- | --- |
| 1 | Duplicated Code or Policy | `finding` | 13-check policy 同時存在於 `release.json`、test constant 與 validator mandatory subset；JSON strictness 又在三個 loaders 間不一致。 |
| 2 | Long Function | `finding` | `load_config()` 約 113 行，混合 schema、Marketplace、Core sync、provider path/inventory 與 managed-output policy；新增 provider 或 gate 時需理解全部分支。 |
| 3 | Large Module or Class | `finding` | `build_release.py` 為 882 行，擁有 config/schema、assets、composition、inventory、ZIP、checksum、existing-output、retry 與 transaction 責任。 |
| 4 | Long Parameter List | `no-finding` | `commit()` 與 `IncompleteRecoveryError` 參數均是明確必要的 transaction state，且後者使用 keyword-only fields。 |
| 5 | Data Clumps | `no-finding` | Recovery diagnostics 已集中於專屬 error；release/core versions 與 provider inventory 也至少由 config 結構分組，未見散傳參數群造成獨立缺陷。 |
| 6 | Primitive Obsession | `finding` | Gate IDs、`status`、`command`、`outcome` 及多表面版本主要以無約束 strings 表達；完整 inventory 與 execution provenance 需靠外部流程補足。 |
| 7 | Feature Envy | `not-applicable` | 範圍以 procedural file/config validation 為主，沒有可合理判定 ownership 錯置的相鄰 domain object。 |
| 8 | Divergent Change | `finding` | Builder 因 package format、Plugin assets、Generic composition、release identity、ZIP/checksum 及 Windows transaction 等不同原因反覆修改；歷史每個主要 release 均觸及它。 |
| 9 | Shotgun Surgery | `finding` | Active `1.3.1` identity 可見於 56 個 source/test/doc files；此次升版跨 release、Core、adapters、Plugin、Marketplace、三語文件與大量 literal tests。 |
| 10 | Message Chains | `not-applicable` | 沒有多層 object navigation；主要依賴是直接函式、Path 與結構化檔案操作。 |
| 11 | Leaky Abstraction | `finding` | Evidence validator 輸出「all required checks passed」，但只驗 declared status 及非空 command/outcome；實際執行、exit status 與 candidate digest 由外部流程保證。 |
| 12 | Shallow Module | `no-finding` | Retry helper、structured recovery error、Marketplace/conformance/evidence validators 均封裝了具體且受測的 policy；沒有單純轉呼叫而成本高於價值的模組。 |

## 5. Findings、影響與信心

### A1 - JSON authority 採用不一致的 duplicate-key policy

Evidence: `validate_release_evidence.read_object()` 以 `object_pairs_hook` 遞迴拒絕 duplicates；`build_release.read_json_object()` 與 `validate_marketplace.load_and_validate()` 使用預設 last-write-wins `json.loads`。多數 current config tests 亦使用預設 loader。

Impact: 未來 ambiguous `release.json`、Plugin manifest 或 Marketplace JSON 可能由 builder/tests 接受，但 evidence validator 對同一類資料採不同 fail-closed 標準。Current files 沒有 duplicate keys，因此不構成 `1.3.1` blocker。

Confidence: `high`。

### A2 - 完整 required-check inventory 不是單一 fail-closed authority

Evidence: 13 項 inventory 在 `release/release.json:43` 與 `tests/release/test_release_contract.py:13` 重複；validator 只在 `scripts/validate_release_evidence.py:22` 硬性保留 `workflow-token-proxy`。模擬移除其他 check 時，builder 與 validator 仍可接受同步縮減的 config/ledger。

Impact: 若執行流程沒有先跑 exact contract test，某個必要 gate 可從 config 與 ledger 一起消失。Current config 是完整 13 項，full suite 與 evidence contracts 均已通過，因此不阻擋本 candidate。

Confidence: `high`。

### A3 - Evidence gate 是 declaration-bound，不是 execution-bound

Evidence: Validator 要求每個 item 為 `status == "passed"` 且 `command`/`outcome` 非空，但不驗 observed exit code、raw result digest、executor identity、timestamp 或被驗證的 ZIP hashes。

Impact: 錯誤或偽造的 ledger 文字可以在結構上通過。Current milestone 另有獨立 raw Review、hash 重算與完整測試觀測，故沒有建立實際錯誤 release claim；這是 assurance architecture concern，不是當前 correctness blocker。

Confidence: `high`。

### A4 - Builder 擁有過多理由變更

Evidence: 882 行單檔同時處理 schema、source、PNG、Generic composition、ZIP、checksum、output validation 與 transaction；`load_config()` 及 `commit()` 是兩個高密度區。Git history 顯示歷次 release 頻繁修改同一模組。

Impact: Package-format 與 filesystem-recovery 改動共用 failure domain；修改局部 policy 時需重跑廣泛 release gates。現有 transaction、safety、parity 與 full tests 提供強防護，因此是非阻斷 maintainability finding。

Confidence: `high`。

### A5 - Active identity 是高 fan-out 手動 projection

Evidence: Current `1.3.1`/`v1.3.1` 出現在 56 個非fixture source/test/doc files；升版需同步 config、Core、Codex/Generic manifests 與 prompts、Plugin、Marketplace、三語 docs、package names 及 literal tests。

Impact: 每次 maintenance bump 都有遺漏或誤改 historical/fixture bytes 的風險。Current exact identity tests、43-file historical guard、13-file Token fixture guard 與 default-dist parity 已證明本次同步正確，因此不阻擋 `1.3.1`。

Confidence: `high`。

## 6. 優先改善提案

1. **先完成目前 release closure，不做 refactor。** 保持 frozen candidate，建立逐項可追溯 ledger 與 Completed local evidence；任何 source/package 變更都必須重跑 affected/full gates 並重新 Review。
2. **建立單一 strict structured-data 讀取與 canonical check-contract boundary。** 若接受 A1/A2，回 `$write-spec` 定義所有 release-critical JSON 都拒絕 duplicate keys，以及哪些 checks 不可由 config 自行縮減。
3. **定義 execution-bound evidence model。** 若接受 A3，Specification 應選擇由 validator 執行 checks，或驗證包含 exit code、raw-result digest 與 candidate hashes 的結果 artifacts；不得直接在本 Ticket 補欄位。
4. **分離 pure release model/composition 與 filesystem transaction。** 若接受 A4，先規格化共享的 parsed config/validated release model，再讓 package composition 與 commit/recovery 依賴它；避免產生第二個 schema authority。
5. **降低 identity projection 手動編輯面。** 若接受 A5，規格應區分可生成 machine metadata 與需人工翻譯的 editorial docs，以結構化 matrix 驗證後者；不可用盲目 global replacement。

以上全部是 `draft`、非阻斷 proposal，不妨礙目前 `1.3.1` candidate，也不授權任何實作。

## 7. 潛在受影響模組

- A1：`scripts/build_release.py`、`scripts/validate_marketplace.py`、`scripts/validate_release_evidence.py`、release JSON tests。
- A2：`release/release.json`、evidence validator、release contract/evidence tests、future ledger schema。
- A3：evidence validator、ledger/evidence artifacts、Ticket 4 execution/evidence workflow、archive hash binding。
- A4：builder、token proxy 對 Generic composer 的 import、Codex/Generic package tests、transaction/safety tests。
- A5：release/Core/adapters/Plugin/Marketplace manifests、Generic prompt headers、Skill envelopes、root/package docs、identity/documentation tests、generated dist 與 checksums。

Historical `1.3.0` artifacts 與 Token fixtures 不屬於任何直接修改建議，必須保持 immutable。

## 8. 未解事項

- Architecture verdict：沒有未解 release-correctness blocker。
- Workflow 狀態：本報告仍為 Draft；Ticket 4 validation ledger、Completed release evidence 與 evidence-only closure 尚待後續完成。
- `.ticket4-isolated-venv/` 是 untracked disposable environment，不得進入 release artifacts。
- 本 context 未親自重跑測試、official validators 或 builder；採用最新 raw observations，並獨立驗 hash/inventory/source。
- 真實 Windows lock 超過約 4.9 秒仍會依設計失敗；永久 ACL 型 `WinError 5` 使用同一 bounded window。
- Same-output concurrent builders、非 Windows 真實 host、external CI 及 live installed Plugin 不在本版驗證範圍。
- Remote `v1.3.1` URLs 在未獲 external publication 授權前不可驗證。
- A1-A5 尚未獲接受或拒絕。
- Working tree 未 commit；任何後續 source/package 變更會使本報告的 hash 與 candidate 判定失效。

## 9. Artifact links

- [Approved Specification](../specs/release-1.3.1-maintenance.md)
- [Approved Ticket Plan](../plans/release-1.3.1-maintenance.md)
- [Project Knowledge Base](../project/knowledge-base.md)
- [Ticket 1 Evidence](release-1.3.1-maintenance-ticket-1.md)
- [Ticket 1 Review](release-1.3.1-maintenance-ticket-1-review.md)
- [Ticket 2 Evidence](release-1.3.1-maintenance-ticket-2.md)
- [Ticket 2 accepted correction Review](release-1.3.1-maintenance-ticket-2-review-after-p2.md)
- [Ticket 3 Evidence](release-1.3.1-maintenance-ticket-3.md)
- [Ticket 3 accepted correction Review](release-1.3.1-maintenance-ticket-3-review-after-envelope-p2.md)
- [Initial Final Review](ask-then-do-it-1.3.1-final-review.md)
- [Final Review after first P2](ask-then-do-it-1.3.1-final-review-after-p2.md)
- [Fresh recovery P2 closure Review](ask-then-do-it-1.3.1-final-review-after-recovery-p2.md)
- [Release configuration](../../release/release.json)
- [Release builder](../../scripts/build_release.py)
- [Evidence validator](../../scripts/validate_release_evidence.py)
- [Default checksums](../../dist/checksums.sha256)

## 10. Knowledge Base Change Summary

`not-applicable`。本診斷沒有修改 Project Knowledge Base，也沒有產生新的 Approved durable knowledge。A1-A5 只是尚未接受的 Draft findings。

若使用者日後接受任一 proposal，只能先回 `$write-spec`；經 Approved Specification、Approved vertical Ticket Plan 及 plan-selected implementation 後，才可另行提出 Knowledge Base additions/modifications/removals 供明確核准。
