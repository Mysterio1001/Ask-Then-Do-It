import re
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "adapters" / "generic-prompts"
MANIFEST = ADAPTER / "manifest.yaml"
PROMPTS = {
    "bootstrap.md",
    "orchestration.md",
    "requirements.md",
    "documented-requirements.md",
    "architecture-improvement.md",
    "specification.md",
    "ticket-planning.md",
    "tdd-implementation.md",
    "review.md",
}


def prompt(name: str) -> str:
    return (ADAPTER / name).read_text(encoding="utf-8")


class GenericPromptContractTests(unittest.TestCase):
    def test_adapter_has_exactly_one_bootstrap_and_eight_module_prompts(self) -> None:
        actual = {path.name for path in ADAPTER.glob("*.md")}
        self.assertEqual(actual, PROMPTS)

    def test_every_prompt_declares_the_required_interface(self) -> None:
        for name in PROMPTS:
            text = prompt(name)
            with self.subTest(prompt=name):
                self.assertRegex(text, r"(?m)^Prompt ID: `[^`]+`$")
                self.assertRegex(text, r"(?m)^Prompt version: `1\.0\.1`$")
                self.assertRegex(text, r"(?m)^Required capability: `[^`]+`$")
                self.assertRegex(text, r"(?m)^Core version: `1\.0\.1`$")
                for heading in (
                    "## Required inputs",
                    "## Expected outputs",
                    "## Stop conditions",
                ):
                    self.assertIn(heading, text)

    def test_prompt_sources_are_english_and_provider_neutral(self) -> None:
        forbidden = ("codex", "claude", "gemini", ".codex", "$skill-", "openai")
        for name in PROMPTS:
            text = prompt(name)
            with self.subTest(prompt=name):
                self.assertIsNone(
                    re.search(r"[\u3400-\u9fff]", text),
                    "canonical generic prompts must remain in English",
                )
                lowered = text.lower()
                for term in forbidden:
                    self.assertNotIn(term, lowered)

    def test_manifest_declares_only_conversation_and_maps_all_rules(self) -> None:
        manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        catalog = yaml.safe_load(
            (ROOT / "core" / "rules" / "rules.yaml").read_text(encoding="utf-8")
        )
        mandatory = {
            rule["id"] for rule in catalog["rules"] if rule.get("mandatory") is True
        }
        self.assertEqual(manifest["capabilities"], ["conversation"])
        self.assertEqual(set(manifest["implemented_rules"]), mandatory)
        self.assertEqual(manifest["artifact_persistence"], "user-managed-markdown")

    def test_manifest_passes_shared_conformance_validator(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_conformance.py"),
                "--catalog",
                str(ROOT / "core" / "rules" / "rules.yaml"),
                "--manifest",
                str(MANIFEST),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Conformance passed: generic-prompts", result.stdout)


class GenericPromptScenarioTests(unittest.TestCase):
    def test_fresh_bootstrap_defaults_unknown_capability_to_conversation(self) -> None:
        text = prompt("bootstrap.md")
        self.assertIn("Default to `conversation`", text)
        self.assertIn("first unmet stage", text)
        self.assertIn("requirement consensus", text)
        self.assertIn("same effective response", text)
        self.assertIn("exactly one high-impact requirement question", text)
        self.assertIn("recommended answer", text)
        self.assertIn("principal tradeoff", text)
        self.assertIn("Do not stop after", text)
        self.assertIn('say "start"', text)

    def test_resumed_bootstrap_imports_artifacts_without_restarting(self) -> None:
        text = prompt("bootstrap.md")
        self.assertIn("Inspect every supplied artifact", text)
        self.assertIn("Reuse verified Approved artifacts", text)
        self.assertIn("Do not restart completed stages", text)
        self.assertIn("approval evidence", text)

    def test_generic_routing_honors_explicit_selection_and_explains_auto_routes(self) -> None:
        texts = prompt("bootstrap.md") + "\n" + prompt("orchestration.md")
        self.assertIn("explicit user selection", texts)
        self.assertIn("requirements.md", texts)
        self.assertIn("documented-requirements.md", texts)
        self.assertIn("architecture-improvement.md", texts)
        for condition in (
            "Project Knowledge Base already exists",
            "changes an existing system",
            "durable project knowledge",
        ):
            self.assertIn(condition, texts)
        self.assertIn("brief reason", texts)
        for trigger in (
            "direct architecture request",
            "systemic review evidence",
            "related Ticket group",
            "release milestone",
        ):
            self.assertIn(trigger, texts)
        self.assertIn("Do not run architecture diagnosis after every Ticket", texts)
        self.assertIn("accepted Architecture Improvement Report", texts)
        self.assertIn("specification.md", texts)
        self.assertIn("Knowledge Base Change Summary", texts)

    def test_requirements_asks_one_recommended_question_and_matches_language(self) -> None:
        text = prompt("requirements.md")
        self.assertIn("Ask exactly one question in each turn", text)
        self.assertIn("recommended answer", text)
        self.assertIn("principal tradeoff", text)
        self.assertIn("Match the user's language", text)

    def test_documented_requirements_keeps_unapproved_knowledge_in_draft(self) -> None:
        text = prompt("documented-requirements.md")
        self.assertIn("Ask exactly one question in each turn", text)
        self.assertIn("recommended answer", text)
        self.assertIn("principal tradeoff", text)
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
        self.assertIn("user owns cross-session persistence", text)

    def test_draft_artifact_prompts_preserve_gates_and_user_persistence(self) -> None:
        for name in ("requirements.md", "specification.md", "ticket-planning.md"):
            text = prompt(name)
            with self.subTest(prompt=name):
                self.assertIn("`Draft`", text)
                self.assertIn("explicit human approval", text)
                self.assertIn("user owns cross-session persistence", text)
                self.assertIn("re-supply", text)

    def test_conversation_implementation_stops_with_unexecuted_handoff(self) -> None:
        text = prompt("tdd-implementation.md")
        required = (
            "UNEXECUTED IMPLEMENTATION GUIDANCE",
            "do not modify or claim to modify repository files",
            "do not run or claim to run commands or tests",
            "do not emit completed Implementation Evidence",
            "Stop after the unexecuted handoff",
            "tools-capable host",
        )
        for phrase in required:
            self.assertIn(phrase, text)

    def test_supplied_diff_review_is_limited_and_non_independent(self) -> None:
        text = prompt("review.md")
        self.assertIn("Review label: `limited-evidence`", text)
        self.assertIn("Independence: `non-independent`", text)
        self.assertIn("Never claim independent review", text)
        self.assertIn("raw diff", text)
        self.assertIn("unavailable evidence", text)

    def test_review_applies_all_twelve_lenses_without_hiding_unknowns(self) -> None:
        text = prompt("review.md")
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
            self.assertIn(lens, text)
        for outcome in ("`finding`", "`no-finding`", "`not-applicable`", "`unverified`"):
            self.assertIn(outcome, text)
        self.assertIn("all twelve", text)
        self.assertIn("missing evidence", text)
        self.assertIn("must not replace", text.lower())

    def test_architecture_prompt_is_diagnostic_and_capability_aware(self) -> None:
        text = prompt("architecture-improvement.md")
        self.assertIn("diagnostic-only by default", text)
        self.assertIn("simulated deletion", text)
        self.assertIn("do not remove, rename, move, or rewrite", text.lower())
        for gate in (
            "explicit user authorization",
            "Tools capability",
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
        self.assertIn("TDD", text)
        for label in ("`unverified`", "`unavailable`"):
            self.assertIn(label, text)

    def test_generic_review_routes_systemic_findings_without_duplicates(self) -> None:
        text = prompt("review.md")
        self.assertIn("systemic", text)
        self.assertIn("architecture-improvement.md", text)
        self.assertIn("already tracked", text)


if __name__ == "__main__":
    unittest.main()
