"""Offline document contracts; passing these is not Claude behavior evidence."""

import hashlib
import json
import re
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "adapters/claude-code/plugin/ask-then-do-it"
GUIDES = ROOT / "docs/guides"
EVIDENCE = ROOT / "tests/claude/fixtures/platform-support"
LOCALES = ("en", "zh-TW", "ja")
ENTRIES = ("/ask-then-do-it:ask-then-do-it", "/ask-then-do-it:ask-then-do-it-5")
VERSION = "1.4.2"
REPOSITORY = "https://github.com/Mysterio1001/Ask-Then-Do-It"
VERSIONED_GUIDES = f"{REPOSITORY}/blob/v{VERSION}/docs/guides"
DOWNLOAD = f"{REPOSITORY}/releases/download/v{VERSION}/ask-then-do-it-claude-{VERSION}.zip"
HEADINGS = {
    "en": ("Installation and preparation", "Getting started", "Full / Lite modes", "Available commands", "Updating and removal", "Common questions", "License and attribution"),
    "zh-TW": ("安裝與準備", "開始使用", "Full／Lite 模式", "可用指令", "更新與移除", "常見問題", "授權與來源"),
    "ja": ("インストールと準備", "使い始める", "Full／Lite モード", "利用できるコマンド", "更新と削除", "よくある質問", "ライセンスと出典"),
}
DOCTOR_HEALTH = {"en": "installation/configuration health", "zh-TW": "安裝／設定健康", "ja": "インストール／設定の健全性"}
UNVERIFIED = {"en": "unverified items", "zh-TW": "未驗證項目", "ja": "未検証項目"}
MODEL_UNCHANGED = {"en": "neither switches models", "zh-TW": "不會替你切換模型", "ja": "モデルを切り替えません"}
PROHIBITED_CLAIMS = {
    "en": ("/doctor converts Ask Then Do It Skills", "ZIP recovery creates a persistent installation", "All nine combinations are live-verified"),
    "zh-TW": ("/doctor 會轉換 Ask Then Do It Skills", "ZIP recovery 會建立持久安裝", "九組環境全部已完成 live 驗證"),
    "ja": ("/doctor は Ask Then Do It Skills を変換します", "ZIP recovery は永続インストールを作成します", "九つの環境すべてが live 検証済みです"),
}
REFERENCE_SECTIONS = {
    "routing": ("known unsupported", "valid unknown", "router failure", "node-too-old", "envelope", "2.1.251+", "operation", "PostModelSwitch", "best-effort", "binding", "Full", "Lite"),
    "config": ('mode = "full"', 'mode = "lite"', "<project>/.claude/ask-then-do-it.toml", "~/.claude/ask-then-do-it.toml", "settings.json", "Codex Config", "host-unavailable", "active project root"),
    "review": ("`Read`", "`Grep`", "`Glob`", "`independent`", "`non-independent`", "`limited-evidence`", "Lite", "shell", "network"),
    "status": ("claude --version", "node --version", "claude plugin marketplace list --json", "claude plugin list --json", "claude plugin details ask-then-do-it@ask-then-do-it", "read-only", "unknown"),
    "platforms": ("Windows", "macOS", "Linux", "terminal CLI", "VS Code", "JetBrains", "compatibility target", "live-verified", "2026-09-09", "standalone CLI", "2.1.251"),
    "lifecycle": ("Mysterio1001/Ask-Then-Do-It", "`user`", "scope", "claude plugin marketplace add Mysterio1001/Ask-Then-Do-It --scope user", "claude plugin install ask-then-do-it@ask-then-do-it --scope user", "claude plugin marketplace update ask-then-do-it", "claude plugin update ask-then-do-it@ask-then-do-it --scope user", "claude plugin uninstall ask-then-do-it@ask-then-do-it --scope user", "rollback", "reload"),
}


def require_all(body: str, phrases: tuple[str, ...]) -> None:
    for phrase in phrases:
        if phrase not in body and not (phrase == "reload" and "reload" in body.lower()):
            raise AssertionError(f"missing document contract: {phrase}")


