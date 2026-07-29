# Ask Then Do It 1.0.0 Rename and Licensing Specification

Artifact type: Specification

Artifact ID: `ask-then-do-it-1-0-spec`

Workflow ID: `ask-then-do-it-1-0`

Target Core version: `1.0.0`

Status: Approved

Approval: Explicitly approved by the user on 2026-07-29 with the response `好`.

## Inputs

- Approved [Ask Then Do It Requirement Decision Record](../requirements/ask-then-do-it-1.0.0.md).
- Approved [Grill Me Clean-slate 1.0.0 Specification](grill-me-clean-slate-1.0.0.md) describing the currently validated behavior to preserve.
- Matt Pocock's official [skills repository](https://github.com/mattpocock/skills) and [MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE).
- The current locally validated `1.0.0` source and two-package release.

## Problem

The current unpublished release uses a product, Plugin, package, and command identity that overlaps with an upstream Skill name. It also distributes no own-project license or upstream legal notice. A recipient therefore cannot determine the license boundary from either ZIP alone and may incorrectly infer that the project is an official Matt Pocock release.

The first public release needs a distinct identity, complete license carriage, accurate attribution, and explicit independence without changing its established development workflow behavior.

## Goals

- Present `Ask Then Do It` as the only active product identity.
- Make `$ask-then-do-it` a simple, memorable primary entry.
- Rename the two requirement Skills consistently while retaining the remaining five stage names.
- Give the project's additions an explicit MIT License with the approved copyright holder.
- Preserve Matt Pocock's complete upstream MIT License and source attribution.
- Keep own-project and upstream license ownership visibly separate.
- Ensure legal notices survive offline extraction and independent ZIP redistribution.
- Rebuild both consumer packages under distinct `1.0.0` names.
- Preserve all approved non-brand runtime behavior and validation strength.

## Non-goals

- Determine legal compliance conclusively or provide trademark clearance.
- Represent that Matt Pocock approved, endorsed, sponsored, or collaborated on this project.
- Modify upstream license wording or ownership.
- Add compatibility aliases for the old unpublished identity.
- Change the Generic adapter's Conversation-only capability.
- Redesign workflow stages, artifacts, gates, TDD, Review, or architecture behavior.
- Install or publish either package.
- Rename the local enclosing workspace folder.

## Users and scenarios

### New Codex user

The user downloads the only Codex archive, extracts `ask-then-do-it/`, reads the license and independent-project notice at the Plugin root, installs manually, and starts a new task with `$ask-then-do-it`.

### New Generic user

The user downloads the only Generic archive, finds both license files beside the existing one-paste entry, understands the Conversation-only boundary, and receives the same immediate first requirement question behavior.

### Source visitor

The visitor sees prominent attribution before onboarding, can distinguish upstream and project ownership, and follows the new product paths without encountering an active old package identity.

### Maintainer

The maintainer edits canonical legal and runtime sources once, runs the existing deterministic builder, and obtains two byte-verifiable packages carrying identical canonical license files.

### License reviewer

The reviewer can trace the upstream source, read Matt Pocock's unmodified MIT License, read the independent disclaimer, and identify the project's own copyright holder.

## Terminology

- **Own-project License**: the MIT License covering additions owned by `Ian Wu, Handle by me Tech Studio`.
- **Third-Party Notice**: the attribution document containing upstream sources, disclaimer, and Matt Pocock's complete MIT License.
- **Active identity**: current runtime, package, manifest, generated output, and consumer documentation naming; it excludes immutable historical evidence and explicit upstream references.
- **Verbatim attribution paragraph**: the exact English paragraph supplied by the user, without editorial changes.

## Required behavior

### 1. Product and release identity

The active product display name MUST be `Ask Then Do It`. The machine-readable product, Plugin, and Codex directory ID MUST be `ask-then-do-it`.

The release and Core version MUST remain `1.0.0`. The rename MUST be represented as preparation of the first public release, not as compatibility with a published predecessor.

The Plugin's outer folder and manifest `name` MUST both equal `ask-then-do-it`. Its human display name MUST equal `Ask Then Do It`. Manifest author or developer attribution MUST identify `Ian Wu, Handle by me Tech Studio`, and its description or long description MUST state that the project is independent and is not affiliated with or endorsed by Matt Pocock.

### 2. Skill identity and routing

The Codex Plugin MUST contain exactly these eight Skill directories:

- `ask-then-do-it`
- `ask-requirements`
- `ask-with-docs`
- `write-spec`
- `plan-tickets`
- `implement-tdd`
- `review-code`
- `improve-architecture`

Each renamed directory, `SKILL.md` frontmatter `name`, UI display name, UI default prompt, orchestrator route, adapter mapping, manifest evidence, human guide, and test expectation MUST agree.

