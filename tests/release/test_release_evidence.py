import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "release" / "release.json"
VALIDATOR = ROOT / "scripts" / "validate_release_evidence.py"


def run_validator(
    ledger: Path, evidence: Path, config: Path = CONFIG
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--config",
            str(config),
            "--ledger",
            str(ledger),
            "--evidence",
            str(evidence),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class ReleaseEvidenceGateTests(unittest.TestCase):
    def make_artifacts(
        self, root: Path, override: tuple[str, str] | None = None
    ) -> tuple[Path, Path]:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        checks = []
        for check_id in config["required_validation_checks"]:
            status = override[1] if override and override[0] == check_id else "passed"
            check = {
                "id": check_id,
                "status": status,
                "command": f"verify {check_id}",
                "outcome": f"{check_id}: {status}",
            }
            if status == "skipped-by-user":
                check["reason"] = "Approved Ticket mode is direct"
                check["approval"] = "optional-ticket-testing-plan"
            checks.append(check)
        ledger = root / "ledger.json"
        version = config["release_version"]
        ledger.write_text(
            json.dumps(
                {"release_version": version, "checks": checks},
                indent=2,
            ),
            encoding="utf-8",
        )
        evidence = root / "evidence.md"
        skipped = any(check["status"] == "skipped-by-user" for check in checks)
        evidence.write_text(
            f"# Ask Then Do It Release {version} Evidence\n\n"
            f"Release version: `{version}`\n\n"
            "Status: Completed\n"
            + ("\nTests: `skipped-by-user`\n" if skipped else ""),
            encoding="utf-8",
        )
        return ledger, evidence

    def test_all_required_passed_checks_accept_completed_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            ledger, evidence = self.make_artifacts(Path(temporary))
            result = run_validator(ledger, evidence)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("validated", result.stdout.lower())

    def test_failed_or_blocked_check_rejects_completed_evidence(self) -> None:
        for status in ("failed", "blocked"):
            with self.subTest(status=status):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    ledger, evidence = self.make_artifacts(
                        Path(temporary), ("automated-tests", status)
                    )
                    result = run_validator(ledger, evidence)
                    self.assertNotEqual(result.returncode, 0)
                self.assertIn(status, result.stderr.lower())

    def test_required_automated_tests_cannot_be_skipped(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            ledger, evidence = self.make_artifacts(
                Path(temporary), ("automated-tests", "skipped-by-user")
            )
            result = run_validator(ledger, evidence)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("automated-tests", result.stderr)
            self.assertIn("not passed", result.stderr.lower())

    def test_user_skip_does_not_apply_to_non_test_release_checks(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            ledger, evidence = self.make_artifacts(
                Path(temporary), ("sha256-verification", "skipped-by-user")
            )
            result = run_validator(ledger, evidence)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("sha256-verification", result.stderr)

    def test_skip_metadata_cannot_override_a_required_status(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            ledger, evidence = self.make_artifacts(
                root, ("automated-tests", "skipped-by-user")
            )
            data = json.loads(ledger.read_text(encoding="utf-8"))
            automated = next(
                check for check in data["checks"] if check["id"] == "automated-tests"
            )
            automated.pop("approval")
            ledger.write_text(json.dumps(data), encoding="utf-8")
            result = run_validator(ledger, evidence)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("automated-tests", result.stderr)
            self.assertIn("not passed", result.stderr.lower())

    def test_missing_required_check_rejects_completed_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            ledger, evidence = self.make_artifacts(root)
            data = json.loads(ledger.read_text(encoding="utf-8"))
            data["checks"].pop()
            ledger.write_text(json.dumps(data), encoding="utf-8")
            result = run_validator(ledger, evidence)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing", result.stderr.lower())

    def test_absent_ledger_or_evidence_rejects(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            ledger, evidence = self.make_artifacts(root)

            missing_ledger = run_validator(root / "missing-ledger.json", evidence)
            self.assertNotEqual(missing_ledger.returncode, 0)
            self.assertIn("missing validation ledger", missing_ledger.stderr.lower())

            missing_evidence = run_validator(ledger, root / "missing-evidence.md")
            self.assertNotEqual(missing_evidence.returncode, 0)
            self.assertIn("missing release evidence", missing_evidence.stderr.lower())

    def test_incomplete_or_version_mismatched_evidence_rejects(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            ledger, evidence = self.make_artifacts(root)
            version = json.loads(CONFIG.read_text(encoding="utf-8"))["release_version"]

            evidence.write_text(
                "# Release evidence\n\n"
                f"Release version: `{version}`\n\n"
                "Status: Review Pending\n",
                encoding="utf-8",
            )
            incomplete = run_validator(ledger, evidence)
            self.assertNotEqual(incomplete.returncode, 0)
            self.assertIn("status: completed", incomplete.stderr.lower())

            ledger_data = json.loads(ledger.read_text(encoding="utf-8"))
            ledger_data["release_version"] = "0.0.0"
            ledger.write_text(json.dumps(ledger_data), encoding="utf-8")
            ledger_mismatch = run_validator(ledger, evidence)
            self.assertNotEqual(ledger_mismatch.returncode, 0)
            self.assertIn("does not match", ledger_mismatch.stderr.lower())

            ledger_data["release_version"] = version
            ledger.write_text(json.dumps(ledger_data), encoding="utf-8")
            evidence.write_text(
                "# Release evidence\n\n"
                "Release version: `0.0.0`\n\n"
                "Status: Completed\n",
                encoding="utf-8",
            )
            evidence_mismatch = run_validator(ledger, evidence)
            self.assertNotEqual(evidence_mismatch.returncode, 0)
            self.assertIn("release version", evidence_mismatch.stderr.lower())

    def test_duplicate_status_metadata_rejects_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            ledger, evidence = self.make_artifacts(root)
            version = json.loads(CONFIG.read_text(encoding="utf-8"))["release_version"]
            evidence.write_text(
                "# Release evidence\n\n"
                f"Release version: `{version}`\n\n"
                "Status: Review Pending\n\n"
                "Status: Completed\n",
                encoding="utf-8",
            )

            result = run_validator(ledger, evidence)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("status", result.stderr.lower())

    def test_duplicate_release_version_metadata_rejects_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            ledger, evidence = self.make_artifacts(root)
            version = json.loads(CONFIG.read_text(encoding="utf-8"))["release_version"]
            evidence.write_text(
                "# Release evidence\n\n"
                "Release version: `0.0.0`\n\n"
                f"Release version: `{version}`\n\n"
                "Status: Completed\n",
                encoding="utf-8",
            )

            result = run_validator(ledger, evidence)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("release version", result.stderr.lower())

    def test_duplicate_json_keys_reject_release_artifacts(self) -> None:
        cases = (
            ("release configuration", "config-root"),
            ("validation ledger", "ledger-root"),
            ("validation ledger", "check-object"),
        )
        for label, location in cases:
            with self.subTest(location=location):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    root = Path(temporary)
                    ledger, evidence = self.make_artifacts(root)
                    config = CONFIG
                    if location == "config-root":
                        config = root / "release.json"
                        config.write_text(
                            CONFIG.read_text(encoding="utf-8").replace(
                                "{",
                                '{"release_version": "0.0.0",',
                                1,
                            ),
                            encoding="utf-8",
                        )
                    elif location == "ledger-root":
                        ledger.write_text(
                            ledger.read_text(encoding="utf-8").replace(
                                "{",
                                '{"release_version": "0.0.0",',
                                1,
                            ),
                            encoding="utf-8",
                        )
                    else:
                        ledger.write_text(
                            ledger.read_text(encoding="utf-8").replace(
                                '"status": "passed"',
                                '"status": "failed",\n      "status": "passed"',
                                1,
                            ),
                            encoding="utf-8",
                        )

                    result = run_validator(ledger, evidence, config)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(label, result.stderr.lower())
                    self.assertIn("duplicate json key", result.stderr.lower())

    def test_non_envelope_metadata_cannot_complete_draft_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            ledger, evidence = self.make_artifacts(root)
            version = json.loads(CONFIG.read_text(encoding="utf-8"))["release_version"]
            cases = {
                "fenced-code": (
                    "# Draft release evidence\n\n"
                    "```text\n"
                    f"Release version: `{version}`\n\n"
                    "Status: Completed\n"
                    "```\n"
                ),
                "tilde-fenced-code": (
                    "# Draft release evidence\n\n"
                    "~~~text\n"
                    f"Release version: `{version}`\n\n"
                    "Status: Completed\n"
                    "~~~\n"
                ),
                "html-comment": (
                    "# Draft release evidence\n\n"
                    "<!--\n"
                    f"Release version: `{version}`\n\n"
                    "Status: Completed\n"
                    "-->\n"
                ),
                "body-section": (
                    "# Draft release evidence\n\n"
                    "### Example\n\n"
                    f"Release version: `{version}`\n\n"
                    "Status: Completed\n"
                ),
                "plain-body": (
                    "# Draft release evidence\n\n"
                    "This is body content, not an artifact envelope.\n\n"
                    f"Release version: `{version}`\n\n"
                    "Status: Completed\n"
                ),
                "setext-section": (
                    "# Draft release evidence\n\n"
                    "Example section\n"
                    "---------------\n\n"
                    f"Release version: `{version}`\n\n"
                    "Status: Completed\n"
                ),
                "setext-metadata-heading": (
                    "# Draft release evidence\n\n"
                    f"Release version: `{version}`\n\n"
                    "Status: Completed\n"
                    "-----------------\n"
                ),
                "second-atx-h1": (
                    "# Draft release evidence\n\n"
                    "# Example section\n\n"
                    f"Release version: `{version}`\n\n"
                    "Status: Completed\n"
                ),
                "raw-html-details": (
                    "# Draft release evidence\n\n"
                    "<details>\n"
                    "<summary>Example</summary>\n\n"
                    f"Release version: `{version}`\n\n"
                    "Status: Completed\n"
                    "</details>\n"
                ),
                "raw-html-pre": (
                    "# Draft release evidence\n\n"
                    "<pre>\n"
                    f"Release version: `{version}`\n\n"
                    "Status: Completed\n"
                    "</pre>\n"
                ),
            }
            for location, body in cases.items():
                with self.subTest(location=location):
                    evidence.write_text(body, encoding="utf-8")
                    result = run_validator(ledger, evidence)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("status: completed", result.stderr.lower())

    def test_non_envelope_examples_do_not_conflict_with_valid_metadata(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            ledger, evidence = self.make_artifacts(root)
            version = json.loads(CONFIG.read_text(encoding="utf-8"))["release_version"]
            evidence.write_text(
                "# Completed release evidence\n\n"
                "Artifact type: Release Evidence\n\n"
                "Artifact ID: `release-evidence`\n\n"
                "Workflow ID: `release-workflow`\n\n"
                "Core version: `1.3.0`\n\n"
                f"Release version: `{version}`\n\n"
                "Status: Completed\n\n"
                "Inputs: Approved Specification and validation ledger.\n\n"
                "Deferred: External publication.\n\n"
                "## Rejected example\n\n"
                "~~~text\n"
                "Release version: `0.0.0`\n\n"
                "Status: Review Pending\n"
                "~~~\n",
                encoding="utf-8",
            )

            result = run_validator(ledger, evidence)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_release_config_cannot_remove_workflow_token_proxy_gate(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            ledger, evidence = self.make_artifacts(root)
            config_data = json.loads(CONFIG.read_text(encoding="utf-8"))
            config_data["required_validation_checks"].remove(
                "workflow-token-proxy"
            )
            config = root / "release.json"
            config.write_text(json.dumps(config_data), encoding="utf-8")

            ledger_data = json.loads(ledger.read_text(encoding="utf-8"))
            ledger_data["checks"] = [
                check
                for check in ledger_data["checks"]
                if check["id"] != "workflow-token-proxy"
            ]
            ledger.write_text(json.dumps(ledger_data), encoding="utf-8")

            result = run_validator(ledger, evidence, config)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("workflow-token-proxy", result.stderr)

    def test_missing_workflow_token_proxy_result_rejects_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            ledger, evidence = self.make_artifacts(root)
            data = json.loads(ledger.read_text(encoding="utf-8"))
            data["checks"] = [
                check
                for check in data["checks"]
                if check["id"] != "workflow-token-proxy"
            ]
            ledger.write_text(json.dumps(data), encoding="utf-8")

            result = run_validator(ledger, evidence)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("workflow-token-proxy", result.stderr)

    def test_failed_workflow_token_proxy_result_rejects_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            ledger, evidence = self.make_artifacts(
                Path(temporary), ("workflow-token-proxy", "failed")
            )
            result = run_validator(ledger, evidence)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("workflow-token-proxy", result.stderr)
            self.assertIn("failed", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
