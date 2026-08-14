import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "release" / "release.json"
SOURCE = ROOT / "adapters" / "generic-prompts"
START_GUIDES = {
    name: ROOT / "release" / "generic" / name
    for name in ("START-HERE.zh-TW.md", "START-HERE.en.md", "START-HERE.ja.md")
}
MODULES = [
    "bootstrap.md",
    "orchestration.md",
    "requirements.md",
    "documented-requirements.md",
    "specification.md",
    "ticket-planning.md",
    "direct-implementation.md",
    "tdd-implementation.md",
    "review.md",
    "architecture-improvement.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_generated_manifest(path: Path) -> dict[str, object]:
    """Parse the deliberately simple generated YAML without a test dependency."""

    result: dict[str, object] = {}
    section: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        if line.startswith("  - ") and section is not None:
            values = result.setdefault(section, [])
            assert isinstance(values, list)
            values.append(json.loads(line.removeprefix("  - ")))
            continue
        key, raw = line.split(":", 1)
        raw = raw.strip()
        section = key
        if raw:
            result[key] = json.loads(raw)
            section = None
    return result


class GenericReleaseTests(unittest.TestCase):
    def test_configuration_declares_generated_entry_and_fixed_module_order(self) -> None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        generic = config["generic"]
        self.assertEqual(generic["source"], "adapters/generic-prompts")
        self.assertEqual(generic["directory"], "generic/ask-then-do-it-generic-1.2.0")
        self.assertEqual(generic["archive"], "generic/ask-then-do-it-generic-1.2.0.zip")
        self.assertEqual(generic["entrypoint"], "generic-workflow.md")
        self.assertEqual(
            generic["start_guide"],
            "release/generic/START-HERE.zh-TW.md",
        )
        self.assertEqual(generic["modules"], MODULES)
        self.assertFalse((SOURCE / "generic-workflow.md").exists())

    def test_builder_emits_self_contained_conversation_only_package(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output_root = Path(temporary) / "dist"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_release.py"),
                    "--package",
                    "generic",
                    "--allow-test-output-root",
                    "--output-root",
                    str(output_root),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            package = output_root / "generic" / "ask-then-do-it-generic-1.2.0"
            archive = output_root / "generic" / "ask-then-do-it-generic-1.2.0.zip"
            checksums = output_root / "checksums.sha256"
            actual_files = {
                path.relative_to(package).as_posix()
                for path in package.rglob("*")
                if path.is_file()
            }
            expected_files = {
                *START_GUIDES,
                "LICENSE",
                "THIRD_PARTY_NOTICES.md",
                "generic-workflow.md",
                "manifest.yaml",
                *{f"prompts/{name}" for name in MODULES},
            }
            self.assertEqual(actual_files, expected_files)

            for name, source in START_GUIDES.items():
                self.assertEqual((package / name).read_bytes(), source.read_bytes())

            start_guide = (package / "START-HERE.zh-TW.md").read_text(
                encoding="utf-8"
            )
            for required in (
                "每個新對話",
                "generic-workflow.md",
                "第一個需求問題",
                "保存",
                "不能直接修改你的檔案或執行測試",
            ):
                self.assertIn(required, start_guide)
            for forbidden in (
                "Conversation-only",
                "Generic adapter",
                "profile",
                "approval evidence",
                "UNEXECUTED IMPLEMENTATION GUIDANCE",
                "limited-evidence",
                "non-independent",
                "artifact_type",
                "checksums.sha256",
                "SHA-256",
                "checksum",
            ):
                self.assertNotIn(forbidden, start_guide)

            for name in MODULES:
                self.assertEqual(
                    (package / "prompts" / name).read_bytes(),
                    (SOURCE / name).read_bytes(),
                )

            combined = (package / "generic-workflow.md").read_text(encoding="utf-8")
            self.assertIn("GENERATED FILE — DO NOT EDIT", combined)
            self.assertIn("Use the included sections internally", combined)
            self.assertIn("do not ask the user to paste another module", combined.lower())
            self.assertIn("Conversation-only capability boundary", combined)
            self.assertIn("same effective response", combined)
            self.assertIn("exactly one high-impact requirement question", combined)
            self.assertIn("explicit approval", combined)
            self.assertIn("UNEXECUTED IMPLEMENTATION GUIDANCE", combined)
            self.assertIn("UNEXECUTED DIRECT IMPLEMENTATION GUIDANCE", combined)
            positions = [combined.index(f"BEGIN SOURCE: {name}") for name in MODULES]
            self.assertEqual(positions, sorted(positions))

            manifest = read_generated_manifest(package / "manifest.yaml")
            self.assertEqual(manifest["package_id"], "ask-then-do-it")
            self.assertEqual(manifest["release_version"], "1.2.0")
            self.assertEqual(manifest["core_version"], "1.2.0")
            self.assertEqual(manifest["adapter_id"], "generic-prompts")
            self.assertEqual(manifest["capabilities"], ["conversation"])
            self.assertEqual(manifest["source_modules"], MODULES)

            with zipfile.ZipFile(archive) as bundle:
                for relative in expected_files:
                    self.assertEqual(
                        bundle.read(f"ask-then-do-it-generic-1.2.0/{relative}"),
                        (package / relative).read_bytes(),
                    )
            self.assertEqual(
                checksums.read_text(encoding="ascii"),
                f"{sha256(archive)}  generic/ask-then-do-it-generic-1.2.0.zip\n",
            )


if __name__ == "__main__":
    unittest.main()
