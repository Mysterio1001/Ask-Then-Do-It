# Ask Then Do It 1.3.1 Maintenance Ticket 3 Independent Review Report

Artifact type: Review Report

Artifact ID: `release-1-3-1-maintenance-ticket-3-review`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `3 - 整合 lockstep 1.3.1 identities、packages 與 checksums`

Execution mode: `tdd`

Status: Changes Requested

Review label: `independent`

Reviewed inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md) Ticket 3、final repository diff、相關 source 與 tests、release config、default `dist` inventory/checksums，以及 raw verification results。

Assumptions: Full mode 已證明；Ticket 3 Approved mode 為 `tdd`；Tickets 1、2 已接受並只作依賴；default output 由單一 builder 串行操作。

Deferred: Ticket 4 Completed release evidence、release-milestone architecture diagnosis，以及 tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement。

Handoff: 三項 P2 必須回 Ticket 3 修正；完成 Red/Green、重建 default `dist`、重跑受影響與完整驗證後，再交 fresh independent closure Review。Review 本身不授權修正或任何 external publication action。

Independence boundary: Reviewer 未讀 [Ticket 3 Implementation Evidence](release-1.3.1-maintenance-ticket-3.md)，未參與實作，也未修改 repository files。

## Findings

沒有 P0、P1 或 P3 finding。以下三項 P2 會阻擋 Ticket 3 完成。

### P2 - 重複 JSON keys 可把 failed check 覆寫成 passed

Trigger: validation ledger 的同一個 check 同時包含 `"status":"failed"` 與 `"status":"passed"`。[`read_object()`](../../scripts/validate_release_evidence.py) 使用預設 `json.loads`，採 last-write-wins；獨立 probe 實測 validator exit `0` 並輸出 `all required checks passed`。

Impact: 含失敗狀態的歧義 ledger 可被接受為 Completed release evidence，違反 duplicate metadata 與 failed-check fail-closed contract。

Remediation direction: 在 JSON object 的每一層拒絕 duplicate keys，並以 config root、ledger root 及 check object 的重複鍵建立 Red tests。

Location: `scripts/validate_release_evidence.py:31`。

### P2 - Markdown fenced code block 內的假 envelope 會被當成真正 metadata

Trigger: Draft evidence 唯一符合格式的 `Release version: \`1.3.1\`` 與 `Status: Completed` 位於 fenced code block。Validator 對完整 raw Markdown 執行行首 regex；獨立 probe 實測 exit `0`。

Impact: 沒有 top-level Completed artifact envelope 的 incomplete evidence 可通過 gate。

Remediation direction: 只解析限定的 top-level artifact envelope，排除 fenced code 與 comment content，並涵蓋 fenced、HTML comment 及衝突 top-level metadata tests。

Location: `scripts/validate_release_evidence.py:88`。

### P2 - Default `dist` 沒有完整的自動化 candidate integrity gate

Trigger: default build 後若在 extracted package 加入 stale/Pillow file，或修改 ZIP 後同步重算 checksum，目前 default-output contract只會確認兩個 archive 與 checksum 自洽。Exact inventory、source parity、ZIP equivalence、no-Pillow 與 reproducibility 都只對 temporary rebuild 驗證；`dist/` 又由 `.gitignore` 排除。

Impact: 完整 suite 可放行與 source 不一致的實際 local candidate，使 Ticket 4 可能凍結不符合 Specification criteria 9-10 的 bytes。

Remediation direction: 將 default `dist` 與 fresh build 做逐檔 byte comparison，或直接對 default candidate 執行完整 inventory、parity、ZIP equivalence 與 no-Pillow gates。

Locations: `tests/release/test_release_contract.py:92`、`tests/release/test_release_1_3_contract.py:389`、`.gitignore:2`。

## Verification

Independent reruns and inspection:

