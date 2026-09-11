import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
START_HERE = ROOT / "START-HERE.zh-TW.md"
CODEX_GUIDE = ROOT / "docs" / "guides" / "codex.zh-TW.md"
GENERIC_GUIDE = ROOT / "docs" / "guides" / "generic.zh-TW.md"
CLAUDE_GUIDE = ROOT / "docs/guides/claude-code.zh-TW.md"
CLAUDE_START_GUIDE = ROOT / "adapters/claude-code/plugin/ask-then-do-it/START-HERE.zh-TW.md"
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
    CLAUDE_GUIDE,
    CLAUDE_START_GUIDE,
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

CLAUDE_GUIDES_BY_LOCALE = {
    locale: localized_sibling(CLAUDE_GUIDE, locale) for locale in ("en", "zh-TW", "ja")
}
CLAUDE_START_BY_LOCALE = {
    locale: localized_sibling(CLAUDE_START_GUIDE, locale) for locale in ("en", "zh-TW", "ja")
}
HOST_GUIDES = {
    "codex": CODEX_GUIDES_BY_LOCALE,
    "claude-code": CLAUDE_GUIDES_BY_LOCALE,
    "generic": GENERIC_GUIDES_BY_LOCALE,
}
HEADINGS = {
    "en": ("Installation and preparation", "Getting started", "Full / Lite modes", "Available commands", "Updating and removal", "Common questions", "License and attribution"),
    "zh-TW": ("安裝與準備", "開始使用", "Full／Lite 模式", "可用指令", "更新與移除", "常見問題", "授權與來源"),
    "ja": ("インストールと準備", "使い始める", "Full／Lite モード", "利用できるコマンド", "更新と削除", "よくある質問", "ライセンスと出典"),
}

VERSIONED_GUIDE_ROOT = (
    "https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0/docs/guides"
)
VERSIONED_README = (
    "https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0/README.md"
)


