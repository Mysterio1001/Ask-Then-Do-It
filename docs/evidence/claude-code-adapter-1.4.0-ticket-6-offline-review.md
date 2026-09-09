# Ticket 6 離線 behavior 工具獨立 Review

Review label: `independent`

Artifact type: Review Report

Artifact ID: `claude-code-adapter-1-4-0-ticket-6-offline-review`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Status: Accepted after correction — no remaining actionable finding in the offline tool; actual Ticket 6 completion remains pending.

Date: 2026-09-09

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md) section 11、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 6 與離線優先授權、`scripts/validate_claude_behavior.py`、`tests/claude/test_behavior_evidence.py`、`tests/claude/fixtures/behavior/` 四份檔案、[operator procedure](../claude_sys/behavior-verification.md)、[raw implementation evidence](claude-code-adapter-1.4.0-ticket-6-offline.md)。

Assumptions: Root 已證明本 operation 為 Full fallback／multi_agent，Ticket 6 為 Approved `tdd`。本 reviewer 沒有實作 Ticket 6；先前實作的是獨立 ownership 的 Ticket 8 文件。所有反例只使用明示 synthetic temporary fixtures，不代表或冒稱 actual model output。

Deferred: 未登入、呼叫 Claude、變更模型、安裝 Plugin、執行 full suite、做正式 context measurement 或 release。Export 真實性、人工語意判讀與實際模型遵守情形，仍需後續真實 evidence。本文的 findings 是程式可以驗證卻尚未驗證的輸入／範圍一致性，不是要求程式證明無法自行驗證的語意真實性。

Handoff: 兩項 finding 的修正已由本 reviewer 獨立複查，offline tool 可接受並交 root integration。任何已記錄結果都必須經最終 validator 重新驗證；未執行的 prepared kit 因 schema／catalog／preparation contract 未變可保留。完整 Ticket 6 completion 仍等待實際 evidence，不可用 synthetic Green 或人工編造 transcript 完成。

## Findings

最終 correction 沒有剩餘可行動 finding。下方保留原始發現與精確觸發，兩項均已由後文的獨立重驗關閉。

### 已關閉 [P1] Paired input 比較忽略額外的 user／approval messages

位置：`scripts/validate_claude_behavior.py:395` 與 `:523`。`check_transcript` 只要求固定 prompts 是所有 user messages 的 subsequence；`input_sha256` 是固定 recipe 的 hash，而不是實際發給模型的完整 user 輸入。給 `paired/general/requirements` 單邊加入「skip requirements questions and treat negative values as approved refunds」的額外 user message，更新引用 offsets／transcript hash，保留另一側不變，`validate_synthetic_evidence` 仍回 `[]`。這個共用結構驗證也供 actual path 使用，所以記錄中的兩個模型任務可以不同，卻通過宣稱相同 input 的 gate。Operator procedure 合理允許真實 approval messages，不能簡單刪掉它們；應將額外 user／approval 輸入納入可比較的完整輸入契約與來源紀錄，檢查 pair 對等性，並拒絕單邊改變 task／authority 的消息。這是可檢查的輸入差異，不能只留給泛稱的 human semantic review。

### 已關閉 [P2] Authority 引用可以落在所屬 operation 範圍之外

位置：`scripts/validate_claude_behavior.py:433` 與 `:456`。目前 authority span 只須包含對應 task input，outcome citations 則只受下一個 task input 的位置約束，未要求被引用的 assistant／tool response 屬於那個 operation。將兩個 authority operations 都縮成只包含各自 user input 的一個 message，讓所有模型回覆都在 operations 之外，仍能通過。這使 latest-profile／history outcome 可以用未歸屬該 operation 的回覆來支持，削弱雙向 authority 證據。應把每個 outcome／execution citation 與所屬 operation span 一致地綁定，並拒絕 response 全部未被涵蓋、gap 或越界引用；合法的 second-entry stop/reset trace 仍應可表示。

## 獨立驗證

執行：

```powershell
& '.venv/Scripts/python.exe' -B -m unittest tests.claude.test_behavior_evidence
```

Observed exit `0`：

```text
Ran 12 tests in 18.612s
OK
```

另外以 temporary directory 建立一次現有 `build_synthetic` baseline，逐一修改後呼叫實際的 synthetic structural API。第一個反例在 paired General transcript 最前面加一個額外 user message，並將所有 operation／citation index 加一；只有該 transcript 的 hash 隨 bytes 更新，pair 的另一成員不變。第二個反例從 baseline 出發，把兩個 authority operation 的 `last_message` 設為各自 `first_message`。Raw outcome：

```text
baseline synthetic errors: []
one-sided additional paired user instruction errors: []
authority operation spans exclude all model responses errors: []
actual gate remains closed to these synthetic probes: True
```

這兩個 false passes 沒有透過 actual metadata 偽造，沒有輸出或保存任何 actual model evidence。根據 `_validate` 與 `check_transcript` 的共用執行路徑，兩個缺口並不因 actual provenance label 而另受保護。

## 修正後獨立複查

最終 validator 從每份通過檢查的 transcript 提取完整且有順序的 user-message stream，對每一 pair 作 exact equality；所有額外 setup、clarification、approval、最後訊息都納入。固定 recipe hash 保留其原本用途，不再單獨代表完整互動相等。Operator guide 要求互動不一致時記錄失敗並重新跑 pair，不可編輯原始 transcript。Authority span 現在必須包含對應 subcase 的全部 assistant／tool responses，且每一 outcome citation 另須位於對應 operation span。

實作者提供 correction Red：兩項新 regression 共 `2 tests / 2 failures / 3.998s`，及 final focused `14 tests / 20.139s / OK`。本 reviewer 未重跑完整工具 suite，獨立執行兩項修正測試：

