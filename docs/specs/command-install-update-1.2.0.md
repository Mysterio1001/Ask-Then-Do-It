# Ask Then Do It 1.2.0 指令安裝、更新與 Plugin 圖示 Specification

Artifact type: Specification

Artifact ID: `command-install-update-1-2-spec`

Workflow ID: `command-install-update`

Core version: `1.1.0`

Target release version: `1.2.0`

Status: Approved

Inputs: Approved [Ask Then Do It 1.2.0 指令安裝、更新與 Plugin 圖示 Requirement Decision Record](../requirements/command-install-update-1.2.0.md) and Approved [Project Knowledge Base](../project/knowledge-base.md).

Assumptions: 目標 Codex CLI 實作 OpenAI 官方文件所描述的 GitHub marketplace、marketplace list/upgrade、Plugin list/add 行為。當目標 CLI 與本規格不相容時，流程必須停止並轉用正式 ZIP 備援，不得猜測替代命令。

Deferred: OpenAI universal public Plugins Directory、背景檢查或推播、無人值守更新、私人 fork 發佈、`logoDark`、實際 Git tag／GitHub Release／push／upload／公告。

Handoff: `$plan-tickets` after explicit Specification approval.

Approval: 使用者於 2026-08-13 在完整 Specification 展示並說明主要假設後明確回覆「核准」。

## Problem

目前 `1.1.0` 只提供 ZIP 型手動安裝。Repository 沒有 Codex 可追蹤的 marketplace catalog，因此使用者無法從官方 GitHub 來源以一致指令安裝，也缺少一份可交由 AI 執行、能分辨首次安裝與更新且遇錯即停的操作契約。Plugin manifest 也沒有品牌色與圖示資產。

## Goals

- 將 `1.2.0` 定義為第一個可從官方 GitHub marketplace 以指令安裝的版本。
- 讓使用者能以明確自然語言授權 AI 檢查狀態並完成首次安裝或更新。
- 確保任何安裝只取用官方 repository 中的正式 Git tag，而不是開發中分支內容。
- 保留 ZIP 手動安裝為受支援的離線或相容性備援。
- 為 Plugin 提供一致、可驗證、適用亮色與深色介面的品牌圖示。
- 在 release gate 阻止版本、catalog、產物、文件或資產不同步的發布。

## Non-goals

- 自動偵測新版、背景更新、推播、排程更新或未經使用者要求的環境寫入。
- 在錯誤後自動降版，或自動改用非官方來源。
- 支援 HTTP、SSH、任意 URL、替代 repository 或私人 fork。
- 以 `codex plugin install` 作為正式使用介面。
- 把 marketplace catalog 放進消費者 ZIP，或取消 ZIP 備援。
- 重新設計核准的紅色海馬問號圖形、使用燈塔圖、提供 `logoDark`。
- 在本功能交付內執行對外發布操作。

## Users and scenarios

### First-time installation

使用者明確要求 AI 安裝 Ask Then Do It。AI 先以唯讀方式確認 marketplace 與 Plugin 狀態。只有在官方 marketplace 尚不存在時，流程才加入官方 GitHub marketplace，然後從該 marketplace 安裝 Plugin。

### Existing installation update

使用者在正式新版發布後明確要求 AI 更新。AI 先唯讀確認現有來源與版本；只有在來源可確認為本規格的官方 marketplace 且有正式新版時，才升級 catalog 並重新安裝 Plugin。

### Version check

使用者只要求檢查版本或表達不明確時，AI 只能讀取與回報狀態。該請求不得被視為 marketplace 或 Plugin 寫入授權。

### Restricted environment

CLI 不支援所需命令、網路不可用、狀態無法可靠辨識或 marketplace 流程失敗時，使用者仍能依正式文件取得同版本 ZIP 並手動安裝。

## Required behavior

### 1. Release identity

Active product、Core、Codex adapter、Generic adapter、Plugin manifest、release configuration、current user documentation、generated package manifests、archive names、checksums and current `1.2.0` release evidence MUST identify release `1.2.0` wherever a current release version is declared.

Historical approved artifacts and published `v1.1.0` content MUST remain historical evidence and MUST NOT be rewritten merely to remove valid `1.1.0` references.

### 2. Repository marketplace contract

The repository MUST expose one marketplace catalog at `.agents/plugins/marketplace.json` with marketplace identity `ask-then-do-it` and user-facing name `Ask Then Do It`.

The catalog MUST expose exactly one `ask-then-do-it` Plugin entry for this release. The entry MUST:

- use source type `git-subdir`;
- use only `https://github.com/Mysterio1001/Ask-Then-Do-It.git`;
- resolve the Plugin from `adapters/codex/plugin/ask-then-do-it`;
- pin `v1.2.0` rather than a mutable branch;
- declare installation policy `AVAILABLE` and authentication policy `ON_INSTALL`;
- use category `Developer Tools`.

