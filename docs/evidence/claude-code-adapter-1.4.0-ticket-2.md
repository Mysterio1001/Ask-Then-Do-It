# Claude Code Adapter 1.4.0 Ticket 2 Implementation Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `claude-code-adapter-1-4-0-ticket-2-implementation`

Workflow ID: `claude-code-adapter`

Core version: `1.3.0`

Target release version: `1.4.0`

Ticket: `2 - 實作安全的 model router 與 session state`

Execution mode: `tdd` (`Add tests`, explicitly selected by the user)

Status: Completed

Inputs: Approved [Claude Code Adapter 1.4.0 Specification](../specs/claude-code-adapter-1.4.0.md)、Approved [Ticket Plan](../plans/claude-code-adapter-1.4.0.md) Ticket 2、Approved [Requirement Decision Record](../requirements/claude-code-adapter-1.4.0.md)、Approved and synchronized [Project Knowledge Base](../project/knowledge-base.md)、Completed Ticket 1 public Plugin boundary，以及 Ticket 3 已通過的 exact binary／Plugin／Marketplace strict-validation preflight evidence。

Assumptions: Exact Claude Code `2.1.251` 的 authenticated namespaced invocation、`UserPromptExpansion.command_name`、`additionalContext`可見性與host failure semantics仍未實測，因此這些邊界只稱為`provisional`／`simulated`。Requested switch 的pending match只使用Approved state schema可保存的generation、`from_model`與source；`PostModelSwitch.to_model`仍是authoritative destination。官方文件明示`PreModelSwitch` timeout會阻止switch；本實作只證明已捕捉的lock／state錯誤會快速回傳非阻斷warning，無法保證外部process hang。

Deferred: Ticket 3 authenticated live session ledger、General與Claude 5 profiles、profile module reload的具體module inventory、paired conformance、context proxy、三語文件、release builder、generated packages、clean live smoke，以及tag、push、GitHub Release、Marketplace activation等全部external publication actions。

Handoff: Fresh [Review after tenth corrections](claude-code-adapter-1.4.0-ticket-2-review-after-tenth-corrections.md)以`independent`標籤得到`Accepted - no actionable findings`，確認第十輪canonical-only與Node-before-state修正關閉前次2×P2，且Ticket 2 deterministic scope符合Approved `tdd` Plan。Ticket 2完成；依Approved sequencing，Tickets 4、5現在可在分離ownership下開始，Ticket 3 authenticated live ledger仍是local `1.4.0`完成前不可略過的hard gate。

Approval: Implementation authority comes from the Approved Ticket Plan、其Approved Ticket 2 `tdd` mode，以及使用者於2026-09-07先後明確回覆「核准」繼續Ticket 2、執行fresh Review所列3×P2／2×P3修正，並核准再修正Review after second corrections所列的generation exhaustion P2與explicit invalid-UTF-8 entry P3；使用者於2026-09-08另明確核准修正Review after third corrections所列的2×P2、Review after fourth corrections所列的1×P1／4×P2、Review after fifth corrections所列的ready-route Claude Code minimum-version P2、Review after sixth correction所列的2×P2、Review after seventh corrections所列的1×P1、Review after eighth correction所列的1×P1／1×P2，以及Review after ninth corrections所列的2×P2。第十輪明確選擇維持Approved Specification的canonical-only session JSON契約並移除sidecar，不擴張或修改Approved Specification。

## Outcome

