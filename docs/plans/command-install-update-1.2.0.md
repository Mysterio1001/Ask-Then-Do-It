# Ask Then Do It 1.2.0 指令安裝、更新與 Plugin 圖示 Ticket Plan

Artifact type: Ticket Plan

Artifact ID: `command-install-update-1-2-plan`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Target release version: `1.2.0`

Status: Approved

Inputs: Approved [1.2.0 Specification](../specs/command-install-update-1.2.0.md), Approved [Requirement Decision Record](../requirements/command-install-update-1.2.0.md), and Approved [Project Knowledge Base](../project/knowledge-base.md).

Assumptions: The user owns every Ticket test choice and there is no default. Adding tests maps internally to `tdd`; declining tests maps internally to `direct`. Target CLI behavior cannot be live-tested in the current environment unless `codex.exe` becomes executable, so official documentation, static contracts, package validation, and ZIP fallback remain required evidence.

Deferred: OpenAI universal public Plugins Directory, background updates, private fork support, `logoDark`, actual Git tag／GitHub Release／push／upload／announcement, and live target-CLI verification when unavailable.

Handoff: Collect all test choices in one response, display the complete mapped plan, request explicit Plan approval, then route each Approved Ticket by its selected mode.

Approval: 使用者於 2026-08-14 在完整 Ticket definitions、依賴順序、所有測試建議與五張 Ticket 的 `tdd` mapping 展示後明確回覆「核准」。

## Planned outcome

Deliver a locally complete Ask Then Do It `1.2.0` release that exposes a tag-pinned official GitHub marketplace, documents a state-aware AI-first installation/update flow, preserves ZIP fallback, includes validated transparent Plugin assets, maintains the approved README boundary, and blocks inconsistent release output.

## Test-time warning and recommendations

Adding tests increases work because each selected Ticket must establish Red before production changes, reach focused Green, refactor under coverage, and run broader verification. Declining tests reduces behavioral verification confidence and leaves the listed behavior checks unavailable; non-test validators, static inspection, image inspection, builds, and Review still apply where permitted.

| Ticket | Outcome | Recommendation | Added work | User test choice |
| --- | --- | --- | --- | --- |
| 1 | Official tag-pinned repository marketplace | Add tests | Medium | Add tests (selected; internal `tdd`) |
| 2 | Transparent Plugin icon/logo and manifest packaging | Add tests | Medium | Add tests (selected; internal `tdd`) |
| 3 | State-aware English, Traditional Chinese, and Japanese install/update documentation | Add tests | Medium | Add tests (selected; internal `tdd`) |
| 4 | Lockstep `1.2.0` release identity and deterministic packages | Add tests | High | Add tests (selected; internal `tdd`) |
| 5 | Integrated release validation, evidence, and milestone diagnosis | Add tests | High | Add tests (selected; internal `tdd`) |

Recommendations are advisory. The user explicitly selected tests for Tickets 1-5 on 2026-08-13. The Plan remains Draft until the complete mapped Plan receives explicit approval.

## Conditional execution policy

- A Ticket with tests added follows its TDD approach, records valid Red before production changes, reaches focused Green, and runs broader risk-proportional verification.
- A Ticket without tests must not create, modify, or execute behavioral tests. Its listed behavioral checks become unavailable evidence; permitted non-test validation and Review still apply.
- Native Plugin/Skill validation, JSON/YAML parsing, deterministic builds, image metadata/visual inspection, checksum verification, `git diff --check`, and final-diff inspection are treated according to their purpose and the selected implementation skill; behavioral regression suites remain prohibited for a direct Ticket.
- Changing any test choice after Plan approval returns the Plan to Draft and requires reapproval before the affected Ticket continues.

## Delivery strategy

Tickets 1, 2, and 3 each deliver an observable contract in separate ownership areas and are parallel-safe after Plan approval when explicitly delegated: Ticket 1 owns marketplace metadata and its focused contract checks; Ticket 2 owns visual assets, Plugin interface, and asset packaging checks; Ticket 3 owns localized install/update documentation and README-preservation checks. Ticket 4 integrates all three into the lockstep `1.2.0` release. Ticket 5 runs combined verification, records evidence, performs independent Review handoff, and triggers the release-milestone architecture diagnosis required by the workflow.

## Ticket 1 - Expose the official tag-pinned repository marketplace

