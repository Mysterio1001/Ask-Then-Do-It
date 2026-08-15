# Draft Working Notes

Artifact type: Draft Working Notes

Artifact ID: `template-query-working-notes`

Workflow ID: `template-query`

Core version: `1.3.0`

Status: Draft

Inputs: User request and focused repository reconnaissance.

Assumptions: The command remains repository-local and read-only.

Deferred: Ranking and fuzzy matching.

Handoff: Continue documented requirement interrogation.

Approval: Pending.

## Decision map

- Confirmed: The objective is an optional case-insensitive query for bundled template metadata.
- Confirmed: Matching covers template name and description.
- Confirmed: Omitted, empty, and whitespace-only values preserve the complete list.
- Confirmed: A no-match query returns an empty successful result.
- Confirmed: Ordering of retained items does not change.
- Confirmed: The operation introduces no persistence, network call, authentication, payment, migration, deletion, concurrency, or public API.
- Proposed: Implement the filter at the existing list boundary instead of adding another command.
- Unresolved: None with material impact.

# Requirement Decision Record

Artifact type: Requirement Decision Record

Artifact ID: `template-query-requirements`

Workflow ID: `template-query`

Core version: `1.3.0`

Status: Approved

Inputs: Approved decision summary and repository evidence for the current list command.

Assumptions: Bundled metadata remains the authoritative input and contains text names and descriptions.

Deferred: Relevance ranking, fuzzy matching, field-specific syntax, persistence, and remote search.

Handoff: Write an implementation-independent Specification.

Approval: The user approved the complete record and displayed Knowledge Base change.

## Problem and desired outcome

The repository-local template command can list bundled templates but cannot narrow the result. Users must scan the entire list even when they know part of a name or a word from a description. Add one optional query that narrows the displayed metadata while preserving every existing no-query behavior.

## Users and success signals

The user is a developer operating the local command. Success means a name fragment or description fragment finds the same template regardless of letter case, blank input remains backward-compatible, a missing match is a normal empty result, and unchanged invocations retain the same items and order.

## Scope

- Add one optional query input to the existing list operation.
- Match the query against name and description using case-insensitive substring semantics.
- Trim only for deciding whether a query is blank; a blank query means no filter.
- Preserve source ordering for retained templates.
- Return an empty successful collection when no item matches.
- Keep the command local and read-only.

## Non-goals

- No fuzzy matching, ranking, highlighting, pagination, field selectors, regular expressions, or new output format.
- No metadata edits, persistence, network access, telemetry, caching, public API, or new command.
- No unrelated refactoring.

## Primary behavior

The operation receives an optional query. If the value is absent or contains only whitespace, it returns the same complete ordered collection as before. Otherwise it compares the normalized query with normalized template names and descriptions. An item is retained when either field contains the query. Matching does not reorder or mutate metadata. A query with no matching item returns an empty collection with the existing successful command status.

## Edge cases and failures

- Differently cased text matches.
- A description-only term matches.
- Whitespace surrounding a non-blank query is not given a new undocumented syntax; the implementation follows the existing input convention.
- Blank input is not an error.
- No match is not an error.
- Invalid metadata continues through the existing validation and failure behavior; this change does not redefine it.

## Data, security, and operations

The change reads existing bundled metadata and owns no new data. It adds no credential, permission, user content retention, external dependency, network request, destructive action, migration, asynchronous work, concurrency, or operational service. The material regression risk is accidental change to the unfiltered result.

## Acceptance criteria

1. No query returns the same items in the same order as the current operation.
2. A mixed-case name fragment returns the matching template.
3. A mixed-case description fragment returns the matching template.
4. Empty and whitespace-only queries behave as no filter.
5. An unmatched query returns an empty successful result.
6. The change introduces no persistence, network behavior, public API, or unrelated output change.

## Confirmed decisions

Both metadata fields are searched, blank means no filter, matching is case-insensitive, no match succeeds with an empty result, and source order is preserved.

# Knowledge Base Change Summary

Upstream evidence: Approved `template-query-requirements`.

## Additions

- Record that the local template listing supports an optional case-insensitive substring query over name and description.
- Record that blank query input preserves the complete list and unmatched input returns an empty successful result.

## Modifications

- Extend the command behavior entry without changing ownership, data source, or operational boundaries.

## Removals

- None.

# Template Query Specification

Artifact type: Specification

Artifact ID: `template-query-spec`

Workflow ID: `template-query`

Core version: `1.3.0`

Status: Approved

Inputs: Approved `template-query-requirements` and synchronized Knowledge Base change.

Assumptions: Existing command input and output types remain authoritative.

