import json
import os
import secrets
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "claude" / "fixtures" / "host-contract" / "plugin"
PRODUCTION_PLUGIN = ROOT / "adapters" / "claude-code" / "plugin" / "ask-then-do-it"
RELEASE_CONFIG = ROOT / "release" / "release.json"
SKILL_NAMES = {"ask-then-do-it", "ask-then-do-it-5"}
SAFETY_LABELS = ("TEST-ONLY", "NOT PRODUCTION", "NOT PACKAGEABLE")


class ClaudeHostContractFixtureTests(unittest.TestCase):
    def test_fixture_is_isolated_labeled_and_reuses_only_target_skill_names(self) -> None:
        self.assertEqual(
            {path.name for path in FIXTURE.iterdir()},
            {".claude-plugin", "skills", "hooks", "scripts", "TEST-ONLY.md"},
        )
        notice = (FIXTURE / "TEST-ONLY.md").read_text(encoding="utf-8")
        manifest = json.loads(
            (FIXTURE / ".claude-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        for label in SAFETY_LABELS:
            self.assertIn(label, notice)
            self.assertIn(label, manifest["description"])
        self.assertEqual(manifest["name"], "ask-then-do-it")
        self.assertIs(manifest["defaultEnabled"], False)

        skills = FIXTURE / "skills"
        self.assertEqual({path.name for path in skills.iterdir()}, SKILL_NAMES)
        for name in SKILL_NAMES:
            text = (skills / name / "SKILL.md").read_text(encoding="utf-8")
            for label in SAFETY_LABELS:
                self.assertIn(label, text)
            self.assertIn(f"name: {name}", text)
            self.assertIn("model: inherit", text)
            self.assertIn("does not start Ask Then Do It", text)

    def test_hook_uses_documented_bounded_output_without_parsing_native_input(self) -> None:
        hooks = json.loads(
            (FIXTURE / "hooks" / "hooks.json").read_text(encoding="utf-8")
        )
        self.assertEqual(set(hooks), {"description", "hooks"})
        self.assertEqual(set(hooks["hooks"]), {"UserPromptExpansion"})
        handlers = hooks["hooks"]["UserPromptExpansion"]
        self.assertEqual(len(handlers), 1)
        commands = handlers[0]["hooks"]
        self.assertEqual(len(commands), 1)
        command = commands[0]
        self.assertEqual(command["type"], "command")
        self.assertEqual(command["command"], "node")
        self.assertEqual(
            command["args"], ["${CLAUDE_PLUGIN_ROOT}/scripts/marker.mjs"]
        )
        self.assertEqual(command["timeout"], 2)

        marker = (FIXTURE / "scripts" / "marker.mjs").read_text(encoding="utf-8")
        self.assertIn('hookEventName: "UserPromptExpansion"', marker)
        self.assertIn("additionalContext: nonce", marker)
        self.assertIn("TICKET3_PREFLIGHT_MODE", marker)
        self.assertIn("TICKET3_PREFLIGHT_NONCE", marker)
        self.assertNotIn("ATDI_HOST_CONTRACT_MARKER_V1", marker)
        for mode in ("marker", "nonzero", "exit-2", "timeout"):
            self.assertIn(f'case "{mode}"', marker)
        for prohibited_input in ("command_name", "session_id", "prompt", "arguments"):
            self.assertNotIn(prohibited_input, marker)

    def test_marker_requires_a_process_local_unpredictable_nonce(self) -> None:
        marker = FIXTURE / "scripts" / "marker.mjs"
        node = shutil.which("node")
        self.assertIsNotNone(node)
        environment = os.environ.copy()
        environment.pop("TICKET3_PREFLIGHT_NONCE", None)
        missing = subprocess.run(
            [node, str(marker)],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(missing.returncode, 0)
        self.assertEqual(missing.stdout, "")

        outputs = []
        nonces = [secrets.token_hex(32), secrets.token_hex(32)]
        self.assertNotEqual(nonces[0], nonces[1])
        for nonce in nonces:
            environment["TICKET3_PREFLIGHT_NONCE"] = nonce
            result = subprocess.run(
                [node, str(marker)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            outputs.append(output["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(outputs, nonces)
        self.assertNotEqual(outputs[0], outputs[1])

        for skill in SKILL_NAMES:
            text = (FIXTURE / "skills" / skill / "SKILL.md").read_text(
                encoding="utf-8"
            )
            for nonce in nonces:
                self.assertNotIn(nonce, text)
            self.assertNotIn("ATDI_HOST_CONTRACT_MARKER_V1", text)

    def test_fixture_markers_cannot_enter_production_or_release_sources(self) -> None:
        prohibited = (
            "ATDI_HOST_CONTRACT_MARKER_V1",
            "TICKET3_PREFLIGHT_NONCE",
            "NOT PACKAGEABLE",
            "fixtures/host-contract",
        )

        def assert_clean(root: Path) -> None:
            for path in root.rglob("*"):
                if path.is_file():
                    text = path.read_text(encoding="utf-8")
                    for token in prohibited:
                        self.assertNotIn(token, text, str(path))

        assert_clean(PRODUCTION_PLUGIN)
        release_text = RELEASE_CONFIG.read_text(encoding="utf-8")
        for token in prohibited:
            self.assertNotIn(token, release_text)
        release = json.loads(release_text)
        for provider in ("codex", "generic"):
            self.assertFalse(str(release[provider]["source"]).startswith("tests/"))

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            candidate = Path(temporary) / "production"
            shutil.copytree(PRODUCTION_PLUGIN, candidate)
            injected = candidate / "fixture-leak.txt"
            injected.write_text(prohibited[0], encoding="utf-8")
            with self.assertRaises(AssertionError):
                assert_clean(candidate)


if __name__ == "__main__":
    unittest.main()
