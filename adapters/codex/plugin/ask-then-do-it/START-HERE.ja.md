# Ask Then Do It Codex Plugin 1.0.1 使用ガイド

この Plugin には、要件の確認から実装、Review、アーキテクチャ改善までを案内する 8 個の Skills が含まれています。

このプロジェクトは Matt Pocock の skills repository から着想を得た独立プロジェクトであり、Matt Pocock との提携関係や同氏による推奨を示すものではありません。ライセンスと出典については、パッケージ内の `LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。

## ダウンロードと展開

`ask-then-do-it-1.0.1.zip` を展開すると、一番外側のフォルダーは `ask-then-do-it/` になります。`skills/` だけを取り出さず、フォルダー全体をそのまま使ってください。

## 手動インストール

この方法では、編集可能なローカル marketplace と、`plugins/ask-then-do-it/` を指す entry がすでに必要です。

1. `ask-then-do-it/` フォルダー全体を marketplace の `plugins/` フォルダーに置きます。
2. その marketplace から `ask-then-do-it` をインストールまたは有効化します。
3. 新しい Codex タスクを開き、インストールした内容を Codex に読み込ませます。

marketplace をまだ作成していない場合は、Codex Plugin のドキュメントに従って設定してから、ここに戻ってください。

## 初めて使う

新しい Codex タスクで次のように入力します。

```text
$ask-then-do-it を使って、この機能の開発を手伝ってください：……
```

AI は現在の段階を判断し、最初に重要な質問を一つ行います。要件、仕様、Ticket 計画には、あなたの明確な承認が必要です。承認前に正式な実装を始めてはいけません。

## 8 個の Skill 入口

通常は `$ask-then-do-it` から始めます。段階を指定したい場合は、次の Skill を直接使えます。

| Skill | 用途 |
| --- | --- |
| `$ask-then-do-it` | 現在の段階を判断し、ワークフロー全体を案内する |
| `$ask-requirements` | 一度に一つ質問して要件を明確にする |
| `$ask-with-docs` | 要件を確認しながら長期的なプロジェクト知識を整理する |
| `$write-spec` | 承認済みの要件を仕様にまとめる |
| `$plan-tickets` | 仕様を縦割りでテスト可能な Tickets に分ける |
| `$implement-tdd` | Ticket を Red、Green、Refactor の順で実装する |
| `$review-code` | 要件とテストの根拠に照らしてコードを Review する |
| `$improve-architecture` | アーキテクチャ上の問題を分析し、改善案を示す |

## 手動更新

1. 新しい ZIP をダウンロードして展開します。
2. marketplace にある現在の `ask-then-do-it/` をバックアップします。
3. 新しいフォルダー全体で置き換えます。
4. Plugin を再インストールまたは有効化し、新しい Codex タスクで `$ask-then-do-it` が使えることを確認します。

## 手動削除

まず Codex で `ask-then-do-it` を削除または無効化します。marketplace の Plugin フォルダーや entry も削除する場合は、同じ marketplace を使う環境がほかにないことを確認してください。
