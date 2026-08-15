import tempfile
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from build_release import compose_generic_workflow


ADAPTER = ROOT / "adapters" / "generic-prompts"
MANIFEST = ADAPTER / "manifest.yaml"
GENERIC_MODULES = [
    "bootstrap.md",
    "orchestration.md",
    "lite-workflow.md",
    "requirements.md",
    "documented-requirements.md",
    "specification.md",
    "ticket-planning.md",
    "direct-implementation.md",
    "tdd-implementation.md",
    "review.md",
    "architecture-improvement.md",
]
RESOLVER_MODULES = ("bootstrap.md", "orchestration.md")
FULL_STAGE_MODULES = (
    "requirements.md",
    "documented-requirements.md",
    "specification.md",
    "ticket-planning.md",
    "direct-implementation.md",
    "tdd-implementation.md",
    "review.md",
    "architecture-improvement.md",
)
STANDALONE_STAGE_MODULES = ("lite-workflow.md", *FULL_STAGE_MODULES)
LITE_RULES = {
    "MODE-RESOLVE-001",
    "FULL-PRESERVE-001",
    "LITE-QUESTIONS-001",
    "LITE-BRIEF-001",
    "LITE-RISK-001",
    "LITE-VALIDATE-001",
    "LITE-REVIEW-001",
    "LITE-SESSION-001",
}
MODE_EDIT_PERMISSION = (
    '<!-- GENERATED FILE — YOU MAY EDIT ONLY THE "Default workflow mode" '
    'DECLARATION BELOW -->'
)
UNQUALIFIED_EDIT_PROHIBITION = "<!-- GENERATED FILE — DO NOT EDIT -->"


def prompt(name: str) -> str:
    return (ADAPTER / name).read_text(encoding="utf-8")


def composed_workflow() -> str:
    config = {
        "display_name": "Ask Then Do It",
        "release_version": "1.3.0",
        "core_version": "1.3.0",
        "generic": {"modules": GENERIC_MODULES},
    }
    return compose_generic_workflow(config, ADAPTER).decode("utf-8")


class GenericLiteCompositionTests(unittest.TestCase):
    def test_generated_workflow_allows_only_default_mode_declaration_edits(self) -> None:
        combined = composed_workflow()
        declaration = "Default workflow mode: full"

        self.assertIn(MODE_EDIT_PERMISSION, combined)
        self.assertLess(combined.index(MODE_EDIT_PERMISSION), combined.index(declaration))
        self.assertNotIn(UNQUALIFIED_EDIT_PROHIBITION, combined)

    def test_generated_workflow_has_one_early_full_default_declaration(self) -> None:
        config = {
            "display_name": "Ask Then Do It",
            "release_version": "1.3.0",
            "core_version": "1.3.0",
            "generic": {
                "modules": [
                    "bootstrap.md",
                    "orchestration.md",
                    "lite-workflow.md",
                    "requirements.md",
                ]
            },
        }

        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            for name in config["generic"]["modules"]:
                (source / name).write_text(f"# {name}\n", encoding="utf-8")
            combined = compose_generic_workflow(config, source).decode("utf-8")

        declaration = "Default workflow mode: full"
        self.assertEqual(combined.splitlines().count(declaration), 1)
        self.assertLess(combined.index(declaration), combined.index("## Internal routing contract"))

    def test_in_memory_inventory_composes_lite_immediately_after_orchestration(self) -> None:
        combined = composed_workflow()

        orchestration = "<!-- BEGIN SOURCE: orchestration.md -->"
        lite = "<!-- BEGIN SOURCE: lite-workflow.md -->"
        requirements = "<!-- BEGIN SOURCE: requirements.md -->"
        self.assertLess(combined.index(orchestration), combined.index(lite))
        self.assertLess(combined.index(lite), combined.index(requirements))
        self.assertEqual(combined.splitlines().count("Default workflow mode: full"), 1)

    def test_combined_one_question_instruction_is_scoped_to_resolved_full(self) -> None:
        combined = composed_workflow()

        self.assertIn("For a fresh resolved Full workflow", combined)
        self.assertNotIn(
            "For a fresh workflow whose first unmet stage is requirement consensus",
            combined,
        )
        self.assertIn("no more than three blocking questions", prompt("lite-workflow.md"))