- 新增零第三方runtime dependency的Node.js `22+` router、四個同步hooks及release-owned exact model mapping。
- `SessionStart`、`PreModelSwitch`、`PostModelSwitch`與兩個public entries使用SHA-256 session key、exact command identity、per-session lock及same-directory atomic replacement。
- 實作`ready`／`pending`／`indeterminate`、startup／resume／compact／clear／fork、operation-bound profile、30-day stale rejection與race-safe cleanup。
- Automatic與explicit `-5`完整區分known Claude 5、supported non-5、unsupported與valid unknown；只有explicit的valid `node-too-old` envelope可進manual fallback。
- Success與failure envelopes固定八欄及closed disclosure enums；raw session ID、prompt、arguments與paths不落盤、不進envelope。
- Runtime mapping以semantic SHA-256綁定30個exact IDs；任何alias、future substitution、classification swap、schema extension或mapping corruption都fail closed。
- Validator會拒絕async hook、alias mapping、Node gate移除／降級、Node gate前的stdin或`${CLAUDE_PLUGIN_DATA}` access、`.post-failure`等第二持久state path、未核准built-in、static／side-effect／dynamic／CommonJS third-party import及network API。
- Optional hook fields依官方Claude Code schema作exact type／closed-enum驗證；`effort.level`、`expansion_type`、`cache_ttl`與`pricing`不接受未知值，但完整合法payload保持相容。
- Mapping、state與lock record分別以64 KiB、16 KiB與1 KiB上限從固定大小Buffer讀取，使用fatal UTF-8 decoder，檔案在讀取期間成長也會fail closed。
- Session lock使用owner token、PID、lease與grace；只有已過期且owner process已死亡的完整record可回收。Lock先完整寫入same-directory prepared file，再以hard link原子發布；release只移除同owner token，並行reclaimer不會同時取得ownership。`PreModelSwitch`仍維持no-wait且不執行回收。
- Resume／compact若保留既有operation但active model已成為unsupported，會保留binding並明確揭露已離開formal support。
- Source-trace validator逐canonical ID確認被引用snapshot確實包含該model ID及相符active／retired狀態，不再只驗證ref名稱與snapshot hash。
- Router不再依賴Node 18／19缺少的`String.prototype.isWellFormed()`；舊runtime仍能把valid explicit `-5`事件正確標為`node-too-old`，不誤報`internal-error`。
- Stdin在JSON parsing前使用fatal UTF-8 decoder；不同非法raw bytes不會被替換成同一個U+FFFD session identity或建立共享state。
- 最後一次成功回收stale lock後必須重新原子取得完整owned lock才可執行callback；若被其他contender搶先取得則fail closed。
- 所有generation increment先檢查`Number.MAX_SAFE_INTEGER`上限；SessionStart、requested Pre與automatic／resume Post不會寫出自己下一次會拒絕的unsafe state。
- Model evidence validator把canonical mapping path、evidence date、source ID inventory、URL／date與exact integer schema version綁回runtime mapping，不能由任意自造snapshot自我證明。
- Resume或automatic／resume Post遇generation exhaustion時，會在同一session lock內把既有state轉為`indeterminate`並保留operation binding；下一個public entry必定fail closed，不能再沿用舊`ready` classification。
- 兩個`UserPromptExpansion` hooks各自傳入固定、可信的command identity；router在讀取untrusted stdin前即決定failure-envelope entry，成功parse後再要求raw `command_name`與可信identity完全一致。Malformed JSON或非法UTF-8不會被部分解析或猜測入口。
- `model_id`與`pending_switch.from_model`只接受release-owned exact mapping ID，或受限於官方model family與純數字版本形狀的undated future correlation ID；後者永遠只分類為`unknown`，但可安全完成requested Pre／Post配對。Dated future、custom／tenant／regex-shaped secret仍只形成`null`與`unknown`，不持久化raw ID；無法建立可信correlation的requested Pre會在不阻止switch下把state標為`indeterminate`。
- Explicit `node-too-old` envelope與missing-envelope／Node-missing兩條manual paths都必須先由available host command獨立證明Claude Code `2.1.251+`；已知過舊或無法證明時停止且不載入Claude 5 profile。Validator以核准bootstrap全文固定此gate。
- Canonical requested Pre的`from_model`與ready state不一致時，先原子提交保留operation binding的`indeterminate` state再回傳非阻斷warning；下一個public entry不能沿用stale classification。
- 三個non-`none` ready disclosure codes都在profile載入前要求明確告知使用者compatibility／無法驗證／fallback結果；successful Post context則要求告知active model已改變、routing state已同步、current operation profile不變且只有下一個permitted public entry重新路由，且不包含raw model ID。
- Same-session `clear`會讀取valid prior generation並嚴格遞增，同時清除model、pending switch與operation authority；stale但schema-valid prior state也只用於安全遞增，不把舊authority帶回來。
- 兩個public entry在接受任何ready route後、執行揭露或載入profile前，都必須以固定`claude --version` host command獨立證明Claude Code `2.1.251+`；`2.1.250`以下、command失敗、輸出缺失／malformed或版本無法證明時一律停止且不載入profile。Canonical validator固定完整bootstrap contract。
- `checkNodeVersion(process.versions.node)`在stdin、`${CLAUDE_PLUGIN_DATA}`、state path及任何持久讀寫之前執行。Node `<22`的四個actions都不建立或修改Plugin data；`UserPromptExpansion`仍以hook argv的可信command identity輸出正確entry之`node-too-old` envelope，Pre／Post則維持exit `0`且只輸出非阻斷warning。
- Post只使用Approved canonical session JSON。Node gate通過且可安全定位session後，router在same-session lock內讀取既有state並先原子提交保留operation與generation的`indeterminate` state，再驗證完整event、mapping、state與transition；成功時在同一lock內提交authoritative `ready` state。可定位Post的後續驗證失敗因此使兩個public entries都以`state-indeterminate`停止，且production沒有`.post-failure` sidecar或任何第二持久routing authority。
- `compact`使用raw event的model presence區分「真的省略」與「有值但不可持久化／分類」；pending或indeterminate state收到present custom／unmapped model時，會遞增generation、保留原operation、清除pending並重建`ready`／`unknown`，同時不落盤或輸出raw model ID。只有真正model-omitted compact才受舊non-ready state阻擋。
- Valid undated future family ID（例如`claude-sonnet-6`）在classification上仍是`unknown`且不會被猜成Claude 5，但可在state內保留為canonical transition correlation，使command／picker／sdk requested switch能進入pending並由matching Post提交known或unknown target。Model-visible output仍不回顯該ID。

## Files changed

- `adapters/claude-code/plugin/ask-then-do-it/hooks/hooks.json`
- `adapters/claude-code/plugin/ask-then-do-it/scripts/router.mjs`
- `adapters/claude-code/plugin/ask-then-do-it/config/model-classifications.json`
- `adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md`
- `adapters/claude-code/plugin/ask-then-do-it/skills/ask-then-do-it-5/SKILL.md`
- `scripts/validate_claude_plugin.py`
- `scripts/validate_claude_model_evidence.py`
- `tests/claude/test_router_contract.py`
- `tests/claude/test_router_review_regressions.py`
- `tests/claude/test_router_schema_validation.py`
- `tests/claude/test_router_state.py`
- `tests/claude/test_router_security.py`
- `tests/claude/test_model_classification_evidence.py`
- `tests/claude/test_public_plugin_contract.py`
- `tests/claude/fixtures/model-classifications/`
- 本Implementation Evidence。

## Red evidence

第一個vertical-slice Red：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.claude.test_router_contract.ClaudeRouterContractTests.test_two_sessions_route_independently -v
```

Observed: production router尚不存在，測試因missing approved behavior失敗；不是test setup failure。後續先後觀察到explicit route、lifecycle／switch、duplicate keys、unknown fields、cleanup、concurrency、hooks、Skill envelope union、official source trace與Node pure gate的預期Red。

安全與schema補強Red：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.claude.test_router_contract.ClaudeRouterContractTests.test_node_21_failure_envelope_preserves_the_explicit_entry_identity tests.claude.test_router_security.ClaudeRouterSecurityTests.test_invalid_model_identifiers_and_operation_tuples_are_rejected tests.claude.test_router_security.ClaudeRouterSecurityTests.test_stale_same_session_state_is_not_routed_or_resumed tests.claude.test_model_classification_evidence.ClaudeModelClassificationEvidenceTests.test_runtime_mapping_loader_rejects_schema_extensions tests.claude.test_public_plugin_contract.ClaudePublicPluginContractTests.test_validator_rejects_runtime_contract_mutations -v
```

