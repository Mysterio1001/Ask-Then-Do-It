import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
CODEX_GUIDE = ROOT / "docs" / "guides" / "codex.zh-TW.md"
GENERIC_GUIDE = ROOT / "docs" / "guides" / "generic.zh-TW.md"
SIMPLE_GUIDE = (
    ROOT / "docs" / "guides" / "getting-started-simple.zh-TW.md"
)
DESIGN = ROOT / "docs" / "design" / "ai-development-skills.zh-TW.md"
V3_PLAN = ROOT / "docs" / "plans" / "ai-development-skills-v3.md"
TICKET_6_EVIDENCE = ROOT / "docs" / "evidence" / "v3-ticket-6.md"
RELEASE_EVIDENCE = ROOT / "docs" / "evidence" / "grill-me-release-3.0.0.md"
ARCHITECTURE_DIAGNOSIS = (
    ROOT / "docs" / "evidence" / "v3-release-architecture-diagnosis.md"
)


class ReleaseDocumentationTests(unittest.TestCase):
    def test_root_readme_is_traditional_chinese_first_and_routes_both_users(self) -> None:
        text = README.read_text(encoding="utf-8")
        chinese = text.index("## 繁體中文快速開始")
        english = text.index("## English Quick Start")
        self.assertLess(chinese, english)
        for required in (
            "Codex Plugin",
            "Generic prompts",
            "python scripts/build_release.py",
            "dist/grill-me/",
            "dist/generic-prompts-3.0.0/generic-workflow.md",
            "grill-me-3.0.0.zip",
            "2.1.0",
            "canonical source",
            "generated",
            "personal installation",
        ):
            self.assertIn(required, text)

    def test_codex_guide_covers_plugin_lifecycle_without_stale_source_paths(self) -> None:
        text = CODEX_GUIDE.read_text(encoding="utf-8")
        for required in (
            "adapters/codex/plugin/grill-me/",
            "dist/grill-me/",
            "grill-me-3.0.0.zip",
            "$ai-dev-workflow",
            "手動安裝",
            "手動更新",
            "手動移除",
            "validate_plugin.py",
            "quick_validate.py",
            "不會自動安裝",
            "$grill-with-docs",
            "$improve-architecture",
            "Project Knowledge Base",
            "12 項",
        ):
            self.assertIn(required, text)
        self.assertNotIn("adapters/codex/skills/", text)

    def test_generic_guide_covers_one_file_modular_resume_and_claim_limits(self) -> None:
        text = GENERIC_GUIDE.read_text(encoding="utf-8")
        for required in (
            "dist/generic-prompts-3.0.0/generic-workflow.md",
            "dist/generic-prompts-3.0.0/prompts/",
            "Conversation-only",
            "UNEXECUTED IMPLEMENTATION GUIDANCE",
            "limited-evidence",
            "non-independent",
            "跨 session",
            "恢復工作流",
            "documented-requirements.md",
            "architecture-improvement.md",
            "Project Knowledge Base",
            "unverified",
            "unavailable",
        ):
            self.assertIn(required, text)

    def test_simple_guide_explains_the_complete_flow_in_plain_language(self) -> None:
        text = SIMPLE_GUIDE.read_text(encoding="utf-8")
        for required in (
            "Grill Me 超簡單使用說明",
            "一次問一題",
            "Requirement Decision Record",
            "Specification",
            "Ticket Plan",
            "Red：先看到紅燈",
            "Green：讓燈變綠",
            "Refactor：把房間整理乾淨",
            "Review 檢查成果",
            "在 Codex 裡怎麼用",
            "在 Gemini 或其他 AI 裡怎麼用",
            "怎麼知道 AI 有沒有做對",
            "Project Knowledge Base",
            "Draft Working Notes",
            "12 種眼鏡",
            "Architecture Improvement Report",
            "$grill-with-docs",
            "$improve-architecture",
        ):
            self.assertIn(required, text)

    def test_design_guide_explains_the_model_neutral_v3_extension(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        for required in (
            "Core v3",
            "Project Knowledge Base",
            "Draft Working Notes",
            "12 項",
            "Architecture Improvement Report",
            "模擬刪除",
            "docs/project/knowledge-base.md",
            "MIGRATE-V2-001",
        ):
            self.assertIn(required, text)

    def test_all_relative_document_links_resolve(self) -> None:
        documents = (
            README,
            DESIGN,
            CODEX_GUIDE,
            GENERIC_GUIDE,
            SIMPLE_GUIDE,
            V3_PLAN,
            TICKET_6_EVIDENCE,
            RELEASE_EVIDENCE,
            ARCHITECTURE_DIAGNOSIS,
        )
        pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
        for document in documents:
            text = document.read_text(encoding="utf-8")
            for target in pattern.findall(text):
                if "://" in target or target.startswith("#"):
                    continue
                path_text = target.split("#", 1)[0]
                resolved = (document.parent / path_text).resolve()
                with self.subTest(document=document.name, target=target):
                    self.assertTrue(resolved.exists(), resolved)


if __name__ == "__main__":
    unittest.main()
