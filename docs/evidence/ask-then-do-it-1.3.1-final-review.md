# Ask Then Do It 1.3.1 Maintenance Final Independent Review

Artifact type: Review Report

Artifact ID: `ask-then-do-it-1-3-1-final-review`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `4 - 完成本機整合驗證與 1.3.1 release evidence`

Execution mode: `tdd`

Status: Changes Requested

Review label: `independent`

Reviewed inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md) Ticket 4、完整current git diff/status、相關source/tests、Tickets 1-3 accepted Review artifacts、default `dist`，以及委託方提供的raw verification。

Assumptions: 同一output directory只由單一builder串行操作；目前`dist`是待封版的本機`1.3.1` candidate；CPython 3.12/Pillow 12.x是唯一正式驗證baseline。

Deferred: Ticket 4 correction closure、release-milestone architecture diagnosis、validation ledger、Completed release evidence、evidence-only closure，以及tag、push、GitHub Release、asset upload、Marketplace activation與announcement。

Independence boundary: Reviewer未參與實作、未讀Ticket 4 implementation evidence或proposed verdict，也未修改repository。Finding由Approved Specification、current source/tests與獨立重跑直接得出。

Handoff: 將下列P2回Ticket 2 builder ownership；Review本身不授權修正。取得核准後須完成Red/Green、affected/full verification及fresh independent closure Review，再重新進入Ticket 4 final Review gate。

## Findings

### P2 - Recovery雙重失敗時沒有明示active output必須人工處理

當forward replacement已部分發生且recovery也失敗時，`scripts/build_release.py:88-93`只回報`candidate was not committed; recovery is incomplete`、primary/recovery errors與三個paths。雖然這能避免宣告成功，卻沒有依Approved Specification明確警告active output不是有效舊版或新版、需要人工處理。操作者可能把「candidate未提交」誤解為舊版仍完整。現有`tests/release/test_release_transaction.py:499-503`只鎖定errors與staging/backup paths，無法拒絕這項必要診斷再次缺漏。應在`IncompleteRecoveryError`訊息加入明確active-output/manual-recovery警告，並新增精確assertion。

沒有其他P0、P1、P2或P3 actionable finding。

## Verification

Reviewer獨立執行：

- Fresh venv：CPython `3.12.13`、`sys.prefix != sys.base_prefix`、`PYTHONPATH=None`、Pillow `12.3.0`、PyYAML `6.0.3`均來自該venv；`pip check`通過。
- Evidence/base/1.3 contracts：`36/36 passed`，9.915秒。
- Deterministic transaction suite：`10/10 passed`，1.064秒。
- 上述36項包含evidence fail-closed、historical/fixture guards、兩個fresh builds對default `dist`逐檔byte parity、inventory/no-Pillow、ZIP equivalence與SHA驗證。
- Marketplace CLI、Codex conformance CLI、Generic conformance CLI均通過。
- Token proxy：Full `14771`、Lite `5480`、reduction `62.90%`，gate passed；fingerprint `e91e7986ac191539bfe54e97cef4807f505a145b4ac8ecc694ebee76ab492610`。
- 獨立重算兩個archives，分別為`557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209`、`6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b`，與`dist/checksums.sha256`一致。
- `git diff --check` exit `0`；僅有LF/CRLF提示。
- 未發現`.dist-release-*` transaction temp roots。

委託方supplied raw evidence另包含：full discovery最終`215/215`、release suite最終`130/130`、Codex `27/27`、Generic `39/39`、conformance `19/19`、package/build `30/30`、documentation/clean/Marketplace identity `49/49`、Skill `18/18`、Plugin `2/2`及official default build passed。

## Architecture And Refactoring Lenses

1. **Duplicated Code or Policy - `no-finding`.** Windows eligibility、attempt bound與delay集中於單一retry helper；identity重複由exact contract與historical guards約束。
2. **Long Function - `no-finding`.** `commit()`雖呈現forward與recovery，但仍是可線性追蹤的單一transaction。
3. **Large Module or Class - `no-finding`.** 新增責任仍屬release builder既有validation/build/commit ownership。
4. **Long Parameter List - `no-finding`.** `commit()`與`IncompleteRecoveryError`參數均直接對應必要transaction state。
5. **Data Clumps - `no-finding`.** Primary error、recovery errors與paths已集中於`IncompleteRecoveryError`。
6. **Primitive Obsession - `no-finding`.** Retry參數使用具名常數，incomplete recovery也有專屬error type。
7. **Feature Envy - `not-applicable`.** 受審流程是procedural filesystem transaction，沒有相鄰domain object ownership。
8. **Divergent Change - `no-finding`.** Builder變更均由managed-output retry/recovery可靠性驅動。
9. **Shotgun Surgery - `no-finding`.** Retry policy變更集中於helper；版本同步雖跨多個active declarations，但有exact lockstep gates。
10. **Message Chains - `not-applicable`.** 沒有跨多層collaborator或object navigation。
11. **Leaky Abstraction - `finding`.** 同上述P2；operator仍須自行從「recovery incomplete」推論active output無效及需要人工復原。
12. **Shallow Module - `no-finding`.** Retry helper、structured recovery error及evidence validator均隱藏了實質policy與fail-closed複雜度。

P2是局部builder診斷缺口，不需要先做系統性架構重構。

## Evidence Unavailable

- Reviewer未重跑完整`215` tests、完整`130` release suite、official Skill/Plugin validators或default-output builder；這些僅有supplied raw evidence。
- 未以外部程序穩定重現真實長時間Windows sharing/ACL lock；deterministic fault injection是主要證據。
- 未在非Windows host、external CI或live installed Plugin環境執行。
- `v1.3.1`遠端URLs尚未發布，無法驗證外部可用性；這屬明確publication boundary。
- Release architecture diagnosis與Completed evidence尚未建立。

## Residual Risks And Untested Areas

- 真實Windows lock超過4.9秒仍會依設計失敗並進入recovery；supplied runs已觀察到偶發lock後串行rerun通過。
- Same-output concurrent builders不受支援。
- 自訂release config仍可縮減除`workflow-token-proxy`外的inventory；current `1.3.1` config則由exact 13-check test鎖定。
- `.ticket4-isolated-venv/`目前是untracked disposable環境，closure前不得納入release artifacts。
- 多表面version projection仍是後續read-only architecture diagnosis應評估的維護風險。
- 任何builder source correction都會使本次final Review與source freeze失效；即使package bytes不變，也必須重跑規定的affected/full gates。

## Completion Assessment

Approved Ticket 4與`1.3.1` maintenance milestone目前**不應判定complete**。大部分dependency、transaction、package、identity、reproducibility、checksum與compatibility gates已有一致證據，但上述P2違反明確的incomplete-recovery diagnostic MUST。修正、驗證及fresh independent closure完成前，不得建立Completed release evidence或進入external publication。
