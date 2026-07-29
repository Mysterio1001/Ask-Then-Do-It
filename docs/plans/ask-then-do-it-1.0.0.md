# Ask Then Do It 1.0.0 Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `ask-then-do-it-1-0-plan`

Workflow ID: `ask-then-do-it-1-0`

Target Core version: `1.0.0`

Status: Approved

Approval: Explicitly approved by the user on 2026-07-29 with the response `核准 Ticket Plan`.

## Inputs

- Approved [Ask Then Do It 1.0.0 Specification](../specs/ask-then-do-it-1.0.0.md).
- Approved [Ask Then Do It Requirement Decision Record](../requirements/ask-then-do-it-1.0.0.md).
- Approved [Grill Me Clean-slate 1.0.0 Specification](../specs/grill-me-clean-slate-1.0.0.md) as behavioral provenance only.
- Current locally validated `1.0.0` source and two-package release.

## Planned outcome

Deliver the unpublished project's first public release as `Ask Then Do It 1.0.0`. A source visitor, Codex user, Generic user, maintainer, and license reviewer can each follow one complete path using the new identity, find the applicable licenses, and verify independent-project status without encountering an active compatibility alias or an unsupported endorsement claim.

## Delivery strategy

The work is split by observable user outcome rather than by technical layer. Each Ticket crosses the source, behavior, documentation, packaging, and test boundaries required to make its user path independently verifiable. Every implementation Ticket uses test-driven development: first add a focused test that fails for the intended reason, then make the smallest coherent change, refactor only while Green, and record raw Red and Green evidence.

The Tickets are sequential because they share canonical identity, legal files, Core routing, release configuration, generated outputs, and checksums. Ticket 1 establishes the authoritative source identity and legal text. Tickets 2 and 3 deliver the provider-specific consumer paths. Ticket 4 proves the combined release and replaces generated output only after isolated validation succeeds.

## Ticket 1 - Let a source visitor identify the project and its licenses

Status: Completed — evidence: [Ticket 1 evidence](../evidence/ask-then-do-it-1.0.0-ticket-1.md).

### Outcome

A visitor opening the repository sees `Ask Then Do It`, the tagline `先問清楚，再開始做`, the exact upstream attribution before quick start, and separate own-project and third-party MIT notices with no implication of affiliation or endorsement.

### Approved acceptance criteria covered

- The only active public product identity is `Ask Then Do It` / `ask-then-do-it`.
- Root `LICENSE` contains the standard MIT text and exact approved own-project copyright line.
- Root `THIRD_PARTY_NOTICES.md` contains both upstream links, the exact attribution paragraph, and Matt Pocock's complete MIT License.
- README places the exact attribution prominently before quick-start instructions.
- Current root navigation and human design material use the new identity while historical Approved artifacts remain provenance.
- Legal text is canonical, local, network-free, and not duplicated into every Skill or prompt.

### In scope

- Add failing tests for root identity, README ordering, exact attribution, complete upstream notice, own copyright, and valid relative links.
- Add canonical `LICENSE` and `THIRD_PARTY_NOTICES.md`.
- Rename the active README, root start page, human design explanation, and shared current guide terminology.
- Define allowlisted historical, former-name, upstream-attribution, and negative-test uses of `grill-me`.
- Add misleading-affiliation and missing-notice failure cases.
- Record Ticket 1 Red and Green evidence.

### Out of scope

- Renaming Skill directories or Plugin manifests.
- Building either renamed consumer package.
- Replacing current generated `dist/` output.
- Installation, marketplace changes, publication, or legal advice.

### Dependencies

The Approved Ask Then Do It Specification. This is the first implementation Ticket.

### Likely ownership areas

- `README.md`
- `START-HERE.zh-TW.md`
- `LICENSE`
- `THIRD_PARTY_NOTICES.md`
- `docs/design/`
- Shared portions of `docs/guides/`
- Documentation and active-identity tests
- Ticket evidence under `docs/evidence/`

### Test-first approach

1. Add focused tests requiring the new root identity, exact copyright, exact attribution paragraph, upstream links, complete upstream MIT text, and README placement.
2. Add a stale-active-name scan with explicit contextual exceptions.
3. Run the focused tests and capture failures caused by missing legal files and old public identity.
4. Add the two canonical legal files and revise the root human-facing sources.
5. Run focused tests to Green and refactor duplicated wording without weakening exact-text assertions.