def assert_no_false_claims(body: str, locale: str) -> None:
    for prohibited in PROHIBITED_CLAIMS[locale]:
        if prohibited in body:
            raise AssertionError("prohibited product claim: " + prohibited)


def split_advanced_reference(body: str) -> tuple[str, str]:
    marker = '<a id="advanced-reference"></a>'
    if body.count(marker) != 1:
        raise AssertionError("one advanced reference anchor is required")
    panel = re.search(
        re.escape(marker) + r'\n<details>\n<summary>[^<]+</summary>\n(.*?)\n</details>',
        body, re.S,
    )
    if panel is None:
        raise AssertionError("advanced reference must be a closed collapsible section")
    return body[:panel.start()] + body[panel.end():], panel.group(1)


def assert_guide_contract(body: str, locale: str) -> None:
    # The whole guide retains the safety contract; only the visible main flow
    # excludes implementation details. Moving text into the panel cannot hide
    # a false claim or an extra public command from validation.
    assert_reference_contract(body, locale)
    if set(re.findall(r"/ask-then-do-it:[a-z0-9-]+", body)) != set(ENTRIES):
        raise AssertionError("exactly two supported namespaced entries")
    if re.search(r"preview|預覽版|プレビュー", body, re.I):
        raise AssertionError("current guide must use the 1.4.2 target")
    body, _ = split_advanced_reference(body)
    if re.findall(r"^## (.+)$", body, re.M) != list(HEADINGS[locale]):
        raise AssertionError("main guide must keep the seven user-facing chapters")
    installation, start, modes, commands, update, faq, attribution = re.split(r"^## .+$", body, flags=re.M)[1:]
    require_all(installation, ("4.6+", "2.1.251+", "22+", "Claude Code", "Node.js", "user scope", "/plugin marketplace add Mysterio1001/Ask-Then-Do-It", "/plugin install ask-then-do-it@ask-then-do-it", '<a id="zip"></a>', DOWNLOAD, "claude --plugin-dir", "session-only"))
    if re.search(r"(?m)^(?:/plugin |claude plugin ).*(?:update|uninstall)", installation):
        raise AssertionError("first installation must not include updating/removal")
    require_all(start, ("/reload-plugins", ENTRIES[0] + " "))
    require_all(modes, ("Full", "Lite", 'mode = "full"', 'mode = "lite"', "<project>/.claude/ask-then-do-it.toml", "~/.claude/ask-then-do-it.toml", f"getting-started-simple.{locale}.md"))
    require_all(commands, (*ENTRIES, MODEL_UNCHANGED[locale]))
    require_all(update, ("/plugin marketplace update ask-then-do-it", "/plugin update ask-then-do-it@ask-then-do-it", "/reload-plugins", "/plugin uninstall ask-then-do-it@ask-then-do-it --scope user", "--keep-data", "Marketplace"))
    require_all(faq, ("/doctor", DOCTOR_HEALTH[locale], "claude --version", "node --version", "-5", "Windows", "macOS", "Linux", "VS Code", "JetBrains", UNVERIFIED[locale], "#advanced-reference", f"{REPOSITORY}/issues"))
    if set(re.findall(r"/ask-then-do-it:[a-z0-9-]+", body)) != set(ENTRIES):
        raise AssertionError("exactly two supported namespaced entries")
    for internal in ("PostModelSwitch", "envelope", "router failure", "limited-evidence", '<a id="platforms">'):
        if internal in body:
            raise AssertionError("internal detail belongs in the advanced reference: " + internal)
    if re.search(r"preview|預覽版|プレビュー", body, re.I):
        raise AssertionError("current guide must use the 1.4.2 target")
    assert_no_false_claims(body, locale)


def section(body: str, name: str) -> str:
    match = re.search(rf'(?s)<a id="{re.escape(name)}"></a>\n(.*?)(?=<a id=|\Z)', body)
    if match is None:
        raise AssertionError(f"missing document section: {name}")
    return match.group(1)