Observed: exit `1`; `Ran 5 tests`; `FAILED (failures=11)`。Failures精確命中Node 21 explicit envelope誤標automatic entry、三種invalid model IDs、兩種illegal operation tuples、stale same-session route、三種runtime mapping drift與dynamic third-party import繞過。

第二批lifecycle／race Red：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.claude.test_router_contract.ClaudeRouterContractTests.test_explicit_entry_identity_is_preserved_for_state_failures tests.claude.test_router_security.ClaudeRouterSecurityTests.test_state_schema_corruption_and_ownership_mismatch_are_rejected tests.claude.test_router_security.ClaudeRouterSecurityTests.test_cleanup_does_not_delete_a_session_while_its_lock_is_held tests.claude.test_router_state.ClaudeRouterStateTests.test_requested_switch_can_recover_from_valid_unknown_startup_model tests.claude.test_router_state.ClaudeRouterStateTests.test_pre_switch_lock_contention_returns_before_the_blocking_timeout -v
```

Observed: exit `1`; `Ran 5 tests`; `FAILED (failures=5)`。Failures精確命中malformed explicit event identity、invalid calendar timestamp、cleanup/delete race、omitted-model requested switch，以及Pre hook在held lock上超過2秒blocking timeout的風險。

Mapping exact-freeze Red另以同一runtime loader test觀察`canonical-id-substitution`與`classification-swap`兩個subtests被舊loader錯誤接受；加入semantic freeze前結果為`FAILED (failures=2)`。

Independent Review findings核准修正後，另建立三批明確Red：

```powershell
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_router_schema_validation -v
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_router_review_regressions -v
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_model_classification_evidence.ClaudeModelClassificationEvidenceTests.test_source_trace_validator_rejects_wrong_refs_and_deleted_supporting_rows -v
```

Observed before production fixes：schema批次`Ran 9 tests`並產生18個預期failure；review-regression初始7 tests中6個預期failure，精確命中unbounded mapping/state reads、growing-file race、孤兒lock無法回收與resume／compact缺unsupported disclosure；source-trace mutation因缺少逐record validator而產生1個預期failure。這些是缺少目標行為造成的Red，不是test setup failure。

Fresh Final Review 的3×P2／2×P3獲核准後，先新增8個test methods、共13個明確失敗情境：

```powershell
.\.venv\Scripts\python.exe -m unittest -v tests.claude.test_router_review_regressions.ClaudeRouterReviewRegressionTests.test_last_attempt_stale_recovery_reacquires_owned_lock_before_callback tests.claude.test_router_review_regressions.ClaudeRouterReviewRegressionTests.test_stdin_rejects_replacement_colliding_invalid_utf8_session_ids
.\.venv\Scripts\python.exe -m unittest -v tests.claude.test_router_contract.ClaudeRouterContractTests.test_node_18_and_19_api_surface_preserves_explicit_node_too_old_failure tests.claude.test_router_state.ClaudeRouterStateTests.test_session_start_does_not_overflow_maximum_safe_generation tests.claude.test_router_state.ClaudeRouterStateTests.test_requested_pre_switch_does_not_write_unsafe_next_generation tests.claude.test_router_state.ClaudeRouterStateTests.test_automatic_post_switch_sources_do_not_overflow_maximum_safe_generation
.\.venv\Scripts\python.exe -m unittest -v tests.claude.test_model_classification_evidence.ClaudeModelClassificationEvidenceTests.test_source_trace_validator_rejects_metadata_drift_from_mapping tests.claude.test_model_classification_evidence.ClaudeModelClassificationEvidenceTests.test_source_trace_validator_rejects_boolean_schema_version
```

Observed before production fixes：第一批`Ran 2 tests in 0.467s`、`FAILED (failures=2)`，證實callback時無完整owned lock、另一contender可進入，以及raw `0xFF`／`0xFE`共用同一replacement-derivedstate key。第二批`Ran 4 tests in 1.107s`、`FAILED (failures=6)`，精確命中Node 18／19誤報與SessionStart／Pre／兩種Post source的unsafe generation。第三批`Ran 2 tests in 0.952s`、`FAILED (failures=5)`，精確命中mapping path、source inventory、URL、date與boolean schema version drift。所有failure皆為缺少目標行為，不是test setup或hash mismatch。

Review after second corrections的1×P2／1×P3獲核准後，建立第三輪Red：

```powershell
.\.venv\Scripts\python.exe -B -m unittest -v tests.claude.test_router_state.ClaudeRouterStateTests.test_resume_generation_exhaustion_fails_closed tests.claude.test_router_state.ClaudeRouterStateTests.test_automatic_post_switch_generation_exhaustion_fails_closed
.\.venv\Scripts\python.exe -B -m unittest -v tests.claude.test_router_review_regressions.ClaudeRouterReviewRegressionTests.test_invalid_utf8_explicit_expansion_preserves_explicit_entry
```

Observed before production fixes：generation批次`Ran 2 tests`、`FAILED (failures=3)`；Resume與Post `source=auto|resume`三個情境在下一個entry都實際得到`routing_status=ready`而非預期的`failure`。Explicit invalid-UTF-8批次`Ran 1 test`、`FAILED (failures=1)`；failure envelope其餘欄位均正確，但`entry`實際誤標`/ask-then-do-it:ask-then-do-it`而非`/ask-then-do-it:ask-then-do-it-5`。兩批皆精確命中missing behavior，且未建立state pollution。

Review after third corrections的2×P2獲核准後，建立第四輪Red：

```powershell
.\.venv\Scripts\python.exe -B -m unittest -v tests.claude.test_router_security.ClaudeRouterSecurityTests.test_noncanonical_session_start_model_is_unknown_without_secret_persistence tests.claude.test_router_security.ClaudeRouterSecurityTests.test_noncanonical_pre_switch_from_model_fails_closed_without_secret_persistence tests.claude.test_router_security.ClaudeRouterSecurityTests.test_noncanonical_post_switch_to_model_is_unknown_without_secret_persistence tests.claude.test_router_security.ClaudeRouterSecurityTests.test_unmapped_canonical_future_model_id_remains_unknown
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_public_plugin_contract.ClaudePublicPluginContractTests.test_explicit_node_too_old_fallback_requires_supported_claude_code -v
```

Observed before production fixes：model persistence批次exit `1`、`Ran 4 tests in 1.202s`、`FAILED (failures=3)`；SessionStart marker實際出現在`model_id`、Pre marker出現在`pending_switch.from_model`且state為`pending`、Post marker出現在`model_id`，所有captured model-visible output均未含marker；unmapped canonical future ID control case通過並維持unknown/general。Manual fallback批次exit `1`、`Ran 1 test`、`FAILED (failures=1)`；valid `node-too-old` paragraph在載入optimized profile前缺少Claude Code minimum version proof。兩批皆為精確missing behavior Red，不是setup failure。

Review after fourth corrections的1×P1／4×P2獲核准後，建立第五輪Red：

```powershell
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_router_security.ClaudeRouterSecurityTests.test_unmapped_regex_shaped_session_start_model_is_unknown_without_secret_persistence tests.claude.test_router_security.ClaudeRouterSecurityTests.test_unmapped_regex_shaped_pre_switch_from_model_fails_closed_without_secret_persistence tests.claude.test_router_security.ClaudeRouterSecurityTests.test_unmapped_regex_shaped_post_switch_to_model_is_unknown_without_secret_persistence tests.claude.test_router_security.ClaudeRouterSecurityTests.test_unmapped_canonical_future_model_id_remains_unknown tests.claude.test_router_security.ClaudeRouterSecurityTests.test_release_allowlisted_model_ids_are_persisted_and_classified -v
.\.venv\Scripts\python.exe -B -m unittest -v tests.claude.test_router_state.ClaudeRouterStateTests.test_mismatched_requested_pre_switch_becomes_indeterminate_without_blocking tests.claude.test_router_state.ClaudeRouterStateTests.test_successful_post_switch_context_requires_complete_user_notification tests.claude.test_router_state.ClaudeRouterStateTests.test_same_session_clear_strictly_increments_generation_and_clears_authority
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_public_plugin_contract.ClaudePublicPluginContractTests.test_ready_route_disclosures_are_user_visible_before_profile_loading -v
```

Observed before production fixes：allowlisted-state批次exit `1`、`Ran 5 tests`、`FAILED (failures=4)`；三個regex-shaped marker與future-looking ID都實際進入state，allowlisted classification control通過。State lifecycle批次`Ran 3 tests in 1.557s`、`FAILED (failures=4)`；Pre mismatch後實際仍為`ready`，requested／automatic Post contexts都缺`tell the user`，clear generation實際`1 → 0`而非`2`。Ready-disclosure批次exit `1`、`Ran 1 test`、`FAILED (failures=3)`；automatic unknown、explicit unknown與explicit non-5三個subtests均找不到profile載入前的使用者揭露動作。所有failure均精確命中review triggers，不是setup failure。

Review after fifth corrections的1×P2獲核准後，建立第六輪Red：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.claude.test_public_plugin_contract.ClaudePublicPluginContractTests.test_ready_routes_prove_supported_claude_code_before_profile_loading
```

