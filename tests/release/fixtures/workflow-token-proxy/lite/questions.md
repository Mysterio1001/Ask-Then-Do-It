1. Should a query match only the template name, or both the name and description? I recommend matching both fields so users can find a template by purpose as well as title; the tradeoff is that a broad term may return more results.

2. How should an empty or whitespace-only query behave? I recommend treating it as no filter so existing callers and interactive users keep the current complete list; rejecting it would add a new failure case without protecting data.
