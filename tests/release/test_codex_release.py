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
PLUGIN = ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it"
SKILLS = PLUGIN / "skills"
START_GUIDE = PLUGIN / "START-HERE.zh-TW.md"
EXPECTED_SKILLS = {
    "ask-then-do-it",
    "ask-requirements",
    "ask-with-docs",
    "implement-tdd",
    "improve-architecture",
    "plan-tickets",
    "review-code",
    "write-spec",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_files(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }


class CodexReleaseSourceTests(unittest.TestCase):
    def test_plugin_start_guide_explains_manual_first_use_and_all_entries(self) -> None:
        self.assertTrue(START_GUIDE.is_file())
        body = START_GUIDE.read_text(encoding="utf-8")
        for required in (
            "1.0.0",
            "手動",
            "$ask-then-do-it",
            "$ask-requirements",
            "$ask-with-docs",
            "$write-spec",
            "$plan-tickets",
            "$implement-tdd",
            "$review-code",
            "$improve-architecture",
            "checksums.sha256",
            "安裝",
            "更新",
            "移除",
        ):
            self.assertIn(required, body)
        self.assertIn("不會自動", body)

    def test_release_identity_and_managed_codex_outputs_are_declared_once(self) -> None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["schema_version"], 2)
        self.assertEqual(config["package_id"], "ask-then-do-it")
        self.assertEqual(
            config["display_name"], "Ask Then Do It"
        )
        self.assertEqual(config["release_version"], "1.0.0")
        self.assertEqual(config["core_version"], "1.0.0")
        self.assertEqual(config["codex"]["source"], "adapters/codex/plugin/ask-then-do-it")
        self.assertEqual(config["codex"]["directory"], "codex/ask-then-do-it")
        self.assertEqual(config["codex"]["archive"], "codex/ask-then-do-it-1.0.0.zip")
        self.assertIn("checksums.sha256", config["managed_outputs"])

    def test_plugin_root_matches_manifest_and_is_the_only_skill_source(self) -> None:
        manifest = json.loads(
            (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(PLUGIN.name, "ask-then-do-it")
        self.assertEqual(manifest["name"], PLUGIN.name)
        self.assertEqual(manifest["version"], "1.0.0")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertFalse((ROOT / "adapters" / "codex" / "skills").exists())
        self.assertEqual(
            {path.name for path in SKILLS.iterdir() if path.is_dir()},
            EXPECTED_SKILLS,
        )


class CodexReleaseBuildTests(unittest.TestCase):
    def test_builder_emits_minimal_equivalent_plugin_zip_and_checksum(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output_root = Path(temporary) / "dist"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_release.py"),
                    "--package",
                    "codex",
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

            package = output_root / "codex" / "ask-then-do-it"
            archive = output_root / "codex" / "ask-then-do-it-1.0.0.zip"
            checksums = output_root / "checksums.sha256"
            expected_files = {
                ".codex-plugin/plugin.json",
                "START-HERE.zh-TW.md",
                "LICENSE",
                "THIRD_PARTY_NOTICES.md",
                *{
                    f"skills/{path.relative_to(SKILLS).as_posix()}"
                    for path in SKILLS.rglob("*")
                    if path.is_file()
                },
            }
            self.assertEqual(relative_files(package), expected_files)
            self.assertEqual(
                (package / "START-HERE.zh-TW.md").read_bytes(),
                START_GUIDE.read_bytes(),
            )
            for source_file in SKILLS.rglob("*"):
                if source_file.is_file():
                    relative = source_file.relative_to(SKILLS).as_posix()
                    self.assertEqual(
                        (package / "skills" / relative).read_bytes(),
                        source_file.read_bytes(),
                        relative,
                    )

            with zipfile.ZipFile(archive) as bundle:
                archive_files = {name for name in bundle.namelist() if not name.endswith("/")}
                self.assertEqual(
                    archive_files,
                    {f"ask-then-do-it/{relative}" for relative in expected_files},
                )
                for relative in expected_files:
                    self.assertEqual(
                        bundle.read(f"ask-then-do-it/{relative}"),
                        (package / relative).read_bytes(),
                    )

            self.assertEqual(
                checksums.read_text(encoding="ascii"),
                f"{sha256(archive)}  codex/ask-then-do-it-1.0.0.zip\n",
            )

            forbidden_names = {
                "marketplace.json",
                "install.ps1",
                "install.bat",
                "setup.exe",
            }
            self.assertTrue(forbidden_names.isdisjoint({p.name for p in package.rglob("*")}))


if __name__ == "__main__":
    unittest.main()
