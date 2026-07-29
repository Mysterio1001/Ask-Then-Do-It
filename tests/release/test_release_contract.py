import json
import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "release" / "release.json"
BUILDER = ROOT / "scripts" / "build_release.py"
REQUIRED_VALIDATION_CHECKS = [
    "automated-tests",
    "codex-skill-validation",
    "codex-plugin-validation",
    "codex-conformance",
    "generic-conformance",
    "codex-package-inventory",
    "generic-package-inventory",
    "reproducible-build",
    "zip-equivalence",
    "sha256-verification",
    "v2-preservation",
    "release-architecture-diagnosis",
]


def run_builder(
    config: Path, output: Path, *, allow_test_output: bool = False
) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(BUILDER),
        "--config",
        str(config),
        "--output-root",
        str(output),
    ]
    if allow_test_output:
        command.append("--allow-test-output-root")
    return subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def top_level_scalar(path: Path, key: str) -> str:
    prefix = f"{key}:"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip().strip("\"'")
    raise AssertionError(f"missing {key} in {path}")


class ReleaseContractTests(unittest.TestCase):
    def test_v3_release_identity_and_validation_gate_are_declared(self) -> None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["schema_version"], 2)
        self.assertEqual(config["release_version"], "3.0.0")
        self.assertEqual(config["core_version"], "3.0.0")
        self.assertEqual(
            config["required_validation_checks"], REQUIRED_VALIDATION_CHECKS
        )

    def test_validated_2_1_release_artifacts_remain_byte_identical(self) -> None:
        expected = {
            "dist/grill-me-2.1.0.zip":
                "10c9b95e9e75c9dac20e570d0f7ed75ef71e4ad0d59e755f53d27ec5a729236d",
            "dist/generic-prompts-2.1.0.zip":
                "5f5d6e86dbde9e2de99f68528c18df1ea1265b59f65d969a4aa9c70bee954254",
            "docs/evidence/grill-me-release-2.1.0.md":
                "cb740d91041363f15e262c090f20f33e7b5716ac554b61bfaa4b0a50f4589879",
        }
        for relative, digest in expected.items():
            path = ROOT / relative
            with self.subTest(path=relative):
                self.assertTrue(path.is_file())
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)
        self.assertEqual(
            (ROOT / "dist" / "checksums-2.1.0.sha256").read_text(
                encoding="ascii"
            ),
            "10c9b95e9e75c9dac20e570d0f7ed75ef71e4ad0d59e755f53d27ec5a729236d  grill-me-2.1.0.zip\n"
            "5f5d6e86dbde9e2de99f68528c18df1ea1265b59f65d969a4aa9c70bee954254  generic-prompts-2.1.0.zip\n",
        )

    def test_non_default_output_requires_explicit_test_opt_in(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            result = run_builder(CONFIG, output)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--allow-test-output-root", result.stderr)
            self.assertFalse((output / "grill-me").exists())

    def test_core_version_is_consistent_across_all_canonical_declarations(self) -> None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        declarations = (
            ROOT / "core" / "rules" / "rules.yaml",
            ROOT / "adapters" / "codex" / "conformance.yaml",
            ROOT / "adapters" / "generic-prompts" / "manifest.yaml",
        )
        for path in declarations:
            with self.subTest(path=path):
                self.assertEqual(
                    top_level_scalar(path, "core_version"), config["core_version"]
                )

    def test_builder_rejects_a_core_version_conflict_before_output(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            config = json.loads(CONFIG.read_text(encoding="utf-8"))
            config["core_version"] = "9.9.9"
            conflicting = root / "release.json"
            conflicting.write_text(
                json.dumps(config, ensure_ascii=False), encoding="utf-8"
            )
            output = root / "dist"

            result = run_builder(conflicting, output)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("core_version", result.stderr)
            self.assertFalse((output / "grill-me").exists())
            self.assertFalse((output / "generic-prompts-3.0.0").exists())

    def test_builder_rejects_unknown_configuration_fields(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            config = json.loads(CONFIG.read_text(encoding="utf-8"))
            config["surprise"] = True
            invalid = root / "release.json"
            invalid.write_text(json.dumps(config), encoding="utf-8")
            result = run_builder(invalid, root / "dist")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown", result.stderr)

    def test_builder_rejects_duplicate_stale_and_extra_runtime_inventory(self) -> None:
        mutations = {
            "duplicate Skill": lambda config, _root: config["codex"]["skills"].append(
                config["codex"]["skills"][0]
            ),
            "stale prompt": lambda config, _root: config["generic"]["modules"].append(
                "stale-prompt.md"
            ),
            "unlisted Skill": lambda config, _root: config["codex"]["skills"].remove(
                "grill-with-docs"
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    root = Path(temporary)
                    config = json.loads(CONFIG.read_text(encoding="utf-8"))
                    mutate(config, root)
                    invalid = root / "release.json"
                    invalid.write_text(json.dumps(config), encoding="utf-8")
                    result = run_builder(
                        invalid, root / "dist", allow_test_output=True
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse((root / "dist" / "grill-me").exists())

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            plugin = root / "source" / "grill-me"
            shutil.copytree(
                ROOT / "adapters" / "codex" / "plugin" / "grill-me", plugin
            )
            (plugin / "unexpected-runtime.txt").write_text(
                "not approved runtime content", encoding="utf-8"
            )
            config = json.loads(CONFIG.read_text(encoding="utf-8"))
            config["codex"]["source"] = plugin.relative_to(ROOT).as_posix()
            invalid = root / "release.json"
            invalid.write_text(json.dumps(config), encoding="utf-8")
            result = run_builder(invalid, root / "dist", allow_test_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unexpected Codex Plugin source entries", result.stderr)

    def test_release_builder_contains_no_install_publish_or_network_operations(self) -> None:
        text = BUILDER.read_text(encoding="utf-8")
        for forbidden in (
            "import subprocess",
            "import urllib",
            "import requests",
            "CODEX_HOME",
            "marketplace.json",
            "codex plugin add",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
