# Ask Then Do It Claude Code 使用ガイド

一つの Claude Code Plugin に、一般 Claude と Claude 5 のワークフロープロファイルが含まれます。

以下は 1.4.2 のインストール／ダウンロード先です。遠隔側で利用できない場合は公開を待ってください。

## インストールと準備

Claude model **4.6+**、Claude Code **2.1.251+** が必要です。モデルの自動判定には Node.js **22+** も必要です。Claude Code 内で実行します。

この版は user scope のみに対応します。以下の初回コマンドは既定の user scope を使います。

```text
/plugin marketplace add Mysterio1001/Ask-Then-Do-It
/plugin install ask-then-do-it@ask-then-do-it
```

<a id="zip"></a>
<details>
<summary>ZIP フォールバック</summary>

ダウンロード後、Release の checksums ファイルで SHA-256 を確認できます。

[ダウンロード ask-then-do-it-claude-1.4.2.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.2/ask-then-do-it-claude-1.4.2.zip)

完全な Plugin をダウンロードして展開します。ターミナルから起動するたびに次を指定します。

```bash
claude --plugin-dir "/path with spaces/ask-then-do-it"
```

そのセッションだけに有効です（session-only）。次回も `--plugin-dir` が必要で、永続的な Marketplace インストールにはなりません。

</details>

## 使い始める

インストール後、`/reload-plugins` を実行するか、新しいセッションを開いて入力します。

```text
/ask-then-do-it:ask-then-do-it 予約サイトの開発を手伝ってください。日本語で進めてください。
```

## Full／Lite モード

**Full** は要件、仕様、Ticket 計画を保存し、実装前に三つの承認を求めます。**Lite** は範囲が明確な変更向けで、短い変更概要と一度の承認を使います。

「今回は Full を使って」または「今回は Lite を使って」と伝えると、現在の操作だけに適用されます。

既定値を設定するには、次のいずれかに `mode = "full"` または `mode = "lite"` を記入します。

- `<project>/.claude/ask-then-do-it.toml`
- `~/.claude/ask-then-do-it.toml`

優先順位は今回の明示的指示、プロジェクト設定、ユーザー設定、最後に Full です。無効な設定では Full に戻り、プロジェクト設定が無効ならユーザー設定へ進みません。判定中に設定を書き換えません。

詳しい手順、テスト選択、進捗の保存は次を参照： [初心者向けガイド](getting-started-simple.ja.md)。

## 利用できるコマンド

通常は最初の入口を使います。どちらも現在のモデルを維持し、モデルを切り替えません。

| 入口 | 用途 |
| --- | --- |
| `/ask-then-do-it:ask-then-do-it` | 一般 Claude／Claude 5 を自動選択。不明なモデルではその旨を説明し、一般プロファイルの互換モードを使います。 |
| `/ask-then-do-it:ask-then-do-it-5` | Claude 5 プロファイルを明示的に要求。既知の対応済み非 Claude 5 モデルでは一般プロファイルを使い、不明なモデルでは未検証であることを伝えます。 |

## 更新と削除

インストール済みの場合は Claude Code 内で実行します。

```text
/plugin marketplace update ask-then-do-it
/plugin update ask-then-do-it@ask-then-do-it
/reload-plugins
```

Plugin を削除するには：

```text
/plugin uninstall ask-then-do-it@ask-then-do-it --scope user
```

Marketplace とワークフロー設定は残ります。最後の scope を削除すると、再作成可能なルーティングデータは既定で削除されます。明示的に保持したい場合だけ `--keep-data` を使います。

バージョンや出所が不明な場合、更新に失敗した場合は停止して確認します。先に削除したり、自動で降版・出所変更をしたりしません。現行版なら再インストールは不要で、無効化状態も維持します。

## よくある質問

- 入口がない：Plugin の有効化を確認し、`/reload-plugins` または新しいセッションを使います。VS Code では `/` で利用可能なコマンドを確認します。
- 自動判定が停止：`claude --version` と `node --version` を確認します。`-5` は万能な修復コマンドではありません。
- `/doctor` は Claude Code のインストール／設定の健全性を調べます。本プロジェクトの Skills を変換・最適化しません。

