"""Exercise the offline calculator; synthetic data is never model evidence."""

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/measure_claude_context.py"


def digest(data):
    return hashlib.sha256(data).hexdigest()


class ClaudeContextProxyTests(unittest.TestCase):
    def tool(self):
        self.assertTrue(SCRIPT.is_file(), "Claude context calculator is not implemented")
        spec = importlib.util.spec_from_file_location("claude_context_under_test", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def fixture(self, directory):
        tool = self.tool()
        fixture = tool.prepare_template()
        fixture["evidence_kind"] = "synthetic"
        fixture["capture_review"] = "synthetic calculator test, not a model run"
        for case in fixture["scenarios"]:
            for field in ("task", "stage_outcome"):
                data = (case["id"] + " " + field).encode()
                name = case["id"] + "-" + field + ".txt"
                (directory / name).write_bytes(data)
                case[field] = {"path": name, "sha256": digest(data)}
            case["capability"] = "multi_agent" if case["id"] == "full-review" else "tools"
            for profile, checkpoints in case["profiles"].items():
                for checkpoint, record in checkpoints.items():
                    record["capture_complete"] = True
                    record["events"] = []
                    for n, (kind, origin) in enumerate(tool.required_material(case["id"], profile, checkpoint)):
                        data = ("g" * 60 if profile == "general" else "c" * 10).encode()
                        name = f'{case["id"]}-{profile}-{checkpoint}-{n}.txt'
                        (directory / name).write_bytes(data)
                        record["events"].append({"kind": kind, "origin": origin, "path": name, "sha256": digest(data)})
        path = directory / "capture.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        return tool, fixture, path

    def test_normalization_and_ceil_are_exact(self):
        tool = self.tool()
        result = tool.measure_texts([" e\u0301\t  x \r\n", " a\u00a0 b "])
        self.assertEqual(result, {"normalized_bytes": 8, "proxy_tokens": 2})
        self.assertEqual(tool.measure_texts(["12345"])["proxy_tokens"], 2)
        self.assertEqual(tool.measure_texts(["a", "a"])["normalized_bytes"], 3)
        self.assertTrue(tool.threshold(3, 1))
        self.assertFalse(tool.threshold(3, 2))
        with self.assertRaises(ValueError):
            tool.threshold(0, 0)

    def test_prepared_capture_is_unexecuted_and_incomplete(self):
        tool = self.tool()
        template = tool.prepare_template()
        self.assertEqual(template["evidence_kind"], "unobserved")
        self.assertEqual(len(template["scenarios"]), 10)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "capture.json"
            path.write_text(json.dumps(template), encoding="utf-8")
            result = tool.evaluate(path, synthetic=True)
            self.assertFalse(result["release_pass"])
            self.assertTrue(result["errors"])
            self.assertEqual(result["measurements"], [])

    def test_preview_runtime_route_rejects_stable_identity_without_changing_target(self):
        tool = self.tool()
        self.assertEqual(tool.prepare_template()["version"], "1.4.0")
        for profile in ("general", "claude-5"):
            envelope = {
                "plugin": "ask-then-do-it", "version": "1.4.0-preview.1",
                "entry": "/ask-then-do-it:ask-then-do-it", "operation_id": "op_" + "a" * 32,
                "model_classification": "supported-non-5" if profile == "general" else "claude-5",
                "selected_profile": profile, "routing_status": "ready", "disclosure_code": "none",
            }
            def framed():
                return "ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1\n" + json.dumps(envelope) + "\nEND_ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1"
            tool.validate_route_text(framed(), profile)
            for wrong_version in ("1.4.0", "1.3.1", "1.4.0-preview.2"):
                envelope["version"] = wrong_version
                with self.subTest(profile=profile, wrong_version=wrong_version):
                    with self.assertRaisesRegex(ValueError, "route identity"):
                        tool.validate_route_text(framed(), profile)

    def test_synthetic_measurement_is_deterministic_and_never_release_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            tool, fixture, path = self.fixture(Path(temp))
            first = tool.evaluate(path, synthetic=True)
            self.assertEqual(first, tool.evaluate(path, synthetic=True))
            self.assertEqual(first["errors"], [])
            self.assertEqual(len(first["measurements"]), 11)
            self.assertTrue(all(row["threshold_pass"] for row in first["measurements"]))
            self.assertFalse(first["release_pass"])
            self.assertEqual(first["status"], "synthetic-only")

    def test_production_measurement_requires_behavior_first(self):
        with tempfile.TemporaryDirectory() as temp:
            tool, fixture, path = self.fixture(Path(temp))
            fixture["evidence_kind"] = "observed"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            with mock.patch.object(tool, "measure_texts", side_effect=AssertionError("must not measure before behavior gate")):
                result = tool.evaluate(path)
            self.assertTrue(result["errors"])
            self.assertFalse(result["release_pass"])
            self.assertEqual(result["measurements"], [])
            fake = Path(temp) / "fake-behavior.json"
            fake.write_text('{"passed":true}', encoding="utf-8")
            with mock.patch.object(tool, "measure_texts", side_effect=AssertionError("must reject fake behavior evidence")):
                result = tool.evaluate(path, behavior_evidence=fake)
            self.assertTrue(result["errors"])

    def test_inventory_hash_path_and_exclusion_corruption_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            tool, fixture, path = self.fixture(Path(temp))
            def record(data):
                return data["scenarios"][0]["profiles"]["general"]["stage-ready"]
            mutations = [
                lambda f: f["scenarios"].pop(),
                lambda f: f["scenarios"].append(copy.deepcopy(f["scenarios"][0])),
                lambda f: record(f)["events"].pop(),
                lambda f: record(f)["events"][0].update(sha256="0" * 64),
                lambda f: record(f)["events"][0].update(path="../outside.txt"),
                lambda f: record(f)["events"][0].update(origin="profiles/claude-5/orchestration.md"),
                lambda f: record(f)["events"][0].update(kind="host-system"),
                lambda f: record(f).update(capture_complete=False),
                lambda f: f["scenarios"][0]["profiles"]["claude-5"].update(unexpected={}),
                lambda f: f["scenarios"][0].update(capability="unknown"),
            ]
            for mutation in mutations:
                candidate = copy.deepcopy(fixture)
                mutation(candidate)
                path.write_text(json.dumps(candidate), encoding="utf-8")
                with self.subTest(mutation=mutation):
                    result = tool.evaluate(path, synthetic=True)
                    self.assertTrue(result["errors"])
                    self.assertFalse(result["release_pass"])

    def test_duplicates_count_and_one_failing_checkpoint_cannot_be_averaged(self):
        with tempfile.TemporaryDirectory() as temp:
            tool, fixture, path = self.fixture(Path(temp))
            before = tool.evaluate(path, synthetic=True)["measurements"][0]
            record = fixture["scenarios"][0]["profiles"]["claude-5"]["stage-ready"]
            record["events"] += [copy.deepcopy(record["events"][0])] * 40
            path.write_text(json.dumps(fixture), encoding="utf-8")
            result = tool.evaluate(path, synthetic=True)
            self.assertEqual(result["errors"], [])
            self.assertFalse(result["measurements"][0]["threshold_pass"])
            self.assertGreater(result["measurements"][0]["claude-5"]["proxy_tokens"], before["claude-5"]["proxy_tokens"])
            self.assertTrue(all(row["threshold_pass"] for row in result["measurements"][1:]))

    def test_cli_preparation_refuses_overwrite_and_synthetic_is_labelled(self):
        with tempfile.TemporaryDirectory() as temp:
            tool, fixture, path = self.fixture(Path(temp))
            prepared = Path(temp) / "prepared.json"
            base = [sys.executable, "-B", str(SCRIPT)]
            first = subprocess.run(base + ["--prepare", str(prepared)], capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = prepared.read_bytes()
            second = subprocess.run(base + ["--prepare", str(prepared)], capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(prepared.read_bytes(), before)
            measured = subprocess.run(base + ["--fixture", str(path), "--synthetic", "--json"], capture_output=True, text=True)
            self.assertEqual(measured.returncode, 0, measured.stderr)
            self.assertFalse(json.loads(measured.stdout)["release_pass"])

    def test_reviewer_checkpoint_cannot_drop_previous_injections(self):
        with tempfile.TemporaryDirectory() as temp:
            tool, fixture, path = self.fixture(Path(temp))
            case = next(case for case in fixture["scenarios"] if case["id"] == "full-review")
            stage = case["profiles"]["general"]["stage-ready"]
            stage["events"].append(copy.deepcopy(stage["events"][0]))
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertTrue(tool.evaluate(path, synthetic=True)["errors"])

    def test_additional_same_profile_stage_is_counted_and_cross_profile_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            tool, fixture, path = self.fixture(Path(temp))
            before = tool.evaluate(path, synthetic=True)["measurements"][0]["general"]["proxy_tokens"]
            record = fixture["scenarios"][0]["profiles"]["general"]["stage-ready"]
            event = {**record["events"][-1], "origin": "profiles/general/requirements.md"}
            record["events"].append(event)
            path.write_text(json.dumps(fixture), encoding="utf-8")
            result = tool.evaluate(path, synthetic=True)
            self.assertEqual(result["errors"], [])
            self.assertGreater(result["measurements"][0]["general"]["proxy_tokens"], before)
            event["origin"] = "profiles/claude-5/requirements.md"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertTrue(tool.evaluate(path, synthetic=True)["errors"])

    def test_reordering_stage_sources_and_asymmetric_exclusions_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            tool, fixture, path = self.fixture(Path(temp))
            record = fixture["scenarios"][0]["profiles"]["general"]["stage-ready"]
            record["events"][2], record["events"][3] = record["events"][3], record["events"][2]
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertTrue(tool.evaluate(path, synthetic=True)["errors"])
            record["events"][2], record["events"][3] = record["events"][3], record["events"][2]
            record["events"].append({**record["events"][0], "kind": "host-system", "origin": "host-system"})
            path.write_text(json.dumps(fixture), encoding="utf-8")
            self.assertTrue(tool.evaluate(path, synthetic=True)["errors"])

    def test_observed_source_padding_and_capture_trace_changes_are_rejected(self):
        """Mock only prior behavior acceptance; host captures are unit-test data."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            tool, fixture, path = self.fixture(root)
            fixture["evidence_kind"] = "observed"
            plugin = root / "plugin"
            for case in fixture["scenarios"]:
                for profile, checkpoints in case["profiles"].items():
                    for checkpoint, record in checkpoints.items():
                        for event in record["events"]:
                            if event["kind"] in tool.FILE_KINDS:
                                canonical = plugin / event["origin"]
                                canonical.parent.mkdir(parents=True, exist_ok=True)
                                text = "same tiny source\n"
                                description = "same description"
                                if event["kind"] in {"public-skill", "reviewer-description", "reviewer-prompt"}:
                                    canonical.write_text(f"---\ndescription: {description}\n---\n{text}", encoding="utf-8")
                                    text = description if event["kind"] == "reviewer-description" else text
                                else:
                                    canonical.write_text(text, encoding="utf-8")
                            else:
                                text = "ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1\n" + json.dumps({
                                    "plugin": "ask-then-do-it", "version": "1.4.0-preview.1",
                                    "entry": "/ask-then-do-it:ask-then-do-it", "operation_id": "op_" + "a" * 32,
                                    "model_classification": "supported-non-5" if profile == "general" else "claude-5",
                                    "selected_profile": profile, "routing_status": "ready", "disclosure_code": "none",
                                }) + "\nEND_ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1"
                            raw = text.encode()
                            (root / event["path"]).write_bytes(raw)
                            event["sha256"] = digest(raw)
                        trace = {"scenario": case["id"], "profile": profile, "checkpoint": checkpoint, "events": record["events"]}
                        raw = json.dumps(trace).encode()
                        name = f'{case["id"]}-{profile}-{checkpoint}-trace.json'
                        (root / name).write_bytes(raw)
                        record["trace"] = {"path": name, "sha256": digest(raw)}
            path.write_text(json.dumps(fixture), encoding="utf-8")
            behavior = root / "prior-behavior.json"
            behavior.write_text("unit-test stub", encoding="utf-8")
            with mock.patch.object(tool, "behavior_errors", return_value=[]):
                result = tool.evaluate(path, behavior_evidence=behavior, plugin_root=plugin)
                self.assertEqual(result["errors"], [])
                self.assertEqual(result["status"], "measured")
                self.assertFalse(result["release_pass"], "equal contexts do not achieve 50% reduction")
                source = plugin / "profiles/general/orchestration.md"
                source.write_text("changed canonical source\n", encoding="utf-8")
                self.assertTrue(tool.evaluate(path, behavior_evidence=behavior, plugin_root=plugin)["errors"])
                source.write_text("same tiny source\n", encoding="utf-8")
                record = fixture["scenarios"][0]["profiles"]["general"]["stage-ready"]
                record["events"].append(copy.deepcopy(record["events"][0]))
                path.write_text(json.dumps(fixture), encoding="utf-8")
                self.assertTrue(tool.evaluate(path, behavior_evidence=behavior, plugin_root=plugin)["errors"])
                record["events"].pop()
                bad = b"not a valid ready route"
                (root / record["events"][0]["path"]).write_bytes(bad)
                record["events"][0]["sha256"] = digest(bad)
                trace_path = root / record["trace"]["path"]
                trace = json.loads(trace_path.read_text(encoding="utf-8"))
                trace["events"] = record["events"]
                raw = json.dumps(trace).encode()
                trace_path.write_bytes(raw)
                record["trace"]["sha256"] = digest(raw)
                path.write_text(json.dumps(fixture), encoding="utf-8")
                self.assertTrue(tool.evaluate(path, behavior_evidence=behavior, plugin_root=plugin)["errors"])


if __name__ == "__main__":
    unittest.main()
