## Requirement question 1

The existing command exposes template names and descriptions. Should the new query match only names, or both names and descriptions? I recommend both fields because users often remember a template's purpose rather than its title; the tradeoff is that broad terms can return more results.

## Requirement question 2

The existing invocation lists every template. Should an omitted, empty, or whitespace-only query preserve that behavior or be rejected? I recommend treating all three as no filter for backward compatibility; rejection would add a new failure path without protecting data.
