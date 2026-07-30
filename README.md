# Ask Then Do It — AI Development Workflow

**先問清楚，再開始做。** Ask Then Do It 是一套模型中立的 AI 開發流程，協助 AI 先釐清需求、取得共識，再規劃、實作與檢查成果。

Release `1.0.1` adds clearer multilingual user documentation to **Ask Then Do It**.

This project is an independent extension inspired by Matt Pocock’s skills repository, particularly grill-me, grilling, and its engineering workflow skills. Matt Pocock’s original work is licensed under the MIT License. This project is not affiliated with or endorsed by Matt Pocock.

Upstream: [Matt Pocock skills repository](https://github.com/mattpocock/skills) · [upstream MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE). See [LICENSE](LICENSE) for this project's additions and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the upstream notice and complete license.

[繁體中文](START-HERE.zh-TW.md) · [English](START-HERE.en.md) · [日本語](START-HERE.ja.md)

## 繁體中文快速開始

請先閱讀 [START-HERE.zh-TW.md](START-HERE.zh-TW.md)，再選擇使用方式：

- Codex Plugin：[下載 ask-then-do-it-1.0.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-1.0.1.zip)，安裝後從 `$ask-then-do-it` 開始。
- Gemini 或其他 AI：[下載 ask-then-do-it-generic-1.0.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-generic-1.0.1.zip)，在每個新對話貼上解壓後的 `generic-workflow.md`。

更多說明：

- [初學者流程](docs/guides/getting-started-simple.zh-TW.md)
- [Codex Plugin 使用說明](docs/guides/codex.zh-TW.md)
- [Generic 使用說明](docs/guides/generic.zh-TW.md)
- [設計說明](docs/design/ai-development-skills.zh-TW.md)

## 維護者

在 Repository 根目錄建置套件並執行測試：

```powershell
python scripts/build_release.py
python -m unittest discover -s tests -p "test_*.py" -v
```