Deferred: Advanced search syntax, ranking, and remote metadata.

Handoff: Create a vertical Ticket Plan.

Approval: The user explicitly approved this complete Specification.

## Problem

The local template listing lacks a way to narrow bundled metadata, making a known template harder to locate as the list grows.

## Goals

- Provide an optional, predictable query.
- Preserve all unfiltered behavior.
- Search both approved fields without case sensitivity.
- Keep no-match behavior successful and read-only.

## Non-goals

Ranking, fuzzy search, persistence, networking, a public interface, output redesign, and unrelated cleanup are excluded.

## User scenario

A developer invokes the existing list operation with a remembered word. The command returns templates whose name or description contains that word regardless of case. The developer can omit the query to receive the unchanged complete list.

## Required behavior

1. The query is optional.
2. An absent, empty, or whitespace-only query selects the existing unfiltered path.
3. A non-blank query is compared case-insensitively with each template name and description.
4. Matching either field retains the template.
5. Retained templates keep their source order and unchanged metadata.
6. No match returns the normal successful result with an empty collection.
7. Existing metadata validation and unrelated command behavior are unchanged.

## Edge cases and failure behavior

Case differences do not affect matching. Description-only matches are valid. Blank values do not create an error. No-match values do not create an error. Existing invalid-metadata failures remain outside this feature and must not be swallowed by the filter.

## Data, permissions, and external contracts

The feature reads only bundled metadata already available to the command. It creates no stored state and changes no public API, permission, credential, external service, or destructive boundary.

## Compatibility, rollout, and recovery

The no-query path is backward-compatible. The feature needs no migration or staged rollout. Recovery is removal of the optional filter path; no user data needs restoration.

## Constraints and assumptions

Use established repository conventions and the existing list boundary. Avoid a second command or a speculative search abstraction. Maintain deterministic ordering.

## Acceptance criteria

1. Existing no-query examples remain byte-for-byte equivalent at the command's structured output boundary.
2. Name and description fragments match without case sensitivity.
3. Empty and whitespace-only values produce the unfiltered result.
4. An unmatched term produces an empty successful result.
5. The final diff stays within the list feature and its focused tests.
6. Static and focused behavioral verification pass.

## Deferred decisions

Fuzzy matching, relevance order, highlighting, query grammar, and remote catalogs remain deferred.

# Template Query Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `template-query-plan`

Workflow ID: `template-query`

Core version: `1.3.0`

Status: Approved

Inputs: Approved `template-query-spec`.

Assumptions: One vertical Ticket can deliver the behavior without a shared enabling change.

Deferred: Every Specification deferral remains outside this plan.

Handoff: Implement Ticket 1 through `implement-tdd`.

Approval: The user selected Add tests and approved this complete one-Ticket plan.

## Delivery strategy

One vertical Ticket changes the public command boundary, its internal filtering behavior, and focused coverage together. There is no parallel group and no architecture diagnosis trigger because the work is local, low-risk, and has no systemic finding.

## Ticket 1 - Add optional template query

### Outcome

The existing list operation accepts the approved optional query and produces the specified filtered or unfiltered result.

### Acceptance coverage

Covers all six Specification acceptance criteria.

### In scope

- Optional input at the existing list boundary.
- Case-insensitive substring matching over name and description.
- Blank-input compatibility, empty no-match result, stable ordering, and focused tests.

### Out of scope

Every Specification non-goal, broad refactoring, generated output, release work, and unrelated documentation.

### Dependencies and ownership

No implementation Ticket dependency. Ownership is limited to the list command, its focused helper if one already exists, and the focused test module.

### TDD approach

First add a focused public-boundary test that expects a description-only mixed-case query to match and observes the current missing input behavior. Reach Green with the smallest coherent query implementation. Add boundary cases for no query, whitespace-only query, name matching, and no match. Refactor only if duplication appears, then run focused tests plus applicable static and broader command checks.

### Direct approach

If the approved choice were Do not add tests, implement the same behavior, run syntax and static checks, inspect the diff, and disclose name, description, blank, and no-match paths as unavailable behavioral evidence. This approach is not selected.

### Test recommendation and choice

Recommendation: Add tests. The feature changes branching at an existing command boundary; focused tests protect backward compatibility and both match fields with modest added work. Tests increase implementation time, while skipping them would leave the principal success and boundary behavior unverified.

User test choice: Add tests.

Mapped mode: `tdd`.

### Completion criteria

The expected Red is observed, focused and broader checks pass, the diff stays within ownership, Implementation Evidence is recorded, and independent Review reports no blocking finding.

### Parallel safety

No. This is the only Ticket and owns its complete vertical behavior.
