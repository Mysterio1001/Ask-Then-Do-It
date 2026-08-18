# Ask Then Do It 1.3.1 Maintenance Ticket 3 Implementation Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `release-1-3-1-maintenance-ticket-3-implementation`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `3 - 整合 lockstep 1.3.1 identities、packages 與 checksums`

Execution mode: `tdd` (`Add tests`, explicitly selected by the user)

Status: Completed

Inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md)、completed Ticket 1 與 accepted Review、completed Ticket 2 與 accepted P2 closure Review、目前 `1.3.0` source/package contracts、release builder、release-evidence validator 與 frozen Token proxy benchmark corpus。

Assumptions: `v1.3.0` 與全部已發布資產、Approved historical artifacts 及其 recorded hashes 不可變；default `dist` 是可由正式 builder 原子替換的本機 candidate。Token proxy 的 algorithm、normalization、event inventory、13 個 fixture files、token counts 與 60% threshold 必須不變；report fingerprint 會依設計納入 active Skill/Generic source bytes，因此核准的同長度版本文字更新會改變衍生 SHA，而不代表 fixture mutation。

Deferred: final `1.3.1` validation ledger、Completed release evidence、release-milestone architecture diagnosis 與 final Full Review（Ticket 4），以及 tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement。

Handoff: Initial [independent Review](release-1.3.1-maintenance-ticket-3-review.md) requested three P2 findings；第一輪修正後的fresh [closure Review](release-1.3.1-maintenance-ticket-3-review-after-p2.md) confirmed JSON duplicate-key與default `dist` findings closed，但requested changes for one remaining Markdown envelope P2。使用者核准後已完成第二輪Red/Green及全部affected/full gates；fresh [second closure Review](release-1.3.1-maintenance-ticket-3-review-after-envelope-p2.md) confirmed all findings closed with no actionable finding。Ticket 3 candidate現可凍結並交給Ticket 4；本evidence不授權外部發布，也不宣稱Ticket 4的release evidence已完成。

Approval: Implementation authority comes from the Approved Ticket Plan、其 approved `tdd` mode，以及使用者對 Ticket 3 execution 的明確核准。Initial Review 顯示三項 P2 後，使用者另行明確回覆「核准」，只授權修正這三項 finding。第一輪closure Review仍發現Markdown envelope P2後，使用者再次明確回覆「核准」，只授權第二輪closure correction。

## Outcome

- Release、Core、Codex adapter、Generic adapter、Plugin、Marketplace candidate metadata、current documents、runtime declarations、package paths、ZIP names 與 checksums 已 lockstep 升至 `1.3.1`。
- Default `dist` 只由 `scripts/build_release.py` 原子替換，現含 Codex 9 Skills、2 assets、Generic 11 prompt modules、兩個 `1.3.1` ZIP 與一份兩行 checksum ledger；沒有舊版 managed output。
- 43 個 tracked Approved `1.3.0` requirements/specification/plan/evidence artifacts 加入固定 SHA-256 guards，全部 bytes 保持不變。
- 13 個 Token proxy fixture files 加入固定 SHA-256 guards；fixture 內作為 benchmark input 的 `1.3.0` 文字未被盲目升版。
- Consumer source、expanded package 與 ZIP entry paths 新增 no-Pillow contract；Codex Plugin manifest 與 Generic manifest 都沒有 Pillow runtime dependency。
- Release-evidence validator 現要求 Markdown 中恰好一個正確的 `Release version` 與一個 `Status: Completed`，並要求每個 configured required check 都必須是 `passed`；duplicate/conflicting metadata 與 `skipped-by-user` 不再能繞過 gate。

## Files changed

