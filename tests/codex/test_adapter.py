import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "adapters" / "codex"
SKILLS = ADAPTER / "plugin" / "ask-then-do-it" / "skills"
CATALOG = ROOT / "core" / "rules" / "rules.yaml"
MANIFEST = ADAPTER / "conformance.yaml"

EXPECTED_SKILLS = {
    "ask-then-do-it",
    "ask-requirements",
    "ask-with-docs",
    "implement-direct",
    "implement-tdd",
    "improve-architecture",
    "plan-tickets",
    "review-code",
    "write-spec",
}


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"expected a YAML mapping in {path}")
    return value


class CodexAdapterTests(unittest.TestCase):
    def test_plugin_skills_are_the_only_source_copy(self) -> None:
        self.assertFalse(
            (ROOT / "skills").exists(),
            "a duplicate root skills directory must not exist",
        )
        self.assertFalse(
            (ADAPTER / "skills").exists(),
            "an intermediate Codex Skill source must not exist",
        )
        self.assertTrue(SKILLS.is_dir(), "the Codex adapter skills root is missing")
        actual = {path.name for path in SKILLS.iterdir() if path.is_dir()}
        self.assertEqual(actual, EXPECTED_SKILLS)

    def test_manifest_declares_full_supported_capabilities_and_rule_coverage(self) -> None:
        manifest = load_yaml(MANIFEST)
        catalog = load_yaml(CATALOG)
        mandatory = {
            rule["id"] for rule in catalog["rules"] if rule.get("mandatory") is True
        }
        self.assertEqual(manifest.get("adapter_id"), "codex")
        self.assertEqual(manifest.get("core_version"), catalog.get("core_version"))
        self.assertEqual(
            manifest.get("capabilities"),
            ["conversation", "tools", "multi_agent"],
        )
        self.assertEqual(set(manifest.get("implemented_rules", [])), mandatory)
        evidence = manifest.get("capability_evidence", {})
        for capability in manifest["capabilities"]:
            self.assertTrue(evidence.get(capability), capability)

        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_conformance.py"),
                "--catalog",
                str(CATALOG),
                "--manifest",
                str(MANIFEST),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Conformance passed: codex", result.stdout)

    def test_every_mandatory_rule_has_a_resolvable_implementation_mapping(self) -> None:
        mapping = load_yaml(ADAPTER / "rule-mapping.yaml")
        catalog = load_yaml(CATALOG)
        mandatory = {
            rule["id"] for rule in catalog["rules"] if rule.get("mandatory") is True
        }
        self.assertEqual(mapping.get("core_version"), catalog.get("core_version"))
        rules = mapping.get("rules")
        self.assertIsInstance(rules, dict)
        self.assertEqual(set(rules), mandatory)

        adapter_root = ADAPTER.resolve()
        for rule_id, implementations in rules.items():
            self.assertIsInstance(implementations, list, rule_id)
            self.assertTrue(implementations, rule_id)
            for implementation in implementations:
                relative = implementation.get("file")
                section = implementation.get("section")
                explanation = implementation.get("implementation")
                self.assertIsInstance(relative, str, rule_id)
                self.assertIsInstance(section, str, rule_id)
                self.assertTrue(section, rule_id)
                self.assertTrue(explanation, rule_id)
                path = (ADAPTER / relative).resolve()
                self.assertTrue(path.is_relative_to(adapter_root), rule_id)
                self.assertTrue(path.is_file(), f"{rule_id}: missing {relative}")
                if path.suffix.lower() == ".md":
                    self.assertIn(
                        f"## {section}",
                        path.read_text(encoding="utf-8"),
                        f"{rule_id}: missing section {section!r} in {relative}",
                    )
                else:
                    self.assertIn(
                        section,
                        load_yaml(path),
                        f"{rule_id}: missing key {section!r} in {relative}",
                    )

    def test_modular_skills_match_user_language(self) -> None:
        for skill_id in EXPECTED_SKILLS:
            text = (SKILLS / skill_id / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_id):
                self.assertIn("Match user-facing", text)

    def test_grill_with_docs_enforces_the_knowledge_approval_contract(self) -> None:
        skill = SKILLS / "ask-with-docs"
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: ask-with-docs", text)
        self.assertIn("core_version` `1.2.0`", text)
        self.assertIn("exactly one question", text)
        self.assertIn("Draft Working Notes", text)
        for state in ("`proposed`", "`confirmed`", "`unresolved`"):
            self.assertIn(state, text)
        self.assertIn("docs/project/knowledge-base.md", text)
        for section in (
            "Glossary",
            "Architecture map",
            "Important decisions",
            "External dependencies",
            "Unresolved items",
            "Artifact links",
        ):
            self.assertIn(section, text)
        for change_type in ("additions", "modifications", "removals"):
            self.assertIn(change_type, text)
        self.assertIn("single explicit approval", text)
        self.assertIn("must not become formal project knowledge", text.lower())
        self.assertIn("Match user-facing", text)

        metadata = load_yaml(skill / "agents" / "openai.yaml")
        interface = metadata.get("interface", {})
        self.assertEqual(interface.get("display_name"), "Ask with Docs")
        self.assertIn("knowledge", interface.get("short_description", "").lower())
        self.assertIn("$ask-with-docs", interface.get("default_prompt", ""))

    def test_orchestrator_declares_runtime_capabilities_before_routing(self) -> None:
        text = (SKILLS / "ask-then-do-it" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Declare capabilities", text)
        self.assertIn("before selecting", text.lower())
        for capability in ("`conversation`", "`tools`", "`multi_agent`"):
            self.assertIn(capability, text)
        self.assertIn("downgrade", text.lower())

    def test_orchestrator_routes_modes_and_honors_direct_selection(self) -> None:
        text = (SKILLS / "ask-then-do-it" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Honor explicit user control", text)
        self.assertIn("## Choose the requirement mode", text)
        self.assertIn("$ask-requirements", text)
        self.assertIn("$ask-with-docs", text)
        self.assertIn("$improve-architecture", text)
        for condition in (
            "Project Knowledge Base already exists",
            "changes an existing system",
            "durable project knowledge",
        ):
            self.assertIn(condition, text)
        self.assertIn("brief reason", text)
        for trigger in (
            "direct architecture request",
            "systemic review evidence",
            "related Ticket group",
            "release milestone",
        ):
            self.assertIn(trigger, text)
        self.assertIn("Do not run architecture diagnosis after every Ticket", text)
        self.assertIn("accepted Architecture Improvement Report", text)
        self.assertIn("$write-spec", text)
        self.assertIn("Knowledge Base Change Summary", text)

    def test_artifact_producers_require_the_portable_envelope(self) -> None:
        producers = {
            "ask-requirements": "Requirement Decision Record",
            "ask-with-docs": "Requirement Decision Record",
            "write-spec": "Specification",
            "plan-tickets": "Ticket Plan",
            "implement-direct": "Direct Implementation Evidence",
            "implement-tdd": "Implementation Evidence",
            "review-code": "Review Report",
            "improve-architecture": "Architecture Improvement Report",
        }
        envelope_fields = (
            "`artifact_type`",
            "`artifact_id`",
            "`workflow_id`",
            "`core_version`",
            "`status`",
            "`inputs`",
            "`assumptions`",
            "`deferred`",
            "`handoff`",
        )
        for skill_id, artifact_type in producers.items():
            text = (SKILLS / skill_id / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_id):
                self.assertIn(artifact_type, text)
                for field in envelope_fields:
                    self.assertIn(field, text)

        for skill_id in (
            "ask-requirements",
            "ask-with-docs",
            "write-spec",
            "plan-tickets",
        ):
            text = (SKILLS / skill_id / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_id, field="approval"):
                self.assertIn("`approval`", text)

    def test_implementation_and_review_require_honest_evidence_labels(self) -> None:
        implementation = (SKILLS / "implement-tdd" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("raw commands", implementation)
        self.assertIn("raw results", implementation)

        review = (SKILLS / "review-code" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for label in ("`independent`", "`non-independent`", "`limited-evidence`"):
            self.assertIn(label, review)

    def test_codex_routes_user_selected_tdd_and_direct_modes(self) -> None:
        planning = (SKILLS / "plan-tickets" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "risk-based test recommendation",
            "tests may increase work time",
            "For every Ticket, warn that tests may increase work time",
            "complete Ticket definitions and all recommendations before requesting one batch test choice",
            "`Add tests to all Tickets`",
            "`Do not add tests to all Tickets`",
            "explicit mixed selection",
            "unresolved Tickets",
            "map `Add tests` to internal mode `tdd`",
            "map `Do not add tests` to internal mode `direct`",
            "`tdd`",
            "`direct`",
            "There is no default",
        ):
            self.assertIn(phrase, planning)
        self.assertLess(
            planning.index("Give every Ticket a risk-based test recommendation"),
            planning.index("Ask in the user's language whether tests should be added"),
        )
        self.assertLess(
            planning.index("For every Ticket, warn that tests may increase work time"),
            planning.index("Ask in the user's language whether tests should be added"),
        )
        prohibition = (
            "Do not present `tdd` and `direct` as the initial user-facing options"
        )
        self.assertIn(prohibition, planning)
        for line in planning.splitlines():
            if "choose between `tdd` and `direct`" in line.lower():
                self.assertTrue(
                    any(word in line.lower() for word in ("do not", "must not", "never"))
                )
        self.assertIn(
            "Retain choices from an incomplete mixed selection and ask only about unresolved Tickets",
            planning,
        )
        for forbidden in (
            "select exactly one implementation mode",
            "choose `tdd` or `direct`",
            "select `tdd` or `direct`",
            "one conversational round trip per Ticket",
            "one response per Ticket",
            "one Ticket at a time",
            "ask each Ticket separately",
        ):
            self.assertNotIn(forbidden, planning)
        for risk in (
            "correctness",
            "regression",
            "security",
            "privacy",
            "migration",
            "integration",
            "destructive behavior",
            "release risk",
        ):
            self.assertIn(risk, planning)
        self.assertIn("must remain `Draft`", planning)

        direct_dir = SKILLS / "implement-direct"
        self.assertTrue((direct_dir / "SKILL.md").is_file())
        self.assertTrue((direct_dir / "agents" / "openai.yaml").is_file())
        direct = (direct_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: implement-direct", direct)
        self.assertIn("Approved `direct` Ticket", direct)
        self.assertIn("Do not create, modify, or execute behavioral tests", direct)
        self.assertIn("`tests: skipped-by-user`", direct)
        self.assertIn("external CI, hosting, or release system", direct)
        self.assertIn("must not claim that `direct` bypasses", direct.lower())
        self.assertIn("Direct Implementation Evidence", direct)
        for check in ("lint", "type-check", "build"):
            self.assertIn(check, direct)

        metadata = load_yaml(direct_dir / "agents" / "openai.yaml")
        interface = metadata.get("interface", {})
        self.assertEqual(interface.get("display_name"), "Implement Direct")
        self.assertIn("$implement-direct", interface.get("default_prompt", ""))

        orchestrator = (SKILLS / "ask-then-do-it" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Approved `tdd` Ticket", orchestrator)
        self.assertIn("$implement-tdd", orchestrator)
        self.assertIn("Approved `direct` Ticket", orchestrator)
        self.assertIn("$implement-direct", orchestrator)
        self.assertIn("Do not infer a default implementation mode", orchestrator)
        self.assertIn("all plain-language test choices in one batch", orchestrator)

        tdd = (SKILLS / "implement-tdd" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Approved `tdd` Ticket", tdd)

        review = (SKILLS / "review-code" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`tests: skipped-by-user`", review)
        self.assertIn(
            "Do not execute or prescribe automatic execution of declined behavioral tests",
            review,
        )

        architecture = (SKILLS / "improve-architecture" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("plan-selected implementation", architecture)

    def test_review_code_applies_all_twelve_lenses_with_evidence(self) -> None:
        review = (SKILLS / "review-code" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for lens in (
            "Duplicated Code or Policy",
            "Long Function",
            "Large Module or Class",
            "Long Parameter List",
            "Data Clumps",
            "Primitive Obsession",
            "Feature Envy",
            "Divergent Change",
            "Shotgun Surgery",
            "Message Chains",
            "Leaky Abstraction",
            "Shallow Module",
        ):
            self.assertIn(lens, review)
        for outcome in ("`finding`", "`no-finding`", "`not-applicable`", "`unverified`"):
            self.assertIn(outcome, review)
        self.assertIn("all twelve", review)
        self.assertIn("must not replace", review.lower())
        self.assertIn("trigger, impact, evidence", review)
        self.assertIn("missing evidence", review)

    def test_improve_architecture_is_diagnostic_and_deletion_safe(self) -> None:
        skill = SKILLS / "improve-architecture"
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: improve-architecture", text)
        self.assertIn("Architecture Improvement Report", text)
        self.assertIn("diagnostic-only by default", text)
        self.assertIn("simulated deletion", text)
        self.assertIn("must not remove, rename, move, or rewrite", text.lower())
        for gate in (
            "explicit user authorization",
            "`tools` capability",
            "disposable, isolated environment",
        ):
            self.assertIn(gate, text)
        for state in ("`draft`", "`accepted`", "`rejected`", "`superseded`"):
            self.assertIn(state, text)
        for section in (
            "Analysis scope and limitations",
            "System architecture summary",
            "Deletion-analysis results",
            "Twelve-lens results",
            "Finding evidence, impact, and confidence",
            "Prioritized improvement proposals",
            "Potentially affected modules",
            "Unresolved items",
            "Artifact links",
            "Knowledge Base Change Summary",
        ):
            self.assertIn(section, text)
        self.assertIn("accepted report does not authorize", text.lower())
        self.assertIn("Specification", text)
        self.assertIn("Ticket Plan", text)
        self.assertIn("plan-selected implementation", text)
        self.assertIn("$implement-tdd", text)
        self.assertIn("$implement-direct", text)
        self.assertIn("Match user-facing", text)

        metadata = load_yaml(skill / "agents" / "openai.yaml")
        interface = metadata.get("interface", {})
        self.assertEqual(interface.get("display_name"), "Improve Architecture")
        self.assertIn("diagnose", interface.get("short_description", "").lower())
        self.assertIn("$improve-architecture", interface.get("default_prompt", ""))

    def test_review_routes_only_systemic_lens_findings_to_architecture(self) -> None:
        review = (SKILLS / "review-code" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("systemic", review)
        self.assertIn("$improve-architecture", review)
        self.assertIn("already tracked", review)


if __name__ == "__main__":
    unittest.main()
