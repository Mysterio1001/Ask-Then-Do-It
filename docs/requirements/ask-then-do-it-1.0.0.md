# Ask Then Do It 1.0.0 Rename and Licensing Requirement Decision Record

Artifact type: Requirement Decision Record

Artifact ID: `ask-then-do-it-1-0-requirements`

Workflow ID: `ask-then-do-it-1-0`

Target Core version: `1.0.0`

Status: Approved

Approval: Explicitly confirmed by the user on 2026-07-29 with the response `好` after the complete requirement summary was presented.

## Problem and desired outcome

The unpublished project currently uses the product and Plugin name `Grill Me`, while Matt Pocock's upstream skills repository includes `grill-me`, `grilling`, and related engineering workflow skills that inspired this project. The current source and packages do not yet carry a clear upstream attribution, the upstream MIT License, an independent-project disclaimer, or a license for the project's own additions. Reusing the same public-facing name could also suggest an official relationship or endorsement that does not exist.

The desired outcome is a clearly independent first public release named `Ask Then Do It`, with a simple primary command, distinct package identities, complete upstream MIT attribution, an explicit license for new work, and notices that remain attached when either consumer ZIP is redistributed independently.

## Users and success signals

### First-time user

- Sees `Ask Then Do It` as the product identity.
- Understands the phrase "Ask first, then act" without needing prior workflow terminology.
- Can distinguish this project from Matt Pocock's original repository.
- Finds the applicable own-project and third-party licenses inside the downloaded package.

### Maintainer

- Has one exact product ID, Skill inventory, package layout, and licensing source of truth.
- Can rebuild both `1.0.0` packages without manually copying license text.
- Can verify that notices in generated directories and ZIPs are byte-equivalent to canonical source.

### Rights holder or reviewer

- Can identify which license applies to this project's additions.
- Can read Matt Pocock's complete original MIT License and source link.
- Sees no claim of affiliation, approval, partnership, or endorsement.

## Scope

- Rename the public product to `Ask Then Do It`.
- Use `ask-then-do-it` as the Plugin and package ID.
- Rename the primary Skill from `ai-dev-workflow` to `ask-then-do-it`.
- Rename `grill-requirements` to `ask-requirements`.
- Rename `grill-with-docs` to `ask-with-docs`.
- Retain `write-spec`, `plan-tickets`, `implement-tdd`, `review-code`, and `improve-architecture`.
- Rename all active routing references, UI metadata, manifests, package paths, human instructions, and validation expectations consistently.
- Release the Codex archive as `ask-then-do-it-1.0.0.zip`.
- Release the Generic archive as `ask-then-do-it-generic-1.0.0.zip` while retaining `generic-workflow.md` as its primary file.
- License the project's own additions under the MIT License with `Copyright (c) 2026 Ian Wu, Handle by me Tech Studio`.
- Add a canonical root `LICENSE` for the project's additions.
- Add a canonical root `THIRD_PARTY_NOTICES.md` with attribution, source links, the independent-project disclaimer, and Matt Pocock's complete original MIT License.
- Include both canonical license files at the root of both generated consumer packages and ZIPs.
- Put prominent attribution in the README and concise independent-project notices in the Plugin manifest and both package start guides.
- Rebuild the first public release as `1.0.0` and recreate checksums and evidence.

## Non-goals

- Claim that Matt Pocock personally approved, reviewed, partnered with, sponsored, or endorsed this project.
- Obtain a private or exclusive license from Matt Pocock.
- Change or relicense Matt Pocock's original work.
- Provide legal advice or a trademark clearance opinion.
- Preserve compatibility aliases, duplicate old ZIPs, or migration behavior for the unpublished `grill-me` package identity.
- Rename the five retained stage Skills or the provider-neutral Generic prompt module IDs.
- Rename the user's enclosing local workspace directory.
- Install a Plugin, configure a marketplace, publish a release, or contact an external person.

## Primary behavior and user flow

### Source visitor

1. Opens the README and immediately sees the independent-project attribution.
2. Opens `LICENSE` for the license covering this project's additions.
3. Opens `THIRD_PARTY_NOTICES.md` for upstream source and license details.
4. Chooses the Codex or Generic `Ask Then Do It` package.

### Codex user

1. Downloads `ask-then-do-it-1.0.0.zip`.
2. Extracts one `ask-then-do-it/` Plugin root.
3. Sees `LICENSE`, `THIRD_PARTY_NOTICES.md`, and `START-HERE.zh-TW.md` at the Plugin root.
4. Installs manually under their own authority.
5. Begins with `$ask-then-do-it` or directly selects one of the other seven Skills.

