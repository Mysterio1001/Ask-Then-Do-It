# Ask Then Do It 1.0.0 GitHub Release Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `ask-then-do-it-github-release-1-0-plan`

Workflow ID: `ask-then-do-it-github-release-1-0`

Target release: `v1.0.0`

Repository: `https://github.com/Mysterio1001/Ask-Then-Do-It`

Status: Approved

Approval: Explicitly approved by the user on 2026-07-29 with the response `繼續往下執行`.

## Planned outcome

Keep generated release output out of normal Git history, direct users from the repository README to stable GitHub Release downloads, and publish the two validated `Ask Then Do It 1.0.0` archives as release assets without changing their bytes.

## Ticket 1 — Keep generated and local-only files out of Git

Status: Completed — evidence: [Ticket 1 evidence](../evidence/github-release-1.0.0-ticket-1.md).

### User-visible outcome

A contributor can clone the repository without receiving generated packages, Python caches, virtual environments, secrets, or local test output. The repository still contains every canonical source required to rebuild the release.

### Scope

- Create root `.gitignore`.
- Ignore `dist/`, `__pycache__/`, `*.py[cod]`, `.venv/`, `venv/`, `.env`, common test caches, and known isolated build-output patterns.
- Do not ignore canonical source, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `requirements-dev.txt`, documentation, tests, release configuration, or builder scripts.
- If generated `dist/` files are already tracked, remove them from the Git index without deleting the validated local files.
- Add deterministic tests or checks proving required source remains trackable and generated/local-only files are ignored.

### Acceptance criteria

- `git check-ignore` identifies representative generated, cache, virtual-environment, and secret paths.
- `git check-ignore` does not match the five root project files or canonical source directories.
- `dist/` is not staged as repository content after the index cleanup.
- Both validated ZIPs remain available locally for Ticket 3.
- No personal Codex, marketplace, credential, or external repository state is changed.

### Dependencies and safety

This is the first Ticket. Index cleanup must use a cache-only Git operation so local release files remain intact.

## Ticket 2 — Route README downloads to GitHub Releases

Status: Completed — evidence: [Ticket 2 evidence](../evidence/github-release-1.0.0-ticket-2.md).

### User-visible outcome

A visitor opening the README can download either consumer package from GitHub Releases without navigating generated repository directories.

### Scope

- Replace README references to `dist/codex/ask-then-do-it-1.0.0.zip` with:
  `https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.0/ask-then-do-it-1.0.0.zip`.
- Replace README references to `dist/generic/ask-then-do-it-generic-1.0.0.zip` with:
  `https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.0/ask-then-do-it-generic-1.0.0.zip`.
- Keep source-building instructions clearly separated for maintainers.
- Update documentation tests so release download URLs, filenames, ordering, attribution, and relative documentation links remain protected.
- Do not change generated ZIP bytes.

### Acceptance criteria

- Both Traditional-Chinese and English README paths use clickable HTTPS GitHub Release links.
- The URLs use the confirmed repository, tag `v1.0.0`, and exact asset filenames.
- README attribution remains before quick start.
- Documentation and link-contract tests pass without requiring the Release to exist during offline unit tests.
- No `dist/` download path remains in README.

### Dependencies and safety

Depends on Ticket 1 establishing that `dist/` is generated and untracked. The links become externally resolvable only after Ticket 3 succeeds.

## Ticket 3 — Publish the two validated ZIP assets

Status: Planned

### User-visible outcome

GitHub Release `v1.0.0` exposes exactly the two approved consumer archives, and each README download link returns the same bytes validated locally.

### Release assets

- `dist/codex/ask-then-do-it-1.0.0.zip` uploaded as `ask-then-do-it-1.0.0.zip`.
- `dist/generic/ask-then-do-it-generic-1.0.0.zip` uploaded as `ask-then-do-it-generic-1.0.0.zip`.

### Scope

- Verify the working tree and intended commit contain Tickets 1 and 2 plus the completed `Ask Then Do It 1.0.0` source.
- Rebuild and rerun the complete local validation gate before publication.
- Verify the two local archive hashes against `dist/checksums.sha256`.
- Confirm GitHub CLI authentication, repository ownership, target branch, tag `v1.0.0`, release title, and release notes.
- Request explicit human publication approval immediately before creating or mutating the GitHub Release.
- Create the GitHub Release or fail safely if the tag or release already exists unexpectedly.
- Upload exactly the two named ZIP assets without altering or recompressing them.
- Download or inspect the published asset metadata and verify both published SHA-256 values match the local validated archives.

### Acceptance criteria

- Release page: `https://github.com/Mysterio1001/Ask-Then-Do-It/releases/tag/v1.0.0` exists.
- Exactly one asset named `ask-then-do-it-1.0.0.zip` exists and matches local SHA-256 `3f7b83d697cb5d431693d76cce79500622d1fd4db45828317b71c5e03e817721`.
- Exactly one asset named `ask-then-do-it-generic-1.0.0.zip` exists and matches local SHA-256 `a65d8c0282ba2b3ec51b891ae26255aaef1031673bddf29ac8dfc41ef6b7f436`.
- Both README download URLs return their matching asset.
- No source archive, unpacked `dist/` directory, credential, cache, personal configuration, or additional unapproved asset is published.
- Publication evidence records the tag, release URL, asset names, asset IDs or URLs, local hashes, and verification results.

### Dependencies and safety

Depends on Tickets 1 and 2, a committed and pushed source state, valid GitHub authentication, and explicit approval at the publication boundary. Creating a tag, Release, or uploaded asset is an external side effect and is not authorized merely by approving implementation of Tickets 1 and 2.

## Sequence

1. Ticket 1: repository hygiene and cache-only untracking.
2. Ticket 2: stable README download links.
3. Ticket 3: validated external GitHub Release publication.

## Plan approval gate

This Approved plan authorizes implementation of Tickets 1 and 2. Ticket 3 additionally requires a final explicit publication confirmation immediately before any GitHub Release mutation.
