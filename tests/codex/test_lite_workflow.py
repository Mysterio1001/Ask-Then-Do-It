import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "adapters" / "codex"
ORCHESTRATOR = (
    ADAPTER
    / "plugin"
    / "ask-then-do-it"
    / "skills"
    / "ask-then-do-it"
)
SKILLS_ROOT = ORCHESTRATOR.parent
SKILL = ORCHESTRATOR / "SKILL.md"
LITE_REFERENCE = ORCHESTRATOR / "references" / "lite-workflow.md"
MANIFEST = ADAPTER / "conformance.yaml"
RULE_MAPPING = ADAPTER / "rule-mapping.yaml"

PUBLIC_SKILLS = {
    "ask-requirements",
    "ask-then-do-it",
    "ask-with-docs",
    "implement-direct",
    "implement-tdd",
    "improve-architecture",
    "plan-tickets",
    "review-code",
    "write-spec",
}
STAGE_SKILLS = PUBLIC_SKILLS - {"ask-then-do-it"}

LITE_RULES = {
    "MODE-RESOLVE-001": ("SKILL.md", "Resolve the top-level mode"),
    "FULL-PRESERVE-001": ("SKILL.md", "Route the selected mode"),
    "LITE-QUESTIONS-001": (
        "references/lite-workflow.md",
        "Ask blocking questions",
    ),
    "LITE-BRIEF-001": (
        "references/lite-workflow.md",
        "Approve the Change Brief",
    ),
    "LITE-RISK-001": (
        "references/lite-workflow.md",
        "Reconsider material risk",
    ),
    "LITE-VALIDATE-001": (
        "references/lite-workflow.md",
        "Validate proportionately",
    ),
    "LITE-REVIEW-001": (
        "references/lite-workflow.md",
        "Run compact Review",
    ),
    "LITE-SESSION-001": (
        "references/lite-workflow.md",
        "Complete and start new sessions",
    ),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"expected a YAML mapping in {path}")
    return value


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing section: {heading}")
    return match.group(1)