Windows、macOS、Linux のローカル CLI、VS Code、JetBrains は互換性の対象です。実モデル、command／hook、独立 Review、完全なインストール・更新には未検証項目があります。オフラインテストの合格だけで実環境すべての検証済みとはなりません。 [詳細リファレンス](#advanced-reference)。

問題は [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues) に、プロジェクトと主プログラム／Node のバージョン、環境、入口、再現手順を添えて報告できます。

<a id="advanced-reference"></a>
<details>
<summary>詳細リファレンス</summary>

ルーティング、設定解析、Review、プラットフォーム根拠の詳細です。通常のインストールと利用は主ガイドを参照してください。

[使用ガイド](claude-code.ja.md)

<a id="routing"></a>
### Routing とセッションの継続

| 信頼できる route 結果 | 自動入口 | 明示的な `-5` 入口 |
| --- | --- | --- |
| 既知の Claude 5 | Claude 5 profile | Claude 5 profile |
| 対応済みの Claude 5 以外 | General profile | 不一致を説明して General |
| `known unsupported`：既知の 4.6 未満 | 停止 | 停止 |
| `valid unknown`：有効だが未登録、または省略されたモデル | 未検証の互換モードと説明して General | 利用者の明示的な未検証の選択と説明して Claude 5 |
| `router failure`：state、ownership、transition、handler の失敗 | 停止 | 下記の二つの Node 例外以外は停止 |

Node の欠如や旧版は、モデルが unknown であることを意味しません。明示的入口に限り、有効な `node-too-old` envelope、または Node が確実に存在せず envelope が利用できない場合、説明したうえで手動の Claude 5 経路を使えます。両方とも Claude Code 2.1.251+ を別途証明する必要があります。モデルの検証、自動 routing、永続 binding、resume、switch tracking は提供しません。Node が存在する状態で envelope が欠落／破損／重複、バージョンが不明、その他の router failure は停止します。利用者の文章やモデルの自己申告から識別しません。

一つの `operation` は選択済み profile を維持します。途中でモデルが変わっても別 profile を読み込んだり従ったりしません。`PostModelSwitch` の commit 後、次に許可された公開入口で再選択でき、過去の profile 指示を置き換えます。Hook には `best-effort` の時間差があり、切り替え直後の最初の invocation での reroute は保証しません。非対応モデルへ切り替えた場合、現在の operation が正式サポートを外れたことも伝えます。

Startup、fork、clear は前の operation を自動再開しません。Resume／compact は信頼できる同一 session context と現在の workflow evidence が必要で、古い binding は別 session の権限になりません。Full は保存した承認済み artifacts を使えますが、Lite の会話状態は session を越えて永続化しません。

<a id="config"></a>
### Full/Lite Config

Profile 選択とフローモードは別です。各 operation は、明示的な `full`／`lite` 指示 → active project root 内の project Config → user Config → Full fallback の順です。明示的モードが衝突したら、一問で確認して停止します。Project の境界は信頼できる host の active project root で決め、作業ディレクトリを推測しません。

- Project：`<project>/.claude/ask-then-do-it.toml`
- User：`~/.claude/ask-then-do-it.toml`

ファイルには top-level の引用符付き代入を一つだけ記述します。

```toml
mode = "full"
```

または `mode = "lite"` です。Project Config が存在しない場合は user Config へ進みます。存在するが読めない、不正な構文、重複、mode 欠落、非対応値の場合は Full に fail closed します。無効な project ファイルから user ファイルへは進みません。大小文字の変種、別名、nested keys、引用符なしの値は無効です。会話のみの能力で host-unavailable source に遭遇した場合は absence と扱い、読んだと偽らず、host Config の提示も求めません。

判定は読み取り専用で、どちらのファイルも作成、修復、書き換えません。Operation override を保存せず、Codex Config の読み書きや `settings.json` への書き込みもしません。この Plugin Config は Claude Code の host settings や再構築可能な routing data とは別です。Full の承認 gates、Ticket ごとのテスト選択、Lite の一度の Change Brief は[共通フローガイド](getting-started-simple.ja.md)を参照してください。

<a id="review"></a>
### Review の能力

Full Review は隔離された Plugin reviewer が実際に利用できる場合に使います。許可ツールは `Read`、`Grep`、`Glob` だけで、write、shell、network はありません。メインのフローは報告を待ち、findings を確認します。Reviewer ファイルがあるだけでは、独立した実行の証拠になりません。

Repository tools が使えても独立 reviewer が利用できない場合、同一 context で Review し `non-independent` と表示します。会話や抜粋だけなら `limited-evidence` とし、未実施の確認と引き継ぎを示し、repository Review の完了を主張しません。`independent` は隔離と生の根拠が実証された場合だけです。Lite は常に同一 context の簡潔な Review を維持します。Finding 自体は修正を許可しません。

<a id="status"></a>
### 読み取り専用の状態確認

以下は `read-only` で、インストール、refresh、更新、有効化、無効化、削除、Config 変更をしません。

```sh
claude --version
node --version
claude plugin marketplace list --json
claude plugin list --json
claude plugin details ask-then-do-it@ask-then-do-it
```

Claude Code／Node、Marketplace 名／source／scope、qualified Plugin identity、インストール scope、version、enabled state、両入口の可用性を別々に報告します。Listing に必要情報がなければ unknown とし、適切な読み取り専用 host state を確認します。Ownership を捏造したり、安全に書けると仮定したりしません。Component discovery と projected token cost はモデルの動作や課金の根拠ではありません。

<a id="platforms"></a>
### プラットフォームと確認範囲

Windows、macOS、Linux の local `terminal CLI`、`VS Code`、`JetBrains` は **compatibility target** で、九つの `live-verified` 組み合わせではありません。この Adapter の完全な live environment はまだ主張しません。Live の主張には exact OS、surface、Claude Code、Node、active model、日付を記録する必要があります。

公式文書を **2026-09-09** に実際に読み取りました。

| Surface | 公式文書の対応と違い |
| --- | --- |
| terminal CLI | Local Plugins は Skills、Agents、hooks を含められ、CLI は全 commands／skills のインターフェースを提供します。文書上の対応は、この Adapter の exact host hooks の検証ではありません。 |
| VS Code | グラフィカルな Plugin 管理があり、host settings／hooks は CLI と共有されます。Chat panel は独自の CLI を同梱しますが、commands／skills は一部だけなので `/` で確認します。Integrated terminal の `claude` には別途 standalone CLI が必要です。Plugin reviewer の invocation／isolation と両 exact namespaced entries は surface ごとの検証が必要です。 |
| JetBrains | IDE integrated terminal で `claude` を動かし、external terminal は `/ide` で接続するのが公式手順です。Plugin 能力はその CLI runtime のもので、IDE integration が編集機能を追加します。別の graphical command interface や、この Adapter の動作検証を意味しません。 |

出典：[Plugin components](https://code.claude.com/docs/en/plugins-reference)、[VS Code](https://code.claude.com/docs/en/vs-code)、[JetBrains](https://code.claude.com/docs/en/jetbrains)、[Skills](https://code.claude.com/docs/en/skills)、[Subagents](https://code.claude.com/docs/en/sub-agents)、[hooks](https://code.claude.com/docs/en/hooks)。現在の公式文書は exact 2.1.251 の動作確認に代わりません。Claude Desktop、web/cloud はこの compatibility target の対象外です。

<a id="lifecycle"></a>
### インストール・更新・削除の詳細規則

永続的な出所は `Mysterio1001/Ask-Then-Do-It`、Plugin は `ask-then-do-it@ask-then-do-it` で、`user` scope のみ対応します。各書き込みの直前に出所、scope、版、有効状態を再確認します。未インストールの場合だけ追加し、現行版なら有効／無効のまま変更しません。新版から降版せず、出所や所有関係、scope が不明なら停止します。

インストール・更新・削除には明示的な依頼が必要です。連続操作でも書き込みごとに状態を再確認し、一部失敗時は停止して読み取りのみで確認し、破壊的な rollback はしません。Marketplace refresh に scope オプションはありません。Node がなくても許可済みの安全な lifecycle 操作は可能ですが、自動判定が使えないことを伝えます。新しい内容を使うには reload または新 session が必要です。背景更新を勝手に有効にしません。

以下はターミナル用です。インストール、更新、削除は別々の操作です。

```sh
# Install
claude plugin marketplace add Mysterio1001/Ask-Then-Do-It --scope user
claude plugin install ask-then-do-it@ask-then-do-it --scope user

# Update
claude plugin marketplace update ask-then-do-it
claude plugin update ask-then-do-it@ask-then-do-it --scope user

# Remove
claude plugin uninstall ask-then-do-it@ask-then-do-it --scope user
```


</details>

## ライセンスと出典

本プロジェクトは Matt Pocock の skills repository に着想を得た独立プロジェクトです。Matt Pocock との所属関係や同氏による承認はありません。`LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。

[README に戻る](../../README.md)
