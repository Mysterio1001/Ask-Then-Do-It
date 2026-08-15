# Ask Then Do It：模型中立的 AI 開發流程設計

Ask Then Do It 將「先問清楚再實作」分成 `Full` 與 `Lite` 兩種頂層模式。Full 保留完整決策、實作與 Review 證據；Lite 用較少的流程內容處理範圍清楚、風險較低的工作，但仍保留使用者授權、最低驗證與誠實回報。

頂層 Full/Lite 和 Full Ticket 內部的測試選擇不是同一件事。Lite 不是 `direct` 的別名，也不能建立假的 Full 文件來取得實作資格。

## 要解決的問題

單一重量級流程雖然可追溯，卻會在小型工作中反覆產生和載入需求、規格、Ticket 與交接內容。若只拿掉 TDD，其他流程內容仍然存在，也不能真正降低 token 使用。

設計因此同時守住兩個目標：

- Full 的既有核准、文件、測試選擇、Review 與架構改善行為保持不變。
- Lite 減少由工作流控制的內容，同時清楚揭露較低的驗證信心與可追溯性。

## Core 與 host 的責任

Core 擁有供應者中立的 Full/Lite 契約，包括模式名稱、Full fallback、Full 相容性、Lite 生命週期、風險停點、核准權、最低驗證、Review 修正權與 session 行為。

| 層次 | 責任 | 不得宣稱的能力 |
| --- | --- | --- |
| Core | 定義兩種模式共同且與模型無關的語意與安全邊界 | 不指定某個 host 的 Config 路徑或工具能力 |
| Codex Plugin | 由 Codex adapter 將使用者與專案 Config、Skills、檔案和命令工具對應到 Core | 不得改寫 Core 語意或把臨時選擇寫回 Config |
| Generic workflow | 由 Generic adapter 將預設模式宣告與對話式模組對應到 Core | 沒有工具證據時，不得宣稱已修改檔案、執行命令或觀察測試結果 |

Codex adapter 負責讀取 Plugin 所屬的 Config、依優先順序選擇模式，並在實際權限內執行檔案與命令操作。Generic adapter 負責產生一份帶有預設模式宣告的長文字工作流，並維持 conversation-only host 的能力誠實。

文件也有清楚的 ownership：三語初學者指南是完整 Full/Lite 使用流程的權威來源；Codex 與 Generic 使用指南分別擁有 host 設定；簡短入口只負責導向；本設計文件擁有維護者契約與 token-proxy 目標。

## Adapter 等價性

不同 host 不必有相同工具，但必須為相同使用者決定產生等價的可觀察結果。等價性至少涵蓋：

- 明確的目前操作指示優先於持久預設，無有效預設時使用 Full。
- Full 保留原本三個核准點；Lite 只有一個 Change Brief 核准點。
- 高風險切換只影響目前操作，實作途中發現重大風險也必須停下來重新詢問。
- Lite 不建立流程文件、不新增測試，且要揭露實際與無法取得的驗證。
- Lite Review 必須整批呈現 findings，使用者核准後才能修正。
- 新 session 必須重新判定模式，不得假裝接續未保存的 Lite 狀態。

Codex 可以實際編輯與驗證；只有對話能力的 Generic host 只能提出計畫或分析使用者提供的證據。這是能力差異，不是流程結果或授權規則的差異。

## Full 契約

Full 適用於高風險、跨模組、需求仍不確定，或需要完整稽核軌跡的工作。它的既有流程保持不變：

1. 先做 repository reconnaissance，再一次只問一個需求問題，達成需求共識。
2. 核准需求後，才把正式內容同步到 Project Knowledge Base。
3. 建立並核准描述行為和失敗方式的規格。
4. 拆成垂直 Tickets，逐張提出測試建議，再由使用者一次決定每張 Ticket 是否加上測試，最後核准完整 Ticket 計畫。
5. Full 會把測試選擇內部對應為 `tdd` 或 `direct`。TDD 需要 Red、Green、Refactor；direct 不執行行為測試並留下未測範圍。
6. 保留實作證據，交給獨立 Review 以十二項視角檢查。系統性問題先進入架構改善分析，再透過規格與 Tickets 取得新的實作授權。

