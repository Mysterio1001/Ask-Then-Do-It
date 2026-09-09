#!/usr/bin/env python3
"""Validate the release-owned Claude model mapping source trace."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


TRACE_KEYS = {
    "schema_version",
    "mapping_path",
    "mapping_sha256",
    "checked_on",
    "sources",
    "records",
}
SOURCE_KEYS = {"url", "checked_on", "snapshot_path", "snapshot_sha256"}
RECORD_KEYS = {
    "model_id",
    "anthropic_status",
    "classification",
    "classification_basis",
    "source_refs",
}
CANONICAL_MAPPING_PATH = (
    "adapters/claude-code/plugin/ask-then-do-it/config/model-classifications.json"
)
ACTIVE_MODEL_ID = re.compile(
    r"^claude-(?:fable|haiku|opus|sonnet)-(\d+)(?:-(\d+))?(?:-\d{8})?$"
)


class EvidenceError(ValueError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise EvidenceError(f"duplicate JSON key {key!r} in {path}")
            value[key] = item
        return value

    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise EvidenceError(f"cannot read valid JSON from {path}: {error}") from error


def expected_active_classification(model_id: str) -> tuple[str, str]:
    match = ACTIVE_MODEL_ID.fullmatch(model_id)
    if match is None:
        raise EvidenceError(f"{model_id}: active model ID has no supported version shape")
    major = int(match.group(1))
    minor = int(match.group(2) or 0)
    if major >= 5:
        return "claude-5", "generation-gte-5"
    if major == 4 and minor >= 6:
        return "supported-non-5", "active-gte-4.6-lt-5"
    return "unsupported", "active-below-product-minimum"


def snapshot_mentions_model(source: str, model_id: str) -> bool:
    boundary = r"(?<![a-z0-9.-])" + re.escape(model_id) + r"(?![a-z0-9.-])"
    return re.search(boundary, source, flags=re.IGNORECASE) is not None


def snapshot_supports_status(source: str, model_id: str, status: str) -> bool:
    accepted = "(?:active|current)" if status == "active" else "retired"
    pattern = rf"(?m)^\s*{re.escape(model_id)}\s*\|\s*{accepted}\s*$"
    return re.search(pattern, source, flags=re.IGNORECASE) is not None


def validate(mapping_path: Path, trace_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        mapping = load_json(mapping_path)
        trace = load_json(trace_path)
    except EvidenceError as error:
        return [str(error)]

    if not isinstance(mapping, dict) or not isinstance(mapping.get("classifications"), dict):
        return ["mapping must contain an object classifications table"]
    if not isinstance(trace, dict) or set(trace) != TRACE_KEYS:
        return ["source trace has an invalid top-level schema"]
    if type(trace.get("schema_version")) is not int or trace.get("schema_version") != 1:
        errors.append("source trace schema_version must equal 1")
    if trace.get("mapping_path") != CANONICAL_MAPPING_PATH:
        errors.append("source trace mapping_path does not identify the canonical mapping")
    if trace.get("mapping_sha256") != sha256(mapping_path):
        errors.append("source trace mapping_sha256 does not match the mapping bytes")
    checked_on = trace.get("checked_on")
    if not isinstance(checked_on, str):
        errors.append("source trace checked_on must be a string")
    if checked_on != mapping.get("evidence_checked_on"):
        errors.append("source trace checked_on does not match the mapping evidence date")

    sources = trace.get("sources")
    if not isinstance(sources, dict) or not sources:
        return errors + ["source trace sources must be a non-empty object"]
    mapping_sources = mapping.get("sources")
    if not isinstance(mapping_sources, dict) or set(sources) != set(mapping_sources):
        errors.append("source trace source inventory does not match the mapping")
        mapping_sources = {}
    snapshot_text: dict[str, str] = {}
    fixture_root = trace_path.resolve().parent
    for source_id, source in sources.items():
        if not isinstance(source_id, str) or not isinstance(source, dict) or set(source) != SOURCE_KEYS:
            errors.append(f"source {source_id!r} has an invalid schema")
            continue
        if source.get("checked_on") != checked_on:
            errors.append(f"source {source_id}: checked_on does not match the trace")
        mapping_source = mapping_sources.get(source_id)
        if not isinstance(mapping_source, dict):
            errors.append(f"source {source_id}: is not declared by the mapping")
        else:
            if source.get("url") != mapping_source.get("url"):
                errors.append(f"source {source_id}: url does not match the mapping")
            if source.get("checked_on") != mapping_source.get("checked_on"):
                errors.append(f"source {source_id}: checked_on does not match the mapping")
        relative = source.get("snapshot_path")
        if not isinstance(relative, str):
            errors.append(f"source {source_id}: snapshot_path must be a string")
            continue
        snapshot = (fixture_root / relative).resolve()
        if not snapshot.is_relative_to(fixture_root):
            errors.append(f"source {source_id}: snapshot_path escapes the fixture root")
            continue
        try:
            text = snapshot.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"source {source_id}: cannot read snapshot: {error}")
            continue
        if source.get("snapshot_sha256") != sha256(snapshot):
            errors.append(f"source {source_id}: snapshot_sha256 does not match")
        if source.get("url") not in text or f"checked_on: {checked_on}" not in text:
            errors.append(f"source {source_id}: snapshot header does not match its trace")
        snapshot_text[source_id] = text

    records = trace.get("records")
    if not isinstance(records, list):
        return errors + ["source trace records must be an array"]
    indexed: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict) or set(record) != RECORD_KEYS:
            errors.append("source trace contains a record with an invalid schema")
            continue
        model_id = record.get("model_id")
        if not isinstance(model_id, str):
            errors.append("source trace record model_id must be a string")
            continue
        if model_id in indexed:
            errors.append(f"{model_id}: duplicate source trace record")
            continue
        indexed[model_id] = record

        status = record.get("anthropic_status")
        classification = record.get("classification")
        basis = record.get("classification_basis")
        refs = record.get("source_refs")
        if status == "retired":
            expected = ("unsupported", "retired")
        elif status == "active":
            try:
                expected = expected_active_classification(model_id)
            except EvidenceError as error:
                errors.append(str(error))
                expected = None
        else:
            errors.append(f"{model_id}: anthropic_status must be active or retired")
            expected = None
        if expected is not None and (classification, basis) != expected:
            errors.append(
                f"{model_id}: classification/basis do not follow the recorded status and version"
            )
        if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) for ref in refs):
            errors.append(f"{model_id}: source_refs must be a non-empty string array")
            continue
        if any(ref not in sources for ref in refs):
            errors.append(f"{model_id}: source_refs contain an unknown source")
            continue
        referenced = [snapshot_text[ref] for ref in refs if ref in snapshot_text]
        if not any(snapshot_mentions_model(text, model_id) for text in referenced):
            errors.append(f"{model_id}: no referenced snapshot contains this exact model ID")
        if status in {"active", "retired"} and not any(
            snapshot_supports_status(text, model_id, status) for text in referenced
        ):
            errors.append(f"{model_id}: no referenced snapshot supports status {status}")

    classifications = mapping["classifications"]
    if set(indexed) != set(classifications):
        errors.append("source trace model IDs do not exactly match the runtime mapping")
    for model_id, mapped_classification in classifications.items():
        record = indexed.get(model_id)
        if record is not None and record.get("classification") != mapped_classification:
            errors.append(f"{model_id}: trace classification does not match the runtime mapping")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--trace", type=Path, required=True)
    arguments = parser.parse_args(argv)
    errors = validate(arguments.mapping, arguments.trace)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Claude model classification evidence is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
