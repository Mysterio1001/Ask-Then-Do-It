# Ask Then Do It claude-code 1.4.0

在 Claude Code 使用同一個 Plugin，即可取得一般 Claude 與 Claude 5 兩種流程設定。

下載並解壓縮完整 Plugin。每次從終端機啟動時加上：

```bash
claude --plugin-dir "/path with spaces/ask-then-do-it"
```

只對這次工作階段生效（session-only）；之後每次都要再加 `--plugin-dir`，不建立持久 Marketplace 安裝。

[使用說明](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0/docs/guides/claude-code.zh-TW.md)

## 開始使用

```text
/ask-then-do-it:ask-then-do-it 幫我建立一個預約網站，請使用繁體中文。
```

**Full** 適合需要需求、規格與工作規劃紀錄的工作，實作前有三個核准點。**Lite** 適合範圍清楚的改動，使用簡短變更摘要與一次核准。

[初學者流程](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0/docs/guides/getting-started-simple.zh-TW.md)

本專案受到 Matt Pocock 的 skills repository 啟發，與其沒有從屬或背書關係。授權與來源請見 `LICENSE` 與 `THIRD_PARTY_NOTICES.md`。

[回到 README](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0/README.md)
