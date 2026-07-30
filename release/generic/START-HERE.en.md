# Ask Then Do It Generic 1.0.1 Guide

This package is for Gemini and other AI services that accept long text. Paste the workflow into a conversation to begin with requirements discovery.

This independent project was inspired by Matt Pocock's skills repository. It is not affiliated with or endorsed by Matt Pocock. See `LICENSE` and `THIRD_PARTY_NOTICES.md` in this package for license and attribution information.

## Start every new conversation

1. Open `generic-workflow.md`.
2. Copy the entire file and paste it into a new AI conversation.
3. In the same message or the next one, describe your request and preferred language.
4. To continue earlier work, also paste the important documents you saved from that work.

The AI's first effective response will briefly state the current stage, then ask the first requirements question with a recommended answer and the main tradeoff.

## What to expect

- The AI asks one important question at a time.
- Requirements, the specification, and the Ticket plan each need your explicit approval.
- Implementation begins only after you approve the Ticket plan.
- Review distinguishes what can be verified from what cannot be verified with the supplied information.

## Capability limits

The Generic package guides the workflow through conversation. It cannot edit files or run tests by itself. If your AI service provides file or tool access, use only the capabilities that service actually makes available.

## Save your progress

Save the requirements record, specification, Ticket plan, Review, and other important documents produced by the AI.

Paste `generic-workflow.md` again in every new conversation. To continue earlier work, also paste the saved documents and your new request. The AI will continue from the first unfinished stage.

## Advanced use

The `prompts/` folder contains nine stage-specific modules. Once you know the workflow, you may select a module directly. For normal use, start with `generic-workflow.md`.
