# Ask Then Do It — AI Development Workflow

This project is an independent extension inspired by Matt Pocock’s skills repository, particularly grill-me, grilling, and its engineering workflow skills. Matt Pocock’s original work is licensed under the MIT License. This project is not affiliated with or endorsed by Matt Pocock.

Upstream: [Matt Pocock skills repository](https://github.com/mattpocock/skills) · [upstream MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE). See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Quick Start

**Ask first, then build.** Ask Then Do It clarifies requirements, records agreement, creates a specification and Tickets, then implements and reviews each Ticket according to the user's test choice.

After the Tickets are drafted, the AI gives each one a test recommendation with time and risk warnings. In one response, you decide whether to add tests to every Ticket: add them to all, add them to none, or name only the Tickets that should have tests.

Please read the [User Guide](/START-HERE.en.md) first, then choose how you want to use it.

## Installation and updates

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

- Codex Plugin: [Download ask-then-do-it-1.2.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.2.0/ask-then-do-it-1.2.0.zip), install it, and start with `$ask-then-do-it`.
- Gemini or another AI: [Download ask-then-do-it-generic-1.2.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.2.0/ask-then-do-it-generic-1.2.0.zip), extract it, and paste `generic-workflow.md` into each new conversation.

Read more:
- [Beginner workflow](docs/guides/getting-started-simple.en.md)
- [Codex Plugin guide](docs/guides/codex.en.md)
- [Generic guide](docs/guides/generic.en.md)
- [Design guide](docs/design/ai-development-skills.en.md)

## 快速開始

**先問清楚，再開始做。** Ask Then Do It 是一套模型中立的 AI 開發流程，協助 AI 釐清需求、取得共識、建立規格與 Tickets，再依使用者決定是否加上測試的結果進行實作與 Review。

Tickets 建立後，AI 會逐張提供測試建議與工時、風險提醒。你可以在一次回覆中決定每張 Ticket 是否加上測試：全部加上、全部不加，或只指定部分 Tickets。

請先閱讀 [使用說明](/START-HERE.zh-TW.md)，再選擇使用方式

## 安裝與更新

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

- Codex Plugin：[下載 ask-then-do-it-1.2.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.2.0/ask-then-do-it-1.2.0.zip)，安裝後從 `$ask-then-do-it` 開始。
- Gemini 或其他 AI：[下載 ask-then-do-it-generic-1.2.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.2.0/ask-then-do-it-generic-1.2.0.zip)，解壓縮後，在每個新對話貼上 `generic-workflow.md`。


更多說明：
- [初學者流程](docs/guides/getting-started-simple.zh-TW.md)
- [Codex Plugin 使用說明](docs/guides/codex.zh-TW.md)
- [Generic 使用說明](docs/guides/generic.zh-TW.md)
- [設計說明](docs/design/ai-development-skills.zh-TW.md)

## クイックスタート

**最初に確認し、合意を残してから作り始めます。** Ask Then Do It は要件を明確にし、仕様と Tickets を作成した後、各 Ticket にテストを追加するかという利用者の決定に従って実装と Review を進めます。

Tickets の作成後、AI は各 Ticket のテスト方針と、時間およびリスクへの影響を説明します。すべての Ticket についてテストを追加するかどうかを一度に回答でき、全部に追加、全部に追加しない、または一部だけを指定できます。

まず [利用ガイド](/START-HERE.ja.md) を読み、その後で利用方法を選んでください。

## インストールと更新

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

- Codex Plugin：[ask-then-do-it-1.2.0.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.2.0/ask-then-do-it-1.2.0.zip)し、インストール後に `$ask-then-do-it` から始めます。
- Gemini またはその他の AI：[ask-then-do-it-generic-1.2.0.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.2.0/ask-then-do-it-generic-1.2.0.zip)して展開し、新しい会話ごとに `generic-workflow.md` を貼り付けます。

詳しい説明：
- [初心者向けフロー](docs/guides/getting-started-simple.ja.md)
- [Codex Plugin 使用ガイド](docs/guides/codex.ja.md)
- [Generic 使用ガイド](docs/guides/generic.ja.md)
- [設計ガイド](docs/design/ai-development-skills.ja.md)
