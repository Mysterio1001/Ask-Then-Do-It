# GitHub Release 1.0.0 Ticket 1 Evidence

Artifact type: Implementation Evidence

Artifact ID: `ask-then-do-it-github-release-1-0-ticket-1`

Workflow ID: `ask-then-do-it-github-release-1-0`

Status: Completed

## Red

Root `.gitignore` was absent and Python `__pycache__` directories appeared as untracked content.

## Green

- Added root `.gitignore` for generated `dist/`, Python caches, virtual environments, local environment files, validation output, editor files, and operating-system files.
- Verified canonical root files and source directories are not ignored.
- Removed `dist/` from the Git index with a cache-only operation.
- Verified `git ls-files -- dist` returns no tracked files.
- Verified both validated local ZIPs remain on disk with their approved hashes.
- No local package, credential, marketplace, or external repository content was deleted.
