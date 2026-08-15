# Ask Then Do It Codex Plugin 1.3.0 使用ガイド

この Plugin は、要件確認から実装と Review までプロジェクトを案内します。ZIP を代替手段として使う場合は、アーカイブをダウンロードして展開し、`ask-then-do-it/` フォルダー全体をそのまま使用してください。

この独立プロジェクトは Matt Pocock の skills repository に着想を得ていますが、Matt Pocock との提携・推奨関係はありません。ライセンスと出典はパッケージ内の `LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。

## インストールまたは更新

Codex タスクで AI に次のように依頼します。

```text
公式 marketplace から Ask Then Do It をインストールまたは更新してください。
```

まず現在の状態を確認します。

```powershell
codex plugin marketplace list
codex plugin list
```

公式 marketplace がない場合だけ追加します。

```powershell
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
```

すでに存在して更新が必要な場合は、代わりに先に更新します。

```powershell
codex plugin marketplace upgrade ask-then-do-it
```

その後 Plugin をインストールまたは更新します。

```powershell
codex plugin add ask-then-do-it@ask-then-do-it
```

インストールまたは更新の成功後は、新しい Codex タスクを開始してください。判断規則、手動の代替手段、更新、削除については [Codex Plugin 詳細ガイド](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides/codex.ja.md)を参照してください。

## 使い始める

新しい Codex タスクで次のように入力します。

```text
$ask-then-do-it を使って、この機能の開発を手伝ってください：……
```

段階を指定する場合は、`$ask-requirements`、`$ask-with-docs`、`$write-spec`、`$plan-tickets`、`$implement-direct`、`$implement-tdd`、`$review-code`、`$improve-architecture` を使用できます。

## Full または Lite を選ぶ

完全な文書化ワークフローと高い検証水準が必要な作業には Full を使用します。範囲が明確で、短いワークフローと必要に応じた検証が適する変更には Lite を使用します。選択前に [Full と Lite の完全なワークフローガイド](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides/getting-started-simple.ja.md)を参照してください。


[README に戻る](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/README.md)