需求共識、規格與 Ticket 計畫是 Full 的三個正式核准點。新增模式 resolver 可以位於 Full 以前，但不得刪除或縮短這些契約。

## Lite 契約與較低可追溯性

Lite 的可追溯性低於 Full，因為 Change Brief、核准、進度與 Review 只存在於目前對話，不形成可供未來 session 直接恢復的流程文件。這項取捨必須在文件和完成回報中保持清楚。

Lite 的共享生命週期是：聚焦 reconnaissance 與風險判定、每輪最多三個阻塞問題、約 800 tokens 的 Change Brief、一個核准點、直接實作、靜態加成功與失敗路徑驗證、精簡 Review、findings 修正核准，以及通常約 500 tokens 的完成回報。

Lite 不新增或修改行為測試，不執行 TDD，也不要求 Full 的十二項 Review 或獨立 reviewer。它仍必須停止範圍擴張、保留使用者變更、執行可用的最低驗證，並讓已知失敗阻止無條件完成宣告。

## 風險與授權邊界

認證、授權、付款、資料搬移、破壞性資料操作、公開契約、跨模組結構、並行、非同步與外部副作用都需要在 Lite 核准前評估。找到重大風險時，host 要提出證據並詢問是否只把目前操作切換為 Full；使用者可以接受風險後繼續 Lite。

若實作中出現新風險，後續修改必須暫停。切換 Full 時保留可觀察變更，並回到最早未滿足的 Full gate。這個選擇不得改寫 Config 或影響其他 session。

## 可重現的 token proxy

Release gate 使用一個等價的代表情境比較 Full 和 Lite。Fixture 固定相同任務、決策、風險與完成結果，兩種模式使用相同正規化與計數方法，讓失敗能在 repository 內重現。

計數納入受工作流控制的材料。計數內容包括問題、Change Brief 或 Full 文件、階段指示、組合後的 prompt 內容、重複交接與完成回報；兩種模式以相同規則處理，不為 Lite 特別排除不利內容。

計數排除任務特定的原始碼、必要的工具輸出與隱藏的模型推理，因為這些內容不是工作流能固定控制的共同成本。Fixture、計數規則、Full 與 Lite 原始計數及公式都必須在測試或 release evidence 中揭露。

縮減率使用相同公式：`(Full proxy - Lite proxy) / Full proxy * 100`。代表情境中的 Lite 必須比 Full 至少降低 60%，否則 release gate 失敗。

這個 proxy 只驗證 repository 可控制的流程材料，不保證 API 帳單、總 context、隱藏推理成本或快取折扣會按相同比例下降。維護者不得把通過 gate 描述成實際收費保證。

## 維護規則

- Core 新增或改變模式語意時，Codex 與 Generic mapping 必須一起更新並證明等價。
- Full 的一次一題、三個核准、每 Ticket 測試選擇、TDD/direct 證據與 Review 不得因 Lite 而弱化。
- Lite 的問題、Change Brief 與完成預算是約略的使用者可見輸出目標；不能為了預算隱藏失敗、風險或缺少的證據。
- 初學者指南保存完整使用者流程；host 指南保存設定細節；短入口不複製完整流程，也不新增獨立 Lite 指南。
- Generic workflow 只能宣稱 host 真正提供的能力，能力不足時要產生清楚的 handoff 或未驗證說明。
- 60% proxy 必須使用等價情境和固定規則，變更 fixture 或算法時要同時檢查兩種模式。

## 閱讀下一步

- [初學者 Full/Lite 流程](../guides/getting-started-simple.zh-TW.md)
- [Codex Plugin 使用說明](../guides/codex.zh-TW.md)
- [Generic 使用說明](../guides/generic.zh-TW.md)


[回到 README](../../README.md)
