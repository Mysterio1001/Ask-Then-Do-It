# Ask Then Do It：確認してから、作り始める

Ask Then Do It には 2 つの進め方があります。Full は重要な作業を文書化しながら厳密に進めるためのモード、Lite は範囲が明確な変更を必要な検証と Review に絞って進めるための短いモードです。

このプロジェクトは [Matt Pocock skills repository](https://github.com/mattpocock/skills) から着想を得た独立プロジェクトであり、Matt Pocock との提携関係や同氏による推奨を示すものではありません。ライセンスと出典については [LICENSE](LICENSE) と [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) を参照してください。

## 1. Codex で使う

[ask-then-do-it-1.3.1.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.1/ask-then-do-it-1.3.1.zip)して展開します。`ask-then-do-it/` Plugin フォルダー全体をインストールしたら、新しい Codex タスクで次のように入力します。

```text
$ask-then-do-it 作りたいものは……
```

インストール、更新、Codex のモード設定は [Codex Plugin 使用ガイド](docs/guides/codex.ja.md)を参照してください。

## 2. Gemini またはその他の AI で使う

[ask-then-do-it-generic-1.3.1.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.1/ask-then-do-it-generic-1.3.1.zip)して展開します。`generic-workflow.md` を開き、全文を新しい AI の会話に貼り付けてから、実現したいことを伝えます。

設定方法、モード選択、機能上の制限は [Generic 使用ガイド](docs/guides/generic.ja.md)を参照してください。

## ワークフローについて知る

- [Full と Lite の完全なワークフローガイド](docs/guides/getting-started-simple.ja.md)
- [設計ガイド](docs/design/ai-development-skills.ja.md)


[README に戻る](README.md)
