# Ask Then Do It — AI Development Workflow

Release `1.0.0` is the first public release of **Ask Then Do It**: a model-neutral workflow that helps an AI ask first, reach agreement, and then do the work.

This project is an independent extension inspired by Matt Pocock’s skills repository, particularly grill-me, grilling, and its engineering workflow skills. Matt Pocock’s original work is licensed under the MIT License. This project is not affiliated with or endorsed by Matt Pocock.

Upstream: [Matt Pocock skills repository](https://github.com/mattpocock/skills) · [upstream MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE). See [LICENSE](LICENSE) for this project's additions and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the upstream notice and complete license.

## 繁體中文快速開始

請先開啟 [START-HERE.zh-TW.md](START-HERE.zh-TW.md)。它會先讓你選擇適合的使用方式：

- Codex Plugin：[下載 ask-then-do-it-1.0.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.0/ask-then-do-it-1.0.0.zip)，從 `$ask-then-do-it` 開始。
- Gemini 或其他 AI：[下載 ask-then-do-it-generic-1.0.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.0/ask-then-do-it-generic-1.0.0.zip)，貼上解壓後的 `generic-workflow.md`。

一般使用者不需要理解 `core/`、`adapters/`、`tests/` 或建置程式，也不需要先執行 Python。完整人類說明：

- [超簡單完整流程](docs/guides/getting-started-simple.zh-TW.md)
- [Codex Plugin 使用說明](docs/guides/codex.zh-TW.md)
- [Generic prompts 使用說明](docs/guides/generic.zh-TW.md)
- [模型中立設計說明](docs/design/ai-development-skills.zh-TW.md)

## 維護者工作區

這個 repository 是 canonical source 與驗證工作區：

- `core/`：所有模型共用的規則、階段與 Artifact 契約。
- `adapters/codex/`：Codex Plugin 與八個 Skills。
- `adapters/generic-prompts/`：Conversation-only 的九個 prompt 模組。
- `release/release.json`：目前版本與兩個套件的發佈契約。
- `scripts/`、`tests/`：建置與驗證工具。
- `dist/`：自動產生的成品，不是 canonical source。

在 repository 根目錄建置：

```powershell
python scripts/build_release.py
```

建置器只管理 `dist/codex/`、`dist/generic/` 與 `dist/checksums.sha256`。它不會修改 personal installation、不會建立或修改 marketplace，也不會安裝或發布任何內容。

目前正式的命名與授權行為契約請見 [Ask Then Do It 1.0.0 Specification](docs/specs/ask-then-do-it-1.0.0.md)，實作順序請見 [Ask Then Do It 1.0.0 Ticket Plan](docs/plans/ask-then-do-it-1.0.0.md)。舊版 Grill Me 文件僅保留為開發歷程。

## English Quick Start

Start with [START-HERE.zh-TW.md](START-HERE.zh-TW.md), then choose one consumer package:

- Codex Plugin: [download ask-then-do-it-1.0.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.0/ask-then-do-it-1.0.0.zip); begin with `$ask-then-do-it`.
- Generic prompts: [download ask-then-do-it-generic-1.0.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.0/ask-then-do-it-generic-1.0.0.zip); paste the extracted `generic-workflow.md` once with your request.

The repository is a maintainer workspace. Edit canonical source under `core/`, `adapters/`, and `release/release.json`; treat `dist/` as generated output. Building does not modify a personal installation, marketplace, or external service.
