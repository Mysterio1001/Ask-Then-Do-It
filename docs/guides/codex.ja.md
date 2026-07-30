# Ask Then Do It Codex Plugin 使用ガイド

このガイドでは、Ask Then Do It のダウンロード、インストール、使用方法を説明します。Plugin には開発フローの各段階を担当する Skills が含まれています。

## ダウンロードと展開

[ask-then-do-it-1.0.1.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.1/ask-then-do-it-1.0.1.zip)して展開します。

展開後、一番外側の `ask-then-do-it/` フォルダーには次のものが含まれます。

- `.codex-plugin/`
- `skills/`
- 使用方法、ライセンス、出典に関する文書

インストールにはフォルダー全体を使用してください。`skills/` だけをコピーしたり、外側にバージョン名のフォルダーを追加したりしないでください。

## 手動インストール

現在の方法では、編集可能なローカル marketplace がすでに必要です。marketplace には名前と、`<local-marketplace-root>/plugins/ask-then-do-it` を指す entry が必要です。

1. marketplace に既存の `plugins/ask-then-do-it/` がある場合はバックアップします。初回インストールでは省略できます。
2. 展開した `ask-then-do-it/` フォルダー全体を `<local-marketplace-root>/plugins/ask-then-do-it/` にコピーします。
3. Codex から marketplace が見えることを確認します。

```powershell
codex plugin marketplace list
```

4. Plugin をインストールし、状態を確認します。

```powershell
codex plugin add ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

5. 新しい Codex タスクを開きます。

marketplace や entry がまだない場合は、[Codex Plugin 公式ガイド](https://developers.openai.com/plugins/build/plugins)に従って作成し、手順 1 に戻ってください。

## 初めて使う

新しい Codex タスクで次のように入力します。

```text
$ask-then-do-it を使って、この機能の開発を手伝ってください：……
```

AI は現在の段階を判断し、最も重要な質問を一つ行います。各質問には推奨回答と主なトレードオフが添えられます。

次の 3 か所では、あなたの明確な承認を待ちます。

1. 要件の合意。
2. 仕様。
3. Ticket 計画。

3 回目の承認が完了してから正式な実装を始めます。

## 8 個の Skill 入口

| Skill | 適した用途 |
| --- | --- |
| `$ask-then-do-it` | 現在の段階を判断し、フロー全体を案内する。通常はここから始める |
| `$ask-requirements` | 影響の大きい要件を一度に一つ確認する |
| `$ask-with-docs` | 要件を確認しながら Project Knowledge Base を整理する |
| `$write-spec` | 承認済みの要件を仕様にまとめる |
| `$plan-tickets` | 仕様を縦割りでテスト可能な Tickets に分ける |
| `$implement-tdd` | Ticket を Red、Green、Refactor の順で実装する |
| `$review-code` | 要件、コード差分、テスト結果を Review する |
| `$improve-architecture` | アーキテクチャとモジュールの関係を分析し、改善案を示す |

どの Skill も直接指定できます。`$ask-then-do-it` だけを使う場合、AI は依頼内容と現在の進捗から次の段階を選びます。

## 手動更新

1. 新しい ZIP をダウンロードして展開します。
2. marketplace にある `plugins/ask-then-do-it/` をバックアップします。
3. 新しい `ask-then-do-it/` フォルダー全体で置き換えます。
4. インストールコマンドをもう一度実行し、`codex plugin list` でバージョンを確認します。
5. 新しい Codex タスクで `$ask-then-do-it` を試します。

新しいバージョンが読み込まれない場合は、バックアップを戻して以前のバージョンを再インストールしてください。

## 手動削除

次のコマンドを実行します。

```powershell
codex plugin remove ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

このコマンドで Codex からインストールを削除できます。marketplace 内の `plugins/ask-then-do-it/` や entry も削除する場合は、同じ marketplace を使う環境がほかにないことを確認してください。

## ライセンスと出典

Ask Then Do It は Matt Pocock の skills repository から着想を得た独立プロジェクトであり、Matt Pocock との提携関係や同氏による推奨を示すものではありません。詳しくは Repository またはパッケージ内の `LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。
