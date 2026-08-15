import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it"
SKILLS = PLUGIN / "skills"
BUILDER = ROOT / "scripts" / "build_release.py"

EXPECTED_SKILLS = {
    "ask-then-do-it",
    "ask-requirements",
    "ask-with-docs",
    "implement-direct",
    "implement-tdd",
    "improve-architecture",
    "plan-tickets",
    "review-code",
    "write-spec",
}

RENAMED_SKILLS = {
    "ask-then-do-it": "Ask Then Do It",
    "ask-requirements": "Ask Requirements",
    "ask-with-docs": "Ask with Docs",
}


class AskThenDoItCodexIdentityTests(unittest.TestCase):
    def test_plugin_folder_manifest_and_skill_inventory_agree(self) -> None:
        self.assertTrue(PLUGIN.is_dir())
        manifest = json.loads(
            (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )

        self.assertEqual(PLUGIN.name, "ask-then-do-it")
        self.assertEqual(manifest["name"], "ask-then-do-it")
        self.assertEqual(manifest["version"], "1.3.0")
        self.assertEqual(manifest["author"]["name"], "Ian Wu, Handle by me Tech Studio")
        self.assertIn("independent", manifest["description"].lower())
        self.assertIn("not affiliated with or endorsed by Matt Pocock", manifest["description"])
        self.assertEqual(
            {path.name for path in SKILLS.iterdir() if path.is_dir()}, EXPECTED_SKILLS
        )

    def test_each_renamed_skill_has_matching_frontmatter_and_ui_metadata(self) -> None:
        for skill_id, display_name in RENAMED_SKILLS.items():
            with self.subTest(skill=skill_id):
                skill_dir = SKILLS / skill_id
                skill = skill_dir / "SKILL.md"
                metadata = skill_dir / "agents" / "openai.yaml"
                self.assertTrue(skill.is_file())
                self.assertTrue(metadata.is_file())
                self.assertIn(f"name: {skill_id}", skill.read_text(encoding="utf-8"))
                metadata_text = metadata.read_text(encoding="utf-8")
                self.assertIn(f'display_name: "{display_name}"', metadata_text)
                self.assertIn(f"${skill_id}", metadata_text)

    def test_orchestrator_routes_to_renamed_requirement_skills(self) -> None:
        orchestrator = (SKILLS / "ask-then-do-it" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("$ask-requirements", orchestrator)
        self.assertIn("$ask-with-docs", orchestrator)
        self.assertNotIn("$grill-requirements", orchestrator)
        self.assertNotIn("$grill-with-docs", orchestrator)

    def test_isolated_codex_package_carries_identical_legal_files(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "release"
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILDER),
                    "--package",
                    "codex",
                    "--output-root",
                    str(output),
                    "--allow-test-output-root",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            package = output / "codex" / "ask-then-do-it"
            archive = output / "codex" / "ask-then-do-it-1.3.0.zip"

            for legal_file in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
                with self.subTest(legal_file=legal_file):
                    self.assertEqual(
                        (package / legal_file).read_bytes(),
                        (ROOT / legal_file).read_bytes(),
                    )
                    with zipfile.ZipFile(archive) as bundle:
                        self.assertEqual(
                            bundle.read(f"ask-then-do-it/{legal_file}"),
                            (ROOT / legal_file).read_bytes(),
                        )

            guide = (package / "START-HERE.zh-TW.md").read_text(encoding="utf-8")
            self.assertIn("沒有從屬或背書關係", guide)
            self.assertIn("THIRD_PARTY_NOTICES.md", guide)


if __name__ == "__main__":
    unittest.main()
