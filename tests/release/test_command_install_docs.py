import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
CODEX_GUIDES = (
    ROOT / "docs" / "guides" / "codex.en.md",
    ROOT / "docs" / "guides" / "codex.zh-TW.md",
    ROOT / "docs" / "guides" / "codex.ja.md",
)
CODEX_STARTS = (
    ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it" / "START-HERE.en.md",
    ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it" / "START-HERE.zh-TW.md",
    ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it" / "START-HERE.ja.md",
)
REQUIRED_COMMANDS = (
    "codex plugin marketplace list",
    "codex plugin marketplace add Mysterio1001/Ask-Then-Do-It",
    "codex plugin marketplace upgrade ask-then-do-it",
    "codex plugin list",
    "codex plugin add ask-then-do-it@ask-then-do-it",
)
FORBIDDEN_COMMANDS = ("codex plugin install",)
LOCALIZED_CONCEPTS = {
    "en": ("new Codex task", "downgrade"),
    "zh-TW": ("新的 Codex 任務", "降級"),
    "ja": ("新しい Codex タスク", "ダウングレード"),
}


def normalize_release_versions(text: str) -> str:
    text = re.sub(r"(?<=-)\d+\.\d+\.\d+(?=\.zip)", "<VERSION>", text)
    return re.sub(r"(?<=/v)\d+\.\d+\.\d+(?=/)", "<VERSION>", text)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def readme_block(body: str, start: str, end: str | None) -> str:
    begin = body.index(start)
    finish = body.index(end, begin) if end else len(body)
    return body[begin:finish]


README_PRESERVED_DIGESTS = {
    "preamble": "417cb00c1890f8d8dc9896d702a5f8b21393b6ea5f149b4bcde6f84cfaeee33e",
    "en": {
        "automatic": "b37758b1bf4a2bcc9851c82601e2d32c8acd7c411472c225308dc8552393e469",
        "manual": "06cf80e46c2c73809607212288d26fa72940fba809254bd49377013ccf44c37f",
        "read-more": "27ce8bda49ab34829834fc762786151de9c9942b8bd1f826b84c244311292ab2",
    },
    "zh-TW": {
        "automatic": "0f1d65607a3de5142b8fa6d671c70c12cd86650119853c85f341618e956e08a0",
        "manual": "648b6ec06aef7fd2d685401d52ddc7a940a2d9c27c349e796367ff3a04208ae0",
        "read-more": "6587249a484cabfa2d78caf37cf4ce449a80b93a51f7bf6299bb8e3bfbcc9514",
    },
    "ja": {
        "automatic": "aab937e6ccad5a242acc2d9ee1eb02997d61ae198f4bd0b17785062b8a575372",
        "manual": "b541ccdfee4ac9407bedd843314592941c06d335506c40a7221d32745c4d1e2a",
        "read-more": "bfd1dbadb1ba45908d64f6dc162263f2b441796e7118196a79b956de6d2779d1",
    },
}


README_LOCALE_SECTIONS = {
    "en": {
        "intro": "## Introduction",
        "quick": "## Quick Start",
        "automatic": "### Automatic installation (CLI)",
        "manual": "### Manual installation",
        "more": "Read more:",
        "next": "## 介紹",
    },
    "zh-TW": {
        "intro": "## 介紹",
        "quick": "## 快速開始",
        "automatic": "### 自動安裝 ( CLI )",
        "manual": "### 手動安裝",
        "more": "更多說明：",
        "next": "## はじめに",
    },
    "ja": {
        "intro": "## はじめに",
        "quick": "## クイックスタート",
        "automatic": "### 自動インストール（CLI）",
        "manual": "### 手動インストール",
        "more": "詳しい説明：",
        "next": None,
    },
}


class CommandInstallDocumentationTests(unittest.TestCase):
    def test_detailed_codex_guides_share_the_safe_command_contract(self) -> None:
        for path in CODEX_GUIDES:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                for command in REQUIRED_COMMANDS:
                    self.assertIn(command, text)
                for command in FORBIDDEN_COMMANDS:
                    self.assertNotIn(command, text)
                for concept in ("ZIP", "marketplace"):
                    self.assertIn(concept.lower(), text.lower())
                language = (
                    "zh-TW"
                    if "zh-TW" in path.name
                    else "ja"
                    if ".ja." in path.name
                    else "en"
                )
                for concept in LOCALIZED_CONCEPTS[language]:
                    self.assertIn(concept, text)

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

    def test_readme_preserved_blocks_are_independent_of_git_head(self) -> None:
        body = README.read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("## Introduction", body)
        preamble = body[: body.index("## Introduction")]
        self.assertEqual(digest(preamble), README_PRESERVED_DIGESTS["preamble"])

        for locale, markers in README_LOCALE_SECTIONS.items():
            required = (
                markers["intro"],
                markers["quick"],
                markers["automatic"],
                markers["manual"],
                markers["more"],
            )
            self.assertTrue(
                all(marker in body for marker in required),
                f"Missing README marker for {locale}: {required}",
            )
            automatic = normalize_release_versions(
                readme_block(body, markers["automatic"], markers["manual"])
            )
            manual = normalize_release_versions(
                readme_block(body, markers["manual"], markers["more"])
            )
            read_more = normalize_release_versions(
                readme_block(body, markers["more"], markers["next"]).rstrip() + "\n"
            )
            expected = README_PRESERVED_DIGESTS[locale]
            with self.subTest(locale=locale, block="automatic"):
                self.assertEqual(digest(automatic), expected["automatic"])
            with self.subTest(locale=locale, block="manual"):
                self.assertEqual(digest(manual), expected["manual"])
            with self.subTest(locale=locale, block="read-more"):
                self.assertEqual(digest(read_more), expected["read-more"])

    def test_readme_keeps_install_heading_order_and_single_sections(self) -> None:
        body = README.read_text(encoding="utf-8")
        for locale, markers in README_LOCALE_SECTIONS.items():
            section = readme_block(body, markers["intro"], markers["next"])
            ordered = [
                markers["intro"],
                markers["quick"],
                markers["automatic"],
                "#### Codex CLI",
                markers["manual"],
                markers["more"],
            ]
            self.assertTrue(
                all(marker in body for marker in ordered),
                f"Missing README marker for {locale}: {ordered}",
            )
            positions = [section.index(marker) for marker in ordered]
            with self.subTest(locale=locale):
                self.assertEqual(positions, sorted(positions))
            for marker in ordered:
                expected_count = 3 if marker == "#### Codex CLI" else 1
                with self.subTest(locale=locale, marker=marker):
                    self.assertEqual(body.count(marker), expected_count)

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
