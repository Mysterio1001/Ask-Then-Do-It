# Claude Context Offline Tool Independent Review

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-7-offline-review`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0` (Review envelope; Approved baseline `1.3.1`)

Status: Reviewed — offline tool accepted；完整 Ticket 7 的真實 context gate 未完成。

Review label: `independent`

Approved implementation mode: `tdd`

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md) section 12、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 7 與 2026-09-09 離線順序；`scripts/measure_claude_context.py`、`tests/claude/test_context_proxy.py`、`tests/release/fixtures/claude-context-proxy/`；Ticket 6 behavior-validator 的公開 gate 與 source binding；[implementation evidence](claude-code-adapter-1.4.0-ticket-7-offline.md) 的原始測試結果。

Assumptions: 本次 Full fallback／multi_agent 已由協調者證明，Ticket mode 保持 `tdd`。本 reviewer 未實作 context tool／fixtures／tests；只讀 raw source、獨立測試及提出 finding，由作者完成修正。

Deferred: 真實 authenticated behavior evidence、十情境十一 checkpoints 的完整 host captures、capture provenance 獨立查核、正式 50% gate、完整 Ticket 7／local release completion。

Handoff: 接受離線工具準備；保留未執行模板與全部真實 gates。取得 behavior 與完整 capture evidence 後才可計算正式結果；source 變更須重新驗證。

## Findings

最終 frozen source 沒有未解 actionable finding。Offline tool acceptance 不代表任何實際 profile 已達成 50% reduction，完整 Ticket 7 仍未完成。

本 Review 發現的 P2 已關閉：原 `check_record` 只接受 scenario 的單一指定 stage，拒絕 documented-requirements 實際組合載入的同 profile `requirements.md`；這會阻止完整合法 capture 被計數。作者新增 closed same-profile stage inventory，保留 mandatory minimum 與 observed canonical-byte comparison。Reviewer 獨立 probe 現在確認額外 requirements stage 增加計數，另一 profile 的同名 stage 仍被拒絕。

## Verification and evidence boundary

Reviewer 自行執行原 focused suite：`Ran 10 tests in 1.868s; OK`。修正 freeze 後自行重跑：

```text
.venv/Scripts/python.exe -B -m unittest tests.claude.test_context_proxy -v
Ran 11 tests in 1.908s
OK
```

Exit `0`。另外獨立 temporary-fixture probe 確認 `profiles/general/requirements.md` 被計入 general total，而在 general trace 加 `profiles/claude-5/requirements.md` 會失敗。NFC／重複來源計數 probe `['e\u0301  x','same','same']` 得 `normalized_bytes:14, proxy_tokens:4`；`threshold(101,50)` 為 true、`threshold(101,51)` 為 false。

逐項檢查了 behavior-first return：正式模式的 missing/invalid behavior gate 在 inventory arithmetic 前結束，`measurements: []`、`release_pass:false`。Synthetic 模式只能讀 synthetic fixture，永遠不能取得 release pass。完整十 scenarios／十一 checkpoint inventory、共同 task/outcome hashes、capability、raw SHA-256、相對路徑、source bytes、load order、reviewer prefix、重複 injection、對稱 exclusion 與每格 integer threshold 均有明確檢查。

Current source comparison 可阻止額外 padding 與 stale source；独立 trace equality 可阻止只改 measurement inventory 的丟棄／重排。這些都不能驗證共同偽造的 capture＋trace 真偽、未記錄 injection 或人工 `capture_review` 敘述的可信性；source 與 README 已明示這個 evidence trust boundary。工具不呼叫模型、不執行登入或 host command。此 Review 沒有正式量測本 repository profiles，也沒有完整 suite 重跑。

## Twelve lenses

| Lens | Outcome | Evidence |
| --- | --- | --- |
| Duplicated Code or Policy | no-finding | Context arithmetic 由單一 tool 擁有；behavior validity 委派 Ticket 6 公開 validator，未複製其 approval logic。 |
| Long Function | no-finding | `evaluate` 做完整驗證後才 arithmetic；capture/source validation 拆到 `check_record`，失敗不產生部分正式結果。 |
| Large Module or Class | no-finding | Scope 是 capture validation、normalization、per-cell result 與 prepare CLI，沒有 host/model executor。 |
| Long Parameter List | no-finding | `check_record` 的 scenario/profile/checkpoint/context 明確界定一個 capture cell，未攜帶 host mutable state。 |
| Data Clumps | no-finding | Raw references、events、checkpoints 使用固定 shape；task/outcome 在 scenario 共用。 |
| Primitive Obsession | no-finding | Scenario、profile、kind、origin、capability 與 relative resource path 均受 closed contracts 限制。 |
| Feature Envy | no-finding | Tool 只消費 behavior validator 回傳的 errors 與 canonical Plugin bytes，不寫入對方的 ledger 或 modules。 |
| Divergent Change | no-finding | 額外合法 stage 修正只改 measurement allowlist／focused regression；沒有改 profile 來掩蓋 context failure。 |
| Shotgun Surgery | no-finding | Context recipe／模板由單一 template function 建立；current capture contract與tests變更面有界。 |
| Message Chains | no-finding | Portable relative path resolver 檢查 containment與links；未透過多層 host state 導航。 |
| Leaky Abstraction | no-finding | 原單一 stage 假設已修正，正常 composed stage 可完整計數。 |
| Shallow Module | no-finding | Tool 隱藏實際 normalization／inventory／per-cell gate複雜性，並明示不提供capture authenticity。 |

## Final source identity

- `scripts/measure_claude_context.py`: `c0602dc408ea0d43536a7dc7d2739f6369b89559fa0cf37014093e5df1097b10`
- `tests/claude/test_context_proxy.py`: `aea8e27d311b936262a02f95aa5ca58e0bda281dd507ee6948edf2df2816ef1a`
