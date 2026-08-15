import hashlib
import json
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


def write_prior_release(output: Path) -> None:
    archives = []
    for provider, directory_name, archive_name in (
        ("codex", "ask-then-do-it", "ask-then-do-it-1.1.0.zip"),
        ("generic", "ask-then-do-it-generic-1.1.0", "ask-then-do-it-generic-1.1.0.zip"),
    ):
        package = output / provider / directory_name
        package.mkdir(parents=True)
        payload = package / "version.txt"
        payload.write_text("1.1.0\n", encoding="utf-8")
        archive = output / provider / archive_name
        with zipfile.ZipFile(archive, "w") as bundle:
            bundle.write(payload, f"{directory_name}/version.txt")
        archives.append(archive)
    (output / "checksums.sha256").write_text(
        "".join(
            f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  "
            f"{archive.relative_to(output).as_posix()}\n"
            for archive in archives
        ),
        encoding="ascii",
    )


class ReleaseSafetyTests(unittest.TestCase):
    def test_unmanaged_content_blocks_build_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            output.mkdir()
            sentinel = output / "maintainer-notes.txt"
            sentinel.write_text("keep me", encoding="utf-8")

            result = run_builder(output)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unmanaged or incomplete output collision", result.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep me")
            self.assertEqual({path.name for path in output.iterdir()}, {sentinel.name})

    def test_repeated_build_replaces_only_a_complete_valid_output_set(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            first = run_builder(output)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = tree_hashes(output)

            second = run_builder(output)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(tree_hashes(output), before)

    def test_complete_verified_prior_release_can_be_upgraded_atomically(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            write_prior_release(output)

            result = run_builder(output)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((output / "codex" / "ask-then-do-it-1.1.0.zip").exists())
            self.assertFalse(
                (output / "generic" / "ask-then-do-it-generic-1.1.0.zip").exists()
            )
            self.assertTrue((output / "codex" / "ask-then-do-it-1.3.0.zip").is_file())
            self.assertTrue(
                (output / "generic" / "ask-then-do-it-generic-1.3.0.zip").is_file()
            )

    def test_unmanaged_collision_stops_without_partial_outputs(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            collision = output / "codex"
            collision.mkdir(parents=True)
            sentinel = collision / "unmanaged.txt"
            sentinel.write_text("do not replace", encoding="utf-8")

            result = run_builder(output)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(str(collision.resolve()), result.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "do not replace")
            self.assertFalse((output / "generic").exists())
            self.assertFalse((output / "checksums.sha256").exists())

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
            self.assertFalse(any(root.glob(".dist-release-staging-*")))

    def test_clean_builds_are_byte_reproducible_and_zips_match_directories(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            outputs = [root / "first", root / "second"]
            for output in outputs:
                result = run_builder(output)
                self.assertEqual(result.returncode, 0, result.stderr)

            for name in (
                "codex/ask-then-do-it-1.3.0.zip",
                "generic/ask-then-do-it-generic-1.3.0.zip",
                "checksums.sha256",
            ):
                self.assertEqual(
                    (outputs[0] / name).read_bytes(),
                    (outputs[1] / name).read_bytes(),
                    name,
                )

            pairs = (
                ("codex/ask-then-do-it", "codex/ask-then-do-it-1.3.0.zip", "ask-then-do-it"),
                (
                    "generic/ask-then-do-it-generic-1.3.0",
                    "generic/ask-then-do-it-generic-1.3.0.zip",
                    "ask-then-do-it-generic-1.3.0",
                ),
            )
            for directory_name, archive_name, archive_root in pairs:
                directory = outputs[0] / directory_name
                with zipfile.ZipFile(outputs[0] / archive_name) as bundle:
                    archived = {
                        name for name in bundle.namelist() if not name.endswith("/")
                    }
                    local = {
                        f"{archive_root}/{path.relative_to(directory).as_posix()}"
                        for path in directory.rglob("*")
                        if path.is_file()
                    }
                    self.assertEqual(archived, local)
                    for name in local:
                        relative = name.removeprefix(f"{archive_root}/")
                        self.assertEqual(bundle.read(name), (directory / relative).read_bytes())


if __name__ == "__main__":
    unittest.main()