def assert_reference_contract(body: str, locale: str) -> None:
    require_all(body, (VERSION, f"claude-code.{locale}.md", f"getting-started-simple.{locale}.md"))
    _, advanced = split_advanced_reference(body)
    for name, required in REFERENCE_SECTIONS.items():
        require_all(section(advanced, name), required)
    assert_no_false_claims(body, locale)


def assert_platform_evidence(ledger: dict, root: Path) -> None:
    if ledger.get("schema_version") != 1 or ledger.get("live_verified") is not False:
        raise AssertionError("official documentation is not live evidence")
    date.fromisoformat(ledger["checked_on"])
    sources = {s["id"]: s for s in ledger["sources"]}
    if not sources or len(sources) != len(ledger["sources"]):
        raise AssertionError("unique official sources required")
    for source in sources.values():
        if not source["url"].startswith("https://code.claude.com/docs/en/"):
            raise AssertionError("source must be official Claude documentation")
        if source["status"] == "read":
            text_path = root / source["path"]
            if not text_path.resolve().is_relative_to(root.resolve()):
                raise AssertionError("source snapshot must remain in fixture")
            raw = text_path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != source["sha256"]:
                raise AssertionError("source snapshot hash mismatch")
        elif source["status"] != "unavailable" or not source.get("error"):
            raise AssertionError("unavailable source needs its observed error")
    expected = {(surface, feature) for surface in ("terminal-cli", "vs-code", "jetbrains") for feature in ("plugins", "skills", "agents", "hooks")}
    rows = ledger["matrix"]
    if len(rows) != 12 or {(r["surface"], r["feature"]) for r in rows} != expected:
        raise AssertionError("complete surface/feature matrix required")
    for row in rows:
        if row["status"] not in ("documented", "conditional", "unknown") or not row["limitation"]:
            raise AssertionError("each feature needs bounded status and limitation")
        if row["status"] != "unknown" and not row["evidence"]:
            raise AssertionError("documented feature needs source excerpts")
        for citation in row["evidence"]:
            source = sources[citation["source"]]
            if source["status"] != "read" or not citation["quote"]:
                raise AssertionError("observed source quotation required")
            text = (root / source["path"]).read_text(encoding="utf-8")
            if citation["quote"] not in text:
                raise AssertionError("quotation absent from captured source")