- Identity and configuration: `release/release.json`、`core/CORE.md`、`core/rules/rules.yaml`、Codex conformance/rule mapping、Plugin manifest、Marketplace catalog 與 Marketplace validator default ref。
- Runtime sources: 8 個會輸出 artifact envelope 的 Codex Skills、Generic manifest 與 11 個 Generic prompt modules。
- Current user documents: README、root START-HERE、Codex/Generic package START-HERE，以及三語 Codex/Generic guides。
- Validation: `scripts/validate_release_evidence.py`、release/Codex/Generic/conformance/documentation/Marketplace current-version tests、43-file historical guard、13-file Token fixture guard、no-Pillow package contract 與 evidence fail-closed tests。
- Generated candidate: default `dist` 的 `1.3.1` expanded packages、ZIPs 與 `checksums.sha256`；builder 以外沒有手改 generated output。
- 本 evidence。既有 Ticket 1/2 evidence、Approved `1.3.1` requirement/spec/plan、Project Knowledge Base、user-owned `claude-code-adapter-working-notes.md` 與全部 historical `1.3.0` artifacts 未改寫。

## Identity Red and Green

First Red command:

`& '.\.venv\Scripts\python.exe' -m unittest -v tests.release.test_release_1_3_contract.ReleaseOneThreeContractTests.test_active_identity_and_current_document_downloads_are_1_3_1 tests.release.test_release_1_3_contract.ReleaseOneThreeContractTests.test_release_config_locks_runtime_inventory_and_proxy_gate tests.release.test_release_1_3_contract.ReleaseOneThreeContractTests.test_approved_historical_1_3_artifacts_are_byte_identical tests.release.test_release_1_3_contract.ReleaseOneThreeContractTests.test_frozen_token_proxy_fixture_bytes_are_identical`

Observed Red: exit `1`; `Ran 4 tests`; active identity 與 archive path 兩個 tests 分別因實際 `1.3.0` 不等於預期 `1.3.1` 而失敗；43-file historical guard 與 13-file Token fixture guard 同時通過。這證明 Red 只偵測缺少的新 current identity，沒有把歷史或 benchmark input 當成 stale source。

Focused Green after source/config/document synchronization: exit `0`; `Ran 4 tests`; `OK`。

## Evidence-gate Red and Green

First metadata command:

`& '.\.venv\Scripts\python.exe' -m unittest -v tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_absent_ledger_or_evidence_rejects tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_incomplete_or_version_mismatched_evidence_rejects tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_duplicate_status_metadata_rejects_evidence tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_duplicate_release_version_metadata_rejects_evidence`

Observed Red: exit `1`; absent/incomplete/simple mismatch characterization cases通過；兩個 duplicate/conflicting metadata cases 失敗，因舊 validator 錯誤回傳成功。最小修正改為精確收集 metadata lines，並要求 values 恰好等於單一 `Completed` 與單一 config version。

Specification requirement 9 另揭露既有 `automated-tests: skipped-by-user` 豁免。新增 `test_required_automated_tests_cannot_be_skipped` 後的 Red 是 exit `1`; `Ran 1 test`; validator 仍回傳 `0`。Green 修正移除 required check 的特殊豁免，任何 status 不是 `passed` 都 fail closed；approval metadata 也不能覆蓋 required status。

Final evidence-gate command: `& '.\.venv\Scripts\python.exe' -m unittest -v tests.release.test_release_evidence`。

Final evidence-gate result: exit `0`; `Ran 13 tests in 1.596s`; `OK`。涵蓋 absent ledger/evidence、incomplete status、ledger/evidence version mismatch、duplicate status/version、missing check、failed/blocked check、required test skip、non-test skip 與 mandatory Token proxy gate。

## Independent Review P2 correction

Initial [independent Review](release-1.3.1-maintenance-ticket-3-review.md) requested three P2 corrections：JSON duplicate keys 可把 failed check 覆寫成 passed；fenced/comment/body-section metadata 可偽造或干擾 top-level artifact envelope；default `dist` 沒有直接綁定 fresh build 的 byte-for-byte candidate gate。三項 finding 都留在 Ticket 3 ownership，沒有擴張為 Ticket 4 或 architecture refactor。

Validator correction Red command：

`& '.\.venv\Scripts\python.exe' -m unittest tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_duplicate_json_keys_reject_release_artifacts tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_non_envelope_metadata_cannot_complete_draft_evidence tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_non_envelope_examples_do_not_conflict_with_valid_metadata`

