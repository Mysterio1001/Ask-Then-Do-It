# Ask Then Do It Generic 1.3.0 使用ガイド

このパッケージは、Gemini など長い文章を受け取れる AI サービス向けです。会話の中でワークフローを案内し、ファイル操作、コマンド、その他のツールは利用するサービスが実際に提供する範囲でのみ使用できます。

このプロジェクトは Matt Pocock の skills repository から着想を得た独立プロジェクトであり、Matt Pocock との提携関係や同氏による推奨を示すものではありません。ライセンスと出典については、パッケージ内の `LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。

## 新しい会話の始め方

1. `generic-workflow.md` を開きます。
2. 全文をコピーして、新しい AI の会話に貼り付けます。
3. 同じメッセージか次のメッセージで、要望と使用したい言語を伝えます。

AI の最初の有効な返答ではワークフローモードを決定し、そのモードの質問と承認の規則に従います。重要な進捗は保存してください。会話だけのホストでは Generic 自体がファイルを直接編集したりテストを実行したりすることはできず、追加操作はホストが実際に提供するツールに限られます。

新しい会話では毎回 `generic-workflow.md` をもう一度貼り付けます。設定方法、モード選択、セッション動作、機能上の制限は [Generic 詳細ガイド](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides/generic.ja.md)を参照してください。

## Full または Lite を選ぶ

Full は一度に一つの要件質問だけを行い、3 つの承認点を使います。Lite は質問が不要な場合があります。阻害要因が残る場合は各回最大 3 つの阻害要因に関する質問を行い、その後 1 つの Change Brief を提示して実装前に 1 回の承認を待ちます。選択前に [Full と Lite の完全なワークフローガイド](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides/getting-started-simple.ja.md)を参照してください。


[README に戻る](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/README.md)
