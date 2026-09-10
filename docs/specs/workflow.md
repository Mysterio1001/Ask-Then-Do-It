# Ask Then Do It 工作流程規格

本文件彙整現行 Core 1.4.0 的 Full／Lite 與 Ticket 測試選擇契約，供維護者查閱。2026-09-10 的文件整理核准只改變文件組織，沒有重新授權或改變產品行為。原始需求、規格及核准紀錄的定位見[來源索引](../evidence/release-history.md#document-sources)。

執行來源仍為 [Core](../../core/CORE.md)、[規則目錄](../../core/rules/rules.yaml)及各 adapter。使用者操作見[初學者流程](../guides/getting-started-simple.zh-TW.md)；Claude 特有行為見 [Claude 規格](claude-code-adapter.md)。

## 目標與能力邊界

工作流程先釐清需求再實作，保留人的決策權、可觀察驗證與誠實的完成回報。不同 host 可提供不同能力，但相同使用者決策必須得到等價的流程結果。

| 能力 | 可以宣稱的證據 |
| --- | --- |
| `conversation` | 對話與使用者提供的資料；產出由使用者保存的文件 |
| `tools` | 實際讀寫 repository、保存產物與執行命令的結果 |
| `multi_agent` | 另具隔離 worker／reviewer context，才可宣稱獨立複查或平行工作 |

每次選擇階段前宣告實際能力。缺少能力時，標示不可取得的證據並交接；不能把建議操作當成已執行，或把同 context Review 稱為獨立。保留使用者變更，外部寫入與發布仍受 host 權限及使用者授權約束。

## 模式解析

頂層只有 `full` 與 `lite`。它們與 Full Ticket 的 `tdd`／`direct` 是不同層次，Lite 不得虛構 Full 文件或 Ticket mode。

每個公開入口、每次操作及新工作階段都重新解析，不沿用前次 mode：

1. 本次明確指示優先；合法指示可覆蓋無效 Config，且不用先讀較低優先設定。
2. 明確指示同時衝突時先釐清，不按出現順序挑選。
3. 合法專案 Config 優先於使用者 Config；專案 Config 不存在才往下找。
4. 專案 Config 存在但無法讀取、TOML 無效、缺少 mode 或 mode 不支援時回到 Full，不讀使用者 Config。
5. 使用者 Config 合法則使用；不存在或無效則 Full fallback。

Codex 設定路徑是 `<project>/.codex/ask-then-do-it.toml` 與 `~/.codex/ask-then-do-it.toml`；Claude 使用各自 `.claude/` 路徑。只接受頂層 `mode = "full"` 或 `mode = "lite"`，不以其他大小寫、巢狀設定或別名替代。專案設定只限 active project root。解析唯讀，不修復設定、不保存本次覆寫；當 fallback 影響預期路由時揭露原因。

Generic 使用組合入口開頭的 `Default workflow mode: full`／`lite`；本次指示優先，缺少或不支援的宣告回 Full，不冒稱讀取 Codex／Claude Config。

直接叫用 requirements、review、architecture 等 stage 只選擇階段，不代表 Full。先經 canonical resolver；無法載入 resolver 的獨立入口只可使用語意相同的 bounded guard。解析為 Lite 就停止 Full stage 並進入 Lite；解析為 Full 才檢查該階段的既有前置條件。

## Full：需求到完成

沿用與本次工作相關、內容一致且有核准證據的既有產物，從第一個未滿足條件接續，不要求重走已完成階段。缺失、矛盾或不可驗證的上游決策回到受影響關卡。

| 階段 | 必要行為與產物 |
| --- | --- |
| 探查 | 讀取適用指示、現有程式／測試／設定、Git 狀態及已核准文件；可查到的事實不再問使用者 |
| 需求 | 一次只問一個決策問題，提出推薦與取捨；形成完整 Requirement Decision Record 並取得明確共識 |
| 文件化需求 | 已有知識庫、既有系統變更或將產生長期知識時自動使用並先說明原因；使用者明確選擇優先 |
| 規格 | 描述可觀察行為、失敗、邊界、驗收與未決事項，不用實作細節代替需求；取得 Specification 核准 |
| Ticket 計畫 | 垂直切分、明確範圍／依賴／驗收，一次收集所有 Ticket 的測試選擇，再核准計畫 |
| 實作 | 依已核准的 Ticket mode 與依賴執行，維持範圍；矛盾回上游，不悄悄改規格 |
| Review | 核對原始需求、規格、Ticket mode、diff 與實際驗證；報告阻塞與未驗證範圍 |
| 完成 | 只有適用條件與阻塞項已處理才能宣稱完成；明示缺少的證據與剩餘風險 |

需求共識、Specification、Ticket Plan 是分別的人工作業核准點；沉默、其他產物的核准或只改 status 都不能代替核准證據。平行實作只限邊界已定、相互獨立的 Ticket；整合後仍驗證共同結果。

## Full Ticket 的測試選擇

先展示每張 Ticket、測試建議及理由，說明加測試可能增加時間，再用使用者語言一次詢問「加測試／不加測試」。不能要求新使用者猜 `tdd`／`direct` 的意義。建議依功能、風險、複雜度、外部契約及既有覆蓋評估；接受全部加、全部不加或明確混合選擇，未回答的 Ticket 不可核准或進入實作。

| 選擇 | 內部 mode | 執行與證據 |
| --- | --- | --- |
| 加測試 | `tdd` | 先有可解釋的失敗 Red，再最小實作、Green、必要 Refactor；無合理自動化失敗測試時依下述 test-first 例外處理；保存實際命令、結果、範圍與風險 |
| 不加測試 | `direct` | 不新增、修改或執行行為測試；可做語法、lint、型別、schema、build 等非測試驗證；記錄 `tests: skipped-by-user`、未測路徑及殘餘風險 |

TDD 的 test-first 例外只適用於文件、格式、產生的輸出或其他沒有合理自動化測試介面的變更。修改前須說明為何自動化失敗測試沒有意義，並指定替代驗證；實際執行後，在 Implementation Evidence 保存例外理由、驗證方法、原始命令與結果及殘餘風險。不為湊 Red 製造無意義的失敗，也不把例外當成任意省略有意義行為測試的理由。依據：[Core TDD 契約](../../core/modules/tdd-implementation.md)。

行為測試含 unit、integration、end-to-end 及等價可執行行為檢查。Workflow 不因安全、資料搬移、CI 或 release 建議而把使用者拒絕的測試改成必選；外部系統真正強制的檢查仍是交付限制，須揭露並解決，不冒稱可繞過。

Review 保留 Ticket mode，不補跑被拒絕的測試，也不把 direct 稱為 tested／TDD-complete。Direct 可在非阻塞 Review 後完成其範圍。核准後改測試選擇，計畫回 Draft，受影響實作等待重新核准；沒有 mode 的舊計畫亦須補齊，不能猜預設。

## Full 知識與產物

唯一正式知識庫位置是 `docs/project/knowledge-base.md`，保留 Glossary、Architecture map、Important decisions、External dependencies、Unresolved items、Artifact links。正式事實只能來自已核准／接受的證據。

需求探查先把資訊標成 proposed／confirmed／unresolved 的 Draft Working Notes；confirmed 不等於正式知識。需同步時，展示完整 Requirement Decision Record 與 Knowledge Base Change Summary，清楚列 additions、modifications、removals，共同核准後只套用已展示變更。後續已核准產物改變長期事實時也須提出對應摘要。

所有邏輯產物依 [common envelope](../../core/artifacts/common.md)記錄 type、穩定 ID、workflow ID、Core version、status、inputs、assumptions、deferred、handoff 與適用的 approval。形式可為 Markdown、結構化資料或 host-native 紀錄，但 Draft／Approved 語意與追溯不可遺失。文件位置整理不改變這些產品契約。

## Review 與架構診斷

Full Review 使用原始證據；有可用隔離 reviewer 時作獨立複查，只有 tools 時標 `non-independent`，只有對話資料時標 `limited-evidence`。不得把能力不足寫成已完成 repository review。

固定十二個面向為 Duplicated Code or Policy、Long Function、Large Module or Class、Long Parameter List、Data Clumps、Primitive Obsession、Feature Envy、Divergent Change、Shotgun Surgery、Message Chains、Leaky Abstraction、Shallow Module。每項記錄 finding／no-finding／not-applicable（理由）／unverified（缺少證據），findings 按 P0–P3 列觸發方式、影響、位置與方向。

架構診斷適用於明確請求、系統性問題、相關 Ticket 群完成或 release milestone，不在每張 Ticket 後機械執行。預設只模擬刪除，追 callers、tests、configuration、data 與操作後果。實際刪除實驗須明確授權精確範圍／風險、可執行工具及可棄置隔離環境。報告先為 draft；accepted 只允許回 Specification，不能直接授權重構，仍經計畫及所選實作路徑。

## Lite：單次精簡變更

Lite 只探查相關範圍，保留現有變更。先評估認證／授權、付款、資料搬移、破壞性操作、公開契約、跨模組結構、並行／非同步及外部副作用；重大風險出現於核准前或實作中都暫停後續修改，說明證據並讓使用者決定本次轉 Full 或接受風險續用 Lite。選擇不寫回 Config。轉 Full 保留已做變更，回第一個未滿足關卡。

1. **問題**：每輪最多三個真正會阻擋／改變實作方向的問題，依影響及不確定性排序；每題最多三句、一個決策、一個推薦與主要取捨，整輪約 500 tokens，沒有問題就不湊數。
2. **Change Brief**：約 800 tokens，含目標、範圍、非目標、三至五個可觀察驗收情境、風險與驗證方式。完整展示後只有一個正式實作前核准點；不為省字隱藏風險，無法清楚表達時建議 Full。
3. **實作**：限核准範圍；不新增或修改行為測試、不作 TDD 宣稱、不作額外清理或範圍擴張。
4. **最低驗證**：檢查 diff、適用的既有靜態驗證、主要成功與重要失敗／邊界路徑（既有 focused test 或 manual smoke）。不用全套測試作預設；真實外部交付要求另行揭露並遵守。修好範圍內失敗後重跑；缺少檢查如實回報，已知失敗不得無條件完成。
5. **精簡 Review**：同 context 核對範圍、失敗、安全與證據；不要求獨立 reviewer、十二面向或 Review 文件。可行動 findings 整批提出，核准後只修核准部分；拒絕項目保留並揭露影響，沒有 findings 就不製造空核准點。
6. **完成**：約 500 tokens 說明交付、變更範圍、已驗證／未驗證、未解 findings 及風險；重大問題可超出預算。新 session 重新解析 mode，不假裝恢復未保存的 Brief／核准／Review。

Lite 不建立／更新 RDR、Working Notes、知識庫、Specification、Ticket Plan、Implementation／Review／Architecture evidence 等 workflow artifacts；使用者要求的產品文件仍可作交付。沒有 tools 就不能宣稱已寫檔或執行測試。

## 驗收與維護

- 明確指示覆蓋合法／無效 Config；衝突暫停；專案 absent 與 present-invalid 的回退結果不同。
- 直接 stage entry 不繞過 mode 或前置核准；Full test choice 缺失／更改都停在 plan gate。
- TDD 有可觀察的先失敗後成功，或符合前述 test-first 例外，已在修改前聲明理由及替代驗證並保存實際執行結果；direct 沒有行為測試且留下 skipped disclosure；Lite 的最低驗證不被當成 TDD。
- 各 host 遵循同一觀察結果，能力不足如實降級；不以 Generic 對話聲稱檔案已保存。
- Codex tools 的固定 benchmark 在相同任務／決策／風險／結果下，Lite 的 workflow-controlled token proxy 至少比 Full 少 60%。兩側用相同 normalization 與 exclusions；fixtures、fingerprint 與原始總量可重算，不代表帳單、總 context 或 latency 保證。Generic 的完整 composed prompt 是 Full／Lite 共同固定成本，單獨列報且 `gate_applied: false`，不套用或宣稱 Generic 60% 縮減保證。
- 三語使用指南保持語意一致，初學者指南承接共同流程，平台指南承接設定與安裝，短 START-HERE 只導向；不新增平行 Lite 指南。

驗證命令與證據限制見[驗證手冊](../maintainer/validation.md)。本規格由 `ask-then-do-it-1.0.0`、`grill-me-clean-slate-1.0.0`、`optional-ticket-testing`、`lite-workflow-mode-1.3.0` 的有效內容及現行 Core 彙整；不再保留版本升級時的施工下一步。

[回到 README](../../README.md)