Observed before production fixes：exit `1`；`Ran 1 test`；`FAILED (failures=2)`。Automatic與explicit兩個subtests都因ready-envelope validation後、route disclosure／profile loading前找不到固定`claude --version` proof而失敗。這是bootstrap instruction contract的deterministic static Red，明確固定`2.1.250`停止、`2.1.251`可繼續及版本無法證明時fail closed；不是authenticated old-host observation，也不是setup failure。

Review after sixth correction的2×P2獲核准後，建立第七輪Red：

以下第七至九輪的fence／sidecar命令與結果是當時實際觀察的歷史TDD evidence；該持久sidecar設計已被第十輪canonical-only correction移除，不代表current runtime contract。

```powershell
.\.venv\Scripts\python.exe -B -m unittest -v tests.claude.test_router_state.ClaudeRouterStateTests.test_automatic_post_failure_fence_survives_unlock_and_omitted_compact tests.claude.test_router_state.ClaudeRouterStateTests.test_valid_unmapped_canonical_current_model_can_complete_requested_switch tests.claude.test_router_state.ClaudeRouterStateTests.test_requested_switch_to_valid_unmapped_canonical_target_stays_unknown
```

Observed before production fixes：exit `1`；`Ran 3 tests in 11.509s`；`FAILED (failures=6)`。Automatic／resume Post遭deterministic lock failure後雖輸出non-blocking warning，解除lock後next route與omitted compact實際仍沿用舊`ready` classification；`claude-sonnet-6` initial route雖正確為unknown/general，但command／picker／sdk Pre均實際轉為`indeterminate`而非`pending`，且known→future Post只留下`null` model ID。另跑既有Pre lock與unsafe custom-marker兩項guard tests皆通過，證明Red不是setup failure且沒有弱化privacy boundary。

為固定safe recovery semantics，另在production調整前把`clear` recovery加入同一fence test；當時該subtest實際得到`failure`而非預期的valid unknown，形成1個追加Red。這確保model-omitted compact不能解除fence，但explicit clear可以安全清除舊authority並重建unknown state。

Review after seventh corrections的1×P1獲核准後，建立第八輪Red：

Public path redaction（2026-09-09）：下方 `<python>` 代表當時使用的 Python executable；僅隱去本機使用者路徑，原測試與結果不變。

