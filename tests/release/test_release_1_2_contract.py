import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "release" / "release.json"
BUILDER = ROOT / "scripts" / "build_release.py"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN = ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it"


def load_builder_module():
    spec = importlib.util.spec_from_file_location("release_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load release builder: {BUILDER}")
    module = importlib.util.module_from_spec(spec)
    scripts_path = str(BUILDER.parent)
    sys.path.insert(0, scripts_path)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts_path)
    return module


def top_level_scalar(path: Path, key: str) -> str:
    prefix = f"{key}:"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip().strip("\"'")
    raise AssertionError(f"missing {key} in {path}")


class ReleaseOneTwoContractTests(unittest.TestCase):
    def test_active_release_declarations_are_in_lockstep(self) -> None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["release_version"], "1.2.0")
        self.assertEqual(config["core_version"], "1.2.0")
        self.assertEqual(config["codex"]["archive"], "codex/ask-then-do-it-1.2.0.zip")
        self.assertEqual(
            config["generic"]["directory"],
            "generic/ask-then-do-it-generic-1.2.0",
        )
        self.assertEqual(
            config["generic"]["archive"],
            "generic/ask-then-do-it-generic-1.2.0.zip",
        )

        self.assertEqual(
            json.loads(
                (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
            )["version"],
            "1.2.0",
        )
        for path in (
            ROOT / "core" / "rules" / "rules.yaml",
            ROOT / "adapters" / "codex" / "conformance.yaml",
            ROOT / "adapters" / "generic-prompts" / "manifest.yaml",
        ):
            self.assertEqual(top_level_scalar(path, "core_version"), "1.2.0")
        self.assertEqual(
            json.loads(MARKETPLACE.read_text(encoding="utf-8"))["plugins"][0]["source"]["ref"],
            "v1.2.0",
        )

    def test_release_builder_rejects_marketplace_ref_version_drift(self) -> None:
        builder = load_builder_module()
        catalog = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        catalog["plugins"][0]["source"]["ref"] = "v1.1.0"

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            candidate = Path(temporary) / "marketplace.json"
            candidate.write_text(json.dumps(catalog), encoding="utf-8")
            with patch.object(builder, "MARKETPLACE_CATALOG", candidate):
                with self.assertRaisesRegex(
                    builder.BuildError,
                    "marketplace.*v1.2.0",
                ):
                    builder.load_config(CONFIG)

    def test_clean_build_has_current_archives_assets_and_package_boundaries(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILDER),
                    "--allow-test-output-root",
                    "--output-root",
                    str(output),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            codex_archive = output / "codex" / "ask-then-do-it-1.2.0.zip"
            generic_archive = output / "generic" / "ask-then-do-it-generic-1.2.0.zip"
            self.assertTrue(codex_archive.is_file())
            self.assertTrue(generic_archive.is_file())
            checksums = (output / "checksums.sha256").read_text(encoding="ascii")
            for archive in (codex_archive, generic_archive):
                relative = archive.relative_to(output).as_posix()
                self.assertIn(
                    f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {relative}\n",
                    checksums,
                )

            with zipfile.ZipFile(codex_archive) as bundle:
                names = set(bundle.namelist())
                self.assertIn("ask-then-do-it/assets/icon.png", names)
                self.assertIn("ask-then-do-it/assets/logo.png", names)
                self.assertFalse(any(name.endswith("marketplace.json") for name in names))
            with zipfile.ZipFile(generic_archive) as bundle:
                names = set(bundle.namelist())
                self.assertFalse(any("/assets/" in name for name in names))
                self.assertFalse(any(name.endswith("marketplace.json") for name in names))


if __name__ == "__main__":
    unittest.main()
