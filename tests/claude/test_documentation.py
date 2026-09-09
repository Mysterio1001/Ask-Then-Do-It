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
PREVIEW_VERSION = "1.4.0-preview.1"
REPOSITORY = "https://github.com/Mysterio1001/Ask-Then-Do-It"
VERSIONED_GUIDES = f"{REPOSITORY}/blob/v{PREVIEW_VERSION}/docs/guides"
MARKETPLACE_URL = f"{REPOSITORY}.git#claude-preview"
PREVIEW_DOWNLOAD = f"{REPOSITORY}/releases/download/v{PREVIEW_VERSION}/ask-then-do-it-claude-{PREVIEW_VERSION}.zip"
BASELINES = {
    "README.md": "11333edd62e58231de0e06c936a646b075eb3c69b93b3c6b36a679d086b6d8d5",
    "START-HERE.en.md": "5511566652ff38a7454fbc69d4f71dfaaa7211dfff9d4bb33239f8009cc4f687",
    "START-HERE.ja.md": "0e762b6ab92901964115ce9ed66ad4be4cf44988710082cac34fca5354ac2d2f",
    "START-HERE.zh-TW.md": "418fd97a88f55bf04abf0bfe3595136920b9f2805c8e4e69b5f150ec9be1e9b7",
    "docs/guides/getting-started-simple.en.md": "abbf30d86f571694c01dde65e9aa550a7d3cfbe9632d6ba1bf66027c60f46d39",
    "docs/guides/getting-started-simple.ja.md": "76f77e55bda741b920258c94560b2ae242c248b6fcc1fa81f1cd7459c05a98ae",
    "docs/guides/getting-started-simple.zh-TW.md": "88ed19078e50ba18f92659bd0673a47e58d029b741a4845e43558151c64cded1",
}
SECTIONS = {
    "versions": (PREVIEW_VERSION, "1.3.1", "Claude", "4.6+", "Claude Code", "2.1.251+", "Node.js", "22+", "strict", "local automated tests"),
    "entries": (*ENTRIES, "model: inherit", "bare"),
    "routing": ("known unsupported", "valid unknown", "router failure", "PostModelSwitch", "operation", "best-effort"),
    "config": ('mode = "full"', 'mode = "lite"', "<project>/.claude/ask-then-do-it.toml", "~/.claude/ask-then-do-it.toml", "settings.json", "Codex Config"),
    "review": ("Read", "Grep", "Glob", "independent", "non-independent", "limited-evidence", "Lite"),
    "status": ("claude --version", "node --version", "claude plugin marketplace list", "claude plugin list", "claude plugin details", "read-only"),
    "install-update": ("--scope user", MARKETPLACE_URL, "ask-then-do-it@ask-then-do-it", "disabled", "newer", "/reload-plugins", "claude plugin marketplace update ask-then-do-it", "claude plugin update ask-then-do-it@ask-then-do-it --scope user"),
    "remove": ("claude plugin uninstall ask-then-do-it@ask-then-do-it --scope user", "--keep-data", "Config", "Marketplace"),
    "zip": ("--plugin-dir", "session-only", PREVIEW_DOWNLOAD, "persistent", "~/.claude/skills"),
    "platforms": ("Windows", "macOS", "Linux", "terminal CLI", "VS Code", "JetBrains", "compatibility target", "live-verified", "2026-09-09"),
    "troubleshooting": ("/doctor", "UserPromptExpansion", "Node", "strict", "2.1.251"),
    "feedback": (f"{REPOSITORY}/issues", PREVIEW_VERSION, "Claude Code", "Node", "model"),
}
PREVIEW_STATUS = {"en": "public preview", "zh-TW": "公開預覽版", "ja": "公開プレビュー"}
DEFERRED = {"en": "deferred", "zh-TW": "延後驗證", "ja": "検証を延期"}
DOCTOR_HEALTH = {"en": "installation/configuration health", "zh-TW": "安裝／設定健康", "ja": "インストール／設定の健全性"}
PROHIBITED_CLAIMS = {
    "en": ("/doctor converts Ask Then Do It Skills", "ZIP recovery creates a persistent installation", "All nine combinations are live-verified"),
    "zh-TW": ("/doctor 會轉換 Ask Then Do It Skills", "ZIP recovery 會建立持久安裝", "九組環境全部已完成 live 驗證"),
    "ja": ("/doctor は Ask Then Do It Skills を変換します", "ZIP recovery は永続インストールを作成します", "九つの環境すべてが live 検証済みです"),
}


def section(body: str, name: str) -> str:
    match = re.search(rf'(?s)<a id="{re.escape(name)}"></a>\n(.*?)(?=<a id=|\Z)', body)
    if match is None:
        raise AssertionError(f"missing document section: {name}")
    return match.group(1)