### Generic user

1. Downloads `ask-then-do-it-generic-1.0.0.zip`.
2. Sees the two license files beside `START-HERE.zh-TW.md` and `generic-workflow.md`.
3. Pastes the workflow once and continues under the existing Conversation-only behavior.

## Data, dependencies, security, privacy, and operational constraints

- The build remains local, deterministic, standard-library-only, and network-free.
- Canonical license text is stored in the repository; a release build must not fetch legal text from the network.
- The verified upstream license source is `https://github.com/mattpocock/skills/blob/main/LICENSE`.
- The upstream repository source is `https://github.com/mattpocock/skills`.
- The official upstream LICENSE observed during requirement authoring begins with `MIT License` and contains `Copyright (c) 2026 Matt Pocock`.
- The user-provided attribution paragraph must remain verbatim in the README and third-party notice.
- Packages must contain no private path, credential, personal marketplace state, or installation mutation.

## Edge cases and failure behavior

- A Plugin folder name that differs from manifest `name` must fail validation.
- Any active reference to a renamed Skill ID must fail the rename inventory check, except in explicit historical or upstream-attribution context.
- `grill-me` may appear when identifying Matt Pocock's upstream Skill or explaining the former local name, but must not remain an active product, package, Plugin, or command identity.
- A missing, altered, or misplaced license file must fail package inventory validation.
- A `THIRD_PARTY_NOTICES.md` that omits the upstream copyright or permission notice must fail validation.
- A statement that implies affiliation or endorsement must fail documentation validation.
- If either generated package differs from canonical license source, the build or release gate must fail.
- Old local generated output must not be presented as a compatibility release.

## Acceptance criteria

- All active product and Plugin identities use `Ask Then Do It` and `ask-then-do-it`.
- The three approved Skill renames are complete and all eight Skills remain valid and directly callable.
- The Codex output is `dist/codex/ask-then-do-it/` and `dist/codex/ask-then-do-it-1.0.0.zip`.
- The Generic output is `dist/generic/ask-then-do-it-generic-1.0.0/` and its matching ZIP.
- Root and both package roots contain the project's `LICENSE` and `THIRD_PARTY_NOTICES.md`.
- The own-project LICENSE contains the exact approved copyright line.
- The third-party notice contains the exact upstream MIT License, both source links, and the complete user-provided attribution paragraph.
- README attribution is visible before quick-start instructions.
- The Plugin manifest and package start guides disclose independent, non-endorsed status.
- Both ZIPs match their unpacked directories, both current hashes match `checksums.sha256`, and exactly two archives are listed.
- Existing non-brand workflow behavior, approval gates, Generic immediate startup, TDD, review, project knowledge, and architecture diagnosis remain unchanged.
- No installation, marketplace mutation, publication, upload, or external message occurs.

## Confirmed decisions

- Product name: `Ask Then Do It`.
- Product and Plugin ID: `ask-then-do-it`.
- Chinese tagline: `先問清楚，再開始做`.
- Primary Skill: `$ask-then-do-it`.
- Requirement Skills: `$ask-requirements` and `$ask-with-docs`.
- Own license: MIT License.
- Own copyright: `Copyright (c) 2026 Ian Wu, Handle by me Tech Studio`.
- Upstream attribution and full MIT License travel with both packages.
- No affiliation or endorsement claim.
- First public release remains `1.0.0` because no release has been published and no user depends on the old identity.

## Assumptions

- Matt Pocock's repository-level MIT License applies to the upstream material referenced by the user; any upstream exception discovered during implementation must return to requirements.
- The approved own copyright line is intentional as written, including capitalization and punctuation.
- Historical Approved artifacts may retain their original names as provenance records, but consumer-facing and active runtime identities must use the new name.

## Deferred decisions

- Formal trademark clearance and legal review before public publication.
- Public repository slug and hosting platform configuration.
- A permanent upstream commit permalink beyond the required repository and LICENSE links.
- Additional translations of legal or onboarding text.

## Explicit consensus evidence

The user adopted the recommended independent attribution and licensing approach, selected `Ask Then Do It`, approved the three Skill renames, supplied the exact own copyright line, approved the new Codex and Generic package names, approved license placement in the repository and both packages, and explicitly confirmed the consolidated requirement summary on 2026-07-29 with `好`.

## Handoff

This Approved Requirement Decision Record authorizes a Draft behavioral Specification. It does not authorize Ticket Planning, production edits, file renames, generated-output replacement, installation, or publication.
