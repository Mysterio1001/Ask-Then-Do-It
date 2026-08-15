import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "core"
CATALOG = CORE / "rules" / "rules.yaml"
LITE_MODULE = CORE / "modules" / "lite-workflow.md"

LITE_RULE_MODULES = {
    "MODE-RESOLVE-001": "orchestration",
    "FULL-PRESERVE-001": "orchestration",
    "LITE-QUESTIONS-001": "lite-workflow",
    "LITE-BRIEF-001": "lite-workflow",
    "LITE-RISK-001": "lite-workflow",
    "LITE-VALIDATE-001": "lite-workflow",
    "LITE-REVIEW-001": "lite-workflow",
    "LITE-SESSION-001": "lite-workflow",
}

def catalog_rules() -> dict[str, dict[str, object]]:
    with CATALOG.open(encoding="utf-8") as handle:
        catalog = yaml.safe_load(handle)
    return {rule["id"]: rule for rule in catalog["rules"]}


class LiteCoreContractTests(unittest.TestCase):
    def test_core_exposes_dedicated_lite_module_without_artifact_template(self) -> None:
        self.assertTrue(
            LITE_MODULE.is_file(),
            "Core must expose a dedicated Lite workflow module",
        )
        index = (CORE / "CORE.md").read_text(encoding="utf-8")
        self.assertIn("[Lite workflow](modules/lite-workflow.md)", index)

        artifact_names = {
            path.name.lower() for path in (CORE / "artifacts").iterdir() if path.is_file()
        }
        self.assertFalse(any("lite" in name for name in artifact_names))
        self.assertFalse(any("change-brief" in name for name in artifact_names))

    def test_lite_module_covers_the_approved_lifecycle(self) -> None:
        text = LITE_MODULE.read_text(encoding="utf-8")
        for rule_id in LITE_RULE_MODULES:
            if rule_id.startswith("LITE-"):
                self.assertIn(rule_id, text)

        for phrase in (
            "no more than three blocking questions",
            "approximately 500 tokens",
            "at most three short sentences",
            "Change Brief MUST target approximately 800 tokens",
            "three to five observable acceptance scenarios",
            "exactly one formal approval",
            "MUST NOT create or update workflow artifacts",
            "authentication or authorization",
            "payments",
            "data migration",
            "destructive data operations",
            "public contracts",
            "cross-module structural change",
            "concurrency or asynchronous behavior",
            "external side effects",
            "MUST pause further modification",
            "MUST NOT create or modify behavioral test files",
            "principal success path",
            "failure or boundary path",
            "known unresolved applicable validation failure",
            "compact, non-independent Review",
            "one batch",
            "explicitly approves",
            "normal completion report MUST target approximately 500 tokens",
            "no actionable findings",
            "MUST NOT create an empty correction gate",
            "MUST resolve mode again",
        ):
            self.assertIn(phrase, text)

    def test_orchestration_resolves_mode_before_full_gates(self) -> None:
        text = (CORE / "modules" / "orchestration.md").read_text(encoding="utf-8")
        mode_heading = "## Resolve the top-level workflow mode"
        full_heading = "## Route Full mode"
        lite_heading = "## Route Lite mode"
        self.assertIn("MODE-RESOLVE-001", text)
        self.assertIn("FULL-PRESERVE-001", text)
        self.assertLess(text.index(mode_heading), text.index(full_heading))
        self.assertLess(text.index(full_heading), text.index(lite_heading))
        for phrase in (
            "current-operation instruction",
            "project-scoped default",
            "user-scoped default",
            "`full` fallback",
            "MUST NOT persist a current-operation override",
            "first unmet condition",
            "lite-workflow.md",
        ):
            self.assertIn(phrase, text)

    def test_mode_resolution_distinguishes_absent_and_invalid_defaults(self) -> None:
        text = (CORE / "modules" / "orchestration.md").read_text(encoding="utf-8")
        for phrase in (
            "A valid explicit current-operation instruction wins",
            "Conflicting explicit instructions require clarification",
            "An absent project-scoped default continues to the user-scoped default",
            "A valid project-scoped default selects its mode",
            "A present but unreadable, malformed, missing-mode, or unsupported project-scoped default resolves to `full`",
            "An absent user-scoped default resolves to `full`",
            "A valid user-scoped default selects its mode",
            "A present but unreadable, malformed, missing-mode, or unsupported user-scoped default resolves to `full`",
        ):
            self.assertIn(phrase, text)

    def test_direct_stage_entry_does_not_imply_full_mode(self) -> None:
        text = (CORE / "modules" / "orchestration.md").read_text(encoding="utf-8")
        for phrase in (
            "Every public workflow entry is an operation",
            "Selecting a stage does not select `full`",
            "delegate to the adapter's canonical mode resolver",
            "apply a bounded direct-entry guard",
            "not complete mode-resolution ownership",
            "reuse a proven current-operation mode without resolving again",
            "stop the Full stage and route to Lite",
            "proven `full` mode",
        ):
            self.assertIn(phrase, text)

        statement = catalog_rules()["MODE-RESOLVE-001"]["statement"]
        self.assertIn("every public workflow entry", statement)
        self.assertIn("stage selection does not imply Full", statement)
        self.assertIn("bounded host-specific entry guard", statement)

        manifest = (CORE / "adapters" / "manifest-contract.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "every public workflow entry",
            "direct stage selection",
            "canonical mode resolver",
            "bounded direct-entry guard",
            "not complete mode-resolution ownership",
            "reuse a proven current-operation mode",
        ):
            self.assertIn(phrase, manifest.lower())

    def test_lite_rules_are_mandatory_and_require_adapter_mapping(self) -> None:
        rules = catalog_rules()
        for rule_id, module in LITE_RULE_MODULES.items():
            self.assertIn(rule_id, rules)
            self.assertIs(rules[rule_id]["mandatory"], True)
            self.assertEqual(rules[rule_id]["module"], module)

        manifest = (CORE / "adapters" / "manifest-contract.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("top-level modes `full` and `lite`", manifest)
        for rule_id in LITE_RULE_MODULES:
            self.assertIn(rule_id, manifest)

    def test_existing_full_modules_and_rules_remain_present(self) -> None:
        index = (CORE / "CORE.md").read_text(encoding="utf-8")
        for module in (
            "modules/requirements.md",
            "modules/project-knowledge.md",
            "modules/specification.md",
            "modules/ticket-planning.md",
            "modules/tdd-implementation.md",
            "modules/direct-implementation.md",
            "modules/review.md",
            "modules/architecture-improvement.md",
        ):
            self.assertIn(module, index)

        actual = set(catalog_rules())
        existing = {
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
        }
        self.assertTrue(existing.issubset(actual))


if __name__ == "__main__":
    unittest.main()
