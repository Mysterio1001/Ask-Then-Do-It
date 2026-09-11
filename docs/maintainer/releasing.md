# 維護與發布手冊

適用來源版本：1.4.1。此手冊承接指令安裝 1.2.0、Windows 發布可靠性 1.3.1、文件／版本統一 1.4.0 與歷次發布計畫；它描述維護操作，不宣稱正式 1.4.1 已發布。當前進度見[狀態](../project/status.md)，歷史依據見[發布紀錄](../evidence/release-history.md)。

## 開發環境

使用 CPython 3.12，從 [requirements-dev.txt](../../requirements-dev.txt) 安裝 `PyYAML>=6.0,<7` 與 `Pillow>=12.3,<13`。既有 Windows 環境使用 `.venv/Scripts/python.exe`；其他平台通常為 `.venv/bin/python`。下列 `python` 表示已選好的開發環境解譯器。

```text
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

測試根目錄不是一般 package，不追加 `-t .`。Claude router 與其測試需要 Node.js 22+；PyYAML／Pillow 是開發依賴，Node 是 Claude 的消費端條件，均不得誤列為 Codex／Generic 使用者依賴。

## 來源與版本更新

[release/release.json](../../release/release.json) 宣告版本、package sources、inventory、checks 與 managed outputs。更新版本時按責任核對，不能全域取代每個舊數字：

| 來源 | 要同步的資訊 |
| --- | --- |
| Core 與 adapter declarations | Core version、adapter version、rule mapping／conformance；schema version 獨立保留 |
| Codex／Claude Plugin manifests | package identity、current version、來源與支援的 metadata |
| 兩種 repository catalogs | provider-specific source、正式 ref、版本及描述，不得互指平台 |
| Claude router／model mapping | runtime version、exact model IDs、官方來源查核日期與 trace |
| Generic manifest／組合入口 | current version、預設模式宣告、固定 module 順序與 attribution |
| 三語 README／guides／START-HERE | 下載檔名、same-version guide URL、平台最低版本與既有 layout |
| tests 與 release evidence | 當前一致性要求、新 candidate hashes 與真正執行的驗證結果 |

歷史 release versions、原始證據 hashes、Claude Code／Node／模型最低版本及資料 schema 不隨套件版本盲目改寫。Consumer payload 必須自足，不新增對 repository 維護文件的執行依賴。

文件責任：初學者指南擁有完整 Full／Lite 使用流程；平台指南擁有安裝、Config、更新、移除與排錯；Claude 進階資訊收在同語言指南的收合區塊。九份平台主指南保留七個章節與三語等價內容。README 保持三語布局、快速開始只放首次安裝、更新獨立收合、更多說明維持初學者→Codex→Claude→Generic→設計。

## Catalog 與安裝契約

Codex 使用 `.agents/plugins/marketplace.json`，Claude 使用 `.claude-plugin/marketplace.json`。Catalog 留在 repository，安裝來源 pin 正式 tag，不能加入 consumer ZIP 或跨平台混用 schema。

Codex 公開操作為 `codex plugin marketplace add Mysterio1001/Ask-Then-Do-It`、`codex plugin add ask-then-do-it@ask-then-do-it` 與 `codex plugin marketplace upgrade ask-then-do-it`；不把 `codex plugin install` 當成支援命令。Claude 的 qualified identity 相同，但使用 Claude 自己的 Marketplace、命令及 `user` scope，詳細狀態矩陣見 [Claude 規格](../specs/claude-code-adapter.md)。

自然語言安裝／更新請求授權該次最小必要操作；版本／狀態檢查唯讀。先查來源、版本與安裝狀態，不反覆重加已有來源、不暗中降版或換來源；失敗停止並回報。ZIP 是受支援的備援，Claude ZIP 只透過 `--plugin-dir` 載入當次 session。來源／狀態不明時不以先移除再安裝掩蓋問題。安裝文件不得冒充 host 原生背景自動更新。

Codex 圖示沿用透明紅色海馬問號與 `#C8262A`；尺寸、透明度、PNG integrity 由既有 assets tests 驗證。保留 [LICENSE](../../LICENSE) 與 [THIRD_PARTY_NOTICES](../../THIRD_PARTY_NOTICES.md) 的來源歸屬。

## 隔離建置與可重現性

先選兩個全新、在 repository 內且與來源分離的輸出位置。`--allow-test-output-root` 只允許明確的測試輸出；不要以來源目錄或個人資料目錄作 output。

```text
python scripts/build_release.py --allow-test-output-root --output-root .claude-offline/candidate-a
python scripts/build_release.py --allow-test-output-root --output-root .claude-offline/candidate-b
```

比對兩棵輸出樹相對清單與每個檔案 bytes，包含展開檔、ZIP、checksum。僅兩個 ZIP 大小相同或 checksum 檔文字相同不構成完整可重現性。測試共用 [built_fixture.py](../../tests/release/built_fixture.py) 在隔離目錄建新 candidate，不把根目錄舊 `dist/` 當成目前來源結果。

| 平台 | 展開目錄 | ZIP（相對 output root） |
| --- | --- | --- |
| Codex | `codex/ask-then-do-it` | `codex/ask-then-do-it-1.4.1.zip` |
| Generic | `generic/ask-then-do-it-generic-1.4.1` | `generic/ask-then-do-it-generic-1.4.1.zip` |
| Claude | `claude/ask-then-do-it` | `claude/ask-then-do-it-claude-1.4.1.zip` |