`$ask-then-do-it` MUST remain the primary automatic router. `$ask-requirements` and `$ask-with-docs` MUST preserve their existing normal and documented requirement behaviors. The other five direct commands MUST preserve their current names and semantics.

No active runtime instruction may route to `$ai-dev-workflow`, `$grill-requirements`, or `$grill-with-docs` after the rename.

### 3. Own-project MIT License

The repository root MUST contain `LICENSE` with the standard MIT License text and the exact line:

`Copyright (c) 2026 Ian Wu, Handle by me Tech Studio`

The own-project License MUST NOT claim ownership of Matt Pocock's original work and MUST NOT remove or replace the upstream notice.

The canonical root `LICENSE` bytes MUST be copied unchanged into both generated package roots and both ZIPs.

### 4. Third-party attribution and license

The repository root MUST contain `THIRD_PARTY_NOTICES.md` that clearly identifies Matt Pocock's skills repository, links to the repository and official LICENSE, identifies `grill-me`, `grilling`, and engineering workflow skills as particular sources of inspiration, and includes this paragraph verbatim:

> This project is an independent extension inspired by Matt Pocock’s skills repository, particularly grill-me, grilling, and its engineering workflow skills. Matt Pocock’s original work is licensed under the MIT License. This project is not affiliated with or endorsed by Matt Pocock.

The notice MUST reproduce the complete official upstream MIT License verbatim, including `Copyright (c) 2026 Matt Pocock`, the permission notice, the notice-retention condition, and warranty disclaimer.

The canonical root notice bytes MUST be copied unchanged into both generated package roots and both ZIPs.

### 5. Human-facing attribution

The README MUST display the verbatim attribution paragraph and both upstream links after the title and introductory sentence but before quick-start instructions. A Traditional Chinese explanation MAY accompany it but MUST NOT weaken or reinterpret the English disclaimer.

The root start page and both package start guides MUST use the new product and command names. Both package start guides MUST state concisely that the project is independent, is inspired by Matt Pocock's repository, and is not affiliated with or endorsed by Matt Pocock. They MUST direct readers to the packaged `THIRD_PARTY_NOTICES.md` for complete terms.

Canonical model-consumed Core and Generic prompt contracts SHOULD remain focused on runtime behavior; complete legal text MUST NOT be duplicated inside every Skill or prompt.

### 6. Codex consumer package

The Codex generated outputs MUST be:

- `dist/codex/ask-then-do-it/`
- `dist/codex/ask-then-do-it-1.0.0.zip`

The archive root MUST be `ask-then-do-it/`. The package root MUST contain exactly the approved Plugin runtime content plus:

- `START-HERE.zh-TW.md`
- `LICENSE`
- `THIRD_PARTY_NOTICES.md`

The package MUST contain no installer, marketplace mutation, compatibility alias, old Plugin root, tests, evidence, Plans, Specifications, or maintainer source.

### 7. Generic consumer package

The Generic generated outputs MUST be:

- `dist/generic/ask-then-do-it-generic-1.0.0/`
- `dist/generic/ask-then-do-it-generic-1.0.0.zip`

The archive root MUST be `ask-then-do-it-generic-1.0.0/`. The package MUST retain `generic-workflow.md`, the generated manifest, and all nine source-equivalent prompts, and MUST add root `LICENSE` and `THIRD_PARTY_NOTICES.md` beside `START-HERE.zh-TW.md`.

The generated manifest MUST identify product `ask-then-do-it`, display name `Ask Then Do It`, release and Core `1.0.0`, and the existing `generic-prompts` adapter. The Generic runtime MUST retain immediate fresh interrogation, resumed artifact routing, user-owned persistence, and Conversation-only claim limits.

### 8. Distribution replacement and compatibility

`dist/` MUST still contain only `codex/`, `generic/`, and `checksums.sha256` at its top level. Within those provider directories, only the new branded current directory and archive may remain.

No old archive, unpacked package, checksum alias, Plugin ID alias, or command alias may be retained for compatibility. The builder MUST stage and validate the complete new output before replacing an existing complete managed output set.

An unmanaged collision MUST fail without deletion or partial replacement.

### 9. Documentation and historical records

Current consumer documentation, design explanation, release configuration, generated manifests, and runtime source MUST use the new identity.

Previously Approved requirement, Specification, Ticket Plan, Review, architecture, and implementation evidence MAY retain their original product names as immutable provenance. New active documents MUST identify them only as superseded inputs, not current download or command paths.

Mentions of `grill-me` are permitted in upstream attribution, license traceability, explicit former-name explanation, and negative tests. They MUST NOT present an active local product identity.

### 10. Validation and release evidence

Validation MUST prove:

