# Ask Then Do It — AI Development Workflow

This project is an independent extension inspired by Matt Pocock’s skills repository, particularly grill-me, grilling, and its engineering workflow skills. Matt Pocock’s original work is licensed under the MIT License. This project is not affiliated with or endorsed by Matt Pocock.

Upstream: [Matt Pocock skills repository](https://github.com/mattpocock/skills) · [upstream MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE). See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Introduction

**Ask first, then build.** Ask Then Do It offers two workflow modes. Full keeps the complete, traceable path from requirements and specification through Tickets, implementation, test decisions, and Review. Lite uses a shorter Change Brief, one approval, direct implementation, minimum validation, and compact Review to reduce workflow overhead.

The default mode comes from Config. An explicit request can switch modes for the current operation without changing later sessions.

Please read the [User Guide](/START-HERE.en.md) first, then choose how you want to use it.

## Quick Start

### Automatic installation (CLI)

#### Codex CLI
```bash
# Install
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
# Update
codex plugin marketplace upgrade ask-then-do-it
```
> **Tip: Tell AI, "Install or update Ask Then Do It from the official marketplace."**

### Manual installation

- Codex Plugin: [Download ask-then-do-it-1.3.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-1.3.0.zip), install it, and start with `$ask-then-do-it`.
- Gemini or another AI: [Download ask-then-do-it-generic-1.3.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-generic-1.3.0.zip), extract it, and paste `generic-workflow.md` into each new conversation.

Read more:
- [Beginner workflow](docs/guides/getting-started-simple.en.md)
- [Codex Plugin guide](docs/guides/codex.en.md)
- [Generic guide](docs/guides/generic.en.md)
- [Design guide](docs/design/ai-development-skills.en.md)

## 介紹

**先問清楚，再開始做。** Ask Then Do It 提供兩種流程模式。Full 保留從需求、規格、Tickets 到實作、測試選擇與 Review 的完整可追溯流程；Lite 使用精簡 Change Brief、一次核准、直接實作、最低驗證與精簡 Review，降低流程負擔。

預設模式由 Config 決定；你可以只針對目前操作明確切換模式，不影響之後的工作階段。

請先閱讀 [使用說明](/START-HERE.zh-TW.md)，再選擇使用方式

## 快速開始

### 自動安裝 ( CLI )

#### Codex CLI
```bash
# 安裝
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
# 更新
codex plugin marketplace upgrade ask-then-do-it
```
> **提示 對 AI 說：「請從官方 marketplace 安裝或更新 Ask Then Do It。」**

### 手動安裝

- Codex Plugin：[下載 ask-then-do-it-1.3.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-1.3.0.zip)，安裝後從 `$ask-then-do-it` 開始。
- Gemini 或其他 AI：[下載 ask-then-do-it-generic-1.3.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-generic-1.3.0.zip)，解壓縮後，在每個新對話貼上 `generic-workflow.md`。


更多說明：
- [初學者流程](docs/guides/getting-started-simple.zh-TW.md)
- [Codex Plugin 使用說明](docs/guides/codex.zh-TW.md)
- [Generic 使用說明](docs/guides/generic.zh-TW.md)
- [設計說明](docs/design/ai-development-skills.zh-TW.md)

## はじめに

**最初に確認してから作り始めます。** Ask Then Do It には二つのワークフローモードがあります。Full は要件、仕様、Tickets、実装、テスト選択、Review までの完全で追跡可能な流れを保ちます。Lite は短い Change Brief、一度の承認、直接実装、最低限の検証、簡潔な Review によってフローの負担を減らします。

デフォルトモードは Config で決まります。明示的な依頼による切り替えは現在の操作だけに適用され、後のセッションには影響しません。

まず [利用ガイド](/START-HERE.ja.md) を読み、その後で利用方法を選んでください。

## クイックスタート

### 自動インストール（CLI）

#### Codex CLI
```bash
# インストール
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
# 更新
codex plugin marketplace upgrade ask-then-do-it
```
> **ヒント：AI に「公式 marketplace から Ask Then Do It をインストールまたは更新してください」と伝えてください。**

### 手動インストール

- Codex Plugin：[ask-then-do-it-1.3.0.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-1.3.0.zip)し、インストール後に `$ask-then-do-it` から始めます。
- Gemini またはその他の AI：[ask-then-do-it-generic-1.3.0.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-generic-1.3.0.zip)して展開し、新しい会話ごとに `generic-workflow.md` を貼り付けます。

詳しい説明：
- [初心者向けフロー](docs/guides/getting-started-simple.ja.md)
- [Codex Plugin 使用ガイド](docs/guides/codex.ja.md)
- [Generic 使用ガイド](docs/guides/generic.ja.md)
- [設計ガイド](docs/design/ai-development-skills.ja.md)
