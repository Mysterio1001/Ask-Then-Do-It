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
CODEX_START_GUIDE = (
    ROOT
    / "adapters"
    / "codex"
    / "plugin"
    / "ask-then-do-it"
    / "START-HERE.zh-TW.md"
)
GENERIC_START_GUIDE = ROOT / "release" / "generic" / "START-HERE.zh-TW.md"
USER_ZH_DOCUMENTS = (
    README,
    START_HERE,
    CODEX_GUIDE,
    GENERIC_GUIDE,
    SIMPLE_GUIDE,
    DESIGN,
    CODEX_START_GUIDE,
    GENERIC_START_GUIDE,
)


def localized_sibling(document: Path, locale: str) -> Path:
    return document.with_name(document.name.replace(".zh-TW.md", f".{locale}.md"))


USER_LOCALIZED_DOCUMENTS = tuple(
    localized_sibling(document, locale)
    for document in USER_ZH_DOCUMENTS
    if document != README
    for locale in ("en", "ja")
)

ROOT_START_BY_LOCALE = {
    "zh-TW": START_HERE,
    "en": localized_sibling(START_HERE, "en"),
    "ja": localized_sibling(START_HERE, "ja"),
}

CODEX_START_BY_LOCALE = {
    "zh-TW": CODEX_START_GUIDE,
    "en": localized_sibling(CODEX_START_GUIDE, "en"),
    "ja": localized_sibling(CODEX_START_GUIDE, "ja"),
}

GENERIC_START_BY_LOCALE = {
    "zh-TW": GENERIC_START_GUIDE,
    "en": localized_sibling(GENERIC_START_GUIDE, "en"),
    "ja": localized_sibling(GENERIC_START_GUIDE, "ja"),
}

FLOW_DOCUMENTS_BY_LOCALE = {
    "zh-TW": USER_ZH_DOCUMENTS,
    "en": tuple(
        localized_sibling(document, "en")
        for document in USER_ZH_DOCUMENTS
        if document != README
    ),
    "ja": tuple(
        localized_sibling(document, "ja")
        for document in USER_ZH_DOCUMENTS
        if document != README
    ),
}


