# Ask Then Do It Codex Plugin ガイド

このガイドでは Ask Then Do It のダウンロード、インストール、使い方を説明します。Plugin には開発ワークフローの各段階を担当する Skill が含まれています。

## ダウンロードと展開

[ask-then-do-it-1.3.0.zip をダウンロード](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-1.3.0.zip)して展開します。

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

成功後は新しい Codex タスクを開始して新しい Plugin の内容を読み込ませます。marketplace の処理ができない場合は、対応する `1.3.0` ZIP を手動のフォールバックとして使います。ダウングレードはユーザーが古い版を明示的に選んだ場合だけ許可されます。

## 手動インストールのフォールバック

ローカル marketplace を使う手動方式では、完全な `ask-then-do-it/` を `<local-marketplace-root>/plugins/ask-then-do-it` に置き、entry がその場所を指すことを確認します。

```powershell
codex plugin marketplace list
codex plugin add ask-then-do-it --marketplace <local-marketplace-name>
codex plugin list --marketplace <local-marketplace-name>
```

完了後は新しい Codex タスクを開きます。

## ワークフローモードの設定

Codex は操作ごとに、次の順序でワークフローモードを決定します。

1. 「今回は Full」「今回は Lite」など、現在の操作に対する明示的な指示。
2. プロジェクト Config。
3. ユーザー Config。
4. Full fallback。

Plugin が所有する設定ファイルは次の場所にあります。

- プロジェクト：`<project>/.codex/ask-then-do-it.toml`。
- ユーザー：`~/.codex/ask-then-do-it.toml`。

各ファイルでは、トップレベルに `mode = "full"` または `mode = "lite"` だけを指定できます。

```toml
mode = "full"
```

```toml
mode = "lite"
```

たとえば、`mode = lite` は不正な形式で、`mode = "fast"` は未対応の値です。プロジェクト Config が存在しない場合だけ、ユーザー Config の読み取りへ進みます。無効なプロジェクト Config は Full にフォールバックし、ユーザー Config には進みません。存在するファイルが読み取れない、形式が不正、トップレベルの `mode` がない、または値が未対応の場合は無効です。現在の操作への明示指示は Config を読み取らずに優先します。

モード判定は読み取り専用であり、設定ファイルを作成、書き込み、修復、正規化しません。明示的な上書きは現在の操作だけに影響し、Config を変更しません。プロジェクト Config はそのプロジェクトだけに適用されます。新しいセッションでは、その操作の指示と現在の Config からモードを再判定します。

高リスクの作業では、現在の操作だけを Full に切り替えるか、リスクを明示的に受け入れて Lite を続けるか確認します。この選択は Config に保存されません。両モードの流れと高リスクの分類は [Full / Lite ワークフローガイド](getting-started-simple.ja.md)を参照してください。

## 初回使用

新しい Codex タスクで次のように入力します。

```text
$ask-then-do-it を使って、この機能の開発を手伝ってください：……
```

決定されたモードによって、その後のライフサイクルが変わります。

### Full モード

Full は一度に一つの要件質問だけを行い、推奨回答と主なトレードオフを添えます。Full には 3 つの承認点があります：

1. 要件の合意。
2. 仕様。
3. Ticket 計画。

3 回目の承認前に全 Ticket とテストの推奨を示し、どの Ticket にテストを追加するかを一度に確認します。既定値はありません。

承認後、内部ではテストを追加する Ticket を `tdd` として `$implement-tdd` に渡し、追加しない Ticket を `direct` として `$implement-direct` に渡します。Review は `tests: skipped-by-user` を保持し、未テストのリスクを説明します。3 回目の承認が終わるまで正式な実装は始まりません。

### Lite モード

repository の根拠ですべての阻害要因を解消できる場合、Lite は質問が不要な場合があります。それ以外では、各回最大 3 つの阻害要因に関する質問を行います。その後、1 つの Change Brief を提示し、実装前に 1 回の承認を待ちます。

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

任意の Skill を直接指定できます。Skill の直接呼び出しは段階を選択するだけで、ワークフローモードは選択しません。`$ask-then-do-it` が引き続き正規のモード判定を担います。通常の開始点にもなります。

モードが未決定なら `$ask-then-do-it` に委ねます。Lite と判定済みなら Lite ライフサイクルへ進みます。Full と判定済みなら通常の前提条件を満たした後にだけ、選択した段階へ進めます。モード指定が競合した場合は停止して確認を求めます。無効な Config は Full にフォールバックします。直接入口ではモード状態を永続化しません。

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


[README に戻る](../../README.md)
