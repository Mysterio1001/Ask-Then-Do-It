# Ask Then Do It 1.3.1 Maintenance Ticket 4 Implementation Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `release-1-3-1-maintenance-ticket-4-implementation`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `4 - 完成本機整合驗證與 1.3.1 release evidence`

Execution mode: `tdd`

Status: Completed

Inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md)、Tickets 1-3 implementation evidence 與 accepted Reviews、[initial final Review](ask-then-do-it-1.3.1-final-review.md)、[Review after first P2](ask-then-do-it-1.3.1-final-review-after-p2.md)、[fresh recovery P2 closure Review](ask-then-do-it-1.3.1-final-review-after-recovery-p2.md)、[release architecture diagnosis](ask-then-do-it-1.3.1-release-architecture-diagnosis.md)、current frozen source 與 default `dist`。

Assumptions: 同一 output directory 只有單一串行 builder；正式 baseline 是 CPython 3.12 與 Pillow 12.x；`dist` 只由正式 builder 生成；external publication 仍未授權。

Deferred: 移除 disposable venv、Architecture Draft A1-A5 的接受或實作、Git tag、push、GitHub Release、asset upload、Marketplace activation、installation 與 announcement。

Handoff: Missing-evidence與`Review Pending` Red、Completed Green、evidence-only closure均已完成。外部 publication仍需另一次明確核准。

## Outcome

Frozen `1.3.1` local candidate 已在 disposable isolated CPython `3.12.13` environment 完成 required gates、fresh independent Full Review 與 read-only release architecture diagnosis。兩個 archives、expanded packages、checksums 與 current identities一致；歷史 `1.3.0` artifacts 與 frozen Token fixtures維持不變。

本 Ticket 僅新增 release workflow evidence artifacts。它沒有修改 product source、tests、generated `dist` 或外部 publication state。

## TDD Red

Actual missing-evidence command:

`& '.\.ticket4-isolated-venv\Scripts\python.exe' -E -B scripts\validate_release_evidence.py --config release\release.json --ledger docs\evidence\ask-then-do-it-release-1.3.1.json --evidence docs\evidence\ask-then-do-it-release-1.3.1.md`

Observed Red: exit `1`；validator 回報 `Invalid or missing validation ledger`，證明尚不存在的 actual `1.3.1` evidence不能被接受。建立 exact ledger與 `Review Pending` evidence後，還需觀察第二個 Red，證明內容完整但未封帳的 evidence仍不能通過。

## Final Candidate Verification

- Runtime：CPython `3.12.13`；`sys.flags.ignore_environment=1`；`include-system-site-packages=false`；Pillow `12.3.0` 與 PyYAML `6.0.3` 均從 `.ticket4-isolated-venv/Lib/site-packages` 載入。
- Focused recovery correction：`1/1 passed`。
- Transaction：`11/11 passed`；release safety：`6/6 passed`。
- Main full discovery：`216/216 passed`；independent reviewer另取得兩次 clean `216/216`。
- Final serial suites：release `131/131`、Codex `27/27`、Generic `39/39`、conformance `19/19`。
- Evidence/base/1.3 contracts：`36/36 passed`。
- Package inventory focus：`9/9 passed`；Codex 27 files、9 Skills、2 assets；Generic 18 files、11 prompt modules；consumer packages無 Pillow。
- Reproducibility/ZIP focus：`2/2 passed`；two isolated builds與 default `dist` byte-for-byte一致，Codex `27/27`、Generic `18/18` ZIP entries等價。
- Documentation/Marketplace/historical guards：`42/42 passed`；Marketplace CLI passed；43個 Approved `1.3.0` artifacts與13個 frozen Token fixture hashes不變。
- Skill validator：canonical + packaged `18/18` valid；Plugin validator：`2/2` passed；兩個 adapter conformance CLI passed against Core `1.3.1`。
- Token proxy：Full `14771`、Lite `5480`、reduction `62.90%`、unchanged `60%` gate passed；Generic fixed cost `15376`；fixture/source fingerprint `e91e7986ac191539bfe54e97cef4807f505a145b4ac8ecc694ebee76ab492610`。
- Default builder：exit `0`，產生 48-file `dist`；沒有 `.dist-release-*` transaction root。
- `git diff --check` exit `0`；只有既有 LF/CRLF warnings。

## Archive Hashes

```text
557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209  codex/ask-then-do-it-1.3.1.zip
6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b  generic/ask-then-do-it-generic-1.3.1.zip
```

兩個獨立重算值都與 `dist/checksums.sha256` 及 correction前的 frozen candidate hashes相同。

## Review And Architecture

Fresh independent [recovery P2 closure Review](ask-then-do-it-1.3.1-final-review-after-recovery-p2.md)沒有 P0-P3 finding，判定 final restored-state correction關閉先前 blocker。

Read-only [release architecture diagnosis](ask-then-do-it-1.3.1-release-architecture-diagnosis.md)沒有未解 release-correctness blocker。Draft A1-A5分別涉及 strict JSON policy、13-check authority、execution-bound evidence、builder責任與version projection；全部是非阻斷 proposal，沒有被接受或實作，也不授權本 Ticket refactor。

## Observed Transients And Residual Risk

- 一次 final release-suite run在 incomplete-recovery fault-injection test觀察 `0 != 50`；同一案例隨即單獨 `1/1` passed，之後完整 release suite乾淨 `131/131`。該次不計為 pass，保留為不可重現的 Windows/test-temp observation。
- Independent reviewer的一次 full run只留下單一 `F` marker而無 test name/traceback/final result；後續兩次完整 discovery均 `216/216`。該次不計為 pass。
- 真實 Windows lock超過約4.9秒仍可耗盡 retry；永久 ACL 型 `WinError 5`使用同一 bounded window。
- Same-output concurrent builders、真正 non-Windows host、external CI與live installed Plugin不在本版保證範圍。
- Runtime process enumeration因 Windows CIM access denied而 unavailable；所有已啟動 test sessions均已取得退出結果，且 repository root沒有 transaction staging。

## Publication Boundary

沒有建立 `v1.3.1` tag、push、GitHub Release、asset upload、Marketplace activation、Plugin installation、announcement或其他 external publication mutation。Remote `v1.3.1` URLs只有 local contract值，尚未宣稱可從外部取得。
