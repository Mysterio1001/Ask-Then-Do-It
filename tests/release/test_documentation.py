import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
START_HERE = ROOT / "START-HERE.zh-TW.md"
CODEX_GUIDE = ROOT / "docs" / "guides" / "codex.zh-TW.md"
GENERIC_GUIDE = ROOT / "docs" / "guides" / "generic.zh-TW.md"
SIMPLE_GUIDE = ROOT / "docs" / "guides" / "getting-started-simple.zh-TW.md"
DESIGN = ROOT / "docs" / "design" / "ai-development-skills.zh-TW.md"


class ReleaseDocumentationTests(unittest.TestCase):
    def test_root_start_page_offers_two_consumer_choices_before_maintenance(self) -> None:
        self.assertTrue(START_HERE.is_file())
        body = START_HERE.read_text(encoding="utf-8")
        codex = body.index("## 1. 我要在 Codex 使用")
        generic = body.index("## 2. 我要在 Gemini 或其他 AI 使用")
        maintainer = body.index("## 維護者")
        self.assertLess(codex, generic)
        self.assertLess(generic, maintainer)
        consumer_section = body[:maintainer]
        self.assertIn("dist/codex/ask-then-do-it-1.0.0.zip", consumer_section)
        self.assertIn(
            "dist/generic/ask-then-do-it-generic-1.0.0.zip", consumer_section
        )
        self.assertNotIn("python scripts/build_release.py", consumer_section)

    def test_readme_links_start_page_before_maintainer_build_command(self) -> None:
        body = README.read_text(encoding="utf-8")
        self.assertLess(
            body.index("START-HERE.zh-TW.md"),
            body.index("python scripts/build_release.py"),
        )

    def test_root_readme_is_traditional_chinese_first_and_routes_both_users(self) -> None:
        body = README.read_text(encoding="utf-8")
        self.assertLess(body.index("## 繁體中文快速開始"), body.index("## English Quick Start"))
        for required in (
            "Codex Plugin",
            "Generic prompts",
            "https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.0/ask-then-do-it-1.0.0.zip",
            "https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.0.0/ask-then-do-it-generic-1.0.0.zip",
            "python scripts/build_release.py",
            "canonical source",
            "personal installation",
        ):
            self.assertIn(required, body)
        self.assertNotIn("dist/codex/ask-then-do-it-1.0.0.zip", body)
        self.assertNotIn("dist/generic/ask-then-do-it-generic-1.0.0.zip", body)
        for obsolete in ("2.1.0", "3.0.0", "checksums-2.1.0"):
            self.assertNotIn(obsolete, body)

    def test_codex_guide_covers_current_manual_plugin_lifecycle(self) -> None:
        body = CODEX_GUIDE.read_text(encoding="utf-8")
        for required in (
            "adapters/codex/plugin/ask-then-do-it/",
            "dist/codex/ask-then-do-it-1.0.0.zip",
            "$ask-then-do-it",
            "$ask-with-docs",
            "$improve-architecture",
            "quick_validate.py",
            "validate_plugin.py",
            "Project Knowledge Base",
        ):
            self.assertIn(required, body)
        self.assertNotIn("adapters/codex/skills/", body)
        self.assertNotIn("MIGRATE-V2-001", body)

    def test_generic_guide_covers_current_conversation_only_package(self) -> None:
        body = GENERIC_GUIDE.read_text(encoding="utf-8")
        for required in (
            "dist/generic/ask-then-do-it-generic-1.0.0/generic-workflow.md",
            "dist/generic/ask-then-do-it-generic-1.0.0/prompts/",
            "Conversation-only",
            "UNEXECUTED IMPLEMENTATION GUIDANCE",
            "limited-evidence",
            "non-independent",
            "documented-requirements.md",
            "architecture-improvement.md",
            "Project Knowledge Base",
            "第一個需求問題",
        ):
            self.assertIn(required, body)
        self.assertNotIn("MIGRATE-V2-001", body)

    def test_simple_guide_explains_the_complete_flow_in_plain_language(self) -> None:
        body = SIMPLE_GUIDE.read_text(encoding="utf-8")
        for required in (
            "Requirement Decision Record",
            "Specification",
            "Ticket Plan",
            "Red",
            "Green",
            "Refactor",
            "Review",
            "Project Knowledge Base",
            "Draft Working Notes",
            "Architecture Improvement Report",
            "$ask-with-docs",
            "$improve-architecture",
        ):
            self.assertIn(required, body)

    def test_design_guide_explains_the_model_neutral_current_workflow(self) -> None:
        body = DESIGN.read_text(encoding="utf-8")
        for required in (
            "Core 1.0.0",
            "Project Knowledge Base",
            "Draft Working Notes",
            "Architecture Improvement Report",
            "docs/project/knowledge-base.md",
            "Generic prompts",
            "Codex Plugin",
        ):
            self.assertIn(required, body)
        self.assertNotIn("MIGRATE-V2-001", body)

    def test_all_relative_document_links_resolve(self) -> None:
        documents = [README, START_HERE, *sorted((ROOT / "docs").rglob("*.md"))]
        pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
        for document in documents:
            for target in pattern.findall(document.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                path_text = target.split("#", 1)[0]
                resolved = (document.parent / path_text).resolve()
                with self.subTest(document=document.relative_to(ROOT), target=target):
                    self.assertTrue(resolved.exists(), resolved)


if __name__ == "__main__":
    unittest.main()