- exact active identity and absence of stale command or package aliases;
- all eight Skill frontmatter and UI metadata contracts;
- source and packaged Plugin validity;
- both adapter conformance results;
- byte-equivalent license and third-party notice copies in directories and ZIPs;
- exact package inventories and ZIP roots;
- deterministic two-build reproducibility;
- exactly two matching SHA-256 entries;
- README and guide disclaimer placement;
- preserved Generic immediate-start and Conversation-only behavior;
- absence of installers, marketplace files, caches, development evidence, and misleading endorsement claims;
- fail-closed Completed release evidence.

Completed `1.0.0` evidence MUST be recreated after the branded packages and hashes are final. Earlier evidence MAY remain as provenance but MUST NOT be presented as proof of the renamed package bytes.

## Edge cases and failure behavior

- If a renamed folder and Skill frontmatter disagree, native Skill validation or package tests must fail.
- If the Plugin folder and manifest name disagree, Plugin or release validation must fail.
- If a UI default prompt invokes an old command, command-inventory validation must fail.
- If the root legal files and either packaged copy differ by any byte, packaging validation must fail.
- If the third-party notice is missing the full upstream license or exact user paragraph, attribution validation must fail.
- If consumer text says or implies "official", "endorsed", or an affiliation with Matt Pocock, documentation validation must fail unless the text explicitly negates that claim.
- If official upstream license content changes before implementation, implementation must stop and disclose the mismatch rather than silently substituting text.
- If generated output contains both old and new identities, the release inventory must fail.
- If a build fails after staging, the previously complete managed output must remain intact.

## Data, permissions, and external contracts

- Own-project license contract: MIT License with the user-approved copyright line.
- Upstream license contract: the official Matt Pocock MIT License observed at the approved URL.
- Source attribution contract: the user-provided English paragraph is literal text.
- Runtime and package manifests are public release metadata and contain no secrets.
- License URLs are documentation references; the deterministic builder does not access them.
- Personal Codex installation, marketplace configuration, hosting, publication, and external accounts remain outside repository authority.

## Compatibility, rollout, and recovery

Because no version has been publicly released and no user depends on the old IDs, rollout is a clean rename within `1.0.0` with no alias or migration layer.

Implementation MUST first add failing identity, attribution, and package tests. It MUST then update canonical source, build isolated outputs, validate them, and replace only the known managed distribution set.

Recovery from an implementation failure is the prior complete local output and unchanged source outside the authorized rename and licensing paths. Recovery MUST NOT create or restore an advertised old compatibility release.

The enclosing local workspace directory may retain its current filesystem name; this does not define public product or package identity.

## Constraints and assumptions

- Canonical Specifications, rules, manifests, prompts, and Skill instructions remain English.
- Human start and detailed usage guides remain Traditional-Chinese-first.
- Legal license text remains in its official English wording.
- Skill instructions remain concise; complete licenses live at package roots rather than inside Skill bodies.
- The source repository remains maintainer-facing and the two ZIPs remain consumer-facing.
- The user-approved copyright spelling is exact and intentional.
- No formal trademark clearance is claimed for `Ask Then Do It`.

## Observable acceptance criteria

- Opening README shows the exact independent attribution before quick start.
- Opening root `LICENSE` shows the own MIT License and exact approved copyright.
- Opening root `THIRD_PARTY_NOTICES.md` shows both source links, the exact attribution paragraph, and Matt Pocock's complete MIT License.
- Extracting the Codex ZIP yields one `ask-then-do-it/` root with the two license files, start guide, valid manifest, and exactly eight valid Skills using the approved names.
- A fresh Codex task can begin with `$ask-then-do-it`; direct invocation of the other seven Skills remains available.
- Extracting the Generic ZIP yields one `ask-then-do-it-generic-1.0.0/` root with both license files, start guide, combined workflow, generated manifest, and nine prompts.
- A fresh Generic conversation still asks one recommended high-impact requirement question in the first effective response.
- No active local runtime or package path uses the former identity outside explicitly allowed traceability contexts.
- Two clean builds are byte-identical, ZIPs equal directories, and `checksums.sha256` lists exactly the two new archives.
- All automated, native, conformance, documentation, safety, and evidence-gate checks pass without installation, publication, or network use during the build.

## Deferred decisions

- Formal legal review and trademark search.
- Public repository rename and release hosting.
- Upstream commit pinning policy.
- Additional provider-native adapters.
- Translated legal notices beyond concise human explanations.

## Handoff

This Approved Specification authorizes vertical Ticket Planning only. It does not authorize production edits, renames, deletion of generated output, package rebuilding, installation, or publication.

## Specification approval evidence

The user explicitly approved this complete behavioral contract on 2026-07-29 with the response `好`. Ticket Planning may begin; implementation still requires an explicitly Approved Ticket Plan.