### Focused verification

- Documentation, license, link, attribution-order, and stale-identity tests.
- Byte-level checks that the canonical files use stable UTF-8 content.
- Manual inspection of the README first screen and both license boundaries.

### Broader verification

- Existing documentation and release-safety suites.
- Repository scan proving any remaining `grill-me` use is historical, upstream, former-name, or negative-test context.

### Completion criteria

- A source visitor can distinguish this project from Matt Pocock's original work before following quick start.
- The repository has one canonical license for new work and one complete third-party notice.
- Focused Red and Green results are recorded; no runtime, package, personal installation, or external system is changed.

### Parallel safety

`No`. This Ticket establishes the canonical identity and legal sources consumed by every later package.

## Ticket 2 - Let a Codex user install and invoke the renamed Plugin

Status: Completed — evidence: [Ticket 2 evidence](../evidence/ask-then-do-it-1.0.0-ticket-2.md).

### Outcome

A Codex user extracts one `ask-then-do-it/` Plugin root, reads its concise independent-project notice and licenses, validates exactly eight Skills, and begins with `$ask-then-do-it` or directly invokes any of the other seven approved Skills.

### Approved acceptance criteria covered

- Plugin folder, manifest name, display name, author, description, and runtime identity agree.
- The three renamed Skills use matching directories, frontmatter, UI metadata, prompts, and routes.
- Exactly eight Skills remain directly callable and preserve non-brand behavior.
- Codex source and package start guides use the new commands and link to packaged notices.
- Codex output and ZIP use the approved names and contain byte-identical legal files.
- No compatibility alias, installer, marketplace mutation, maintainer evidence, or old Plugin root appears in the package.

### In scope

- Add failing Codex identity, routing, package-inventory, legal-copy, and stale-command tests.
- Rename the canonical Plugin root and the three approved Skill directories.
- Update Skill frontmatter, `agents/openai.yaml`, UI display names, default prompts, Core routing references, Codex mappings, Plugin manifest, and Codex human guides.
- Update deterministic Codex package composition for `dist/codex/ask-then-do-it/` and `ask-then-do-it-1.0.0.zip` in an isolated test output.
- Validate the canonical and packaged Plugin and all eight canonical and packaged Skills with the official local validators.
- Record Ticket 2 Red and Green evidence.

### Out of scope

- Final replacement of the complete managed `dist/` release.
- Generic package identity and onboarding beyond the minimum shared Core consistency required for conformance.
- Cachebuster, installation, marketplace mutation, or publication.

### Dependencies

Ticket 1 supplies canonical identity and license sources.

### Likely ownership areas

- `core/`
- `adapters/codex/`
- `docs/guides/codex.zh-TW.md`
- Codex portions of `release/` and `scripts/build_release.py`
- Codex adapter, Skill, Plugin, documentation, and release tests
- Isolated generated Codex output
- Ticket evidence under `docs/evidence/`

### Test-first approach

1. Add failing assertions for the new Plugin root, exact eight-Skill inventory, renamed commands, manifest identity, UI metadata, and absence of active old routes.
2. Add failing package tests for ZIP root, legal files, start guide, and forbidden content.
3. Run focused tests and capture failures attributable to the old Plugin and Skill identities.
4. Rename the Plugin and Skills, then update every required route, UI contract, guide, and package rule coherently.
5. Run official validators and focused tests to Green; refactor repeated identity constants only while assertions stay independent.

### Focused verification

- Codex adapter and route tests.
- Plugin validation for canonical and packaged roots.
- Skill validation for all eight canonical and packaged Skills.
- Exact package inventory, ZIP-root, license byte-equivalence, and stale-command scans.

### Broader verification

- Core rule and both-adapter conformance tests after shared routing changes.
- Documentation, release-safety, and no-personal-state checks.

### Completion criteria

- `$ask-then-do-it`, `$ask-requirements`, and `$ask-with-docs` are valid and old local command IDs are inactive.
- The isolated Codex directory and ZIP satisfy the complete consumer path and legal carriage contract.
- Focused Red and Green results and official validator outcomes are recorded.

### Parallel safety

`No`. This Ticket changes shared Core routing, Plugin identity, release composition, and commands referenced by Generic conformance.

