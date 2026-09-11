# Claude context capture contract

`capture-template.json` 是尚未執行的固定十情境模板，不是模型紀錄，也不包含本專案已達成 50% 精簡的證據。測試在 temporary directory 建立明示 synthetic 的小段文字，只驗證計算與拒絕不完整資料的行為。

準備新的模板（目的檔必須尚未存在）：

```text
python scripts/measure_claude_context.py --prepare <new-capture.json>
```

取得並通過真實 behavior evidence 後，才可計算正式 context gate：

```text
python scripts/measure_claude_context.py --fixture <capture.json> --behavior-evidence <behavior-evidence.json> --json
```

`--synthetic` 只接受 `evidence_kind: synthetic`；輸出永遠 `release_pass: false`。此處 `release_pass` 僅指 context gate，不能代表完整版本或其他 release gates 已通過。未執行模板、缺失／偽造的簡單 `passed: true` behavior 物件會在計算前失敗。

每個 scenario 共用相同 `task`、`stage_outcome` 的相對路徑／raw SHA-256 與 `capability`。`model-switch-continuation` 固定採 Lite 延續階段；兩 profiles 必須使用相同任務、capability 與結果，記錄切換 notices 和所有實際注入。

每個 profile 的 `stage-ready`（Full Review 另有 `reviewer-ready`）保存：

- `capture_complete`：只有獨立檢查完整 host injection 紀錄後才設 true。
- `trace`：相對路徑／SHA-256，指向另存的 JSON `{scenario, profile, checkpoint, events}`；實測 events 必須與 measurement inventory 完全相同且同序。
- `events`：按实际載入次序，每筆有 `kind`、`origin`、`path`、`sha256`。同一段重複注入需重複列入；reviewer-ready 必須保留 stage-ready 的全部前綴紀錄。

必要 material 的確切來源由 `required_material()` 列出：automatic public Skill body、selected profile orchestration 和 stage、`UserPromptExpansion` 的完整 model-visible route context。Full Review 的 reviewer-ready 再包含 reviewer description 與 agent prompt body。只讀 canonical file 的來源會對照當前 Plugin bytes；Skill/agent 的 body 依 frontmatter 邊界取出，description 單獨計入。若 host 額外載入 listing，用 `skill-listing`／`host-skill-listing`；其他 hooks 用 `hook-context`／`hook-additional-context`，不要把同一次 route 注入重複拆成兩個事件。實際重複注入則逐次計數。

可排除的 `kind` 僅有 `host-system`、`tool-definitions`、`user-task`、`repository-source`、`task-artifacts`、`necessary-tool-output`、`hidden-reasoning`、`model-output`；它們的 `origin` 必須與 kind 相同且兩邊 hash／順序相同。Plugin instructions 不得重新命名為排除項目。只由 machine 執行而未送入模型的 router/config source 不列為注入；它們送入模型的 output 要列入。

依每次注入的原始 UTF-8 bytes 保存 SHA-256。計算逐段 NFC、Unicode whitespace collapse、trim，依載入次序以一個 LF 連接；`proxy_tokens = ceil(normalized_bytes / 4)`。每一格以 `optimized * 100 <= general * 50` 判斷，不可用平均補償。輸出保留版本、fixture hash、behavior evidence hash、input hashes、source 路徑/hash/次序、兩側 bytes/tokens、公式、reduction 與各格結果。

工具檢查的是提供資料的一致性，不能證明 host log 真偽或偵測完全沒有被記錄的注入。`capture_review` 要寫明獨立查核來源與結論；不可透過共同修改 capture、trace 和 reference 冒充真實觀察。任何 source 變更都需要重新取得受影響的 behavior/context evidence。正式量測尚未執行；本輪僅交付離線工具。

必要 stage 是最低 inventory，並非最多只計一份。若 documented requirements 同時載入同一 profile 的 `requirements.md`，或 workflow 到達此 checkpoint 前已載入其他合法 stage，必須用額外 `stage` event 記錄。工具接受 closed stage inventory 中同一 profile 的模組、逐次計數並在 observed 模式比對 canonical bytes；另一 profile 的來源仍會被拒絕。
