# Ask Then Do It Generic 使用ガイド

Gemini など、長いテキストを受け取れる AI 向けです。ワークフローを貼り付けるだけで、Plugin のインストールは不要です。

以下は 1.4.0 のインストール／ダウンロード先です。遠隔側で利用できない場合は公開を待ってください。

## インストールと準備

パッケージをダウンロードして展開し、`generic-workflow.md` と `prompts/` を保持します。

[ダウンロード ask-then-do-it-generic-1.4.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0/ask-then-do-it-generic-1.4.0.zip)

## 使い始める

新しい会話ごとに `generic-workflow.md` の**全文**を貼り付け、その後に依頼を伝えます。例：

```text
予約サイトの開発を手伝ってください。日本語で進めてください。
```

## Full／Lite モード

**Full** は要件、仕様、Ticket 計画を保存し、実装前に三つの承認を求めます。**Lite** は範囲が明確な変更向けで、短い変更概要と一度の承認を使います。

「今回は Full を使って」または「今回は Lite を使って」と伝えると、現在の操作だけに適用されます。

ワークフロー内の宣言を一つだけ保持し、`Default workflow mode: full` または `Default workflow mode: lite` とします。貼り付けたテキストの設定であり、Codex／Claude の設定ファイルは読みません。宣言がないか無効なら Full を使います。

詳しい手順、テスト選択、進捗の保存は次を参照： [初心者向けガイド](getting-started-simple.ja.md)。

## 利用できるコマンド

通常は `generic-workflow.md` だけで十分です。慣れたら `prompts/` の個別モジュールを貼り付けられますが、モード判定や承認は省略されません。

<details>
<summary>詳細な入口を表示</summary>

| Prompt | 用途 |
| --- | --- |
| `bootstrap.md` | 現在の進捗と次の段階を判断する |
| `orchestration.md` | ワークフロー全体を調整する |
| `lite-workflow.md` | モード決定後に Lite の全ライフサイクルを案内する |
| `requirements.md` | 要件について一度に一つ質問する |
| `documented-requirements.md` | 要件を確認し、長期的なプロジェクト知識を整理する |
| `specification.md` | 承認済みの要件を仕様にまとめる |
| `ticket-planning.md` | 仕様を縦割りの Tickets に分け、テストを追加するかを一度に確認する |
| `direct-implementation.md` | 振る舞いテストなしの直接実装ガイダンスを提示する |
| `tdd-implementation.md` | Ticket ごとにテストと実装を準備する |
| `review.md` | 会話で提示された内容を Review する |
| `architecture-improvement.md` | アーキテクチャ上の問題と改善案を分析する |

</details>

## 更新と削除

新版 ZIP を取得し、新しい会話で新版ワークフローを貼り付けます。利用をやめるには貼り付けをやめ、必要ならダウンロードしたコピーを削除します。プロジェクト文書は別に保存してください。

## よくある質問

- 新しい会話で進捗がない：ワークフローを再度貼り、Full の継続なら保存済みの要件、仕様、Ticket 計画も渡します。Lite の状態は会話をまたいで保存されません。
- ファイル編集やテストができない：利用可能な能力はサービスとツールに依存します。チャットだけの場合は、自分で内容を適用して結果を渡します。

問題は [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues) に、プロジェクトの版、AI サービス／主プログラム、環境、再現手順を添えてください。

## ライセンスと出典

本プロジェクトは Matt Pocock の skills repository に着想を得た独立プロジェクトです。Matt Pocock との所属関係や同氏による承認はありません。`LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。

[README に戻る](../../README.md)
