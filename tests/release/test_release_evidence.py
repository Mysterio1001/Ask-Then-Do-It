import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "release" / "release.json"
VALIDATOR = ROOT / "scripts" / "validate_release_evidence.py"


def run_validator(ledger: Path, evidence: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--config",
            str(CONFIG),
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
            checks.append(
                {
                    "id": check_id,
                    "status": status,
                    "command": f"verify {check_id}",
                    "outcome": f"{check_id}: {status}",
                }
            )
        ledger = root / "ledger.json"
        ledger.write_text(
            json.dumps(
                {"release_version": "3.0.0", "checks": checks},
                indent=2,
            ),
            encoding="utf-8",
        )
        evidence = root / "evidence.md"
        evidence.write_text(
            "# Grill Me Release 3.0.0 Evidence\n\n"
            "Release version: `3.0.0`\n\n"
            "Status: Completed\n",
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


if __name__ == "__main__":
    unittest.main()
