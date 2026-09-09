# Claude Code Adapter 1.4.0 Ticket 9 Offline Packaging Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-9-offline`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Approved implementation mode: `tdd`

Status: Offline tools 與 frozen-source preview locally verified；ZIP Review finding 已修正且獨立 reviewer accepted。完整 Ticket 9 與正式 release 尚未完成。

Inputs: Approved [Specification](../specs/claude-code-adapter-1.4.0.md) section 10；Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 9 及 2026-09-09 離線優先核准節；既有 deterministic builder、release transaction tests 與 canonical Claude source。

Assumptions: 協調者已證明本次 Full fallback、`multi_agent` capability、無適用 AGENTS；使用者核准提前執行離線 builder／preview 工作，所有 Ticket mode 仍 `tdd`。合成 fixtures 只供 packaging tests，不是 Claude behavior／host observation。

Deferred: Authenticated host、30＋30 scenarios、paired authority、正式 context gate、lockstep activation、canonical Claude conformance、default `dist/` 更新、final candidate freeze 與 live smoke。缺失檢查不視為 passed。

Handoff: [獨立 Review](claude-code-adapter-1.4.0-ticket-9-offline-review.md)已接受 ZIP correction；交回中央整合完整驗證。可交付預覽保留於 `.claude-offline/package/`。正式 identity transition 與 release completion 等待所有原定 gates。

## Delivered offline behavior

`scripts/build_release.py --preview-claude --output-root <isolated-repository-directory> --allow-test-output-root` 使用固定 Claude-only preview config。該模式拒絕 default `dist/`、其子目錄、repository sources／protected roots、symlink/junction ancestors、非 explicit isolated opt-in、其他 family 或自訂 config。命令輸出明示 `NOT A RELEASE`。

預覽沿用既有 staging、ZIP writer、checksums、managed-output validation、commit、WinError 5 retry、rollback 與 incomplete-recovery 保留流程。Expanded payload 是 `claude/ask-then-do-it/`；ZIP 是 `claude/ask-then-do-it-claude-1.4.0-preview.zip`。外層 deterministic `preview.json` 標記 `status: not-a-release`、`evidence_claim: packaging-only-no-host-or-model-verification`，並列每個來源檔的 SHA-256；此 metadata 不進 runtime package 或 ZIP。Checksum 只列選定 archive。

新 standard-library `scripts/validate_claude_package.py` 固定 section 10 的 30 runtime files 與 2 legal files；拒絕缺檔、extra file、額外空 directory、non-regular entries、symlink/junction 及錯誤 manifest identity/version。Runtime bytes 從同一 canonical source複製；legal bytes 來自 repository root；staged package 逐檔比對來源。ZIP duplicate members 與 provider directory 額外內容也被拒絕，即使 caller 更新 checksum。

現行 config 不含 Claude 時，`--package all` 仍只選 Codex／Generic；`release/release.json`、current identities、canonical Claude conformance、default `dist/` 及歷史 evidence 均未修改。Builder 預先支援 optional formal `claude` family config，但要求 exact source/directory/archive/inventory、Core/release lockstep、canonical Claude conformance identity 及 Claude-required check declarations。這只驗證打包輸入，不執行或核准行為／context／live results，也不寫 release completion evidence；正式 activation 仍是後續 gate。

## Changes

- `scripts/build_release.py`
- `scripts/validate_claude_package.py`
- `tests/claude/test_release_preview.py`
- 本 evidence

## Observed Red

初步 synthetic-main 測試因尚無 preview 分支而落入一般 release path，報缺少 synthetic repo 的 Core declarations；此 setup/path failure **不列為有效 Red**。改以 public CLI option 邊界確認缺失行為後，才開始 production implementation。

```text
.venv/Scripts/python.exe -B -m unittest tests.claude.test_release_preview.ClaudeReleasePreviewTests.test_cli_explicit_preview_mode_is_supported -v

build_release.py: error: unrecognized arguments: --preview-claude
AssertionError: Explicit offline Claude preview option is unavailable: 2
Ran 1 test in 0.050s
FAILED (failures=1)
```

Exit `1`。實作完成第一輪 Green：

```text
.venv/Scripts/python.exe -B -m unittest tests.claude.test_release_preview -v

Ran 7 tests in 2.110s
OK
```

第二個 regression Red 先加入 duplicate ZIP member／extra provider file 測試，第一個 boundary 在當時未被拒絕：

```text
.venv/Scripts/python.exe -B -m unittest tests.claude.test_release_preview.ClaudeReleasePreviewTests.test_duplicate_zip_member_and_extra_provider_file_are_rejected -v

AssertionError: BuildError not raised
Ran 1 test in 0.289s
FAILED (failures=1)
```

Exit `1`。隨後加入 duplicate-member 與 exact provider inventory guards。

## Focused and relevant regression Green

```text
.venv/Scripts/python.exe -B -m unittest tests.claude.test_release_preview tests.release.test_release_contract tests.release.test_release_transaction tests.release.test_release_safety tests.release.test_codex_release tests.release.test_generic_release -v

Ran 43 tests in 10.564s
OK
```

