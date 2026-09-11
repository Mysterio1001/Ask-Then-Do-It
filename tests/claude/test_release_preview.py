"""Offline packaging checks using explicitly synthetic runtime bytes."""
import contextlib
import hashlib
import io
import json
import tempfile
import types
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest import mock

from tests.release.test_release_transaction import load_builder_module


ROOT = Path(__file__).resolve().parents[2]
SOURCE = "adapters/claude-code/plugin/ask-then-do-it"
MODULES = (
    "orchestration.md", "lite-workflow.md", "requirements.md",
    "documented-requirements.md", "specification.md", "ticket-planning.md",
    "tdd-implementation.md", "direct-implementation.md", "review.md",
    "architecture-improvement.md",
)
RUNTIME = {
    ".claude-plugin/plugin.json", "skills/ask-then-do-it/SKILL.md",
    "skills/ask-then-do-it-5/SKILL.md", "agents/ask-then-do-it-reviewer.md",
    "hooks/hooks.json", "scripts/router.mjs", "config/model-classifications.json",
    "START-HERE.en.md", "START-HERE.zh-TW.md", "START-HERE.ja.md",
    *(f"profiles/{profile}/{name}" for profile in ("general", "claude-5") for name in MODULES),
}
LEGAL = {"LICENSE", "THIRD_PARTY_NOTICES.md"}
ARCHIVE = "claude/ask-then-do-it-claude-1.4.0-preview.1.zip"


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


