# Claude context 計算工具：離線準備

Artifact type: TDD Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-7-offline`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0` (workflow envelope; authoring baseline `1.3.1`)

Status: 離線工具與複查修正已接受。Ticket 7 的真實 context gate 尚未執行。

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md) section 12、[Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 7 與 2026-09-09 使用者核准的離線優先順序；Approved `tdd` mode。

Assumptions: 本次無 explicit mode；project/user Config 均 absent，因此 Full fallback；工具及獨立 agents 提供 `multi_agent`。計算器不呼叫模型；測試文字是 synthetic。Observed branch 單元測試只在 temporary fake Plugin 及 mocked prior behavior acceptance 下檢查 source/trace 拒絕邊界，不是 host/model evidence。

Deferred: 真實 behavior gate、實際十情境及十一 checkpoints 的 captured load logs、正式 50% 結果、Ticket 7 completion、local release completion。

Handoff: [獨立 Review](claude-code-adapter-1.4.0-ticket-7-offline-review.md) 已接受 calculator、固定模板、操作說明與 tests；完整 regression 由中央整合。沒有任何實際專案 profile 的正式量測或 50% 達標聲明。

Approval: 使用者核准先完成不用登入的工具，既有全部加入測試決定保持不變。

## 交付與限制

- `scripts/measure_claude_context.py` 提供準備未執行模板與驗證／計算介面。正式模式先呼叫 Ticket 6 `validate_behavior_evidence`，缺失、不完整或 synthetic evidence 不進入計算。
- 十固定情境、Full Review 額外 checkpoint、正確 normalization／整數 threshold、同源重複注入計數、每格獨立結果與 raw hashes 可重算。
- 檢查 source/path/hash、current Plugin bytes、ready automatic envelope、shared inputs、完整 checkpoint inventory、stage 載入順序、reviewer 前綴保留與對稱 exclusions。
- `tests/release/fixtures/claude-context-proxy/` 保存未執行模板與 capture 操作協定。完整 trace 比對可拒絕單邊刪改；不能判定一起偽造的 trace/capture 真偽。獨立查核仍必要。

## 觀察到的 Red / Green

初次先建立 7 個工具測試，再執行：

```text
.venv/Scripts/python.exe -B -m unittest tests.claude.test_context_proxy -v
Ran 7 tests in 0.006s
FAILED (failures=7)
```

Exit `1`，明確 assertion：`Claude context calculator is not implemented`。工具建立後同 command：`Ran 7 tests in 1.591s; OK`，exit `0`。

補上 reviewer-ready 不可漏計 stage-ready 重複注入的回歸，先觀察 `Ran 1 test in 0.218s; FAILED (failures=1)`，原因是錯誤漏計沒有被拒絕。修正前綴保留後 `Ran 9 tests in 1.398s; OK`。

增加獨立 capture/current-source 分支測試後，故意把 model-visible route 同時改成 malformed text 並更新對應 hash/trace，先觀察 `Ran 1 test in 0.480s; FAILED (failures=1)`。加入 ready automatic route validation 後，最終 focused command：

```text
Ran 10 tests in 1.827s
OK
```

Exit `0`。實際來源 padding／更換、trace/inventory 不一致、排除項目不對稱、hash mismatch、path traversal、stage ordering、單格 fail 與重複注入等檢查皆包含在 focused suite。CLI template command 成功建立固定 `unobserved` 模板；覆寫既存模板會被拒絕。

## 獨立複查修正

Reviewer 發現合法的 documented-requirements 路徑可能另載入同 profile 的 `requirements.md`，舊計算器只接受指定單一 stage，無法完整計數。先新增額外 stage 計數及 cross-profile 拒絕測試，觀察 `Ran 1 test in 0.234s; FAILED (failures=1)`；錯誤是合法 stage 被拒絕。修正為 closed same-profile stage inventory，保留 mandatory minimum、source bytes 與 load order 檢查後：`Ran 11 tests in 2.402s; OK`。

Reviewer 獨立重跑 `Ran 11 tests in 1.908s; OK`，另以自己的 fixture 驗證額外 stage 確實增加 totals、另一 profile 仍遭拒絕；本次離線修正已接受。所有真實 behavior／context／release gates 保留。
