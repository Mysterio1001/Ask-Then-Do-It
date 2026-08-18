import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "release" / "release.json"
BUILDER = ROOT / "scripts" / "build_release.py"


class AskThenDoItGenericIdentityTests(unittest.TestCase):
    def test_isolated_generic_package_has_new_identity_legal_files_and_entrypoint(self) -> None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["package_id"], "ask-then-do-it")
        self.assertEqual(config["display_name"], "Ask Then Do It")
        self.assertEqual(
            config["generic"]["directory"], "generic/ask-then-do-it-generic-1.3.1"
        )

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "release"
            result = subprocess.run(
                [sys.executable, str(BUILDER), "--package", "generic", "--output-root", str(output), "--allow-test-output-root"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            package = output / "generic" / "ask-then-do-it-generic-1.3.1"
            archive = output / "generic" / "ask-then-do-it-generic-1.3.1.zip"
            manifest = (package / "manifest.yaml").read_text(encoding="utf-8")
            combined = (package / "generic-workflow.md").read_text(encoding="utf-8")
            guide = (package / "START-HERE.zh-TW.md").read_text(encoding="utf-8")

            self.assertIn('package_id: "ask-then-do-it"', manifest)
            self.assertIn('display_name: "Ask Then Do It"', manifest)
            self.assertIn("same effective response", combined)
            self.assertIn("exactly one high-impact requirement question", combined)
            self.assertIn("沒有從屬關係", guide)
            self.assertIn("THIRD_PARTY_NOTICES.md", guide)
            for legal_file in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
                self.assertEqual((package / legal_file).read_bytes(), (ROOT / legal_file).read_bytes())
                with zipfile.ZipFile(archive) as bundle:
                    self.assertEqual(bundle.read(f"ask-then-do-it-generic-1.3.1/{legal_file}"), (ROOT / legal_file).read_bytes())


if __name__ == "__main__":
    unittest.main()