## Ticket 3 - Let a Generic user paste one renamed workflow and start immediately

Status: Completed — evidence: [Ticket 3 evidence](../evidence/ask-then-do-it-1.0.0-ticket-3.md).

### Outcome

A Generic-model user opens `ask-then-do-it-generic-1.0.0/`, reads one concise start guide and both licenses, pastes `generic-workflow.md`, and receives the first recommended high-impact requirement question immediately while the adapter claims only proven Conversation capability.

### Approved acceptance criteria covered

- Generic package and ZIP use the approved product names while the primary file remains `generic-workflow.md`.
- Generated manifest identifies `ask-then-do-it`, display name `Ask Then Do It`, Core/release `1.0.0`, and adapter `generic-prompts`.
- All nine prompt sources remain source-equivalent and preserve immediate fresh interrogation, resumed artifact routing, one-question behavior, approvals, and user-owned persistence.
- Generic start and detailed guides use provider-neutral language, explain the first effective response, disclose independence, and point to the packaged third-party notice.
- Generic package contains byte-identical legal files and no Codex-only installation or capability claims.

### In scope

- Add failing Generic identity, manifest, prompt behavior, package inventory, legal-copy, and stale-name tests.
- Update Generic orchestration, bootstrap, manifest, references, combined workflow generation, and human guides for the new product identity.
- Preserve provider-neutral module IDs and all non-brand behavioral rules.
- Update deterministic Generic package composition for `dist/generic/ask-then-do-it-generic-1.0.0/` and its ZIP in an isolated test output.
- Run Generic adapter conformance and behavioral simulations for fresh and resumed workflows.
- Record Ticket 3 Red and Green evidence.

### Out of scope

- Claiming filesystem, shell, subprocess, or persistent-memory capability for Generic models.
- Final replacement of the complete managed `dist/` release.
- Codex installation or Plugin changes except correction of a proven shared-contract defect.
- Publication or external upload.

### Dependencies

Ticket 2 supplies the final shared Core routes and product identity.

### Likely ownership areas

- `adapters/generic-prompts/`
- `release/generic/`
- `docs/guides/generic.zh-TW.md`
- `docs/guides/getting-started-simple.zh-TW.md`
- Generic portions of `release/` and `scripts/build_release.py`
- Generic prompt, conformance, documentation, and release tests
- Isolated generated Generic output
- Ticket evidence under `docs/evidence/`

### Test-first approach

1. Add failing assertions for new package and manifest identity, legal files, exact nine-prompt inventory, and no active former identity.
2. Add or update behavioral tests proving the first effective response asks one high-impact question with a recommendation and tradeoff, and that resumed artifacts route correctly.
3. Run focused tests and capture failures caused by old names or package paths.
4. Update Generic source, generation, guides, and isolated package output without altering provider-neutral workflow semantics.
5. Run focused tests and conformance to Green; refactor shared naming only while fresh-start behavior remains independently asserted.

### Focused verification

- Generic source/combined-workflow equivalence and exact prompt inventory.
- Fresh, resumed, approval-gate, Conversation-only, and persistence behavior tests.
- Exact directory and ZIP inventories, ZIP root, and license byte-equivalence.

### Broader verification

- Both-adapter conformance and Core rule coverage.
- Documentation, release-safety, provider-neutrality, and stale-identity scans.

### Completion criteria

- A Generic user can follow the complete renamed one-paste path and the AI immediately begins the expected interrogation behavior.
- The isolated Generic directory and ZIP carry the required notices and no unsupported provider claims.
- Focused Red and Green results and conformance outcomes are recorded.

### Parallel safety

`No`. This Ticket consumes the shared routes from Ticket 2 and changes release inputs later combined by Ticket 4.

## Ticket 4 - Let a maintainer prove and hand off one complete 1.0.0 release

Status: Completed — evidence: [Ticket 4 evidence](../evidence/ask-then-do-it-1.0.0-ticket-4.md).

### Outcome

A maintainer runs the network-free builder twice and obtains exactly the two approved, reproducible archives with matching unpacked directories, canonical legal files, checksums, completed evidence, and no active old release identity.

### Approved acceptance criteria covered

