# Ask Then Do It 1.3.1 WinError 5 Knowledge Base Change Summary

Artifact type: Knowledge Base Change Summary

Artifact ID: `release-1-3-1-winerror5-kb-change-summary`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Status: Approved

Inputs: 使用者於 2026-08-17 明確核准的 `WinError 5` 行為取捨、Approved revised `release-1-3-1-maintenance-requirements`、更新前的 Approved Project Knowledge Base，以及造成該決策的獨立 Specification review finding。

Assumptions: 本摘要只精確化既有 `1.3.1` Windows retry 決策，不擴大 maintenance scope，也不代表 implementation 或 release 已完成。

Deferred: 精確 retry 次數、等待間隔、backoff 形式，以及除 `WinError 5` 外的最終 Windows transient error-code allowlist。

Handoff: 下列 modification 已套用至 Project Knowledge Base，並已交回 `$write-spec`。

Approval: 使用者於 2026-08-17 聯合核准本摘要與修訂版 Requirement Decision Record 的精確內容。

## Additions

- None.

## Modifications

- 將 Project Knowledge Base `Important decisions` 中現有的 Windows retry 決策精確化為：managed-output replacement 與 rollback restoration 的 Windows `WinError 5` 明確列入 bounded-retry allowlist。因該 error code 無法區分暫時檔案占用與永久 ACL，永久 access-denied 可能短暫等待至 retry 上限；其他非 allowlisted errors 立即失敗。Rollback 無法完成時，仍須保留 staging/backup 並同時揭露 primary 與 recovery failure。

## Removals

- None.
