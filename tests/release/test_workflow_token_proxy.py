import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "measure_workflow_token_proxy.py"
FIXTURE_ROOT = (
    ROOT / "tests" / "release" / "fixtures" / "workflow-token-proxy"
)
FIXTURE = FIXTURE_ROOT / "benchmark.json"
EXPECTED_CATEGORIES = [
    "selected-instructions",
    "questions",
    "scope-and-planning",
    "handoffs",
    "implementation-validation",
    "review-completion",
]
EXPECTED_INSTRUCTIONS = {
    "full": [
        "adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md",
        "adapters/codex/plugin/ask-then-do-it/skills/ask-with-docs/SKILL.md",
        "adapters/codex/plugin/ask-then-do-it/skills/write-spec/SKILL.md",
        "adapters/codex/plugin/ask-then-do-it/skills/plan-tickets/SKILL.md",
        "adapters/codex/plugin/ask-then-do-it/skills/implement-tdd/SKILL.md",
        "adapters/codex/plugin/ask-then-do-it/skills/review-code/SKILL.md",
    ],
    "lite": [
        "adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md",
        "adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/references/lite-workflow.md",
    ],
}
EXPECTED_GENERIC_MODULES = [
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


def run_proxy(fixture: Path = FIXTURE) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--fixture", str(fixture), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def read_fixture() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def write_fixture(path: Path, data: dict[str, object]) -> None:
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def event(data: dict[str, object], mode: str, event_id: str) -> dict[str, object]:
    modes = data["modes"]
    assert isinstance(modes, dict)
    mode_data = modes[mode]
    assert isinstance(mode_data, dict)
    events = mode_data["events"]
    assert isinstance(events, list)
    return next(item for item in events if item["id"] == event_id)


def load_proxy_module():
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import measure_workflow_token_proxy

    return measure_workflow_token_proxy


class WorkflowTokenProxyTests(unittest.TestCase):
    def assert_schema_error(
        self, data: dict[str, object], expected: str
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            fixture = Path(temporary) / "benchmark.json"
            write_fixture(fixture, data)
            result = run_proxy(fixture)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn(expected, result.stderr)
        return result

    def build_report_with_proxy_counts(
        self, full: int, lite: int
    ) -> dict[str, object]:
        proxy = load_proxy_module()
        modes = {
            "full": {"proxy_tokens": full},
            "lite": {"proxy_tokens": lite},
        }
        with (
            mock.patch.object(proxy, "measure_modes", return_value=(modes, [])),
            mock.patch.object(
                proxy,
                "measure_generic",
                return_value=({"gate_applied": False}, b"generic"),
            ),
        ):
            return proxy.build_report(FIXTURE)

    def test_representative_codex_fixture_passes_sixty_percent_gate(self) -> None:
        result = run_proxy()

        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        gate = report["codex"]["gate"]
        full = report["codex"]["full"]["proxy_tokens"]
        lite = report["codex"]["lite"]["proxy_tokens"]
        self.assertTrue(gate["passed"])
        self.assertGreaterEqual(gate["reduction_basis_points"], 6000)
        self.assertLessEqual(lite * 100, full * 40)
        self.assertEqual(report["codex"]["difference_proxy_tokens"], full - lite)
        self.assertEqual(gate["formula"], "(full - lite) / full * 100")
        self.assertEqual(
            (
                full,
                lite,
                report["codex"]["difference_proxy_tokens"],
                gate["reduction_basis_points"],
            ),
            (14771, 5480, 9291, 6290),
        )

    def test_output_is_deterministic_and_discloses_algorithm_and_fixture(self) -> None:
        first = run_proxy()
        second = run_proxy()

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, second.stdout)
        report = json.loads(first.stdout)
        self.assertEqual(report["algorithm"]["id"], "normalized-utf8-quarter-v1")
        self.assertEqual(report["algorithm"]["bytes_per_proxy_token"], 4)
        self.assertFalse(report["algorithm"]["billing_guarantee"])
        self.assertRegex(report["fixture"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertNotIn(str(ROOT), first.stdout)

    def test_fixture_uses_one_conservative_scenario_and_exact_event_inventory(self) -> None:
        data = read_fixture()
        scenario = data["scenario"]
        self.assertEqual(scenario["host"], "codex")
        self.assertEqual(scenario["capability"], "tools")
        self.assertEqual(scenario["ticket_count"], 1)
        self.assertEqual(scenario["review_finding_count"], 0)
        self.assertIs(scenario["architecture_diagnosis"], False)
        self.assertEqual(data["controlled_categories"], EXPECTED_CATEGORIES)

        expected_ids = {
            "full": {
                "full-orchestrator",
                "full-documented-requirements",
                "full-write-spec",
                "full-plan-tickets",
                "full-implement-tdd",
                "full-review-code",
                "full-questions",
                "full-scope-and-planning",
                "full-handoffs",
                "full-implementation-evidence",
                "full-review",
                "full-completion",
            },
            "lite": {
                "lite-orchestrator",
                "lite-workflow-reference",
                "lite-questions",
                "lite-change-brief",
                "lite-handoffs",
                "lite-implementation-validation",
                "lite-review",
                "lite-completion",
            },
        }
        for mode in ("full", "lite"):
            events = data["modes"][mode]["events"]
            self.assertEqual({item["id"] for item in events}, expected_ids[mode])
            self.assertEqual(
                [
                    item["source"]
                    for item in events
                    if item["category"] == "selected-instructions"
                ],
                EXPECTED_INSTRUCTIONS[mode],
            )
            self.assertEqual(
                {item["category"] for item in events}, set(EXPECTED_CATEGORIES)
            )

    def test_lite_budgeted_outputs_stay_within_500_800_500(self) -> None:
        result = run_proxy()
        self.assertEqual(result.returncode, 0, result.stderr)
        budgets = json.loads(result.stdout)["codex"]["lite"]["budgets"]

        self.assertEqual(
            {name: item["limit"] for name, item in budgets.items()},
            {"change-brief": 800, "completion": 500, "questions": 500},
        )
        self.assertTrue(all(item["passed"] for item in budgets.values()))
        self.assertTrue(
            all(item["proxy_tokens"] <= item["limit"] for item in budgets.values())
        )

    def test_lite_budget_labels_cannot_move_to_different_events(self) -> None:
        data = read_fixture()
        event(data, "lite", "lite-review")["budget"] = "completion"
        event(data, "lite", "lite-completion")["budget"] = None

        self.assert_schema_error(data, "completion budget must belong to lite-completion")

    def test_lite_growth_below_threshold_fails_without_changing_threshold(self) -> None:
        report = self.build_report_with_proxy_counts(full=10000, lite=4001)
        self.assertFalse(report["codex"]["gate"]["passed"])
        self.assertLess(report["codex"]["gate"]["reduction_basis_points"], 6000)
        self.assertEqual(
            report["codex"]["gate"]["minimum_reduction_basis_points"], 6000
        )

    def test_event_contract_rejects_redirected_sources_for_both_modes(self) -> None:
        mutations = (
            (
                "full",
                "full-questions",
                "tests/release/fixtures/workflow-token-proxy/lite/questions.md",
            ),
            (
                "lite",
                "lite-implementation-validation",
                "tests/release/fixtures/workflow-token-proxy/full/implementation-evidence.md",
            ),
        )
        for mode, event_id, source in mutations:
            with self.subTest(mode=mode, event_id=event_id):
                data = read_fixture()
                event(data, mode, event_id)["source"] = source
                self.assert_schema_error(
                    data, f"{mode} event contract does not match the fixed benchmark"
                )

    def test_event_contract_rejects_category_redirection(self) -> None:
        data = read_fixture()
        event(data, "full", "full-completion")["category"] = (
            "implementation-validation"
        )

        self.assert_schema_error(
            data, "full event contract does not match the fixed benchmark"
        )

    def test_replayed_full_output_cannot_manufacture_a_passing_gate(self) -> None:
        data = read_fixture()
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            lite_growth = root / "lite-growth.md"
            full_replay = root / "unrelated-full-source.md"
            original = (
                FIXTURE_ROOT / "lite" / "implementation-validation.md"
            ).read_text(encoding="utf-8")
            lite_growth.write_text(
                original + (" workflow growth" * 5000), encoding="utf-8"
            )
            full_replay.write_text(
                " unrelated full source" * 5000, encoding="utf-8"
            )
            event(data, "lite", "lite-implementation-validation")["source"] = (
                lite_growth.relative_to(ROOT).as_posix()
            )
            for full_event in data["modes"]["full"]["events"]:
                if full_event["category"] != "selected-instructions":
                    full_event["source"] = full_replay.relative_to(ROOT).as_posix()
            fixture = root / "benchmark.json"
            write_fixture(fixture, data)

            result = run_proxy(fixture)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn(
            "full event contract does not match the fixed benchmark", result.stderr
        )

    def test_signed_reduction_percentage_when_lite_exceeds_full(self) -> None:
        cases = (
            (-6109, "-61.09"),
            (-101, "-1.01"),
            (-1, "-0.01"),
            (0, "0.00"),
            (6109, "61.09"),
        )
        for basis_points, expected in cases:
            with self.subTest(basis_points=basis_points):
                report = self.build_report_with_proxy_counts(
                    full=10000, lite=10000 - basis_points
                )
                gate = report["codex"]["gate"]
                self.assertEqual(gate["reduction_basis_points"], basis_points)
                self.assertEqual(gate["reduction_percent"], expected)

    def test_threshold_is_not_fixture_configurable(self) -> None:
        data = read_fixture()
        data["minimum_reduction_basis_points"] = 1

        self.assert_schema_error(data, "unknown")

    def test_mode_specific_exclusions_are_rejected(self) -> None:
        data = read_fixture()
        data["modes"]["lite"]["exclusions"] = []

        self.assert_schema_error(data, "unknown")

    def test_shared_task_facts_are_excluded_equally(self) -> None:
        baseline = run_proxy()
        self.assertEqual(baseline.returncode, 0, baseline.stderr)
        expected = json.loads(baseline.stdout)["codex"]
        data = read_fixture()
        data["scenario"]["task"] += " shared task source" * 2000

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            fixture = Path(temporary) / "benchmark.json"
            write_fixture(fixture, data)
            changed = run_proxy(fixture)

        self.assertEqual(changed.returncode, 0, changed.stderr)
        actual = json.loads(changed.stdout)["codex"]
        self.assertEqual(actual["full"]["proxy_tokens"], expected["full"]["proxy_tokens"])
        self.assertEqual(actual["lite"]["proxy_tokens"], expected["lite"]["proxy_tokens"])

    def test_normalization_is_stable_for_unicode_line_endings_and_whitespace(self) -> None:
        proxy = load_proxy_module()
        first = proxy.measure_normalized_parts(
            [proxy.normalize("Cafe\u0301\r\nnext\tline")]
        )
        second = proxy.measure_normalized_parts(
            [proxy.normalize("Caf\u00e9 next line")]
        )

        self.assertEqual(first, second)

    def test_duplicate_event_id_is_rejected(self) -> None:
        data = read_fixture()
        event(data, "lite", "lite-completion")["id"] = "lite-review"

        self.assert_schema_error(data, "Duplicate event id")

    def test_missing_traversal_absolute_and_non_utf8_sources_are_rejected(self) -> None:
        mutations = {
            "missing": "tests/release/fixtures/workflow-token-proxy/missing.md",
            "traversal": "../outside.md",
            "absolute": str((ROOT / "README.md").resolve()),
        }
        for label, source in mutations.items():
            with self.subTest(label=label):
                data = read_fixture()
                event(data, "lite", "lite-completion")["source"] = source
                self.assert_schema_error(data, "source")

        data = read_fixture()
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            invalid = root / "invalid.md"
            invalid.write_bytes(b"\xff\xfe\x00")
            event(data, "lite", "lite-completion")["source"] = (
                invalid.relative_to(ROOT).as_posix()
            )
            fixture = root / "benchmark.json"
            write_fixture(fixture, data)
            result = run_proxy(fixture)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("UTF-8", result.stderr)

    def test_generic_full_composed_prompt_fixed_cost_is_reported_separately(self) -> None:
        result = run_proxy()
        self.assertEqual(result.returncode, 0, result.stderr)
        generic = json.loads(result.stdout)["generic"]

        self.assertIs(generic["gate_applied"], False)
        self.assertEqual(generic["applies_equally_to"], ["full", "lite"])
        self.assertEqual(
            generic["composed_prompt"]["source_modules"], EXPECTED_GENERIC_MODULES
        )
        self.assertGreater(generic["composed_prompt"]["proxy_tokens"], 0)
        self.assertRegex(generic["composed_prompt"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertFalse(any("reduction" in key for key in generic))
        self.assertIn("fixed cost", generic["limitation"])
        self.assertIn("no Generic 60% guarantee", generic["limitation"])
        self.assertIn("no billing guarantee", generic["limitation"])

    def test_generic_source_must_be_the_canonical_prompt_directory(self) -> None:
        data = read_fixture()
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            alternate = root / "generic-prompts"
            alternate.mkdir()
            for index, name in enumerate(EXPECTED_GENERIC_MODULES):
                content = "filler alternate sources!\n" if index == 0 else "filler\n"
                (alternate / name).write_text(content, encoding="utf-8")
            data["generic_composed_prompt"]["source"] = (
                alternate.relative_to(ROOT).as_posix()
            )
            fixture = root / "benchmark.json"
            write_fixture(fixture, data)

            result = run_proxy(fixture)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn(
            "fixture.generic_composed_prompt.source must equal "
            "adapters/generic-prompts",
            result.stderr,
        )

    def test_generic_report_hashes_the_actual_builder_composition(self) -> None:
        scripts = str(ROOT / "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        from build_release import compose_generic_workflow

        data = read_fixture()
        config = json.loads((ROOT / "release" / "release.json").read_text(encoding="utf-8"))
        config = copy.deepcopy(config)
        modules = data["generic_composed_prompt"]["module_order"]
        config["generic"]["modules"] = modules
        source = ROOT / data["generic_composed_prompt"]["source"]
        expected = compose_generic_workflow(config, source)

        result = run_proxy()
        self.assertEqual(result.returncode, 0, result.stderr)
        actual_hash = json.loads(result.stdout)["generic"]["composed_prompt"]["sha256"]
        self.assertEqual(actual_hash, hashlib.sha256(expected).hexdigest())


if __name__ == "__main__":
    unittest.main()
