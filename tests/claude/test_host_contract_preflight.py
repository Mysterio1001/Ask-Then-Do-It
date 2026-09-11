import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_claude_host_contract.py"
UNVERIFIED_CONTRACT = (
    ROOT / "tests" / "claude" / "fixtures" / "host-contract" / "contract.json"
)

STRICT_CHECKS = (
    "canonical-plugin-strict-validation",
    "marketplace-strict-validation",
    "compatibility-plugin-strict-validation",
)
ENTRY_CHECKS = (
    "automatic-entry-expansion",
    "explicit-entry-expansion",
)
FAILURE_CHECKS = (
    "node-unavailable",
    "handler-nonzero",
    "handler-exit-2",
    "handler-timeout",
)
BARE_ALIAS_CHECK = "bare-alias-observation"
OFFICIAL_BINARY_URL = (
    "https://downloads.claude.ai/claude-code-releases/2.1.251/"
    "win32-x64/claude.exe"
)
OFFICIAL_BINARY_SHA256 = (
    "8d1229a281281b98fd2dee72b3253a704be4fce4d45207200cd32a9bb5a6c909"
)
OFFICIAL_BINARY_SIZE = 217360032
FIXTURE_SUBJECT = "tests/claude/fixtures/host-contract/plugin"
SUBJECTS = {
    "canonical-plugin-strict-validation": (
        "adapters/claude-code/plugin/ask-then-do-it"
    ),
    "marketplace-strict-validation": ".claude-plugin/marketplace.json",
    "compatibility-plugin-strict-validation": FIXTURE_SUBJECT,
    "automatic-entry-expansion": FIXTURE_SUBJECT,
    "explicit-entry-expansion": FIXTURE_SUBJECT,
    "node-unavailable": FIXTURE_SUBJECT,
    "handler-nonzero": FIXTURE_SUBJECT,
    "handler-exit-2": FIXTURE_SUBJECT,
    "handler-timeout": FIXTURE_SUBJECT,
    BARE_ALIAS_CHECK: FIXTURE_SUBJECT,
}


