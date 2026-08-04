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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    return parser.parse_args()


def read_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"Invalid or missing {label}: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EvidenceError(f"{label} must be a JSON object: {path}")
    return value


def validate(
    config_path: Path, ledger_path: Path, evidence_path: Path
) -> tuple[str, bool]:
    config = read_object(config_path, "release configuration")
    ledger = read_object(ledger_path, "validation ledger")
    version = config.get("release_version")
    required = config.get("required_validation_checks")
    if not isinstance(version, str) or not isinstance(required, list) or not required:
        raise EvidenceError("Release configuration lacks the evidence gate contract")
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

    tests_skipped = False
    for check_id in required:
        item = indexed[check_id]
        status = item.get("status")
        if check_id == "automated-tests" and status == "skipped-by-user":
            tests_skipped = True
            for field in ("reason", "approval"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    raise EvidenceError(
                        f"Skipped automated-tests lacks {field} metadata"
                    )
        elif status != "passed":
            raise EvidenceError(f"Required check {check_id} is {status!r}, not passed")
        for field in ("command", "outcome"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise EvidenceError(f"Required check {check_id} lacks {field}")

    try:
        evidence = evidence_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise EvidenceError(f"Missing release evidence: {evidence_path}") from exc
    if re.search(r"^Status:\s*Completed\s*$", evidence, re.MULTILINE) is None:
        raise EvidenceError("Release evidence is not marked Status: Completed")
    if f"Release version: `{version}`" not in evidence:
        raise EvidenceError("Release evidence version does not match release")
    if tests_skipped and "Tests: `skipped-by-user`" not in evidence:
        raise EvidenceError(
            "Release evidence lacks Tests: `skipped-by-user` disclosure"
        )
    return version, tests_skipped


def main() -> int:
    args = parse_args()
    try:
        version, tests_skipped = validate(
            args.config, args.ledger, args.evidence
        )
    except EvidenceError as exc:
        print(f"Release evidence validation failed: {exc}", file=sys.stderr)
        return 1
    if tests_skipped:
        print(
            f"Release evidence {version} validated: automated tests "
            "skipped-by-user; all other required checks passed"
        )
    else:
        print(f"Release evidence {version} validated: all required checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
