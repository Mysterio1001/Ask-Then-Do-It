# Ask Then Do It Generic 1.3.1 Guide

This package is for Gemini and other AI services that accept long text. It guides the workflow through conversation and can use only the file, command, or other tools that the host actually provides.

This independent project was inspired by Matt Pocock's skills repository. It is not affiliated with or endorsed by Matt Pocock. See `LICENSE` and `THIRD_PARTY_NOTICES.md` in this package for license and attribution information.

## Start every new conversation

1. Open `generic-workflow.md`.
2. Paste the entire file into a new AI conversation.
3. In the same message or the next one, describe your request and preferred language.

The AI's first effective response resolves the workflow mode and follows that mode's question and approval rules. Save important progress. On a conversation-only host, Generic cannot directly edit your files or run tests; any additional action depends on tools the host actually provides.

Paste `generic-workflow.md` again in each new conversation. For setup, mode selection, session behavior, and capability limits, see the [detailed Generic guide](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.1/docs/guides/generic.en.md).

## Choose Full or Lite

Full uses exactly one requirement question at a time and three approval gates. Lite may ask no questions; when blockers remain, it asks at most three blocking questions per round, then presents one Change Brief and waits for one approval before implementation. See the [complete Full and Lite workflow guide](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.1/docs/guides/getting-started-simple.en.md) before choosing.


[Back to README](https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.1/README.md)
