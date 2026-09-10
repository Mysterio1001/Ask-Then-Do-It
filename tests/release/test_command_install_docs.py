"""Installation commands and README navigation, independent of prose hashes."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
LOCALES = ("en", "zh-TW", "ja")
CODEX_GUIDES = tuple(ROOT / f"docs/guides/codex.{locale}.md" for locale in LOCALES)
CODEX_STARTS = tuple(ROOT / f"adapters/codex/plugin/ask-then-do-it/START-HERE.{locale}.md" for locale in LOCALES)
REQUIRED_COMMANDS = (
    "codex plugin marketplace list",
    "codex plugin marketplace add Mysterio1001/Ask-Then-Do-It",
    "codex plugin marketplace upgrade ask-then-do-it",
    "codex plugin list",
    "codex plugin add ask-then-do-it@ask-then-do-it",
    "codex plugin remove ask-then-do-it --marketplace ask-then-do-it",
)
LOCALIZED_CONCEPTS = {
    "en": (r"new Codex task", r"downgrade", r"disabled", r"backup", r"Restore"),
    "zh-TW": (r"新的 Codex 任務", r"降版|降級", r"停用", r"備份", r"還原"),
    "ja": (r"新しい Codex タスク", r"降版|ダウングレード", r"無効化", r"バックアップ", r"戻せ"),
}
README_LOCALE_SECTIONS = {
    "en": {
        "intro": "## Introduction", "quick": "## Quick Start",
        "automatic": "### Automatic installation (CLI)", "manual": "### Manual installation",
        "more": "Read more:", "update": "## Updating", "next": "## 介紹",
    },
    "zh-TW": {
        "intro": "## 介紹", "quick": "## 快速開始",
        "automatic": "### 自動安裝 ( CLI )", "manual": "### 手動安裝",
        "more": "更多說明：", "update": "## 更新方式", "next": "## はじめに",
    },
    "ja": {
        "intro": "## はじめに", "quick": "## クイックスタート",
        "automatic": "### 自動インストール（CLI）", "manual": "### 手動インストール",
        "more": "詳しい説明：", "update": "## 更新方法", "next": None,
    },
}


def readme_block(body: str, start: str, end: str | None) -> str:
    if start not in body or (end and end not in body):
        raise AssertionError(f"Missing README boundary: {start}, {end}")
    begin = body.index(start)
    finish = body.index(end, begin) if end else len(body)
    return body[begin:finish]


def assert_readme_layout(body: str) -> None:
    """Protect user-approved layout without restoring old insertion markers."""
    if "<!-- claude:" in body:
        raise AssertionError("Obsolete insertion markers must not return")
    for locale, markers in README_LOCALE_SECTIONS.items():
        section = readme_block(body, markers["intro"], markers["next"])
        ordered = [markers["intro"], markers["quick"], markers["automatic"], "#### Codex CLI", "#### Claude Code", markers["manual"], markers["more"], markers["update"]]
        if any(section.count(marker) != 1 for marker in ordered):
            raise AssertionError(f"Each README section must occur once: {locale}")
        positions = [section.index(marker) for marker in ordered]
        if positions != sorted(positions):
            raise AssertionError(f"README section order changed: {locale}")
        quick = readme_block(section, markers["quick"], markers["manual"])
        commands = re.findall(r"^(?:codex plugin |/plugin ).+$", quick, re.M)
        if commands != [
            "codex plugin marketplace add Mysterio1001/Ask-Then-Do-It",
            "codex plugin add ask-then-do-it@ask-then-do-it",
            "/plugin marketplace add Mysterio1001/Ask-Then-Do-It",
            "/plugin install ask-then-do-it@ask-then-do-it",
        ]:
            raise AssertionError("Quick Start must contain only first-install commands")
        more = readme_block(section, markers["more"], markers["update"])
        links = re.findall(r"\[[^]]+\]\(([^)]+)\)", more)
        expected = [f"docs/guides/{name}.{locale}.md" for name in ("getting-started-simple", "codex", "claude-code", "generic")]
        expected.append(f"docs/design/ai-development-skills.{locale}.md")
        if links != expected:
            raise AssertionError("Read-more links must remain beginner, Codex, Claude, Generic, design")
        update = readme_block(section, markers["update"], None)
        if not re.search(r"(?s)<details>\s*<summary>.+?</summary>.*</details>", update):
            raise AssertionError("Updating must have its own collapsible section")
        updates = re.findall(r"^(?:codex plugin |/plugin |/reload-plugins).*$", update, re.M)
        if updates != [
            "codex plugin marketplace upgrade ask-then-do-it",
            "/plugin marketplace update ask-then-do-it",
            "/plugin update ask-then-do-it@ask-then-do-it",
            "/reload-plugins",
        ]:
            raise AssertionError("Updating must preserve supported host commands")


class CommandInstallDocumentationTests(unittest.TestCase):
    def test_detailed_codex_guides_share_the_safe_command_contract(self) -> None:
        for locale, path in zip(LOCALES, CODEX_GUIDES):
            body = path.read_text(encoding="utf-8")
            with self.subTest(locale=locale):
                for command in REQUIRED_COMMANDS:
                    self.assertIn(command, body)
                self.assertNotIn("codex plugin install", body)
                for command in (
                    "codex plugin add ask-then-do-it --marketplace <local-marketplace-name>",
                    "codex plugin list --marketplace <local-marketplace-name>",
                ):
                    self.assertIn(command, body)
                for concept in LOCALIZED_CONCEPTS[locale]:
                    self.assertRegex(body, concept)
                self.assertIn('<a id="zip"></a>', body)
                self.assertIn("plugins/ask-then-do-it/", body)
                self.assertIn("https://developers.openai.com/plugins/build/plugins", body)

    def test_start_pages_handoff_to_the_detailed_command_contract(self) -> None:
        for path in CODEX_STARTS:
            text = path.read_text(encoding="utf-8")
            language = (
                "zh-TW"
                if "zh-TW" in path.name
                else "ja"
                if ".ja." in path.name
                else "en"
            )
            with self.subTest(path=path):
                self.assertIn(f"/docs/guides/codex.{language}.md", text)
                self.assertNotIn("codex plugin install", text)

    def test_readme_keeps_install_update_and_navigation_layout(self) -> None:
        assert_readme_layout(README.read_text(encoding="utf-8"))

    def test_readme_contract_rejects_mixed_install_update_and_navigation_drift(self) -> None:
        body = README.read_text(encoding="utf-8")
        mutations = {
            "update-in-install": body.replace("# Install", "# Install\ncodex plugin marketplace upgrade ask-then-do-it", 1),
            "invalid-codex-command": body.replace("codex plugin add ask-then-do-it@ask-then-do-it", "codex plugin install ask-then-do-it@ask-then-do-it", 1),
            "missing-collapse": body.replace("<details>", "", 1),
            "wrong-update": body.replace("/plugin update ask-then-do-it@ask-then-do-it", "/plugin install ask-then-do-it@ask-then-do-it", 1),
            "missing-update-heading": body.replace("## Updating", "", 1),
            "read-more-order": body.replace("docs/guides/getting-started-simple.en.md", "docs/guides/generic.en.md", 1),
            "old-markers": body + "\n<!-- claude:begin -->old<!-- claude:end -->\n",
        }
        for name, changed in mutations.items():
            with self.subTest(mutation=name), self.assertRaises(AssertionError):
                assert_readme_layout(changed)

    def test_localized_guide_relative_links_resolve(self) -> None:
        pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
        for document in CODEX_GUIDES:
            for target in pattern.findall(document.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (document.parent / target).resolve()
                with self.subTest(document=document, target=target):
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.exists(), resolved)


if __name__ == "__main__":
    unittest.main()