Observed Red: exit `1`; `Ran 3 tests in 1.026s`; `FAILED (failures=7)`。Config root、ledger root 與 nested check object 的 duplicate keys 都被舊 `json.loads` last-write-wins 接受；backtick fence、HTML comment 與 body section內的假 version/status 都被舊 raw regex 接受；反向案例中，正確 top-level envelope 反而被後續範例 fence 的 metadata干擾而拒絕。全部失敗原因都直接對應 Review finding，沒有 setup failure。

P2-3 是 generated-output test-first exception：default candidate 在 Review 時已與 fresh build相同，因此不能誠實製造 natural production Red，也禁止手改 generated `dist`。替代驗證把 default `dist` 加入既有 two-clean-build逐檔 comparison，並只在 disposable copy 注入額外 `pillow-stale.txt` 與 checksum byte drift，證明同一 comparator 會拒絕 inventory及content mismatch。第一次 sensitivity run因 helper內 `subTest` 攔截 `AssertionError` 而 `Ran 1 test`、`FAILED (failures=2)`；這是 test-harness defect，不被記作 behavioral Red。移除該攔截後，隔離 extra-file與byte-drift都由預期的 `assertRaises` 捕捉，default/fresh comparison通過，且沒有增加 builder invocation。

Minimal Green:

- `read_object()` 透過遞迴 `object_pairs_hook` 拒絕 config、ledger及nested object的任何 duplicate JSON key，保留既有 label/path diagnostics。
- Evidence parser只在第一個二至六級 body heading前解析 top-level envelope；CommonMark backtick/tilde fenced code與HTML comments不提供 metadata。Fence外的 exact-one version/status contract維持不變。
- Existing two-build reproducibility test現在同時要求 `first == second == ROOT/dist`，並以暫存 drifted copy證明 extra file與byte mutation敏感度；default `dist`只有 read access。

Focused Green command與結果：同一三-method validator command exit `0`; `Ran 3 tests in 0.770s`; `OK`。Final evidence module exit `0`; `Ran 16 tests in 2.546s`; `OK`。Evidence、base release與1.3 contract整合 command exit `0`; `Ran 36 tests in 6.136s`; `OK`。

## Closure Review Markdown-envelope correction

First [closure Review after P2](release-1.3.1-maintenance-ticket-3-review-after-p2.md) independently confirmed duplicate JSON與default `dist` findings closed，但以完整validator重現合法Setext H2、後續第二個H1及raw HTML body內的假metadata仍可讓Draft evidence exit `0`。這是initial Markdown P2的同一root cause，不是新的workflow feature。

Second correction Red command：

`& '.\.venv\Scripts\python.exe' -m unittest -v tests.release.test_release_evidence.ReleaseEvidenceGateTests.test_non_envelope_metadata_cannot_complete_draft_evidence`

Observed Red: exit `1`; `Ran 1 test in 1.248s`; `FAILED (failures=6)`。舊hand-written Markdown parser錯誤接受plain body、Setext section、metadata line本身作為Setext heading、後續ATX H1、`<details>`及`<pre>`後的version/status；原本backtick fence、tilde fence、HTML comment與ATX H3 cases仍正確拒絕。

Minimal Green移除逐項辨識fence/comment/heading的state machine，改為明確的artifact-envelope grammar：文件第一行必須是ATX H1，之後只收集連續的ASCII `Field: value` metadata lines與其間空行；第一個plain body、heading、fence、comment或raw HTML line立即結束envelope。Metadata line若下一行是Setext underline，也不計入envelope。這使unknown Markdown body construct預設fail closed，而不是持續擴張blacklist。

Focused Green: 同一one-method command exit `0`; `Ran 1 test in 0.890s`; `OK`。第一次整個evidence module執行有`2`個failure，原因是既有version-mismatch與duplicate-version tests建立的片段缺少新contract要求的H1，因而先被正確判定為missing envelope；這是test-fixture specificity，不是production regression。補上H1後，這些tests再次精確驗證原本的version failure reason。

Final second-correction verification：

