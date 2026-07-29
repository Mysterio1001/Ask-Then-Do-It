# Ask Then Do It 1.0.0 Ticket 1 Evidence

Artifact type: Implementation Evidence

Artifact ID: `ask-then-do-it-1-0-ticket-1`

Workflow ID: `ask-then-do-it-1-0`

Ticket: 1 — Let a source visitor identify the project and its licenses

Status: Completed

Date: 2026-07-29

## Scope completed

- Added canonical root `LICENSE` for this project's additions.
- Added canonical root `THIRD_PARTY_NOTICES.md` with the exact required attribution, upstream links, and complete upstream MIT License.
- Renamed root README and Traditional-Chinese start page to `Ask Then Do It` and added the tagline `先問清楚，再開始做`.
- Placed the required attribution paragraph before quick start in the README.
- Updated the human design explanation to use the current Specification, Ticket Plan, and `$ask-with-docs` identity.
- Added focused identity, attribution, license, and design-document tests.

## Red evidence

The initial direct command `python -m unittest tests.release.test_ask_then_do_it_identity -v` could not run because this workspace does not expose `python` on `PATH`. The bundled workspace Python was then used.

Command:

```powershell
& 'C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.release.test_ask_then_do_it_identity -v
```

Result before implementation: `FAILED (failures=4)`.

- Root `LICENSE` was absent.
- `THIRD_PARTY_NOTICES.md` was absent.
- README began with the former product name and lacked the required attribution.
- Root start page lacked the approved product name and Chinese tagline.

## Green evidence

Command:

```powershell
& 'C:\Users\Ian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.release.test_ask_then_do_it_identity tests.release.test_documentation.ReleaseDocumentationTests.test_all_relative_document_links_resolve -v
```

Result: `Ran 6 tests ... OK`.

The passing checks prove:

- README and start page show the approved identity and tagline.
- README contains the verbatim attribution before the start-page link and contains both upstream URLs.
- Root `LICENSE` contains the exact approved copyright and complete MIT permission and warranty text.
- `THIRD_PARTY_NOTICES.md` contains the required attribution, both URLs, Matt Pocock's copyright, and complete MIT permission and warranty text.
- The human design explanation points to current artifacts and `$ask-with-docs`.
- All Markdown relative links resolve.

## Boundary confirmation

No Plugin folder, Skill, adapter runtime, generated package, `dist/` output, personal installation, marketplace, publication target, or external service was changed by this Ticket. The two future archive paths in the start page are intentionally displayed as code paths rather than links until the final release Ticket generates them.