三平台 inventory 必須符合來源與 release config。展開內容與 ZIP 相對清單／bytes 相同，ZIP metadata 固定，拒絕重複成員、路徑逃逸、symlink、未知檔案與非預期目錄。每個 archive 在 `checksums.sha256` 恰有一筆 SHA-256，順序穩定；catalogs、tests、維護 evidence、local state 與機器路徑不得進 consumer payload。

Generic builder 依固定 module 順序組合 `SKILL.md`，維持可上傳至 Claude Desktop 的自足 Skill 入口；文字對話服務可直接貼上同一份 `SKILL.md`。單獨 modules 是維護來源，不增加跨 session 持久性的宣稱。Claude package validator 另核對 canonical source 的精確 bytes。

Generic ZIP 保留單一套件資料夾，入口位於 `ask-then-do-it-generic-<version>/SKILL.md`，不是 ZIP 最外層。檔案從 YAML frontmatter 開始，包含 `name` 與 `description`；這個資料夾封裝方式與 [Anthropic 的 Skill packager](https://github.com/anthropics/skills/blob/main/skills/skill-creator/scripts/package_skill.py) 一致。ZIP inventory 與 frontmatter 通過僅代表本機格式驗證，不代表 Claude Desktop 已完成安全掃描、成功匯入或觸發。

Generic-only 本機候選包請使用獨立且已忽略的輸出目錄，例如 `python scripts/build_release.py --package generic --allow-test-output-root --output-root ticket-generic-build-candidate`。不要手動混入既有 `dist/`，否則多版本目錄與額外 checksum 會破壞 managed output inventory。本次已核准將專案、Core 與三平台套件統一升至 1.4.1，release config、各平台與 Marketplace 必須同步；不能以新 bytes 覆蓋已發布的同版資產。

## 更新既有輸出與失敗復原

`python scripts/build_release.py` 以 `dist/` 為預設輸出；執行前先保存需保留的舊 candidate。Builder 只管理 config 列出的 `codex`、`generic`、`claude`、`checksums.sha256`，不擅自掃掉 unmanaged content。

維護契約是單一 builder 串行操作同一 output root；目前不承諾同 output 並行 builds。流程先完整 staging validation，再檢查舊輸出、備份、替換與復原。

- 完整且驗證過的舊 Codex／Generic 二套件可升級至三套件；未知、多餘、缺檔、checksum 破損或 ZIP parity 不符都拒絕。
- 新 candidate 在 staging 未通過時不碰舊輸出；替換中失敗則復原先前 bytes，並移除本次部分安裝的新 family。
- Windows `WinError 5` 在 replacement／rollback 的 bounded-retry allowlist；永久 ACL 問題可能等待到上限才失敗，不能無限重試。未列入 allowlist 的錯誤立即失敗。
- 復原成功：回報失敗的 build 與舊輸出已還原，不宣稱新 candidate 成功。
- 復原仍失敗：保留 staging／backup，回報 primary error、recovery errors、相關位置與需人工復原的狀態；不得清理掉唯一復原資料或宣稱存在有效 release。

以上由 release transaction／safety tests 保護，文件清理不改動實作。

## 驗證與正式完成

先依[驗證手冊](validation.md)執行適用檢查，再將實際結果寫入 candidate 專屬 ledger。`release/release.json` 的 required checks 涵蓋 automated tests、workflow token proxy、Codex Skill／Plugin、三 adapter conformance、三 package inventory、reproducibility、ZIP equivalence、SHA-256、removed-artifact scan、architecture diagnosis，以及 Claude Plugin、behavior、context、live-smoke。

```text
python scripts/validate_release_evidence.py --config release/release.json --ledger <candidate-ledger.json> --evidence <candidate-evidence.md>
```

該工具驗證 evidence／ledger 的結構、版本、check 完整性與狀態，不會替維護者執行或認證每個命令。只填 passed 不是真實證據；保留命令、exit code、raw output、candidate hashes 及必要人工判讀。

來源 1.4.1 與離線 ZIP 可以先完成，缺少 Claude 實測時仍不得宣稱正式 release gate 或完整 local candidate 驗收通過。不得為省步驟把 behavior、context、live-smoke 的 unverified 改成 passed；也不新增「缺實測就禁止任何離線 ZIP」的限制。

## 對外發布與歷史保存

本機 source、ZIP、checksum 與驗證完成不等於 tag／GitHub Release／Marketplace 啟用完成。對外 tag、push、PR merge、asset upload、公告或 Community Marketplace submission，依該次使用者明確授權與觀察結果記錄。正式傳輸檢查核對 tag tree、公開 assets bytes、same-version guide URLs 及 provider catalogs，不能由本機成功推論。

不要改寫已發布 tag 或把新文件升版套到舊 ledger。歷史原始文件可在已核准清理後移出工作目錄，但 bytes、hash 與定位必須能找回；保存方式見[歷史來源](../evidence/release-history.md#archive)。

固定 `--preview-claude` 入口仍只適用 `1.4.0-preview.1` 的來源。它不能用目前 1.4.1 source 建立 preview；若要重現，使用相應歷史 source 和隔離 output。這次升版沒有退役此功能或移除其安全測試。

[回到 README](../../README.md)
