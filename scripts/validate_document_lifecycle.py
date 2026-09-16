#!/usr/bin/env python3
"""Validate a repository-local document lifecycle manifest without writing files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


class LifecycleError(RuntimeError):
    """The document lifecycle contract is not satisfied."""


ENVELOPE_FIELDS = {
    "artifact_type",
    "artifact_id",
    "workflow_id",
    "core_version",
    "status",
    "inputs",
    "assumptions",
    "deferred",
    "handoff",
    "approval",
}
LIFECYCLE_STATUSES = {"Draft", "Approved", "Superseded"}
EVIDENCE_STATUSES = {"unverified", "skipped", "blocked"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
MARKDOWN_FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9 _-]*):[ \t]*(.*?)\s*$")
SHA256_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")
MIGRATION_STATUSES = {"staged", "completed", "partial", "failed"}
MIGRATION_DISPOSITIONS = {"pointer", "archived", "retained"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    return parser.parse_args()


def unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise LifecycleError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=unique_json_object,
        )
    except (OSError, json.JSONDecodeError, LifecycleError) as exc:
        raise LifecycleError(f"invalid {label}: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise LifecycleError(f"{label} must be a JSON object: {path}")
    return value


def safe_relative(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LifecycleError(f"{label} must be a non-empty relative path")
    path = Path(value.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise LifecycleError(f"{label} must be repository-relative and contain no '..': {value}")
    return path.as_posix()


def resolve_path(root: Path, value: Any, label: str) -> Path:
    relative = safe_relative(value, label)
    candidate = (root / relative).resolve()
    resolved_root = root.resolve()
    try:
        candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise LifecycleError(f"{label} escapes the repository root: {value}") from exc
    return candidate


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise LifecycleError(f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise LifecycleError(f"{label} must be an array")
    return value


def require_id(value: Any, label: str) -> str:
    if not isinstance(value, str) or ID_PATTERN.fullmatch(value) is None:
        raise LifecycleError(f"{label} must be a stable artifact identifier")
    return value


def read_artifact_metadata(path: Path) -> dict[str, Any]:
    if path.suffix.casefold() == ".json":
        return read_json(path, "artifact")
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LifecycleError(f"cannot read artifact {path}: {exc}") from exc
    metadata: dict[str, Any] = {}
    for line in text.splitlines():
        match = MARKDOWN_FIELD.fullmatch(line)
        if match and match.group(1) in {
            "Artifact type",
            "Artifact ID",
            "Workflow ID",
            "Core version",
            "Status",
            "Inputs",
            "Assumptions",
            "Deferred",
            "Handoff",
            "Approval",
        }:
            key = match.group(1).lower().replace(" ", "_")
            metadata[key] = match.group(2).strip().strip("`")
    return metadata


def validate_envelope(record: dict[str, Any], label: str) -> None:
    missing = sorted(ENVELOPE_FIELDS.difference(record))
    if missing:
        raise LifecycleError(f"{label} is missing envelope fields: {missing}")
    require_id(record["artifact_id"], f"{label}.artifact_id")
    require_id(record["workflow_id"], f"{label}.workflow_id")
    if record["status"] not in LIFECYCLE_STATUSES | EVIDENCE_STATUSES:
        raise LifecycleError(f"{label}.status is unsupported: {record['status']!r}")
    if record["status"] in EVIDENCE_STATUSES and record["approval"] not in (None, ""):
        raise LifecycleError(f"{label} evidence state cannot contain approval evidence")


def validate_actual_metadata(record: dict[str, Any], path: Path, label: str) -> None:
    actual = read_artifact_metadata(path)
    for key in ("artifact_id", "workflow_id", "core_version", "status"):
        expected = str(record[key])
        if actual.get(key) != expected:
            raise LifecycleError(
                f"{label} metadata mismatch for {key}: expected {expected!r}, got {actual.get(key)!r}"
            )
    expected_type = str(record["artifact_type"])
    if actual.get("artifact_type") != expected_type:
        raise LifecycleError(
            f"{label} metadata mismatch for artifact_type: expected {expected_type!r}, got {actual.get('artifact_type')!r}"
        )


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_migration(
    root: Path,
    migration: Any,
    canonical_by_id: dict[str, dict[str, Any]],
) -> None:
    """Validate the recoverable metadata produced by a document migration."""
    record = require_object(migration, "manifest.migration")
    status = record.get("status")
    if status not in MIGRATION_STATUSES:
        raise LifecycleError(
            f"manifest.migration.status must be one of {sorted(MIGRATION_STATUSES)}"
        )
    migration_id = require_id(record.get("migration_id"), "manifest.migration.migration_id")
    workflow_id = require_id(record.get("workflow_id"), "manifest.migration.workflow_id")
    core_version = record.get("core_version")
    if not isinstance(core_version, str) or not core_version.strip():
        raise LifecycleError("manifest.migration.core_version must be non-empty")
    canonical_workflows = {item["workflow_id"] for item in canonical_by_id.values()}
    if workflow_id not in canonical_workflows:
        raise LifecycleError(f"migration workflow is not canonical: {workflow_id}")
    if any(item["core_version"] != core_version for item in canonical_by_id.values()):
        raise LifecycleError("migration core_version does not match canonical artifacts")

    source_manifest_value = safe_relative(
        record.get("source_manifest"), "manifest.migration.source_manifest"
    )
    backup_root_value = safe_relative(
        record.get("backup_root"), "manifest.migration.backup_root"
    )
    staging_root_value = safe_relative(
        record.get("staging_root"), "manifest.migration.staging_root"
    )
    source_manifest_path = resolve_path(
        root, source_manifest_value, "manifest.migration.source_manifest"
    )
    backup_root = resolve_path(root, backup_root_value, "manifest.migration.backup_root")
    staging_root = resolve_path(root, staging_root_value, "manifest.migration.staging_root")
    if not source_manifest_path.is_file():
        raise LifecycleError(
            f"migration source manifest is missing: {source_manifest_value}"
        )
    if not backup_root.is_dir():
        raise LifecycleError(f"migration backup root is missing: {backup_root_value}")
    if not staging_root.is_dir():
        raise LifecycleError(f"migration staging root is missing: {staging_root_value}")
    source_manifest_digest = record.get("source_manifest_sha256")
    if not isinstance(source_manifest_digest, str) or SHA256_PATTERN.fullmatch(source_manifest_digest) is None:
        raise LifecycleError(
            "manifest.migration.source_manifest_sha256 must be a 64-character SHA-256 digest"
        )
    if file_digest(source_manifest_path).casefold() != source_manifest_digest.casefold():
        raise LifecycleError("migration source manifest hash mismatch")

    recovery = require_object(record.get("recovery"), "manifest.migration.recovery")
    if not isinstance(recovery.get("rollback_available"), bool):
        raise LifecycleError("manifest.migration.recovery.rollback_available must be boolean")
    primary_error = recovery.get("primary_error")
    if primary_error not in (None, "") and not isinstance(primary_error, str):
        raise LifecycleError(
            "manifest.migration.recovery.primary_error must be null or a string"
        )
    recovery_errors = require_list(
        recovery.get("recovery_errors"),
        "manifest.migration.recovery.recovery_errors",
    )
    for index, error in enumerate(recovery_errors):
        if not isinstance(error, str) or not error.strip():
            raise LifecycleError(
                f"manifest.migration.recovery.recovery_errors[{index}] must be a non-empty string"
            )
    if status == "completed" and (primary_error not in (None, "") or recovery_errors):
        raise LifecycleError("completed migration cannot retain primary or recovery errors")
    if status in {"partial", "failed"} and primary_error in (None, "") and not recovery_errors:
        raise LifecycleError(f"{status} migration must retain recovery error information")

    source_manifest = read_json(source_manifest_path, "migration source manifest")
    if source_manifest.get("schema_version") != 1:
        raise LifecycleError("migration source manifest schema_version must be 1")
    if source_manifest.get("workflow_id") != workflow_id:
        raise LifecycleError("migration source manifest workflow does not match migration")
    if source_manifest.get("core_version") != core_version:
        raise LifecycleError("migration source manifest core version does not match migration")
    sources = require_list(source_manifest.get("sources"), "migration source manifest.sources")
    if not sources:
        raise LifecycleError("migration source manifest.sources must not be empty")
    seen_artifacts: set[str] = set()
    seen_sources: set[str] = set()
    seen_backups: set[str] = set()
    for index, raw in enumerate(sources):
        source = require_object(raw, f"migration sources[{index}]")
        artifact_id = require_id(
            source.get("source_artifact_id"),
            f"migration sources[{index}].source_artifact_id",
        )
        target_id = require_id(
            source.get("target_artifact_id"),
            f"migration sources[{index}].target_artifact_id",
        )
        target_section_id = require_id(
            source.get("target_section_id"),
            f"migration sources[{index}].target_section_id",
        )
        source_status = source.get("source_status_before")
        target_status = source.get("target_status_after")
        if source_status not in LIFECYCLE_STATUSES | EVIDENCE_STATUSES:
            raise LifecycleError(
                f"migration sources[{index}].source_status_before is unsupported: {source_status!r}"
            )
        if target_status not in LIFECYCLE_STATUSES | EVIDENCE_STATUSES:
            raise LifecycleError(
                f"migration sources[{index}].target_status_after is unsupported: {target_status!r}"
            )
        if target_id not in canonical_by_id:
            raise LifecycleError(f"migration target is not canonical: {target_id}")
        if target_status != canonical_by_id[target_id]["status"]:
            raise LifecycleError(f"migration target status does not match canonical target: {target_id}")
        if source_status in {"Draft", "unverified", "skipped", "blocked"} and target_status == "Approved":
            raise LifecycleError(
                f"migration promotes non-approved source {artifact_id} to Approved"
            )
        disposition = source.get("source_disposition")
        if disposition not in MIGRATION_DISPOSITIONS:
            raise LifecycleError(
                f"migration sources[{index}].source_disposition is unsupported: {disposition!r}"
            )
        source_exists_after = source.get("source_exists_after")
        if not isinstance(source_exists_after, bool):
            raise LifecycleError(
                f"migration sources[{index}].source_exists_after must be boolean"
            )
        source_path_value = safe_relative(
            source.get("source_path"), f"migration sources[{index}].source_path"
        )
        backup_path_value = safe_relative(
            source.get("backup_path"), f"migration sources[{index}].backup_path"
        )
        digest = source.get("original_sha256")
        if not isinstance(digest, str) or SHA256_PATTERN.fullmatch(digest) is None:
            raise LifecycleError(
                f"migration sources[{index}].original_sha256 must be a 64-character SHA-256 digest"
            )
        if artifact_id in seen_artifacts:
            raise LifecycleError(f"duplicate migration artifact: {artifact_id}")
        if source_path_value in seen_sources:
            raise LifecycleError(f"duplicate migration source path: {source_path_value}")
        if backup_path_value in seen_backups:
            raise LifecycleError(f"duplicate migration backup path: {backup_path_value}")
        backup_path = resolve_path(
            root, backup_path_value, f"migration sources[{index}].backup_path"
        )
        source_path = resolve_path(
            root, source_path_value, f"migration sources[{index}].source_path"
        )
        try:
            backup_path.relative_to(backup_root)
        except ValueError as exc:
            raise LifecycleError(
                f"migration backup path is outside backup root: {backup_path_value}"
            ) from exc
        if backup_path == source_path:
            raise LifecycleError(
                f"migration source and backup paths must differ: {source_path_value}"
            )
        if not backup_path.is_file():
            raise LifecycleError(f"migration backup file is missing: {backup_path_value}")
        if file_digest(backup_path).casefold() != digest.casefold():
            raise LifecycleError(f"migration backup hash mismatch: {backup_path_value}")
        if source_path.exists() and not source_path.is_file():
            raise LifecycleError(f"migration source is not a file: {source_path_value}")
        if source_path.exists() != source_exists_after:
            raise LifecycleError(
                f"migration source existence does not match metadata: {source_path_value}"
            )
        if disposition == "pointer" and not source_exists_after:
            raise LifecycleError(
                f"pointer migration source must remain at its historical path: {source_path_value}"
            )
        seen_artifacts.add(artifact_id)
        seen_sources.add(source_path_value)
        seen_backups.add(backup_path_value)

    if status == "completed" and not recovery["rollback_available"]:
        raise LifecycleError("completed migration must retain rollback_available")


def validate_manifest(root: Path, manifest_path: Path) -> bool:
    root = root.resolve()
    manifest_path = manifest_path.resolve()
    try:
        manifest_path.relative_to(root)
    except ValueError as exc:
        raise LifecycleError("manifest must be inside the repository root") from exc
    manifest = read_json(manifest_path, "lifecycle manifest")
    if manifest.get("schema_version") != 1:
        raise LifecycleError("lifecycle manifest schema_version must be 1")

    canonical = require_list(manifest.get("canonical"), "manifest.canonical")
    pointers = require_list(manifest.get("pointers"), "manifest.pointers")
    approved = require_list(manifest.get("approved_artifacts"), "manifest.approved_artifacts")
    archive_paths = require_list(
        manifest.get("historical_archive_paths", []),
        "manifest.historical_archive_paths",
    )
    archive_set: set[str] = set()
    for value in archive_paths:
        archive_path = safe_relative(value, "historical archive path")
        if not resolve_path(root, archive_path, "historical archive path").is_file():
            raise LifecycleError(f"missing historical archive path: {archive_path}")
        archive_set.add(archive_path)

    canonical_by_id: dict[str, dict[str, Any]] = {}
    canonical_by_path: dict[str, dict[str, Any]] = {}
    canonical_by_key: dict[str, dict[str, Any]] = {}
    content_paths: dict[str, str] = {}
    for index, raw in enumerate(canonical):
        record = require_object(raw, f"canonical[{index}]")
        validate_envelope(record, f"canonical[{index}]")
        path_value = safe_relative(record.get("path"), f"canonical[{index}].path")
        key = record.get("canonical_key")
        if not isinstance(key, str) or not key.strip():
            raise LifecycleError(f"canonical[{index}].canonical_key must be non-empty")
        artifact_id = record["artifact_id"]
        if artifact_id in canonical_by_id:
            raise LifecycleError(f"duplicate canonical artifact: {artifact_id}")
        if path_value in canonical_by_path:
            raise LifecycleError(f"duplicate canonical path: {path_value}")
        if key in canonical_by_key:
            raise LifecycleError(f"duplicate canonical claim: {key}")
        path = resolve_path(root, path_value, f"canonical[{index}].path")
        if not path.is_file():
            raise LifecycleError(f"missing canonical artifact: {path_value}")
        validate_actual_metadata(record, path, f"canonical[{index}]")
        digest = file_digest(path)
        if path_value not in archive_set and digest in content_paths:
            raise LifecycleError(
                f"duplicate full-text artifact: {path_value} matches {content_paths[digest]}"
            )
        if path_value not in archive_set:
            content_paths[digest] = path_value
        canonical_by_id[artifact_id] = record
        canonical_by_path[path_value] = record
        canonical_by_key[key] = record

    for index, raw in enumerate(approved):
        artifact_id = require_id(raw, f"approved_artifacts[{index}]")
        if artifact_id not in canonical_by_id:
            raise LifecycleError(f"orphaned approved artifact: {artifact_id}")

    pointer_ids: set[str] = set()
    pointer_paths: set[str] = set()
    for index, raw in enumerate(pointers):
        record = require_object(raw, f"pointers[{index}]")
        validate_envelope(record, f"pointers[{index}]")
        pointer_path = safe_relative(record.get("path"), f"pointers[{index}].path")
        target_id = require_id(record.get("target_artifact_id"), f"pointers[{index}].target_artifact_id")
        canonical_path = safe_relative(record.get("canonical_path"), f"pointers[{index}].canonical_path")
        history_link = safe_relative(record.get("history_link"), f"pointers[{index}].history_link")
        if target_id not in canonical_by_id:
            raise LifecycleError(f"pointer target is not canonical: {target_id}")
        target = canonical_by_id[target_id]
        expected_path = safe_relative(target["path"], f"canonical target {target_id}.path")
        if canonical_path != expected_path:
            raise LifecycleError(f"pointer canonical path does not match target: {canonical_path}")
        if record["status"] != target["status"]:
            raise LifecycleError(f"pointer status does not match target: {pointer_path}")
        if record["artifact_id"] in pointer_ids:
            raise LifecycleError(f"duplicate pointer artifact: {record['artifact_id']}")
        if pointer_path in pointer_paths:
            raise LifecycleError(f"duplicate pointer path: {pointer_path}")
        pointer_file = resolve_path(root, pointer_path, f"pointers[{index}].path")
        if not pointer_file.is_file():
            raise LifecycleError(f"missing pointer file: {pointer_path}")
        history_file = resolve_path(root, history_link, f"pointers[{index}].history_link")
        if not history_file.is_file():
            raise LifecycleError(f"missing pointer history link: {history_link}")
        validate_actual_metadata(record, pointer_file, f"pointers[{index}]")
        pointer_ids.add(record["artifact_id"])
        pointer_paths.add(pointer_path)
        digest = file_digest(pointer_file)
        if pointer_path not in archive_set and digest in content_paths:
            raise LifecycleError(
                f"duplicate full-text artifact: {pointer_path} matches {content_paths[digest]}"
            )
        if pointer_path not in archive_set:
            content_paths[digest] = pointer_path

    for record in canonical:
        if record["artifact_type"] != "Decision Packet":
            continue
        path = resolve_path(root, record["path"], "Decision Packet path")
        if path.suffix.casefold() != ".json":
            continue
        packet = read_json(path, "Decision Packet")
        knowledge_change = require_object(
            packet.get("knowledge_change"),
            "Decision Packet knowledge_change",
        )
        summary_required = knowledge_change.get("summary_required")
        summary_id = knowledge_change.get("summary_artifact_id")
        summary_ids = {
            item["artifact_id"]
            for item in canonical
            if item.get("artifact_type") == "Knowledge Base Change Summary"
            and item.get("workflow_id") == record["workflow_id"]
        }
        if summary_required is True and summary_id not in summary_ids:
            raise LifecycleError("Decision Packet requires a canonical Knowledge Base Change Summary")
        if summary_required is False and summary_id is not None:
            raise LifecycleError("Decision Packet without durable change must omit summary_artifact_id")

    migration_present = "migration" in manifest
    if migration_present:
        validate_migration(root, manifest["migration"], canonical_by_id)
    return migration_present


def main() -> int:
    args = parse_args()
    try:
        migration_present = validate_manifest(args.root, args.manifest)
    except (LifecycleError, OSError) as exc:
        print(f"Document lifecycle validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Document lifecycle validation passed: {args.manifest}")
    if migration_present:
        print("Migration recovery validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