- Evidence module: exit `0`; `Ran 16 tests in 3.100s`; `OK`。
- Evidence、base release與1.3 contracts: exit `0`; `Ran 36 tests in 10.460s`; `OK`。
- Official default builder: exit `0`; `Built codex, generic release 1.3.1 in ...\dist`。
- Full discovery: exit `0`; `Ran 215 tests in 33.550s`; `OK`；本輪沒有Windows lock failure。
- Skill validator `18/18`、Plugin validator `2/2`、Marketplace、Codex/Generic conformance全部passed。
- Token proxy保持Full `14771`、Lite `5480`、reduction `62.90%`、gate passed。
- Codex與Generic ZIP SHA-256仍分別為`557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209`與`6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b`，與`dist/checksums.sha256`相符。

Fresh [second independent closure Review](release-1.3.1-maintenance-ticket-3-review-after-envelope-p2.md) independently reran `36/36` affected contracts、seven additional temp-only Markdown/HTML adversarial probes及default `dist` parity。Review found no P0-P3 actionable finding，confirmed all initial and first-closure P2 findings closed，and assessed Ticket 3 complete。

## Package build and candidate

Default candidate command:

`& '.\.venv\Scripts\python.exe' 'scripts\build_release.py'`

Observed result: exit `0`; `Built codex, generic release 1.3.1 in ...\dist`。

Post-correction default rebuild使用相同正式 command再次 exit `0`；consumer source沒有因 validator/test correction改變，因此 archive bytes與下列 SHA-256保持不變。

Final archive hashes:

```text
557246c241a8e808c4dd554a92f7882c25134f63f19401204b37b4f6ea9e7209  codex/ask-then-do-it-1.3.1.zip
6e095478bb299d95d3b3f294161b7011a338e29ae9b07b0a4245b3d3d14e241b  generic/ask-then-do-it-generic-1.3.1.zip
```

`dist/checksums.sha256` contains exactly these two names and digests。Focused build contracts prove exact inventories、source/package parity、ZIP equivalence、two-clean-build byte reproducibility、checksum verification、current guide links、no Marketplace metadata inside packages，以及 no-Pillow source/package/archive boundary。

一次含多個 temp build 的 focused run 中，第一個 staged Codex install 在 50 次 retry 後仍遇到 `WinError 5`；同一 suite 的後續 builds 通過，該 test 隨即單獨串行重跑為 exit `0`; `Ran 1 test in 0.560s`; `OK`。之後 137-test focused suite 與兩次完整 212-test discovery 的所有 build paths 都通過。這保留為已知 external-lock residual risk，不視為未重現即消失的證據。

## Token proxy preservation

Command:

`& '.\.venv\Scripts\python.exe' 'scripts\measure_workflow_token_proxy.py' --fixture 'tests\release\fixtures\workflow-token-proxy\benchmark.json' --json`

Observed result: exit `0`; algorithm 仍為 `normalized-utf8-quarter-v1`，Full/Lite 分別 `14771`/`5480` proxy tokens，difference `9291`，reduction `62.90%` (`6290` basis points)，minimum threshold `6000`，gate passed。Generic composed prompt仍是 `15376` proxy tokens，且不宣稱 Generic 60% 或 billing guarantee。

13 個 fixture files 的固定 hashes 全部通過。衍生 fixture fingerprint 從 pre-change `06115845cc9d658ec86ec0e503ba214e55cb0725bc4c73f33769b24c9fd6d2e1` 變為 `e91e7986ac191539bfe54e97cef4807f505a145b4ac8ecc694ebee76ab492610`；Generic composed source SHA 同樣因 `1.3.0` -> `1.3.1` bytes 更新而改變。Fingerprint function、inputs inventory、fixture bytes、normalized lengths、token counts 與 threshold 均未修改。

## Broader verification

