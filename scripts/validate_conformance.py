#!/usr/bin/env python3
"""Validate an adapter manifest against the portable workflow core catalog."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


class ConformanceError(ValueError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
    except FileNotFoundError as exc:
        raise ConformanceError(f"file not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise ConformanceError(f"invalid YAML in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConformanceError(f"expected a mapping in {path}")
    return value


def require_string(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConformanceError(f"missing non-empty string: {key}")
    return value.strip()


def require_string_list(mapping: dict[str, Any], key: str) -> list[str]:
    value = mapping.get(key)
    if not isinstance(value, list) or not value:
        raise ConformanceError(f"missing non-empty list: {key}")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ConformanceError(f"{key} must contain non-empty strings")
    return [item.strip() for item in value]


def validate(catalog: dict[str, Any], manifest: dict[str, Any]) -> tuple[str, str]:
    core_version = require_string(catalog, "core_version")
    adapter_id = require_string(manifest, "adapter_id")
    require_string(manifest, "adapter_version")
    require_string(manifest, "target")
    require_string(manifest, "artifact_persistence")

    manifest_version = require_string(manifest, "core_version")
    if manifest_version != core_version:
        raise ConformanceError(
            f"incompatible core version: adapter={manifest_version}, core={core_version}"
        )

    rules = catalog.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ConformanceError("core catalog has no rules")
    rule_ids: list[str] = []
    mandatory: set[str] = set()
    for rule in rules:
        if not isinstance(rule, dict):
            raise ConformanceError("core catalog rule must be a mapping")
        rule_id = require_string(rule, "id")
        rule_ids.append(rule_id)
        if rule.get("mandatory") is True:
            mandatory.add(rule_id)
    if len(rule_ids) != len(set(rule_ids)):
        raise ConformanceError("core catalog contains duplicate rule IDs")

    implemented_list = require_string_list(manifest, "implemented_rules")
    if len(implemented_list) != len(set(implemented_list)):
        raise ConformanceError("implemented_rules contains duplicates")
    implemented = set(implemented_list)
    unknown = sorted(implemented - set(rule_ids))
    if unknown:
        raise ConformanceError(f"unknown rules: {', '.join(unknown)}")
    missing = sorted(mandatory - implemented)
    if missing:
        raise ConformanceError(f"missing mandatory rules: {', '.join(missing)}")

    profiles = catalog.get("capability_profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise ConformanceError("core catalog has no capability profiles")
    capabilities = require_string_list(manifest, "capabilities")
    unknown_capabilities = sorted(set(capabilities) - set(profiles))
    if unknown_capabilities:
        raise ConformanceError(
            f"unknown capability profiles: {', '.join(unknown_capabilities)}"
        )

    capability_set = set(capabilities)
    for capability in capabilities:
        profile = profiles[capability]
        if not isinstance(profile, dict):
            raise ConformanceError(f"invalid capability profile: {capability}")
        includes = profile.get("includes", [])
        if not isinstance(includes, list):
            raise ConformanceError(f"invalid capability hierarchy: {capability}")
        missing_includes = sorted(set(includes) - capability_set)
        if missing_includes:
            raise ConformanceError(
                f"incomplete capability hierarchy for {capability}: "
                f"missing {', '.join(missing_includes)}"
            )

    evidence = manifest.get("capability_evidence")
    if not isinstance(evidence, dict):
        raise ConformanceError("missing capability_evidence mapping")
    for capability in capabilities:
        items = evidence.get(capability)
        if not isinstance(items, list) or not items or any(
            not isinstance(item, str) or not item.strip() for item in items
        ):
            raise ConformanceError(f"capability lacks evidence: {capability}")

    validation = manifest.get("validation")
    if not isinstance(validation, dict):
        raise ConformanceError("missing validation mapping")
    require_string(validation, "status")
    require_string(validation, "environment")
    require_string_list(validation, "commands")

    return adapter_id, core_version


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        catalog = load_yaml(args.catalog)
        manifest = load_yaml(args.manifest)
        adapter_id, core_version = validate(catalog, manifest)
    except ConformanceError as exc:
        print(f"Conformance failed: {exc}", file=sys.stderr)
        return 1
    print(f"Conformance passed: {adapter_id} against core {core_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
