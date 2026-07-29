# GitHub Release 1.0.0 Ticket 2 Evidence

Artifact type: Implementation Evidence

Artifact ID: `ask-then-do-it-github-release-1-0-ticket-2`

Workflow ID: `ask-then-do-it-github-release-1-0`

Status: Completed

## Red

The updated README contract test failed because both Chinese and English quick starts still referenced local `dist/` paths.

## Green

- Both README languages now use clickable GitHub Release asset URLs under `Mysterio1001/Ask-Then-Do-It` and tag `v1.0.0`.
- No README download entry uses a local `dist/` path.
- Attribution remains before quick start and maintainer build instructions remain separate.
- Complete verification passed: `Ran 58 tests ... OK`.

## Boundary

The external links are intentionally expected to become live only after Ticket 3 publication. No tag, GitHub Release, or asset was created by this Ticket.