Status: Completed.

Execution mode: `tdd` (user selected tests).

System recommendation: Add tests. The marketplace is a supply-chain boundary: a wrong URL, mutable ref, source type, path, policy, or identity could install unreviewed content or make the public command silently fail. Tests add medium time but provide durable rejection coverage for unsafe catalog changes.

### Outcome and acceptance coverage

A Codex user can add `Mysterio1001/Ask-Then-Do-It` as marketplace `ask-then-do-it`, and the catalog exposes exactly the official `ask-then-do-it` Plugin from the approved subdirectory pinned to `v1.2.0`.

This Ticket covers Specification acceptance criterion 1 and the marketplace-specific portions of criteria 2, 7, 8, and 10.

### Scope

In scope:

- Repository marketplace identity and display metadata.
- Exactly one Plugin entry with the approved HTTPS URL, `git-subdir`, subdirectory, formal tag, policies, and category.
- Focused validation that rejects mutable refs, alternate sources, incorrect paths, identities, policies, or extra entries when tests are selected.
- Static confirmation that the catalog is repository metadata, not a personal marketplace mutation.

Out of scope:

- Installing or updating the Plugin in the user's environment.
- Plugin visual assets, localized documentation, generated packages, checksums, release evidence, or external publication.
- Editing personal Codex configuration or marketplace state.

### Dependencies and ownership

Dependency: Approved Specification and Plan. No implementation Ticket dependency.

Likely ownership: `.agents/plugins/marketplace.json`, a focused marketplace/release-contract test area under `tests/release/`, and Ticket evidence under `docs/evidence/`.

### TDD approach

1. Add focused failing checks for the absent catalog and each approved marketplace field, plus negative cases for mutable or alternate sources.
2. Record Red before adding marketplace production metadata.
3. Add the smallest catalog satisfying the approved contract.
4. Reach focused Green and run relevant release-contract checks without performing network or install operations.

### Direct approach

- Add the catalog without creating or running behavioral tests.
- Parse the JSON, inspect every externally observable field, and verify the catalog contains no credential, local path, or personal marketplace state.
- Record that automated rejection evidence for unsafe source/ref/path variants is unavailable.

### Verification and completion

Focused TDD verification: marketplace schema/contract tests and negative source/ref/path/policy cases. Broader TDD verification: relevant release-contract and clean-inventory tests.

Direct verification: JSON parsing, exact structured-field inspection, repository-path inspection, and `git diff --check`; no behavioral suite.

Complete when the repository contains exactly one valid official catalog entry pinned to `v1.2.0`, no personal state is changed, and Review finds no alternate-source or mutable-ref path. Evidence: [Ticket 1 implementation](../evidence/command-install-update-1.2.0-ticket-1.md) and [Ticket 1 Review](../evidence/command-install-update-1.2.0-ticket-1-review.md).

Parallel safety: `Yes` with Tickets 2 and 3 after Plan approval; ownership does not overlap their Plugin asset, manifest, or documentation files. Ticket 4 consumes this result.

## Ticket 2 - Add release-ready transparent Plugin visual assets

Status: Completed.

Execution mode: `tdd` (user selected tests).

System recommendation: Add tests. Asset dimensions, alpha, transparent corners, manifest paths, source inventory, and package inclusion are easy to regress and may not be obvious from a single visual preview. Tests add medium time; skipping them leaves only metadata and visual inspection evidence.

### Outcome and acceptance coverage

The canonical Plugin displays the approved red seahorse-question-mark branding through a 512×512 transparent composer icon, a 1024×1024 transparent logo, and `#C8262A`, and the release builder accepts and copies those assets without including the superseded source images.

This Ticket covers Specification acceptance criteria 5 and 6, the asset portions of criteria 7 and 9, and the visual exclusions in criterion 10.

### Scope

In scope:

- Verify the approved source image hash before processing.
- Remove the light background and edge haze while preserving, centering, and padding the approved subject.
- Produce canonical `assets/icon.png` and `assets/logo.png` at the approved dimensions with alpha.
- Add the approved brand color and asset paths to the Plugin interface.
- Update canonical Plugin inventory/build acceptance so assets are copied into the Codex package.
- Focused automated asset and package-source checks when tests are selected.

Out of scope:

