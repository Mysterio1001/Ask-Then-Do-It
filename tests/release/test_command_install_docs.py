import subprocess
import unittest
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
DOCS = (
    ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it" / "START-HERE.en.md",
    ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it" / "START-HERE.zh-TW.md",
    ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it" / "START-HERE.ja.md",
    ROOT / "docs" / "guides" / "codex.en.md",
    ROOT / "docs" / "guides" / "codex.zh-TW.md",
    ROOT / "docs" / "guides" / "codex.ja.md",
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


def read_head_readme() -> str:
    result = subprocess.run(
        ["git", "show", "HEAD:README.md"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return result.stdout.decode("utf-8")


def remove_inserted_readme_sections(text: str) -> str:
    markers = (
        ("## Install or update with AI\n", "Read more:\n"),
        ("## 使用指令安裝與更新\n", "更多說明：\n"),
        ("## AI によるインストールと更新\n", "詳しい説明：\n"),
    )
    result = text
    for start, end in markers:
        if start in result:
            begin = result.index(start)
            finish = result.index(end, begin)
            result = result[:begin] + result[finish:]
    return result


class CommandInstallDocumentationTests(unittest.TestCase):
    def test_all_localized_guides_share_the_safe_command_contract(self) -> None:
        for path in DOCS:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                for command in REQUIRED_COMMANDS:
                    self.assertIn(command, text)
                for command in FORBIDDEN_COMMANDS:
                    self.assertNotIn(command, text)
                for concept in ("ZIP", "marketplace"):
                    self.assertIn(concept.lower(), text.lower())
                language = "zh-TW" if "zh-TW" in path.name else "ja" if ".ja." in path.name else "en"
                for concept in LOCALIZED_CONCEPTS[language]:
                    self.assertIn(concept, text)

    def test_readme_changes_stay_inside_the_approved_boundary(self) -> None:
        baseline = read_head_readme()
        current = README.read_text(encoding="utf-8")
        expected = baseline.replace("1.1.0", "1.2.0")
        stripped = remove_inserted_readme_sections(current)
        self.assertEqual(stripped, expected)

        self.assertEqual(current.count("ask-then-do-it-1.2.0.zip"), 6)
        self.assertEqual(current.count("ask-then-do-it-generic-1.2.0.zip"), 6)
        self.assertNotIn("releases/download/v1.1.0/", current)

    def test_readme_has_one_localized_section_before_each_more_information_marker(self) -> None:
        text = README.read_text(encoding="utf-8")
        for heading, marker in (
            ("## Install or update with AI", "Read more:"),
            ("## 使用指令安裝與更新", "更多說明："),
            ("## AI によるインストールと更新", "詳しい説明："),
        ):
            with self.subTest(heading=heading):
                self.assertEqual(text.count(heading), 1)
                self.assertLess(text.index(heading), text.index(marker))

    def test_localized_guide_relative_links_resolve(self) -> None:
        pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
        for document in DOCS:
            for target in pattern.findall(document.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (document.parent / target).resolve()
                with self.subTest(document=document, target=target):
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.exists(), resolved)


if __name__ == "__main__":
    unittest.main()