Adding the marketplace by GitHub shorthand without an explicit ref MUST allow Codex to follow the repository default branch `main`. The Plugin selected by that catalog MUST still resolve from the pinned release tag.

The catalog MUST remain repository metadata. It MUST NOT appear in the Codex or Generic consumer ZIP, their unpacked package roots, or checksum inventory.

### 3. User authorization contract

An explicit natural-language request to install or update Ask Then Do It MUST constitute authorization for only the marketplace and Plugin writes necessary for that one request after read-only inspection succeeds.

A request to inspect, check, compare, or report a version MUST authorize read-only operations only. Ambiguous language MUST be treated as read-only.

No request in this contract authorizes automatic downgrade, alternate source selection, background monitoring, publication, credential changes, or unrelated environment mutation.

### 4. State-aware command flow

The documented and AI-facing flow MUST inspect configured marketplaces and installed Plugins before choosing a write action. It MUST distinguish at least these states:

- Official marketplace absent.
- Official marketplace present and Plugin absent.
- Official marketplace and Plugin present with a newer formal release available.
- Installed Plugin already matches the latest formal release.
- Source, version, or CLI state cannot be determined reliably.

For an authorized first installation, the supported command contract MUST add marketplace `Mysterio1001/Ask-Then-Do-It` only when absent and MUST install with `codex plugin add ask-then-do-it@ask-then-do-it`.

For an authorized update, the supported command contract MUST upgrade marketplace `ask-then-do-it` before reinstalling with the same `codex plugin add` command.

When the installed version is current, the flow MUST report that state and perform no write. When reliable classification is impossible, it MUST stop and report the uncertainty.

After a successful install or update, the flow MUST direct the user to start a new Codex task so the new Plugin contents are loaded.

### 5. Failure and recovery behavior

The update flow MUST NOT remove the current Plugin before attempting an update and MUST NOT automatically install an older version.

If any write command fails, the flow MUST stop subsequent writes, report the command that failed and the observable reason, and preserve or honestly report the observable installed state. It MUST NOT claim that the prior version remains intact when the CLI leaves that state unknown.

A downgrade is permitted only after a user explicitly identifies the older tag or version to install. ZIP recovery MUST remain documented as the supported fallback when marketplace installation cannot proceed.

### 6. User documentation

English, Traditional Chinese, and Japanese documentation MUST describe the same install, update, read-only check, failure-stop, no-automatic-downgrade, ZIP fallback, and new-task behavior.

Natural-language instructions to AI MUST be presented as the primary interface. Corresponding Codex CLI commands MUST be shown for audit, manual execution, and troubleshooting. The formal Plugin installation subcommand MUST be `codex plugin add`; documentation MUST NOT present `codex plugin install` as supported project behavior.

The root README MUST change only in these ways:

- replace the existing English, Traditional Chinese, and Japanese `1.1.0` Codex and Generic ZIP display text and release URLs with `1.2.0` equivalents;
- insert one localized command-install/update section immediately before `Read more:`, `更多說明：`, and `詳しい説明：` respectively.

All other pre-existing README text, order, and links MUST remain byte-for-byte unchanged apart from line-ending normalization already imposed by the repository environment.

The three localized Plugin start guides and three localized Codex guides MAY be revised as needed, but their behavior and commands MUST remain semantically equivalent across languages.

### 7. Plugin visual identity

The canonical Plugin MUST include `assets/icon.png` and `assets/logo.png`, derived only from the user-approved red seahorse-question-mark source whose SHA-256 is `C22CF733EBF01ECFEB9C5E9A29AC37496A8B78BBE09F22D5942EC31F0B374EBB`.

The visual subject MUST remain recognizable and proportionally unchanged. The light gray-white source background and visible edge haze MUST be removed. The subject MUST be centered on a square transparent canvas, include visible padding on every side, and MUST NOT be clipped or redesigned.

`icon.png` MUST be a 512×512 PNG with an alpha channel. `logo.png` MUST be a 1024×1024 PNG with an alpha channel. Each corner MUST be transparent and the nontransparent subject MUST be nonempty.

The Plugin interface MUST declare:

- brand color `#C8262A`;
- composer icon path `./assets/icon.png`;
- logo path `./assets/logo.png`.

Each declared asset MUST exist inside both canonical and packaged Plugin roots. The superseded lighthouse image and the temporary source-image path MUST NOT be included in source packages or generated releases.

### 8. Packaging and release gate

The deterministic release build MUST copy both visual assets and the updated manifest into the unpacked Codex package and Codex ZIP without adding marketplace metadata to either package.

The Generic package MUST advance to the same release identity but MUST NOT receive Codex Plugin assets or marketplace content.

Release validation MUST fail when any current release declaration disagrees among the marketplace tag, Plugin manifest, release configuration, generated package metadata, archive names, checksums, active localized version references, or completed release evidence.

