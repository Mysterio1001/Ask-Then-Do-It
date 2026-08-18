# Ask Then Do It 1.3.1 Maintenance Final Independent Review After P2

Artifact type: Review Report

Artifact ID: `ask-then-do-it-1-3-1-final-review-after-p2`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `4 - 完成本機整合驗證與 1.3.1 release evidence`

Execution mode: `tdd`

Status: Changes Requested

Review label: `independent`

Reviewed inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md) Ticket 4、initial [final Review](ask-then-do-it-1.3.1-final-review.md)、current git diff/status、相關source/tests、Tickets 1-3 accepted Reviews、default `dist`及委託方提供的raw correction results。

Assumptions: 本次operation已由canonical resolver證明為Full；同一output directory只由單一builder串行操作；CPython 3.12/Pillow 12.x是正式baseline；目前`dist`是待封版的本機candidate。

Deferred: P2 correction、fresh closure Review、release-milestone architecture diagnosis、validation ledger、Completed release evidence、evidence-only closure及所有external publication actions。

Independence boundary: Reviewer未參與修正、未讀Ticket 4 implementation evidence或implementer conclusions，也未修改repository。Verdict來自Approved inputs、current code/tests、獨立重跑及temp-only adversarial probe。

Handoff: 下列P2須回Ticket 2 builder ownership，以Approved `tdd` mode修正並重跑affected/full gates，再交另一個fresh independent closure Review。本Review不授權修正、architecture diagnosis、evidence creation或external publication。

## Findings

### P2 - 已完整恢復的prior release仍被誤報為invalid並要求人工復原

Trigger: Forward安裝第二個candidate失敗後，第一個已安裝candidate的removal持續`WinError 5`至50次上限；錯誤隨後解除，使backup restoration可成功覆寫candidate並完整恢復所有prior bytes。`commit()`仍只因`recovery_errors`非空而拋出`IncompleteRecoveryError`，未依最終managed-output完整性判定recovery結果。

獨立temp-only probe觀察到`prior_restored=True`、backup已空、removal attempts為`50`，但錯誤訊息仍聲稱active output不是有效prior/candidate且需要manual recovery。`main()`還會保留實際已不需要人工復原的staging。

Impact: 這違反Specification「Recovery成功與否以整個先前managed output set完整性判定」、successful-recovery cleanup及準確診斷契約。操作者會收到錯誤的active-state警告並被要求進行不必要的人工復原。

Remediation direction: Recovery完成全部後應依最終prior-output完整性分類結果，或在成功restore已覆寫先前candidate-removal failure時消除已被後續操作取代的error。加入deterministic test：candidate removal耗盡、隨後backup restore成功，要求一般failed-build結果明示pre-build state restored、清除transaction-only data，且不得拋`IncompleteRecoveryError`。

Locations: `scripts/build_release.py:773-800`、`scripts/build_release.py:865-871`、`tests/release/test_release_transaction.py:394-508`。

沒有其他P0、P1、P2或P3 actionable finding。

## Initial P2 Closure

Initial final-Review P2 **已關閉**。`scripts/build_release.py:88-95`現在明示active output不是有效prior或candidate並需要manual recovery；`tests/release/test_release_transaction.py:499-508`透過`main()`的stderr精確鎖定該警告、primary/recovery errors及preserved paths。

這項修正對真正不完整的recovery是正確的；新finding在於程式目前也會把已由後續restore完整修復的狀態錯誤分類成同一情況。

## Independent Verification

- CPython `3.12.13`重跑transaction與release safety：`16/16 passed`。
- Default-dist/fresh-build byte parity focused contract：`1/1 passed`。
- Default `dist`共有`48` files；未發現`.dist-release-*` transaction roots。
- Codex SHA-256：`557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209`。
- Generic SHA-256：`6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b`。
- 兩個實際archive hashes與`dist/checksums.sha256`一致。
- `git diff --check`通過，只有LF/CRLF提示。
- Temp-only adversarial state probe重現本Review P2，未修改default `dist`或repository files。

