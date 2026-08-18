# Ask Then Do It 1.3.1 Evidence-Only Closure Review

Artifact type: Review Report

Artifact ID: `ask-then-do-it-1-3-1-evidence-closure-review`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `4 - 完成本機整合驗證與 1.3.1 release evidence`

Execution mode: `tdd`

Status: Complete - no actionable findings

Review label: `non-independent`

Reviewed inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md) Ticket 4、[fresh independent recovery P2 closure Review](ask-then-do-it-1.3.1-final-review-after-recovery-p2.md)、[Draft release architecture diagnosis](ask-then-do-it-1.3.1-release-architecture-diagnosis.md)、[Ticket 4 implementation evidence](release-1.3.1-maintenance-ticket-4.md)、[validation ledger](ask-then-do-it-release-1.3.1.json)、[Completed release evidence](ask-then-do-it-release-1.3.1.md)、current `dist`/checksums、raw validator/full-discovery/evidence-contract results與current working-tree state。

Assumptions: 同一 output root由單一串行 builder擁有；CPython 3.12/Pillow 12.x是正式 baseline；`dist`是由 official builder產生的 frozen local candidate；external publication仍未授權。

Deferred: Architecture Draft A1-A5的接受或後續規格化、Git tag、push、GitHub Release、asset upload、Marketplace activation、Plugin installation、announcement、external CI、真正 non-Windows host及 live installed Plugin驗證。

Handoff: Ticket 4 local evidence closure已完成，implementation evidence與Ticket Plan已標為完成，disposable validation venv已移除；這不授權任何 external publication action。

## Findings

沒有 P0、P1、P2 或 P3 actionable finding。

Evidence gate已實際證明兩個 Red與一個 Green：不存在的 `1.3.1` ledger被拒絕；完整 ledger搭配 `Status: Review Pending`被精確拒絕；只把 status改為 `Completed`後，validator輸出 `Release evidence 1.3.1 validated: all required checks passed`。ledger具有config要求的精確13個、無重複 id的 checks，全部為 `passed` 且有非空 command/outcome。

Completed evidence的首段 envelope只有一個 `Release version: `1.3.1``與一個 `Status: Completed`；relative evidence links均存在。兩個 archive hashes與 `dist/checksums.sha256` 一致：

```text
557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209  codex/ask-then-do-it-1.3.1.zip
6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b  generic/ask-then-do-it-generic-1.3.1.zip
```

Post-evidence full discovery是 `216/216`；evidence/base/1.3 contracts是 `36/36`；validator重新執行通過。先前 fresh independent Full Review已關閉 recovery P2，Draft architecture diagnosis沒有未解 release-correctness blocker。release evidence沒有宣稱 tag、push、GitHub Release、upload、Marketplace activation、installation或公告已發生。

## Verification Performed

- `scripts/validate_release_evidence.py` 對 current config、ledger與Markdown evidence exit `0`。
- Full discovery：`216/216` passed；evidence/base/1.3 contracts：`36/36` passed。
- JSON parse確認 `release_version`是 `1.3.1`，checks count與unique id count均為 `13`。
- Completed envelope的 `Status`與`Release version`各恰好一筆。
- 10個 referenced evidence/config/checksum paths存在；新 evidence artifacts沒有 trailing whitespace。
- `Get-FileHash`重算兩個 ZIP並逐字比對 checksum ledger。
- `git diff --check` exit `0`；只有LF/CRLF warnings。

## Architecture And Refactoring Lenses

1. **Duplicated Code or Policy - `no-finding`.** Evidence ids與current config的精確inventory一致；architecture Draft A1/A2已記錄更廣泛且非阻斷的policy ownership proposal。
2. **Long Function - `not-applicable`.** 本closure只審查JSON/Markdown artifacts與validator result，沒有新增或修改production function。
3. **Large Module or Class - `not-applicable`.** 本closure沒有擴張builder或validator module責任。
4. **Long Parameter List - `not-applicable`.** Evidence artifacts沒有callable interface或parameter list。
5. **Data Clumps - `no-finding`.** 每個ledger entry必要地以id/status/command/outcome一起描述單一gate，未見重複且不一致的平行representation。
6. **Primitive Obsession - `no-finding`.** Validator與exact-id test約束status/version/check ids；architecture Draft A3保留更強execution-bound evidence model的未接受proposal。
7. **Feature Envy - `not-applicable`.** 受審範圍是declarative evidence，不含相鄰object ownership轉移。
8. **Divergent Change - `no-finding`.** Ticket 4 evidence檔案只為local release closure改變，沒有混入product behavior或publication責任。
9. **Shotgun Surgery - `no-finding`.** Closure只新增Ticket 4 ownership的ledger/evidence/review artifacts，沒有跨source/package修改。
10. **Message Chains - `not-applicable`.** 沒有多層object navigation；links直接指向inputs。
11. **Leaky Abstraction - `unverified`.** Validator驗證declared status與非空provenance，不重新執行各gate；本closure以raw test/CLI/hash結果交叉核對，architecture Draft A3仍是未接受的更強execution-bound assurance proposal。
12. **Shallow Module - `not-applicable`.** 本closure沒有新增module或wrapper。

## Evidence Unavailable

- 本次evidence-only review不是fresh independent：同一implementation context執行了fallback review。
- 已嘗試建立新的isolated reviewer，但服務端回傳 `429 Too Many Requests`並在retry limit後中止；這不是repository、test或candidate failure。
- 沒有在external CI、non-Windows host或live installed Plugin環境重跑。
- 沒有驗證未授權的remote `v1.3.1` URLs或進行任何external mutation。

## Residual Risks

- 真實 Windows lock超過約4.9秒仍可耗盡bounded retry；same-output concurrent builders不受支援。
- Ledger validator是declaration-bound；目前raw execution evidence、hash重算、Full Review與Draft architecture diagnosis降低此風險，但Architecture Draft A3尚未接受。
- `.ticket4-isolated-venv/`已在completion bookkeeping後移除，且從未屬於release artifact。

## Completion Assessment

所有Ticket 4 required observed gates、fresh independent Full Review、read-only architecture diagnosis、exact13-check ledger、Completed evidence validator與evidence-only closure均已完成，沒有未解 release blocker。由於evidence-only closure需以non-independent fallback完成，這個限制已明確記錄；它不改變所有本機technical gates的pass結果。

Ticket 4與本機 `1.3.1` maintenance candidate可以標記完成。外部發布仍完全延後，且需要獨立的新核准。
