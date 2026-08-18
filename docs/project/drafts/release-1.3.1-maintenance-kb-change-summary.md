# Ask Then Do It 1.3.1 維護版本 Knowledge Base Change Summary

Artifact type: Knowledge Base Change Summary

Artifact ID: `release-1-3-1-maintenance-kb-change-summary`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Status: Approved

Inputs: Approved `release-1-3-1-maintenance-requirements`、Approved `1.3.0` release evidence 與更新前的 Approved Project Knowledge Base。

Assumptions: 本摘要只描述 Requirement Decision Record 核准後可套用的正式 Knowledge Base 變更；不代表 `1.3.1` 已實作或發布。

Deferred: Specification、Ticket Plan、implementation、completed release evidence、Git tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement facts。

Handoff: 下列明示變更已套用至 Project Knowledge Base，並已交給 `$write-spec`。

Approval: 使用者於 2026-08-17 在完整 Requirement Decision Record 與本摘要展示後明確回覆「核准」。

## Additions

- 在 Important decisions 新增：`1.3.1` 是發布可靠性維護版，範圍限於宣告 Pillow development/test dependency 與改善 Windows serial release replacement reliability。
- 在 Important decisions 新增：same-output concurrent builds、Token fingerprint、CI、dependency lock、文件擴充與全面 builder 重構不屬於 `1.3.1`。
- 在 Important decisions 新增：Windows replacement 只對 allowlisted transient errors 做 bounded retry；rollback 無法完成時保留 staging/backup 並揭露 primary 與 recovery failure。
- 在 Important decisions 新增：current release/Core/adapters/runtime identities lockstep 升至 `1.3.1`，`v1.3.0` 與其 artifacts 保持不可變。
- 在 External dependencies 新增：CPython 3.12 與 `Pillow>=12.3,<13` 是 `1.3.1` development/release-validation dependency，不是 consumer runtime dependency。
- 在 Unresolved items 新增：`v1.3.1` tag、push、GitHub Release、asset upload、Marketplace activation 與 announcement 仍待後續明確核准與實際結果。
- 在 Artifact links 新增本 Requirement Decision Record，並將 `1.3.1` Specification 與 Ticket Plan 標為 pending。

## Modifications

- 將 Knowledge Base envelope 的 current Core version 從 `1.1.0` 更新為已由 Approved `1.3.0` release evidence 證明的 `1.3.0`；`1.3.1` 在實作完成前只標示為 approved target。
- 將 Inputs 與 Assumptions 更新為同時引用 Approved `1.3.0` release evidence 與 Approved `1.3.1` Requirement Decision Record，不再把 `1.2.0` 描述為尚待完成的 target state。
- 將 Architecture map 的 release builder 說明補充為：以完整 staging validation、managed-output replacement 與 rollback 保護本機 release output。
- 將 Artifact links 中過時的「Ticket Plan pending after Specification approval」改為連結既有 Approved `1.3.0` requirement/specification/plan/release evidence，並另列 `1.3.1` Specification/Ticket Plan pending。

## Removals

- 移除已被 Approved `1.3.0` release evidence supersede 的 `1.2.0 entries describe the approved target state until implementation and release evidence establish completion` 假設。
- 不移除或改寫任何歷史 Requirement、Specification、Ticket Plan、Review、release evidence 或 tag reference。