- Marketplace metadata, localized command documentation, global `1.2.0` version migration, release checksums/evidence, `logoDark`, or visual redesign.
- Committing the original temporary image or the superseded lighthouse image.

### Dependencies and ownership

Dependency: Approved Specification and Plan. No implementation Ticket dependency.

Likely ownership: canonical Plugin `assets/`, `.codex-plugin/plugin.json`, Codex source-inventory validation in the release builder, focused Codex release tests, and Ticket evidence.

### TDD approach

1. Add failing checks for missing asset paths/files, dimensions, PNG/alpha, transparent corners, nonempty subject, approved brand color, and package-source inventory.
2. Record Red before adding assets or manifest fields.
3. Produce the minimum approved derivatives and update manifest/build inventory.
4. Reach focused Green, visually inspect both assets on light and dark backgrounds, run canonical Plugin validation, and refactor processing only if output stays identical.

### Direct approach

- Verify the source hash, produce the two derivatives, update manifest/build inventory, and do not add or run behavioral tests.
- Use image metadata inspection, alpha/corner sampling, visual inspection on contrasting backgrounds, JSON parsing, and native Plugin validation as permitted non-test evidence.
- Record that automated regression coverage for missing/wrong/opaque assets and package inclusion is unavailable.

### Verification and completion

Focused TDD verification: asset contract, manifest path, Plugin source inventory, and package-copy tests. Broader TDD verification: Codex release-source tests and canonical Plugin validator.

Direct verification: source hash, PNG metadata, alpha/corner/content sampling, light/dark visual inspection, Plugin validation, build-source inventory inspection, and `git diff --check`.

Complete when both canonical assets satisfy the approved visual/metadata contract, the manifest resolves them inside the Plugin, the builder accepts them, and no source or lighthouse image enters the Plugin. Evidence: [Ticket 2 implementation](../evidence/command-install-update-1.2.0-ticket-2.md) and [Ticket 2 Review](../evidence/command-install-update-1.2.0-ticket-2-review.md).

Parallel safety: `Yes` with Tickets 1 and 3 after Plan approval. Ticket 2 owns Plugin asset/manifest and Codex asset-inventory areas; Ticket 4 consumes the result.

## Ticket 3 - Document a state-aware AI-first install and update flow

Status: Completed.

Execution mode: `tdd` (user selected tests).

System recommendation: Add tests. This Ticket carries authorization and failure safety in three languages and has a strict README preservation boundary. Tests add medium time but protect against accidental writes for version checks, alternate sources, automatic downgrade claims, inconsistent translations, and unrelated README churn.

### Outcome and acceptance coverage

English, Traditional Chinese, and Japanese users receive equivalent natural-language instructions that lead an AI through read-only state inspection, authorized first install/update branches, failure-stop behavior, ZIP fallback, and new-task loading, with the exact supported CLI commands available for audit and manual use.

This Ticket covers Specification acceptance criteria 2, 3, and 4, plus documentation exclusions in criterion 10.

### Scope

In scope:

- Update the three canonical Plugin start guides and three detailed Codex guides.
- Present AI instructions as primary and marketplace/Plugin CLI commands as supporting evidence.
- Cover read-only version checks, first install, update, already-current, source mismatch/unknown, failure stop, no automatic downgrade, ZIP fallback, and start-a-new-task behavior.
- Update the six existing README download entries from `1.1.0` to `1.2.0` and insert the three localized command-install/update sections at the approved positions.
- Enforce semantic parity and the README exact-change boundary when tests are selected.

Out of scope:

- Marketplace JSON, Plugin assets/manifest, other README prose/order/links, Generic workflow behavior, generated packages, checksums, release evidence, or executing CLI writes.

### Dependencies and ownership

Dependency: Approved Specification and Plan. No implementation Ticket dependency.

Likely ownership: `README.md`, localized canonical Plugin start guides, localized `docs/guides/codex.*.md`, focused documentation tests, and Ticket evidence.

### TDD approach

1. Add failing checks for all required state branches, approved commands, three-language parity, prohibited behavior, exact README insertion positions, and preservation of every other README byte.
2. Record Red against existing manual-only `1.1.0` documentation.
3. Make the smallest localized documentation changes satisfying the approved behavior and README boundary.
4. Reach focused Green, validate every relative link, and compare the README diff against the approved whitelist.

### Direct approach

