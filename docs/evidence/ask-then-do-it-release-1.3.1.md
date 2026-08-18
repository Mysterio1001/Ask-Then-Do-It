# Ask Then Do It Release 1.3.1 Evidence

Artifact type: Release Evidence

Artifact ID: `ask-then-do-it-release-1.3.1-evidence`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Release version: `1.3.1`

Status: Completed

Inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md)、Tickets 1-4 implementation evidence、accepted ticket Reviews、[fresh recovery P2 closure Review](ask-then-do-it-1.3.1-final-review-after-recovery-p2.md)、[release architecture diagnosis](ask-then-do-it-1.3.1-release-architecture-diagnosis.md)、[evidence-only closure Review](ask-then-do-it-1.3.1-evidence-closure-review.md) 與 [validation ledger](ask-then-do-it-release-1.3.1.json)。

Assumptions: 本文件只聲明 frozen local pre-publication candidate；CPython 3.12/Pillow 12.x 是正式 baseline；同一 output root 只由一個串行 builder 寫入。

Deferred: Evidence-only closure、Architecture Draft A1-A5 的判定與任何後續規格流程、Git tag、push、GitHub Release、asset upload、Marketplace activation、Plugin installation、announcement、external CI、真正 non-Windows host 與 live installed Plugin驗證。

Handoff: `Review Pending` evidence已被 validator正確拒絕；只變更此 status為 `Completed` 後，validator已通過。外部發布仍需另一次明確核准，不由本機 evidence、review 或 architecture diagnosis授權。

## Outcome

Ask Then Do It `1.3.1` maintenance candidate已在 isolated CPython `3.12.13` / Pillow `12.3.0`環境完成本機 validation。Pillow只存在於 development/test environment；Codex與Generic consumer packages不包含Pillow。Windows managed-output replacement與recovery現在使用 bounded `WinError 5` retry，完整恢復與不完整恢復具有不同且受測的最終狀態與cleanup/diagnostic行為。

Current release、Core、Codex/Generic adapters、Plugin、Marketplace candidate metadata、current documents、runtime identity、package names、ZIP與checksums均為 `1.3.1`。Approved `1.3.0` artifacts與 frozen Token benchmark inputs保持 byte-identical。

## Validation

- Main full discovery：`216/216` passed；independent reviewer另取得兩次 clean `216/216`。
- Final serial suites：release `131/131`、Codex `27/27`、Generic `39/39`、conformance `19/19`。
- Transaction `11/11`、release safety `6/6`、evidence/base/1.3 contracts `36/36`。
- Canonical與packaged Skill validation `18/18`；Plugin validation `2/2`。
- Marketplace、Codex conformance與Generic conformance CLIs全部passed against current `1.3.1` contracts。
- Package inventory focus `9/9`；Codex expanded package/ZIP為27 files，Generic為18 files，兩者均無Pillow consumer dependency。
- Reproducibility/ZIP focus `2/2`；two isolated builds與default `dist` inventory及bytes一致，ZIP entries與expanded directories等價。
- Documentation、Marketplace、clean-slate、historical及Token fixture guards `42/42`。
- Token proxy保持 Full `14,771`、Lite `5,480`、difference `9,291`、reduction `62.90%`，通過未變的 `60.00%` gate；Generic fixed cost `15,376`，沒有Generic reduction或API billing claim。
- `git diff --check` exit `0`；沒有 whitespace error，只有既有 LF/CRLF warnings。
- `dist`有48 files，沒有 transaction staging root。
- Evidence-only closure沒有 actionable finding；其因服務端 reviewer `429` 而採用的 non-independent fallback與限制已明確記錄。

## Runtime Baseline

```text
Python: 3.12.13
ignore_environment: 1
venv include-system-site-packages: false
Pillow: 12.3.0 from .ticket4-isolated-venv/Lib/site-packages/PIL
PyYAML: 6.0.3 from .ticket4-isolated-venv/Lib/site-packages/yaml
```

## Archive Hashes

```text
557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209  codex/ask-then-do-it-1.3.1.zip
6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b  generic/ask-then-do-it-generic-1.3.1.zip
```

兩個獨立重算值均與 `dist/checksums.sha256` 相符，且 recovery P2 correction前後未改變。

## Review And Architecture

Fresh independent Full Review關閉兩輪 recovery P2，最終沒有 P0-P3 actionable finding。Read-only release-milestone architecture diagnosis沒有未解 release-correctness blocker。

Architecture report維持 Draft。A1-A5涉及 strict JSON authority、required-check authority、execution-bound evidence、builder責任與active identity fan-out，全部是非阻斷且未接受的後續提案，不授權本 release暗中重構。

## Observed Transients

一次 release-suite run在 deterministic incomplete-recovery test觀察 `0 != 50`；該 test隨即單獨通過，之後 release suite乾淨 `131/131`。Independent reviewer另有一次 full run只留下單一 `F` marker且無 traceback/final result；後續兩次 full均 `216/216`。上述不完整或失敗 runs均未計為成功證據，也沒有可重現的 source assertion failure。

## Publication Boundary

本流程在本機 candidate、expanded packages、ZIP、checksums、13-check ledger、Review與architecture diagnosis停止。沒有建立 `v1.3.1` tag、push、GitHub Release、asset upload、Marketplace activation、Plugin installation、publication或announcement。Remote `v1.3.1` URLs尚未宣稱外部可用。
