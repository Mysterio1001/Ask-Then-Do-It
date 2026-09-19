"""Offline tool tests; fixtures are synthetic and never release evidence."""

import json
import copy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts import validate_claude_behavior as behavior
from tests.claude.fixtures.behavior.synthetic import build_synthetic, write_json


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validate_claude_behavior.py"


class BehaviorPreparationTests(unittest.TestCase):
    def test_prepare_produces_only_unexecuted_ledger_and_release_gate_rejects_it(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "prepared"
            result = subprocess.run(
                [sys.executable, "-B", str(SCRIPT), "prepare", "--output", str(target)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            ledger = json.loads((target / "behavior-evidence.json").read_text(encoding="utf-8"))
            self.assertEqual(ledger["evidence_kind"], "unexecuted")
            self.assertEqual(ledger["status"], "pending")
            self.assertEqual(len(ledger["runs"]), 86)
            self.assertTrue(all(run["status"] == "pending" for run in ledger["runs"]))
            self.assertFalse(any((target / "transcripts").iterdir()))
            rejected = subprocess.run(
                [sys.executable, "-B", str(SCRIPT), "validate", "--evidence", str(target / "behavior-evidence.json")],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("actual", rejected.stdout + rejected.stderr)

    def test_prepare_refuses_overwrite_and_preserves_files(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "prepared"
            behavior.prepare(target)
            ledger = target / "behavior-evidence.json"
            before = ledger.read_bytes()
            with self.assertRaises(behavior.BehaviorEvidenceError):
                behavior.prepare(target)
            self.assertEqual(ledger.read_bytes(), before)


class BehaviorEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template_directory = tempfile.TemporaryDirectory()
        cls.template = build_synthetic(Path(cls.template_directory.name) / "synthetic")

    @classmethod
    def tearDownClass(cls):
        cls.template_directory.cleanup()

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / "evidence"
        self.root.mkdir()
        self.path = self.root / "behavior-evidence.json"
        shutil.copyfile(self.template, self.path)
        shutil.copytree(self.template.parent / "transcripts", self.root / "transcripts")
        self.ledger = json.loads(self.path.read_text(encoding="utf-8"))

    def validate_mutation(self, mutate, expected_fragment=None):
        candidate = copy.deepcopy(self.ledger)
        mutate(candidate)
        write_json(self.path, candidate)
        errors = behavior.validate_synthetic_evidence(self.path)
        self.assertTrue(errors)
        if expected_fragment:
            self.assertIn(expected_fragment, " ".join(errors))

    def mutate_transcript(self, run_id, mutate):
        run = next(run for run in self.ledger["runs"] if run["id"] == run_id)
        path = self.root / run["transcript"]["path"]
        transcript = json.loads(path.read_text(encoding="utf-8"))
        mutate(transcript)
        write_json(path, transcript)
        run["transcript"]["sha256"] = behavior.digest(path.read_bytes())
        write_json(self.path, self.ledger)

    def test_complete_synthetic_structure_cannot_pass_actual_release_gate(self):
        self.assertEqual(behavior.validate_synthetic_evidence(self.path), [])
        self.assertTrue(behavior.validate_behavior_evidence(self.path))
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "check-synthetic", "--evidence", str(self.path)],
                                capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Release behavior gate has NOT passed", result.stdout)
        self.assertNotIn("Actual-evidence structural boundaries passed", result.stdout)

    def test_exact_inventory_hash_provenance_and_review_rejections(self):
        mutations = (
            ("missing-run", lambda value: value["runs"].pop()),
            ("extra-run", lambda value: value["runs"].append(copy.deepcopy(value["runs"][0]))),
            ("duplicate-run", lambda value: value["runs"].__setitem__(1, copy.deepcopy(value["runs"][0]))),
            ("missing-outcome", lambda value: value["runs"][0]["observations"].pop()),
            ("passed-boolean", lambda value: value["runs"][0].update(passed=True)),
            ("unverified", lambda value: value["runs"][0]["observations"][0].update(verdict="unverified")),
            ("violated", lambda value: value["runs"][0]["observations"][0].update(verdict="violated")),
            ("wrong-catalog", lambda value: value.update(catalog_sha256="0" * 64)),
            ("wrong-fixture", lambda value: value.update(fixture_sha256="0" * 64)),
            ("wrong-staged", lambda value: value.update(staged_conformance_sha256="0" * 64)),
            ("stale-source", lambda value: value["source_hashes"].update({next(iter(value["source_hashes"])): "0" * 64})),
            ("source-inventory", lambda value: value["source_hashes"].update({"profiles/third.md": "0" * 64})),
            ("reused-session", lambda value: value["runs"][1].update(session_sha256=value["runs"][0]["session_sha256"])),
            ("not-fresh", lambda value: value["runs"][0].update(fresh_session=False)),
            ("future-date", lambda value: value["operator_review"].update(reviewed_at="2999-01-01T00:00:00Z")),
            ("stale-date", lambda value: value["runs"][0].update(started_at="2000-01-01T00:00:00Z")),
            ("incomplete-review", lambda value: value["operator_review"].update(complete_transcripts_reviewed=False)),
            ("wrong-provenance", lambda value: value["operator_review"].update(provenance="self-approved")),
            ("pending", lambda value: value.update(status="pending")),
            ("run-synthetic-mismatch", lambda value: value["runs"][0].update(evidence_kind="unexecuted")),
        )
        for label, mutate in mutations:
            with self.subTest(mutation=label):
                self.validate_mutation(mutate)

    def test_environment_minimum_tools_model_and_pair_identity(self):
        for field, bad_value in (
            ("claude_code", "2.1.250"), ("node", "21.0.0"), ("model", "claude-opus-4-5-20251101"),
            ("model", "self-reported-Claude5"), ("effort", "unknown"), ("surface", "web"),
            ("tools", ["shell", "shell"]), ("fixture_sha256", "0" * 64),
        ):
            with self.subTest(field=field, value=bad_value):
                self.validate_mutation(lambda value, f=field, bad=bad_value: value["runs"][0]["environment"].update({f: bad}))
        run_id = "paired/claude-5/requirements"
        run = next(run for run in self.ledger["runs"] if run["id"] == run_id)
        run["environment"]["effort"] = "medium"
        self.mutate_transcript(run_id, lambda transcript: transcript["environment"].update(effort="medium"))
        self.assertIn("paired requirements", " ".join(behavior.validate_synthetic_evidence(self.path)))

    def test_paired_extra_user_approval_must_be_identical_on_both_sides(self):
        run_id = "paired/claude-5/requirements"
        self.mutate_transcript(run_id, lambda transcript: transcript["messages"].append(
            {"role": "user", "text": "I approve this exact record and authorize the next stage."}
        ))
        self.assertTrue(behavior.validate_synthetic_evidence(self.path), "one-sided extra approval must break paired input equality")

    def test_raw_transcript_digest_paths_schema_and_scrub_fail_closed(self):
        for path in ("../outside.json", "transcripts/../../outside.json", "/outside.json", "transcripts\\outside.json", "transcripts/missing.json"):
            with self.subTest(path=path):
                self.validate_mutation(lambda value, p=path: value["runs"][0]["transcript"].update(path=p))
        self.validate_mutation(lambda value: value["runs"][0]["transcript"].update(sha256="0" * 64), "changed/reused")
        for sensitive in ("api_key=do-not-leak", "C:\\Users\\person\\secret", "/home/person/secret", "Bearer exampletoken"):
            with self.subTest(sensitive=sensitive):
                self.validate_mutation(lambda value, s=sensitive: value["runs"][0]["observations"][0].update(assessment=s), "unscrubbed")
        # Duplicate JSON keys must not be silently resolved by the parser.
        self.path.write_text('{"schema_version":1,"schema_version":1}', encoding="utf-8")
        self.assertIn("duplicate JSON", " ".join(behavior.validate_synthetic_evidence(self.path)))

    def test_citation_must_match_observed_response_and_same_subcase(self):
        mutations = (
            ("missing", lambda item: item.update(citations=[])),
            ("quote", lambda item: item["citations"][0].update(quote="invented quote")),
            ("span", lambda item: item["citations"][0].update(end=999999)),
            ("input", lambda item: item["citations"][0].update(message_index=0)),
            ("bool-offset", lambda item: item["citations"][0].update(start=False)),
        )
        for label, mutate in mutations:
            with self.subTest(mutation=label):
                self.validate_mutation(lambda value, change=mutate: change(value["runs"][0]["observations"][0]))
        run = next(run for run in self.ledger["runs"] if run["case_id"] == "CAP-MULTI-AGENT")
        transcript = json.loads((self.root / run["transcript"]["path"]).read_text(encoding="utf-8"))
        wrong_message = transcript["messages"][3]["text"]
        run["observations"][0]["citations"] = [{"message_index": 3, "start": 0, "end": len(wrong_message), "quote": wrong_message}]
        write_json(self.path, self.ledger)
        self.assertIn("different task subcase", " ".join(behavior.validate_synthetic_evidence(self.path)))

    def test_actual_gate_cannot_be_enabled_by_relabeling_only_ledger(self):
        # This deliberate mislabel mutation remains an invalid test candidate,
        # never a saved or purported actual-evidence fixture.
        candidate = copy.deepcopy(self.ledger)
        candidate["evidence_kind"] = "actual"
        write_json(self.path, candidate)
        self.assertTrue(behavior.validate_behavior_evidence(self.path))

    def test_relabeling_all_metadata_cannot_promote_known_synthetic_markers(self):
        # Deliberately invalid spoof candidate in a temporary test directory.
        # It is never delivered, retained, or claimed as actual evidence.
        candidate = copy.deepcopy(self.ledger)
        candidate["evidence_kind"] = "actual"
        candidate["operator_review"]["provenance"] = "human-reviewed-actual-transcripts"
        for run in candidate["runs"]:
            run["evidence_kind"] = "actual"
            path = self.root / run["transcript"]["path"]
            transcript = json.loads(path.read_text(encoding="utf-8"))
            transcript.update(evidence_kind="actual", capture_method="claude-code-export")
            write_json(path, transcript)
            run["transcript"]["sha256"] = behavior.digest(path.read_bytes())
        write_json(self.path, candidate)
        self.assertTrue(behavior.validate_behavior_evidence(self.path), "known synthetic records must not become actual evidence by metadata edits")

    def test_authority_operations_prohibit_wrong_profile_cross_load_and_overlap(self):
        run_id = "authority/general-to-claude-5"
        self.mutate_transcript(run_id, lambda transcript: transcript["operations"][1]["loaded_sources"].append("profiles/general/requirements.md"))
        self.assertIn("cross-profile", " ".join(behavior.validate_synthetic_evidence(self.path)))

    def test_authority_operation_spans_must_include_observed_response_and_citations(self):
        run_id = "authority/general-to-claude-5"
        self.mutate_transcript(run_id, lambda transcript: transcript["operations"][1].update(
            last_message=transcript["operations"][1]["first_message"]
        ))
        self.assertTrue(behavior.validate_synthetic_evidence(self.path), "an input-only operation cannot establish observed authority")

    def test_execution_evidence_requires_real_phases_and_tool_citations(self):
        run_id = "scenario/general/FULL-TDD"
        self.mutate_transcript(run_id, lambda transcript: transcript.update(executions=[]))
        self.assertIn("raw tool execution", " ".join(behavior.validate_synthetic_evidence(self.path)))

    def test_fixed_recipe_staged_conformance_and_pair_inputs(self):
        catalog, manifest, _ = behavior.contracts()
        self.assertEqual(tuple(manifest["implemented_rules"]), behavior.RULE_IDS)
        self.assertEqual(len(manifest["rule_scenarios"]), 30)
        current = yaml.safe_load((ROOT / "adapters/claude-code/conformance.yaml").read_text(encoding="utf-8"))
        self.assertEqual(current["adapter_version"], "1.4.2")
        self.assertEqual(current["validation"]["status"], "unverified")
        self.assertEqual(tuple(current["implemented_rules"]), behavior.RULE_IDS)
        recipes = {recipe["id"]: recipe for recipe in behavior.run_recipes(catalog)}
        for pair in behavior.PAIRED_IDS:
            self.assertEqual(behavior.input_hash(recipes[f"paired/general/{pair}"]), behavior.input_hash(recipes[f"paired/claude-5/{pair}"]))


if __name__ == "__main__":
    unittest.main()
