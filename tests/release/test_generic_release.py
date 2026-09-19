from tests.release.built_fixture import current_distribution

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "release" / "release.json"
SOURCE = ROOT / "adapters" / "generic-prompts"
START_GUIDES = {
    name: ROOT / "release" / "generic" / name
    for name in ("START-HERE.zh-TW.md", "START-HERE.en.md", "START-HERE.ja.md")
}

MODE_EDIT_PERMISSION = (
    '<!-- GENERATED FILE — YOU MAY EDIT ONLY THE "Default workflow mode" '
    'DECLARATION BELOW -->'
)
UNQUALIFIED_EDIT_PROHIBITION = "<!-- GENERATED FILE — DO NOT EDIT -->"
MODULES = [
    "bootstrap.md",
    "orchestration.md",
    "lite-workflow.md",
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
    def test_built_workflow_allows_only_default_mode_declaration_edits(self) -> None:
        combined = (current_distribution() / "generic/ask-then-do-it-generic-1.4.2/SKILL.md").read_text(encoding="utf-8")
        declaration = "Default workflow mode: full"

        self.assertIn(MODE_EDIT_PERMISSION, combined)
        self.assertLess(combined.index(MODE_EDIT_PERMISSION), combined.index(declaration))
        self.assertNotIn(UNQUALIFIED_EDIT_PROHIBITION, combined)

    def test_configuration_declares_generated_entry_and_fixed_module_order(self) -> None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        generic = config["generic"]
        self.assertEqual(generic["source"], "adapters/generic-prompts")
        self.assertEqual(generic["directory"], "generic/ask-then-do-it-generic-1.4.2")
        self.assertEqual(generic["archive"], "generic/ask-then-do-it-generic-1.4.2.zip")
        self.assertEqual(generic["entrypoint"], "SKILL.md")
        self.assertEqual(
            generic["start_guide"],
            "release/generic/START-HERE.zh-TW.md",
        )
        self.assertEqual(generic["modules"], MODULES)
        self.assertFalse((SOURCE / "SKILL.md").exists())

    def test_built_skill_has_parseable_required_frontmatter(self) -> None:
        skill = current_distribution() / "generic/ask-then-do-it-generic-1.4.2/SKILL.md"
        content = skill.read_bytes().decode("utf-8")
        self.assertTrue(content.startswith("---\n"))
        _, frontmatter, body = content.split("---\n", 2)
        metadata = yaml.safe_load(frontmatter)
        self.assertEqual(set(metadata), {"name", "description"})
        self.assertEqual(metadata["name"], "ask-then-do-it-generic")
        self.assertIsInstance(metadata["description"], str)
        self.assertTrue(metadata["description"].strip())
        self.assertLessEqual(len(metadata["description"]), 1024)
        self.assertNotRegex(metadata["description"], r"[<>]")
        self.assertIn(MODE_EDIT_PERMISSION, body)

    def test_builder_rejects_nonstandard_skill_entrypoint(self) -> None:
        for entrypoint in ("generic-workflow.md", "skill.md"):
            with self.subTest(entrypoint=entrypoint), tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                config = json.loads(CONFIG.read_text(encoding="utf-8"))
                config["generic"]["entrypoint"] = entrypoint
                candidate = Path(temporary) / "release.json"
                candidate.write_text(json.dumps(config), encoding="utf-8")
                output = Path(temporary) / "dist"
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/build_release.py"),
                     "--package", "generic", "--config", str(candidate),
                     "--allow-test-output-root", "--output-root", str(output)],
                    cwd=ROOT, capture_output=True, text=True, check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("generic.entrypoint must be SKILL.md", result.stderr)
                self.assertFalse(any(output.rglob("*.zip")))

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

            package = output_root / "generic" / "ask-then-do-it-generic-1.4.2"
            archive = output_root / "generic" / "ask-then-do-it-generic-1.4.2.zip"
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
                "SKILL.md",
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
                "SKILL.md",
                "全文",
                "generic.zh-TW.md",
                "getting-started-simple.zh-TW.md",
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

            combined = (package / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("generic-workflow.md", actual_files)
            self.assertIn(MODE_EDIT_PERMISSION, combined)
            self.assertLess(
                combined.index(MODE_EDIT_PERMISSION),
                combined.index("Default workflow mode: full"),
            )
            self.assertNotIn(UNQUALIFIED_EDIT_PROHIBITION, combined)
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
            self.assertEqual(manifest["release_version"], "1.4.2")
            self.assertEqual(manifest["core_version"], "1.4.2")
            self.assertEqual(manifest["adapter_id"], "generic-prompts")
            self.assertEqual(manifest["entrypoint"], "SKILL.md")
            self.assertEqual(manifest["capabilities"], ["conversation"])
            self.assertEqual(manifest["source_modules"], MODULES)

            with zipfile.ZipFile(archive) as bundle:
                self.assertEqual(
                    bundle.namelist(),
                    sorted(f"ask-then-do-it-generic-1.4.2/{name}" for name in expected_files),
                )
                for relative in expected_files:
                    self.assertEqual(
                        bundle.read(f"ask-then-do-it-generic-1.4.2/{relative}"),
                        (package / relative).read_bytes(),
                    )
            self.assertEqual(
                checksums.read_text(encoding="ascii"),
                f"{sha256(archive)}  generic/ask-then-do-it-generic-1.4.2.zip\n",
            )


if __name__ == "__main__":
    unittest.main()
