# Ask Then Do It claude-code 1.4.2

一つの Claude Code Plugin に、一般 Claude と Claude 5 のワークフロープロファイルが含まれます。

完全な Plugin をダウンロードして展開します。ターミナルから起動するたびに次を指定します。

```bash
claude --plugin-dir "/path with spaces/ask-then-do-it"
```

そのセッションだけに有効です（session-only）。次回も `--plugin-dir` が必要で、永続的な Marketplace インストールにはなりません。

[使用ガイド](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.2/docs/guides/claude-code.ja.md)

## 使い始める

```text
/ask-then-do-it:ask-then-do-it 予約サイトの開発を手伝ってください。日本語で進めてください。
```

**Full** は要件、仕様、Ticket 計画を保存し、実装前に三つの承認を求めます。**Lite** は範囲が明確な変更向けで、短い変更概要と一度の承認を使います。

[初心者向けガイド](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.2/docs/guides/getting-started-simple.ja.md)

本プロジェクトは Matt Pocock の skills repository に着想を得た独立プロジェクトです。Matt Pocock との所属関係や同氏による承認はありません。`LICENSE` と `THIRD_PARTY_NOTICES.md` を参照してください。

[README に戻る](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.2/README.md)