- Evidence 與 1.3 contract suites：`23/23 passed`，其中 evidence `13/13`。
- Default `dist` 與一次 fresh build：`48/48` files，inventory delta `0`、byte mismatch `0`。
- Default Codex ZIP SHA-256：`557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209`。
- Default Generic ZIP SHA-256：`6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b`。
- 兩個 archive hashes 與 `checksums.sha256` 完全相符。
- Current identity scan 未發現 active `1.3.0`；default `dist` 無 `1.3.0`。
- Historical `1.3.0` artifacts 與 guard inventory 為 `43/43`；Token fixtures hashes 為 `13/13`。
- Consumer source、package 與 default `dist` 未發現 Pillow/PIL dependency 或檔案。
- Token proxy 為 Full `14771`、Lite `5480`、reduction `62.90%`、`6290` basis points，gate passed；fixture 與 algorithm 未變。
- Marketplace、Codex conformance、Generic conformance與 `git diff --check` 通過。
- Historical `1.3.0` evidence 對 current config exit `1`；不存在的 `1.3.1` evidence exit `1`。
- Runtime 為 CPython `3.12.13`、Pillow `12.3.0`。

Provided implementation evidence, not rerun by this reviewer: focused `137/137`、full discovery `212/212`、canonical/packaged Skill 與 Plugin validators。

## Evidence Unavailable

- 沒有外部 CI 或其他作業系統的執行結果。
- 沒有真實長時間 Windows kernel lock 的確定性重現；Ticket 2 已接受的 fault-injection coverage只作依賴。
- Tag、push、GitHub Release、asset upload、Marketplace activation與 announcement 均未授權也未執行。

## Architecture And Refactoring Lenses

1. **Duplicated Code or Policy - `finding`.** Default candidate 與 temporary build 採用不同完整性 gates，形成第三項 P2。
2. **Long Function - `no-finding`.** `validate()` 涵蓋多個步驟，但仍維持單一 evidence consistency workflow。
3. **Large Module or Class - `no-finding`.** 變更集中於 release contract 與 validator responsibility，未新增跨域大型單元。
4. **Long Parameter List - `no-finding`.** Config、ledger、evidence 三個 path 是穩定且必要的 CLI interface。
5. **Data Clumps - `no-finding`.** 三項 artifact paths 只在單一入口共同傳遞，沒有重複 coordination。
6. **Primitive Obsession - `finding`.** Raw JSON/Markdown strings 承擔 artifact semantics，具體導致前兩項 P2。
7. **Feature Envy - `not-applicable`.** 相關程式是無狀態 file-validation functions，沒有跨物件 ownership。
8. **Divergent Change - `no-finding`.** Validator changes 均屬 release-evidence gate。
9. **Shotgun Surgery - `finding`.** Identity 分布與獨立 generated `dist` 要求同步修改及重建；缺少 default parity gate 使風險具體化為第三項 P2。
10. **Message Chains - `not-applicable`.** 變更沒有 object navigation 或多層 message chain。
11. **Leaky Abstraction - `finding`.** Caller 必須知道 fenced content 不得含 envelope-like text，具體對應第二項 P2。
12. **Shallow Module - `no-finding`.** Validator 以簡單 CLI 封裝 config、ledger 與 evidence consistency，interface cost 合理。

三項 finding 都可在 Ticket 3 ownership 內局部修正，尚不需要 `$improve-architecture` 系統性診斷。

## Residual Risks And Untested Areas

縮減自訂 config 的 required-check inventory 仍可通過 validator。本 Review 不另列 finding，因 Ticket 3 明確限定 current `1.3.1` config，且 `tests/release/test_release_contract.py` 已精確鎖定 13 項 inventory；若 validator 未來被視為可獨立信任的 publication gate，應把 canonical inventory 納入 validator 自身 contract。

目前 candidate bytes 實際正確，但三項 fail-closed/TDD coverage 缺口仍可產生錯誤 Completed 宣告或放行 drift。Windows external lock 超過既定 retry window、same-output concurrent builders，以及尚未執行的 Ticket 4 isolated validation仍是既有 residual risks。

## Completion Assessment

Ticket 3 **does not appear complete**。依 Approved Ticket 的「Review 無未解 blocker」條件，三項 P2 必須完成修正、驗證與 fresh independent closure Review 後，Ticket 3 才能標記 Completed。
