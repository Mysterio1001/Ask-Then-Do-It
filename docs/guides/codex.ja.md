# Ask Then Do It Codex Plugin ガイド

このガイドでは Ask Then Do It のダウンロード、インストール、使い方を説明します。Plugin には開発ワークフローの各段階を担当する Skill が含まれています。

## ダウンロードと展開

[ask-then-do-it-1.2.0.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.2.0/ask-then-do-it-1.2.0.zip)して展開します。

展開後、一番外側のフォルダーは `ask-then-do-it/` です。次の内容を含む完全なフォルダーを使ってください。

- `.codex-plugin/`
- `skills/`
- 使用方法、ライセンス、出典の文書

`skills/` だけをコピーしたり、別のバージョン名フォルダーで包んだりしないでください。

## AI によるインストールと更新

自然言語で AI に依頼することが主なインターフェースです。

```text
公式 marketplace から Ask Then Do It をインストールまたは更新してください。
```

AI は書き込みの前に marketplace とインストール済み Plugin の状態を確認します。

```powershell
codex plugin marketplace list
codex plugin list
```

公式 marketplace がない場合だけ追加し、その後に Plugin を追加します。

```powershell
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
```

公式 marketplace があり、新しい正式版が利用できる場合は、marketplace を先に更新します。

```powershell
codex plugin marketplace upgrade ask-then-do-it
codex plugin add ask-then-do-it@ask-then-do-it
```

インストール済みの版が最新なら状態だけを報告し、書き込みません。ソース、バージョン、CLI の対応、または結果を確実に判定できない場合は停止して不確実性を報告します。書き込みに失敗したら後続の書き込みを止め、現在の Plugin を先に削除したり、別のソースを選んだり、自動でダウングレードしたりしません。対応する `add` サブコマンドだけを使い、ほかのインストール別名は使いません。

成功後は新しい Codex タスクを開始して新しい Plugin の内容を読み込ませます。marketplace の処理ができない場合は、対応する `1.2.0` ZIP を手動のフォールバックとして使います。ダウングレードはユーザーが古い版を明示的に選んだ場合だけ許可されます。

## 手動インストールのフォールバック

ローカル marketplace を使う手動方式では、完全な `ask-then-do-it/` を `<local-marketplace-root>/plugins/ask-then-do-it` に置き、entry がその場所を指すことを確認します。

```powershell
codex plugin marketplace list
codex plugin add ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

完了後は新しい Codex タスクを開きます。

## 初回使用

新しい Codex タスクで次のように入力します。

```text
$ask-then-do-it を使って、この機能の開発を手伝ってください：……
```

AI は現在の段階を判定し、最も重要な質問を一つずつ行います。要件、仕様、Ticket 計画の承認が必要です。3 回目の承認前に全 Ticket とテストの推奨を示し、どの Ticket にテストを追加するかを一度に確認します。既定値はありません。

承認後、内部ではテストを追加する Ticket を `tdd` として `$implement-tdd` に渡し、追加しない Ticket を `direct` として `$implement-direct` に渡します。Review は `tests: skipped-by-user` を保持し、未テストのリスクを説明します。3 回目の承認が終わるまで正式な実装は始まりません。

## Skill 入口

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

## 手動更新

1. 対応する版の ZIP をダウンロードして展開します。
2. marketplace にある現在の `plugins/ask-then-do-it/` をバックアップします。
3. 新しい完全なフォルダーで置き換えます。
4. Plugin を再度有効にし、新しい Codex タスクで `$ask-then-do-it` を確認します。

自動でダウングレードしないでください。古い版を使う場合は、ユーザーがその版を明示的に選択してください。

## 手動削除

```powershell
codex plugin remove ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

Plugin を削除する前に、同じ marketplace を使うほかの環境がないことを確認してください。

## ライセンスと出典

Ask Then Do It は Matt Pocock の skills repository に着想を得た独立プロジェクトです。Matt Pocock との提携・推奨関係はありません。詳細は `LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。