def user_document_footer(document: Path) -> str:
    package_starts = (*CODEX_START_BY_LOCALE.values(), *GENERIC_START_BY_LOCALE.values(), *CLAUDE_START_BY_LOCALE.values())
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


    def test_mode_configuration_stays_in_host_guides(self) -> None:
        non_host_documents = (
            README,
            *ROOT_START_BY_LOCALE.values(),
            *CODEX_START_BY_LOCALE.values(),
            *GENERIC_START_BY_LOCALE.values(),
            *CLAUDE_START_BY_LOCALE.values(),
        )
        for document in non_host_documents:
            body = document.read_text(encoding="utf-8")
            with self.subTest(document=document.relative_to(ROOT)):
                self.assertNotIn("~/.codex/ask-then-do-it.toml", body)
                self.assertNotIn("<project>/.codex/ask-then-do-it.toml", body)
                self.assertNotIn("Default workflow mode:", body)
                self.assertNotIn(".claude/ask-then-do-it.toml", body)
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
            # Claude's ZIP checksum check is user-facing integrity guidance.
            for phrase in forbidden:
                if document == CLAUDE_GUIDE and phrase in ("checksums.sha256", "SHA-256", "checksum"):
                    continue
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


    def test_all_twelve_start_pages_are_concise_versioned_handoffs(self) -> None:
        groups = {
            "root": ROOT_START_BY_LOCALE,
            "codex": CODEX_START_BY_LOCALE,
            "claude-code": CLAUDE_START_BY_LOCALE,
            "generic": GENERIC_START_BY_LOCALE,
        }
        self.assertEqual(sum(map(len, groups.values())), 12)
        for group, documents in groups.items():
            for locale, document in documents.items():
                with self.subTest(group=group, locale=locale):
                    body = document.read_text(encoding="utf-8")
                    self.assertIn("1.4.0", body.splitlines()[0])
                    self.assertLess(len(body.splitlines()), 65)
                    self.assertIn("Full", body)
                    self.assertIn("Lite", body)
                    self.assertNotIn("mode =", body)
                    self.assertNotIn("Default workflow mode:", body)
                    if group == "root":
                        links = [f"docs/guides/{name}.{locale}.md" for name in ("getting-started-simple", "codex", "claude-code", "generic")]
                        links.append(f"docs/design/ai-development-skills.{locale}.md")
                        positions = [body.index(link) for link in links]
                        self.assertEqual(positions, sorted(positions))
                    else:
                        self.assertIn(f"{VERSIONED_GUIDE_ROOT}/{group}.{locale}.md", body)
                        self.assertIn(f"{VERSIONED_GUIDE_ROOT}/getting-started-simple.{locale}.md", body)
                        self.assertRegex(body, r"(?s)```text\n\S.+?\n```")
                    if group == "codex":
                        self.assertIn(f"codex.{locale}.md#zip", body)
                        self.assertIn("$ask-then-do-it", body)
                        self.assertIn("Marketplace", body)
                    elif group == "claude-code":
                        self.assertIn("/ask-then-do-it:ask-then-do-it", body)
                        self.assertIn("claude --plugin-dir", body)
                        self.assertIn("session-only", body)
                    elif group == "generic":
                        self.assertIn("generic-workflow.md", body)

    def test_nine_main_guides_have_seven_ordered_chapters_and_start_examples(self) -> None:
        for host, documents in HOST_GUIDES.items():
            for locale, document in documents.items():
                with self.subTest(host=host, locale=locale):
                    body = document.read_text(encoding="utf-8")
                    self.assertEqual(re.findall(r"^## (.+)$", body, re.M), list(HEADINGS[locale]))
                    sections = re.split(r"^## .+$", body, flags=re.M)[1:]
                    installation, start, modes, commands, update, faq, license_text = sections
                    self.assertNotRegex(installation, r"(?m)^(?:codex plugin |/plugin |claude plugin ).*(?:upgrade|update|uninstall|remove)")
                    self.assertRegex(start, r"(?s)```text\n\S.+?\n```")
                    self.assertIn("Full", modes)
                    self.assertIn("Lite", modes)
                    self.assertIn(f"getting-started-simple.{locale}.md", modes)
                    for marker in ("Matt Pocock", "LICENSE", "THIRD_PARTY_NOTICES.md"):
                        self.assertIn(marker, license_text)
                    self.assertIn("https://github.com/Mysterio1001/Ask-Then-Do-It/issues", faq)
                    if host == "codex":
                        self.assertIn("$ask-then-do-it ", start)
                    elif host == "claude-code":
                        self.assertIn("/ask-then-do-it:ask-then-do-it ", start)
                    else:
                        self.assertIn("generic-workflow.md", start)

    def test_current_consumer_documents_use_current_release_targets(self) -> None:
        documents = set(USER_ZH_DOCUMENTS + USER_LOCALIZED_DOCUMENTS)
        documents.update((ROOT / "docs/guides").glob("claude-code.*.md"))
        repository = "https://github.com/Mysterio1001/Ask-Then-Do-It"
        for document in documents:
            with self.subTest(document=document.relative_to(ROOT)):
                body = document.read_text(encoding="utf-8")
                self.assertNotRegex(body.lower(), r"preview|預覽版|閱覽版|プレビュー")
                self.assertNotIn("vscode://", body)
                for version in re.findall(re.escape(repository) + r"/(?:blob|releases/download)/v([^/]+)/", body):
                    self.assertEqual(version, "1.4.0")
        for host, documents in HOST_GUIDES.items():
            suffix = {"codex": "", "claude-code": "-claude", "generic": "-generic"}[host]
            expected = f"{repository}/releases/download/v1.4.0/ask-then-do-it{suffix}-1.4.0.zip"
            for document in documents.values():
                self.assertIn(expected, document.read_text(encoding="utf-8"))
            self.assertIn(expected, README.read_text(encoding="utf-8"))

    def test_host_guides_keep_mode_settings_and_direct_entry_boundaries(self) -> None:
        prerequisites = {"en": r"prerequisites|does not bypass", "zh-TW": r"前置條件|不會跳過", "ja": r"前提条件|省略されません"}
        for host, documents in HOST_GUIDES.items():
            for locale, document in documents.items():
                body = document.read_text(encoding="utf-8")
                with self.subTest(host=host, locale=locale):
                    if host == "generic":
                        self.assertIn("Default workflow mode: full", body)
                        self.assertIn("Default workflow mode: lite", body)
                        self.assertNotIn(".codex/ask-then-do-it.toml", body)
                        self.assertNotIn(".claude/ask-then-do-it.toml", body)
                    else:
                        folder = ".codex" if host == "codex" else ".claude"
                        for source in ("<project>", "~"):
                            self.assertIn(f"{source}/{folder}/ask-then-do-it.toml", body)
                        for mode in ("full", "lite"):
                            self.assertIn(f'mode = "{mode}"', body)
                        self.assertNotIn("Default workflow mode:", body)
                    if host != "claude-code":
                        self.assertRegex(body, prerequisites[locale])

    def test_codex_and_generic_advanced_entry_lists_remain_complete(self) -> None:
        skills = ("ask-then-do-it", "ask-requirements", "ask-with-docs", "write-spec", "plan-tickets", "implement-direct", "implement-tdd", "review-code", "improve-architecture")
        prompts = ("bootstrap", "orchestration", "lite-workflow", "requirements", "documented-requirements", "specification", "ticket-planning", "direct-implementation", "tdd-implementation", "review", "architecture-improvement")
        for document in CODEX_GUIDES_BY_LOCALE.values():
            body = document.read_text(encoding="utf-8")
            self.assertEqual(set(re.findall(r"\| `\$([\w-]+)` \|", body)), set(skills))
        for document in GENERIC_GUIDES_BY_LOCALE.values():
            body = document.read_text(encoding="utf-8")
            self.assertEqual(set(re.findall(r"\| `([\w-]+)\.md` \|", body)), set(prompts))

    def test_generic_guides_scope_pasting_progress_and_tool_capabilities(self) -> None:
        contracts = {
            "en": (r"every new conversation", r"entire", r"saved requirements, specification, and Ticket Plan", r"Lite does not persist", r"capabilities depend", r"stop pasting"),
            "zh-TW": (r"每個新對話", r"全文", r"已保存的需求、規格與工作規劃", r"Lite 不自動保存", r"能力取決於", r"不再貼入"),
            "ja": (r"新しい会話ごと", r"全文", r"保存済みの要件、仕様、Ticket 計画", r"Lite の状態は.*保存されません", r"能力は.*依存", r"貼り付けをやめ"),
        }
        for locale, document in GENERIC_GUIDES_BY_LOCALE.items():
            body = document.read_text(encoding="utf-8")
            with self.subTest(locale=locale):
                for pattern in contracts[locale]:
                    self.assertRegex(body, pattern)
                self.assertNotRegex(body, r"(?:codex plugin |claude plugin |/plugin )(?:install|add|update|uninstall|remove)")
                self.assertNotIn("$ask-then-do-it", body)
                self.assertNotIn("/ask-then-do-it:", body)

    def test_current_document_navigation_anchors_resolve_offline(self) -> None:
        documents = set(USER_ZH_DOCUMENTS + USER_LOCALIZED_DOCUMENTS)
        documents.update((ROOT / "docs").rglob("*.md"))
        prefix = "https://github.com/Mysterio1001/Ask-Then-Do-It/blob/v1.4.0/"
        for document in documents:
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                if target.startswith(prefix):
                    target = "/" + target[len(prefix):]
                elif "://" in target:
                    continue
                path_text, _, anchor = target.partition("#")
                resolved = (ROOT / path_text.lstrip("/") if path_text.startswith("/") else document.parent / path_text).resolve() if path_text else document
                with self.subTest(document=document.relative_to(ROOT), target=target):
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.is_file(), resolved)
                    if anchor:
                        linked = resolved.read_text(encoding="utf-8")
                        heading_ids = {re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-") for heading in re.findall(r"^#+ (.+)$", linked, re.M)}
                        explicit_ids = set(re.findall(r'<a id="([^"]+)"', linked))
                        self.assertIn(anchor, heading_ids | explicit_ids)


if __name__ == "__main__":
    unittest.main()
