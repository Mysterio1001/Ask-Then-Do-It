# Ask Then Do It — Claude Code ガイド

このガイドは Claude Adapter `1.4.0-preview.1` の公開プレビューを説明します。Codex と Generic は安定版 `1.3.1` を維持します。共通の Full/Lite フローは[初心者向けガイド](getting-started-simple.ja.md)を参照してください。

<a id="versions"></a>
## プレビューの状況と三つのバージョン

**明示的に選ぶ公開プレビュー 1.4.0-preview.1 のリリース手順です。** 安定版は **1.3.1** のままで、その Codex／Generic パッケージにはこの Claude Adapter は含まれません。インストール手順と[バージョン固定のプレビュー ZIP](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0-preview.1/ask-then-do-it-claude-1.4.0-preview.1.zip)は、プレビュー tag、ZIP、`claude-preview` Marketplace ブランチの公開後に使用できます。利用できない場合は公開を待ち、別の source に置き換えないでください。

| 要件 | 意味 |
| --- | --- |
| Claude model `4.6+` | モデルの対応基準。有効でも一覧にないモデルは未検証です。 |
| Claude Code `2.1.251+` | モデルとは別に確認するホストの最低バージョン。 |
| Node.js `22+` | 自動 profile routing の独立した要件。native Claude Code 自体のインストールとは別です。 |

プレビューの検証範囲は native `strict` validation とローカル自動テスト（`local automated tests`）です。実際の公式 Claude Code session における command／hook 動作、モデルシナリオ、両 profile の等価性、context reduction、完全な live smoke は**検証を延期**しています。今回の公開条件には含めず、合格も主張しません。Exact Claude Code 2.1.251 の schema validation は live 動作や将来のホスト版を保証しません。

<a id="entries"></a>
## 二つの公開入口

インストールを確認して reload した後、自分でどちらかを呼び出します。

```text
/ask-then-do-it:ask-then-do-it この機能を作るのを手伝って……
/ask-then-do-it:ask-then-do-it-5 この機能を作るのを手伝って……
```

最初の入口は profile を自動選択し、二つ目は以下のルールに従って Claude 5 の経路を明示的に要求します。両方とも `model: inherit` で、現在のモデルを維持し、切り替えたり固定したりしません。サポートする namespaced entries はこの二つだけです。内部 stage は追加コマンドになりません。ホストが提供する bare aliases の有無は保証しません。

<a id="routing"></a>
## Routing とセッションの継続

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
## Full/Lite Config

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
## Review の能力

Full Review は隔離された Plugin reviewer が実際に利用できる場合に使います。許可ツールは `Read`、`Grep`、`Glob` だけで、write、shell、network はありません。メインのフローは報告を待ち、findings を確認します。Reviewer ファイルがあるだけでは、独立した実行の証拠になりません。

Repository tools が使えても独立 reviewer が利用できない場合、同一 context で Review し `non-independent` と表示します。会話や抜粋だけなら `limited-evidence` とし、未実施の確認と引き継ぎを示し、repository Review の完了を主張しません。`independent` は隔離と生の根拠が実証された場合だけです。Lite は常に同一 context の簡潔な Review を維持します。Finding 自体は修正を許可しません。

<a id="status"></a>
## 読み取り専用の状態確認

以下は `read-only` で、インストール、refresh、更新、有効化、無効化、削除、Config 変更をしません。

```sh
claude --version
node --version
claude plugin marketplace list --json
claude plugin list --json
claude plugin details ask-then-do-it@ask-then-do-it
```

Claude Code／Node、Marketplace 名／source／scope、qualified Plugin identity、インストール scope、version、enabled state、両入口の可用性を別々に報告します。Listing に必要情報がなければ unknown とし、適切な読み取り専用 host state を確認します。Ownership を捏造したり、安全に書けると仮定したりしません。Component discovery と projected token cost はモデルの動作や課金の根拠ではありません。

<a id="install-update"></a>
## User scope のインストールと更新