def assert_guide_contract(body: str, locale: str) -> None:
    if PREVIEW_STATUS[locale] not in section(body, "versions"):
        raise AssertionError("guide must disclose public preview status")
    if DEFERRED[locale] not in section(body, "versions"):
        raise AssertionError("guide must disclose deferred official-session verification")
    for name, required in SECTIONS.items():
        content = section(body, name)
        for phrase in required:
            if phrase not in content:
                raise AssertionError(f"{name}: missing {phrase}")
    if DOCTOR_HEALTH[locale] not in section(body, "troubleshooting"):
        raise AssertionError("doctor must be scoped to host health")
    if re.search(r"https://[^\s)]+/releases/download/v1\.4\.0/", body):
        raise AssertionError("preview must not link to an unreleased stable Claude download")
    if "claude plugin marketplace add Mysterio1001/Ask-Then-Do-It" in body:
        raise AssertionError("Claude preview must use the opt-in marketplace branch")
    public_entries = set(re.findall(r"/ask-then-do-it:[a-z0-9-]+", body))
    if public_entries != set(ENTRIES):
        raise AssertionError("exactly two supported namespaced entries")
    for prohibited in PROHIBITED_CLAIMS[locale]:
        if prohibited in body:
            raise AssertionError("prohibited product claim: " + prohibited)


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
    def test_existing_documents_are_changed_only_by_localized_insertions(self) -> None:
        for name, digest in BASELINES.items():
            body = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("<!-- claude:begin -->", body, name)
            restored = re.sub(r"(?s)<!-- claude:begin -->.*?<!-- claude:end -->\n", "", body)
            self.assertEqual(hashlib.sha256(restored.encode()).hexdigest(), digest, name)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for locale in LOCALES:
            self.assertIn(f"docs/guides/claude-code.{locale}.md", readme)
            self.assertIn(f"claude-code.{locale}.md", (ROOT / f"START-HERE.{locale}.md").read_text(encoding="utf-8"))
            self.assertIn(f"claude-code.{locale}.md", (GUIDES / f"getting-started-simple.{locale}.md").read_text(encoding="utf-8"))

    def test_three_guides_cover_same_contract_and_reject_omissions(self) -> None:
        for locale in LOCALES:
            with self.subTest(locale=locale):
                body = (GUIDES / f"claude-code.{locale}.md").read_text(encoding="utf-8")
                assert_guide_contract(body, locale)
                for name in SECTIONS:
                    with self.assertRaises(AssertionError):
                        assert_guide_contract(body.replace(f'<a id="{name}"></a>', "", 1), locale)
                for wrong in (body.replace("2.1.251+", "2.1.250+"), body.replace(MARKETPLACE_URL, f"{REPOSITORY}.git"), body.replace(PREVIEW_DOWNLOAD, f"{REPOSITORY}/releases/latest/download/candidate.zip"), body.replace(DEFERRED[locale], ""), body + "\n/ask-then-do-it:doctor\n", body + "\nhttps://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.4.0/candidate.zip\n"):
                    with self.assertRaises(AssertionError):
                        assert_guide_contract(wrong, locale)
                for prohibited in PROHIBITED_CLAIMS[locale]:
                    with self.assertRaises(AssertionError):
                        assert_guide_contract(body + "\n" + prohibited, locale)

    def test_twelve_start_pages_exist_and_claude_handoffs_are_brief(self) -> None:
        roots = (ROOT, ROOT / "adapters/codex/plugin/ask-then-do-it", ROOT / "release/generic", PLUGIN)
        starts = [folder / f"START-HERE.{locale}.md" for folder in roots for locale in LOCALES]
        self.assertEqual(len(starts), 12)
        for path in starts:
            self.assertTrue(path.is_file(), path)
        for locale in LOCALES:
            body = (PLUGIN / f"START-HERE.{locale}.md").read_text(encoding="utf-8")
            self.assertLess(len(body.splitlines()), 65)
            self.assertIn(PREVIEW_VERSION, body)
            self.assertIn(PREVIEW_STATUS[locale], body)
            self.assertIn(DEFERRED[locale], body)
            for entry in ENTRIES:
                self.assertIn(entry, body)
            self.assertIn(f"{VERSIONED_GUIDES}/claude-code.{locale}.md", body)
            self.assertNotIn("mode =", body)

    def test_new_local_document_links_resolve_and_no_stable_claude_download(self) -> None:
        documents = [ROOT / "README.md", *(ROOT / f"START-HERE.{locale}.md" for locale in LOCALES), *(GUIDES / f"claude-code.{locale}.md" for locale in LOCALES), *(PLUGIN / f"START-HERE.{locale}.md" for locale in LOCALES)]
        for path in documents:
            body = path.read_text(encoding="utf-8")
            self.assertNotRegex(body, r"https://[^\s)]+/releases/download/v1\.4\.0/")
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", body):
                if "://" in target or target.startswith("#"):
                    continue
                target = target.split("#")[0]
                resolved = ROOT / target.lstrip("/") if target.startswith("/") else path.parent / target
                self.assertTrue(resolved.exists(), (path, target))

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
