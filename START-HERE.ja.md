# Ask Then Do It：確認してから、作り始める

Ask Then Do It は、AI が最初に要望を確認し、その後に仕様、作業計画、実装、確認の順で進められるよう案内します。

このプロジェクトは [Matt Pocock skills repository](https://github.com/mattpocock/skills) から着想を得た独立プロジェクトであり、Matt Pocock との提携関係や同氏による推奨を示すものではありません。ライセンスと出典については [LICENSE](LICENSE) と [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) を参照してください。

## 1. Codex で使う

[ask-then-do-it-1.1.0.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.1.0/ask-then-do-it-1.1.0.zip)して展開します。`ask-then-do-it/` Plugin フォルダー全体をインストールしたら、新しい Codex タスクで次のように入力します。

```text
$ask-then-do-it 作りたいものは……
```

AI は最初に重要な質問を一つ行い、要件が確認されてから次の段階へ進みます。Tickets の作成後、AI は各 Ticket のテスト方針を提案し、すべての Ticket についてテストを追加するかどうかを一度に確認します。最後に計画全体を承認します。インストール、更新、9 個の Skill の使い方は [Codex Plugin 使用ガイド](docs/guides/codex.ja.md)を参照してください。

## 2. Gemini またはその他の AI で使う

[ask-then-do-it-generic-1.1.0.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.1.0/ask-then-do-it-generic-1.1.0.zip)して展開します。`generic-workflow.md` を開き、全文を新しい AI の会話に貼り付けてから、実現したいことを伝えます。

AI は最初に要件について一つ質問します。ワークフローで作成された重要な文書は保存してください。別の新しい会話を始めるときは、ワークフローと保存した文書をもう一度貼り付けます。詳しい手順は [Generic 使用ガイド](docs/guides/generic.ja.md)を参照してください。

## ワークフローについて知る

- [初心者向けフロー](docs/guides/getting-started-simple.ja.md)
- [設計ガイド](docs/design/ai-development-skills.ja.md)
