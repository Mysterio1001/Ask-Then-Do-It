import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "core" / "artifacts" / "document-lifecycle.md"
PROJECT_KNOWLEDGE_MODULE = ROOT / "core" / "modules" / "project-knowledge.md"
CODEX_ASK_WITH_DOCS = (
    ROOT
    / "adapters"
    / "codex"
    / "plugin"
    / "ask-then-do-it"
    / "skills"
    / "ask-with-docs"
    / "SKILL.md"
)
FIXTURES = ROOT / "tests" / "release" / "fixtures" / "document-lifecycle" / "contract"
VALIDATOR = ROOT / "scripts" / "validate_document_lifecycle.py"
MIGRATION_ROOT = ROOT / "docs" / "project" / "drafts" / "codex-skill-runtime-slimming"
MIGRATION_MANIFEST = MIGRATION_ROOT / "lifecycle-manifest.json"

ENVELOPE_FIELDS = {
    "artifact_type",
    "artifact_id",
    "workflow_id",
    "core_version",
    "status",
    "inputs",
    "assumptions",
    "deferred",
    "handoff",
    "approval",
}


def load_fixture(name: str) -> dict:
    with (FIXTURES / name).open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"expected object fixture: {name}")
    return value


def assert_envelope(test: unittest.TestCase, value: dict) -> None:
    test.assertTrue(ENVELOPE_FIELDS.issubset(value), sorted(ENVELOPE_FIELDS - value.keys()))
    test.assertEqual(value["core_version"], "1.4.1")
    test.assertIsInstance(value["artifact_id"], str)
    test.assertRegex(value["artifact_id"], r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    test.assertIsInstance(value["workflow_id"], str)
    test.assertRegex(value["workflow_id"], r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")


def write_manifest_tree(
    root: Path,
    *,
    broken_pointer: bool = False,
    duplicate_key: bool = False,
    orphan: bool = False,
    migration: bool = False,
) -> Path:
    spec = root / "spec.md"
    knowledge = root / "knowledge.md"
    old = root / "old-spec.md"
    history = root / "history.md"
    spec.write_text(
        "# Specification\n\nArtifact type: Specification\nArtifact ID: `spec-1`\n"
        "Workflow ID: `workflow-1`\nCore version: `1.4.1`\nStatus: Approved\n"
        "Inputs: audit\nAssumptions: none\nDeferred: none\nHandoff: plan\n"
        "Approval: approved\n\n## Problem\nUnique specification.\n",
        encoding="utf-8",
    )
    knowledge.write_text(
        "# Knowledge\n\nArtifact type: Project Knowledge Base\nArtifact ID: `kb-1`\n"
        "Workflow ID: `workflow-1`\nCore version: `1.4.1`\nStatus: Approved\n"
        "Inputs: audit\nAssumptions: none\nDeferred: none\nHandoff: maintain\n"
        "Approval: approved\n\n## Facts\nUnique knowledge.\n",
        encoding="utf-8",
    )
    old.write_text(
        "# Pointer\n\nArtifact type: Document Pointer\nArtifact ID: `pointer-1`\n"
        "Workflow ID: `workflow-1`\nCore version: `1.4.1`\nStatus: Approved\n"
        "Inputs: migration\nAssumptions: none\nDeferred: none\nHandoff: read\n"
        "Approval: approved\n\nTarget: spec-1\n",
        encoding="utf-8",
    )
    history.write_text("history\n", encoding="utf-8")

    pointer_path = "missing.md" if broken_pointer else "spec.md"
    pointer_status = "Draft" if broken_pointer else "Approved"
    canonical_key = "behavior-copy" if duplicate_key else "behavior"
    canonical = [
        {
            "artifact_type": "Specification",
            "artifact_id": "spec-1",
            "workflow_id": "workflow-1",
            "core_version": "1.4.1",
            "status": "Approved",
            "canonical_key": canonical_key,
            "path": "spec.md",
            "inputs": ["audit"],
            "assumptions": ["none"],
            "deferred": ["none"],
            "handoff": "plan",
            "approval": "approved",
        },
        {
            "artifact_type": "Project Knowledge Base",
            "artifact_id": "kb-1",
            "workflow_id": "workflow-1",
            "core_version": "1.4.1",
            "status": "Approved",
            "canonical_key": "knowledge",
            "path": "knowledge.md",
            "inputs": ["audit"],
            "assumptions": ["none"],
            "deferred": ["none"],
            "handoff": "maintain",
            "approval": "approved",
        },
    ]
    if duplicate_key:
        duplicate = dict(canonical[0])
        duplicate["artifact_id"] = "spec-duplicate"
        duplicate["path"] = "knowledge.md"
        canonical.append(duplicate)
    pointers = [
        {
            "artifact_type": "Document Pointer",
            "artifact_id": "pointer-1",
            "workflow_id": "workflow-1",
            "core_version": "1.4.1",
            "status": pointer_status,
            "path": "old-spec.md",
            "target_artifact_id": "spec-1",
            "canonical_path": pointer_path,
            "replacement_reason": "Consolidated into canonical artifact.",
            "history_link": "history.md",
            "inputs": ["migration"],
            "assumptions": ["none"],
            "deferred": ["none"],
            "handoff": "read",
            "approval": "approved",
        }
    ]
    manifest = {
        "schema_version": 1,
        "canonical": canonical,
        "pointers": pointers,
        "approved_artifacts": ["spec-1", "kb-1", "missing-approved"] if orphan else ["spec-1", "kb-1"],
        "historical_archive_paths": [],
    }
    if migration:
        backup_root = root / "migration" / "backup"
        staging_root = root / "migration" / "staging"
        backup_root.mkdir(parents=True)
        staging_root.mkdir(parents=True)
        backup_file = backup_root / "old-spec.md"
        backup_file.write_bytes(old.read_bytes())
        source_manifest = root / "migration" / "source-manifest.json"
        source_manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workflow_id": "workflow-1",
                    "core_version": "1.4.1",
                    "sources": [
                        {
                            "source_path": "old-spec.md",
                            "backup_path": "migration/backup/old-spec.md",
                            "source_artifact_id": "pointer-1",
                            "target_artifact_id": "spec-1",
                            "target_section_id": "spec-1",
                            "original_sha256": hashlib.sha256(old.read_bytes()).hexdigest(),
                            "source_status_before": "Approved",
                            "target_status_after": "Approved",
                            "source_disposition": "retained",
                            "source_exists_after": True,
                        }
                    ]
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        manifest["migration"] = {
            "migration_id": "migration-1",
            "workflow_id": "workflow-1",
            "core_version": "1.4.1",
            "status": "completed",
            "source_manifest": "migration/source-manifest.json",
            "backup_root": "migration/backup",
            "staging_root": "migration/staging",
            "recovery": {
                "rollback_available": True,
                "primary_error": None,
                "recovery_errors": [],
            },
        }
        manifest["migration"]["source_manifest_sha256"] = hashlib.sha256(
            source_manifest.read_bytes()
        ).hexdigest()
    manifest_path = root / "lifecycle-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def run_validator(manifest: Path, root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--root",
            str(root),
            "--manifest",
            str(manifest),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class DocumentLifecycleContractTests(unittest.TestCase):
    def test_core_index_links_the_single_lifecycle_contract(self) -> None:
        core_index = (ROOT / "core" / "CORE.md").read_text(encoding="utf-8")
        self.assertIn("[Document Lifecycle Contract](artifacts/document-lifecycle.md)", core_index)

    def test_contract_declares_envelope_ownership_and_path_rules(self) -> None:
        text = CONTRACT.read_text(encoding="utf-8")
        self.assertIn("# Document Lifecycle Artifact Contract", text)
        for field in sorted(ENVELOPE_FIELDS):
            self.assertIn(f"`{field}`", text)
        for category in (
            "Durable project facts",
            "Observable product behavior",
            "Implementation slices",
            "Actual commands and results",
            "Current workflow state",
            "Unapproved requirement exploration",
        ):
            self.assertIn(category, text)
        for status in ("Draft", "Approved", "Superseded", "unverified", "skipped", "blocked"):
            self.assertIn(f"`{status}`", text)
        self.assertIn("repository-relative", text)
        self.assertIn("MUST NOT contain `..`", text)
        self.assertIn("Knowledge Base Change Summary", text)

    def test_decision_packet_has_independent_section_ids_and_statuses(self) -> None:
        packet = load_fixture("decision-packet.json")
        assert_envelope(self, packet)
        self.assertEqual(packet["artifact_type"], "Decision Packet")
        self.assertEqual(packet["status"], "Draft")
        self.assertEqual(packet["knowledge_change"]["summary_required"], True)

        sections = packet["sections"]
        self.assertEqual(
            {section["artifact_type"] for section in sections},
            {
                "Draft Working Notes",
                "Requirement Decision Record",
                "Knowledge Base Change Summary",
            },
        )
        self.assertEqual(len({section["artifact_id"] for section in sections}), 3)
        for section in sections:
            assert_envelope(self, section)
            self.assertEqual(section["workflow_id"], packet["workflow_id"])
            self.assertEqual(section["status"], "Draft")
        self.assertIsNone(packet["approval"])

    def test_no_durable_change_does_not_create_an_empty_summary(self) -> None:
        packet = load_fixture("decision-packet-no-summary.json")
        assert_envelope(self, packet)
        self.assertFalse(packet["knowledge_change"]["summary_required"])
        self.assertNotIn("summary_artifact_id", packet["knowledge_change"])
        self.assertNotIn(
            "Knowledge Base Change Summary",
            {section["artifact_type"] for section in packet["sections"]},
        )

    def test_pointer_exposes_only_target_and_recovery_metadata(self) -> None:
        pointer = load_fixture("pointer.json")
        assert_envelope(self, pointer)
        self.assertEqual(pointer["artifact_type"], "Document Pointer")
        self.assertEqual(pointer["status"], "Superseded")
        for field in (
            "target_artifact_id",
            "canonical_path",
            "replacement_reason",
            "history_link",
        ):
            self.assertIsInstance(pointer.get(field), str)
            self.assertTrue(pointer[field])
        self.assertNotIn("requirements", pointer)
        self.assertNotIn("acceptance_criteria", pointer)
        for field in ("canonical_path", "history_link"):
            self.assertFalse(pointer[field].startswith(("/", "\\")))
            self.assertNotIn("..", Path(pointer[field]).parts)

    def test_archive_index_reuses_pointer_metadata_without_substantive_copy(self) -> None:
        archive = load_fixture("archive-index.json")
        assert_envelope(self, archive)
        self.assertEqual(archive["artifact_type"], "Archive Index")
        self.assertGreaterEqual(len(archive["entries"]), 1)
        for entry in archive["entries"]:
            for field in (
                "target_artifact_id",
                "canonical_path",
                "status",
                "replacement_reason",
                "history_link",
            ):
                self.assertIn(field, entry)
            self.assertEqual(entry["status"], "Superseded")
            self.assertNotIn("requirements", entry)
            self.assertNotIn("acceptance_criteria", entry)

    def test_contract_fixtures_cover_non_promotable_states(self) -> None:
        states = load_fixture("state-fixtures.json")["states"]
        self.assertEqual(
            {state["status"] for state in states},
            {"Draft", "Approved", "Superseded", "unverified", "skipped", "blocked"},
        )
        for state in states:
            self.assertRegex(state["artifact_id"], r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
            if state["status"] in {"unverified", "skipped", "blocked"}:
                self.assertFalse(state["approval"])

    def test_core_project_knowledge_routes_full_documentation_to_one_packet(self) -> None:
        text = PROJECT_KNOWLEDGE_MODULE.read_text(encoding="utf-8")
        for marker in (
            "one Decision Packet per `workflow_id`",
            "Draft Working Notes",
            "Requirement Decision Record",
            "Knowledge Base Change Summary",
            "separate stable `artifact_id` and `status`",
            "`summary_required: true`",
            "`summary_required: false`",
            "MUST NOT create an empty summary",
            "canonical Specification",
            "docs/project/knowledge-base.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_codex_documented_producer_links_packet_sections_and_canonical_outputs(self) -> None:
        text = CODEX_ASK_WITH_DOCS.read_text(encoding="utf-8")
        for marker in (
            "one Decision Packet per workflow ID",
            "decision-packet.md",
            "Draft Working Notes",
            "Requirement Decision Record",
            "Knowledge Base Change Summary",
            "separate stable `artifact_id` and `status`",
            "canonical Specification",
            "canonical Knowledge Base",
            "docs/project/knowledge-base.md",
            "stable IDs instead of copying content",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_full_producer_and_lite_path_keep_packet_creation_separate(self) -> None:
        core_text = PROJECT_KNOWLEDGE_MODULE.read_text(encoding="utf-8")
        codex_text = CODEX_ASK_WITH_DOCS.read_text(encoding="utf-8")
        for text, source in ((core_text, "Core"), (codex_text, "Codex")):
            with self.subTest(source=source):
                self.assertIn("Lite", text)
                self.assertIn("MUST NOT create a Decision Packet", text)
                self.assertIn("Full", text)

    def test_lifecycle_validator_accepts_a_consistent_manifest(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            manifest = write_manifest_tree(root)
            result = run_validator(manifest, root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Document lifecycle validation passed", result.stdout)

    def test_lifecycle_validator_rejects_broken_pointer(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            manifest = write_manifest_tree(root, broken_pointer=True)
            result = run_validator(manifest, root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("canonical path", result.stderr.lower())

    def test_lifecycle_validator_rejects_duplicate_canonical_claim(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            manifest = write_manifest_tree(root, duplicate_key=True)
            result = run_validator(manifest, root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate canonical", result.stderr.lower())

    def test_lifecycle_validator_rejects_missing_historical_archive_exemption(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            manifest = write_manifest_tree(root)
            value = json.loads(manifest.read_text(encoding="utf-8"))
            value["historical_archive_paths"] = ["missing-archive.md"]
            manifest.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            result = run_validator(manifest, root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing historical archive", result.stderr.lower())

    def test_lifecycle_validator_rejects_orphaned_approved_artifact(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            manifest = write_manifest_tree(root, orphan=True)
            result = run_validator(manifest, root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("orphan", result.stderr.lower())

    def test_lifecycle_validator_accepts_migration_recovery_metadata(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            manifest = write_manifest_tree(root, migration=True)
            result = run_validator(manifest, root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("migration recovery validated", result.stdout.lower())

    def test_lifecycle_validator_rejects_missing_migration_backup_manifest(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            manifest = write_manifest_tree(root, migration=True)
            value = json.loads(manifest.read_text(encoding="utf-8"))
            value["migration"]["source_manifest"] = "migration/missing.json"
            manifest.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            result = run_validator(manifest, root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source manifest", result.stderr.lower())

    def test_lifecycle_validator_accepts_partial_migration_recovery_metadata(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            manifest = write_manifest_tree(root, migration=True)
            value = json.loads(manifest.read_text(encoding="utf-8"))
            value["migration"]["status"] = "partial"
            value["migration"]["recovery"] = {
                "rollback_available": True,
                "primary_error": "pointer staging interrupted",
                "recovery_errors": ["no files were removed"],
            }
            manifest.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            result = run_validator(manifest, root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("migration recovery validated", result.stdout.lower())

    def test_lifecycle_validator_rejects_migration_status_promotion(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            manifest = write_manifest_tree(root, migration=True)
            value = json.loads(manifest.read_text(encoding="utf-8"))
            source_manifest = root / "migration" / "source-manifest.json"
            source_value = json.loads(source_manifest.read_text(encoding="utf-8"))
            source_value["sources"][0]["source_status_before"] = "Draft"
            source_value["sources"][0]["target_status_after"] = "Approved"
            source_manifest.write_text(
                json.dumps(source_value, indent=2) + "\n", encoding="utf-8"
            )
            value["migration"]["source_manifest_sha256"] = hashlib.sha256(
                source_manifest.read_bytes()
            ).hexdigest()
            manifest.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            result = run_validator(manifest, root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("promotes", result.stderr.lower())

    def test_representative_migration_has_one_packet_and_metadata_only_pointers(self) -> None:
        manifest = json.loads(MIGRATION_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(
            [item["path"] for item in manifest["canonical"]],
            ["docs/project/drafts/codex-skill-runtime-slimming/decision-packet.md"],
        )
        self.assertEqual(len(manifest["pointers"]), 3)
        for pointer in manifest["pointers"]:
            body = (ROOT / pointer["path"]).read_text(encoding="utf-8")
            self.assertIn("Target artifact ID:", body)
            self.assertIn("Canonical path:", body)
            self.assertNotIn("## Problem", body)
            self.assertNotIn("Acceptance criteria", body)
            self.assertNotIn("## Additions", body)

    def test_representative_migration_preserves_source_hashes(self) -> None:
        manifest = json.loads(MIGRATION_MANIFEST.read_text(encoding="utf-8"))
        source_manifest_path = ROOT / manifest["migration"]["source_manifest"]
        source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
        for source in source_manifest["sources"]:
            backup = ROOT / source["backup_path"]
            self.assertTrue(backup.is_file(), backup)
            self.assertEqual(
                hashlib.sha256(backup.read_bytes()).hexdigest(),
                source["original_sha256"].lower(),
            )

    def test_project_indexes_link_to_migrated_packet_without_copying_draft_sections(self) -> None:
        knowledge_base = (ROOT / "docs/project/knowledge-base.md").read_text(encoding="utf-8")
        status = (ROOT / "docs/project/status.md").read_text(encoding="utf-8")
        history = (ROOT / "docs/evidence/release-history.md").read_text(encoding="utf-8")
        packet_link = "drafts/codex-skill-runtime-slimming/decision-packet.md"
        for document in (knowledge_base, status, history):
            self.assertIn(packet_link, document)
        self.assertIn("lifecycle-manifest.json", history)
        self.assertNotIn("The Codex adapter's public skills preserve", status)

    def test_final_review_evidence_discloses_scope_and_environment_limits(self) -> None:
        review = ROOT / "docs/evidence/workflow-document-lifecycle-deduplication-2026-09-16-review.md"
        body = review.read_text(encoding="utf-8")
        for marker in (
            "T1",
            "T2",
            "T3",
            "T4",
            "T5",
            "T6",
            "23/23",
            "19/19",
            "PyYAML",
            "Generic",
            "Claude",
            "not authorized",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, body)


if __name__ == "__main__":
    unittest.main()