class ClaudeReleasePreviewTests(unittest.TestCase):
    def setUp(self):
        self.builder = load_builder_module()
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / SOURCE
        for name in RUNTIME:
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"Synthetic packaging fixture only: {name}\n", encoding="utf-8")
        (self.source / ".claude-plugin/plugin.json").write_text(json.dumps({
            "name": "ask-then-do-it", "displayName": "Ask Then Do It", "version": "1.4.0-preview.1",
        }), encoding="utf-8")
        for name in LEGAL:
            (self.root / name).write_text(f"Synthetic legal fixture: {name}\n", encoding="utf-8")
        self.output = self.root / "isolated-preview"
        for name, value in (("ROOT", self.root), ("DEFAULT_OUTPUT", self.root / "dist")):
            patch = mock.patch.object(self.builder, name, value)
            patch.start()
            self.addCleanup(patch.stop)

    def run_preview(self, output=None, **overrides):
        args = types.SimpleNamespace(
            config=self.builder.DEFAULT_CONFIG, output_root=output or self.output,
            allow_test_output_root=True, package="all", preview_claude=True,
        )
        for key, value in overrides.items():
            setattr(args, key, value)
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(self.builder, "parse_args", return_value=args), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = self.builder.main()
        return result, stdout.getvalue(), stderr.getvalue()

    def test_cli_explicit_preview_mode_is_supported(self):
        with mock.patch("sys.argv", ["build_release.py", "--preview-claude", "--output-root", str(self.output), "--allow-test-output-root"]):
            try:
                args = self.builder.parse_args()
            except SystemExit as exc:
                self.fail(f"Explicit offline Claude preview option is unavailable: {exc}")
        self.assertTrue(args.preview_claude)

    def test_preview_exact_bytes_inventory_and_reproducibility(self):
        before = snapshot(self.source)
        first = self.run_preview()
        self.assertEqual(first[0], 0, first)
        self.assertIn("NOT A RELEASE", first[1])
        self.assertEqual({p.name for p in self.output.iterdir()}, {"claude", "checksums.sha256", "preview.json"})
        package = self.output / "claude/ask-then-do-it"
        expected = {**before, **{name: (self.root / name).read_bytes() for name in LEGAL}}
        self.assertEqual(snapshot(package), expected)
        with zipfile.ZipFile(self.output / ARCHIVE) as archive:
            self.assertEqual(archive.namelist(), sorted(f"ask-then-do-it/{name}" for name in expected))
            for name, content in expected.items():
                self.assertEqual(archive.read(f"ask-then-do-it/{name}"), content)
            self.assertTrue(all(i.date_time == (1980, 1, 1, 0, 0, 0) for i in archive.infolist()))
        checksums = (self.output / "checksums.sha256").read_text()
        self.assertEqual(checksums, hashlib.sha256((self.output / ARCHIVE).read_bytes()).hexdigest() + "  " + ARCHIVE + "\n")
        marker = json.loads((self.output / "preview.json").read_text())
        self.assertEqual(marker["status"], "not-a-release")
        self.assertEqual(marker["evidence_claim"], "packaging-only-no-host-or-model-verification")
        self.assertEqual(marker["source_sha256"], {name: hashlib.sha256(data).hexdigest() for name, data in expected.items()})
        second = self.root / "second-preview"
        self.assertEqual(self.run_preview(second)[0], 0)
        self.assertEqual(snapshot(self.output), snapshot(second))
        self.assertEqual(snapshot(self.source), before)

    def test_preview_requires_explicit_isolation_and_never_touches_default_dist(self):
        for target, overrides in (
            (self.root / "dist", {}), (self.root / "dist/nested", {}),
            (self.source / "preview", {}), (self.root, {}),
            (self.output, {"allow_test_output_root": False}),
        ):
            with self.subTest(target=target, overrides=overrides):
                before = snapshot(self.root)
                result = self.run_preview(target, **overrides)
                self.assertNotEqual(result[0], 0)
                self.assertEqual(snapshot(self.root), before)

    def test_preview_rejects_extra_missing_or_wrong_version_source_before_output(self):
        for mutation in ("extra", "missing", "wrong-version", "empty-directory"):
            with self.subTest(mutation=mutation):
                if mutation == "extra":
                    changed = self.source / ".claude-plugin/marketplace.json"
                    changed.write_text("{}")
                elif mutation == "missing":
                    changed = self.source / "START-HERE.en.md"
                    old = changed.read_bytes()
                    changed.unlink()
                elif mutation == "wrong-version":
                    changed = self.source / ".claude-plugin/plugin.json"
                    old = changed.read_bytes()
                    changed.write_text('{"name":"ask-then-do-it","displayName":"Ask Then Do It","version":"9.9.9"}')
                else:
                    changed = self.source / "local-state"
                    changed.mkdir()
                result = self.run_preview()
                self.assertNotEqual(result[0], 0, result)
                self.assertFalse(self.output.exists())
                if mutation == "extra":
                    changed.unlink()
                elif mutation == "empty-directory":
                    changed.rmdir()
                else:
                    changed.write_bytes(old)

    def test_nonmanaged_content_and_marker_tampering_are_preserved(self):
        self.output.mkdir()
        (self.output / "personal.txt").write_text("keep me")
        before = snapshot(self.output)
        result = self.run_preview()
        self.assertNotEqual(result[0], 0, result)
        self.assertEqual(snapshot(self.output), before)
        (self.output / "personal.txt").unlink()
        self.assertEqual(self.run_preview()[0], 0)
        (self.output / "preview.json").write_text('{"status":"Completed"}')
        before = snapshot(self.output)
        self.assertNotEqual(self.run_preview()[0], 0)
        self.assertEqual(snapshot(self.output), before)

    def test_source_byte_drift_is_caught_even_with_matching_zip_and_checksums(self):
        self.assertEqual(self.run_preview()[0], 0)
        config = self.builder.claude_preview_config()
        package = self.output / "claude/ask-then-do-it"
        (package / "scripts/router.mjs").write_text("wrong bytes")
        self.builder.write_reproducible_zip(package, self.output / ARCHIVE, "ask-then-do-it")
        (self.output / "checksums.sha256").write_text(self.builder.sha256(self.output / ARCHIVE) + "  " + ARCHIVE + "\n")
        with self.assertRaisesRegex(self.builder.BuildError, "source|parity|differs"):
            self.builder.validate_output_set(self.output, config, ["claude"], allow_absent=False, require_source_equivalence=True)

    def test_preview_replacement_uses_shared_transaction_rollback(self):
        self.assertEqual(self.run_preview()[0], 0)
        before = snapshot(self.output)
        (self.source / "scripts/router.mjs").write_text("updated synthetic bytes")
        real_replace = self.builder.replace_managed_path
        def fail_candidate_marker(source, target):
            if Path(target) == self.output / "preview.json" and Path(source).parent.name != ".previous-release":
                raise OSError("simulated candidate placement failure")
            real_replace(source, target)
        with mock.patch.object(self.builder, "replace_managed_path", side_effect=fail_candidate_marker):
            result = self.run_preview()
        self.assertNotEqual(result[0], 0)
        self.assertIn("pre-build output state restored", result[2])
        self.assertEqual(snapshot(self.output), before)

    def test_duplicate_zip_member_and_extra_provider_file_are_rejected(self):
        self.assertEqual(self.run_preview()[0], 0)
        config = self.builder.claude_preview_config()
        archive_path = self.output / ARCHIVE
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(archive_path, "a") as archive:
                archive.writestr("ask-then-do-it/LICENSE", (self.root / "LICENSE").read_bytes())
        (self.output / "checksums.sha256").write_text(self.builder.sha256(archive_path) + "  " + ARCHIVE + "\n")
        with self.assertRaisesRegex(self.builder.BuildError, "duplicate|ZIP inventory"):
            self.builder.validate_output_set(self.output, config, ["claude"], allow_absent=False, require_source_equivalence=True)
        package = self.output / "claude/ask-then-do-it"
        self.builder.write_reproducible_zip(package, archive_path, "ask-then-do-it")
        (self.output / "checksums.sha256").write_text(self.builder.sha256(archive_path) + "  " + ARCHIVE + "\n")
        (self.output / "claude/local-state.json").write_text("{}")
        with self.assertRaisesRegex(self.builder.BuildError, "inventory|Unmanaged"):
            self.builder.validate_output_set(self.output, config, ["claude"], allow_absent=False, require_source_equivalence=True)

    def test_link_source_is_rejected_and_formal_activation_needs_conformance(self):
        real_link = self.builder.claude_package.is_link
        target = self.source / "profiles"
        with mock.patch.object(self.builder.claude_package, "is_link", side_effect=lambda path: Path(path) == target or real_link(path)):
            result = self.run_preview()
        self.assertNotEqual(result[0], 0)
        self.assertIn("link", result[2])
        self.assertFalse(self.output.exists())
        config = self.builder.claude_preview_config()
        del config["offline_preview"]
        config["release_version"] = config["core_version"] = "1.4.1"
        (self.source / ".claude-plugin/plugin.json").write_text(json.dumps({
            "name": "ask-then-do-it", "displayName": "Ask Then Do It", "version": "1.4.1",
        }), encoding="utf-8")
        config["claude"]["archive"] = "claude/ask-then-do-it-claude-1.4.1.zip"
        config["claude"]["inventory"] = sorted(RUNTIME | LEGAL)
        config["required_validation_checks"] = [
            "claude-plugin-validation", "claude-conformance", "claude-package-inventory",
            "claude-behavior", "claude-context", "claude-live-smoke",
        ]
        with self.assertRaisesRegex(self.builder.BuildError, "canonical declaration"):
            self.builder.validate_claude_config(config)
        declaration = self.root / "adapters/claude-code/conformance.yaml"
        declaration.write_text("adapter_id: claude-code\ntarget: claude-code-plugin\nadapter_version: 1.4.1\ncore_version: 1.4.1\n")
        self.builder.validate_claude_config(config)
        config["required_validation_checks"].remove("claude-live-smoke")
        with self.assertRaisesRegex(self.builder.BuildError, "validation checks"):
            self.builder.validate_claude_config(config)

    def test_zip_directories_and_noncanonical_metadata_are_rejected(self):
        self.assertEqual(self.run_preview()[0], 0)
        config = self.builder.claude_preview_config()
        archive_path = self.output / ARCHIVE
        original = archive_path.read_bytes()
        for mutation in ("empty-directory", "traversal-directory", "symlink", "timestamp", "compression"):
            with self.subTest(mutation=mutation):
                archive_path.write_bytes(original)
                with zipfile.ZipFile(archive_path) as archive:
                    entries = [(info, archive.read(info)) for info in archive.infolist()]
                with zipfile.ZipFile(archive_path, "w") as archive:
                    for index, (info, content) in enumerate(entries):
                        if index == 0:
                            if mutation == "symlink":
                                info.external_attr = 0o120777 << 16
                            elif mutation == "timestamp":
                                info.date_time = (2020, 1, 1, 0, 0, 0)
                            elif mutation == "compression":
                                info.compress_type = zipfile.ZIP_STORED
                        archive.writestr(info, content)
                    if mutation in ("empty-directory", "traversal-directory"):
                        archive.writestr("unexpected/" if mutation == "empty-directory" else "../outside/", b"")
                (self.output / "checksums.sha256").write_text(self.builder.sha256(archive_path) + "  " + ARCHIVE + "\n")
                with self.assertRaisesRegex(self.builder.BuildError, "ZIP"):
                    self.builder.validate_output_set(self.output, config, ["claude"], allow_absent=False, require_source_equivalence=True)
                with self.assertRaisesRegex(self.builder.BuildError, "ZIP"):
                    self.builder.validate_existing_output_set(self.output, config, ["claude"])


if __name__ == "__main__":
    unittest.main()
