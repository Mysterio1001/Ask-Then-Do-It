from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
MAPPING = (
    ROOT
    / "adapters"
    / "claude-code"
    / "plugin"
    / "ask-then-do-it"
    / "config"
    / "model-classifications.json"
)
FIXTURE_ROOT = ROOT / "tests" / "claude" / "fixtures" / "model-classifications"
TRACE = FIXTURE_ROOT / "source-trace.json"
ROUTER = MAPPING.parents[1] / "scripts" / "router.mjs"
EVIDENCE_VALIDATOR = ROOT / "scripts" / "validate_claude_model_evidence.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_evidence_validator(
    mapping: Path = MAPPING,
    trace: Path = TRACE,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(EVIDENCE_VALIDATOR), "--mapping", str(mapping), "--trace", str(trace)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class ClaudeModelClassificationEvidenceTests(unittest.TestCase):
    def test_source_trace_validator_rejects_metadata_drift_from_mapping(self) -> None:
        baseline = run_evidence_validator()
        self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)

        def change_mapping_path(trace: dict, fixture_root: Path) -> None:
            del fixture_root
            trace["mapping_path"] = "adapters/codex/config/model-classifications.json"

        def rename_source_id(trace: dict, fixture_root: Path) -> None:
            del fixture_root
            old_id = "models-overview"
            new_id = "renamed-models-overview"
            trace["sources"][new_id] = trace["sources"].pop(old_id)
            for record in trace["records"]:
                record["source_refs"] = [
                    new_id if source_id == old_id else source_id
                    for source_id in record["source_refs"]
                ]

        def change_source_url(trace: dict, fixture_root: Path) -> None:
            source = trace["sources"]["models-overview"]
            old_url = source["url"]
            source["url"] = "https://example.invalid/not-anthropic"
            snapshot = fixture_root / source["snapshot_path"]
            snapshot.write_text(
                snapshot.read_text(encoding="utf-8").replace(
                    old_url,
                    source["url"],
                    1,
                ),
                encoding="utf-8",
            )
            source["snapshot_sha256"] = sha256(snapshot)

        def change_checked_on(trace: dict, fixture_root: Path) -> None:
            old_checked_on = trace["checked_on"]
            trace["checked_on"] = "2099-12-31"
            for source in trace["sources"].values():
                source["checked_on"] = trace["checked_on"]
                snapshot = fixture_root / source["snapshot_path"]
                snapshot.write_text(
                    snapshot.read_text(encoding="utf-8").replace(
                        f"checked_on: {old_checked_on}",
                        f"checked_on: {trace['checked_on']}",
                        1,
                    ),
                    encoding="utf-8",
                )
                source["snapshot_sha256"] = sha256(snapshot)

        mutations = {
            "noncanonical-mapping-path": change_mapping_path,
            "renamed-source-id": rename_source_id,
            "source-url-drift": change_source_url,
            "trace-and-source-date-drift": change_checked_on,
        }
        with tempfile.TemporaryDirectory(prefix="claude evidence metadata ") as temporary:
            root = Path(temporary)
            for label, mutate in mutations.items():
                with self.subTest(label=label):
                    case_root = root / label
                    case_root.mkdir()
                    mapping = case_root / "model-classifications.json"
                    mapping.write_bytes(MAPPING.read_bytes())
                    fixture_root = case_root / "model-classifications"
                    shutil.copytree(FIXTURE_ROOT, fixture_root)
                    trace_path = fixture_root / "source-trace.json"
                    trace = json.loads(trace_path.read_text(encoding="utf-8"))

                    mutate(trace, fixture_root)
                    trace_path.write_text(json.dumps(trace), encoding="utf-8")

                    self.assertEqual(trace["mapping_sha256"], sha256(mapping))
                    for source in trace["sources"].values():
                        snapshot = fixture_root / source["snapshot_path"]
                        self.assertEqual(source["snapshot_sha256"], sha256(snapshot))
                    rejected = run_evidence_validator(mapping, trace_path)
                    self.assertNotEqual(
                        rejected.returncode,
                        0,
                        f"{label}: validator accepted metadata drift",
                    )

    def test_source_trace_validator_rejects_boolean_schema_version(self) -> None:
        baseline = run_evidence_validator()
        self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)

        with tempfile.TemporaryDirectory(prefix="claude evidence schema ") as temporary:
            root = Path(temporary)
            mapping = root / "model-classifications.json"
            mapping.write_bytes(MAPPING.read_bytes())
            fixture_root = root / "model-classifications"
            shutil.copytree(FIXTURE_ROOT, fixture_root)
            trace_path = fixture_root / "source-trace.json"
            trace = json.loads(trace_path.read_text(encoding="utf-8"))
            trace["schema_version"] = True
            trace_path.write_text(json.dumps(trace), encoding="utf-8")

            rejected = run_evidence_validator(mapping, trace_path)
            self.assertNotEqual(
                rejected.returncode,
                0,
                "validator accepted boolean source trace schema_version",
            )

    def test_source_trace_validator_rejects_wrong_refs_and_deleted_supporting_rows(
        self,
    ) -> None:
        baseline = run_evidence_validator()
        self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)

        with tempfile.TemporaryDirectory(prefix="claude evidence mutations ") as temporary:
            root = Path(temporary)
            mapping = root / "model-classifications.json"
            mapping.write_bytes(MAPPING.read_bytes())
            fixture_root = root / "model-classifications"
            shutil.copytree(FIXTURE_ROOT, fixture_root)
            trace_path = fixture_root / "source-trace.json"

            wrong_ref = json.loads(trace_path.read_text(encoding="utf-8"))
            next(
                record
                for record in wrong_ref["records"]
                if record["model_id"] == "claude-1.0"
            )["source_refs"] = ["models-overview"]
            trace_path.write_text(json.dumps(wrong_ref), encoding="utf-8")
            rejected_ref = run_evidence_validator(mapping, trace_path)
            self.assertNotEqual(rejected_ref.returncode, 0)
            self.assertIn("claude-1.0", rejected_ref.stdout + rejected_ref.stderr)

            shutil.rmtree(fixture_root)
            shutil.copytree(FIXTURE_ROOT, fixture_root)
            trace_path = fixture_root / "source-trace.json"
            deleted_row = fixture_root / "sources" / "model-deprecations.normalized.txt"
            source = deleted_row.read_text(encoding="utf-8")
            deleted_row.write_text(
                source.replace("claude-1.0 | retired\n", "", 1),
                encoding="utf-8",
            )
            trace = json.loads(trace_path.read_text(encoding="utf-8"))
            trace["sources"]["model-deprecations"]["snapshot_sha256"] = sha256(deleted_row)
            trace_path.write_text(json.dumps(trace), encoding="utf-8")
            rejected_row = run_evidence_validator(mapping, trace_path)
            self.assertNotEqual(rejected_row.returncode, 0)
            self.assertIn("claude-1.0", rejected_row.stdout + rejected_row.stderr)

    def test_every_exact_model_classification_has_dated_source_trace(self) -> None:
        self.assertTrue(TRACE.is_file(), "model classification source trace is missing")
        mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
        trace = json.loads(TRACE.read_text(encoding="utf-8"))
        self.assertEqual(
            set(trace),
            {
                "schema_version",
                "mapping_path",
                "mapping_sha256",
                "checked_on",
                "sources",
                "records",
            },
        )
        self.assertEqual(trace["schema_version"], 1)
        self.assertEqual(trace["checked_on"], "2026-09-07")
        self.assertEqual(
            trace["mapping_path"],
            "adapters/claude-code/plugin/ask-then-do-it/config/model-classifications.json",
        )
        self.assertEqual(trace["mapping_sha256"], sha256(MAPPING))

        for source_id, source in trace["sources"].items():
            with self.subTest(source=source_id):
                self.assertEqual(
                    set(source), {"url", "checked_on", "snapshot_path", "snapshot_sha256"}
                )
                self.assertEqual(source["checked_on"], "2026-09-07")
                snapshot = FIXTURE_ROOT / source["snapshot_path"]
                self.assertTrue(snapshot.is_file())
                self.assertEqual(source["snapshot_sha256"], sha256(snapshot))
                text = snapshot.read_text(encoding="utf-8")
                self.assertIn(source["url"], text)
                self.assertIn("checked_on: 2026-09-07", text)

        records = trace["records"]
        self.assertEqual(len(records), len(mapping["classifications"]))
        indexed = {record["model_id"]: record for record in records}
        self.assertEqual(set(indexed), set(mapping["classifications"]))
        for model_id, classification in mapping["classifications"].items():
            with self.subTest(model=model_id):
                record = indexed[model_id]
                self.assertEqual(
                    set(record),
                    {
                        "model_id",
                        "anthropic_status",
                        "classification",
                        "classification_basis",
                        "source_refs",
                    },
                )
                self.assertEqual(record["classification"], classification)
                self.assertIn(record["anthropic_status"], {"active", "retired"})
                self.assertIn(
                    record["classification_basis"],
                    {
                        "generation-gte-5",
                        "active-gte-4.6-lt-5",
                        "active-below-product-minimum",
                        "retired",
                    },
                )
                self.assertTrue(record["source_refs"])
                self.assertTrue(set(record["source_refs"]) <= set(trace["sources"]))

    def test_alias_provider_case_and_future_ids_are_not_promoted_to_exact_models(self) -> None:
        classifications = json.loads(MAPPING.read_text(encoding="utf-8"))["classifications"]
        for value in (
            "sonnet",
            "opus",
            "haiku",
            "default",
            "opusplan",
            "claude-sonnet-4-5",
            "anthropic.claude-opus-5",
            "us.anthropic.claude-opus-5",
            "custom-gateway/claude-opus-5",
            "claude-opus-5-1",
            "Claude-Opus-5",
            " claude-opus-5",
        ):
            with self.subTest(model=value):
                self.assertNotIn(value, classifications)

    def test_runtime_mapping_loader_rejects_schema_extensions(self) -> None:
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js is required for the Claude router tests")
        baseline = json.loads(MAPPING.read_text(encoding="utf-8"))
        mutations = {
            "unknown-top-level": lambda value: value.update({"aliases": {}}),
            "unknown-source-field": lambda value: value["sources"]["models-overview"].update(
                {"mirror": "untrusted"}
            ),
            "alias-classification": lambda value: value["classifications"].update(
                {"sonnet": "supported-non-5"}
            ),
            "canonical-id-substitution": lambda value: (
                value["classifications"].pop("claude-sonnet-5"),
                value["classifications"].update({"claude-made-up-9": "claude-5"}),
            ),
            "classification-swap": lambda value: value["classifications"].update(
                {
                    "claude-sonnet-5": "supported-non-5",
                    "claude-sonnet-4-6": "claude-5",
                }
            ),
        }
        probe = f"""
import {{ loadMapping }} from {json.dumps(ROUTER.as_uri())};
try {{ await loadMapping(process.argv[1]); console.log("accepted"); }}
catch (error) {{ console.log(error.code ?? error.name); }}
"""
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                candidate = json.loads(json.dumps(baseline))
                mutate(candidate)
                with tempfile.TemporaryDirectory(prefix="claude mapping schema ") as temporary:
                    pathname = Path(temporary) / "mapping.json"
                    pathname.write_text(json.dumps(candidate), encoding="utf-8")
                    result = subprocess.run(
                        [node, "--input-type=module", "--eval", probe, str(pathname)],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), "mapping-invalid")


if __name__ == "__main__":
    unittest.main()