- Update only the approved documentation without creating or running behavioral tests.
- Inspect each language against a shared decision checklist, verify command strings, validate relative links, and compare the README diff manually with the approved boundary.
- Record that automated semantic-parity, prohibited-claim, and exact-preservation evidence is unavailable.

### Verification and completion

Focused TDD verification: localized command-flow, unsafe-claim, README-whitelist, and documentation-link tests. Broader TDD verification: complete documentation regression module.

Direct verification: three-language checklist, exact command search, link resolution, README diff inspection, and `git diff --check`; no behavioral suite.

Complete when all three languages describe equivalent safe behavior, only `plugin add` is supported, and README changes are limited exactly to the approved version/URL replacements and insertions. Evidence: [Ticket 3 implementation](../evidence/command-install-update-1.2.0-ticket-3.md) and [Ticket 3 Review](../evidence/command-install-update-1.2.0-ticket-3-review.md).

Parallel safety: `Yes` with Tickets 1 and 2 after Plan approval; its files and tests do not overlap their marketplace or asset areas. Ticket 4 consumes this result.

## Ticket 4 - Integrate the lockstep `1.2.0` deterministic release

Status: Completed.

Execution mode: `tdd` (user selected tests).

System recommendation: Add tests. This Ticket changes shared version identity, build configuration, current package inventories, generated archives, checksums, and version gates across both adapters. Tests add high time but are the primary protection against inconsistent or unreproducible release output.

### Outcome and acceptance coverage

All active current-release declarations identify `1.2.0`; deterministic Codex and Generic packages are rebuilt with the approved marketplace exclusion and Plugin asset inclusion; archives, generated metadata, documentation references, and checksums agree while historical `1.1.0` artifacts remain unchanged.

This Ticket covers Specification acceptance criteria 7 and 8, the release-integration portions of criteria 1, 2, 4, 5, 6, and 9, and all applicable exclusions in criterion 10.

### Scope

In scope:

- Move active product/Core/adapter/Plugin/release declarations and current user-facing version references to `1.2.0` without rewriting historical approved artifacts.
- Extend release validation to enforce marketplace tag and current-version consistency across source, generated metadata, archives, checksums, current documentation, and evidence inputs.
- Rebuild both unpacked packages and archives plus checksums from canonical source.
- Prove Codex packages include approved visual assets but no catalog, and Generic packages include neither.
- Update release, Codex, Generic, conformance, clean-identity, safety, reproducibility, ZIP-equivalence, checksum, and current documentation expectations when tests are selected.

Out of scope:

- New marketplace behavior beyond Ticket 1, visual redesign beyond Ticket 2, new install/update wording beyond Ticket 3, external publication, final completed release evidence, or architecture refactoring.

### Dependencies and ownership

Dependencies: Tickets 1, 2, and 3.

Likely ownership: active version declarations across Core/adapters/current docs, `release/release.json`, release builder/validators, release/conformance tests, generated `dist/`, and Ticket evidence. Historical `1.0.x`/`1.1.0` requirements, specifications, plans, and completed evidence are read-only boundaries.

### TDD approach

1. Add or update focused release-contract tests so the integrated pre-change repository fails on `1.2.0` identity, marketplace consistency, asset inventory, package exclusion, and archive/checksum expectations.
2. Record Red before changing active version declarations and generated output.
3. Apply the minimum coherent lockstep source/configuration updates and rebuild both packages atomically.
4. Reach focused Green, prove reproducibility and ZIP equivalence, and run the broader release/conformance suite.

### Direct approach

- Update active declarations, release validation, and generated output without creating, modifying, or running behavioral tests.
- Run only permitted schema/native/static validation, deterministic build commands, checksum comparison, package inventory inspection, and diff checks.
- Record that automated regression evidence for version mismatch, unsafe inventories, reproducibility, and historical-boundary preservation is unavailable.

### Verification and completion

Focused TDD verification: release identity, marketplace/version gate, Codex/Generic package inventory, deterministic build, ZIP parity, and checksum tests. Broader TDD verification: full release, Codex, Generic, conformance, and documentation regression suites plus native Plugin/Skill validation.

Direct verification: configuration/YAML/JSON parsing, native validation, two deterministic builds compared byte-for-byte, ZIP/directory inventory comparison, checksum recalculation, historical-artifact diff inspection, and `git diff --check`.

