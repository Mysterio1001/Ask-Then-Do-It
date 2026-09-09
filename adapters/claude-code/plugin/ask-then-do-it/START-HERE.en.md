# Ask Then Do It Claude Code Plugin 1.4.0-preview.1

**Opt-in public preview.** Keep the complete Plugin folder together. Stable Codex and Generic remain on 1.3.1. The linked release instructions apply after preview publication; if unavailable, wait.

The compatibility target is Claude model 4.6+, Claude Code 2.1.251+, and Node.js 22+ for automatic routing. Verification covers native strict validation and local automated tests. Real official Claude session verification is deferred.

After a verified installation or explicitly selected local test session, use one of the two supported entries yourself:

```text
/ask-then-do-it:ask-then-do-it Help me build...
/ask-then-do-it:ask-then-do-it-5 Help me build...
```

Both preserve the active model. The second explicitly selects the Claude 5 path subject to model and host checks. Internal stages are not public commands.

Use the immutable same-version [detailed Claude Code guide](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0-preview.1/docs/guides/claude-code.en.md) for Full/Lite, routing, Config, opt-in Marketplace installation, updates, removal, reviewer limits, platforms, session-only ZIP recovery, and feedback. ZIP use with `--plugin-dir` does not create a persistent installation.

This independent project was inspired by Matt Pocock's skills repository and is not affiliated with or endorsed by Matt Pocock. The matching package includes `LICENSE` and `THIRD_PARTY_NOTICES.md`.

[Back to README](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0-preview.1/README.md)