プレビューを選ぶ場合は、正確な Marketplace source `https://github.com/Mysterio1001/Ask-Then-Do-It.git#claude-preview` と qualified Plugin `ask-then-do-it@ask-then-do-it` を `--scope user` で使用します。Fragment は継続的に更新する `claude-preview` ブランチを選びます。Refresh はそのブランチを追跡するため、後続プレビューで URL を変える必要はありません。安定版 1.3.1 は昇格しません。[公式 Marketplace 文書](https://code.claude.com/docs/en/plugin-marketplaces)にこの `#ref` 構文が記載されています。

毎回の書き込み直前に、ownership、source、scope、現在の state を完全に再確認します。以前の status では不十分です。期待する Marketplace と Plugin が両方なく、曖昧さがない場合：

```sh
claude plugin marketplace add "https://github.com/Mysterio1001/Ask-Then-Do-It.git#claude-preview" --scope user
claude plugin install ask-then-do-it@ask-then-do-it --scope user
```

Claude Code 内で対応する Marketplace コマンドは `/plugin marketplace add https://github.com/Mysterio1001/Ask-Then-Do-It.git#claude-preview` です。Plugin だけがなく、Marketplace source／ref が正しい場合は install だけを実行します。期待するプレビューのインストールが古く、明示的な更新要求がある場合：

```sh
claude plugin marketplace update ask-then-do-it
claude plugin update ask-then-do-it@ask-then-do-it --scope user
```

Marketplace refresh には scope option がないため、前後の source／scope を確認し、次の書き込み前にも state を再確認します。Current version は enabled でも `disabled` でも no-op とし、無効化の選択を維持します。有効化は別の明示的操作です。インストール済みが `newer` なら停止し、downgrade も先に削除する更新もしません。

Source 不一致、同名の別 source、project／local／managed や複数 scope、変化または読めない state、非対応 Claude Code では書かずに停止します。Node がなくても他の条件を満たす明示的な lifecycle 操作は可能ですが、自動 routing は利用できません。Partial failure では以後の writes を止め、状態を読み直して実際の成否を報告し、破壊的 rollback をしません。成功後は `/reload-plugins` または新 session を使ってから新 bytes の有効化を主張します。背景 auto-update は有効にしません。

<a id="remove"></a>
## 削除とデータ保持

明示的な削除要求がある場合、実行直前に ownership／source／user scope／state を再確認します。

```sh
claude plugin uninstall ask-then-do-it@ask-then-do-it --scope user
```

最後の scope を削除する前に、Plugin data は再構築可能な routing state のみで、標準では削除されると説明します。明示的に保持を希望した場合だけ `--keep-data` を追加します。通常削除は Marketplace、二つの workflow Config、他の scopes を残します。それらを消すには別の purge 要求が必要です。実際の結果を確認し、失敗時に削除済みと主張しません。

<a id="zip"></a>
## Session-only ZIP リカバリー

[バージョン固定のプレビュー release](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/tag/v1.4.0-preview.1)から [ask-then-do-it-claude-1.4.0-preview.1.zip](https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0-preview.1/ask-then-do-it-claude-1.4.0-preview.1.zip)をダウンロードし、その release の checksums で SHA-256 を確認してから展開し、Plugin folder 全体を保持します。この tag は Marketplace ブランチが進んでも同じプレビューを指します。各 test／recovery session で、展開先を引用符付きの一引数として渡します。

```sh
claude --plugin-dir "/path with spaces/ask-then-do-it"
```

これは `session-only` で、`persistent` Marketplace インストールや更新ではありません。Session ごとに `--plugin-dir` が必要です。単独の `claude plugin list` はこの ZIP session の読み込みを証明しません。同じ flag を付けるか、その session 内で確認します。Local Marketplace を作らず、`~/.claude/skills` にコピーせず、personal Skill のインストールとも呼びません。短い Plugin START-HERE は変更されない same-version guide を参照します。

<a id="platforms"></a>
## プラットフォームと確認範囲

Windows、macOS、Linux の local `terminal CLI`、`VS Code`、`JetBrains` は **compatibility target** で、九つの `live-verified` 組み合わせではありません。この Adapter の完全な live environment はまだ主張しません。Live の主張には exact OS、surface、Claude Code、Node、active model、日付を記録する必要があります。

公式文書を **2026-09-09** に実際に読み取りました。

| Surface | 公式文書の対応と違い |
| --- | --- |
| terminal CLI | Local Plugins は Skills、Agents、hooks を含められ、CLI は全 commands／skills のインターフェースを提供します。文書上の対応は、この Adapter の exact host hooks の検証ではありません。 |
| VS Code | グラフィカルな Plugin 管理があり、host settings／hooks は CLI と共有されます。Chat panel は独自の CLI を同梱しますが、commands／skills は一部だけなので `/` で確認します。Integrated terminal の `claude` には別途 standalone CLI が必要です。Plugin reviewer の invocation／isolation と両 exact namespaced entries は surface ごとの検証が必要です。 |
| JetBrains | IDE integrated terminal で `claude` を動かし、external terminal は `/ide` で接続するのが公式手順です。Plugin 能力はその CLI runtime のもので、IDE integration が編集機能を追加します。別の graphical command interface や、この Adapter の動作検証を意味しません。 |

出典：[Plugin components](https://code.claude.com/docs/en/plugins-reference)、[VS Code](https://code.claude.com/docs/en/vs-code)、[JetBrains](https://code.claude.com/docs/en/jetbrains)、[Skills](https://code.claude.com/docs/en/skills)、[Subagents](https://code.claude.com/docs/en/sub-agents)、[hooks](https://code.claude.com/docs/en/hooks)。現在の公式文書は exact 2.1.251 の動作確認に代わりません。Claude Desktop、web/cloud はこの compatibility target の対象外です。

<a id="troubleshooting"></a>
## トラブルシューティング

- 入口がない場合：実際のインストール、source、scope、enabled、reload／新 session を確認します。Host の bare alias はサポート入口の契約ではなく、VS Code は一部しか表示しない場合があります。
- Routing が停止した場合：非対応 Claude Code／model、Node の欠如／旧版、`UserPromptExpansion` envelope の失敗、invalid／pending state を区別します。別 profile／model を推測したり、他 session を流用したりせず、前述の限定された explicit fallback だけを使います。
- 更新に失敗した場合：partial state を報告して停止し、先に削除したり別 source を選んだり、disabled Plugin を黙って有効化したりしません。
- Built-in `/doctor` は任意の Claude Code **インストール／設定の健全性**チェック専用です。Ask Then Do It Skills の変換、最適化、検証はしません。独自の Plugin doctor コマンドはありません。
- Claude Code `2.1.251` の native `strict` validation 合格は schema の根拠だけです。公式 session の入口動作、実モデルの結果、live lifecycle smoke はこのプレビュー以降に検証します。Context reduction や課金節約の結果は主張しません。

<a id="feedback"></a>
## プレビューへのフィードバック

再現可能な問題は [GitHub Issues](https://github.com/Mysterio1001/Ask-Then-Do-It/issues) に報告してください。プレビュー `1.4.0-preview.1`、OS と surface、Claude Code／Node のバージョン、現在の model、使用した入口、期待した結果と実際の結果を記載します。Logs を共有する前に認証情報や私的な会話内容を取り除いてください。

[README に戻る](../../README.md)