class ReleaseDocumentationTests(unittest.TestCase):
    def test_all_nine_start_pages_use_plain_language_batch_test_choices(self) -> None:
        expected = {
            "zh-TW": ("一次", "是否加上測試"),
            "en": ("one response", "whether to add tests"),
            "ja": ("一度に", "テストを追加するか"),
        }
        root_sequences = {
            "zh-TW": "AI 會先提出一個重要問題，等你確認需求後才進入下一階段。Tickets 建立後，AI 會逐張提供測試建議，再由你一次決定每張 Ticket 是否加上測試，最後才核准完整規劃。",
            "en": "The AI will ask one important question first. It will not move to the next stage until you confirm the requirements. After the Tickets are drafted, it gives a test recommendation for each Ticket, then asks you in one response whether to add tests to each Ticket before you approve the complete plan.",
            "ja": "AI は最初に重要な質問を一つ行い、要件が確認されてから次の段階へ進みます。Tickets の作成後、AI は各 Ticket のテスト方針を提案し、すべての Ticket についてテストを追加するかどうかを一度に確認します。最後に計画全体を承認します。",
        }
        for locale, document in ROOT_START_BY_LOCALE.items():
            self.assertIn(
                root_sequences[locale],
                document.read_text(encoding="utf-8"),
            )
        for group in (
            ROOT_START_BY_LOCALE,
            CODEX_START_BY_LOCALE,
            GENERIC_START_BY_LOCALE,
        ):
            for locale, document in group.items():
                body = document.read_text(encoding="utf-8")
                for phrase in expected[locale]:
                    with self.subTest(
                        document=document.relative_to(ROOT), phrase=phrase
                    ):
                        self.assertIn(phrase, body)

    def test_all_localized_flow_documents_avoid_mode_jargon_as_the_choice(self) -> None:
        expected = {
            "zh-TW": ("一次", "是否加上測試"),
            "en": ("one response", "whether to add tests"),
            "ja": ("一度に", "テストを追加するか"),
        }
        forbidden = (
            "選擇 `tdd` 或 `direct`",
            "choose `tdd` or `direct`",
            "select `tdd` or `direct`",
            "tdd or direct",
            "tdd または direct",
            "tdd か direct",
        )
        for locale, documents in FLOW_DOCUMENTS_BY_LOCALE.items():
            for document in documents:
                body = document.read_text(encoding="utf-8")
                for phrase in expected[locale]:
                    with self.subTest(
                        document=document.relative_to(ROOT), phrase=phrase
                    ):
                        self.assertIn(phrase, body)
                for phrase in forbidden:
                    with self.subTest(
                        document=document.relative_to(ROOT), forbidden=phrase
                    ):
                        self.assertNotIn(phrase, body.lower())
                for line in body.splitlines():
                    if "`tdd`" in line and "`direct`" in line:
                        with self.subTest(
                            document=document.relative_to(ROOT), line=line
                        ):
                            normalized = line.lower()
                            self.assertTrue(
                                any(
                                    marker in normalized
                                    for marker in (
                                        "internal",
                                        "record",
                                        "map",
                                        "內部",
                                        "記錄",
                                        "對應",
                                        "内部",
                                        "記録",
                                        "対応",
                                    )
                                ),
                                "Internal values may appear together only in a mapping explanation",
                            )
                            self.assertNotIn("?", line)
                            self.assertNotIn("？", line)

        readme = README.read_text(encoding="utf-8")
        for phrases in expected.values():
            for phrase in phrases:
                self.assertIn(phrase, readme)
        for phrase in forbidden:
            self.assertNotIn(phrase, readme.lower())

    def test_root_start_page_offers_two_direct_consumer_choices(self) -> None:
        self.assertTrue(START_HERE.is_file())
        body = START_HERE.read_text(encoding="utf-8")
        codex = body.index("## 1. 我要在 Codex 使用")
        generic = body.index("## 2. 我要在 Gemini 或其他 AI 使用")
        self.assertLess(codex, generic)
        self.assertIn(
            "https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/"
            "v1.1.0/ask-then-do-it-1.1.0.zip",
            body,
        )
        self.assertIn(
            "https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/"
            "v1.1.0/ask-then-do-it-generic-1.1.0.zip",
            body,
        )
        self.assertNotIn("## 維護者", body)
        self.assertNotIn("python scripts/build_release.py", body)

    def test_readme_links_start_page_before_maintainer_build_command(self) -> None:
        body = README.read_text(encoding="utf-8")
        self.assertLess(
            body.index("START-HERE.zh-TW.md"),
            body.index("python scripts/build_release.py"),
        )

    def test_root_readme_is_traditional_chinese_first_and_routes_both_users(self) -> None:
        body = README.read_text(encoding="utf-8")
        for required in (
            "## 繁體中文快速開始",
            "Codex Plugin",
            "generic-workflow.md",
            "https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.1.0/ask-then-do-it-1.1.0.zip",
            "https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.1.0/ask-then-do-it-generic-1.1.0.zip",
            "python scripts/build_release.py",
        ):
            self.assertIn(required, body)
        self.assertNotIn("dist/codex/ask-then-do-it-1.1.0.zip", body)
        self.assertNotIn("dist/generic/ask-then-do-it-generic-1.1.0.zip", body)
        for obsolete in ("2.1.0", "3.0.0", "checksums-2.1.0"):
            self.assertNotIn(obsolete, body)

    def test_root_entry_documents_exclude_internal_development_conversation(self) -> None:
        forbidden = (
            "一般使用者不需要",
            "canonical source",
            "generated output",
            "personal installation",
            "docs/requirements/",
            "docs/specs/",
            "docs/plans/",
            "docs/evidence/",
            "checksums.sha256",
            "SHA-256",
            "開發歷程",
        )
        for document in (README, START_HERE):
            body = document.read_text(encoding="utf-8")
            for phrase in forbidden:
                with self.subTest(document=document.name, phrase=phrase):
                    self.assertNotIn(phrase, body)
        start_body = START_HERE.read_text(encoding="utf-8")
        self.assertNotIn("dist/codex/", start_body)
        self.assertNotIn("dist/generic/", start_body)

    def test_codex_guide_covers_current_manual_plugin_lifecycle(self) -> None:
        body = CODEX_GUIDE.read_text(encoding="utf-8")
        for required in (
            "ask-then-do-it-1.1.0.zip",
            "## 下載與解壓縮",
            "## 手動安裝",
            "codex plugin add ask-then-do-it --marketplace <local-marketplace-name>",
            "## 第一次使用",
            "## 手動更新",
            "## 手動移除",
            "## 九個 Skill 入口",
            "$ask-then-do-it",
            "$ask-with-docs",
            "$implement-direct",
            "$improve-architecture",
            "Project Knowledge Base",
            "執行測試可能增加工時",
            "`tdd`",
            "`direct`",
            "`tests: skipped-by-user`",
        ):
            self.assertIn(required, body)
        for forbidden in (
            "adapters/codex/",
            "dist/codex/",
            "quick_validate.py",
            "validate_plugin.py",
            "conformance",
            "checksums.sha256",
            "SHA-256",
            "checksum",
            "canonical source",
            "personal installation",
            "generated manifest",
            "cachebuster",
            "docs/specs/",
            "../specs/",
        ):
            self.assertNotIn(forbidden, body)

    def test_generic_guide_covers_current_conversation_only_package(self) -> None:
        body = GENERIC_GUIDE.read_text(encoding="utf-8")
        for required in (
            "ask-then-do-it-generic-1.1.0.zip",
            "## 快速開始",
            "每個新對話",
            "generic-workflow.md",
            "## 保存進度",
            "不能直接修改你的檔案或執行測試",
            "documented-requirements.md",
            "direct-implementation.md",
            "architecture-improvement.md",
            "Project Knowledge Base",
            "第一個需求問題",
            "執行測試可能增加工時",
            "`tdd`",
            "`direct`",
        ):
            self.assertIn(required, body)
        for forbidden in (
            "dist/generic/",
            "canonical prompts",
            "Canonical source",
            "Conversation-only",
            "Generic adapter",
            "profile",
            "approval evidence",
            "UNEXECUTED IMPLEMENTATION GUIDANCE",
            "limited-evidence",
            "non-independent",
            "artifact_type",
            "workflow_id",
            "core_version",
            "checksums.sha256",
            "SHA-256",
            "generated output",
            "python scripts/build_release.py",
            "../specs/",
        ):
            self.assertNotIn(forbidden, body)

    def test_simple_guide_explains_the_complete_flow_in_plain_language(self) -> None:
        body = SIMPLE_GUIDE.read_text(encoding="utf-8")
        self.assertLessEqual(len(body.splitlines()), 180)
        for required in (
            "一次問一題",
            "需求共識",
            "專案知識庫",
            "規格",
            "Ticket",
            "Red",
            "Green",
            "Refactor",
            "Review",
            "架構改善",
            "$ask-then-do-it",
            "$implement-direct",
            "generic-workflow.md",
            "執行測試可能增加工時",
            "`tests: skipped-by-user`",
        ):
            self.assertIn(required, body)
        for forbidden in (
            "Requirement Decision Record",
            "Draft Working Notes",
            "Architecture Improvement Report",
            "UNEXECUTED IMPLEMENTATION GUIDANCE",
            "limited-evidence",
            "non-independent",
            "artifact_type",
            "Rule ID",
            "profile",
            "adapter",
        ):
            self.assertNotIn(forbidden, body)

    def test_design_guide_explains_the_model_neutral_current_workflow(self) -> None:
        body = DESIGN.read_text(encoding="utf-8")
        for required in (
            "Ask Then Do It",
            "Core",
            "Codex Plugin",
            "Generic workflow",
            "Project Knowledge Base",
            "需求共識",
            "規格",
            "Ticket",
            "TDD",
            "Review",
            "架構改善",
        ):
            self.assertIn(required, body)
        for forbidden in (
            "core/",
            "adapters/",
            "docs/",
            "Rule ID",
            "artifact_type",
            "遷移清冊",
            "開發歷程",
            "../specs/",
            "../plans/",
            "../evidence/",
        ):
            self.assertNotIn(forbidden, body)

    def test_all_traditional_chinese_user_documents_exclude_internal_material(self) -> None:
        forbidden = (
            "一般使用者不需要",
            "checksums.sha256",
            "SHA-256",
            "checksum",
            "personal installation",
            "canonical source",
            "generated output",
            "quick_validate.py",
            "validate_plugin.py",
            "conformance",
            "docs/requirements/",
            "docs/specs/",
            "docs/plans/",
            "docs/evidence/",
            "../requirements/",
            "../specs/",
            "../plans/",
            "../evidence/",
        )
        for document in USER_ZH_DOCUMENTS:
            body = document.read_text(encoding="utf-8")
            for phrase in forbidden:
                with self.subTest(document=document.relative_to(ROOT), phrase=phrase):
                    self.assertNotIn(phrase, body)

    def test_every_user_document_has_english_and_japanese_translations(self) -> None:
        for source in USER_ZH_DOCUMENTS:
            if source == README:
                continue
            for locale in ("en", "ja"):
                translated = localized_sibling(source, locale)
                with self.subTest(source=source.relative_to(ROOT), locale=locale):
                    self.assertTrue(translated.is_file(), translated)
                    self.assertGreater(len(translated.read_text(encoding="utf-8")), 100)
        self.assertEqual(list(ROOT.rglob("*.jp.md")), [])

        readme = README.read_text(encoding="utf-8")
        for language_link in (
            "[繁體中文](START-HERE.zh-TW.md)",
            "[English](START-HERE.en.md)",
            "[日本語](START-HERE.ja.md)",
        ):
            self.assertIn(language_link, readme)

    def test_localized_user_documents_keep_commands_and_avoid_internal_material(self) -> None:
        forbidden = (
            "checksums.sha256",
            "SHA-256",
            "checksum",
            "canonical source",
            "generated output",
            "quick_validate.py",
            "validate_plugin.py",
            "conformance",
            "docs/requirements/",
            "docs/specs/",
            "docs/plans/",
            "docs/evidence/",
            "../requirements/",
            "../specs/",
            "../plans/",
            "../evidence/",
        )
        for document in USER_LOCALIZED_DOCUMENTS:
            body = document.read_text(encoding="utf-8")
            for phrase in forbidden:
                with self.subTest(document=document.relative_to(ROOT), phrase=phrase):
                    self.assertNotIn(phrase, body)

        for source in (CODEX_START_GUIDE, CODEX_GUIDE):
            for locale in ("en", "ja"):
                body = localized_sibling(source, locale).read_text(encoding="utf-8")
                for skill in (
                    "$ask-then-do-it",
                    "$ask-requirements",
                    "$ask-with-docs",
                    "$write-spec",
                    "$plan-tickets",
                    "$implement-direct",
                    "$implement-tdd",
                    "$review-code",
                    "$improve-architecture",
                ):
                    self.assertIn(skill, body)
                for required in ("`tdd`", "`direct`", "`tests: skipped-by-user`"):
                    self.assertIn(required, body)

        for source in (GENERIC_START_GUIDE, GENERIC_GUIDE):
            for locale in ("en", "ja"):
                body = localized_sibling(source, locale).read_text(encoding="utf-8")
                self.assertIn("generic-workflow.md", body)
                self.assertIn("direct-implementation.md", body)
                self.assertIn("1.1.0", body)
                self.assertIn("`tdd`", body)
                self.assertIn("`direct`", body)

        for locale in ("en", "ja"):
            simple = localized_sibling(SIMPLE_GUIDE, locale).read_text(encoding="utf-8")
            for required in (
                "$ask-then-do-it",
                "$implement-direct",
                "generic-workflow.md",
                "Red",
                "Green",
                "Refactor",
                "Review",
            ):
                self.assertIn(required, simple)
            design = localized_sibling(DESIGN, locale).read_text(encoding="utf-8")
            for required in ("Core", "Codex Plugin", "Generic workflow", "TDD", "direct", "Review"):
                self.assertIn(required, design)

    def test_all_relative_document_links_resolve(self) -> None:
        documents = [
            README,
            START_HERE,
            *USER_LOCALIZED_DOCUMENTS,
            *sorted((ROOT / "docs").rglob("*.md")),
        ]
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
