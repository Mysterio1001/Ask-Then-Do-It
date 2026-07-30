# Ask Then Do It — AI Development Workflow

## English

**Ask first, then start doing.** Ask Then Do It is a model-neutral AI development workflow that helps AI clarify requirements, reach consensus, plan, implement, and review the results.

Release `1.0.1` adds clearer multilingual user documentation to **Ask Then Do It**.

This project is an independent extension inspired by Matt Pocock’s skills repository, particularly grill-me, grilling, and its engineering workflow skills. Matt Pocock’s original work is licensed under the MIT License. This project is not affiliated with or endorsed by Matt Pocock.

Upstream: [Matt Pocock skills repository](https://github.com/mattpocock/skills) · [upstream MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE). See [LICENSE](LICENSE) for this project's additions and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the upstream notice and complete license.

### Quick Start

Please read [Traditional Chinese](START-HERE.zh-TW.md) · [English](START-HERE.en.md) · [Japanese](START-HERE.ja.md) first, then choose how you want to use it:

- Codex Plugin: [Download ask-then-do-it-1.0.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-1.0.1.zip), install it, and start with `$ask-then-do-it`.
- Gemini or another AI: [Download ask-then-do-it-generic-1.0.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-generic-1.0.1.zip), extract it, and paste `generic-workflow.md` into each new conversation.

More information:

- [Beginner workflow](docs/guides/getting-started-simple.en.md)
- [Codex Plugin guide](docs/guides/codex.en.md)
- [Generic guide](docs/guides/generic.en.md)
- [Design guide](docs/design/ai-development-skills.en.md)

### Maintainers

Build the packages and run the tests from the repository root:

```powershell
python scripts/build_release.py
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 繁體中文

**先問清楚，再開始做。** Ask Then Do It 是一套模型中立的 AI 開發流程，協助 AI 先釐清需求、取得共識，再規劃、實作與檢查成果。

`1.0.1` 版本為 **Ask Then Do It** 提供了更清楚的多語言使用者文件。

本專案是受到 Matt Pocock 的 skills repository 啟發而開發的獨立延伸作品，尤其參考了 grill-me、grilling 與相關工程工作流程 skills。Matt Pocock 的原始作品採用 MIT License。本專案與 Matt Pocock 沒有從屬關係，也未獲得其背書。

上游來源：[Matt Pocock skills repository](https://github.com/mattpocock/skills) · [上游 MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE)。本專案新增內容的授權請見 [LICENSE](LICENSE)；上游來源聲明與完整授權內容請見 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

### 快速開始

請先閱讀 [繁體中文](START-HERE.zh-TW.md) · [英文](START-HERE.en.md) · [日文](START-HERE.ja.md)，再選擇使用方式：

- Codex Plugin：[下載 ask-then-do-it-1.0.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-1.0.1.zip)，安裝後從 `$ask-then-do-it` 開始。
- Gemini 或其他 AI：[下載 ask-then-do-it-generic-1.0.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-generic-1.0.1.zip)，解壓縮後，在每個新對話貼上 `generic-workflow.md`。

更多說明：

- [初學者流程](docs/guides/getting-started-simple.zh-TW.md)
- [Codex Plugin 使用說明](docs/guides/codex.zh-TW.md)
- [Generic 使用說明](docs/guides/generic.zh-TW.md)
- [設計說明](docs/design/ai-development-skills.zh-TW.md)

### 維護者

在儲存庫根目錄建置套件並執行測試：

```powershell
python scripts/build_release.py
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 日本語

**まず確認し、それから作業を始めます。** Ask Then Do It は、AI が要件を明確にし、合意を得てから、計画、実装、成果の確認へ進むための、モデルに依存しない AI 開発ワークフローです。

リリース `1.0.1` では、**Ask Then Do It** の多言語ユーザー向けドキュメントをより分かりやすくしました。

本プロジェクトは、Matt Pocock の skills repository、特に grill-me、grilling、および関連するエンジニアリングワークフロー skills に着想を得た独立拡張プロジェクトです。Matt Pocock の原著作物は MIT License の下で提供されています。本プロジェクトは Matt Pocock と提携しておらず、同氏の推奨または承認を受けたものでもありません。

アップストリーム：[Matt Pocock skills repository](https://github.com/mattpocock/skills) · [アップストリームの MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE)。本プロジェクトで追加された内容のライセンスについては [LICENSE](LICENSE) を、アップストリームに関する通知と完全なライセンスについては [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) を参照してください。

### クイックスタート

まず [繁体字中国語](START-HERE.zh-TW.md) · [英語](START-HERE.en.md) · [日本語](START-HERE.ja.md) を読み、その後で利用方法を選んでください：

- Codex Plugin：[ask-then-do-it-1.0.1.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-1.0.1.zip)し、インストール後に `$ask-then-do-it` から始めます。
- Gemini またはその他の AI：[ask-then-do-it-generic-1.0.1.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-generic-1.0.1.zip)して展開し、新しい会話を始めるたびに `generic-workflow.md` を貼り付けます。

詳しい説明：

- [初心者向けワークフロー](docs/guides/getting-started-simple.ja.md)
- [Codex Plugin 利用ガイド](docs/guides/codex.ja.md)
- [Generic 利用ガイド](docs/guides/generic.ja.md)
- [設計ガイド](docs/design/ai-development-skills.ja.md)

### メンテナー

リポジトリのルートディレクトリでパッケージをビルドし、テストを実行します：

```powershell
python scripts/build_release.py
python -m unittest discover -s tests -p "test_*.py" -v
```
