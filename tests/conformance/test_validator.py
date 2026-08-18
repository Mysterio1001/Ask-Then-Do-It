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
            "MODE-RESOLVE-001",
            "FULL-PRESERVE-001",
            "LITE-QUESTIONS-001",
            "LITE-BRIEF-001",
            "LITE-RISK-001",
            "LITE-VALIDATE-001",
            "LITE-REVIEW-001",
            "LITE-SESSION-001",
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
        }
        with CATALOG.open(encoding="utf-8") as handle:
            catalog = yaml.safe_load(handle)
        actual = {
            rule["id"]
            for rule in catalog["rules"]
            if rule.get("mandatory") is True
        }
        self.assertEqual(actual, expected)

    def test_core_defines_documented_requirements_artifacts(self) -> None:
        with CATALOG.open(encoding="utf-8") as handle:
            catalog = yaml.safe_load(handle)
        self.assertEqual(catalog["core_version"], "1.3.1")

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

    def test_core_defines_the_twelve_review_lenses(self) -> None:
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

    def test_core_defines_safe_architecture_diagnosis(self) -> None:
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
        self.assertIn("plan-selected implementation path", module)

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

    def test_core_routes_documented_requirements_and_architecture(self) -> None:
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

    def test_core_defines_user_selected_implementation_modes(self) -> None:
        planning = (ROOT / "core" / "modules" / "ticket-planning.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "risk-based test recommendation",
            "tests may increase work time",
            "For every Ticket, warn that tests may increase work time",
            "complete Ticket definitions and all recommendations before requesting one batch test choice",
            "`Add tests`",
            "`Do not add tests`",
            "all Tickets",
            "explicit mixed selection",
            "unresolved Tickets",
            "map `Add tests` to internal mode `tdd`",
            "map `Do not add tests` to internal mode `direct`",
            "`tdd`",
            "`direct`",
            "MUST NOT become `Approved`",
        ):
            self.assertIn(phrase, planning)
        self.assertLess(
            planning.index("Present a risk-based test recommendation"),
            planning.index("Request all per-Ticket choices in one batch"),
        )
        self.assertLess(
            planning.index("For every Ticket, warn that tests may increase work time"),
            planning.index("Request all per-Ticket choices in one batch"),
        )
        prohibition = (
            "Do not ask the user to choose between `tdd` and `direct` as the initial decision"
        )
        self.assertIn(prohibition, planning)
        for line in planning.splitlines():
            if "choose between `tdd` and `direct`" in line.lower():
                self.assertIn("do not", line.lower())
        self.assertIn(
            "Retain resolved choices from an incomplete mixed selection and ask only about unresolved Tickets",
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

        ticket_plan = (ROOT / "core" / "artifacts" / "ticket-plan.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("plain-language test choice", ticket_plan)
        self.assertIn("mapped internal implementation mode", ticket_plan)
        self.assertIn("one batch", ticket_plan)
        self.assertIn("no default", ticket_plan)

        orchestration = (
            ROOT / "core" / "modules" / "orchestration.md"
        ).read_text(encoding="utf-8")
        self.assertIn("approved `tdd` Ticket", orchestration)
        self.assertIn("approved `direct` Ticket", orchestration)
        self.assertIn("MUST NOT infer a default implementation mode", orchestration)
        self.assertIn("all plain-language test choices in one batch", orchestration)

        direct = (
            ROOT / "core" / "modules" / "direct-implementation.md"
        ).read_text(encoding="utf-8")
        self.assertIn("MUST NOT create, modify, or execute behavioral tests", direct)
        self.assertIn("`tests: skipped-by-user`", direct)
        self.assertIn("external CI, hosting, or release system", direct)
        self.assertIn("MUST NOT claim that `direct` bypasses", direct)
        for check in ("lint", "type-check", "build"):
            self.assertIn(check, direct)

        direct_evidence = (
            ROOT / "core" / "artifacts" / "direct-implementation-evidence.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`tests: skipped-by-user`", direct_evidence)
        self.assertIn("unavailable behavioral evidence", direct_evidence)

        review = (ROOT / "core" / "modules" / "review.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "MUST NOT execute or prescribe automatic execution of declined behavioral tests",
            review,
        )
        self.assertIn("`tests: skipped-by-user`", review)

        architecture = (
            ROOT / "core" / "modules" / "architecture-improvement.md"
        ).read_text(encoding="utf-8")
        self.assertIn("plan-selected implementation path", architecture)

        index = (ROOT / "core" / "CORE.md").read_text(encoding="utf-8")
        self.assertIn("Direct implementation", index)
        self.assertIn("Direct Implementation Evidence", index)

        with CATALOG.open(encoding="utf-8") as handle:
            catalog = yaml.safe_load(handle)
        statements = {rule["id"]: rule["statement"] for rule in catalog["rules"]}
        self.assertIn("plain-language test choices in one batch", statements["GATE-PLAN-001"])
        self.assertIn("internal implementation mode", statements["GATE-PLAN-001"])
        self.assertIn("Ticket implementation mode", statements["ROUTE-USER-001"])
        self.assertIn("skipped tests", statements["REVIEW-EVIDENCE-001"])
        self.assertIn("plan-selected implementation", statements["ARCH-REFLOW-001"])

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
