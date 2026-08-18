import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "release" / "release.json"
CODEX = ROOT / "adapters" / "codex"
GENERIC = ROOT / "adapters" / "generic-prompts"

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

EXPECTED_PROMPTS = {
    "architecture-improvement.md",
    "bootstrap.md",
    "documented-requirements.md",
    "direct-implementation.md",
    "lite-workflow.md",
    "orchestration.md",
    "requirements.md",
    "review.md",
    "specification.md",
    "tdd-implementation.md",
    "ticket-planning.md",
}

EXPECTED_RULES = {
    "ADAPTER-COVERAGE-001",
    "ARCH-DELETE-001",
    "ARCH-DIAG-001",
    "ARCH-REFLOW-001",
    "ARCH-REPORT-001",
    "ART-STATE-001",
    "CAP-CLAIM-001",
    "CAP-DECLARE-001",
    "FULL-PRESERVE-001",
    "GATE-PLAN-001",
    "GATE-REQ-001",
    "GATE-SPEC-001",
    "GRILL-ONE-001",
    "KB-DRAFT-001",
    "KB-EVIDENCE-001",
    "KB-SYNC-001",
    "LITE-BRIEF-001",
    "LITE-QUESTIONS-001",
    "LITE-REVIEW-001",
    "LITE-RISK-001",
    "LITE-SESSION-001",
    "LITE-VALIDATE-001",
    "MODE-RESOLVE-001",
    "PLAN-VERTICAL-001",
    "REVIEW-EVIDENCE-001",
    "REVIEW-LENSES-001",
    "ROUTE-DOCS-001",
    "ROUTE-USER-001",
    "SPEC-NOCODE-001",
    "TDD-RED-001",
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class CleanSlateContractTests(unittest.TestCase):
    def test_all_active_component_versions_are_1_3_1(self) -> None:
        config = json.loads(text(RELEASE))
        self.assertEqual(config["release_version"], "1.3.1")
        self.assertEqual(config["core_version"], "1.3.1")
        self.assertIn("Core version: `1.3.1`", text(ROOT / "core" / "CORE.md"))
        self.assertIn("core_version: 1.3.1", text(ROOT / "core" / "rules" / "rules.yaml"))

        for manifest in (
            CODEX / "conformance.yaml",
            CODEX / "rule-mapping.yaml",
            GENERIC / "manifest.yaml",
        ):
            with self.subTest(manifest=manifest.relative_to(ROOT)):
                self.assertNotIn("3.0.0", text(manifest))
                self.assertIn("1.3.1", text(manifest))

        plugin = json.loads(
            text(CODEX / "plugin" / "ask-then-do-it" / ".codex-plugin" / "plugin.json")
        )
        self.assertEqual(plugin["version"], "1.3.1")

        for prompt in EXPECTED_PROMPTS:
            with self.subTest(prompt=prompt):
                self.assertIn("Core version: `1.3.1`", text(GENERIC / prompt))

        for skill in EXPECTED_SKILLS:
            with self.subTest(skill=skill):
                self.assertNotIn(
                    "core_version` `3.0.0`",
                    text(CODEX / "plugin" / "ask-then-do-it" / "skills" / skill / "SKILL.md"),
                )

    def test_migration_contract_is_completely_absent(self) -> None:
        self.assertFalse((ROOT / "tests" / "migration").exists())
        self.assertFalse((CODEX / "migration-inventory.yaml").exists())
        for area in (ROOT / "core", ROOT / "adapters"):
            for path in area.rglob("*"):
                if path.is_file() and path.suffix.lower() in {
                    ".json",
                    ".md",
                    ".yaml",
                    ".yml",
                }:
                    body = text(path)
                    with self.subTest(path=path.relative_to(ROOT)):
                        self.assertNotIn("MIGRATE-V2-001", body)
                        self.assertNotIn("Migrate v2 on first use", body)
                        self.assertNotIn("v2 first use migration", body)

    def test_only_current_canonical_artifacts_remain(self) -> None:
        specs = {p.name for p in (ROOT / "docs" / "specs").glob("*.md")}
        plans = {p.name for p in (ROOT / "docs" / "plans").glob("*.md")}
        evidence = {p.name for p in (ROOT / "docs" / "evidence").glob("*")}
        self.assertIn("ask-then-do-it-1.0.0.md", specs)
        self.assertIn("ask-then-do-it-1.0.0.md", plans)
        for ticket in (1, 2, 3):
            self.assertIn(f"ask-then-do-it-1.0.0-ticket-{ticket}.md", evidence)
        for collection in (specs, plans, evidence):
            self.assertFalse(any("2.1.0" in name or "3.0.0" in name for name in collection))

    def test_release_configuration_uses_provider_directories(self) -> None:
        config = json.loads(text(RELEASE))
        self.assertEqual(config["codex"]["directory"], "codex/ask-then-do-it")
        self.assertEqual(
            config["codex"]["archive"], "codex/ask-then-do-it-1.3.1.zip"
        )
        self.assertEqual(
            config["generic"]["directory"],
            "generic/ask-then-do-it-generic-1.3.1",
        )
        self.assertEqual(
            config["generic"]["archive"],
            "generic/ask-then-do-it-generic-1.3.1.zip",
        )
        self.assertEqual(
            config["managed_outputs"],
            ["codex", "generic", "checksums.sha256"],
        )
        self.assertNotIn("v2-preservation", config["required_validation_checks"])

    def test_retained_workflow_inventory_and_rules_are_unchanged(self) -> None:
        skills = CODEX / "plugin" / "ask-then-do-it" / "skills"
        self.assertEqual({p.name for p in skills.iterdir() if p.is_dir()}, EXPECTED_SKILLS)
        self.assertEqual({p.name for p in GENERIC.glob("*.md")}, EXPECTED_PROMPTS)

        catalog = text(ROOT / "core" / "rules" / "rules.yaml")
        actual_rules = set(re.findall(r"(?m)^\s*- id: ([A-Z0-9-]+)$", catalog))
        self.assertEqual(actual_rules, EXPECTED_RULES)

    def test_no_historical_distribution_output_remains(self) -> None:
        dist = ROOT / "dist"
        if not dist.exists():
            return
        self.assertEqual(
            {path.name for path in dist.iterdir()},
            {"codex", "generic", "checksums.sha256"},
        )


if __name__ == "__main__":
    unittest.main()
