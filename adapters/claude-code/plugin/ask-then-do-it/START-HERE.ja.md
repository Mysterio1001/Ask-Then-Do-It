# Ask Then Do It Claude Code Plugin 1.4.0-preview.1

**明示的に選ぶ公開プレビューです。** Plugin folder 全体を保持してください。Codex と Generic は安定版 1.3.1 を維持します。リンク先の手順はプレビュー公開後に使用し、利用できない場合は公開を待ってください。

互換性の目標は Claude model 4.6+、Claude Code 2.1.251+、自動 routing には Node.js 22+ が必要です。検証範囲は native strict validation とローカル自動テストです。実際の公式 Claude session は検証を延期しています。

インストール確認後、または明示的に選択した local test session で、二つのサポート入口の一方を自分で使います。

```text
/ask-then-do-it:ask-then-do-it この機能を作るのを手伝って……
/ask-then-do-it:ask-then-do-it-5 この機能を作るのを手伝って……
```

どちらも現在のモデルを維持します。二つ目はモデルと host の確認に従って Claude 5 の経路を明示的に選びます。内部 stages は公開コマンドではありません。

Full/Lite、routing、Config、明示的に選ぶ Marketplace のインストール、更新、削除、reviewer の制限、platform、session-only ZIP リカバリー、フィードバックは、変更されない same-version の[Claude Code 詳細ガイド](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0-preview.1/docs/guides/claude-code.ja.md)を参照してください。ZIP を `--plugin-dir` で使用しても永続インストールは作成されません。

この独立プロジェクトは Matt Pocock の skills repository に着想を得ており、提携や推奨を示しません。対応するパッケージに `LICENSE` と `THIRD_PARTY_NOTICES.md` が含まれます。

[README に戻る](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0-preview.1/README.md)
