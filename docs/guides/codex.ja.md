# Ask Then Do It Codex Plugin 使用ガイド

Codex Plugin で要件確認から実装、Review まで進めます。通常は `$ask-then-do-it` から始めます。

以下は 1.4.0 のインストール／ダウンロード先です。遠隔側で利用できない場合は公開を待ってください。

## インストールと準備

初回はターミナルで次を実行します。AI に実行を依頼することもできます。

```bash
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
```

<a id="zip"></a>
<details>
<summary>ZIP フォールバック</summary>

[ダウンロード ask-then-do-it-1.4.0.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0/ask-then-do-it-1.4.0.zip)

`skills/` だけでなく完全な `ask-then-do-it/` を保持します。設定済みで編集可能なローカル Marketplace の `plugins/ask-then-do-it/` に置き、entry もそこを指すようにしてから実行します。

```bash
codex plugin add ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

ローカル Marketplace がなければ[公式ガイド](https://developers.openai.com/plugins/build/plugins)で作成してください。

</details>

## 使い始める

インストール後、新しい Codex タスクを開いて入力します。

```text
$ask-then-do-it 予約サイトの開発を手伝ってください。日本語で進めてください。
```

## Full／Lite モード

**Full** は要件、仕様、Ticket 計画を保存し、実装前に三つの承認を求めます。**Lite** は範囲が明確な変更向けで、短い変更概要と一度の承認を使います。

「今回は Full を使って」または「今回は Lite を使って」と伝えると、現在の操作だけに適用されます。

既定値を設定するには、次のいずれかに `mode = "full"` または `mode = "lite"` を記入します。

- `<project>/.codex/ask-then-do-it.toml`
- `~/.codex/ask-then-do-it.toml`

優先順位は今回の明示的指示、プロジェクト設定、ユーザー設定、最後に Full です。無効な設定では Full に戻り、プロジェクト設定が無効ならユーザー設定へ進みません。判定中に設定を書き換えません。

詳しい手順、テスト選択、進捗の保存は次を参照： [初心者向けガイド](getting-started-simple.ja.md)。

## 利用できるコマンド

通常は `$ask-then-do-it` を使います。特定の段階を選ぶ場合は表を開いてください。直接呼び出す場合も各段階の前提条件は必要です。

<details>
<summary>詳細な入口を表示</summary>

| Skill | 用途 |
| --- | --- |
| `$ask-then-do-it` | 現在の段階を判定して全体を案内 |
| `$ask-requirements` | 重要な要件を一つずつ確認 |
| `$ask-with-docs` | 要件を確認し Project Knowledge Base を整理 |
| `$write-spec` | 承認済み要件を仕様に変換 |
| `$plan-tickets` | 仕様を Ticket に分割しテスト選択を確認 |
| `$implement-direct` | 行動テストなしで `direct` Ticket を実装 |
| `$implement-tdd` | Red、Green、Refactor で Ticket を実装 |
| `$review-code` | 変更と証拠を Review |
| `$improve-architecture` | アーキテクチャを分析し改善案を提示 |

</details>

## 更新と削除

インストール済みの場合はターミナルで実行します。

```bash
codex plugin marketplace upgrade ask-then-do-it
codex plugin add ask-then-do-it@ask-then-do-it
```

手動更新では先にバックアップし、新版の完全なフォルダーで置き換えて再追加します。読み込み失敗時はバックアップを戻せます。

更新後は新しい Codex タスクを開いてください。

Plugin を削除するには：

```text
codex plugin remove ask-then-do-it --marketplace ask-then-do-it
```

ローカル Marketplace を使った場合は、削除コマンドの名前を自分の `<local-marketplace-name>` に置き換えてください。

インストールだけを削除します。ローカル Marketplace のファイルを消す前に、他の環境が共有していないことを確認してください。

バージョンや出所が不明な場合、更新に失敗した場合は停止して確認します。先に削除したり、自動で降版・出所変更をしたりしません。現行版なら再インストールは不要で、無効化状態も維持します。

## よくある質問

- Skill がない：`codex plugin list` でインストールを確認し、新しいタスクを開きます。
- 出所が不明：まず `codex plugin marketplace list` で確認します。

問題は [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues) に、プロジェクトの版、AI サービス／主プログラム、環境、再現手順を添えてください。

## ライセンスと出典

本プロジェクトは Matt Pocock の skills repository に着想を得た独立プロジェクトです。Matt Pocock との所属関係や同氏による承認はありません。`LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。

[README に戻る](../../README.md)