```powershell
& <python> -m unittest tests.claude.test_router_schema_validation.ClaudeRouterSchemaValidationTests.test_locatable_post_schema_failure_fences_both_public_entries -v
```

Observed before production fix：exit `1`；`Ran 1 test in 0.353s`；`FAILED (failures=2)`。Automatic與explicit兩個subtests都在valid session的Post optional `pricing: dynamic` schema failure後實際得到`routing_status: ready`而非`failure`，同時確認Post仍exit `0`、只輸出non-blocking warning且舊state bytes不被改寫。這精確證明fence建立點晚於完整schema validation，不是setup failure。

在Green code trace中另發現successful Post原本於session lock釋放後才清除fence，可能與另一個較晚失敗的Post交錯，因此先加入lock-boundary Red：

```powershell
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_router_review_regressions.ClaudeRouterReviewRegressionTests.test_successful_post_clears_failure_fence_while_session_lock_is_owned -v
```

Observed before production fix：exit `1`；`Ran 1 test in 0.001s`；`FAILED (failures=1)`，clear位置實際在session lock boundary之後。這個deterministic contract固定「successful Post只有在仍持有same-session lock時才可清除fence」，避免unlock後的並行清除競爭窗。

Review after eighth correction的1×P1／1×P2獲核准後，建立第九輪Red：

```powershell
.\.venv\Scripts\python.exe -B -m unittest tests.claude.test_router_security.ClaudeRouterSecurityTests.test_nonregular_post_failure_fence_blocks_both_public_entries tests.claude.test_router_state.ClaudeRouterStateTests.test_compact_with_present_unmapped_model_recovers_nonready_state_as_unknown -v
```

Observed before production fixes：exit `1`；`Ran 2 tests in 1.399s`；`FAILED (failures=4)`。Directory占用precise Post fence final path時，automatic與explicit兩個subtests都在Post warning後實際取得`ready`而非`failure`；pending與indeterminate兩個compact subtests則都保留原non-ready status，沒有重建`ready`／`unknown`。四個failure逐一命中Review triggers，且Post／SessionStart subprocess均exit `0`，不是setup failure。

Review after ninth corrections的2×P2獲核准後，建立第十輪canonical-only與Node-gate Red。Canonical批次先鎖定只有canonical session JSON可作持久authority、可定位Post必須在同一lock內先提交`indeterminate`再嘗試完整驗證／authoritative commit，以及production不得含sidecar：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.claude.test_router_schema_validation.ClaudeRouterSchemaValidationTests.test_locatable_invalid_post_schema_writes_only_canonical_indeterminate_state tests.claude.test_router_review_regressions.ClaudeRouterReviewRegressionTests.test_post_precommit_indeterminate_and_successful_commit_share_session_lock tests.claude.test_router_state.ClaudeRouterStateTests.test_post_failure_recovers_without_secondary_persistent_state tests.claude.test_router_security.ClaudeRouterSecurityTests.test_router_declares_no_secondary_durable_post_state_path
```

Observed before production fixes：`Ran 4 tests in 1.910s`；`FAILED (failures=7)`。Failures精確命中sidecar仍是第二持久authority、invalid Post未只寫canonical `indeterminate` state，以及Post precommit／success commit沒有共用核准的locked canonical transaction；不是setup failure。

Node gate批次同時要求Node `<22`的四個actions不建立或修改Plugin data、explicit expansion保留正確`node-too-old` entry envelope、Pre／Post維持非阻斷warning，且validator拒絕gate前Plugin-data access：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.claude.test_router_contract.ClaudeRouterContractTests.test_node_21_gate_precedes_plugin_data_access_for_all_actions tests.claude.test_public_plugin_contract.ClaudePublicPluginContractTests.test_validator_rejects_runtime_contract_mutations
```

Observed before production fixes：`Ran 2 tests in 5.566s`；`FAILED (failures=2)`。Post在Node `21.9.0`仍建立Plugin data，且validator錯誤接受gate前`${CLAUDE_PLUGIN_DATA}` access；其他action、explicit envelope與Pre／Post warning assertions已到達預期邊界。兩個failure均為缺少目標行為，不是setup failure。

## Focused Green and refactor

上述各批focused commands在最小production changes後均exit `0`。Final lifecycle／race focused result：

```text
Ran 5 tests in 1.902s
OK
```

Final expanded boundary focused result：

```text
Ran 6 tests in 11.089s
OK
```

Review修正後的三批focused Green：

```text
Schema validation: Ran 9 tests in 6.773s; OK
Review regressions: Ran 10 tests in 11.329s; OK
Model evidence: Ran 4 tests in 0.720s; OK
```

Fresh Final Review correction的三批focused Green：

```text
Lock ownership + fatal UTF-8: Ran 2 tests in 0.325s; OK
Node-old surface + generation boundaries: Ran 4 tests in 1.334s; OK
Evidence metadata/schema binding: Ran 2 tests in 0.680s; OK
```

第三輪correction focused Green：

```text
Generation exhaustion fail-closed: Ran 2 tests in 1.174s; OK
Explicit invalid-UTF-8 entry identity: Ran 1 test in 0.095s; OK
Trusted hook command identity contract: Ran 1 test in 0.000s; OK
```

第四輪correction focused Green：

```text
Canonical-or-null persistence and future canonical control: Ran 4 tests in 1.214s; OK
Explicit node-too-old Claude Code version gate: Ran 1 test in 0.001s; OK
Router/state/security/public adjacent regression: Ran 44 tests in 32.479s; OK (skipped=1)
```

第五輪correction focused Green：

```text
Allowlisted-only persistence with unknown-route controls: Ran 5 tests in 1.476s; OK
Pre mismatch, Post notice, and monotonic clear: Ran 3 tests in 1.728s; OK
Three ready-route user disclosures plus canonical validator: Ran 1 test in 0.100s; OK
Router/state/security/review/public adjacent regression: Ran 62 tests in 48.372s; OK (skipped=1)
```