class GenericLiteRoutingTests(unittest.TestCase):
    def test_mode_resolution_uses_instruction_then_declaration_then_full_fallback(self) -> None:
        routing = prompt("bootstrap.md") + "\n" + prompt("orchestration.md")

        ordered_markers = (
            "explicit current-operation instruction",
            "embedded `Default workflow mode` declaration",
            "Full fallback",
        )
        positions = [routing.index(marker) for marker in ordered_markers]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("missing or invalid", routing)
        self.assertIn("conflicting", routing)
        self.assertIn("clarification", routing)
        self.assertIn("only the current operation", routing)
        self.assertIn("MUST NOT persist", routing)

    def test_generic_routing_does_not_claim_host_specific_config_access(self) -> None:
        texts = "\n".join(
            prompt(name)
            for name in ("bootstrap.md", "orchestration.md", "lite-workflow.md")
        )
        lowered = texts.lower()

        for forbidden in ("codex", ".codex", "user config", "project config"):
            self.assertNotIn(forbidden, lowered)

    def test_resolved_full_preserves_existing_order_gates_and_ticket_modes(self) -> None:
        routing = prompt("orchestration.md")

        self.assertIn("Resolved Full", routing)
        for marker in (
            "requirement consensus",
            "Approved Specification",
            "Approved Ticket Plan",
            "Approved `tdd` Ticket",
            "Approved `direct` Ticket",
            "evidence-based review",
            "architecture-improvement.md",
        ):
            self.assertIn(marker, routing)
        self.assertIn("FULL-PRESERVE-001", routing)


class GenericDirectEntryModeTests(unittest.TestCase):
    def test_all_public_modules_treat_direct_paste_as_stage_selection(self) -> None:
        for name in GENERIC_MODULES:
            with self.subTest(module=name):
                text = prompt(name)
                self.assertIn(
                    "Directly pasting this module selects its workflow stage, "
                    "not Full or Lite.",
                    text,
                )
                self.assertIn("MODE-RESOLVE-001", text)

    def test_all_public_modules_cover_the_direct_entry_resolution_matrix(self) -> None:
        ordered_markers = (
            "unambiguous explicit current-operation instruction",
            "embedded `Default workflow mode` declaration",
            "Full fallback",
        )

        for name in GENERIC_MODULES:
            with self.subTest(module=name):
                text = prompt(name)
                for marker in ordered_markers:
                    self.assertIn(marker, text)
                positions = [text.index(marker) for marker in ordered_markers]
                self.assertEqual(positions, sorted(positions))
                self.assertIn("exactly `full` or `lite`", text)
                self.assertIn("missing or invalid", text)
                self.assertIn("explicit current-operation instructions conflict", text)
                self.assertIn("clarification", text)
                self.assertIn("only the current operation", text)
                self.assertIn("MUST NOT persist", text)

    def test_complete_resolvers_and_bounded_stage_guards_have_distinct_ownership(
        self,
    ) -> None:
        for name in RESOLVER_MODULES:
            with self.subTest(module=name):
                text = prompt(name)
                self.assertIn("owns complete top-level mode resolution", text)
                self.assertNotIn(
                    "bounded direct-entry guard, not complete resolver ownership",
                    text,
                )
                self.assertIn("Route resolved Lite", text)
                self.assertIn("resolved Full", text)

        for name in STANDALONE_STAGE_MODULES:
            with self.subTest(module=name):
                text = prompt(name)
                self.assertIn(
                    "bounded direct-entry guard, not complete resolver ownership",
                    text,
                )
                self.assertNotIn("owns complete top-level mode resolution", text)

    def test_bounded_guards_reuse_proven_mode_before_direct_entry_resolution(
        self,
    ) -> None:
        reuse = (
            "When composed orchestration supplies a proven current-operation mode, "
            "reuse it and MUST NOT re-resolve."
        )
        unresolved_direct_entry = (
            "Only when directly pasted without a proven current-operation mode, "
            "resolve"
        )

        for name in STANDALONE_STAGE_MODULES:
            with self.subTest(module=name):
                text = prompt(name)
                self.assertIn(reuse, text)
                self.assertIn(unresolved_direct_entry, text)
                self.assertLess(text.index(reuse), text.index(unresolved_direct_entry))
                self.assertNotIn("Before applying it, resolve", text)

    def test_direct_full_stages_route_lite_and_require_proven_full(self) -> None:
        for name in FULL_STAGE_MODULES:
            with self.subTest(module=name):
                text = prompt(name)
                self.assertIn("If Lite resolves", text)
                self.assertIn("stop this Full stage", text)
                self.assertIn("route to `lite-workflow.md`", text)
                self.assertIn("Continue this stage only when Full resolves", text)

    def test_direct_lite_stage_routes_full_and_requires_proven_lite(self) -> None:
        text = prompt("lite-workflow.md")

        self.assertIn("If Full resolves", text)
        self.assertIn("stop this Lite stage", text)
        self.assertIn("route to Full orchestration in `orchestration.md`", text)
        self.assertIn("Continue this stage only when Lite resolves", text)


