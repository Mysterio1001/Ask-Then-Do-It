import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import validate_codex_contract as contract


ADAPTER = ROOT / "adapters" / "codex"
SOURCE_PACKAGE = ADAPTER / "plugin" / "ask-then-do-it"
ORCHESTRATOR = (
    SOURCE_PACKAGE
    / "skills"
    / "ask-then-do-it"
)
SKILLS_ROOT = ORCHESTRATOR.parent
SKILL = ORCHESTRATOR / "SKILL.md"
FULL_REFERENCE = ORCHESTRATOR / "references" / "full-routing.md"
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

FULL_ONLY_SECTIONS = (
    "Decide whether to orchestrate",
    "Honor explicit user control",
    "Choose the requirement mode",
    "Discover the current stage",
    "Route implementation modes",
    "Route architecture diagnosis",
    "Synchronize project knowledge",
    "Enforce the gates",
    "Coordinate tickets",
    "Finish",
)

ROOT_SECTIONS = (
    "Declare capabilities",
    "Resolve the top-level mode",
    "Route the selected mode",
    "Operating rules",
)

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


def parse_frontmatter_description(text: str) -> str:
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if frontmatter_match is None:
        raise AssertionError("orchestrator frontmatter is required")
    description_match = re.search(
        r"^description:[ \t]*(.*?)\s*$",
        frontmatter_match.group(1),
        flags=re.MULTILINE,
    )
    if description_match is None:
        raise AssertionError("orchestrator description is required")
    diagnostics: list[contract.Diagnostic] = []
    description = contract.parse_yaml_scalar(
        description_match.group(1),
        field="description",
        path=SKILL,
        diagnostics=diagnostics,
    )
    if diagnostics or description is None:
        rendered = "; ".join(item.render() for item in diagnostics)
        raise AssertionError(f"invalid orchestrator description: {rendered}")
    return description


def parse_rule_mapping() -> dict[str, list[dict[str, str]]]:
    diagnostics: list[contract.Diagnostic] = []
    mapping = contract.parse_rule_mapping(RULE_MAPPING, diagnostics)
    if diagnostics:
        rendered = "; ".join(item.render() for item in diagnostics)
        raise AssertionError(f"invalid rule mapping: {rendered}")
    return mapping.rules