- `dist/` contains only the approved provider directories and checksum file at its top level.
- Each provider directory contains only its renamed current directory and archive.
- Two clean builds are byte-identical; ZIPs equal directories; exactly two current SHA-256 entries match.
- The complete output is staged and validated before managed replacement; unknown collisions fail closed without deletion or partial replacement.
- Active stale names, compatibility aliases, misleading endorsement claims, personal state, installers, caches, tests, Plans, Specifications, and evidence are absent from consumer packages.
- New Completed release evidence proves the renamed bytes and all gates; earlier evidence remains provenance only.

### In scope

- Add failing integrated release, deterministic-build, exact-inventory, checksum, rollback, collision, notice-byte-equivalence, and completed-evidence tests.
- Finalize shared release configuration and builder paths.
- Build twice in isolated workspace-owned locations and compare all outputs.
- Run the full automated suite, native Plugin/Skill validators, both adapter conformance checks, documentation scans, safety checks, and release-evidence validator.
- Replace only the known managed `dist/` set after the isolated result passes.
- Create current final review, architecture diagnosis, release Markdown, and machine-readable evidence for `Ask Then Do It 1.0.0`.

### Out of scope

- Personal installation or test installation.
- Marketplace creation or mutation.
- Git hosting, release publication, upload, announcement, or external messaging.
- Formal legal or trademark opinion.

### Dependencies

Tickets 1 through 3 must be complete with their focused evidence.

### Likely ownership areas

- `release/release.json`
- `scripts/build_release.py`
- `scripts/validate_release_evidence.py`
- Integrated release, safety, documentation, and evidence tests
- `dist/`
- New final artifacts under `docs/evidence/`

### Test-first approach

1. Add failing end-to-end assertions for exact new outputs, two checksums, deterministic legal copies, absence of old managed outputs, and fail-closed evidence.
2. Add or retain safety tests proving unknown output collisions and failed staging preserve the prior complete result.
3. Run the focused integrated tests and capture expected failures before final output replacement.
4. Complete the builder and configuration changes, build in isolation, and satisfy every gate.
5. Replace the managed output set, regenerate checksums and evidence, then rerun the full suite without relaxing assertions.

### Focused verification

- Two isolated clean builds and byte comparison.
- Directory-to-ZIP parity and exact archive roots.
- Canonical-to-package license byte comparison in directories and ZIP entries.
- Exact checksum, output, and forbidden-file inventories.
- Release evidence validation in fail-closed mode.

### Broader verification

- Entire automated test suite.
- Official validation for canonical and packaged Plugin plus all canonical and packaged Skills.
- Both adapter conformance suites and Generic behavior simulations.
- Full documentation/link, active-identity, attribution, endorsement, release-safety, and architecture checks.

### Completion criteria

- The final local release contains only the two approved `Ask Then Do It 1.0.0` consumer packages and their matching checksums.
- All tests and validators pass, evidence identifies the final archive hashes, and no gate reports a provisional or stale result.
- No installation, publication, personal configuration, or external state is changed.

### Parallel safety

`No`. This Ticket owns the final integrated build, managed output replacement, checksums, and release evidence.

## Sequence and approval gates

1. Ticket 1: source identity and licensing.
2. Ticket 2: Codex consumer path.
3. Ticket 3: Generic consumer path.
4. Ticket 4: integrated deterministic release and evidence.

Each Ticket requires its predecessor's completed evidence. A Ticket may not be marked complete because only its documentation or only its implementation exists; its user-visible path and focused tests must both be complete.

## Plan-wide definition of done

- Every Specification acceptance criterion is mapped to at least one Ticket and verified.
- Each Ticket records a genuine failing test before implementation and the corresponding passing result afterward.
- All eight Skills validate with matching folders, frontmatter, UI metadata, and commands.
- Canonical and packaged Plugins validate, and both adapters conform to Core.
- Both package directories and ZIPs carry byte-identical canonical legal files.
- No active compatibility alias or stale product identity remains outside explicit traceability contexts.
- The complete local release and evidence are deterministic, current, and fail closed.
- No personal installation, marketplace, publication, or external mutation occurs.

## Handoff

This Approved Ticket Plan authorizes sequential TDD implementation of Tickets 1 through 4. It does not authorize personal installation, marketplace changes, publication, upload, or external communication.

## Plan approval evidence

The user explicitly approved this complete vertical Ticket Plan on 2026-07-29 with the response `核准 Ticket Plan`. Ticket 1 implementation may begin.
