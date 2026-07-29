import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate_conformance.py"
CATALOG = ROOT / "core" / "rules" / "rules.yaml"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


class ConformanceValidatorTests(unittest.TestCase):
    def run_fixture(self, name: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--catalog",
                str(CATALOG),
                "--manifest",
                str(FIXTURES / name),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def assert_rejected(self, name: str, message: str) -> None:
        result = self.run_fixture(name)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stderr)

    def test_accepts_complete_compatible_manifest(self) -> None:
        result = self.run_fixture("valid.yaml")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Conformance passed", result.stdout)

    def test_rejects_missing_mandatory_rule(self) -> None:
        self.assert_rejected("missing-rule.yaml", "missing mandatory rules")

    def test_rejects_unknown_rule(self) -> None:
        self.assert_rejected("unknown-rule.yaml", "unknown rules")

    def test_rejects_incompatible_core_version(self) -> None:
        self.assert_rejected("incompatible-version.yaml", "incompatible core version")

    def test_rejects_capability_without_evidence(self) -> None:
        self.assert_rejected("unsupported-capability.yaml", "capability lacks evidence")

    def test_core_catalog_contains_approved_mandatory_rules(self) -> None:
        expected = {
            "CAP-DECLARE-001",
            "CAP-CLAIM-001",
            "GATE-REQ-001",
            "GATE-SPEC-001",
            "GATE-PLAN-001",
            "GRILL-ONE-001",
            "SPEC-NOCODE-001",
            "PLAN-VERTICAL-001",
            "TDD-RED-001",
            "REVIEW-EVIDENCE-001",
            "ART-STATE-001",
            "ADAPTER-COVERAGE-001",
            "KB-EVIDENCE-001",
            "KB-DRAFT-001",
            "KB-SYNC-001",
            "REVIEW-LENSES-001",
            "ARCH-DIAG-001",
            "ARCH-DELETE-001",
            "ARCH-REPORT-001",
            "ARCH-REFLOW-001",
            "ROUTE-USER-001",
            "ROUTE-DOCS-001",
            "MIGRATE-V2-001",
        }
        with CATALOG.open(encoding="utf-8") as handle:
            catalog = yaml.safe_load(handle)
        actual = {
            rule["id"]
            for rule in catalog["rules"]
            if rule.get("mandatory") is True
        }
        self.assertEqual(actual, expected)

    def test_core_v3_defines_documented_requirements_artifacts(self) -> None:
        with CATALOG.open(encoding="utf-8") as handle:
            catalog = yaml.safe_load(handle)
        self.assertEqual(catalog["core_version"], "3.0.0")

        knowledge = (
            ROOT / "core" / "artifacts" / "project-knowledge-base.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`docs/project/knowledge-base.md`", knowledge)
        for section in (
            "Glossary",
            "Architecture map",
            "Important decisions",
            "External dependencies",
            "Unresolved items",
            "Artifact links",
        ):
            self.assertIn(section, knowledge)
        for change_type in ("additions", "modifications", "removals"):
            self.assertIn(change_type, knowledge)
        self.assertIn("approved or accepted evidence", knowledge)

        notes = (
            ROOT / "core" / "artifacts" / "draft-working-notes.md"
        ).read_text(encoding="utf-8")
        for state in ("`proposed`", "`confirmed`", "`unresolved`"):
            self.assertIn(state, notes)
        self.assertIn("MUST NOT become formal project knowledge", notes)

        module = (
            ROOT / "core" / "modules" / "project-knowledge.md"
        ).read_text(encoding="utf-8")
        for rule_id in ("KB-EVIDENCE-001", "KB-DRAFT-001", "KB-SYNC-001"):
            self.assertIn(rule_id, module)
        self.assertIn("exactly one question", module)
        self.assertIn("single explicit approval", module)

    def test_core_v3_defines_the_twelve_review_lenses(self) -> None:
        lenses = (
            ROOT / "core" / "references" / "architecture-refactoring-lenses.md"
        ).read_text(encoding="utf-8")
        expected = (
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
        )
        positions = [lenses.index(name) for name in expected]
        self.assertEqual(positions, sorted(positions))
        for outcome in ("`finding`", "`no-finding`", "`not-applicable`", "`unverified`"):
            self.assertIn(outcome, lenses)
        self.assertIn("MUST NOT remove", lenses)
        self.assertIn("reason", lenses)

        review = (ROOT / "core" / "modules" / "review.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("REVIEW-LENSES-001", review)
        self.assertIn("all twelve", review)
        self.assertIn("changed code", review)

    def test_core_v3_defines_safe_architecture_diagnosis(self) -> None:
        module = (
            ROOT / "core" / "modules" / "architecture-improvement.md"
        ).read_text(encoding="utf-8")
        for rule_id in (
            "ARCH-DIAG-001",
            "ARCH-DELETE-001",
            "ARCH-REPORT-001",
            "ARCH-REFLOW-001",
        ):
            self.assertIn(rule_id, module)
        self.assertIn("diagnostic-only by default", module)
        self.assertIn("MUST NOT remove, rename, move, or rewrite", module)
        for gate in (
            "explicit user authorization",
            "Tools capability",
            "disposable, isolated environment",
        ):
            self.assertIn(gate, module)
        self.assertIn("Specification", module)
        self.assertIn("Ticket Plan", module)
        self.assertIn("TDD", module)

        report = (
            ROOT / "core" / "artifacts" / "architecture-improvement-report.md"
        ).read_text(encoding="utf-8")
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
            self.assertIn(section, report)
        for state in ("`draft`", "`accepted`", "`rejected`", "`superseded`"):
            self.assertIn(state, report)
        self.assertIn("MUST NOT authorize", report)

    def test_core_v3_routes_documented_requirements_and_architecture(self) -> None:
        orchestration = (
            ROOT / "core" / "modules" / "orchestration.md"
        ).read_text(encoding="utf-8")
        for rule_id in ("ROUTE-USER-001", "ROUTE-DOCS-001"):
            self.assertIn(rule_id, orchestration)
        self.assertIn("explicit user selection", orchestration)
        for condition in (
            "Project Knowledge Base already exists",
            "changes an existing system",
            "durable project knowledge",
        ):
            self.assertIn(condition, orchestration)
        self.assertIn("brief reason", orchestration)
        for trigger in (
            "directly requests architecture diagnosis",
            "systemic architecture evidence",
            "related Ticket group",
            "release milestone",
        ):
            self.assertIn(trigger, orchestration)
        self.assertIn("MUST NOT run after every Ticket", orchestration)
        self.assertIn("accepted Architecture Improvement Report", orchestration)
        self.assertIn("Specification", orchestration)

    def test_core_contract_is_provider_neutral(self) -> None:
        core = ROOT / "core"
        files = [path for path in core.rglob("*") if path.is_file()]
        self.assertGreaterEqual(len(files), 12, "core contract files are missing")
        forbidden = ("codex", "claude", "gemini", ".codex", "$skill-")
        for path in files:
            if path.suffix.lower() not in {".md", ".yaml", ".yml", ".json"}:
                continue
            text = path.read_text(encoding="utf-8").lower()
            for term in forbidden:
                self.assertNotIn(term, text, f"{term!r} leaked into {path}")


if __name__ == "__main__":
    unittest.main()
