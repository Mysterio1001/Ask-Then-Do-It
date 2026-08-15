# Change Brief

## Objective

Add an optional case-insensitive query filter to the repository-local command that lists bundled template metadata.

## In scope

- Accept an optional query without changing the existing invocation.
- Match a non-blank query against both template name and description, without case sensitivity.
- Treat an omitted, empty, or whitespace-only query as no filter.
- Return an empty successful result when no template matches.

## Non-goals

- No ranking, fuzzy matching, persistence, network access, public API, or output-format redesign.
- No unrelated refactor and no new or modified test files in Lite.

## Acceptance scenarios

1. With no query, the complete list and its ordering are unchanged.
2. A differently cased name fragment returns the matching template.
3. A description-only fragment returns the matching template.
4. Whitespace-only input behaves like no query.
5. A term with no matches returns an empty successful result.

## Material risks

Risk is low. The command reads bundled metadata only and has no authentication, authorization, payment, migration, destructive operation, public contract, concurrency, asynchronous behavior, external side effect, or persisted state. The main regression risk is accidentally changing unfiltered output.

## Intended validation

Inspect status and diff, run applicable syntax and static checks, execute an existing focused success-path check for case-insensitive matching, and execute an existing boundary-path check for blank or unmatched input. If those checks are unavailable, perform equivalent local smoke checks and disclose the limitation.