Supplied raw results：clean Red只因缺少指定active-output/manual-recovery訊息而失敗；focused Green `1/1`、transaction `10/10`、safety `6/6`、default builder通過；第一次post-change full run因真實`WinError 5`為`214/215`，affected test單獨通過後clean full discovery為`215/215`；evidence/base/1.3為`36/36`。兩個archive hashes重建後未變。

## Architecture And Refactoring Lenses

1. **Duplicated Code or Policy - `no-finding`.** Windows eligibility、attempt bound及delay集中於單一retry helper；identity policy由exact contracts約束。
2. **Long Function - `no-finding`.** `commit()`雖涵蓋forward與recovery，但state transitions仍可線性追蹤；本P2來自分類條件而非長度。
3. **Large Module or Class - `no-finding`.** 變更維持release builder既有validation/build/commit責任。
4. **Long Parameter List - `no-finding`.** `commit()`及`IncompleteRecoveryError`參數直接對應必要transaction state。
5. **Data Clumps - `no-finding`.** Primary error、recovery errors及paths已集中於專屬error type。
6. **Primitive Obsession - `finding`.** 程式以非空`recovery_errors` list代理最終recovery state，未表達「操作曾失敗但最終prior set已完整恢復」的domain state，直接形成上述P2。
7. **Feature Envy - `not-applicable`.** 受審區是procedural filesystem transaction，沒有相鄰domain object ownership。
8. **Divergent Change - `no-finding`.** Builder變更均由managed-output transaction可靠性驅動。
9. **Shotgun Surgery - `no-finding`.** Retry與recovery政策集中於builder helpers及transaction tests。
10. **Message Chains - `not-applicable`.** 沒有多層collaborator或object navigation。
11. **Leaky Abstraction - `finding`.** `IncompleteRecoveryError`把中途operation failure直接暴露為最終active-output結論；caller與operator無法依其名稱及訊息可靠得知實際state。
12. **Shallow Module - `no-finding`.** Retry helper及structured recovery error仍封裝實質policy；缺口是最終state判定，不是介面缺乏價值。

此P2是局部builder correctness問題，不需要先進行系統性architecture diagnosis。

## Evidence Unavailable

- Reviewer未重跑完整`215` tests、evidence/base/1.3全部`36`項、official Skill/Plugin validators、Marketplace及完整conformance commands；這些採用supplied raw evidence。
- 未由外部程序穩定重現長時間Windows kernel lock；deterministic fault injection仍是Specification要求的主要證據。
- 未在真正非Windows host、external CI或live installed Plugin環境執行。
- Ticket 4 implementation evidence及implementer conclusions依independence boundary刻意未讀。
- Remote `v1.3.1` URLs、architecture diagnosis及Completed release evidence尚不存在或尚未授權。

## Residual Risks And Untested Areas

- 真實Windows lock超過4.9秒仍會依設計耗盡retry；永久ACL型`WinError 5`也會等待相同bounded window。
- Same-output concurrent builders不受支援。
- 自訂release config仍可縮減除`workflow-token-proxy`外的inventory；current config由exact 13-check contract鎖定。
- `.ticket4-isolated-venv/`仍是untracked disposable environment，不得納入release artifacts。
- 多表面version projection仍應由後續read-only architecture diagnosis評估。
- 任一builder source correction都會使目前source freeze與Review失效，必須重跑affected及clean full gates。

## Completion Assessment

Initial final-Review P2已關閉，candidate bytes、checksums、identity及既有verification結果保持一致；但新P2違反Approved Specification對recovery final-state判定、診斷及cleanup的明確要求。

Approved Ticket 4與`1.3.1` maintenance milestone目前**不應判定complete**。修正、fresh independent closure及受影響驗證完成前，不得進入release architecture diagnosis、Completed evidence或任何external publication action。
