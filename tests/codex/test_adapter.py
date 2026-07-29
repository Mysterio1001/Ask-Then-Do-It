import hashlib
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

LEGACY_SKILLS = {
    "ask-then-do-it",
    "ask-requirements",
    "implement-tdd",
    "plan-tickets",
    "review-code",
    "write-spec",
}
EXPECTED_SKILLS = LEGACY_SKILLS | {"ask-with-docs", "improve-architecture"}

# This snapshot was captured from the approved v1 source before migration. It
# protects skill behavior and Codex provider metadata from accidental rewrites.
EXPECTED_FILE_HASHES = {
    "ask-then-do-it/SKILL.md":
        "87c0efd63fd96910c8b24479e94dc5f7412cc7e5e58977c30ede067699dea546",
    "ask-then-do-it/agents/openai.yaml":
        "25b6062bef499ea486c1193b55e2cb2eadb40727238135ba113c3fe9e202c6b6",
    "ask-requirements/SKILL.md":
        "4100d4cd1e0300d16d86641789613556f436b5e7f4f8d88081e0402ffc27bcd6",
    "ask-requirements/agents/openai.yaml":
        "c9051df766cd762decded3d267bde5ec7fce335a7c772e1fcff30419d03c065a",
    "implement-tdd/SKILL.md":
        "3ccaeac0700c32ec92cf8cc208ebdf569e22265b2adc9c8ae9b2f74a1a2a81b3",
    "implement-tdd/agents/openai.yaml":
        "f190cd2031eb1d95afc513a4322f51e8023ccc7ccb37305f7c58d58bf1e12779",
    "plan-tickets/SKILL.md":
        "2341d90ac091608e0bff5a4c8be8d84ac45540ca7d7d1a610425330b04682e96",
    "plan-tickets/agents/openai.yaml":
        "86c121173812398f1fa29ba5db6547853baf9fad27ee536adaa4000939bdd0bf",
    "review-code/SKILL.md":
        "aad8d0b13fc079783ebda93582d49725cc7d0e5eb84dc51f251d84caa35072b1",
    "review-code/agents/openai.yaml":
        "673bba8f305c8d6e9700e4ea668764ed1ea5cc4dc4b4eb0b1ee8b28b47647cbc",
    "write-spec/SKILL.md":
        "67d8376479b6110b481607450b1311d6822f47695930679cb039be2425d43d79",
    "write-spec/agents/openai.yaml":
        "b5d40f998e48f852fb1f9720ac4576b2086310cecf34d32c2a011c3e696f50eb",
}


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"expected a YAML mapping in {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CodexAdapterTests(unittest.TestCase):
    def test_migrated_skills_are_the_only_source_copy(self) -> None:
        self.assertFalse(
            (ROOT / "skills").exists(),
            "the duplicate v1 root skills directory must be removed",
        )
        self.assertFalse(
            (ADAPTER / "skills").exists(),
            "the intermediate Codex Skill source must be removed after Plugin migration",
        )
        self.assertTrue(SKILLS.is_dir(), "the Codex adapter skills root is missing")
        actual = {path.name for path in SKILLS.iterdir() if path.is_dir()}
        self.assertEqual(actual, EXPECTED_SKILLS)

    def test_migration_inventory_preserves_v1_snapshot_and_tracks_v2_payload(self) -> None:
        actual_files = {
            path.relative_to(SKILLS).as_posix()
            for skill_id in LEGACY_SKILLS
            for path in (SKILLS / skill_id).rglob("*")
            if path.is_file()
        }
        self.assertEqual(actual_files, set(EXPECTED_FILE_HASHES))

        inventory = load_yaml(ADAPTER / "migration-inventory.yaml")
        entries = {entry["id"]: entry for entry in inventory["skills"]}
        for relative, expected_v1_hash in EXPECTED_FILE_HASHES.items():
            skill_id, skill_relative = relative.split("/", 1)
            recorded = entries[skill_id]["files"][skill_relative]
            with self.subTest(file=relative):
                self.assertEqual(recorded["pre_migration_sha256"], expected_v1_hash)
                self.assertEqual(
                    recorded["current_sha256"],
                    sha256(SKILLS / relative),
                )

    def test_migration_inventory_has_safe_rollback_mapping(self) -> None:
        inventory = load_yaml(ADAPTER / "migration-inventory.yaml")
        self.assertEqual(inventory.get("source_root"), "skills")
        self.assertEqual(inventory.get("intermediate_root"), "adapters/codex/skills")
        self.assertEqual(
            inventory.get("destination_root"),
            "adapters/codex/plugin/ask-then-do-it/skills",
        )
        entries = inventory.get("skills")
        self.assertIsInstance(entries, list)
        self.assertEqual({entry.get("id") for entry in entries}, LEGACY_SKILLS)

        for entry in entries:
            skill_id = entry["id"]
            self.assertEqual(entry.get("source"), f"skills/{skill_id}")
            self.assertEqual(
                entry.get("intermediate"), f"adapters/codex/skills/{skill_id}"
            )
            self.assertEqual(
                entry.get("destination"),
                f"adapters/codex/plugin/ask-then-do-it/skills/{skill_id}",
            )
            rollback = entry.get("rollback")
            self.assertEqual(rollback.get("from"), entry["destination"])
            self.assertEqual(rollback.get("to"), entry["intermediate"])
            files = entry.get("files")
            self.assertIsInstance(files, dict)
            expected_relatives = {
                relative.removeprefix(f"{skill_id}/")
                for relative in EXPECTED_FILE_HASHES
                if relative.startswith(f"{skill_id}/")
            }
            self.assertEqual(set(files), expected_relatives)
            for relative, hashes in files.items():
                self.assertEqual(
                    hashes.get("pre_migration_sha256"),
                    EXPECTED_FILE_HASHES[f"{skill_id}/{relative}"],
                )
                self.assertEqual(
                    hashes.get("current_sha256"),
                    sha256(SKILLS / skill_id / relative),
                )

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
        self.assertIn("core_version` `1.0.0`", text)
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
        self.assertEqual(interface.get("display_name"), "Grill with Docs")
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
        self.assertIn("TDD", text)
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
