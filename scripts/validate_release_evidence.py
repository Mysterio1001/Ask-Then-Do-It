#!/usr/bin/env python3
"""Reject completed release evidence unless every configured check passed."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


class EvidenceError(RuntimeError):
    """A release evidence gate was not satisfied."""


class DuplicateJsonKeyError(ValueError):
    """A JSON object contains an ambiguous duplicate member."""


MANDATORY_VALIDATION_CHECKS = {"workflow-token-proxy"}
ARTIFACT_TITLE = re.compile(r"^#[ \t]+\S.*$")
ENVELOPE_FIELD = re.compile(r"^[A-Za-z][A-Za-z0-9 _-]*:[^\r\n]*$")
SETEXT_UNDERLINE = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    return parser.parse_args()


def unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateJsonKeyError(f"Duplicate JSON key: {key}")
        value[key] = item
    return value


def read_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=unique_json_object,
        )
    except (FileNotFoundError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        raise EvidenceError(f"Invalid or missing {label}: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EvidenceError(f"{label} must be a JSON object: {path}")
    return value


def artifact_envelope(markdown: str) -> str:
    lines = markdown.splitlines()
    if not lines or ARTIFACT_TITLE.fullmatch(lines[0]) is None:
        return ""

    fields: list[str] = []
    index = 1
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if ENVELOPE_FIELD.fullmatch(line) is None:
            break
        if index + 1 < len(lines) and SETEXT_UNDERLINE.fullmatch(lines[index + 1]):
            break
        fields.append(line)
        index += 1
    return "\n".join(fields)


def validate(
    config_path: Path, ledger_path: Path, evidence_path: Path
) -> str:
    config = read_object(config_path, "release configuration")
    ledger = read_object(ledger_path, "validation ledger")
    version = config.get("release_version")
    required = config.get("required_validation_checks")
    if not isinstance(version, str) or not isinstance(required, list) or not required:
        raise EvidenceError("Release configuration lacks the evidence gate contract")
    missing_mandatory = sorted(MANDATORY_VALIDATION_CHECKS.difference(required))
    if missing_mandatory:
        raise EvidenceError(
            f"Release configuration lacks mandatory validation checks: "
            f"{missing_mandatory}"
        )
    if ledger.get("release_version") != version:
        raise EvidenceError("Validation ledger release_version does not match release")
    checks = ledger.get("checks")
    if not isinstance(checks, list):
        raise EvidenceError("Validation ledger checks must be an array")

    indexed: dict[str, dict[str, Any]] = {}
    for item in checks:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise EvidenceError("Every validation check must be an object with an id")
        check_id = item["id"]
        if check_id in indexed:
            raise EvidenceError(f"Duplicate validation check: {check_id}")
        indexed[check_id] = item
    missing = [check_id for check_id in required if check_id not in indexed]
    extra = [check_id for check_id in indexed if check_id not in required]
    if missing:
        raise EvidenceError(f"Missing required validation checks: {missing}")
    if extra:
        raise EvidenceError(f"Unknown validation checks: {extra}")

    for check_id in required:
        item = indexed[check_id]
        status = item.get("status")
        if status != "passed":
            raise EvidenceError(f"Required check {check_id} is {status!r}, not passed")
        for field in ("command", "outcome"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise EvidenceError(f"Required check {check_id} lacks {field}")

    try:
        evidence = evidence_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise EvidenceError(f"Missing release evidence: {evidence_path}") from exc
    envelope = artifact_envelope(evidence)
    statuses = re.findall(r"^Status:\s*(.*?)\s*$", envelope, re.MULTILINE)
    if statuses != ["Completed"]:
        raise EvidenceError(
            "Release evidence must contain exactly one Status: Completed"
        )
    versions = re.findall(
        r"^Release version:\s*`([^`\r\n]+)`\s*$", envelope, re.MULTILINE
    )
    if versions != [version]:
        raise EvidenceError(
            "Release evidence must contain exactly one matching Release version"
        )
    return version


def main() -> int:
    args = parse_args()
    try:
        version = validate(args.config, args.ledger, args.evidence)
    except EvidenceError as exc:
        print(f"Release evidence validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Release evidence {version} validated: all required checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
