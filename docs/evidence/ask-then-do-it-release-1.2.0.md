# Ask Then Do It Release 1.2.0 Evidence

Artifact type: Implementation Evidence

Artifact ID: `ask-then-do-it-release-1.2.0-evidence`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Release version: `1.2.0`

Status: Completed

Inputs: Approved [1.2.0 Specification](../specs/command-install-update-1.2.0.md), completed [Ticket Plan](../plans/command-install-update-1.2.0.md), Tickets 1-5 evidence and Reviews, [Release Architecture Diagnosis](ask-then-do-it-1.2.0-release-architecture-diagnosis.md), and [validation ledger](ask-then-do-it-release-1.2.0.json).

Assumptions: This is local release evidence. It does not claim a Git tag, GitHub Release, live installation, publication, upload, or personal marketplace mutation.

Deferred: External publication and announcement, live target-CLI verification, external CI, additional operating systems, unattended updates, and optional Draft architecture proposals.

Handoff: Maintainer-controlled inspection, tagging, publication, and installation decisions.

## Outcome

Ask Then Do It `1.2.0` is locally complete as the first command-installable release. The repository marketplace exposes exactly the official tag-pinned Plugin, the three languages document equivalent state-aware AI-first installation/update behavior with ZIP fallback, and the Plugin carries the approved transparent red seahorse-question-mark icon and logo. Deterministic Codex and Generic packages agree on `1.2.0`; marketplace metadata remains repository-only.

## Validation

- Final full automated discovery: `Ran 113 tests in 7.758s`; `OK`.
- Marketplace validation passed.
- Canonical and packaged Plugin validation passed.
- All 18 canonical/packaged Skill validations passed.
- Codex and Generic conformance passed against Core `1.2.0`.
- Release tests passed for version lockstep, asset metadata/transparency, README whitelist, localized command parity, deterministic builds, prior-release atomic upgrade, ZIP equivalence, checksums, package inventories, exclusions, and evidence gates.
- Icon and logo were visually inspected on transparent rendering and remain centered, padded, recognizable, and unclipped.
- Final Review has no blocking finding. Architecture diagnosis is Draft and authorizes no refactor.

## Package layout

```text
dist/
|- codex/
|  |- ask-then-do-it/
|  `- ask-then-do-it-1.2.0.zip
|- generic/
|  |- ask-then-do-it-generic-1.2.0/
|  `- ask-then-do-it-generic-1.2.0.zip
`- checksums.sha256
```

## Archive hashes

```text
c5b19837336ba1ac54407a1d0878a1d552921ba45e4e9adafcf0c1a2013048f2  codex/ask-then-do-it-1.2.0.zip
b9b27fafddd80f60b4e2818f3d61757146973d41bee345a65d00ef1b18e99af0  generic/ask-then-do-it-generic-1.2.0.zip
```

## Publication boundary

No Plugin installation, personal marketplace change, Git tag, GitHub Release, push, upload, announcement, background updater, alternate source, or automatic downgrade occurred.
