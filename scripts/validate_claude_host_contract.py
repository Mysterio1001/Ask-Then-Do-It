#!/usr/bin/env python3
"""Validate scrubbed, execution-bound Claude Code 2.1.251 observations.

This is a project-owned normalized evidence format, not a Claude native output
schema. Digests and cross-checks detect incomplete claims; they do not prove an
operator's honesty.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXACT_VERSION = "2.1.251"
OFFICIAL_BINARY_URL = "https://downloads.claude.ai/claude-code-releases/2.1.251/win32-x64/claude.exe"
OFFICIAL_BINARY_SHA256 = "8d1229a281281b98fd2dee72b3253a704be4fce4d45207200cd32a9bb5a6c909"
OFFICIAL_BINARY_SIZE = 217360032
OFFICIAL_PLATFORM = "win32-x64"
FIXTURE_SUBJECT = "tests/claude/fixtures/host-contract/plugin"
STRICT_CHECKS = {"canonical-plugin-strict-validation", "marketplace-strict-validation", "compatibility-plugin-strict-validation"}
ENTRY_CHECKS = {"automatic-entry-expansion", "explicit-entry-expansion"}
FAILURE_CHECKS = {"node-unavailable", "handler-nonzero", "handler-exit-2", "handler-timeout"}
BARE_ALIAS_CHECK = "bare-alias-observation"
ALL_CHECKS = STRICT_CHECKS | ENTRY_CHECKS | FAILURE_CHECKS | {BARE_ALIAS_CHECK}
EXPECTED_SUBJECTS = {
    "canonical-plugin-strict-validation": "adapters/claude-code/plugin/ask-then-do-it",
    "marketplace-strict-validation": ".claude-plugin/marketplace.json",
    **{check_id: FIXTURE_SUBJECT for check_id in ALL_CHECKS - {"canonical-plugin-strict-validation", "marketplace-strict-validation"}},
}

# These remain empty until exact-host observations are reviewed and approved.
# Thus no guessed command identity or failure result can satisfy this gate.
APPROVED_COMMAND_NAMES: dict[str, str] = {}
HOST_RESULTS = {"skill-expanded-without-context", "skill-expansion-blocked", "request-aborted", "host-error-visible"}
APPROVED_FAILURE_RESULTS: dict[str, str | None] = {
    "node-unavailable": None,
    "handler-nonzero": None,
    "handler-exit-2": "skill-expansion-blocked",
    "handler-timeout": None,
}

ROOT_FIELDS = {"schema_version", "target_claude_code_version", "status", "evidence_kind", "environment", "checks"}
ENVIRONMENT_FIELDS = {"binary_source_url", "binary_sha256", "binary_size", "binary_platform", "reported_version", "os", "surface", "node_version", "executed_at"}
COMMON_CHECK_FIELDS = {"id", "status", "evidence_kind", "observed_at", "executor", "argv", "exit_code", "timed_out", "warnings", "subject", "outcome", "raw_evidence"}
ENTRY_FIELDS = {"command_name", "command_source", "hook_triggered", "additional_context_visible", "nonce_sha256"}
ALIAS_FIELDS = {"observation_scope", "observations"}
RAW_REFERENCE_FIELDS = {"path", "sha256"}
RAW_RECORD_FIELDS = {"schema_version", "check_id", "observed_at", "binary", "node_version", "execution", "subject", "result", "stdout", "stderr"}
BINARY_FIELDS = {"source_url", "sha256", "size", "version", "platform"}
EXECUTION_FIELDS = {"executor", "argv", "exit_code", "timed_out", "warnings"}
SUBJECT_FIELDS = {"path", "sha256"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
NODE_VERSION = re.compile(r"^v?([0-9]+)\.([0-9]+)\.([0-9]+)$")
SCRUB_PATTERNS = (
    re.compile(r'''(?i)["']?(?:session_id|prompt|command_args)["']?\s*[:=]'''),
    re.compile(r"(?i)(?:anthropic_)?api[_-]?key\s*[:=]"),
    re.compile(r"(?i)authorization\s*:|bearer\s+[A-Za-z0-9]"),
    # Match embedded Windows drive paths, but not the ``s://`` suffix in URI
    # schemes such as ``https://``.
    re.compile(r"(?i)[a-z]:(?:\\|/(?!/))"),
    re.compile(r"\\\\[^\\\s]+\\[^\\\s]+"),
    re.compile(r"/(?:Users|home)/[^/\s]+", re.IGNORECASE),
)
SENSITIVE_FIELDS = {"session_id", "prompt", "command_args"}


class HostContractError(RuntimeError):
    """The normalized observation cannot satisfy the exact-host hard gate."""


class DuplicateJsonKeyError(ValueError):
    pass


def unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateJsonKeyError(f"Duplicate JSON key: {key}")
        value[key] = item
    return value


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise HostContractError(f"{label} must be an object")
    return value


def require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    missing = sorted(expected - set(value))
    unknown = sorted(set(value) - expected)
    if missing or unknown:
        details = []
        if missing:
            details.append(f"missing {missing}")
        if unknown:
            details.append(f"unknown {unknown}")
        raise HostContractError(f"Invalid {label} fields: {', '.join(details)}")


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise HostContractError(f"{label} must be a non-empty string")
    return value


def read_ledger(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes(), object_pairs_hook=unique_json_object)
    except FileNotFoundError as exc:
        raise HostContractError(f"Missing host contract ledger: {path}") from exc
    except (json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        raise HostContractError(f"Invalid host contract ledger: {exc}") from exc
    return require_object(value, "Host contract ledger")


def parse_raw_record(content: bytes, check_id: str) -> dict[str, Any]:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HostContractError(f"Execution-bound raw record for {check_id} must be UTF-8 JSON") from exc
    for pattern in SCRUB_PATTERNS:
        if pattern.search(text):
            raise HostContractError(f"Execution-bound raw record for {check_id} failed the scrub gate")
    try:
        value = json.loads(text, object_pairs_hook=unique_json_object)
    except (json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        raise HostContractError(f"Execution-bound raw record for {check_id} is invalid") from exc
    value = require_object(value, f"Execution-bound raw record for {check_id}")
    scrub_decoded_record(value, check_id)
    return value


def scrub_decoded_record(value: Any, check_id: str) -> None:
    """Reject sensitive fields and personal paths after JSON escape decoding."""

    if isinstance(value, dict):
        if any(key in SENSITIVE_FIELDS for key in value):
            raise HostContractError(
                f"Execution-bound raw record for {check_id} failed the scrub gate"
            )
        for key, item in value.items():
            scrub_decoded_record(key, check_id)
            scrub_decoded_record(item, check_id)
        return
    if isinstance(value, list):
        for item in value:
            scrub_decoded_record(item, check_id)
        return
    if isinstance(value, str) and any(pattern.search(value) for pattern in SCRUB_PATTERNS[1:]):
        raise HostContractError(
            f"Execution-bound raw record for {check_id} failed the scrub gate"
        )


def is_link_or_junction(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or (is_junction is not None and is_junction())


def has_link_component(path: Path, boundary: Path) -> bool:
    """Return whether path or any component below boundary is a link/junction."""

    current = path
    while True:
        if is_link_or_junction(current):
            return True
        if current == boundary:
            return False
        parent = current.parent
        if parent == current:
            return False
        current = parent


def digest_subject(path: Path) -> str:
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if has_link_component(item, path):
            raise HostContractError("Host contract subject must not contain links")
        if not item.is_file():
            continue
        digest.update(item.relative_to(path).as_posix().encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(item.read_bytes()).digest())
    return digest.hexdigest()


def validate_timestamp(value: Any, label: str) -> str:
    text = require_text(value, label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HostContractError(f"{label} timestamp is invalid") from exc
    if parsed.tzinfo is None:
        raise HostContractError(f"{label} timestamp must include a timezone")
    return text


def validate_node_version(value: Any) -> str:
    text = require_text(value, "Validated node version")
    match = NODE_VERSION.fullmatch(text)
    if match is None or int(match.group(1)) < 22:
        raise HostContractError("Validated node version must be an exact Node 22+ version")
    return text


def validate_environment(value: Any) -> dict[str, Any]:
    environment = require_object(value, "Host environment")
    require_exact_keys(environment, ENVIRONMENT_FIELDS, "host environment")
    expected = {
        "binary_source_url": OFFICIAL_BINARY_URL,
        "binary_sha256": OFFICIAL_BINARY_SHA256,
        "binary_size": OFFICIAL_BINARY_SIZE,
        "binary_platform": OFFICIAL_PLATFORM,
        "reported_version": EXACT_VERSION,
        "os": "windows",
        "surface": "terminal-cli",
    }
    for field, required in expected.items():
        if environment[field] != required or type(environment[field]) is not type(required):
            raise HostContractError(
                f"Host environment {field.replace('_', ' ')} must be exact {required!r}"
            )
    validate_node_version(environment["node_version"])
    validate_timestamp(environment["executed_at"], "Host execution")
    return environment


def validate_string_list(value: Any, label: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value) or any(not isinstance(item, str) or not item for item in value):
        raise HostContractError(f"{label} must be a string array")
    return value


def validate_subject(value: Any, check_id: str) -> dict[str, str]:
    subject = require_object(value, f"Subject for {check_id}")
    require_exact_keys(subject, SUBJECT_FIELDS, f"subject for {check_id}")
    expected_path = EXPECTED_SUBJECTS[check_id]
    if subject["path"] != expected_path:
        raise HostContractError(f"Subject path for {check_id} is not approved")
    digest = require_text(subject["sha256"], f"Subject digest for {check_id}")
    if SHA256.fullmatch(digest) is None:
        raise HostContractError(f"Subject digest for {check_id} is invalid")
    path = ROOT / expected_path
    root = ROOT.resolve()
    if has_link_component(path, root) or not path.exists() or not path.resolve().is_relative_to(root):
        raise HostContractError(f"Subject for {check_id} is missing or unsafe")
    if digest_subject(path) != digest:
        raise HostContractError(f"Subject digest mismatch for {check_id}")
    return subject


def expected_raw_result(check: dict[str, Any], check_id: str) -> dict[str, Any]:
    if check_id in STRICT_CHECKS:
        return {"kind": "strict-validation", "warning_count": len(check["warnings"])}
    if check_id in ENTRY_CHECKS:
        return {field: check[field] for field in ENTRY_FIELDS} | {"kind": "entry-expansion"}
    if check_id in FAILURE_CHECKS:
        return {"kind": "failure-semantics", "host_result": check["host_result"]}
    return {"kind": "bare-alias-observation", "observation_scope": check["observation_scope"], "observations": check["observations"]}


def validate_raw_record(reference_value: Any, evidence_root: Path, check: dict[str, Any], environment: dict[str, Any]) -> None:
    check_id = check["id"]
    reference = require_object(reference_value, f"Raw evidence for {check_id}")
    require_exact_keys(reference, RAW_REFERENCE_FIELDS, f"raw evidence for {check_id}")
    relative = Path(require_text(reference["path"], "Raw evidence path"))
    digest = require_text(reference["sha256"], "Raw evidence sha256")
    if relative.is_absolute() or ".." in relative.parts or SHA256.fullmatch(digest) is None:
        raise HostContractError(f"Raw evidence for {check_id} has an unsafe path or digest")
    root = evidence_root.resolve(strict=True)
    path = (root / relative).resolve(strict=True)
    candidate = root / relative
    if is_link_or_junction(evidence_root) or has_link_component(candidate, root) or not path.is_file() or not path.is_relative_to(root):
        raise HostContractError(f"Raw evidence for {check_id} escapes its root")
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != digest:
        raise HostContractError(f"Raw evidence digest mismatch for {check_id}")
    record = parse_raw_record(content, check_id)
    require_exact_keys(record, RAW_RECORD_FIELDS, f"raw record for {check_id}")
    if record["schema_version"] != 1 or type(record["schema_version"]) is not int or record["check_id"] != check_id or record["observed_at"] != check["observed_at"]:
        raise HostContractError(f"Execution-bound raw record identity mismatch for {check_id}")
    binary = require_object(record["binary"], f"Raw binary record for {check_id}")
    require_exact_keys(binary, BINARY_FIELDS, f"raw binary record for {check_id}")
    expected_binary = {"source_url": environment["binary_source_url"], "sha256": environment["binary_sha256"], "size": environment["binary_size"], "version": environment["reported_version"], "platform": environment["binary_platform"]}
    if binary != expected_binary or record["node_version"] != environment["node_version"]:
        raise HostContractError(f"Execution-bound raw record environment mismatch for {check_id}")
    execution = require_object(record["execution"], f"Raw execution for {check_id}")
    require_exact_keys(execution, EXECUTION_FIELDS, f"raw execution for {check_id}")
    if execution != {field: check[field] for field in EXECUTION_FIELDS}:
        raise HostContractError(f"Execution-bound raw record claim mismatch for {check_id}")
    if record["subject"] != check["subject"] or record["result"] != expected_raw_result(check, check_id):
        raise HostContractError(f"Execution-bound raw record result mismatch for {check_id}")
    if not isinstance(record["stdout"], str) or not isinstance(record["stderr"], str):
        raise HostContractError(f"Execution-bound raw record streams for {check_id} must be text")


def validate_alias_observations(value: Any) -> None:
    if not isinstance(value, list) or len(value) != 2:
        raise HostContractError("Bare alias observations must contain both entries")
    indexed: dict[str, str] = {}
    for item in value:
        observation = require_object(item, "Bare alias observation")
        require_exact_keys(observation, {"entry", "state"}, "bare alias observation")
        entry = observation["entry"]
        if entry in indexed or entry not in {"ask-then-do-it", "ask-then-do-it-5"}:
            raise HostContractError("Bare alias observation has a duplicate or unknown entry")
        if observation["state"] not in {"present", "absent"}:
            raise HostContractError("Bare alias state must be observed present or absent")
        indexed[entry] = observation["state"]
    if set(indexed) != {"ask-then-do-it", "ask-then-do-it-5"}:
        raise HostContractError("Bare alias observations must contain both entries")


def validate_check(item: Any, environment: dict[str, Any], evidence_root: Path) -> str:
    check = require_object(item, "Host contract check")
    check_id = require_text(check.get("id"), "Host contract check id")
    if check_id not in ALL_CHECKS:
        raise HostContractError(f"Unknown host contract check: {check_id}")
    extra = ENTRY_FIELDS if check_id in ENTRY_CHECKS else {"host_result"} if check_id in FAILURE_CHECKS else ALIAS_FIELDS if check_id == BARE_ALIAS_CHECK else set()
    if check_id in FAILURE_CHECKS and "host_outcome_recorded" in check:
        raise HostContractError(f"Failure check {check_id} requires a closed typed host result")
    check_label = "bare alias check" if check_id == BARE_ALIAS_CHECK else f"check {check_id}"
    require_exact_keys(check, COMMON_CHECK_FIELDS | extra, check_label)
    if check["status"] != "passed" or check["evidence_kind"] != "observed":
        raise HostContractError(f"Check {check_id} must be passed with observed evidence")
    validate_timestamp(check["observed_at"], f"Observation {check_id}")
    if check["executor"] != "claude":
        raise HostContractError(f"Executor for {check_id} must be claude")
    validate_string_list(check["argv"], f"Argv for {check_id}", nonempty=True)
    warnings = validate_string_list(check["warnings"], f"Warnings for {check_id}")
    if type(check["timed_out"]) is not bool:
        raise HostContractError(f"Timed-out fact for {check_id} must be a boolean")
    if check["timed_out"] and check["exit_code"] is not None:
        raise HostContractError(f"Timed-out check {check_id} must not claim an exit code")
    if not check["timed_out"] and type(check["exit_code"]) is not int:
        raise HostContractError(f"Exit code for {check_id} must be an integer")
    check["subject"] = validate_subject(check["subject"], check_id)
    require_text(check["outcome"], f"Outcome for {check_id}")
    if check_id in STRICT_CHECKS and (check["exit_code"] != 0 or check["timed_out"] or warnings):
        raise HostContractError(f"Strict validation {check_id} has a warning or failure")
    if check_id in ENTRY_CHECKS:
        require_text(check["command_name"], f"Command identity for {check_id}")
        if check["command_source"] != "plugin" or check["hook_triggered"] is not True or check["additional_context_visible"] is not True:
            raise HostContractError(f"Entry {check_id} lacks plugin hook or additional context")
        if SHA256.fullmatch(require_text(check["nonce_sha256"], "Nonce digest")) is None:
            raise HostContractError(f"Entry {check_id} has an invalid nonce digest")
    elif check_id in FAILURE_CHECKS and check["host_result"] not in HOST_RESULTS:
        raise HostContractError(f"Failure check {check_id} requires a closed typed host result")
    elif check_id == BARE_ALIAS_CHECK:
        if check["observation_scope"] != "observed-only":
            raise HostContractError("Bare alias result must be observed-only, never a guarantee")
        validate_alias_observations(check["observations"])
    validate_raw_record(check["raw_evidence"], evidence_root, check, environment)
    return check_id


def validate(ledger_path: Path, evidence_root: Path) -> None:
    ledger = read_ledger(ledger_path)
    require_exact_keys(ledger, ROOT_FIELDS, "host contract ledger")
    if ledger["schema_version"] != 1 or type(ledger["schema_version"]) is not int:
        raise HostContractError("Host contract schema_version must be integer 1")
    if ledger["target_claude_code_version"] != EXACT_VERSION:
        raise HostContractError(f"Target Claude Code version must be {EXACT_VERSION}")
    if ledger["status"] != "passed":
        raise HostContractError("Host contract ledger is unverified or not passed")
    if ledger["evidence_kind"] != "observed":
        raise HostContractError("Host contract ledger must use observed evidence")
    environment = validate_environment(ledger["environment"])
    checks = ledger["checks"]
    if not isinstance(checks, list):
        raise HostContractError("Host contract checks must be an array")
    ids = [require_text(require_object(item, "Host contract check").get("id"), "Host contract check id") for item in checks]
    duplicates = sorted({check_id for check_id in ids if ids.count(check_id) > 1})
    if duplicates:
        raise HostContractError(f"Duplicate host contract checks: {duplicates}")
    unknown = sorted(set(ids) - ALL_CHECKS)
    if unknown:
        raise HostContractError(f"Unknown host contract checks: {unknown}")
    missing = sorted(ALL_CHECKS - set(ids))
    if missing:
        label = "bare alias" if BARE_ALIAS_CHECK in missing else "host contract"
        raise HostContractError(f"Missing {label} checks: {missing}")
    indexed = {validate_check(item, environment, evidence_root): item for item in checks}
    for check_id in ENTRY_CHECKS:
        approved = APPROVED_COMMAND_NAMES.get(check_id)
        if approved is None or indexed[check_id]["command_name"] != approved:
            raise HostContractError(f"Exact command identity for {check_id} remains unverified or unapproved")
    for check_id, expected in APPROVED_FAILURE_RESULTS.items():
        if expected is None:
            raise HostContractError(f"Typed host result for {check_id} remains unverified or unapproved")
        if indexed[check_id]["host_result"] != expected:
            raise HostContractError(f"Typed host result for {check_id} does not match its pass predicate")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        validate(args.ledger, args.evidence_root)
    except (HostContractError, OSError) as exc:
        print(f"Claude host contract validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Claude Code {EXACT_VERSION} host contract validated from bound observations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