第六輪correction focused Green：

```text
Ready-route Claude Code minimum-version gate: Ran 1 test in 0.001s; OK
Public Plugin contract module: Ran 11 tests in 11.773s; OK
Canonical Claude Plugin validator: passed
```

第七輪correction focused Green：

以下第七至九輪sidecar Green只保存當時已執行結果，已被第十輪canonical-only設計取代，不作current acceptance evidence：

```text
Durable Post fence + valid future correlation: Ran 3 tests in 14.087s; OK
Focused new/legacy privacy guards: Ran 7 tests in 13.131s; OK
Router/state/security/review/public adjacent regression: Ran 66 tests in 66.936s; OK (skipped=1)
```

第八輪correction focused Green：

```text
Early Post schema fence: Ran 1 test in 0.396s; OK
Early fence + lock-boundary + recovery: Ran 3 tests in 12.739s; OK
```

第九輪correction focused Green／refactor verification：

```text
Non-regular fence + present-unmapped compact recovery: Ran 2 tests in 1.888s; OK
After stronger disclosure/privacy assertions: Ran 2 tests in 1.970s; OK
Narrow adjacent failure-path audit: Ran 5 tests in 14.101s; OK; no actionable finding
```

第十輪correction focused Green：

```text
Canonical-only Post, Node gate, validator and adjacent guards: Ran 7 tests in 7.676s; OK
```

首次六模組相鄰驗證另揭露一項過時test expectation：

```text
Router/state/security/review/public adjacent modules: Ran 79 tests in 63.004s; FAILED (failures=3)
```

三個failure都來自既有security test仍要求invalid Post保留舊`ready` bytes，與本輪核准的canonical `indeterminate`行為矛盾；這不是production regression。把該test更新為要求唯一canonical JSON進入`indeterminate`且兩entries fail closed後，focused test `Ran 1 test in 1.322s`; `OK`。六模組隨後重跑`Ran 79 tests in 62.000s`; `OK (skipped=1)`。

Refactor後仍將input validation、mapping validation、state validation、route tuples、closed disclosure sets、lock policy與atomic I/O維持在單一dependency-free router內；Pre lock採no-wait以避免已知lock contention跨越blocking timeout。正常route lock保留bounded retry，只回收過期、完整且已確認owner process死亡的lock；prepared-file＋hard-link publish與owner-token release關閉partial record、ABA release及並行回收競爭。Cleanup保持在current-session lock之外，candidate session使用no-wait exclusive lock，避免cross-session deadlock與刪除剛更新state。第十輪移除所有production sidecar；Post在Node gate後以同一session lock內的canonical `indeterminate` precommit與authoritative `ready` commit取代第二持久authority，validator則固定Node gate先於stdin／Plugin-data access並保留sidecar negative guard。`modelWasOmitted`仍是compact recovery的domain signal。未拆分router、修改Approved Specification或擴張approved behavior。

## Broader verification

Claude-focused suite：

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests\claude -p 'test_*.py' -v
```

Observed after the tenth correction: exit `0`; `Ran 106 tests in 71.723s`; `OK (skipped=1)`。唯一skip是Windows未授予建立檔案symlink的權限；同一suite的真實directory junction防護測試通過。

Full repository suite：

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p 'test_*.py'
```

Observed after all tenth-round final test assertions: exit `0`; `Ran 322 tests in 91.296s`; `OK (skipped=1)`。Skip與上述相同。先前第八、九輪full-suite結果仍是歷史evidence，但不作current candidate驗證。

Non-test validation：

```powershell
node --check adapters\claude-code\plugin\ask-then-do-it\scripts\router.mjs
.\.venv\Scripts\python.exe scripts\validate_claude_plugin.py
.\.venv\Scripts\python.exe scripts\validate_claude_model_evidence.py --mapping adapters\claude-code\plugin\ask-then-do-it\config\model-classifications.json --trace tests\claude\fixtures\model-classifications\source-trace.json
git diff --check
```

Observed against the tenth-round final files: 四者皆exit `0`；Node syntax無輸出；Claude Plugin validator回報`Claude Plugin validation passed`，model evidence validator回報`Claude model classification evidence is valid.`；diff check只有既有`docs/project/knowledge-base.md` LF→CRLF warning。Production adapter中的sidecar references為`0`；validator與tests仍保留負向sidecar guard。六個router/state/security/review/public adjacent modules最終重跑：`Ran 79 tests in 62.000s`；`OK (skipped=1)`。

Exact Claude Code `2.1.251` strict validation：

```powershell
.\.ticket3-preflight\claude-code-2.1.251\claude.exe --version
.\.ticket3-preflight\claude-code-2.1.251\claude.exe plugin validate adapters\claude-code\plugin\ask-then-do-it --strict
.\.ticket3-preflight\claude-code-2.1.251\claude.exe plugin validate . --strict
```

Observed against the tenth-round final files: binary version、Plugin strict validation與repository Marketplace strict validation皆exit `0`且無warning；binary回報`2.1.251 (Claude Code)`，兩項validation均顯示`Validation passed`。使用一次性OS-temp `CLAUDE_CONFIG_DIR`並停用autoupdate／nonessential traffic／telemetry；未登入、未安裝或啟用Marketplace，temp config已清除。這只證明native strict schema；不冒稱authenticated command invocation或route context已實測。

## Independent Review correction closure

先前 [Independent Review](claude-code-adapter-1.4.0-ticket-2-review.md) 的三個P2與一個可直接修正的P3 evidence gap已逐項處理：

- P2 orphan lock：以owner-token／PID／lease／grace、dead-process確認、prepared-file＋hard-link atomic publish與race tests修正；fresh／live／malformed locks均不回收，Pre hook仍立即返回。
- P2 resume／compact disclosure：保留operation/profile binding，同時揭露unsupported active model。
- P2 unbounded state read：state 16 KiB；同一bounded reader亦套用mapping 64 KiB與lock 1 KiB，並測試讀取期間成長。
- P3 source trace：新增獨立CLI validator與wrong-ref／deleted-row mutation tests，逐筆驗證來源內容支持model record。