class GenericLitePromptContractTests(unittest.TestCase):
    def test_lite_questions_and_change_brief_have_approved_budgets_and_gate(self) -> None:
        text = prompt("lite-workflow.md")

        for marker in (
            "no more than three blocking questions",
            "approximately 500 tokens for the complete batch",
            "at most three short sentences",
            "one decision",
            "one concrete recommendation",
            "principal tradeoff",
            "approximately 800 tokens",
            "exactly one formal pre-implementation approval",
        ):
            self.assertIn(marker, text)
        for section in (
            "objective",
            "in-scope behavior",
            "explicit non-goals",
            "three to five observable acceptance scenarios",
            "material risks",
            "intended validation",
        ):
            self.assertIn(section, text)

    def test_lite_reconsiders_material_risk_only_for_current_operation(self) -> None:
        text = prompt("lite-workflow.md")

        for category in (
            "authentication",
            "authorization",
            "payment",
            "data migration",
            "destructive data operation",
            "public contract",
            "cross-module structural change",
            "concurrency",
            "asynchronous behavior",
            "external side effect",
        ):
            self.assertIn(category, text)
        self.assertIn("before Change Brief approval", text)
        self.assertIn("after approval or during implementation", text)
        self.assertIn("stop further implementation guidance", text)
        self.assertIn("only the current operation", text)
        self.assertIn("MUST NOT change the embedded default declaration", text)

    def test_lite_prohibits_workflow_artifacts_new_tests_and_tdd_claims(self) -> None:
        text = prompt("lite-workflow.md")

        for artifact in (
            "Requirement Decision Record",
            "Draft Working Notes",
            "Project Knowledge Base",
            "Specification",
            "Ticket Plan",
            "Implementation Evidence",
            "Direct Implementation Evidence",
            "Review Report",
            "Architecture Improvement Report",
        ):
            self.assertIn(artifact, text)
        self.assertIn("MUST NOT create or modify behavioral tests", text)
        self.assertIn("MUST NOT require or claim Red, Green, Refactor", text)

    def test_lite_capability_boundary_uses_unexecuted_guidance_without_overclaims(self) -> None:
        text = prompt("lite-workflow.md")

        for marker in (
            "UNEXECUTED IMPLEMENTATION GUIDANCE",
            "MUST NOT claim repository inspection or file changes",
            "MUST NOT claim command or test execution",
            "MUST NOT claim durable persistence",
            "MUST NOT claim observed validation without supplied evidence",
            "MUST NOT claim independent Review",
        ):
            self.assertIn(marker, text)

    def test_lite_validation_covers_static_success_failure_and_known_failures(self) -> None:
        text = prompt("lite-workflow.md")

        for marker in (
            "status and diff",
            "syntax, lint, type-check, build, configuration, schema",
            "principal success path",
            "most important failure or boundary path",
            "MUST NOT run a complete behavioral suite by default",
            "known unresolved applicable failure",
        ):
            self.assertIn(marker, text)

    def test_lite_review_batches_findings_before_approved_correction(self) -> None:
        text = prompt("lite-workflow.md")

        for marker in (
            "compact, non-independent Review",
            "Change Brief coverage",
            "diff and file scope",
            "principal failure and boundary paths",
            "security-sensitive behavior and sensitive information",
            "observed and unavailable validation",
            "residual risk",
            "one complete batch",
            "explicitly approves the batch",
            "material scope expansion",
            "no actionable findings",
            "MUST NOT create an empty correction gate",
        ):
            self.assertIn(marker, text)
        self.assertIn("MUST NOT require the Full twelve-lens pass", text)

    def test_lite_completion_and_session_state_remain_evidence_honest(self) -> None:
        text = prompt("lite-workflow.md")

        for marker in (
            "approximately 500 tokens",
            "delivered behavior",
            "changed files or ownership areas",
            "observed validation and outcomes",
            "unavailable checks",
            "unresolved findings",
            "residual risks",
            "not durable cross-session state",
            "MUST resolve mode again",
            "MUST NOT claim to resume",
        ):
            self.assertIn(marker, text)

    def test_manifest_maps_all_new_rules_to_conversation_evidence(self) -> None:
        manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))

        self.assertTrue(LITE_RULES.issubset(set(manifest["implemented_rules"])))
        evidence = manifest["capability_evidence"]["conversation"]
        self.assertIn("adapters/generic-prompts/lite-workflow.md", evidence)
        self.assertIn("tests/generic/test_generic_lite_workflow.py", evidence)


if __name__ == "__main__":
    unittest.main()
