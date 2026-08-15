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
    "workflow-token-proxy",
    "codex-skill-validation",
    "codex-plugin-validation",
    "codex-conformance",
    "generic-conformance",
    "codex-package-inventory",
    "generic-package-inventory",
    "reproducible-build",
    "zip-equivalence",
    "sha256-verification",
    "removed-artifact-scan",
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
    def test_unittest_discovery_includes_every_test_package(self) -> None:
        for package in ("codex", "conformance", "generic", "release"):
            marker = ROOT / "tests" / package / "__init__.py"
            with self.subTest(package=package):
                self.assertTrue(
                    marker.is_file(),
                    f"unittest discover would skip tests/{package} without {marker.name}",
                )

    def test_current_release_identity_and_validation_gate_are_declared(self) -> None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["schema_version"], 2)
        self.assertEqual(config["release_version"], "1.3.0")
        self.assertEqual(config["core_version"], "1.3.0")
        self.assertEqual(
            config["required_validation_checks"], REQUIRED_VALIDATION_CHECKS
        )

    def test_current_distribution_has_exactly_two_verified_archives(self) -> None:
        checksums = (ROOT / "dist" / "checksums.sha256").read_text(
            encoding="ascii"
        ).splitlines()
        expected = {
            "codex/ask-then-do-it-1.3.0.zip",
            "generic/ask-then-do-it-generic-1.3.0.zip",
        }
        self.assertEqual({line.split("  ", 1)[1] for line in checksums}, expected)
        for line in checksums:
            digest, relative = line.split("  ", 1)
            archive = ROOT / "dist" / relative
            with self.subTest(archive=relative):
                self.assertTrue(archive.is_file())
                self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), digest)

    def test_non_default_output_requires_explicit_test_opt_in(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            result = run_builder(CONFIG, output)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--allow-test-output-root", result.stderr)
            self.assertFalse((output / "codex").exists())

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
            self.assertFalse((output / "codex").exists())
            self.assertFalse((output / "generic").exists())

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
                "ask-with-docs"
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
                    self.assertFalse((root / "dist" / "codex").exists())

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            plugin = root / "source" / "ask-then-do-it"
            shutil.copytree(
                ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it", plugin
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
            "codex plugin add",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