def run_validator(
    ledger: Path, evidence_root: Path
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-B",
            str(VALIDATOR),
            "--ledger",
            str(ledger),
            "--evidence-root",
            str(evidence_root),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def subject_digest(relative: str) -> str:
    subject = ROOT / relative
    if subject.is_file():
        return hashlib.sha256(subject.read_bytes()).hexdigest()
    digest = hashlib.sha256()
    for path in sorted(item for item in subject.rglob("*") if item.is_file()):
        name = path.relative_to(subject).as_posix().encode()
        digest.update(name)
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def write_raw_record(
    root: Path, check: dict, environment: dict, result: dict
) -> dict[str, str]:
    check_id = check["id"]
    path = root / f"{check_id}.json"
    record = {
        "schema_version": 1,
        "check_id": check_id,
        "observed_at": check["observed_at"],
        "binary": {
            "source_url": environment["binary_source_url"],
            "sha256": environment["binary_sha256"],
            "size": environment["binary_size"],
            "version": environment["reported_version"],
            "platform": environment["binary_platform"],
        },
        "node_version": environment["node_version"],
        "execution": {
            "executor": check["executor"],
            "argv": check["argv"],
            "exit_code": check["exit_code"],
            "timed_out": check["timed_out"],
            "warnings": check["warnings"],
        },
        "subject": check["subject"],
        "result": result,
        "stdout": "scrubbed validator negative-test capture",
        "stderr": "",
    }
    content = json.dumps(record, indent=2).encode()
    path.write_bytes(content)
    return {
        "path": path.name,
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def claimed_observed_contract(evidence_root: Path) -> dict:
    """Build an adversarial claim for negative validator tests only."""
    observed_at = "2026-09-06T00:00:00Z"
    environment = {
        "binary_source_url": OFFICIAL_BINARY_URL,
        "binary_sha256": OFFICIAL_BINARY_SHA256,
        "binary_size": OFFICIAL_BINARY_SIZE,
        "binary_platform": "win32-x64",
        "reported_version": "2.1.251",
        "os": "windows",
        "surface": "terminal-cli",
        "node_version": "24.19.0",
        "executed_at": observed_at,
    }

    def common(check_id: str, argv: list[str]) -> dict:
        relative = SUBJECTS[check_id]
        return {
            "id": check_id,
            "status": "passed",
            "evidence_kind": "observed",
            "observed_at": observed_at,
            "executor": "claude",
            "argv": argv,
            "exit_code": 0,
            "timed_out": False,
            "warnings": [],
            "subject": {
                "path": relative,
                "sha256": subject_digest(relative),
            },
        }

    checks = []
    for check_id in STRICT_CHECKS:
        target = SUBJECTS[check_id]
        argv_target = "." if check_id == "marketplace-strict-validation" else target
        check = common(check_id, ["plugin", "validate", argv_target, "--strict"])
        check["outcome"] = "strict validation completed without warnings"
        result = {"kind": "strict-validation", "warning_count": 0}
        check["raw_evidence"] = write_raw_record(
            evidence_root, check, environment, result
        )
        checks.append(check)
    for check_id in ENTRY_CHECKS:
        command_name = f"opaque-{check_id}"
        check = common(
            check_id,
            ["--plugin-dir", FIXTURE_SUBJECT, "--print", f"/{command_name}"],
        )
        check.update(
            {
                "command_name": command_name,
                "command_source": "plugin",
                "hook_triggered": True,
                "additional_context_visible": True,
                "nonce_sha256": "b" * 64,
                "outcome": "nonce context was visible to the invoked Skill",
            }
        )
        result = {
            "kind": "entry-expansion",
            "command_name": command_name,
            "command_source": "plugin",
            "hook_triggered": True,
            "additional_context_visible": True,
            "nonce_sha256": check["nonce_sha256"],
        }
        check["raw_evidence"] = write_raw_record(
            evidence_root, check, environment, result
        )
        checks.append(check)
    for check_id in FAILURE_CHECKS:
        check = common(
            check_id,
            ["--plugin-dir", FIXTURE_SUBJECT, "--print", "/failure-observation"],
        )
        check.update(
            {
                "host_result": "skill-expanded-without-context",
                "outcome": "typed host result was captured",
            }
        )
        result = {
            "kind": "failure-semantics",
            "host_result": check["host_result"],
        }
        check["raw_evidence"] = write_raw_record(
            evidence_root, check, environment, result
        )
        checks.append(check)

    aliases = [
        {"entry": "ask-then-do-it", "state": "present"},
        {"entry": "ask-then-do-it-5", "state": "absent"},
    ]
    alias_check = common(
        BARE_ALIAS_CHECK,
        ["--plugin-dir", FIXTURE_SUBJECT, "plugin", "details", "ask-then-do-it"],
    )
    alias_check.update(
        {
            "observation_scope": "observed-only",
            "observations": aliases,
            "outcome": "bare aliases were recorded without a product guarantee",
        }
    )
    alias_check["raw_evidence"] = write_raw_record(
        evidence_root,
        alias_check,
        environment,
        {
            "kind": "bare-alias-observation",
            "observation_scope": "observed-only",
            "observations": aliases,
        },
    )
    checks.append(alias_check)
    return {
        "schema_version": 1,
        "target_claude_code_version": "2.1.251",
        "status": "passed",
        "evidence_kind": "observed",
        "environment": environment,
        "checks": checks,
    }


class ClaudeHostContractPreflightTests(unittest.TestCase):
    def validate_mutation(self, mutate) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            evidence_root = root / "raw"
            evidence_root.mkdir()
            value = claimed_observed_contract(evidence_root)
            mutate(value)
            ledger = root / "contract.json"
            ledger.write_text(json.dumps(value, indent=2), encoding="utf-8")
            return run_validator(ledger, evidence_root)

    def test_missing_and_unverified_contracts_are_rejected(self) -> None:
        missing = run_validator(ROOT / "missing-host-contract.json", ROOT)
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("missing", missing.stderr.lower())

        unverified = run_validator(UNVERIFIED_CONTRACT, UNVERIFIED_CONTRACT.parent)
        self.assertNotEqual(unverified.returncode, 0)
        self.assertIn("unverified", unverified.stderr.lower())

    def test_exact_binary_version_and_source_are_required(self) -> None:
        mutations = {
            "missing-binary": lambda value: value["environment"].update(
                {"binary_source_url": ""}
            ),
            "wrong-target": lambda value: value.update(
                {"target_claude_code_version": "2.1.252"}
            ),
            "wrong-reported-version": lambda value: value["environment"].update(
                {"reported_version": "2.1.252"}
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                result = self.validate_mutation(mutate)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                expected = "binary" if label == "missing-binary" else "2.1.251"
                self.assertIn(expected, result.stderr.lower())

    def test_strict_validation_warning_is_rejected(self) -> None:
        def add_warning(value: dict) -> None:
            value["checks"][0]["warnings"] = ["native warning"]

        result = self.validate_mutation(add_warning)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("warning", result.stderr.lower())

    def test_missing_entry_context_is_rejected(self) -> None:
        def hide_context(value: dict) -> None:
            entry = next(
                check
                for check in value["checks"]
                if check["id"] == "automatic-entry-expansion"
            )
            entry["additional_context_visible"] = False

        result = self.validate_mutation(hide_context)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("additional context", result.stderr.lower())

    def test_simulated_evidence_cannot_claim_an_observed_pass(self) -> None:
        def mark_simulated(value: dict) -> None:
            value["checks"][-1]["evidence_kind"] = "simulated"

        result = self.validate_mutation(mark_simulated)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("observed", result.stderr.lower())

    def test_missing_raw_digest_is_rejected(self) -> None:
        def remove_digest(value: dict) -> None:
            del value["checks"][0]["raw_evidence"]["sha256"]

        result = self.validate_mutation(remove_digest)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("raw evidence", result.stderr.lower())

    def test_duplicate_and_unknown_checks_are_rejected(self) -> None:
        def duplicate(value: dict) -> None:
            value["checks"].append(copy.deepcopy(value["checks"][0]))

        def add_unknown(value: dict) -> None:
            unknown = copy.deepcopy(value["checks"][0])
            unknown["id"] = "future-unapproved-check"
            value["checks"].append(unknown)

        for label, mutate in {"duplicate": duplicate, "unknown": add_unknown}.items():
            with self.subTest(label=label):
                result = self.validate_mutation(mutate)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(label, result.stderr.lower())

    def test_freeform_claim_without_execution_bound_records_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            evidence_root = root / "raw"
            evidence_root.mkdir()
            value = claimed_observed_contract(evidence_root)
            raw = value["checks"][0]["raw_evidence"]
            content = b"arbitrary free-form log\n"
            (evidence_root / raw["path"]).write_bytes(content)
            raw["sha256"] = hashlib.sha256(content).hexdigest()
            ledger = root / "contract.json"
            ledger.write_text(json.dumps(value), encoding="utf-8")
            result = run_validator(ledger, evidence_root)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("execution-bound raw record", result.stderr.lower())

    def test_official_binary_and_validated_runtime_facts_are_exact(self) -> None:
        mutations = {
            "source-url": lambda value: value["environment"].update(
                {"binary_source_url": "https://example.invalid/claude.exe"}
            ),
            "binary-sha": lambda value: value["environment"].update(
                {"binary_sha256": "a" * 64}
            ),
            "node-version": lambda value: value["environment"].update(
                {"node_version": "not-a-version"}
            ),
            "timestamp": lambda value: value["environment"].update(
                {"executed_at": "sometime"}
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                result = self.validate_mutation(mutate)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(label.split("-")[0], result.stderr.lower())

    def test_unapproved_opaque_command_identity_is_rejected(self) -> None:
        result = self.validate_mutation(lambda value: None)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("command identity", result.stderr.lower())

    def test_unapproved_failure_predicates_remain_blocking_after_command_names_are_known(
        self,
    ) -> None:
        spec = importlib.util.spec_from_file_location(
            "ticket3_host_contract_validator", VALIDATOR
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            evidence_root = root / "raw"
            evidence_root.mkdir()
            value = claimed_observed_contract(evidence_root)
            ledger = root / "contract.json"
            ledger.write_text(json.dumps(value), encoding="utf-8")
            entries = {
                check["id"]: check["command_name"]
                for check in value["checks"]
                if check["id"] in ENTRY_CHECKS
            }
            validator.APPROVED_COMMAND_NAMES.update(entries)

            with self.assertRaisesRegex(
                validator.HostContractError,
                "node-unavailable.*unverified or unapproved",
            ):
                validator.validate(ledger, evidence_root)

    def test_failure_claim_requires_a_closed_typed_host_result(self) -> None:
        def legacy_freeform(value: dict) -> None:
            failure = next(
                check for check in value["checks"] if check["id"] == "handler-nonzero"
            )
            del failure["host_result"]
            failure["host_outcome_recorded"] = True

        result = self.validate_mutation(legacy_freeform)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("typed host result", result.stderr.lower())

    def test_raw_evidence_rejects_sensitive_or_machine_personal_content(self) -> None:
        samples = {
            "session": '{"session_id":"private-session"}',
            "prompt": '{"prompt":"private user request"}',
            "args": '{"command_args":"private args"}',
            "api-key": "ANTHROPIC_API_KEY=secret-value",
            "authorization": "Authorization: Bearer secret-value",
            "windows-path": "C:\\Users\\someone\\private.txt",
            "unc-path": "\\\\server\\share\\private.txt",
            "mac-path": "/Users/someone/private.txt",
            "linux-path": "/home/someone/private.txt",
        }
        for label, content in samples.items():
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    root = Path(temporary)
                    evidence_root = root / "raw"
                    evidence_root.mkdir()
                    value = claimed_observed_contract(evidence_root)
                    raw = value["checks"][0]["raw_evidence"]
                    path = evidence_root / raw["path"]
                    encoded = content.encode()
                    path.write_bytes(encoded)
                    raw["sha256"] = hashlib.sha256(encoded).hexdigest()
                    ledger = root / "contract.json"
                    ledger.write_text(json.dumps(value), encoding="utf-8")
                    result = run_validator(ledger, evidence_root)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("scrub", result.stderr.lower())

    def test_raw_evidence_rejects_embedded_windows_path_after_json_decoding(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            evidence_root = root / "raw"
            evidence_root.mkdir()
            value = claimed_observed_contract(evidence_root)
            raw = value["checks"][0]["raw_evidence"]
            path = evidence_root / raw["path"]
            record = json.loads(path.read_text(encoding="utf-8"))
            record["stdout"] = r"prefixC:\Users\someone\private.txt"
            encoded = json.dumps(record, indent=2).encode()
            path.write_bytes(encoded)
            raw["sha256"] = hashlib.sha256(encoded).hexdigest()
            ledger = root / "contract.json"
            ledger.write_text(json.dumps(value), encoding="utf-8")
            result = run_validator(ledger, evidence_root)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("scrub", result.stderr.lower())

    def test_raw_evidence_rejects_unicode_escaped_windows_path_after_json_decoding(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            evidence_root = root / "raw"
            evidence_root.mkdir()
            value = claimed_observed_contract(evidence_root)
            raw = value["checks"][0]["raw_evidence"]
            path = evidence_root / raw["path"]
            record = json.loads(path.read_text(encoding="utf-8"))
            record["stdout"] = r"prefixC:\Users\someone\private.txt"
            wire = json.dumps(record, indent=2).replace(
                "prefixC:", r"prefix\u0043:", 1
            )
            encoded = wire.encode()
            path.write_bytes(encoded)
            raw["sha256"] = hashlib.sha256(encoded).hexdigest()
            ledger = root / "contract.json"
            ledger.write_text(json.dumps(value), encoding="utf-8")
            result = run_validator(ledger, evidence_root)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("scrub", result.stderr.lower())

    def test_subject_digest_rejects_nested_link_or_junction_components(self) -> None:
        from scripts import validate_claude_host_contract as validator

        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            root = Path(temporary)
            nested = root / "nested"
            nested.mkdir()
            (nested / "subject.txt").write_text("subject\n", encoding="utf-8")
            original = validator.is_link_or_junction

            def nested_link(path: Path) -> bool:
                return path == nested or original(path)

            with patch.object(
                validator, "is_link_or_junction", side_effect=nested_link
            ):
                with self.assertRaisesRegex(
                    validator.HostContractError, "must not contain links"
                ):
                    validator.digest_subject(root)

    def test_bare_alias_observation_is_required_without_a_guarantee(self) -> None:
        committed = json.loads(UNVERIFIED_CONTRACT.read_text(encoding="utf-8"))
        checks = {check["id"]: check for check in committed["checks"]}
        self.assertIn("bare-alias-observation", checks)
        observation = checks["bare-alias-observation"]
        self.assertNotIn("guarantee", observation)
        self.assertEqual(observation["status"], "unverified")

        def remove(value: dict) -> None:
            value["checks"] = [
                check
                for check in value["checks"]
                if check["id"] != BARE_ALIAS_CHECK
            ]

        def guarantee(value: dict) -> None:
            alias = next(
                check for check in value["checks"] if check["id"] == BARE_ALIAS_CHECK
            )
            alias["guarantee"] = "aliases-exist"

        def unknown_state(value: dict) -> None:
            alias = next(
                check for check in value["checks"] if check["id"] == BARE_ALIAS_CHECK
            )
            alias["observations"][0]["state"] = "guaranteed"

        for label, mutate in {
            "missing": remove,
            "guarantee": guarantee,
            "state": unknown_state,
        }.items():
            with self.subTest(label=label):
                result = self.validate_mutation(mutate)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("bare alias", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
