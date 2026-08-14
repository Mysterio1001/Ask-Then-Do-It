# Ask Then Do It Codex Plugin 1.2.0 使用ガイド

この Plugin には、要件確認から実装、Review、アーキテクチャ診断までを案内する 9 個の Skill が含まれています。

この独立プロジェクトは Matt Pocock の skills repository に着想を得ていますが、Matt Pocock との提携・推奨関係はありません。ライセンスと出典はパッケージ内の `LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。

## ダウンロードと展開

`ask-then-do-it-1.2.0.zip` を展開すると、一番外側のフォルダーは `ask-then-do-it/` になります。`skills/` だけを取り出さず、フォルダー全体をそのまま使ってください。

## AI によるインストールと更新

Codex タスクで AI に自然言語で依頼することが主な入口です。

```text
公式 marketplace から Ask Then Do It をインストールまたは更新してください。
```

AI は書き込みの前に必ず状態を読み取ります。

```powershell
codex plugin marketplace list
codex plugin list
```

公式 marketplace がない場合だけ、marketplace を追加してから Plugin を追加します。

```powershell
codex plugin marketplace add Mysterio1001/Ask-Then-Do-It
codex plugin add ask-then-do-it@ask-then-do-it
```

公式 marketplace があり、新しい正式版が利用できる場合は、先に marketplace を更新してから同じ Plugin コマンドを実行します。

```powershell
codex plugin marketplace upgrade ask-then-do-it
codex plugin add ask-then-do-it@ask-then-do-it
```

インストール済みの版が最新なら、AI は状態だけを報告し、書き込みません。ソース、バージョン、CLI の対応、または結果を確実に判定できない場合は停止して不確実性を報告します。書き込みに失敗したら後続の書き込みを止め、現在の Plugin を先に削除したり、別のソースを選んだり、自動でダウングレードしたりしません。このプロジェクトでは文書に示した `add` サブコマンドだけを使い、ほかのインストール別名は使いません。

成功後は新しい Codex タスクを開始して新しい Plugin の内容を読み込ませます。marketplace の処理ができない場合は、対応する `1.2.0` ZIP を手動のフォールバックとして使います。ダウングレードは、ユーザーが古い版を明示的に選んだ場合だけ許可されます。

## 手動インストールのフォールバック

手動でインストールする場合は、完全な `ask-then-do-it/` フォルダーをローカル marketplace の `plugins/` に置き、entry がそのフォルダーを指すことを確認してから Plugin を有効にします。完了後は新しい Codex タスクを開始してください。

## 初回使用

新しい Codex タスクで次のように入力します。

```text
$ask-then-do-it を使って、この機能の開発を手伝ってください：……
```

AI は現在の段階を判定し、一度に最も重要な質問を一つだけ行います。要件、仕様、Ticket 計画の承認が必要です。3 回目の承認前に、AI は全 Ticket とテストの推奨を示し、どの Ticket にテストを追加するかを一度に確認します。既定値はありません。

承認後、内部ではテストを追加する Ticket を `tdd` として `$implement-tdd` に渡し、追加しない Ticket を `direct` として `$implement-direct` に渡します。Review は `tests: skipped-by-user` を保持し、未テストのリスクを説明します。3 回目の承認が終わるまで正式な実装は始まりません。

## 9 個の Skill 入口

通常は `$ask-then-do-it` から始めます。段階を直接指定する場合は次を使えます。

| Skill | 用途 |
| --- | --- |
| `$ask-then-do-it` | 現在の段階を判定して全体を案内 |
| `$ask-requirements` | 重要な要件を一つずつ確認 |
| `$ask-with-docs` | 要件を確認し Project Knowledge Base を整理 |
| `$write-spec` | 承認済み要件を仕様に変換 |
| `$plan-tickets` | 仕様を垂直 Ticket に分割しテスト選択を確認 |
| `$implement-direct` | 行動テストなしで承認済み `direct` Ticket を実装 |
| `$implement-tdd` | Red、Green、Refactor で Ticket を実装 |
| `$review-code` | 変更と証拠を Review |
| `$improve-architecture` | アーキテクチャを分析し改善案を提示 |

## 手動更新

1. 対応する版の ZIP をダウンロードして展開します。
2. marketplace にある現在の `ask-then-do-it/` をバックアップします。
3. 新しいフォルダー全体で置き換えます。
4. Plugin を再度有効にし、新しい Codex タスクで `$ask-then-do-it` を確認します。

自動でダウングレードしないでください。古い版を使う場合は、ユーザーがその版を明示的に選択してください。

## 手動削除

Codex で `ask-then-do-it` を削除または無効化します。marketplace の Plugin フォルダーや entry も削除する場合は、同じ marketplace を使う環境がほかにないことを確認してください。
