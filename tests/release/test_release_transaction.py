import contextlib
import importlib.util
import io
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "scripts" / "build_release.py"
CONFIG = ROOT / "release" / "release.json"


def load_builder_module():
    spec = importlib.util.spec_from_file_location("release_builder_transaction", BUILDER)
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


def winerror_5(message: str = "simulated transient access denial") -> OSError:
    error = OSError(message)
    error.winerror = 5
    return error


def windows_error(code: int, message: str) -> OSError:
    error = OSError(message)
    error.winerror = code
    return error


def write_transaction_fixture(root: Path) -> tuple[Path, Path, dict[str, bytes]]:
    staging = root / "staging"
    output = root / "dist"
    staging.mkdir()
    output.mkdir()
    prior = {
        "first.txt": b"prior first",
        "second.txt": b"prior second",
    }
    for name, content in prior.items():
        (output / name).write_bytes(content)
        (staging / name).write_bytes(content.replace(b"prior", b"candidate"))
    return staging, output, prior


def read_outputs(output: Path, names: dict[str, bytes]) -> dict[str, bytes]:
    return {name: (output / name).read_bytes() for name in names}


class ReleaseTransactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = load_builder_module()

    def setUp(self) -> None:
        windows = mock.patch.object(self.builder, "IS_WINDOWS", True, create=True)
        windows.start()
        self.addCleanup(windows.stop)

    def test_transient_winerror_5_is_retried_until_replacement_succeeds(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            staging = root / "staging"
            output = root / "dist"
            staging.mkdir()
            output.mkdir()
            source = staging / "artifact.txt"
            target = output / source.name
            source.write_bytes(b"candidate")
            real_replace = self.builder.os.replace
            attempts = 0

            def transient_replace(replace_source: Path, replace_target: Path) -> None:
                nonlocal attempts
                if Path(replace_source) == source and Path(replace_target) == target:
                    attempts += 1
                    if attempts < 3:
                        raise winerror_5()
                real_replace(replace_source, replace_target)

            with mock.patch.object(
                self.builder.os, "replace", side_effect=transient_replace
            ):
                self.builder.commit(
                    staging,
                    output,
                    [source.name],
                    existing_names=[],
                )

            self.assertEqual(attempts, 3)
            self.assertEqual(target.read_bytes(), b"candidate")
            self.assertFalse(source.exists())

    def test_backup_movement_uses_the_same_winerror_5_retry_policy(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            staging, output, prior = write_transaction_fixture(Path(temporary))
            source = output / "first.txt"
            target = staging / ".previous-release" / "first.txt"
            real_replace = self.builder.os.replace
            attempts = 0

            def transient_backup_move(replace_source: Path, replace_target: Path) -> None:
                nonlocal attempts
                if Path(replace_source) == source and Path(replace_target) == target:
                    attempts += 1
                    if attempts < 3:
                        raise winerror_5("transient backup movement failure")
                real_replace(replace_source, replace_target)

            with (
                mock.patch.object(
                    self.builder.os, "replace", side_effect=transient_backup_move
                ),
                mock.patch.object(self.builder.time, "sleep") as sleep,
            ):
                self.builder.commit(
                    staging,
                    output,
                    list(prior),
                    existing_names=list(prior),
                )

            self.assertEqual(attempts, 3)
            self.assertEqual(sleep.call_count, 2)
            self.assertEqual(
                read_outputs(output, prior),
                {name: content.replace(b"prior", b"candidate") for name, content in prior.items()},
            )

    def test_persistent_winerror_5_stops_at_the_bounded_attempt_limit(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            staging = root / "staging"
            output = root / "dist"
            staging.mkdir()
            output.mkdir()
            source = staging / "artifact.txt"
            source.write_bytes(b"candidate")
            attempts = 0

            def persistent_failure(_source: Path, _target: Path) -> None:
                nonlocal attempts
                attempts += 1
                raise winerror_5("persistent access denial")

            with (
                mock.patch.object(
                    self.builder.os, "replace", side_effect=persistent_failure
                ),
                mock.patch.object(self.builder.time, "sleep") as sleep,
                self.assertRaisesRegex(
                    self.builder.BuildError, "Atomic release replacement failed"
                ),
            ):
                self.builder.commit(
                    staging,
                    output,
                    [source.name],
                    existing_names=[],
                )

            self.assertEqual(
                attempts, self.builder.WINDOWS_MANAGED_OUTPUT_MAX_ATTEMPTS
            )
            self.assertEqual(
                sleep.call_count,
                self.builder.WINDOWS_MANAGED_OUTPUT_MAX_ATTEMPTS - 1,
            )
            self.assertTrue(source.is_file())
            self.assertFalse((output / source.name).exists())

    def test_nonallowlisted_os_error_is_not_retried(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            staging = root / "staging"
            output = root / "dist"
            staging.mkdir()
            output.mkdir()
            source = staging / "artifact.txt"
            source.write_bytes(b"candidate")
            attempts = 0

            def structural_failure(_source: Path, _target: Path) -> None:
                nonlocal attempts
                attempts += 1
                raise windows_error(32, "simulated nonallowlisted error")

            with (
                mock.patch.object(
                    self.builder.os, "replace", side_effect=structural_failure
                ),
                mock.patch.object(self.builder.time, "sleep") as sleep,
                self.assertRaisesRegex(
                    self.builder.BuildError, "Atomic release replacement failed"
                ),
            ):
                self.builder.commit(
                    staging,
                    output,
                    [source.name],
                    existing_names=[],
                )

            self.assertEqual(attempts, 1)
            sleep.assert_not_called()
            self.assertTrue(source.is_file())
            self.assertFalse((output / source.name).exists())

    def test_winerror_5_is_not_retried_on_non_windows_platforms(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            staging = root / "staging"
            output = root / "dist"
            staging.mkdir()
            output.mkdir()
            source = staging / "artifact.txt"
            source.write_bytes(b"candidate")
            attempts = 0

            def non_windows_failure(_source: Path, _target: Path) -> None:
                nonlocal attempts
                attempts += 1
                raise winerror_5("simulated non-Windows access denial")

            with (
                mock.patch.object(self.builder, "IS_WINDOWS", False),
                mock.patch.object(
                    self.builder.os, "replace", side_effect=non_windows_failure
                ),
                mock.patch.object(self.builder.time, "sleep") as sleep,
                self.assertRaisesRegex(
                    self.builder.BuildError, "Atomic release replacement failed"
                ),
            ):
                self.builder.commit(
                    staging,
                    output,
                    [source.name],
                    existing_names=[],
                )

            self.assertEqual(attempts, 1)
            sleep.assert_not_called()

    def test_forward_failure_with_successful_recovery_restores_prior_release(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            staging, output, prior = write_transaction_fixture(Path(temporary))
            failed_source = staging / "second.txt"
            failed_target = output / "second.txt"
            real_replace = self.builder.os.replace
            primary_attempts = 0

            def fail_second_candidate(source: Path, target: Path) -> None:
                nonlocal primary_attempts
                if Path(source) == failed_source and Path(target) == failed_target:
                    primary_attempts += 1
                    raise winerror_5("persistent forward failure")
                real_replace(source, target)

            with (
                mock.patch.object(
                    self.builder.os, "replace", side_effect=fail_second_candidate
                ),
                mock.patch.object(self.builder.time, "sleep"),
                self.assertRaises(self.builder.BuildError) as caught,
            ):
                self.builder.commit(
                    staging,
                    output,
                    list(prior),
                    existing_names=list(prior),
                )

            self.assertEqual(
                primary_attempts, self.builder.WINDOWS_MANAGED_OUTPUT_MAX_ATTEMPTS
            )
            self.assertIn("candidate was not committed", str(caught.exception))
            self.assertEqual(read_outputs(output, prior), prior)
            self.assertEqual(list((staging / ".previous-release").iterdir()), [])

    def test_recovery_retries_winerror_5_while_removing_installed_candidate(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            staging, output, prior = write_transaction_fixture(Path(temporary))
            failed_source = staging / "second.txt"
            failed_target = output / "second.txt"
            candidate = output / "first.txt"
            real_replace = self.builder.os.replace
            real_remove = self.builder.remove_path
            removal_attempts = 0

            def fail_second_candidate(source: Path, target: Path) -> None:
                if Path(source) == failed_source and Path(target) == failed_target:
                    raise windows_error(32, "nonallowlisted forward failure")
                real_replace(source, target)

            def transient_candidate_removal(path: Path) -> None:
                nonlocal removal_attempts
                if Path(path) == candidate:
                    removal_attempts += 1
                    if removal_attempts < 3:
                        raise winerror_5("transient candidate removal failure")
                real_remove(path)

            with (
                mock.patch.object(
                    self.builder.os, "replace", side_effect=fail_second_candidate
                ),
                mock.patch.object(
                    self.builder,
                    "remove_path",
                    side_effect=transient_candidate_removal,
                ),
                mock.patch.object(self.builder.time, "sleep") as sleep,
                self.assertRaises(self.builder.BuildError) as caught,
            ):
                self.builder.commit(
                    staging,
                    output,
                    list(prior),
                    existing_names=list(prior),
                )

            self.assertNotIsInstance(
                caught.exception, self.builder.IncompleteRecoveryError
            )
            self.assertEqual(removal_attempts, 3)
            self.assertEqual(sleep.call_count, 2)
            self.assertEqual(read_outputs(output, prior), prior)
            self.assertEqual(list((staging / ".previous-release").iterdir()), [])

    def test_successful_restore_supersedes_exhausted_candidate_removal(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            staging, output, prior = write_transaction_fixture(Path(temporary))
            failed_source = staging / "second.txt"
            failed_target = output / "second.txt"
            candidate = output / "first.txt"
            real_replace = self.builder.os.replace
            real_remove = self.builder.remove_path
            removal_attempts = 0

            def fail_second_candidate(source: Path, target: Path) -> None:
                if Path(source) == failed_source and Path(target) == failed_target:
                    raise windows_error(32, "nonallowlisted forward failure")
                real_replace(source, target)

            def persistent_candidate_removal(path: Path) -> None:
                nonlocal removal_attempts
                if Path(path) == candidate:
                    removal_attempts += 1
                    raise winerror_5("persistent candidate removal failure")
                real_remove(path)

            with (
                mock.patch.object(
                    self.builder.os, "replace", side_effect=fail_second_candidate
                ),
                mock.patch.object(
                    self.builder,
                    "remove_path",
                    side_effect=persistent_candidate_removal,
                ),
                mock.patch.object(self.builder.time, "sleep") as sleep,
                self.assertRaises(self.builder.BuildError) as caught,
            ):
                self.builder.commit(
                    staging,
                    output,
                    list(prior),
                    existing_names=list(prior),
                )

            self.assertNotIsInstance(
                caught.exception, self.builder.IncompleteRecoveryError
            )
            self.assertIn("pre-build output state restored", str(caught.exception))
            self.assertNotIn("requires manual recovery", str(caught.exception))
            self.assertEqual(
                removal_attempts, self.builder.WINDOWS_MANAGED_OUTPUT_MAX_ATTEMPTS
            )
            self.assertEqual(
                sleep.call_count,
                self.builder.WINDOWS_MANAGED_OUTPUT_MAX_ATTEMPTS - 1,
            )
            self.assertEqual(read_outputs(output, prior), prior)
            self.assertEqual(list((staging / ".previous-release").iterdir()), [])

    def test_recovery_retries_transient_winerror_5_and_restores_prior_release(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            staging, output, prior = write_transaction_fixture(Path(temporary))
            failed_source = staging / "second.txt"
            failed_target = output / "second.txt"
            recovery_source = staging / ".previous-release" / "second.txt"
            real_replace = self.builder.os.replace
            primary_attempts = 0
            recovery_attempts = 0

            def fail_forward_then_recover(source: Path, target: Path) -> None:
                nonlocal primary_attempts, recovery_attempts
                source = Path(source)
                target = Path(target)
                if source == failed_source and target == failed_target:
                    primary_attempts += 1
                    raise winerror_5("persistent forward failure")
                if source == recovery_source and target == failed_target:
                    recovery_attempts += 1
                    if recovery_attempts < 3:
                        raise winerror_5("transient recovery failure")
                real_replace(source, target)

            with (
                mock.patch.object(
                    self.builder.os, "replace", side_effect=fail_forward_then_recover
                ),
                mock.patch.object(self.builder.time, "sleep"),
                self.assertRaisesRegex(
                    self.builder.BuildError, "Atomic release replacement failed"
                ),
            ):
                self.builder.commit(
                    staging,
                    output,
                    list(prior),
                    existing_names=list(prior),
                )

            self.assertEqual(
                primary_attempts, self.builder.WINDOWS_MANAGED_OUTPUT_MAX_ATTEMPTS
            )
            self.assertEqual(recovery_attempts, 3)
            self.assertEqual(read_outputs(output, prior), prior)
            self.assertEqual(list((staging / ".previous-release").iterdir()), [])

    def test_incomplete_recovery_reports_both_errors_and_recovery_paths(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            staging, output, prior = write_transaction_fixture(Path(temporary))
            failed_source = staging / "second.txt"
            failed_target = output / "second.txt"
            backup = staging / ".previous-release"
            recovery_source = backup / "second.txt"
            real_replace = self.builder.os.replace

            def fail_forward_and_recovery(source: Path, target: Path) -> None:
                source = Path(source)
                target = Path(target)
                if source == failed_source and target == failed_target:
                    raise winerror_5("persistent primary replacement failure")
                if source == recovery_source and target == failed_target:
                    raise winerror_5("persistent recovery replacement failure")
                real_replace(source, target)

            with (
                mock.patch.object(
                    self.builder.os, "replace", side_effect=fail_forward_and_recovery
                ),
                mock.patch.object(self.builder.time, "sleep"),
                self.assertRaises(self.builder.BuildError) as caught,
            ):
                self.builder.commit(
                    staging,
                    output,
                    list(prior),
                    existing_names=list(prior),
                )

            message = str(caught.exception)
            self.assertIn("candidate was not committed", message)
            self.assertIn("persistent primary replacement failure", message)
            self.assertIn("persistent recovery replacement failure", message)
            self.assertIn(str(staging.resolve()), message)
            self.assertIn(str(backup.resolve()), message)
            self.assertTrue((staging / "second.txt").is_file())
            self.assertEqual((backup / "second.txt").read_bytes(), prior["second.txt"])

    def test_main_preserves_recovery_data_after_incomplete_recovery(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            output = root / "dist"
            args = types.SimpleNamespace(
                config=CONFIG,
                output_root=output,
                allow_test_output_root=True,
                package="all",
            )
            with (
                mock.patch.object(self.builder, "parse_args", return_value=args),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(self.builder.main(), 0)

            real_replace = self.builder.os.replace
            primary_attempts = 0
            recovery_attempts = 0

            def fail_checksum_commit_and_recovery(source: Path, target: Path) -> None:
                nonlocal primary_attempts, recovery_attempts
                source = Path(source)
                target = Path(target)
                checksum_target = output / "checksums.sha256"
                if target == checksum_target and source.parent.name == ".previous-release":
                    recovery_attempts += 1
                    raise winerror_5("persistent recovery replacement failure")
                if (
                    target == checksum_target
                    and source.name == "checksums.sha256"
                    and source.parent != output
                ):
                    primary_attempts += 1
                    raise winerror_5("persistent primary replacement failure")
                real_replace(source, target)

            stderr = io.StringIO()
            with (
                mock.patch.object(self.builder, "parse_args", return_value=args),
                mock.patch.object(
                    self.builder.os,
                    "replace",
                    side_effect=fail_checksum_commit_and_recovery,
                ),
                mock.patch.object(self.builder.time, "sleep"),
                contextlib.redirect_stderr(stderr),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(self.builder.main(), 1)

            self.assertEqual(
                primary_attempts, self.builder.WINDOWS_MANAGED_OUTPUT_MAX_ATTEMPTS
            )
            self.assertEqual(
                recovery_attempts, self.builder.WINDOWS_MANAGED_OUTPUT_MAX_ATTEMPTS
            )
            recovery_roots = list(root.glob(".dist-release-staging-*"))
            self.assertEqual(len(recovery_roots), 1, recovery_roots)
            staging = recovery_roots[0]
            backup = staging / ".previous-release"
            self.assertTrue((staging / "checksums.sha256").is_file())
            self.assertTrue((backup / "checksums.sha256").is_file())
            self.assertFalse((output / "checksums.sha256").exists())
            message = stderr.getvalue()
            self.assertIn("persistent primary replacement failure", message)
            self.assertIn("persistent recovery replacement failure", message)
            self.assertIn(
                "active output is not a valid prior or candidate release and "
                "requires manual recovery",
                message,
            )
            self.assertIn(str(staging.resolve()), message)
            self.assertIn(str(backup.resolve()), message)


if __name__ == "__main__":
    unittest.main()