class CodexLiteWorkflowTests(unittest.TestCase):
    def test_direct_skill_entry_keeps_mode_resolution_with_the_orchestrator(self) -> None:
        actual_skills = {
            path.parent.name for path in SKILLS_ROOT.glob("*/SKILL.md")
        }
        self.assertEqual(PUBLIC_SKILLS, actual_skills)

        resolver = " ".join(
            section(read(SKILL), "Resolve the top-level mode").split()
        )
        for phrase in (
            "Direct selection of any public stage Skill selects a stage, not top-level Full",
            "no current-operation mode proof",
            "delegate here before stage behavior",
            "never treat direct Skill selection as Full fallback",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, resolver)

    def test_every_direct_stage_entry_obeys_the_mode_matrix(self) -> None:
        required_contract = (
            "not top-level `full`",
            "Before any stage behavior",
            "current-operation mode",
            "never persist or reuse mode",
            "No proof",
            "stop and delegate to `$ask-then-do-it`",
            "explicit `lite`",
            "Config `lite`",
            "conflicting explicit modes pause for clarification",
            "invalid Config fails closed to Full",
            "Full fallback",
            "Proven `lite`",
            "stop this Full stage",
            "canonical Lite workflow",
            "Proven `full`",
            "continue subject to every existing prerequisite and gate",
        )

        for skill_name in sorted(STAGE_SKILLS):
            with self.subTest(skill=skill_name):
                skill = read(SKILLS_ROOT / skill_name / "SKILL.md")
                direct_entry = " ".join(
                    section(
                        skill,
                        "Resolve the top-level mode before this stage",
                    ).split()
                )
                for phrase in required_contract:
                    self.assertIn(phrase, direct_entry)

    def test_implicit_discovery_resolves_mode_for_every_software_change_size(self) -> None:
        orchestrator = read(SKILL)
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", orchestrator, re.DOTALL)
        self.assertIsNotNone(frontmatter_match, "orchestrator frontmatter is required")
        metadata = yaml.safe_load(frontmatter_match.group(1))
        self.assertIsInstance(metadata, dict)
        description = " ".join(metadata["description"].lower().split())

        self.assertIn("every software-changing operation", description)
        for request_class in (
            "trivial",
            "fully specified",
            "formatting-only",
            "single-line",
        ):
            with self.subTest(request_class=request_class):
                self.assertIn(request_class, description)
        self.assertIn("implicit discovery", description)
        self.assertIn("mode", description)
        self.assertIn("non-software", description)

        full_dispatch = " ".join(
            section(orchestrator, "Decide whether to orchestrate").split()
        )
        for boundary in (
            "resolved Full mode",
            "explicitly resolved-Full subpath",
            "not a third top-level mode",
            "never applies after Lite is selected",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, full_dispatch)

    def test_orchestrator_links_one_level_lite_reference_without_new_skill(self) -> None:
        self.assertTrue(
            LITE_REFERENCE.is_file(),
            "the existing orchestrator Skill must own a one-level Lite reference",
        )
        orchestrator = read(SKILL)
        self.assertIn("[Lite workflow](references/lite-workflow.md)", orchestrator)
        self.assertFalse(
            (ORCHESTRATOR.parent / "lite-workflow").exists(),
            "Lite is a mode, not a separately invokable top-level Skill",
        )

    def test_mode_resolver_is_read_only_fail_closed_and_deterministic(self) -> None:
        resolver = section(read(SKILL), "Resolve the top-level mode")
        for literal in (
            "`full`",
            "`lite`",
            "`~/.codex/ask-then-do-it.toml`",
            "`<project>/.codex/ask-then-do-it.toml`",
            '`mode = "full"`',
            '`mode = "lite"`',
            "explicit current-operation instruction",
            "project Config",
            "user Config",
            "Full fallback",
            "missing-mode",
            "unsupported",
            "malformed",
            "unreadable",
            "outside the active project root",
        ):
            with self.subTest(literal=literal):
                self.assertIn(literal, resolver)

        lower = resolver.lower()
        self.assertIn("read-only", lower)
        self.assertIn("do not write", lower)
        self.assertIn("do not repair", lower)
        self.assertIn("do not reuse", lower)
        self.assertIn("pause", lower)
        self.assertLess(
            resolver.index("explicit current-operation instruction"),
            resolver.index("project Config"),
        )
        self.assertLess(resolver.index("project Config"), resolver.index("user Config"))
        self.assertLess(resolver.index("user Config"), resolver.index("Full fallback"))

        normalized = " ".join(resolver.lower().split())
        for outcome in (
            "valid explicit instruction wins without reading Config",
            "conflicting explicit full and lite instructions pause",
            "absent project Config continues to user Config",
            "valid project Config wins over user Config",
            "present invalid project Config fails closed to Full",
            "absent user Config falls back to Full",
            "present invalid user Config fails closed to Full",
        ):
            with self.subTest(outcome=outcome):
                self.assertIn(outcome.lower(), normalized)

    def test_full_and_lite_routes_remain_separate(self) -> None:
        orchestrator = read(SKILL)
        routing = section(orchestrator, "Route the selected mode")
        self.assertIn("top-level", routing)
        self.assertIn("Ticket-level `tdd` and `direct`", routing)
        self.assertIn("read the [Lite workflow](references/lite-workflow.md) completely", routing)
        self.assertIn("continue through the existing Full workflow below unchanged", routing)
        self.assertIn("MUST NOT fabricate", routing)

        for existing_full_section in (
            "Discover the current stage",
            "Route implementation modes",
            "Enforce the gates",
            "Coordinate tickets",
            "Finish",
        ):
            self.assertIn(f"## {existing_full_section}", orchestrator)

    def test_lite_questions_brief_and_risk_gates_are_complete(self) -> None:
        lite = read(LITE_REFERENCE)
        questions = section(lite, "Ask blocking questions")
        for phrase in (
            "no more than three",
            "approximately 500 tokens",
            "at most three short sentences",
            "one decision",
            "concrete recommendation",
            "principal tradeoff",
            "impact and uncertainty",
            "repository evidence",
        ):
            self.assertIn(phrase, questions)

        brief = section(lite, "Approve the Change Brief")
        for phrase in (
            "objective",
            "in-scope behavior",
            "explicit non-goals",
            "three to five observable acceptance scenarios",
            "material risks",
            "intended validation",
            "approximately 800 tokens",
            "exactly one formal pre-implementation approval",
            "conversation-only",
            "MUST NOT create or update",
            "Implementation Evidence",
            "Review Report",
        ):
            self.assertIn(phrase, brief)

        risk = section(lite, "Reconsider material risk")
        for phrase in (
            "authentication",
            "authorization",
            "payment",
            "data migration",
            "destructive data",
            "public contract",
            "cross-module",
            "concurrency",
            "asynchronous",
            "external side effect",
            "before Change Brief approval",
            "during implementation",
            "pause further modification",
            "only the current operation",
            "MUST NOT persist",
            "earliest unmet Full gate",
        ):
            self.assertIn(phrase, risk)

    def test_lite_implementation_validation_review_and_completion_are_complete(self) -> None:
        lite = read(LITE_REFERENCE)
        implementation = section(lite, "Implement within scope")
        for phrase in (
            "approved Change Brief",
            "materially new behavior or scope",
            "MUST NOT create or modify",
            "behavioral test files",
            "Red, Green, Refactor",
            "unrelated refactoring",
        ):
            self.assertIn(phrase, implementation)

        validation = section(lite, "Validate proportionately")
        for phrase in (
            "repository status and diff",
            "syntax",
            "lint",
            "type-check",
            "build",
            "configuration",
            "schema",
            "principal success path",
            "most important failure or boundary path",
            "existing focused test",
            "manual smoke check",
            "complete behavioral suite",
            "unavailable",
            "known unresolved applicable failure",
            "unqualified completion claim",
        ):
            self.assertIn(phrase, validation)

        review = section(lite, "Run compact Review")
        for phrase in (
            "same implementing AI",
            "non-independent",
            "Change Brief coverage",
            "diff and file scope",
            "principal failure and boundary paths",
            "security-sensitive behavior",
            "sensitive information",
            "observed and unavailable validation",
            "residual risk",
            "one batch",
            "explicitly approves",
            "approved subset",
            "rerun relevant validation",
            "material scope expansion",
            "no actionable findings",
            "MUST NOT create an empty correction gate",
            "twelve-lens",
        ):
            self.assertIn(phrase, review)

        completion = section(lite, "Complete and start new sessions")
        for phrase in (
            "approximately 500 tokens",
            "delivered behavior",
            "changed files or ownership areas",
            "observed validation and outcomes",
            "unavailable checks",
            "unresolved findings",
            "residual risks",
            "new session",
            "resolve mode again",
            "MUST NOT claim to resume",
        ):
            self.assertIn(phrase, completion)

    def test_manifest_and_rule_mapping_truthfully_cover_all_eight_lite_rules(self) -> None:
        manifest = load_yaml(MANIFEST)
        self.assertTrue(LITE_RULES.keys() <= set(manifest["implemented_rules"]))

        mapping = load_yaml(RULE_MAPPING)["rules"]
        for rule_id, (relative, heading) in LITE_RULES.items():
            with self.subTest(rule=rule_id):
                implementations = mapping.get(rule_id)
                self.assertIsInstance(implementations, list)
                self.assertTrue(implementations)
                self.assertTrue(
                    any(
                        entry.get("file")
                        == f"plugin/ask-then-do-it/skills/ask-then-do-it/{relative}"
                        and entry.get("section") == heading
                        and entry.get("implementation")
                        for entry in implementations
                    ),
                    f"{rule_id} lacks a truthful Codex implementation mapping",
                )


if __name__ == "__main__":
    unittest.main()