Review另提出的Large Module／Divergent Change只授權診斷，沒有在本Ticket順手拆檔。Draft [Architecture Improvement Report](claude-code-adapter-1.4.0-ticket-2-architecture-diagnosis.md)記錄A1–A5與後續proposal；若使用者日後接受任何架構改善，必須回到Specification／Ticket Plan，不能由本Evidence直接授權實作。

Fresh [Final Independent Review](claude-code-adapter-1.4.0-ticket-2-review-final.md)目前仍保存當時的`changes-requested` verdict；其3×P2／2×P3 correction targets本輪處理如下，是否關閉仍交給下一個fresh reviewer判定：

- 最後attempt stale recovery：回收後立即以新token重新取得lock；reacquire競爭失敗時不執行callback。
- Invalid stdin UTF-8：在parse/hash前fatal decode，拒絕replacement collision且零state write。
- Node 18／19 API surface：以portable UTF-16 surrogate validation取代缺少的prototype API，保留valid explicit `node-too-old` envelope。
- Source metadata/schema：canonical path、date、source inventory、URL/date與mapping逐欄一致；schema version拒絕Python boolean。
- Generation upper bound：三種increment paths共用checked helper；requested Pre到達safe上限時維持非阻斷且不寫unsafe state，Resume與automatic／resume Post則在同一lock內提交`indeterminate`並保留operation binding，使下一entry fail closed。

Fresh [Review after second corrections](claude-code-adapter-1.4.0-ticket-2-review-after-second-corrections.md)的1×P2／1×P3 correction targets已完成實作與驗證，是否正式關閉仍交給下一個fresh reviewer判定：

- Resume與automatic／resume Post generation exhaustion：在lock內提交保留operation的`indeterminate` state，使下一entry fail closed；requested Pre仍維持非阻斷且不寫unsafe generation。
- Explicit invalid-UTF-8 entry：兩個hooks以固定argv傳入可信command identity，failure envelope不依賴untrusted stdin；parse成功後仍拒絕identity mismatch。

Fresh [Review after third corrections](claude-code-adapter-1.4.0-ticket-2-review-after-third-corrections.md)的2×P2 correction targets已完成實作與驗證，是否正式關閉仍交給下一個fresh reviewer判定：

- Noncanonical model persistence：共用canonical syntax boundary約束持久state；SessionStart／Post noncanonical值只形成`null`／unknown，Pre noncanonical source清除不可信model state並標`indeterminate`，custom marker不進state或output；canonical future ID仍可作unmapped unknown。
- Explicit manual fallback version gate：valid `node-too-old` envelope也必須在載入profile前另證Claude Code `2.1.251+`，與missing-envelope path一致；validator與negative contract test同步固定。

Fresh [Review after fourth corrections](claude-code-adapter-1.4.0-ticket-2-review-after-fourth-corrections.md)的1×P1／4×P2 correction targets已完成實作與驗證，是否正式關閉仍交給下一個fresh reviewer判定：

- Regex-shaped secret／PII persistence：持久化邊界先收斂為release mapping；第七輪只對官方family＋純數字版本形狀的undated future ID開放transition correlation，dated future、custom／tenant／regex-shaped secret仍不保存raw ID。所有unmapped classification仍固定為unknown，無法證明source時Pre fail closed。
- Canonical Pre mismatch：在lock內提交保留operation的`indeterminate` state；warning仍不deny或改寫model switch。
- Ready disclosures：automatic unknown、explicit unknown、explicit non-5三條route均要求在profile載入前做使用者可見揭露，並由canonical validator鎖定。
- Successful Post notification：requested／automatic及supported／unknown paths的context均要求完整通知同步與下一入口邊界，不回顯raw model ID。
- Monotonic clear：same-session clear從prior generation嚴格遞增並清除所有model／operation authority；既有stale-clear斷言同步改為monotonic contract。

Fresh [Review after fifth corrections](claude-code-adapter-1.4.0-ticket-2-review-after-fifth-corrections.md)的1×P2 correction target已完成實作與驗證，是否正式關閉仍交給下一個fresh reviewer判定：

- Ready-route minimum version：兩個canonical bootstrap在驗證ready envelope後、執行任何route result／disclosure／profile instruction前，以固定`claude --version`命令要求Claude Code `2.1.251+` proof；`2.1.250`以下、command失敗、輸出缺失／malformed或無法證明時停止且不載入profile。Static TDD contract與canonical validator同步固定順序、threshold及fail-closed行為。

Fresh [Review after sixth correction](claude-code-adapter-1.4.0-ticket-2-review-after-sixth-correction.md)確認上述version gate已關閉並提出下列2×P2。Valid future correlation仍是current behavior；當時的sidecar correction只保留為歷史evidence，已由第十輪canonical-only設計取代：

- Automatic／resume Post commit failure：第七輪曾以fixed-content same-session fence實作；該第二持久authority已於第十輪移除，現行行為改由唯一canonical session JSON的locked `indeterminate` precommit fail closed。
- Valid unmapped canonical model switch：受限undated future family ID可保留為unknown correlation，command／picker／sdk Pre建立pending，matching Post可提交known或unknown target；custom／tenant／dated future persistence guards仍通過。

Fresh [Review after seventh corrections](claude-code-adapter-1.4.0-ticket-2-review-after-seventh-corrections.md)提出的1×P1曾於第八輪以early fence處理；該實作同樣已被第十輪canonical-only設計取代：

- 可安全定位且已有canonical state的Post，現在在Node gate之後取得same-session lock，先以同一canonical JSON提交`indeterminate`，再執行完整`validateEvent()`、mapping／state驗證及authoritative commit；invalid optional schema failure後兩個entries均回傳`state-indeterminate`且不建立新operation。Successful Post的`indeterminate` precommit與`ready` commit屬於同一locked transaction，不再有fence clear競爭。

