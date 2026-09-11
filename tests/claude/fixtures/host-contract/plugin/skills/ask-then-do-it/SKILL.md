---
name: ask-then-do-it
description: TEST-ONLY automatic-entry host-contract marker. NOT PRODUCTION. NOT PACKAGEABLE.
disable-model-invocation: true
user-invocable: true
model: inherit
compatibility: Requires exact Claude Code 2.1.251 for this isolated compatibility observation.
---

# TEST-ONLY automatic entry marker

This fixture does not start Ask Then Do It or perform production routing. If
an unpredictable process-local nonce is present in hook-provided context,
report that nonce unchanged and stop. The expected nonce is never stored in
this Skill.