Release validation MUST also fail when an asset is missing, has the wrong format or dimensions, lacks alpha, has nontransparent corners, resolves outside the Plugin root, is absent from the packaged Plugin, or differs between the unpacked package and ZIP.

## Edge cases and failure behavior

- A configured marketplace with the same name but a different source MUST be treated as an unresolved source mismatch, not silently replaced.
- A Plugin installed from an unverified marketplace MUST not be updated through this official flow until its source is resolved.
- A mutable Plugin ref such as `main` in the catalog MUST fail release validation.
- A catalog at `main` that still pins an older tag MUST fail the current release consistency gate.
- A CLI that recognizes `install` but not the documented `add`, or vice versa, MUST not cause the workflow to guess an alias; the documented contract remains `add`, and incompatibility falls back to ZIP guidance.
- If an asset conversion produces an empty, clipped, opaque-background, or visibly haloed result, the asset validation MUST fail and the Plugin manifest MUST not reference that result as release-ready.
- A failed build or validation MUST not produce completed `1.2.0` release evidence.

## Data, permissions, and external contracts

- The official repository URL, Plugin subdirectory, tag, marketplace identity, Plugin identity, policies, category, brand color, asset paths, and supported CLI command names are externally observable contracts.
- Marketplace and Plugin writes require an explicit install/update request. Version inspection remains read-only.
- No credential, personal marketplace state, local temporary path, or private repository detail may enter committed source or release packages.
- Image processing may read the hash-identified user source during implementation. Only approved derivative assets belong in canonical source and distribution output.
- GitHub tag and Release creation remain external maintainer operations and are not authorized by this Specification.

## Compatibility, rollout, and recovery

- `v1.1.0` remains immutable and downloadable. `1.2.0` introduces the marketplace path without removing manual ZIP compatibility.
- Users may move from ZIP installation to marketplace installation by explicitly requesting the official installation flow; the workflow must inspect state before writing.
- Marketplace updates are active user operations, not background behavior.
- Recovery after marketplace incompatibility uses the matching formal ZIP. Downgrade requires a separately explicit version choice.
- A release is locally complete only after all specified tests, native validations, conformance checks, deterministic build checks, package equivalence checks, checksums, documentation checks, and release evidence gates pass.

## Constraints and assumptions

- Canonical source remains authoritative; generated `dist/` output is disposable and rebuilt rather than hand-edited.
- Historical approved requirements, specifications, plans, and evidence remain traceable even when they describe earlier release constraints.
- The repository cannot guarantee behavior of an arbitrary AI or unsupported CLI. It guarantees the documented prompt, commands, state rules, validation, and fallback contract.
- The current environment's inability to execute `codex.exe --help` is a verification limitation, not permission to invent another command contract.

## Acceptance criteria

1. A valid marketplace catalog exposes exactly the official `ask-then-do-it` Plugin from the approved subdirectory at `v1.2.0`, and validation rejects wrong source, ref, policy, category, name, or path.
2. Localized documentation presents a state-aware AI-first flow and the official marketplace list/add/upgrade, Plugin list, and `plugin add` command contract with semantically equivalent behavior.
3. Automated checks prove that read-only requests do not instruct writes, explicit install/update requests cover their required state branches, current versions avoid writes, and failures stop without automatic downgrade or alternate sources.
4. README changes are limited to the six existing localized download entries (Codex and Generic in each of three languages), updating both the displayed ZIP version and its release URL from `1.1.0` to `1.2.0`, plus three localized insertions at the approved positions.
5. Canonical and packaged Plugin manifests identify `1.2.0`, declare `#C8262A`, and resolve both approved asset paths inside the Plugin root.
6. `icon.png` and `logo.png` satisfy the approved dimensions, PNG/alpha/transparency/content requirements and are byte-equivalent between canonical-derived unpacked output and the archive.
7. The Codex ZIP contains the assets but no marketplace catalog; the Generic ZIP contains neither Plugin assets nor marketplace catalog.
8. Active release versions, marketplace tag, package names, generated metadata, checksums, documentation, and completed evidence agree on `1.2.0`; historical `1.1.0` evidence remains unchanged.
9. Deterministic rebuild, ZIP equivalence, checksum verification, automated regression tests, Codex and Generic conformance, all Skill validators, canonical and packaged Plugin validation, documentation link checks, and release evidence validation pass.
10. No Git tag, GitHub Release, push, upload, background updater, automatic downgrade, alternate source, lighthouse asset, `logoDark`, or `codex plugin install` support is introduced by the implementation.

## Deferred decisions

- Submission to the universal public Plugins Directory.
- Background notifications, scheduled checks, and unattended upgrades.
- Private forks and configurable marketplace sources.
- Dark-mode-specific logo asset.
- Actual external publication and live target-CLI verification.
