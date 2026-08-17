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

# README is the navigation root, so it does not need a self-referential footer.
USER_FOOTER_DOCUMENTS = tuple(
    document for document in USER_ZH_DOCUMENTS if document != README
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

CODEX_GUIDES_BY_LOCALE = {
    "zh-TW": CODEX_GUIDE,
    "en": localized_sibling(CODEX_GUIDE, "en"),
    "ja": localized_sibling(CODEX_GUIDE, "ja"),
}

GENERIC_GUIDES_BY_LOCALE = {
    "zh-TW": GENERIC_GUIDE,
    "en": localized_sibling(GENERIC_GUIDE, "en"),
    "ja": localized_sibling(GENERIC_GUIDE, "ja"),
}

SIMPLE_GUIDES_BY_LOCALE = {
    "zh-TW": SIMPLE_GUIDE,
    "en": localized_sibling(SIMPLE_GUIDE, "en"),
    "ja": localized_sibling(SIMPLE_GUIDE, "ja"),
}

DESIGN_GUIDES_BY_LOCALE = {
    "zh-TW": DESIGN,
    "en": localized_sibling(DESIGN, "en"),
    "ja": localized_sibling(DESIGN, "ja"),
}

VERSIONED_GUIDE_ROOT = (
    "https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/docs/guides"
)
VERSIONED_README = (
    "https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.3.0/README.md"
)


def user_document_footer(document: Path) -> str:
    package_starts = (*CODEX_START_BY_LOCALE.values(), *GENERIC_START_BY_LOCALE.values())
    root_starts = ROOT_START_BY_LOCALE.values()

    if document in package_starts:
        target = VERSIONED_README
    elif document in root_starts:
        target = "README.md"
    else:
        target = "../../README.md"

    if document == README:
        target = "README.md"
        label = "回到 README"
    elif document.name.endswith(".en.md"):
        label = "Back to README"
    elif document.name.endswith(".ja.md"):
        label = "README に戻る"
    else:
        label = "回到 README"
    return f"[{label}]({target})"


def document_section(body: str, start: str, end: str | None) -> str:
    begin = body.index(start)
    finish = body.index(end, begin) if end else len(body)
    return body[begin:finish]


class ReleaseDocumentationTests(unittest.TestCase):
    def test_user_documents_end_with_readme_footer(self) -> None:
        documents = (*USER_FOOTER_DOCUMENTS, *USER_LOCALIZED_DOCUMENTS)
        for document in documents:
            body = document.read_text(encoding="utf-8")
            expected = user_document_footer(document)
            with self.subTest(document=document.relative_to(ROOT)):
                self.assertEqual(body.rstrip().splitlines()[-1], expected)

    def test_all_nine_start_pages_are_concise_full_lite_handoffs(self) -> None:
        expected_links = {
            "root": {
                "zh-TW": (
                    "docs/guides/codex.zh-TW.md",
                    "docs/guides/generic.zh-TW.md",
                    "docs/guides/getting-started-simple.zh-TW.md",
                ),
                "en": (
                    "docs/guides/codex.en.md",
                    "docs/guides/generic.en.md",
                    "docs/guides/getting-started-simple.en.md",
                ),
                "ja": (
                    "docs/guides/codex.ja.md",
                    "docs/guides/generic.ja.md",
                    "docs/guides/getting-started-simple.ja.md",
                ),
            },
            "codex": {
                locale: (
                    f"{VERSIONED_GUIDE_ROOT}/codex.{locale}.md",
                    f"{VERSIONED_GUIDE_ROOT}/getting-started-simple.{locale}.md",
                )
                for locale in ("zh-TW", "en", "ja")
            },
            "generic": {
                locale: (
                    f"{VERSIONED_GUIDE_ROOT}/generic.{locale}.md",
                    f"{VERSIONED_GUIDE_ROOT}/getting-started-simple.{locale}.md",
                )
                for locale in ("zh-TW", "en", "ja")
            },
        }
        groups = {
            "root": ROOT_START_BY_LOCALE,
            "codex": CODEX_START_BY_LOCALE,
            "generic": GENERIC_START_BY_LOCALE,
        }
        forbidden = (
            "500 tokens",
            "800 tokens",
            "~/.codex/ask-then-do-it.toml",
            "<project>/.codex/ask-then-do-it.toml",
            "Default workflow mode:",
            "whether to add tests",
            "是否加上測試",
            "テストを追加するか",
            "`tdd`",
            "`direct`",
            "Red, Green, and Refactor",
            "Red、Green、Refactor",
            "| --- |",
        )
        for group_name, group in groups.items():
            for locale, document in group.items():
                body = document.read_text(encoding="utf-8")
                with self.subTest(group=group_name, locale=locale, contract="headings"):
                    self.assertLessEqual(body.count("\n## "), 3)
                self.assertIn("Full", body)
                self.assertIn("Lite", body)
                for link in expected_links[group_name][locale]:
                    with self.subTest(group=group_name, locale=locale, link=link):
                        self.assertIn(link, body)
                for phrase in forbidden:
                    with self.subTest(
                        group=group_name, locale=locale, forbidden=phrase
                    ):
                        self.assertNotIn(phrase, body)

    def test_detailed_full_guides_keep_plain_language_ticket_test_choices(self) -> None:
        expected = {
            "zh-TW": ("一次回覆", "是否加上測試"),
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
        for locale, documents in {
            locale: (
                SIMPLE_GUIDES_BY_LOCALE[locale],
                CODEX_GUIDES_BY_LOCALE[locale],
                GENERIC_GUIDES_BY_LOCALE[locale],
            )
            for locale in ("zh-TW", "en", "ja")
        }.items():
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

    def test_root_start_page_offers_two_direct_consumer_choices(self) -> None:
        self.assertTrue(START_HERE.is_file())
        body = START_HERE.read_text(encoding="utf-8")
        codex = body.index("## 1. 我要在 Codex 使用")
        generic = body.index("## 2. 我要在 Gemini 或其他 AI 使用")
        self.assertLess(codex, generic)
        self.assertIn(
            "https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/"
            "v1.3.0/ask-then-do-it-1.3.0.zip",
            body,
        )
        self.assertIn(
            "https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/"
            "v1.3.0/ask-then-do-it-generic-1.3.0.zip",
            body,
        )
        self.assertNotIn("## 維護者", body)
        self.assertNotIn("python scripts/build_release.py", body)

    def test_readme_links_start_page_before_each_locale_more_section(self) -> None:
        body = README.read_text(encoding="utf-8")
        for start_page, more_marker in (
            ("START-HERE.en.md", "Read more:"),
            ("START-HERE.zh-TW.md", "更多說明："),
            ("START-HERE.ja.md", "詳しい説明："),
        ):
            with self.subTest(start_page=start_page):
                self.assertLess(body.index(start_page), body.index(more_marker))

    def test_readme_uses_approved_localized_introduction_and_quick_start_order(
        self,
    ) -> None:
        body = README.read_text(encoding="utf-8")
        expected = {
            "en": (
                "## Introduction",
                "[User Guide](/START-HERE.en.md)",
                "## Quick Start",
                "### Automatic installation (CLI)",
                "#### Codex CLI",
                "### Manual installation",
                "Read more:",
            ),
            "zh-TW": (
                "## 介紹",
                "[使用說明](/START-HERE.zh-TW.md)",
                "## 快速開始",
                "### 自動安裝 ( CLI )",
                "#### Codex CLI",
                "### 手動安裝",
                "更多說明：",
            ),
            "ja": (
                "## はじめに",
                "[利用ガイド](/START-HERE.ja.md)",
                "## クイックスタート",
                "### 自動インストール（CLI）",
                "#### Codex CLI",
                "### 手動インストール",
                "詳しい説明：",
            ),
        }
        next_locale_heading = {
            "en": "## 介紹",
            "zh-TW": "## はじめに",
            "ja": None,
        }
        forbidden_intro_detail = (
            "500 tokens",
            "800 tokens",
            "~/.codex/ask-then-do-it.toml",
            "<project>/.codex/ask-then-do-it.toml",
            "Default workflow mode:",
            "`tdd`",
            "`direct`",
        )
        for locale, markers in expected.items():
            self.assertTrue(
                all(marker in body for marker in markers),
                f"Missing README marker for {locale}: {markers}",
            )
            section = document_section(
                body, markers[0], next_locale_heading[locale]
            )
            positions = [section.index(marker) for marker in markers]
            with self.subTest(locale=locale, contract="order"):
                self.assertEqual(positions, sorted(positions))
            for marker in markers:
                with self.subTest(locale=locale, marker=marker):
                    expected_count = 3 if marker == "#### Codex CLI" else 1
                    self.assertEqual(body.count(marker), expected_count)
            introduction = section[positions[0] : positions[2]]
            self.assertIn("Full", introduction)
            self.assertIn("Lite", introduction)
            self.assertIn("Config", introduction)
            self.assertLessEqual(len(introduction), 900)
            for forbidden in forbidden_intro_detail:
                with self.subTest(locale=locale, intro_forbidden=forbidden):
                    self.assertNotIn(forbidden, introduction)

        for obsolete in (
            "## Installation and updates",
            "## 安裝與更新",
            "## インストールと更新",
        ):
            self.assertNotIn(obsolete, body)

    def test_root_readme_routes_both_users(self) -> None:
        body = README.read_text(encoding="utf-8")
        for required in (
            "## 介紹",
            "## 快速開始",
            "Codex Plugin",
            "generic-workflow.md",
            "https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-1.3.0.zip",
            "https://github.com/Mysterio1001/Ask-Then-Do-It/releases/download/v1.3.0/ask-then-do-it-generic-1.3.0.zip",
        ):
            self.assertIn(required, body)
        self.assertNotIn("dist/codex/ask-then-do-it-1.3.0.zip", body)
        self.assertNotIn("dist/generic/ask-then-do-it-generic-1.3.0.zip", body)
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
            "ask-then-do-it-1.3.0.zip",
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
            "ask-then-do-it-generic-1.3.0.zip",
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

    def test_localized_codex_guides_document_mode_config_contract(self) -> None:
        expected = {
            "zh-TW": {
                "heading": "## 流程模式設定",
                "end": "## 第一次使用",
                "precedence": (
                    "目前操作的明確指示",
                    "專案 Config",
                    "使用者 Config",
                    "Full fallback",
                ),
                "semantics": (
                    "專案 Config 不存在時，才繼續讀取使用者 Config",
                    "無效的專案 Config 會直接回到 Full",
                    "不會繼續讀取使用者 Config",
                    "不需要讀取 Config",
                    "模式判定是唯讀操作",
                    "不會建立、寫入、修復或正規化",
                    "只影響目前操作",
                    "新的工作階段",
                    "高風險",
                ),
            },
            "en": {
                "heading": "## Workflow mode configuration",
                "end": "## First use",
                "precedence": (
                    "explicit instruction for the current operation",
                    "Project Config",
                    "User Config",
                    "Full fallback",
                ),
                "semantics": (
                    "An absent Project Config continues to User Config",
                    "A present invalid Project Config falls back to Full",
                    "does not continue to User Config",
                    "without reading Config",
                    "Mode resolution is read-only",
                    "does not create, write, repair, or normalize",
                    "only the current operation",
                    "new session",
                    "High-risk",
                ),
            },
            "ja": {
                "heading": "## ワークフローモードの設定",
                "end": "## 初回使用",
                "precedence": (
                    "現在の操作に対する明示的な指示",
                    "プロジェクト Config",
                    "ユーザー Config",
                    "Full fallback",
                ),
                "semantics": (
                    "プロジェクト Config が存在しない場合だけ",
                    "無効なプロジェクト Config は Full にフォールバック",
                    "ユーザー Config には進みません",
                    "Config を読み取らずに優先",
                    "モード判定は読み取り専用",
                    "作成、書き込み、修復、正規化しません",
                    "現在の操作だけ",
                    "新しいセッション",
                    "高リスク",
                ),
            },
        }
        common_literals = (
            "`~/.codex/ask-then-do-it.toml`",
            "`<project>/.codex/ask-then-do-it.toml`",
            '`mode = "full"`',
            '`mode = "lite"`',
            "`mode = lite`",
            '`mode = "fast"`',
        )
        for locale, document in CODEX_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            contract = expected[locale]
            self.assertIn(contract["heading"], body)
            self.assertIn(contract["end"], body)
            start = body.index(contract["heading"])
            end = body.index(contract["end"], start)
            section = body[start:end]
            positions = [section.index(marker) for marker in contract["precedence"]]
            with self.subTest(locale=locale, contract="precedence"):
                self.assertEqual(positions, sorted(positions))
            for literal in common_literals:
                with self.subTest(locale=locale, literal=literal):
                    self.assertIn(literal, section)
            for marker in contract["semantics"]:
                with self.subTest(locale=locale, semantics=marker):
                    self.assertIn(marker, section)
            self.assertIn(f"getting-started-simple.{locale}.md", section)

    def test_localized_generic_guides_document_embedded_mode_contract(self) -> None:
        expected = {
            "zh-TW": {
                "heading": "## 流程模式設定",
                "end": "## Full 模式的核准點",
                "precedence": (
                    "目前操作的明確指示",
                    "工作流內的預設模式宣告",
                    "Full fallback",
                ),
                "semantics": (
                    "宣告不存在或不是支援值",
                    "不會讀取任何 Codex Config",
                    "只影響目前操作",
                    "不會修改宣告",
                    "新的工作階段",
                    "只有對話能力",
                    "不能檢查 repository、修改檔案、執行命令或測試、保存狀態、宣稱已觀察驗證結果，或執行獨立 Review",
                ),
                "modules": "## 十一個進階模組",
            },
            "en": {
                "heading": "## Workflow mode configuration",
                "end": "## Full mode approval points",
                "precedence": (
                    "explicit instruction for the current operation",
                    "embedded default-mode declaration",
                    "Full fallback",
                ),
                "semantics": (
                    "missing or unsupported declaration",
                    "does not read either Codex Config file",
                    "only the current operation",
                    "does not modify the declaration",
                    "new session",
                    "conversation-only",
                    "cannot inspect a repository, edit files, run commands or tests, persist state, report observed validation, or perform an independent Review",
                ),
                "modules": "## Eleven advanced modules",
            },
            "ja": {
                "heading": "## ワークフローモードの設定",
                "end": "## Full モードの承認点",
                "precedence": (
                    "現在の操作に対する明示的な指示",
                    "ワークフロー内のデフォルトモード宣言",
                    "Full fallback",
                ),
                "semantics": (
                    "宣言がないか未対応の値",
                    "Codex Config を読み取りません",
                    "現在の操作だけ",
                    "宣言を変更しません",
                    "新しいセッション",
                    "会話だけ",
                    "repository の確認、ファイル編集、コマンドやテストの実行、状態の永続化、観測済み検証の報告、独立 Review はできません",
                ),
                "modules": "## 11 個の詳細モジュール",
            },
        }
        declarations = (
            "`Default workflow mode: full`",
            "`Default workflow mode: lite`",
        )
        for locale, document in GENERIC_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            contract = expected[locale]
            self.assertIn(contract["heading"], body)
            self.assertIn(contract["end"], body)
            start = body.index(contract["heading"])
            end = body.index(contract["end"], start)
            section = body[start:end]
            positions = [section.index(marker) for marker in contract["precedence"]]
            with self.subTest(locale=locale, contract="precedence"):
                self.assertEqual(positions, sorted(positions))
            for declaration in declarations:
                with self.subTest(locale=locale, declaration=declaration):
                    self.assertIn(declaration, section)
            for marker in contract["semantics"]:
                with self.subTest(locale=locale, semantics=marker):
                    self.assertIn(marker, body)
            self.assertIn(f"getting-started-simple.{locale}.md", section)
            self.assertIn(contract["modules"], body)
            self.assertLess(body.index("`orchestration.md`"), body.index("`lite-workflow.md`"))
            self.assertLess(body.index("`lite-workflow.md`"), body.index("`requirements.md`"))

    def test_localized_codex_guides_document_direct_skill_entry_contract(
        self,
    ) -> None:
        expected = {
            "zh-TW": {
                "section": ("## 九個 Skill 入口", "## 手動更新"),
                "markers": (
                    "只會選擇階段，不會選擇流程模式",
                    "`$ask-then-do-it` 仍是標準模式判定入口",
                    "模式尚未判定時，會交由 `$ask-then-do-it`",
                    "判定為 Lite 時，會轉入 Lite 流程",
                    "判定為 Full 時，只有在一般前置條件都滿足後，才能繼續所選階段",
                    "模式訊號衝突時會暫停並要求釐清",
                    "無效 Config 會回到 Full",
                    "直接入口不會保存模式狀態",
                ),
            },
            "en": {
                "section": ("## Nine Skill entry points", "## Manual update"),
                "markers": (
                    "selects a stage, not a workflow mode",
                    "`$ask-then-do-it` remains the canonical mode resolver",
                    "An unresolved mode delegates to `$ask-then-do-it`",
                    "Resolved Lite routes to the Lite lifecycle",
                    "Resolved Full may continue to the selected stage only after its normal prerequisites are satisfied",
                    "Conflicting mode signals pause for clarification",
                    "Invalid Config falls back to Full",
                    "Direct entry does not persist mode state",
                ),
            },
            "ja": {
                "section": ("## Skill 入口", "## 手動更新"),
                "markers": (
                    "段階を選択するだけで、ワークフローモードは選択しません",
                    "`$ask-then-do-it` が引き続き正規のモード判定を担います",
                    "モードが未決定なら `$ask-then-do-it` に委ねます",
                    "Lite と判定済みなら Lite ライフサイクルへ進みます",
                    "Full と判定済みなら通常の前提条件を満たした後にだけ、選択した段階へ進めます",
                    "モード指定が競合した場合は停止して確認を求めます",
                    "無効な Config は Full にフォールバックします",
                    "直接入口ではモード状態を永続化しません",
                ),
            },
        }

        for locale, document in CODEX_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            contract = expected[locale]
            section = document_section(body, *contract["section"])
            for marker in contract["markers"]:
                with self.subTest(locale=locale, marker=marker):
                    self.assertIn(marker, section)

    def test_localized_generic_guides_document_direct_module_entry_contract(
        self,
    ) -> None:
        expected = {
            "zh-TW": {
                "section": ("## 十一個進階模組", "## 授權與來源"),
                "markers": (
                    "Generic 不一定使用 Lite",
                    "貼上模組只會選擇階段，不會選擇流程模式",
                    "既有的模式優先順序與結果都不變",
                    "`bootstrap.md` 與 `orchestration.md` 擁有完整的模式判定器",
                    "其他九個可單獨貼上的模組",
                    "相同、範圍有限且最小化的直接入口保護規則",
                    "只因可能在沒有上述判定器時被貼上",
                    "不代表它們擁有完整的模式判定權",
                    "由組合後 orchestration 證實的模式會直接沿用",
                    "只有在直接貼上且模式尚未證實時，才依 `目前操作的明確指示 > 可取得的內嵌宣告 > Full fallback` 判定",
                    "指示衝突時暫停並要求釐清",
                    "無效宣告選擇 Full",
                    "結果不會保存",
                    "判定為 Lite 時會轉入 `lite-workflow.md`",
                    "判定為 Full 時直接進入 `lite-workflow.md` 會轉回 `orchestration.md`",
                ),
            },
            "en": {
                "section": ("## Eleven advanced modules", "## License and attribution"),
                "markers": (
                    "Generic is not always Lite",
                    "selects a stage, not a workflow mode",
                    "established mode precedence and outcomes do not change",
                    "`bootstrap.md` and `orchestration.md` own the complete mode resolver",
                    "The other nine standalone modules include the same bounded, minimal direct-entry guard",
                    "only because each can be pasted without that resolver",
                    "does not transfer complete resolver ownership",
                    "A mode already proven by composed orchestration is reused",
                    "Only an unproven direct paste applies `explicit operation instruction > available embedded declaration > Full fallback`",
                    "Conflicting instructions pause for clarification",
                    "An invalid declaration selects Full",
                    "the result is not persisted",
                    "Resolved Lite routes to `lite-workflow.md`",
                    "Direct entry to `lite-workflow.md` with resolved Full routes to `orchestration.md`",
                ),
            },
            "ja": {
                "section": ("## 11 個の詳細モジュール", "## ライセンスと出典"),
                "markers": (
                    "Generic が常に Lite になるわけではありません",
                    "モジュールの貼り付けで選択されるのは段階であり、ワークフローモードではありません",
                    "既存のモード優先順位と結果は変わりません",
                    "`bootstrap.md` と `orchestration.md` が完全なモード判定を担います",
                    "他の 9 個の単独で貼り付けられるモジュール",
                    "同じ限定的で最小限の直接入口ガード",
                    "判定器なしで貼り付けられる可能性があるためだけに",
                    "完全なモード判定の所有権を移すものではありません",
                    "構成済み orchestration によって証明済みのモードは再利用します",
                    "モードが未証明の直接貼り付けに限り、`現在の操作に対する明示的な指示 > 利用可能な埋め込み宣言 > Full fallback` を適用します",
                    "指示が競合すると停止して確認を求めます",
                    "無効な宣言では Full を選択します",
                    "結果を永続化しません",
                    "Lite と判定済みなら `lite-workflow.md` へ進みます",
                    "Full と判定済みの状態で `lite-workflow.md` に直接入ると `orchestration.md` へ戻ります",
                ),
            },
        }

        for locale, document in GENERIC_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            contract = expected[locale]
            section = document_section(body, *contract["section"])
            for marker in contract["markers"]:
                with self.subTest(locale=locale, marker=marker):
                    self.assertIn(marker, section)

    def test_mode_enabled_host_guides_scope_question_and_approval_contracts(
        self,
    ) -> None:
        contracts = {
            "en": {
                "codex": (
                    "## First use",
                    "### Full mode",
                    "### Lite mode",
                    "## Nine Skill entry points",
                ),
                "generic": (
                    "## Full mode approval points",
                    "## Lite mode questions and approval",
                    "## Capability limits",
                ),
                "full": (
                    "exactly one requirement question at a time",
                    "three approval gates",
                ),
                "full_gates": (
                    "Requirements consensus",
                    "Specification",
                    "Ticket plan",
                ),
                "lite": (
                    "may ask no questions",
                    "at most three blocking questions",
                    "one Change Brief",
                    "one approval",
                ),
                "unscoped": (
                    "asks the first requirements question",
                    "asks the single most important question",
                ),
            },
            "zh-TW": {
                "codex": (
                    "## 第一次使用",
                    "### Full 模式",
                    "### Lite 模式",
                    "## 九個 Skill 入口",
                ),
                "generic": (
                    "## Full 模式的核准點",
                    "## Lite 模式的問題與核准",
                    "## 能力限制",
                ),
                "full": (
                    "一次只問一個需求問題",
                    "三個核准點",
                ),
                "full_gates": ("需求共識", "規格", "Ticket 規劃"),
                "lite": (
                    "可以不提出問題",
                    "每輪最多三個阻塞問題",
                    "一份 Change Brief",
                    "一次核准",
                ),
                "unscoped": (
                    "提出第一個需求問題",
                    "提出一個最重要的問題",
                ),
            },
            "ja": {
                "codex": (
                    "## 初回使用",
                    "### Full モード",
                    "### Lite モード",
                    "## Skill 入口",
                ),
                "generic": (
                    "## Full モードの承認点",
                    "## Lite モードの質問と承認",
                    "## できることの範囲",
                ),
                "full": (
                    "一度に一つの要件質問",
                    "3 つの承認点",
                ),
                "full_gates": ("要件の合意", "仕様", "Ticket 計画"),
                "lite": (
                    "質問が不要な場合があります",
                    "各回最大 3 つの阻害要因に関する質問",
                    "1 つの Change Brief",
                    "1 回の承認",
                ),
                "unscoped": (
                    "最初の要件質問が行われます",
                    "最も重要な質問を一つずつ行います",
                ),
            },
        }

        for locale, contract in contracts.items():
            codex_body = CODEX_GUIDES_BY_LOCALE[locale].read_text(encoding="utf-8")
            first_use, full_heading, lite_heading, codex_end = contract["codex"]
            first_use_section = document_section(codex_body, first_use, codex_end)
            for heading in (full_heading, lite_heading):
                with self.subTest(locale=locale, document="codex", heading=heading):
                    self.assertIn(heading, first_use_section)
            if full_heading in first_use_section and lite_heading in first_use_section:
                full_section = document_section(
                    first_use_section, full_heading, lite_heading
                )
                lite_section = document_section(first_use_section, lite_heading, None)
                for marker in contract["full"]:
                    with self.subTest(locale=locale, document="codex", full=marker):
                        self.assertIn(marker, full_section)
                for marker in contract["full_gates"]:
                    with self.subTest(
                        locale=locale, document="codex", full_gate=marker
                    ):
                        self.assertIn(marker, full_section)
                for marker in contract["lite"]:
                    with self.subTest(locale=locale, document="codex", lite=marker):
                        self.assertIn(marker, lite_section)
                prefix = first_use_section[: first_use_section.index(full_heading)]
                for stale in contract["unscoped"]:
                    with self.subTest(locale=locale, document="codex", stale=stale):
                        self.assertNotIn(stale, prefix)

            generic_body = GENERIC_GUIDES_BY_LOCALE[locale].read_text(
                encoding="utf-8"
            )
            generic_full, generic_lite, generic_end = contract["generic"]
            for heading in (generic_full, generic_lite):
                with self.subTest(locale=locale, document="generic", heading=heading):
                    self.assertIn(heading, generic_body)
            for stale in contract["unscoped"]:
                with self.subTest(locale=locale, document="generic", stale=stale):
                    self.assertNotIn(stale, generic_body[: generic_body.index(generic_full)])
            if generic_lite in generic_body:
                full_section = document_section(
                    generic_body, generic_full, generic_lite
                )
                lite_section = document_section(generic_body, generic_lite, generic_end)
                for marker in contract["full"]:
                    with self.subTest(locale=locale, document="generic", full=marker):
                        self.assertIn(marker, full_section)
                for marker in contract["lite"]:
                    with self.subTest(locale=locale, document="generic", lite=marker):
                        self.assertIn(marker, lite_section)

    def test_localized_generic_guides_distinguish_full_and_lite_session_continuation(
        self,
    ) -> None:
        contracts = {
            "en": {
                "section": ("## Save your progress", "## Eleven advanced modules"),
                "full": (
                    "### Full",
                    "durable workflow documents",
                    "first unfinished Full stage",
                ),
                "lite": (
                    "### Lite",
                    "resolves the workflow mode again",
                    "Change Brief, approval, progress, or Review",
                    "cannot resume",
                    "reconstructs a new Change Brief",
                    "repository state",
                    "user input",
                ),
                "stale": (
                    "Save the important documents created at each stage",
                    "proceeds to the first unfinished stage",
                ),
                "quick_start_stale": (
                    "To continue earlier work, also paste the important documents you saved.",
                ),
            },
            "zh-TW": {
                "section": ("## 保存進度", "## 十一個進階模組"),
                "full": (
                    "### Full",
                    "可保存的流程文件",
                    "第一個尚未完成的 Full 階段",
                ),
                "lite": (
                    "### Lite",
                    "重新判定流程模式",
                    "Change Brief、核准、進度或 Review",
                    "無法延續",
                    "重新建立一份 Change Brief",
                    "repository 現況",
                    "使用者輸入",
                ),
                "stale": (
                    "每完成一個階段，請保存 AI 產生的重要文件",
                    "前往第一個尚未完成的階段",
                ),
                "quick_start_stale": (
                    "如果要延續之前的工作，再一起貼上先前保存的重要文件。",
                ),
            },
            "ja": {
                "section": ("## 進捗を保存する", "## 11 個の詳細モジュール"),
                "full": (
                    "### Full",
                    "永続化できるワークフロー文書",
                    "最初の未完了の Full 段階",
                ),
                "lite": (
                    "### Lite",
                    "ワークフローモードを再決定",
                    "Change Brief、承認、進捗、Review",
                    "再開できません",
                    "新しい Change Brief を再構築",
                    "repository の状態",
                    "ユーザー入力",
                ),
                "stale": (
                    "各段階で作成された重要な文書を保存してください",
                    "最初の未完了段階へ進みます",
                ),
                "quick_start_stale": (
                    "以前の作業を続ける場合は、保存した重要な文書も貼り付けます。",
                ),
            },
        }

        for locale, document in GENERIC_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            contract = contracts[locale]
            section = document_section(body, *contract["section"])
            for mode in ("full", "lite"):
                for marker in contract[mode]:
                    with self.subTest(locale=locale, mode=mode, marker=marker):
                        self.assertIn(marker, section)
            for stale in contract["stale"]:
                with self.subTest(locale=locale, stale=stale):
                    self.assertNotIn(stale, section)
            for stale in contract["quick_start_stale"]:
                with self.subTest(locale=locale, quick_start_stale=stale):
                    self.assertNotIn(stale, body)

    def test_generic_start_pages_keep_full_only_startup_claims_mode_scoped(
        self,
    ) -> None:
        contracts = {
            "en": {
                "heading": "## Choose Full or Lite",
                "full": (
                    "Full uses exactly one requirement question at a time",
                    "three approval gates",
                ),
                "lite": (
                    "Lite may ask no questions",
                    "at most three blocking questions",
                    "one Change Brief",
                    "one approval",
                ),
                "stale": "asks the first requirements question",
            },
            "zh-TW": {
                "heading": "## 選擇 Full 或 Lite",
                "full": ("Full 一次只問一個需求問題", "三個核准點"),
                "lite": (
                    "Lite 可以不提出問題",
                    "每輪最多三個阻塞問題",
                    "一份 Change Brief",
                    "一次核准",
                ),
                "stale": "提出第一個需求問題",
            },
            "ja": {
                "heading": "## Full または Lite を選ぶ",
                "full": ("Full は一度に一つの要件質問", "3 つの承認点"),
                "lite": (
                    "Lite は質問が不要な場合があります",
                    "各回最大 3 つの阻害要因に関する質問",
                    "1 つの Change Brief",
                    "1 回の承認",
                ),
                "stale": "最初の要件質問を行います",
            },
        }
        for locale, document in GENERIC_START_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            contract = contracts[locale]
            heading = contract["heading"]
            self.assertIn(heading, body)
            setup, mode_summary = body.split(heading, 1)
            with self.subTest(locale=locale, contract="unscoped stale claim"):
                self.assertNotIn(contract["stale"], setup)
            for mode in ("full", "lite"):
                for marker in contract[mode]:
                    with self.subTest(locale=locale, mode=mode, marker=marker):
                        self.assertIn(marker, mode_summary)

    def test_mode_configuration_stays_in_host_guides(self) -> None:
        non_host_documents = (
            README,
            *ROOT_START_BY_LOCALE.values(),
            *CODEX_START_BY_LOCALE.values(),
            *GENERIC_START_BY_LOCALE.values(),
        )
        for document in non_host_documents:
            body = document.read_text(encoding="utf-8")
            with self.subTest(document=document.relative_to(ROOT)):
                self.assertNotIn("~/.codex/ask-then-do-it.toml", body)
                self.assertNotIn("<project>/.codex/ask-then-do-it.toml", body)
                self.assertNotIn("Default workflow mode:", body)
        for document in GENERIC_GUIDES_BY_LOCALE.values():
            body = document.read_text(encoding="utf-8")
            self.assertNotIn("~/.codex/ask-then-do-it.toml", body)
            self.assertNotIn("<project>/.codex/ask-then-do-it.toml", body)
        for document in CODEX_GUIDES_BY_LOCALE.values():
            self.assertNotIn(
                "Default workflow mode:", document.read_text(encoding="utf-8")
            )

    def test_localized_simple_guides_define_complete_full_and_lite_flows(self) -> None:
        expected = {
            "zh-TW": {
                "precedence": "## 模式優先順序",
                "comparison": "## Full 與 Lite 比較",
                "table": "| 比較項目 | Full | Lite |",
                "full": "## Full 模式",
                "lite": "## Lite 模式",
                "risk": "## 高風險操作",
                "full_markers": (
                    "一次只問一個需求問題",
                    "三個正式核准點",
                ),
                "lite_markers": (
                    "每輪最多三個阻塞問題",
                    "約 `500 tokens`",
                    "Change Brief 約 `800 tokens`",
                    "恰好一個正式核准點",
                    "不建立或更新流程文件",
                    "不新增或修改測試",
                    "靜態檢查",
                    "主要成功路徑",
                    "最重要的失敗或邊界路徑",
                    "同一批列出",
                    "核准後才能修正",
                    "完成回報通常約 `500 tokens`",
                ),
                "global_markers": (
                    "目前操作的明確指示",
                    "專案 Config",
                    "使用者 Config",
                    "Full 作為 fallback",
                    "只針對目前操作切換至 Full",
                    "其他工作階段仍以 Config 為準",
                    "新的工作階段會重新判定模式",
                ),
                "risk_markers": (
                    "認證與授權",
                    "破壞性資料操作",
                ),
            },
            "en": {
                "precedence": "## Mode precedence",
                "comparison": "## Full and Lite compared",
                "table": "| Comparison | Full | Lite |",
                "full": "## Full mode",
                "lite": "## Lite mode",
                "risk": "## High-risk operations",
                "full_markers": (
                    "one requirements question at a time",
                    "three formal approval gates",
                ),
                "lite_markers": (
                    "up to three blocking questions per round",
                    "about `500 tokens`",
                    "Change Brief targets about `800 tokens`",
                    "exactly one formal approval gate",
                    "does not create or update workflow artifact files",
                    "does not add or modify tests",
                    "static checks",
                    "principal success path",
                    "most important failure or boundary path",
                    "one batch",
                    "approval before making corrections",
                    "completion response normally targets about `500 tokens`",
                ),
                "global_markers": (
                    "explicit instruction for the current operation",
                    "project Config",
                    "user Config",
                    "Full fallback",
                    "switch only the current operation to Full",
                    "other sessions continue to use Config",
                    "A new session resolves the mode again",
                ),
                "risk_markers": (
                    "Authentication and authorization",
                    "destructive data operations",
                ),
            },
            "ja": {
                "precedence": "## モードの優先順位",
                "comparison": "## Full と Lite の比較",
                "table": "| 比較項目 | Full | Lite |",
                "full": "## Full モード",
                "lite": "## Lite モード",
                "risk": "## 高リスクの操作",
                "full_markers": (
                    "要件の質問を一度に一つだけ行い",
                    "3 つの正式な承認点",
                ),
                "lite_markers": (
                    "1 回につき最大 3 個の阻害質問",
                    "約 `500 tokens`",
                    "Change Brief は約 `800 tokens`",
                    "正式な承認点はちょうど 1 つ",
                    "ワークフロー成果物ファイルを作成も更新もしません",
                    "テストを追加も変更もしません",
                    "静的チェック",
                    "主要な成功経路",
                    "最も重要な失敗または境界経路",
                    "一つのまとまりで提示",
                    "修正前に承認",
                    "完了報告は通常約 `500 tokens`",
                ),
                "global_markers": (
                    "現在の操作に対する明示的な指示",
                    "プロジェクト Config",
                    "ユーザー Config",
                    "Full fallback",
                    "現在の操作だけを Full に切り替える",
                    "他のセッションでは引き続き Config が基準",
                    "新しいセッションではモードを再判定",
                ),
                "risk_markers": (
                    "認証と認可",
                    "破壊的なデータ操作",
                ),
            },
        }
        for locale, document in SIMPLE_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            markers = expected[locale]
            positions = [
                body.index(markers[heading])
                for heading in ("precedence", "comparison", "full", "lite", "risk")
            ]
            with self.subTest(locale=locale, contract="section order"):
                self.assertEqual(positions, sorted(positions))
            self.assertIn(markers["table"], body)

            full_section = body[positions[2] : positions[3]]
            lite_section = body[positions[3] : positions[4]]
            risk_section = body[positions[4] :]
            self.assertRegex(full_section, r"(?m)^1\. ")
            self.assertRegex(lite_section, r"(?m)^1\. ")
            for marker in markers["full_markers"]:
                with self.subTest(locale=locale, full=marker):
                    self.assertIn(marker, full_section)
            for marker in markers["lite_markers"]:
                with self.subTest(locale=locale, lite=marker):
                    self.assertIn(marker, lite_section)
            for marker in markers["global_markers"]:
                with self.subTest(locale=locale, global_marker=marker):
                    self.assertIn(marker, body)
            for marker in markers["risk_markers"]:
                with self.subTest(locale=locale, risk_marker=marker):
                    self.assertIn(marker, risk_section)

    def test_localized_simple_guides_include_separate_full_and_lite_mermaid_flows(
        self,
    ) -> None:
        headings = {
            "zh-TW": ("## Full 模式", "## Lite 模式", "## 高風險操作"),
            "en": ("## Full mode", "## Lite mode", "## High-risk operations"),
            "ja": ("## Full モード", "## Lite モード", "## 高リスクの操作"),
        }
        expected_edges = {
            "full": (
                ("F_STATE", "F_REQUIREMENTS"),
                ("F_REQUIREMENTS", "F_REQUIREMENTS_GATE"),
                ("F_REQUIREMENTS_GATE", "F_REQUIREMENTS"),
                ("F_REQUIREMENTS_GATE", "F_KNOWLEDGE"),
                ("F_KNOWLEDGE", "F_SPECIFICATION"),
                ("F_SPECIFICATION", "F_SPECIFICATION_GATE"),
                ("F_SPECIFICATION_GATE", "F_SPECIFICATION"),
                ("F_SPECIFICATION_GATE", "F_TICKETS"),
                ("F_TICKETS", "F_TICKET_PLAN_GATE"),
                ("F_TICKET_PLAN_GATE", "F_TICKETS"),
                ("F_TICKET_PLAN_GATE", "F_TEST_CHOICE"),
                ("F_TEST_CHOICE", "F_TDD"),
                ("F_TEST_CHOICE", "F_DIRECT"),
                ("F_TDD", "F_EVIDENCE"),
                ("F_DIRECT", "F_EVIDENCE"),
                ("F_EVIDENCE", "F_REVIEW"),
                ("F_REVIEW", "F_COMPLETE"),
                ("F_REVIEW", "F_TEST_CHOICE"),
                ("F_REVIEW", "F_ARCHITECTURE"),
                ("F_ARCHITECTURE", "F_SPECIFICATION"),
            ),
            "lite": (
                ("L_STATE", "L_BLOCKERS"),
                ("L_BLOCKERS", "L_CHANGE_BRIEF"),
                ("L_CHANGE_BRIEF", "L_CHANGE_BRIEF_GATE"),
                ("L_CHANGE_BRIEF_GATE", "L_CHANGE_BRIEF"),
                ("L_CHANGE_BRIEF_GATE", "L_IMPLEMENT"),
                ("L_IMPLEMENT", "L_CHANGE_BRIEF"),
                ("L_IMPLEMENT", "L_VALIDATE"),
                ("L_VALIDATE", "L_VALIDATION_STATUS"),
                ("L_VALIDATION_STATUS", "L_REVIEW"),
                ("L_VALIDATION_STATUS", "L_FIX_VALIDATION"),
                ("L_FIX_VALIDATION", "L_VALIDATE"),
                ("L_VALIDATION_STATUS", "L_COMPLETE"),
                ("L_REVIEW", "L_FINDINGS"),
                ("L_FINDINGS", "L_COMPLETE"),
                ("L_FINDINGS", "L_CORRECTION_GATE"),
                ("L_CORRECTION_GATE", "L_UNRESOLVED"),
                ("L_UNRESOLVED", "L_COMPLETE"),
                ("L_CORRECTION_GATE", "L_FIX_REVIEW"),
                ("L_FIX_REVIEW", "L_VALIDATE"),
            ),
        }
        mermaid_block = re.compile(r"```mermaid\r?\n(.*?)\r?\n```", re.DOTALL)
        mermaid_edge = re.compile(
            r"(?m)^\s*([FL]_[A-Z_]+)\s*-->\s*(?:\|[^|\r\n]+\|\s*)?"
            r"([FL]_[A-Z_]+)\s*$"
        )
        mermaid_node = re.compile(r"(?m)^\s*([FL]_[A-Z_]+)(?:\[|\{)")

        for locale, document in SIMPLE_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            full_heading, lite_heading, risk_heading = headings[locale]
            full_section = body[body.index(full_heading) : body.index(lite_heading)]
            lite_section = body[body.index(lite_heading) : body.index(risk_heading)]
            full_blocks = mermaid_block.findall(full_section)
            lite_blocks = mermaid_block.findall(lite_section)

            with self.subTest(locale=locale, contract="diagram count and scope"):
                self.assertEqual(body.count("```mermaid"), 2)
                self.assertEqual(len(full_blocks), 1)
                self.assertEqual(len(lite_blocks), 1)

            if len(full_blocks) != 1 or len(lite_blocks) != 1:
                continue

            for mode, block in (("full", full_blocks[0]), ("lite", lite_blocks[0])):
                with self.subTest(locale=locale, mode=mode, contract="direction"):
                    self.assertEqual(block.splitlines()[0], "flowchart TD")
                expected_nodes = {
                    node for edge in expected_edges[mode] for node in edge
                }
                with self.subTest(locale=locale, mode=mode, contract="topology"):
                    self.assertCountEqual(
                        mermaid_edge.findall(block), expected_edges[mode]
                    )
                    self.assertEqual(set(mermaid_node.findall(block)), expected_nodes)

    def test_localized_simple_guides_skip_empty_correction_gate_when_review_is_clean(
        self,
    ) -> None:
        expected = {
            "zh-TW": (
                "## Lite 模式",
                "## 高風險操作",
                "沒有可處理的 findings 時，AI 必須明確回報為零，不得建立空的修正核准點",
            ),
            "en": (
                "## Lite mode",
                "## High-risk operations",
                "When there are zero actionable findings, the AI says so and does not create an empty correction approval gate",
            ),
            "ja": (
                "## Lite モード",
                "## 高リスクの操作",
                "対応可能な findings が 0 件の場合、AI はそのことを明示し、空の修正承認点を作りません",
            ),
        }
        for locale, document in SIMPLE_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            lite_heading, risk_heading, marker = expected[locale]
            lite_section = body[body.index(lite_heading) : body.index(risk_heading)]
            with self.subTest(locale=locale):
                self.assertIn(marker, lite_section)

    def test_localized_simple_guides_keep_section_scoped_workflow_contracts(
        self,
    ) -> None:
        expected = {
            "zh-TW": {
                "precedence_headings": ("## 模式優先順序", "## Full 與 Lite 比較"),
                "precedence_steps": (
                    "目前操作的明確指示",
                    "專案 Config",
                    "使用者 Config",
                    "Full 作為 fallback",
                ),
                "full_headings": ("## Full 模式", "## Lite 模式"),
                "full_steps": (
                    "理解現況",
                    "取得需求共識",
                    "寫規格",
                    "拆成垂直 Tickets",
                    "依測試選擇實作",
                    "留下實作證據",
                    "Review",
                    "完成",
                ),
                "lite_headings": ("## Lite 模式", "## 高風險操作"),
                "lite_steps": (
                    "理解現況與風險",
                    "只問阻塞問題",
                    "顯示 Change Brief",
                    "取得一次核准",
                    "直接實作核准範圍",
                    "執行最低驗證",
                    "進行精簡 Review",
                    "完成回報",
                ),
                "risk_headings": ("## 高風險操作", "## 在 Codex 開始"),
                "risk_categories": (
                    "認證",
                    "授權",
                    "付款",
                    "資料搬移",
                    "破壞性資料操作",
                    "公開契約",
                    "跨模組",
                    "並行",
                    "非同步",
                    "外部副作用",
                ),
                "completion_target": "約 `500 tokens`",
                "completion_exceptions": (
                    "失敗",
                    "阻塞",
                    "安全問題",
                    "缺少或無法取得的證據",
                    "未解決 findings",
                ),
            },
            "en": {
                "precedence_headings": ("## Mode precedence", "## Full and Lite compared"),
                "precedence_steps": (
                    "explicit instruction for the current operation",
                    "Project Config",
                    "User Config",
                    "Full fallback",
                ),
                "full_headings": ("## Full mode", "## Lite mode"),
                "full_steps": (
                    "Understand the current state",
                    "Reach requirements consensus",
                    "Write the specification",
                    "Split the work into vertical Tickets",
                    "Implement according to the test choice",
                    "Keep implementation evidence",
                    "Review",
                    "Complete",
                ),
                "lite_headings": ("## Lite mode", "## High-risk operations"),
                "lite_steps": (
                    "Understand current state and risk",
                    "Ask only blockers",
                    "Present the Change Brief",
                    "Obtain one approval",
                    "Implement the approved scope directly",
                    "Run minimum validation",
                    "Perform compact Review",
                    "Report completion",
                ),
                "risk_headings": ("## High-risk operations", "## Start in Codex"),
                "risk_categories": (
                    "Authentication",
                    "authorization",
                    "payment",
                    "data migration",
                    "destructive data operations",
                    "public contracts",
                    "cross-module",
                    "concurrency",
                    "asynchronous",
                    "external side effects",
                ),
                "completion_target": "about `500 tokens`",
                "completion_exceptions": (
                    "Failures",
                    "blockers",
                    "security concerns",
                    "missing or unavailable evidence",
                    "unresolved findings",
                ),
            },
            "ja": {
                "precedence_headings": ("## モードの優先順位", "## Full と Lite の比較"),
                "precedence_steps": (
                    "現在の操作に対する明示的な指示",
                    "プロジェクト Config",
                    "ユーザー Config",
                    "Full fallback",
                ),
                "full_headings": ("## Full モード", "## Lite モード"),
                "full_steps": (
                    "現状を理解する",
                    "要件の合意を得る",
                    "仕様を書く",
                    "縦割りの Tickets に分ける",
                    "テスト選択に従って実装する",
                    "実装根拠を残す",
                    "Review する",
                    "完了する",
                ),
                "lite_headings": ("## Lite モード", "## 高リスクの操作"),
                "lite_steps": (
                    "現状とリスクを理解する",
                    "阻害要因だけを質問する",
                    "Change Brief を提示する",
                    "一度だけ承認を得る",
                    "承認済み範囲を直接実装する",
                    "最低限の検証を行う",
                    "簡潔な Review を行う",
                    "完了を報告する",
                ),
                "risk_headings": ("## 高リスクの操作", "## Codex で始める"),
                "risk_categories": (
                    "認証",
                    "認可",
                    "支払い",
                    "データ移行",
                    "破壊的なデータ操作",
                    "公開契約",
                    "複数モジュール",
                    "並行",
                    "非同期",
                    "外部への副作用",
                ),
                "completion_target": "約 `500 tokens`",
                "completion_exceptions": (
                    "失敗",
                    "阻害要因",
                    "セキュリティ上の懸念",
                    "不足または利用できない根拠",
                    "未解決 findings",
                ),
            },
        }

        def section_between(body: str, headings: tuple[str, str]) -> str:
            start, end = headings
            return body[body.index(start) : body.index(end)]

        def numbered_flow(section: str) -> list[tuple[int, str, str]]:
            matches = list(re.finditer(r"(?m)^(\d+)\. \*\*(.+?)\*\*", section))
            return [
                (
                    int(match.group(1)),
                    match.group(2),
                    section[
                        match.start() : matches[index + 1].start()
                        if index + 1 < len(matches)
                        else len(section)
                    ],
                )
                for index, match in enumerate(matches)
            ]

        for locale, document in SIMPLE_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            contract = expected[locale]
            for headings in (
                contract["precedence_headings"],
                contract["full_headings"],
                contract["lite_headings"],
                contract["risk_headings"],
            ):
                for heading in headings:
                    with self.subTest(locale=locale, heading=heading):
                        self.assertIn(heading, body)

            precedence = section_between(body, contract["precedence_headings"])
            precedence_steps = re.findall(r"(?m)^(\d+)\. (.+)$", precedence)
            with self.subTest(locale=locale, contract="precedence levels"):
                self.assertEqual(
                    [int(number) for number, _ in precedence_steps],
                    [1, 2, 3, 4],
                )
            for (_, step), marker in zip(
                precedence_steps, contract["precedence_steps"], strict=True
            ):
                with self.subTest(locale=locale, precedence=marker):
                    self.assertIn(marker, step)

            full_steps = numbered_flow(section_between(body, contract["full_headings"]))
            lite_steps = numbered_flow(section_between(body, contract["lite_headings"]))
            for name, steps, markers in (
                ("Full", full_steps, contract["full_steps"]),
                ("Lite", lite_steps, contract["lite_steps"]),
            ):
                with self.subTest(locale=locale, flow=name):
                    self.assertEqual([number for number, _, _ in steps], list(range(1, 9)))
                for (_, title, _), marker in zip(steps, markers, strict=True):
                    with self.subTest(locale=locale, flow=name, step=marker):
                        self.assertIn(marker, title)

            risk = section_between(body, contract["risk_headings"])
            for category in contract["risk_categories"]:
                with self.subTest(locale=locale, risk=category):
                    self.assertIn(category, risk)

            completion = lite_steps[-1][2]
            with self.subTest(locale=locale, contract="completion target"):
                self.assertIn(contract["completion_target"], completion)
            for exception in contract["completion_exceptions"]:
                with self.subTest(locale=locale, completion_exception=exception):
                    self.assertIn(exception, completion)

    def test_localized_design_guides_define_ownership_and_token_proxy(self) -> None:
        expected = {
            "zh-TW": (
                "Core 擁有供應者中立的 Full/Lite 契約",
                "Codex adapter",
                "Generic adapter",
                "等價的可觀察結果",
                "Lite 的可追溯性低於 Full",
                "等價的代表情境",
                "受工作流控制的材料",
                "問題、Change Brief 或 Full 文件、階段指示、組合後的 prompt 內容、重複交接與完成回報",
                "任務特定的原始碼、必要的工具輸出與隱藏的模型推理",
                "至少降低 60%",
                "不保證 API 帳單",
            ),
            "en": (
                "Core owns the provider-neutral Full/Lite contract",
                "Codex adapter",
                "Generic adapter",
                "equivalent observable outcomes",
                "Lite has lower traceability than Full",
                "equivalent representative scenario",
                "workflow-controlled material",
                "questions, the Change Brief or Full documents, stage instructions, composed prompt content, repeated handoffs, and completion reporting",
                "task-specific source code, necessary tool output, and hidden model reasoning",
                "at least 60%",
                "does not guarantee an API bill",
            ),
            "ja": (
                "Core はプロバイダー中立の Full/Lite 契約を所有します",
                "Codex adapter",
                "Generic adapter",
                "同等の観測可能な結果",
                "Lite の追跡可能性は Full より低くなります",
                "同等の代表シナリオ",
                "ワークフローが制御する材料",
                "質問、Change Brief または Full の文書、段階の指示、構成済み prompt の内容、繰り返される引き継ぎ、完了報告",
                "タスク固有のソースコード、必要なツール出力、非公開のモデル推論",
                "60% 以上削減",
                "API 請求額を保証するものではありません",
            ),
        }
        for locale, document in DESIGN_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            for marker in expected[locale]:
                with self.subTest(locale=locale, marker=marker):
                    self.assertIn(marker, body)

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
            "[使用說明](/START-HERE.zh-TW.md)",
            "[User Guide](/START-HERE.en.md)",
            "[利用ガイド](/START-HERE.ja.md)",
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

        for locale, document in CODEX_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
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
                with self.subTest(locale=locale, skill=skill):
                    self.assertIn(skill, body)
            for required in ("`tdd`", "`direct`", "`tests: skipped-by-user`"):
                self.assertIn(required, body)

        for locale, document in GENERIC_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            self.assertIn("generic-workflow.md", body)
            self.assertIn("direct-implementation.md", body)
            self.assertIn("1.3.0", body)
            self.assertIn("`tdd`", body)
            self.assertIn("`direct`", body)

        for locale, document in CODEX_START_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            self.assertIn("$ask-then-do-it", body)
            self.assertIn(f"{VERSIONED_GUIDE_ROOT}/codex.{locale}.md", body)

        for locale, document in GENERIC_START_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            self.assertIn("generic-workflow.md", body)
            self.assertIn("1.3.0", body)
            self.assertIn(f"{VERSIONED_GUIDE_ROOT}/generic.{locale}.md", body)

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
                resolved = (
                    ROOT / path_text.lstrip("/")
                    if path_text.startswith("/")
                    else document.parent / path_text
                ).resolve()
                with self.subTest(document=document.relative_to(ROOT), target=target):
                    self.assertTrue(resolved.exists(), resolved)


if __name__ == "__main__":
    unittest.main()
