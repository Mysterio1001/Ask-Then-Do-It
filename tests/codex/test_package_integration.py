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
CONTRACT_VALIDATOR = ROOT / "scripts" / "validate_codex_contract.py"
ADAPTER = ROOT / "adapters" / "codex"
SOURCE_PLUGIN = ADAPTER / "plugin" / "ask-then-do-it"
RULE_MAPPING = ADAPTER / "rule-mapping.yaml"
CORE_CATALOG = ROOT / "core" / "rules" / "rules.yaml"
CONFORMANCE = ADAPTER / "conformance.yaml"
BASELINE = ROOT / "docs" / "evidence" / "codex-skill-runtime-slimming-t1-baseline.json"

EXPECTED_REFERENCES = {
    "skills/ask-then-do-it/references/architecture-refactoring-lenses.md",
    "skills/ask-then-do-it/references/artifact-contract.md",
    "skills/ask-then-do-it/references/full-routing.md",
    "skills/ask-then-do-it/references/lite-workflow.md",
}


def relative_files(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_codex(output_root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(BUILDER),
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


class CodexPackageIntegrationTests(unittest.TestCase):
    def test_isolated_package_contains_references_and_matches_source(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "codex-build"
            result = build_codex(output)
            self.assertEqual(result.returncode, 0, result.stderr)

            package = output / "codex" / "ask-then-do-it"
            self.assertTrue(package.is_dir())
            self.assertTrue(EXPECTED_REFERENCES <= relative_files(package))
            self.assertFalse(
                any(
                    path.relative_to(package).parts[0] in {"generic", "claude", "core"}
                    for path in package.rglob("*")
                    if path.is_file()
                )
            )
            self.assertFalse((package / "AGENTS.md").exists())

            source_files = relative_files(SOURCE_PLUGIN)
            source_files.update({"LICENSE", "THIRD_PARTY_NOTICES.md"})
            self.assertEqual(relative_files(package), source_files)
            for relative in source_files:
                source = SOURCE_PLUGIN / relative
                if not source.is_file():
                    source = ROOT / relative
                self.assertEqual(
                    (package / relative).read_bytes(),
                    source.read_bytes(),
                    relative,
                )

            validation = subprocess.run(
                [
                    sys.executable,
                    str(CONTRACT_VALIDATOR),
                    "--adapter-root",
                    str(ADAPTER),
                    "--source-package-root",
                    str(SOURCE_PLUGIN),
                    "--package-root",
                    str(package),
                    "--rule-mapping",
                    str(RULE_MAPPING),
                    "--core-catalog",
                    str(CORE_CATALOG),
                    "--conformance",
                    str(CONFORMANCE),
                    "--json",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(validation.returncode, 0, validation.stderr)
            report = json.loads(validation.stdout)
            self.assertFalse(report["package"]["package_matches_source"])
            self.assertEqual(
                set(report["validation"]["reference_targets"]),
                EXPECTED_REFERENCES,
            )

    def test_two_isolated_builds_are_reproducible_and_zip_equivalent(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            outputs = [root / "first", root / "second"]
            for output in outputs:
                result = build_codex(output)
                self.assertEqual(result.returncode, 0, result.stderr)

            first_package = outputs[0] / "codex" / "ask-then-do-it"
            second_package = outputs[1] / "codex" / "ask-then-do-it"
            self.assertEqual(relative_files(first_package), relative_files(second_package))
            for relative in relative_files(first_package):
                self.assertEqual(
                    (first_package / relative).read_bytes(),
                    (second_package / relative).read_bytes(),
                    relative,
                )

            archive_name = "codex/ask-then-do-it-1.4.2.zip"
            first_archive = outputs[0] / archive_name
            second_archive = outputs[1] / archive_name
            self.assertEqual(first_archive.read_bytes(), second_archive.read_bytes())
            self.assertEqual(
                (outputs[0] / "checksums.sha256").read_bytes(),
                (outputs[1] / "checksums.sha256").read_bytes(),
            )
            self.assertEqual(sha256(first_archive), (outputs[0] / "checksums.sha256").read_text(encoding="ascii").split()[0])

            archive_root = "ask-then-do-it"
            expected_members = {
                f"{archive_root}/{relative}" for relative in relative_files(first_package)
            }
            with zipfile.ZipFile(first_archive) as archive:
                actual_members = {
                    name for name in archive.namelist() if not name.endswith("/")
                }
                self.assertEqual(actual_members, expected_members)
                for name in expected_members:
                    relative = name.removeprefix(f"{archive_root}/")
                    self.assertEqual(
                        archive.read(name),
                        (first_package / relative).read_bytes(),
                    )

    def test_after_proxy_reports_stage_entry_and_action_ready_context(self) -> None:
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        current = subprocess.run(
            [
                sys.executable,
                str(CONTRACT_VALIDATOR),
                "--json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(current.returncode, 0, current.stderr)
        report = json.loads(current.stdout)

        self.assertEqual(set(report["load_sets"]), set(baseline["load_sets"]))
        self.assertEqual(
            set(report["action_ready_load_sets"]),
            set(baseline["load_sets"]),
        )
        self.assertLess(
            report["load_sets"]["root-router"]["loaded_context_proxy"],
            baseline["load_sets"]["root-router"]["loaded_context_proxy"],
        )
        self.assertLess(
            report["load_sets"]["lite"]["loaded_context_proxy"],
            baseline["load_sets"]["lite"]["loaded_context_proxy"],
        )
        artifact_contract = (
            "skills/ask-then-do-it/references/artifact-contract.md"
        )
        lens_contract = (
            "skills/ask-then-do-it/references/architecture-refactoring-lenses.md"
        )
        for route, entry_set in report["load_sets"].items():
            load_set = report["action_ready_load_sets"][route]
            self.assertLessEqual(
                entry_set["loaded_context_proxy"],
                load_set["loaded_context_proxy"],
                route,
            )
            if route.startswith("full-"):
                self.assertIn(
                    "skills/ask-then-do-it/references/full-routing.md",
                    load_set["sources"],
                    route,
                )
                self.assertIn(artifact_contract, load_set["sources"], route)
                self.assertNotIn(artifact_contract, entry_set["sources"], route)
            if route in {"full-review", "full-architecture"}:
                self.assertIn(lens_contract, load_set["sources"], route)
                self.assertNotIn(lens_contract, entry_set["sources"], route)


if __name__ == "__main__":
    unittest.main()
