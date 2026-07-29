import hashlib
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "core" / "rules" / "rules.yaml"
V2_SNAPSHOTS = {
    ROOT / "docs" / "specs" / "ai-development-skills.md":
        "3af2b978cfa7aa74be816d8e0cc1169bfd523aee6f6c0961638898d5bce6f615",
    ROOT / "docs" / "plans" / "ai-development-skills.md":
        "efe1d9b90d2a24faedeb66e80b82dd68f4fcad1a7df06115e6455b081dc56e62",
    ROOT / "dist" / "generic-prompts-2.1.0" / "manifest.yaml":
        "057237b84308db74acfd4ab414745e046e550f69cb075618774314353d1474f4",
}


class V2MigrationContractTests(unittest.TestCase):
    def test_migration_rule_and_core_contract_are_present(self) -> None:
        catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
        mandatory = {
            rule["id"] for rule in catalog["rules"] if rule.get("mandatory") is True
        }
        self.assertIn("MIGRATE-V2-001", mandatory)

        contract = (ROOT / "core" / "modules" / "project-knowledge.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "v2 first use",
            "approved v2 artifacts",
            "propose an initial Project Knowledge Base",
            "additions, modifications, and removals",
            "explicit approval",
            "unresolved",
            "MUST NOT rewrite, relabel, or overwrite",
        ):
            self.assertIn(phrase, contract)

    def test_approved_v2_sources_and_generic_release_are_unchanged(self) -> None:
        for path, expected in V2_SNAPSHOTS.items():
            with self.subTest(path=path):
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(actual, expected)

        prompt = (
            ROOT
            / "dist"
            / "generic-prompts-2.1.0"
            / "prompts"
            / "bootstrap.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Core version: `2.0.0`", prompt)

    def test_both_v3_adapters_expose_the_same_first_use_safeguards(self) -> None:
        sources = (
            ROOT
            / "adapters"
            / "codex"
            / "plugin"
            / "grill-me"
            / "skills"
            / "ai-dev-workflow"
            / "SKILL.md",
            ROOT / "adapters" / "generic-prompts" / "bootstrap.md",
        )
        for source in sources:
            text = source.read_text(encoding="utf-8")
            with self.subTest(source=source):
                self.assertIn("approved v2 artifacts", text)
                self.assertIn("propose an initial Project Knowledge Base", text)
                self.assertIn("explicit approval", text)
                self.assertIn("unresolved", text)
                self.assertIn("rewrite, relabel, or overwrite", text.lower())


if __name__ == "__main__":
    unittest.main()
