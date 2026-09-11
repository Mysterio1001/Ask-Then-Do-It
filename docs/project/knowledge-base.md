# Ask Then Do It Project Knowledge Base

Artifact type: Project Knowledge Base

Artifact ID: `ask-then-do-it-project-knowledge-base`

Workflow ID: `repository-cleanup-2026-09-10`

Core version: `1.4.0`

Status: Consolidated — 既有核准知識的整理；不新增產品行為核准。

Inputs: 現行 Core／adapter sources、既有核准需求／規格／計畫、最新關鍵 Reviews 與發布收據；原始版本見[來源索引](../evidence/release-history.md#document-sources)。

Assumptions: 當前來源 1.4.0，離線工具與真實模型驗證分開判斷。

Deferred: 未完成的 live gates 與未接受的架構提案列在[狀態文件](status.md)。

Handoff: 維護時先讀本索引，再讀相關規格／手冊；不要依舊 Ticket 的下一步重走已完成工作。

Approval: 使用者在 2026-09-10 看過逐檔合併／刪除去向及保留範圍後回覆「核准 開始執行」，授權本次內容整理與知識遷移；不變更產品 Full／Lite 契約。

## Glossary

| 名詞 | 定義／所有權 |
| --- | --- |
| Core | Provider-neutral 流程、30 條 mandatory rules、artifact 與能力契約 |
| Full／Lite | 頂層 assurance／精簡模式；不同於 Ticket 的 tdd／direct |
| tdd／direct | Full Ticket 加測試／不加測試的內部映射；只按已核准選擇執行 |
| Repository marketplace | Codex／Claude 各自的 catalog，pin provider canonical source，留在 repository 不進 ZIP |
| Operation-bound profile | 每次 Claude 公開入口綁定；操作中切換模型不換 profile，PostModelSwitch commit 後的下一 permitted entry 才保證重新選擇 |
| Valid unknown／router failure | 前者為可信 ready state 中未提供／未列出的 exact model ID；後者為 Node、hook、schema、ownership 或 transition 故障，不得混用 |
| Route envelope | UserPromptExpansion 同次輸出的 bounded 結果；不帶 prompt、arguments、raw session ID 或 paths |
| Compatibility target／live-verified | 設計支援的平台與實際通過 exact environment smoke 的證據是不同層級 |
| Loaded-context proxy | 實際載入的 Plugin-controlled text 的固定量測，不代表總 context 或帳單 |
| ZIP recovery | 平台版本化備援；Claude `--plugin-dir` 僅當次 session，不是持久 Marketplace 安裝 |

## Architecture map

| 邊界 | 現行責任 |
| --- | --- |
| [core/](../../core/CORE.md) | 流程與產物契約；不指定 host Config 或執行能力 |
| [Codex adapter](../../adapters/codex/conformance.yaml) | 九個公開 Skills、manifest、rule mapping、Plugin-owned .codex mode Config |
| [Generic adapter](../../adapters/generic-prompts/manifest.yaml) | 固定 module 順序與可貼上的組合入口；預設模式在入口宣告，能力不足如實降級 |
| [Claude adapter](../../adapters/claude-code/conformance.yaml) | 兩個公開 Skills、兩 profiles 各十模組、唯讀 reviewer、四種 hooks、dependency-free Node router |
| [release config](../../release/release.json)／[builder](../../scripts/build_release.py) | 三套件、exact inventory、reproducible ZIP、checksum、managed replacement／rollback |
| [tests/](../../tests/release/built_fixture.py) | 來源、契約、安全、套件與證據驗證；fresh isolated build 不依賴舊 dist |

Codex catalog 位於 `.agents/plugins/marketplace.json`，Claude 位於 `.claude-plugin/marketplace.json`；兩者 schema、source、validator 與 lifecycle 分開。Claude immutable resources 在 `${CLAUDE_PLUGIN_ROOT}`，state 僅在 `${CLAUDE_PLUGIN_DATA}/routing/v1/sessions/<session-key>.json`；mode Config 在 user/project `.claude/ask-then-do-it.toml`，不混入 settings.json 或 Codex Config。

## Important decisions

- **完整與精簡模式分開**：Lite 降低 workflow-controlled tokens 與持久追溯成本；不移除 Full 的需求／規格／計畫核准及測試選擇權。新 session 不冒稱恢復未保存 Lite state。依據：[流程規格](../specs/workflow.md)與現行 Core。
- **短入口與自足套件**：START-HERE 只導引；runtime 指令留在各 adapter，不依賴 repository 開發文件。三語表達可編輯但需語意等價。原始 1.3.0 設計與後續版本對齊決策支持此分工。
- **平台 catalog 分離**：Claude 與 Codex 即使 qualified identity 相同，也不能共用 schema 或互指 source。Exact Claude strict validator 要求 marketplace description；2026-09-06 的修正已接受，不能靠忽略 warning 宣告通過。依據：[Ticket 1 Review](../evidence/claude-code-adapter-1.4.0-ticket-1-marketplace-description-correction-review.md)。
- **可信路由先於精簡 context**：只以官方事件的 canonical model IDs 作 exact mapping，不看使用者自述或 substring；unknown 與 failure 分開。Profile 不改 active model；same-session 舊 instructions 不能覆蓋新 operation authority。依據：[Claude 規格](../specs/claude-code-adapter.md)。
- **不阻擋使用者切模型**：PreModelSwitch best effort pending，不 deny／delay switch；Post commit 才是下一次 route guarantee，commit 前 race 如實揭露。State／lock failures fail closed，不改成跨 session「最新 state」。依據：Claude 規格與 [Ticket 2 Review](../evidence/claude-code-adapter-1.4.0-ticket-2-review-after-tenth-corrections.md)。
- **只保存最小 runtime state**：session ID 立即 SHA-256；禁止 prompt、task、repository paths、credentials、diff、個資或 telemetry；state 不寫 cached Plugin。來源、path、input 均視為 untrusted。模型來源日期／snapshot hashes 是 mapping 維護依據。
- **驗證能力與完成狀態分開**：General／Claude 5 靜態指令修正通過，不代表各 30 scenarios 的實際行為通過。先 behavior 100%，再每個 context checkpoint 50%；Codex tools 的 Full／Lite 另有固定 60% proxy 門檻。Generic composed prompt 是兩模式共同固定成本，不宣稱 60% 縮減；上述量測都不是帳單保證。依據：兩個最新 profile Reviews 與[驗證手冊](../maintainer/validation.md)。
- **來源升版不等於發布完成**：2026-09-10 已核准先對齊 1.4.0 與離線 ZIP，不新增缺 live evidence 即禁止 builder 的限制。正式 completion 仍保留原驗收 gates。來源下載連結不是遠端存在證明。
- **安全安裝更新**：明確 install/update/remove 請求授權該次必要 writes；status 唯讀。已 current／disabled 維持 no-op／disabled，未知來源、scope 或 partial failure 停止而不 remove-first。Claude 只支援 user scope；normal uninstall 保留 marketplace／mode Config，可重建 data 預設刪除，明確要求才 keep-data。
- **串行輸出與復原**：Windows WinError 5 bounded retry 也適用 rollback；permanent ACL 可能等到上限，unknown error 立即失敗。Recovery 未完成必須保留 primary／recovery errors 及 staging／backup。Same-output concurrent builds 不是現行承諾。依據：1.3.1 規格與[發布手冊](../maintainer/releasing.md)。
- **品牌與歸屬**：獨立專案，受 Matt Pocock MIT skills 啟發，不宣稱隸屬或背書。透明紅色海馬問號與 `#C8262A`，保留 LICENSE／THIRD_PARTY_NOTICES；原資產製作 source-image SHA-256 為 `C22CF733EBF01ECFEB9C5E9A29AC37496A8B78BBE09F22D5942EC31F0B374EBB`，只作歷史製作來源。

## External dependencies

- Codex Plugin marketplace／CLI 的外部契約；本專案靜態驗證不能替代實際安裝／host 操作證據。
- Claude model 4.6+、Claude Code 2.1.251+、Node.js 22+ 是分開的最低條件。Exact 2.1.251 用來確認最低 host contract，真實環境 model availability 另行觀測。
- Anthropic 官方 [Plugins](https://code.claude.com/docs/en/plugins-reference)、[Marketplace](https://code.claude.com/docs/en/plugin-marketplaces)、[Skills](https://code.claude.com/docs/en/skills)、[Hooks](https://code.claude.com/docs/en/hooks)、[Subagents](https://code.claude.com/docs/en/sub-agents) 與 [CLI](https://code.claude.com/docs/en/cli-reference) 是原 2026-09-04 設計來源；本次未重新上網查證。版本化 snapshots 在 tests/claude/fixtures，維護時更新查核證據。
- CPython 3.12、PyYAML 6.x、Pillow 12.3–12.x 是目前開發／驗證依賴。Node 不進 Codex／Generic consumer prerequisites。
- GitHub repository `Mysterio1001/Ask-Then-Do-It` 承載各 provider catalogs、tags 與 assets；目前遠端狀態須另外查核，不能由工作目錄推斷。

## Unresolved items

真實 host／profile／context／smoke 缺口以[狀態清單](status.md#必須接續的驗證)為唯一現況入口。保留既有未接受架構提案：細化 rule-clause／scenario mappings、locale-neutral policy inventory、strict release JSON 與必需 check boundary、execution-bound evidence、pure composer／transaction 分離、router state-store／deadline／RouteDecision、identity projection／test helper 組織。這些是 future proposals，不代表已授權重構。

新增其他 adapters、universal installer／registry、Claude 非 user scopes、Desktop／web/cloud、unattended updates、private fork 分發、Community Marketplace 與 signing/provenance 方案均待後續決策。官方 bare aliases 是否顯示與 exact invocation 仍按實測記錄，不作多一個受支援公開入口的承諾。

## Artifact links

- [工作流程規格](../specs/workflow.md)、[Claude adapter 規格](../specs/claude-code-adapter.md)：承接既有需求與規格。
- [目前狀態](status.md)：承接原 Ticket Plan 的剩餘工作、依賴、已核准測試選擇。
- [發布手冊](../maintainer/releasing.md)、[驗證手冊](../maintainer/validation.md)：操作與回歸依據。
- [發布歷史與原始來源](../evidence/release-history.md#document-sources)：原 RDR／Specification／Ticket Plan／Review 仍可從已驗證快照找回，沒有把新摘要當成原始核准證據。

## 本次知識整理對照

Additions：主要文件導覽、清理快照定位與必要回歸測試索引。Modifications：按現行來源與較新正式決策整理 architecture／依賴；過期交接移入歷史。Removals：重複的規格全文、已套用 KB 差異及「現在進入 Ticket 2」等不再適用的下一步。未完成驗證與未接受提案移入狀態頁，沒有刪除其事實或變成通過。

Approval: 原始 Knowledge Base 於 2026-08-13 核准；使用者於 2026-08-17 在完整 `1.3.1` Requirement Decision Record 與 Knowledge Base Change Summary 展示後明確核准該次同步；使用者於 2026-09-04 在完整 Claude Code Adapter `1.4.0` Requirement Decision Record 與 Knowledge Base Change Summary 展示後明確回覆「核准」，共同核准該次同步；同日，使用者在完整 Claude Code Adapter `1.4.0` Specification Knowledge Base Change Summary 展示後再次明確回覆「核准」，核准本次 Specification knowledge 同步；同日，使用者在完整 Specification Knowledge Base Correction Summary 展示後明確回覆「核准」，核准 route guarantee 與 provenance 的三項最小修正；使用者於 2026-09-05 核准完整 Ticket Plan 與十張 Ticket 的全部 `tdd` mapping，並在完整 Planning Knowledge Base Change Summary 展示後明確回覆「核准」，核准本次 planning knowledge 同步；使用者於2026-09-06在完整Marketplace description Draft Specification correction、Knowledge Base Change Summary與exact-host blocker evidence展示後明確回覆「核准」，核准本次明示同步；使用者於2026-09-07在被告知provisional implementation可能因exact-host差異返工後，明確核准將Ticket 3移至local completion hard gate並先進入Ticket 2，核准本次sequencing knowledge同步；使用者於 2026-09-10 在完整文件精簡與版本統一需求及知識庫變更摘要展示後明確回覆「核准」，共同核准本次明示同步；使用者於 2026-09-10 核准文件精簡與版本統一完整計畫、三項測試選擇及規劃知識庫變更摘要，核准本次明示同步。

上述為原始知識庫的歷史核准來源；其原始 bytes 同時保存在清理快照。

[回到 README](../../README.md)
