# Grill Me — AI Development Workflow

Release `3.0.0` packages the model-neutral core `3.0.0` for two supported usage paths: one Codex Plugin and one Generic prompt bundle. The validated `2.1.0` archives and checksum snapshot remain available for rollback and comparison.

## 繁體中文快速開始

Grill Me 是一套有明確人類核准點的 AI 軟體開發工作流，依序處理需求釐清、Specification、Ticket Planning、TDD 實作與證據式 Review。它不是只為 Codex 設計：共用規則在 `core/`，Codex Plugin 與 Generic prompts 都只是 adapter。

第一次使用，建議先閱讀 [Grill Me 超簡單使用說明](docs/guides/getting-started-simple.zh-TW.md)。它用蓋小屋的方式解釋完整流程與每個階段。

先在 repository 根目錄建置：

```powershell
python scripts/build_release.py
```

這個命令只會產生 repository 內的 `dist/` 成品，不會自動安裝 Plugin、不會修改 personal installation、不會建立 marketplace，也不會發布到網路。

### 路徑 A：Codex Plugin

- 未壓縮套件：`dist/grill-me/`
- 可發布壓縮檔：`dist/grill-me-3.0.0.zip`
- 主要入口：`$ai-dev-workflow`
- 進階入口：八個 Skill 都可獨立呼叫

Codex 會從已設定的 marketplace 安裝 Plugin；本專案只建置與驗證 Plugin bundle，不會替你設定 marketplace。安裝、更新與移除方式請見 [Codex Plugin 繁體中文使用說明](docs/guides/codex.zh-TW.md)。

### 路徑 B：Generic prompts

- 建議入口：`dist/generic-prompts-3.0.0/generic-workflow.md`
- 模組化替代方案：`dist/generic-prompts-3.0.0/prompts/`
- 適用環境：任何能接受文字 prompt 的一般語言模型或聊天介面

把 `generic-workflow.md` 全文貼入同一段對話，接著附上需求與既有 Artifacts。這個 adapter 僅宣告 Conversation-only 能力，不會假裝改過檔案、跑過測試或完成獨立 Review。詳見 [Generic prompts 繁體中文使用說明](docs/guides/generic.zh-TW.md)。

### 三種位置不要混用

| 類型 | 位置 | 是否可編輯 |
| --- | --- | --- |
| canonical source | `core/`、`adapters/`、`release/release.json` | 是；維護者只在這裡改規則、adapter 與 release 設定 |
| generated release | `dist/` | 否；刪除後可由 builder 重建 |
| personal installation | Codex 或其他主機管理的使用者環境 | 不屬於本 repository；任何修改都需要另外授權 |

`dist/checksums.sha256` 驗證目前的 `3.0.0` archives；`dist/checksums-2.1.0.sha256` 保留舊版驗證值。架構理由請閱讀 [繁體中文設計說明](docs/design/ai-development-skills.zh-TW.md)；正式行為契約以 [Portable AI Development Workflow v3 Specification](docs/specs/ai-development-skills-v3.md) 為準，原始包裝邊界則記錄於 [Release Packaging Specification](docs/specs/grill-me-release-packaging.md)。

## English Quick Start

Grill Me is a model-neutral, gated AI development workflow. Build both supported runtime packages from the repository root:

```powershell
python scripts/build_release.py
```

The command writes generated files only under `dist/`. It does not install a plugin, modify a personal installation, create a marketplace, publish anything, or use the network.

### Path A: Codex Plugin

- Unpacked plugin: `dist/grill-me/`
- Reproducible archive: `dist/grill-me-3.0.0.zip`
- Primary entry: `$ai-dev-workflow`
- Advanced use: invoke any of the eight Skills directly

Codex installs plugins from a configured marketplace. This repository builds the plugin bundle but does not configure or mutate a marketplace. See the [Traditional Chinese Codex guide](docs/guides/codex.zh-TW.md) for the manual lifecycle boundary.

### Path B: Generic prompts

- Recommended one-file entry: `dist/generic-prompts-3.0.0/generic-workflow.md`
- Modular alternative: `dist/generic-prompts-3.0.0/prompts/`
- Host requirement: a language model or chat interface that accepts text prompts

Paste the complete generated workflow into one conversation and then supply the request and existing Artifacts. This adapter is Conversation-only and never claims repository writes, command execution, completed TDD, durable persistence, or independent review. See the [Traditional Chinese Generic guide](docs/guides/generic.zh-TW.md).

Edit only canonical source under `core/`, `adapters/`, and `release/release.json`; treat `dist/` as generated; treat every personal installation as external user state requiring separate authorization. The versioned `2.1.0` archives and `checksums-2.1.0.sha256` remain preserved beside the current `3.0.0` release.