Complete when all current `1.2.0` contracts agree, packages are reproducible and minimal, assets/catalog boundaries are correct, checksums match, and no historical evidence or external state is changed.

Evidence: [Ticket 4 implementation](../evidence/command-install-update-1.2.0-ticket-4.md) and [Ticket 4 Review](../evidence/command-install-update-1.2.0-ticket-4-review.md).

Parallel safety: `No`; it integrates Tickets 1-3 and owns shared version/build/test contracts.

## Ticket 5 - Complete integrated validation and release evidence

Status: Completed.

Execution mode: `tdd` (user selected tests).

System recommendation: Add tests. This Ticket establishes the final release claim across every behavior and package boundary, and omissions could allow incomplete evidence to appear completed. Tests add high time because the full suite, native validators, reproducibility, visual checks, independent Review, and evidence gate must all agree.

### Outcome and acceptance coverage

The combined `1.2.0` change has trustworthy implementation evidence, independent code Review, release-milestone architecture diagnosis, complete local release evidence, and no unresolved blocking finding or failed required check.

This Ticket covers Specification acceptance criterion 9 and final integrated proof for criteria 1-8 and 10.

### Scope

In scope:

- Run the complete selected behavioral regression scope and all mandatory non-test release validations.
- Validate canonical and packaged Plugin/Skills, marketplace contract, localized documentation, image metadata and visual quality, deterministic builds, ZIP equivalence, checksums, and release evidence completeness.
- Perform the workflow's independent Review handoff and fix only through the approved Ticket path if findings arise.
- Perform a read-only release-milestone architecture diagnosis and record its result without authorizing unrelated refactoring.
- Create current `1.2.0` implementation/review/release evidence and validation ledger only after the underlying observations exist.

Out of scope:

- New product behavior, architecture refactoring, Git tag, GitHub Release, push/upload, marketplace installation, external messaging, background monitoring, or live CLI claims that cannot be observed.

### Dependencies and ownership

Dependencies: Tickets 1-4 completed with their required Reviews and evidence.

Likely ownership: new `1.2.0` evidence, validation ledger, release architecture diagnosis, final review artifacts, and any narrowly required evidence-gate expectations. Production/source fixes discovered here return to the owning Ticket rather than being hidden in evidence work.

### TDD approach

1. Add or update a focused evidence-gate check only if the approved `1.2.0` evidence contract is not already rejected when incomplete or inconsistent; record Red before validator changes.
2. Make the minimum evidence-validator change needed, if any, and reach focused Green.
3. Run the full regression and mandatory validation matrix, then create evidence from observed results.
4. Run independent Review and architecture diagnosis; resolve findings through the earliest affected gate or owning Ticket.

### Direct approach

- Do not create, modify, or run behavioral tests.
- Run mandatory native/static/build/checksum/image/diff validation permitted by direct mode, document behavioral suites as skipped by user with the required approval metadata, and preserve the resulting reduced confidence.
- Create no completed release evidence unless the evidence gate accepts the selected test status and every non-test required check passes.

### Verification and completion

Focused TDD verification: release-evidence completeness and rejection cases when validator changes are needed. Broader TDD verification: full automated discovery plus all native, conformance, build, package, checksum, image, documentation, and evidence validations.

Direct verification: every mandatory non-test validation, independent diff Review, read-only architecture diagnosis, and evidence-gate validation with honest `skipped-by-user` disclosure.

Complete when all required checks have accepted evidence, Review has no blocking finding, architecture diagnosis reports no accepted unplanned refactor, the local release ledger/evidence agree, and all external publication work remains explicitly deferred.

Evidence: [Ticket 5 implementation](../evidence/command-install-update-1.2.0-ticket-5.md), [Ticket 5 Review](../evidence/command-install-update-1.2.0-ticket-5-review.md), and [release evidence](../evidence/ask-then-do-it-release-1.2.0.md).

Parallel safety: `No`; it consumes the fully integrated repository and final observations from every earlier Ticket.

## Dependency order and parallel groups

1. Parallel-safe group after Plan approval: Tickets 1, 2, and 3, only if explicitly delegated with their stated ownership boundaries.
2. Sequential integration: Ticket 4 after Tickets 1-3.
3. Sequential completion: Ticket 5 after Ticket 4 and all required Ticket Reviews.

All test choices were resolved as Add tests, internally mapped to `tdd`. All five Approved Tickets are complete.
