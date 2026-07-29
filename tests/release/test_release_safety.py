import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "scripts" / "build_release.py"
CONFIG = ROOT / "release" / "release.json"


def run_builder(output_root: Path, config: Path = CONFIG) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(BUILDER),
            "--config",
            str(config),
            "--allow-test-output-root",
            "--output-root",
            str(output_root),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file()
    }


class ReleaseSafetyTests(unittest.TestCase):
    def test_v3_build_replaces_only_validated_legacy_overlap(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            output.mkdir()
            source_dist = ROOT / "dist"
            with zipfile.ZipFile(source_dist / "grill-me-2.1.0.zip") as bundle:
                bundle.extractall(output)
            shutil.copytree(
                source_dist / "generic-prompts-2.1.0",
                output / "generic-prompts-2.1.0",
            )
            for name in (
                "grill-me-2.1.0.zip",
                "generic-prompts-2.1.0.zip",
                "checksums-2.1.0.sha256",
            ):
                shutil.copyfile(source_dist / name, output / name)
            shutil.copyfile(
                output / "checksums-2.1.0.sha256", output / "checksums.sha256"
            )
            protected = {
                name: hashlib.sha256((output / name).read_bytes()).hexdigest()
                for name in (
                    "grill-me-2.1.0.zip",
                    "generic-prompts-2.1.0.zip",
                    "checksums-2.1.0.sha256",
                )
            }

            result = run_builder(output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "grill-me-3.0.0.zip").is_file())
            self.assertTrue((output / "generic-prompts-3.0.0.zip").is_file())
            self.assertTrue((output / "generic-prompts-2.1.0").is_dir())
            for name, digest in protected.items():
                self.assertEqual(
                    hashlib.sha256((output / name).read_bytes()).hexdigest(), digest
                )

    def test_repeated_build_replaces_valid_outputs_and_preserves_unknown_content(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            output.mkdir()
            sentinel = output / "maintainer-notes.txt"
            sentinel.write_text("keep me", encoding="utf-8")
            first = run_builder(output)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = tree_hashes(output)

            second = run_builder(output)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(tree_hashes(output), before)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep me")

    def test_unmanaged_collision_stops_without_partial_outputs(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            collision = output / "grill-me"
            collision.mkdir(parents=True)
            sentinel = collision / "unmanaged.txt"
            sentinel.write_text("do not replace", encoding="utf-8")

            result = run_builder(output)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(str(collision.resolve()), result.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "do not replace")
            self.assertFalse((output / "grill-me-3.0.0.zip").exists())
            self.assertFalse((output / "generic-prompts-3.0.0").exists())

    def test_failed_rebuild_preserves_prior_valid_release(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            output = root / "dist"
            first = run_builder(output)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = tree_hashes(output)

            broken = json.loads(CONFIG.read_text(encoding="utf-8"))
            broken["generic"]["source"] = "adapters/generic-prompts-missing"
            broken_config = root / "broken-release.json"
            broken_config.write_text(
                json.dumps(broken, ensure_ascii=False), encoding="utf-8"
            )
            failed = run_builder(output, broken_config)
            self.assertNotEqual(failed.returncode, 0)
            self.assertEqual(tree_hashes(output), before)
            self.assertFalse(any(output.glob(".release-staging-*")))

    def test_clean_builds_are_byte_reproducible_and_zips_match_directories(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            outputs = [root / "first", root / "second"]
            for output in outputs:
                result = run_builder(output)
                self.assertEqual(result.returncode, 0, result.stderr)

            for name in (
                "grill-me-3.0.0.zip",
                "generic-prompts-3.0.0.zip",
                "checksums.sha256",
            ):
                self.assertEqual(
                    (outputs[0] / name).read_bytes(),
                    (outputs[1] / name).read_bytes(),
                    name,
                )

            pairs = (
                ("grill-me", "grill-me-3.0.0.zip"),
                ("generic-prompts-3.0.0", "generic-prompts-3.0.0.zip"),
            )
            for directory_name, archive_name in pairs:
                directory = outputs[0] / directory_name
                with zipfile.ZipFile(outputs[0] / archive_name) as bundle:
                    archived = {
                        name for name in bundle.namelist() if not name.endswith("/")
                    }
                    local = {
                        f"{directory_name}/{path.relative_to(directory).as_posix()}"
                        for path in directory.rglob("*")
                        if path.is_file()
                    }
                    self.assertEqual(archived, local)
                    for name in local:
                        relative = name.removeprefix(f"{directory_name}/")
                        self.assertEqual(bundle.read(name), (directory / relative).read_bytes())


if __name__ == "__main__":
    unittest.main()