def parse_implemented_rules() -> set[str]:
    diagnostics: list[contract.Diagnostic] = []
    manifest = contract.parse_conformance_manifest(MANIFEST, diagnostics)
    if diagnostics:
        rendered = "; ".join(item.render() for item in diagnostics)
        raise AssertionError(f"invalid conformance manifest: {rendered}")
    return set(manifest.implemented_rule_ids)


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
            "Before stage behavior",
            "current-operation mode",
            "never persist or reuse mode",
            "Missing proof",
            "stop and delegate to `$ask-then-do-it`",
            "Proven `lite`",
            "stop this Full stage",
            "Lite workflow",
            "Proven `full`",
            "continue with this stage's prerequisites and gates",
        )
        forbidden_resolver_matrix = (
            "project Config",
            "user Config",
            "missing-mode",
            "unsupported mode",
            "malformed TOML",
            "Full fallback",
            "conflicting explicit",
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
                for phrase in forbidden_resolver_matrix:
                    with self.subTest(forbidden=phrase):
                        self.assertNotIn(phrase, direct_entry)

    def test_direct_stage_guards_are_concise(self) -> None:
        for skill_name in sorted(STAGE_SKILLS):
            with self.subTest(skill=skill_name):
                direct_entry = section(
                    read(SKILLS_ROOT / skill_name / "SKILL.md"),
                    "Resolve the top-level mode before this stage",
                )
                self.assertLessEqual(len(direct_entry.split()), 115)

    def test_implicit_discovery_resolves_mode_for_every_software_change_size(self) -> None:
        orchestrator = read(SKILL)
        description = " ".join(
            parse_frontmatter_description(orchestrator).lower().split()
        )

        self.assertIn("every software-changing operation", description)
        for request_class in (
            "trivial",
            "fully specified",
            "formatting-only",
            "single-line",
        ):
            with self.subTest(request_class=request_class):
                self.assertIn(request_class, description)
        self.assertIn("implicit", description)
        self.assertIn("discovery", description)
        self.assertIn("mode", description)
        self.assertIn("non-software", description)

        full_dispatch = " ".join(
            section(read(FULL_REFERENCE), "Decide whether to orchestrate").split()
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

    def test_selected_modes_load_mutually_exclusive_direct_references(self) -> None:
        orchestrator = read(SKILL)
        routing = section(orchestrator, "Route the selected mode")
        self.assertIn("top-level", routing)
        self.assertIn("Ticket-level `tdd` and `direct`", routing)
        self.assertIn("MUST NOT fabricate", routing)

        branches = {}
        for mode in ("full", "lite"):
            match = re.search(
                rf"^- For [^\n]*`{mode}`.*?(?=^- For |\Z)",
                routing,
                flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
            )
            self.assertIsNotNone(match, f"missing {mode} route")
            branches[mode] = match.group(0)

        expected_links = {
            "full": "references/full-routing.md",
            "lite": "references/lite-workflow.md",
        }
        for mode, branch in branches.items():
            with self.subTest(mode=mode):
                normalized = " ".join(branch.lower().split())
                links = re.findall(r"\[[^]]+\]\(([^)]+)\)", branch)
                self.assertEqual(links, [expected_links[mode]])
                self.assertIn("proven", normalized)
                self.assertIn("completely", normalized)
                self.assertIn("before acting", normalized)

        self.assertNotIn(expected_links["lite"], branches["full"])
        self.assertNotIn(expected_links["full"], branches["lite"])

    def test_full_only_sections_have_one_runtime_owner(self) -> None:
        root_headings = contract.markdown_h2_headings(read(SKILL))
        full_headings = contract.markdown_h2_headings(read(FULL_REFERENCE))

        for heading in ROOT_SECTIONS:
            with self.subTest(root_heading=heading):
                self.assertEqual(root_headings.count(heading), 1)

        for heading in FULL_ONLY_SECTIONS:
            with self.subTest(full_heading=heading):
                self.assertEqual(root_headings.count(heading), 0)
                self.assertEqual(full_headings.count(heading), 1)

    def test_full_reference_is_direct_leaf_and_mappings_are_reachable(self) -> None:
        graph, diagnostics = contract.validate_reference_graph(
            SOURCE_PACKAGE,
            SOURCE_PACKAGE,
        )
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(graph)
        assert graph is not None

        root_source = "skills/ask-then-do-it/SKILL.md"
        full_target = "skills/ask-then-do-it/references/full-routing.md"
        lite_target = "skills/ask-then-do-it/references/lite-workflow.md"
        self.assertEqual(graph.graph[root_source], (full_target, lite_target))
        self.assertEqual(graph.graph[full_target], ())

        contract.validate_contract(
            ADAPTER,
            SOURCE_PACKAGE,
            SOURCE_PACKAGE,
            RULE_MAPPING,
        )
        mapping = parse_rule_mapping()
        expected_mappings = {
            "CAP-CLAIM-001": "Finish",
            "ART-STATE-001": "Enforce the gates",
            "ROUTE-USER-001": "Honor explicit user control",
            "ROUTE-DOCS-001": "Choose the requirement mode",
        }
        expected_file = (
            "plugin/ask-then-do-it/skills/ask-then-do-it/"
            "references/full-routing.md"
        )
        for rule_id, heading in expected_mappings.items():
            with self.subTest(rule=rule_id):
                self.assertTrue(
                    any(
                        entry["file"] == expected_file
                        and entry["section"] == heading
                        for entry in mapping[rule_id]
                    )
                )

    def test_measurement_load_sets_follow_selected_route(self) -> None:
        root_source = "skills/ask-then-do-it/SKILL.md"
        full_reference = "skills/ask-then-do-it/references/full-routing.md"
        lite_reference = "skills/ask-then-do-it/references/lite-workflow.md"
        artifact_contract = "skills/ask-then-do-it/references/artifact-contract.md"
        lens_contract = (
            "skills/ask-then-do-it/references/architecture-refactoring-lenses.md"
        )
        entry_sets = contract.DEFAULT_LOAD_SETS
        load_sets = contract.ACTION_READY_LOAD_SETS

        self.assertEqual(entry_sets["root-router"], (root_source,))
        self.assertEqual(entry_sets["lite"], (root_source, lite_reference))
        self.assertEqual(load_sets["root-router"], entry_sets["root-router"])
        self.assertEqual(load_sets["lite"], entry_sets["lite"])
        for name, sources in entry_sets.items():
            if not name.startswith("full-"):
                continue
            with self.subTest(load_set=name):
                self.assertEqual(len(sources), 3)
                self.assertEqual(sources[:2], (root_source, full_reference))
                self.assertNotIn(lite_reference, sources)
                self.assertEqual(load_sets[name][:3], sources)
                self.assertEqual(load_sets[name][-1], artifact_contract)
                if name in {"full-review", "full-architecture"}:
                    self.assertEqual(load_sets[name][-2], lens_contract)
                else:
                    self.assertNotIn(lens_contract, load_sets[name])

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
        self.assertTrue(LITE_RULES.keys() <= parse_implemented_rules())

        mapping = parse_rule_mapping()
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