class ClaudeDocumentationTests(unittest.TestCase):
    def test_consumer_entry_documents_link_the_matching_claude_guide(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for locale in LOCALES:
            self.assertIn(f"docs/guides/claude-code.{locale}.md#zip", readme)
            self.assertIn(f"claude-code.{locale}.md", (ROOT / f"START-HERE.{locale}.md").read_text(encoding="utf-8"))
            self.assertIn(f"claude-code.{locale}.md", (GUIDES / f"getting-started-simple.{locale}.md").read_text(encoding="utf-8"))

    def test_three_main_guides_keep_the_user_contract_and_reject_omissions(self) -> None:
        for locale in LOCALES:
            body = (GUIDES / f"claude-code.{locale}.md").read_text(encoding="utf-8")
            with self.subTest(locale=locale):
                assert_guide_contract(body, locale)
            removed_contracts = ("2.1.251+", "4.6+", "22+", '<a id="zip"></a>', "session-only", "--keep-data", UNVERIFIED[locale], MODEL_UNCHANGED[locale], DOCTOR_HEALTH[locale])
            for phrase in removed_contracts:
                with self.subTest(locale=locale, omission=phrase), self.assertRaises(AssertionError):
                    assert_guide_contract(body.replace(phrase, ""), locale)
            for heading in HEADINGS[locale]:
                with self.subTest(locale=locale, heading=heading), self.assertRaises(AssertionError):
                    assert_guide_contract(body.replace("## " + heading, ""), locale)
            mutations = (
                body.replace(DOWNLOAD, f"{REPOSITORY}/releases/latest/download/candidate.zip"),
                body.replace("/plugin marketplace add Mysterio1001/Ask-Then-Do-It", "/plugin marketplace add Mysterio1001/Ask-Then-Do-It#claude-preview"),
                body + "\n/ask-then-do-it:doctor\n",
                body + "\nPostModelSwitch envelope router failure\n",
                *(body + "\n" + prohibited for prohibited in PROHIBITED_CLAIMS[locale]),
            )
            for index, changed in enumerate(mutations):
                with self.subTest(locale=locale, mutation=index), self.assertRaises(AssertionError):
                    assert_guide_contract(changed, locale)

    def test_three_inline_references_preserve_safety_and_evidence_contracts(self) -> None:
        for locale in LOCALES:
            body = (GUIDES / f"claude-code.{locale}.md").read_text(encoding="utf-8")
            with self.subTest(locale=locale):
                assert_reference_contract(body, locale)
            for structural in ('<a id="advanced-reference"></a>', "</details>"):
                with self.subTest(locale=locale, structure=structural), self.assertRaises(AssertionError):
                    assert_reference_contract(body.replace(structural, ""), locale)
            for name in REFERENCE_SECTIONS:
                with self.subTest(locale=locale, missing_section=name), self.assertRaises(AssertionError):
                    assert_reference_contract(body.replace(f'<a id="{name}"></a>', "", 1), locale)
            for phrase in ("node-too-old", "best-effort", "`limited-evidence`", "2026-09-09", "--scope user"):
                with self.subTest(locale=locale, omission=phrase), self.assertRaises(AssertionError):
                    assert_reference_contract(body.replace(phrase, ""), locale)
            for prohibited in PROHIBITED_CLAIMS[locale]:
                with self.subTest(locale=locale, false_claim=prohibited), self.assertRaises(AssertionError):
                    assert_reference_contract(body + "\n" + prohibited, locale)

    def test_twelve_start_pages_exist_and_claude_handoffs_are_brief(self) -> None:
        roots = (ROOT, ROOT / "adapters/codex/plugin/ask-then-do-it", ROOT / "release/generic", PLUGIN)
        starts = [folder / f"START-HERE.{locale}.md" for folder in roots for locale in LOCALES]
        self.assertEqual(len(starts), 12)
        for path in starts:
            self.assertTrue(path.is_file(), path)
        for locale in LOCALES:
            body = (PLUGIN / f"START-HERE.{locale}.md").read_text(encoding="utf-8")
            self.assertLess(len(body.splitlines()), 65)
            self.assertIn(VERSION, body)
            self.assertIn(ENTRIES[0], body)
            self.assertIn("claude --plugin-dir", body)
            self.assertIn("session-only", body)
            self.assertIn(f"{VERSIONED_GUIDES}/claude-code.{locale}.md", body)
            self.assertIn(f"{VERSIONED_GUIDES}/getting-started-simple.{locale}.md", body)
            self.assertNotIn("mode =", body)
            self.assertNotIn("PostModelSwitch", body)

    def test_main_and_advanced_guide_links_resolve_and_do_not_claim_live_results(self) -> None:
        for locale in LOCALES:
            path = GUIDES / f"claude-code.{locale}.md"
            body = path.read_text(encoding="utf-8")
            assert_no_false_claims(body, locale)
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", body):
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT))
                self.assertTrue(resolved.is_file(), (path, target))

    def test_preview_marketplace_branch_syntax_has_captured_official_support(self) -> None:
        source = (EVIDENCE / "plugin-marketplaces.txt").read_text(encoding="utf-8")
        self.assertIn("append @ref to the GitHub shorthand or #ref to a git URL", source)
        self.assertIn("updates to the latest commit of that ref, not the repository’s default branch", source)


    def test_dated_official_feature_evidence_is_complete_and_not_live(self) -> None:
        ledger = json.loads((EVIDENCE / "sources.json").read_text(encoding="utf-8"))
        assert_platform_evidence(ledger, EVIDENCE)
        for mutate in (lambda x: x.update(live_verified=True), lambda x: x.update(matrix=x["matrix"][:-1]), lambda x: x.update(checked_on="unknown")):
            altered = json.loads(json.dumps(ledger))
            mutate(altered)
            with self.assertRaises((AssertionError, ValueError)):
                assert_platform_evidence(altered, EVIDENCE)



if __name__ == "__main__":
    unittest.main()