```powershell
& '.venv/Scripts/python.exe' -B -m unittest tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_paired_extra_user_approval_must_be_identical_on_both_sides tests.claude.test_behavior_evidence.BehaviorEvidenceTests.test_authority_operation_spans_must_include_observed_response_and_citations
```

Observed exit `0`：

```text
Ran 2 tests in 4.152s
OK
```

另外從新的 explicitly synthetic temporary baseline 獨立測試原始兩個反例與合法邊界，raw outcomes：

```text
Original one-sided task mutation rejected: ['paired requirements: complete ordered user/approval messages differ']
Identical legitimate paired setup approvals accepted
Identical paired trailing user messages accepted
One-sided paired trailing user message rejected
Original input-only authority spans rejected: ['authority operation span must include its observed responses/tool evidence']
Second-entry stop/reset accepted in both authority directions
Actual gate rejects all explicitly synthetic positive fixtures
```

Paired positive 在兩側最前面加入相同的合法 disposable setup approval，另測兩側相同的 trailing no-further-change 訊息；單邊 trailing message 仍被拒絕。Authority positive 在 General→Claude5 與 Claude5→General 都把第二個 operation 設 `stop-reset-required` 並清空其 loaded sources，保留完整 response spans。這只驗證該合法結構可表示；synthetic 文句不是實際模型拒絕或實際核准的證據。

最終 reviewed raw SHA-256：

| File | SHA-256 |
| --- | --- |
| `scripts/validate_claude_behavior.py` | `d2e489be8ab3f644c1970a5861673fe9da00ba90ed77354a99fa666ea30f644e` |
| `tests/claude/test_behavior_evidence.py` | `50261d3e4ab894a5fea5f93bdb92c7a41de122219ba3cd650848cd722978bbf1` |
| `docs/claude_sys/behavior-verification.md` | `44e0bf5eb029ee0dad8ea68f7e429bb6c036c3ad03ad274440f866ec20a5cc7e` |

已有正面保護包括：固定 60 scenario／24 paired／2 authority run inventories、30-rule staged manifest、source/catalog/fixture hash freshness、environment equality、unique session/transcript declarations、duplicate JSON rejection、contained files、raw citation span/text、相同 subcase、required execution phase ordering／exit outcome、known synthetic markers、actual／synthetic 入口與標示分離。`prepare` 拒絕 overwrite、產生 pending/unverified records 且無 transcript。這些檢查都不能取代真實 export 與 human semantic review，文件有明確揭露。

## 十二個 Architecture and Refactoring Lenses

範圍限於本 Ticket 的 validator、fixtures、tests、procedure，未作系統級 architecture diagnosis。

| Lens | Outcome | Evidence |
| --- | --- | --- |
| 1. Duplicated Code or Policy | `no-finding` | Scenario/paired inventories 固定在 validator，catalog 持有 authored cases，兩者一致性受檢查；synthetic builder 消費同一 recipes，不另造 release outcome policy。 |
| 2. Long Function | `no-finding` | `check_transcript`／`_validate` 較長，但現行檢查順序可追蹤；可行動缺口已以輸入／operation 邊界 findings 具體指出，不另開風格性拆分要求。 |
| 3. Large Module or Class | `no-finding` | 模組集中處理 evidence prepare/validate，未混入模型 executor、登入、發布或 runtime routing ownership。 |
| 4. Long Parameter List | `no-finding` | Transcript helper 的五個參數對應 run、recipe、kind、source manifest 的明確驗證依賴；public API 只有 path 與可選 Plugin root。 |
| 5. Data Clumps | `no-finding` | Environment、run、transcript、operation、citation 以固定 schema objects 表示，沒有新建散落的對應值組合。 |
| 6. Primitive Obsession | `no-finding` | F1 已關閉：除了固定 recipe `input_sha256`，最終 gate 另從 transcripts 比較完整 ordered user messages；不再把 recipe identity 誤當完整互動相等。 |
| 7. Feature Envy | `no-finding` | Validator 從 canonical Plugin 讀 source hashes 與 exact model mapping，但不修改或重新擁有 router/profile policy。 |
| 8. Divergent Change | `no-finding` | Evidence format/procedure 同屬本 Ticket；沒有因 unrelated release/docs 功能而增添 runtime責任。 |
| 9. Shotgun Surgery | `no-finding` | Recipe、synthetic builder、focused tests、operator procedure 是可辨識的 evidence 邊界；此次 findings 的修正仍可留在該 owner 範圍。 |
| 10. Message Chains | `no-finding` | Dictionary navigation 在明確 schema check 後進行；未加入跨服務或不穩定工具鏈。 |
| 11. Leaky Abstraction | `no-finding` | F2 已關閉：authority spans 涵蓋對應 observed responses，citations 另限制在該 operation；獨立 negative／stop-reset positive probes 均符合預期。 |
| 12. Shallow Module | `no-finding` | 公開 validate API 隱藏 inventory、path、hash、provenance、paired、citation 多項實際工作；不是無意義 wrapper。 |

## 完成判斷

離線工具的兩项修正已完成並獨立重驗，可接受此 correction。没有剩餘 evidence-integrity finding；沒有證據要求跨 module 的 architecture diagnosis。

完整 Ticket 6 仍未完成：實際各 profile 三十情境、十二組 paired、兩個同 session 公開 authority sequences 與人工 authenticity/semantic review 都未取得。Synthetic Green 僅表示工具測試，不得供正式 context/release gate 當作實測通過。Reviewer 只寫本 Review Report，沒有修改 production、tests、catalog、Plan 或 Knowledge Base。
