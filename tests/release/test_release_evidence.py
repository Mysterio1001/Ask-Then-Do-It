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

    def test_user_may_skip_automated_tests_with_explicit_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            ledger, evidence = self.make_artifacts(
                Path(temporary), ("automated-tests", "skipped-by-user")
            )
            result = run_validator(ledger, evidence)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("skipped-by-user", result.stdout)

    def test_user_skip_does_not_apply_to_non_test_release_checks(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            ledger, evidence = self.make_artifacts(
                Path(temporary), ("sha256-verification", "skipped-by-user")
            )
            result = run_validator(ledger, evidence)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("sha256-verification", result.stderr)

    def test_skipped_tests_require_approval_metadata(self) -> None:
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
            self.assertIn("approval", result.stderr.lower())

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