- Focused release/adapter/documentation/conformance command：exit `0`; `Ran 137 tests in 19.456s`; `OK`。
- Initial full discovery after source synchronization：`Ran 212 tests`; 11 subtest failures全部來自遺漏的 `tests/generic/test_generic_prompts.py` 仍要求 active prompt `1.3.0`；沒有 production behavior failure。同步該 current contract後，focused Generic prompt module為 `17/17`。
- Final full command：`& '.\.venv\Scripts\python.exe' -m unittest discover -s tests -p 'test_*.py'`。
- Final full result after evidence-gate strictness correction：exit `0`; `Ran 212 tests in 19.662s`; `OK`。
- Post-Review correction affected release contracts：exit `0`; `Ran 36 tests in 6.136s`; `OK`。
- Post-Review correction首次 full observation至少出現一個 failure marker，但 terminal session在 traceback回傳前結束；該次不計為 pass。下一次完整 diagnostic run執行 `215` tests，兩個 release-safety cases因真實 Windows `WinError 5` 超過既定4.9秒 retry window而失敗；builder均正確退出並還原 pre-build state，沒有 candidate corruption。
- 兩個受影響 release-safety cases隨即串行重跑：exit `0`; `Ran 2 tests in 4.984s`; `OK`。
- Final post-correction full discovery：exit `0`; `Ran 215 tests in 22.771s`; `OK`。測試數由 `212` 增為 `215`，來自三個 evidence regression methods；default `dist` gate併入既有 reproducibility method，沒有增加 test count或 builder invocation。
- Official Skill validation：skill-creator `quick_validate.py` 對 9 canonical + 9 packaged Skill roots，`18/18` valid。
- Official Plugin validation：plugin-creator `validate_plugin.py` 對 canonical 與 packaged Plugin，`2/2` passed。
- Marketplace：exit `0`; `Marketplace validation passed` for repository catalog pinned to `v1.3.1`。
- Conformance：Codex 與 Generic 分別 against Core `1.3.1`，兩者 exit `0`。
- Post-correction official rerun再次得到 Skill `18/18`、Plugin `2/2`、Marketplace passed、Codex/Generic conformance passed；Token proxy保持 Full `14771`、Lite `5480`、reduction `62.90%`、gate passed。
- Fail-closed probes：current config 配 historical `1.3.0` ledger/evidence 因 ledger version mismatch exit `1`；尚不存在的 `1.3.1` ledger/evidence 因 missing ledger exit `1`，符合 Ticket 3 尚未建立 final release evidence 的邊界。
- Active scan：release/Core/adapters/Plugin/Marketplace/scripts/current guides/root docs 無 `1.3.0` 或 `v1.3.0` identity；tests 中只剩固定 historical dictionary 與三個 frozen Token fixture files。
- Historical/frozen diff：43 個 `1.3.0` artifacts 與 Token fixture tree沒有 `git diff`；所有固定 SHA tests通過。
- `git diff --check`：exit `0`；只有既有 Git LF-to-CRLF warnings，沒有 whitespace error。
- Repository root沒有 `.dist-release-*` 或遺留 test temp directory。

## Refactor and scope inspection

版本同步只修改盤點出的 active/current owners，沒有 global replacement。Evidence parser 的兩個 regex 只解析 top-level line-shaped metadata；required-check loop 收斂成一致的 `status == passed` contract，未加入版本特判或新 config field。Package no-Pillow test重用既有 builder、exact inventory與ZIP equivalence boundary，沒有掃描 PNG bytes。

Final diff inspection found no Token algorithm/fixture/threshold edit、historical artifact edit、consumer runtime dependency、unmanaged `dist` output、network/publish operation、tag、push、release upload 或 Marketplace activation。

## Residual risk

- Windows external lock lasting beyond 4.9 seconds can still exhaust the approved retry window；本 Ticket實際觀測一次，後續串行 rerun、137 focused tests與最終 212 tests皆成功。Same-output concurrent builders仍不支援。
- Token report fingerprint是 active source-inclusive derived value；未來若只比較舊 SHA 而不理解 inputs，可能誤判合法 source update。Frozen fixture file hashes與不變 token counts提供獨立保護。
- Official validators證明 schema/frontmatter/manifest validity，不替代 Ticket 4 的 isolated CPython 3.12 final release validation、architecture diagnosis與 final independent Review。
- External publication全部未執行，`v1.3.1` URLs在未來另行授權發布前不會外部可用。