Exit `0`。其中 9 個新 preview tests 覆蓋 explicit CLI、exact bytes/inventory、兩次 ZIP/checksum reproducibility、metadata 非正式標記、無 metadata 進 ZIP、隔離寫入、missing/extra/wrong-version source、link rejection、current formal declaration gate、nonmanaged content preservation、marker tamper rejection、source-byte drift rejection、shared rollback。既有 34 個相關 tests 覆蓋 current two-family identity、Codex/Generic package contracts、collision、staging、prior-version replacement、WinError 5 bounded retry、successful rollback、incomplete recovery 保留與 no-network/install/publish builder boundary。

測試只生成明示 synthetic bytes 的 temporary repository fixtures 與 isolated test outputs；未啟動 Claude、登入、安裝、卸載、network 或 publication。未執行 full repository suite。

## Independent ZIP finding correction

獨立 reviewer 指出 validator 忽略 ZIP directory entries 且未驗證metadata，可能接受額外目錄、traversal directory或非regular entry。先新增以下 regression：

```text
.venv/Scripts/python.exe -B -m unittest tests.claude.test_release_preview.ClaudeReleasePreviewTests.test_zip_directories_and_noncanonical_metadata_are_rejected -v
Ran 1 test in 0.642s
FAILED (failures=5)
```

五個 `BuildError not raised` 分別是 unexpected empty directory、`../outside/` directory、symlink mode、非canonical timestamp、stored compression；每次都重新計算checksum，故不是hash損壞造成拒絕。

修正為完整且排序正確的 ZipInfo inventory，以及canonical timestamp、Unix regular `0644` mode、deflate、flags／comment／extra field檢查；directory entries一律不在generator的expected inventory中。首次broader run因歷史synthetic Codex/Generic prior archive使用不同timestamp而有1 failure。保留既有prior-release upgrade compatibility：僅既有Codex/Generic prior archives允許非canonical timestamp/compression；全部paths、duplicates、file contents與regular-file安全條件仍驗證；所有新staging與Claude previews都驗證canonical metadata。

最終相同六個相關test modules重跑：

```text
.venv/Scripts/python.exe -B -m unittest tests.claude.test_release_preview tests.release.test_release_contract tests.release.test_release_transaction tests.release.test_release_safety tests.release.test_codex_release tests.release.test_generic_release
Ran 44 tests in 8.689s
OK
```

Exit `0`；其中10個preview tests，其餘34個既有release regressions。`git diff --check -- scripts/build_release.py` exit `0`。

獨立 reviewer 重跑五種 ZIP mutations 的 candidate／prior-preview 兩入口，共十筆拒絕觀察，並唯讀確認既有 default `dist/` 及 current `1.3.1`／`1.3.1`仍通過。最後僅做source格式整理：既有Generic generated Markdown hard-break尾端空白改寫為Python `\x20\x20`，獨立載入修改前後的builder比較`compose_generic_workflow`結果，bytes完全相同；因此不需再跑behavior tests，preview bytes亦不變。

## Frozen canonical source preview

文件owner explicit freeze後，從同一canonical source產生兩次isolated preview；最終命令：

```text
.venv/Scripts/python.exe -B scripts/build_release.py --preview-claude --output-root .claude-offline/package --allow-test-output-root
.venv/Scripts/python.exe -B scripts/build_release.py --preview-claude --output-root .claude-preview-1.4.0-b --allow-test-output-root
```

兩次exit `0`，stdout皆有 `NOT A RELEASE`。逐檔raw-byte比對結果：

```json
{
  "final_preview_identical": true,
  "files": 35,
  "zip_sha256": "6c83d5b712b34c00131ad92c745f47cd57a49da7e63fc0a5ec7337b9c7c61348",
  "destination": ".claude-offline/package"
}
```

35 files = 32 runtime/legal payload files＋ZIP＋checksums＋外層preview marker。可交付ZIP為 `.claude-offline/package/claude/ask-then-do-it-claude-1.4.0-preview.zip`，55,573 bytes。Expanded/ZIP均不含preview metadata、Marketplace、test fixtures或local state；payload raw-source hashes保存在外層 `preview.json`。

兩份舊temporary previews在確認resolved absolute path位於本workspace且具有marker後，以PowerShell `Remove-Item -LiteralPath`安全清理；保留使用者可檢視的`.claude-offline/package/`。Readonly `git diff --name-only`對`release/release.json`、Core/Codex/Generic current declarations、default `dist/`沒有輸出。沒有提前啟用canonical Claude conformance。

## Residual limits

Preview marker 是明示 packaging evidence 與 managed-output ownership marker，不是安全簽章；若有人一致地改動 payload、ZIP、checksums 與 marker，它不能證明原來的來源。Staging 的 canonical byte comparison 保護本次 build，後續正式 evidence 必須另外追蹤 frozen source hashes。沒有 model／host behavior 可以從 package parity 推導。

此工具保留目前的 two-family release identity，沒有產生正式 three-family `1.4.0` candidate。完整 Ticket 9 仍不得標 Completed。
