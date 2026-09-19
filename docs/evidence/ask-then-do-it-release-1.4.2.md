# Ask Then Do It 1.4.2 Release Evidence

Artifact type: Release Evidence

Artifact ID: `ask-then-do-it-release-1.4.2-evidence`

Release version: `1.4.2`

Status: Completed

tests: skipped-by-user

## 結論

`1.4.2` 的 16 項必要 repository、套件與發布檢查均有通過結果。正式資產必須從 exact release commit 的乾淨 checkout 重新建置，且三個 ZIP 與 `checksums.sha256` 必須在發布前再次核對。

T3A 曾在隔離環境執行完整 suite：596 tests、10 個已揭露的平台 skip、exit 0；這是整理前的歷史證據，不冒充 final exact-commit 已測試。後續 direct tickets 依使用者指定不再執行行為測試（`tests: skipped-by-user`）；提交前整理只移除一次性 release evidence machinery／逐 Ticket 流水帳，保留可重用的 Codex baseline fixture，不改 consumer runtime。整理後受影響範圍改以靜態驗證、exact-commit build checks 與 final Review 把關。

## 必要檢查

| 範圍 | 結果 |
| --- | --- |
| Automated suite | 整理前歷史證據：596 tests，10 skipped，exit 0；final-diff tests 依使用者指定未重跑 |
| Workflow token proxy | Codex Full 17,240、Lite 3,846，降低 77.69%；Generic 固定成本 15,460 |
| Codex | 九個 source／packaged Skills、Plugin、conformance、30-file package inventory 通過 |
| Generic | conformance、18-file package inventory 通過 |
| Claude | repository-side Plugin／model mapping、conformance、32-file package inventory 通過 |
| Build | 兩次隔離建置均為 84 files 且逐 byte 相同 |
| Archives | 三個 ZIP 與展開目錄一致；checksum 重算相符 |
| Safety | 套件不含 tests、evidence、cache、credentials、transcripts、Git 或 machine-local paths |
| Architecture／Review | 無 P0-P3 product、packaging 或 release blocker；過度複雜的一次性 binding 流程已在提交前移除 |

完整 16-check command／outcome 清單保存在同名 JSON ledger。

## 候選資產 identity

| 資產 | SHA-256 |
| --- | --- |
| `codex/ask-then-do-it-1.4.2.zip` | `e8212a69f3ba1424f0f827003beb1761705293ec39d7bebe87669630b92b5360` |
| `generic/ask-then-do-it-generic-1.4.2.zip` | `48b16b732483f050fb036b45bf5f78b22504cc03f71c6fb31db9871ff7880485` |
| `claude/ask-then-do-it-claude-1.4.2.zip` | `8e27c1010563d2cb7935f137671ba250a0dc138f7bfbce541f9b82592f250013` |
| `checksums.sha256` | `3c51d6e0cfb932455c30cc2e481035d3934e8179237a5ef0e77e863128c3641c` |

若 exact-commit clean build 不符合以上 identity，停止發布並以重新建置結果釐清原因，不覆寫同版公開資產。

## Claude claim boundary

必要 Claude checks 只證明 repository-side 靜態結構、conformance 與 package parity。下列選配 qualification 均不是 release gate：

- `claude-behavior`: `not run / unverified`
- `claude-context`: `not run / unverified`
- `claude-live-smoke`: `not run / unverified`

本次沒有登入、OAuth、模型呼叫、session／transcript export、context capture 或真實 lifecycle smoke；因此不得宣稱 Claude `live-verified`。

## 發布邊界

- 只使用既有 `dev`，不建立新分支。
- 禁止 force push、覆寫既有同版 tag／Release／assets，以及 `git add -A`。
- ignored 本機輸出、舊 candidates、cache、credentials 與 transcripts 不進 commit 或 consumer packages。
- Git tag 與 GitHub Release 是公開發布狀態的最終 authority；本文件不以尚未發生的遠端結果冒充完成。
