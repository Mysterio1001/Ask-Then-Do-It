# Ask Then Do It Generic 使用ガイド

Claude Desktop Skills と、長いテキストを受け取れるその他の AI 向けです。Claude Desktop では ZIP を Skill としてアップロードし、テキストのみのホストではワークフローを貼り付けます。

## インストールと準備

パッケージをダウンロードし、Claude Desktop の Skills 機能から ZIP をアップロードします。ZIP 内の一つのパッケージフォルダーの直下に `SKILL.md` があり、先頭に YAML の `name` と `description` を含みます。テキストのみのホストでは ZIP を展開します。パッケージ直下の `SKILL.md` は全機能用、`LITE.md` は Lite 用です。

[ダウンロード ask-then-do-it-generic-1.5.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.5.0/ask-then-do-it-generic-1.5.0.zip)

## 使い始める

Claude Desktop ではアップロードとセキュリティスキャンの完了後に Skill を有効にし、Ask Then Do It の使用を依頼します。指示は Skill が選択されたときに読み込まれます。テキストのみのホストでは、新しい会話ごとに、Lite を使うなら `LITE.md`、全機能を使うなら `SKILL.md` を選び、**全文**と依頼を同じメッセージで送ります。例：

```text
Ask Then Do It を使って予約サイトの計画を手伝ってください。日本語で進めてください。
```

## Full／Lite モード

**Full** は要件、仕様、Ticket 計画を保存し、実装前に三つの承認を求めます。**Lite** は範囲が明確な変更向けで、短い変更概要と一度の承認を使います。

「今回は Full を使って」または「今回は Lite を使って」と伝えると、現在の操作だけに適用されます。

`SKILL.md` 内の宣言を一つだけ保持し、`Default workflow mode: full` または `Default workflow mode: lite` とします。インストール済みの Skill は編集後に再パッケージしてアップロードします。ワークフローのテキスト設定であり、Codex／Claude の設定ファイルは読みません。宣言がないか無効なら Full を使います。

詳しい手順、テスト選択、進捗の保存は次を参照： [初心者向けガイド](getting-started-simple.ja.md)。

## 利用できるコマンド

短い Lite 入口から Full へ切り替える際は、完全な `SKILL.md` と、すでに決めた内容を渡します。慣れたら `prompts/` の個別モジュールを貼り付けられますが、モード判定や承認は省略されません。

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
| `ticket-planning.md` | 仕様を縦割りの Tickets に分け、テスト方針を一度に確認する |
| `direct-implementation.md` | 承認に従い、既存テストのみ実行するかテストを省略する手順を示す |
| `tdd-implementation.md` | Ticket ごとにテストと実装を準備する |
| `review.md` | 会話で提示された内容を Review する |
| `architecture-improvement.md` | アーキテクチャ上の問題と改善案を分析する |

</details>

## 更新と削除

新版 ZIP を取得して Skill を再アップロードするか、新しいテキスト会話で新版 `SKILL.md` を貼り付けます。利用をやめるには Skill を無効化または削除するか、貼り付けをやめます。必要ならダウンロードしたコピーを削除し、プロジェクト文書は別に保存してください。

## よくある質問

- 新しい会話で進捗がない：有効な Skill を使用し、テキストのみのホストではワークフローを再度貼ります。Full の継続なら保存済みの要件、仕様、Ticket 計画も渡します。Skill のインストールは進捗を保存せず、Lite の状態は会話をまたいで保存されません。
- ファイル編集やテストができない：利用可能な能力はサービスとツールに依存します。チャットだけの場合は、自分で内容を適用して結果を渡します。

問題は [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues) に、プロジェクトの版、AI サービス／主プログラム、環境、再現手順を添えてください。

## ライセンスと出典

本プロジェクトは Matt Pocock の skills repository に着想を得た独立プロジェクトです。Matt Pocock との所属関係や同氏による承認はありません。`LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。

[README に戻る](../../README.md)