Fresh [Review after eighth correction](claude-code-adapter-1.4.0-ticket-2-review-after-eighth-correction.md)提出的1×P1 sidecar-hardening只保留為已取代的歷史evidence；其1×P2 compact correction仍是current behavior：

- Non-regular Post fence：第九輪曾加固此secondary path；第十輪已完全移除production sidecar，validator與tests改為負向拒絕任何`.post-failure`或第二持久state path。
- Present-unmapped compact：以raw `modelWasOmitted`區分省略與present值；pending／indeterminate收到schema-valid custom model時會重建`ready`／`unknown`、generation加一、pending清除並保留operation，且raw model不落盤或輸出。

Fresh [Review after ninth corrections](claude-code-adapter-1.4.0-ticket-2-review-after-ninth-corrections.md)提出的2×P2已完成第十輪TDD修正與完整驗證，是否正式關閉仍交給下一個fresh independent reviewer判定：

- Canonical-only persistent state：所有production `.post-failure` sidecar及其建立／讀取／清除流程已移除；可定位Post只透過Approved canonical session JSON，在同一lock內先提交保留operation／generation的`indeterminate`，驗證成功才提交`ready`。Production adapters sidecar references為`0`，validator與tests保留negative guard。
- Node-before-state boundary：Node `22+` gate現在先於stdin、`${CLAUDE_PLUGIN_DATA}`、state path與任何persistent access；Node `<22`四actions零Plugin-data mutation，explicit expansion仍輸出正確entry的`node-too-old` envelope，Pre／Post仍是exit-0非阻斷warning。Validator mutation tests固定此前置順序。

## Residual risk and evidence limits

- Exact `UserPromptExpansion.command_name`、two-entry `additionalContext`、Node missing／nonzero／exit `2`／timeout的host結果仍是Ticket 3 live ledger hard gate；目前測試是simulated。
- 官方host可在`PostModelSwitch` commit前先送下一個request；commit前只能best effort，commit後next permitted public entry才有新classification保證。
- Process在取得lock後被強制終止，會留下最長lease＋grace後才能由確認死亡的owner安全回收；grace期間正常route會bounded failure，Pre hook仍立即返回。這是避免誤刪live lock的安全取捨，不是零等待crash recovery。
- Windows file-symlink測試因權限skip；directory junction有live test，其他OS symlink/path行為仍是automated compatibility target而非live OS claim。
- Router目前1,603行／48,572 bytes，SHA-256為`d0383da5c7581c7d643ab68789cbfac907655cba95540ad56a85c378af8baa32`，仍是單一dependency-free runtime module；Large Module／Divergent Change風險已形成Draft architecture diagnosis，但尚未接受或排程任何拆分。Draft report保存修正前1,482行snapshot，若未來要接受該報告，必須先以current bytes重新確認，不可把舊hash當current。
- Fresh [Review after third corrections](claude-code-adapter-1.4.0-ticket-2-review-after-third-corrections.md)保存當時的`changes-requested` verdict；其兩項P2已完成第四輪TDD修正，但在新的fresh independent Review Accepted前，本Evidence仍不宣告Ticket 2 Completed。
- Fresh [Review after fourth corrections](claude-code-adapter-1.4.0-ticket-2-review-after-fourth-corrections.md)保存當時的`Changes Requested` verdict；其1×P1／4×P2已完成第五輪TDD修正，但在新的fresh independent Review Accepted前，本Evidence仍不宣告Ticket 2 Completed。
- Fresh [Review after fifth corrections](claude-code-adapter-1.4.0-ticket-2-review-after-fifth-corrections.md)保存當時的`Changes Requested` verdict；其1×P2已完成第六輪TDD修正，但在新的fresh independent Review Accepted前，本Evidence仍不宣告Ticket 2 Completed。
- Fresh [Review after sixth correction](claude-code-adapter-1.4.0-ticket-2-review-after-sixth-correction.md)保存當時的`Changes Requested` verdict；其2×P2已完成第七輪TDD修正，但在新的fresh independent Review Accepted前，本Evidence仍不宣告Ticket 2 Completed。
- Fresh [Review after seventh corrections](claude-code-adapter-1.4.0-ticket-2-review-after-seventh-corrections.md)的verdict為`Changes Requested`，包含1×P1；其sidecar路線是已取代的歷史實作，第十輪current驗證改證canonical-only Post transaction。在新的fresh independent Review Accepted前，Ticket 2仍未Completed。
- Fresh [Review after eighth correction](claude-code-adapter-1.4.0-ticket-2-review-after-eighth-correction.md)的verdict為`Changes requested`，包含1×P1與1×P2；sidecar-hardening已由第十輪移除，present-unmapped compact correction仍通過current suite。在新的fresh independent Review Accepted前，Ticket 2仍未Completed。
- Fresh [Review after ninth corrections](claude-code-adapter-1.4.0-ticket-2-review-after-ninth-corrections.md)的verdict為`Changes requested`，包含2×P2：sidecar違反Approved單一JSON契約，以及Post在Node 22 gate前已寫persistent data而validator漏檢。兩項均已依核准的canonical-only／Node-before-state方案完成第十輪TDD修正與驗證；仍須fresh independent Review判定是否關閉，因此Ticket 2尚未Completed。
- Fresh [Review after tenth corrections](claude-code-adapter-1.4.0-ticket-2-review-after-tenth-corrections.md)以`independent`標籤得到`Accepted - no actionable findings`；它獨立重跑Claude `106`與full repository `322` tests、兩個validators、Node syntax、diff check及exact Claude Code `2.1.251`兩項strict validation，並逐項完成十二個architecture/refactoring lenses。上述舊Reviews的待Review條件至此已滿足，Ticket 2 deterministic scope完成。
