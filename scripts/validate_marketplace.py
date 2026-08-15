#!/usr/bin/env python3
"""Validate the official Ask Then Do It repository marketplace catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / ".agents" / "plugins" / "marketplace.json"


class CatalogError(RuntimeError):
    """The marketplace catalog violates the approved release contract."""


def require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    missing = sorted(expected - set(value))
    unknown = sorted(set(value) - expected)
    if missing or unknown:
        details = []
        if missing:
            details.append(f"missing {missing}")
        if unknown:
            details.append(f"unknown {unknown}")
        raise CatalogError(f"Invalid {label} fields: {', '.join(details)}")


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CatalogError(f"{label} must be an object")
    return value


def validate_catalog(value: dict[str, Any], *, expected_ref: str = "v1.3.0") -> None:
    require_exact_keys(value, {"name", "interface", "plugins"}, "catalog")
    if value["name"] != "ask-then-do-it":
        raise CatalogError("catalog.name must be 'ask-then-do-it'")

    interface = require_object(value["interface"], "catalog.interface")
    require_exact_keys(interface, {"displayName"}, "catalog.interface")
    if interface["displayName"] != "Ask Then Do It":
        raise CatalogError("catalog.interface.displayName must be 'Ask Then Do It'")

    plugins = value["plugins"]
    if not isinstance(plugins, list) or len(plugins) != 1:
        raise CatalogError("catalog.plugins must contain exactly one entry")
    plugin = require_object(plugins[0], "catalog.plugins[0]")
    require_exact_keys(
        plugin,
        {"name", "source", "policy", "category"},
        "catalog.plugins[0]",
    )
    if plugin["name"] != "ask-then-do-it":
        raise CatalogError("Plugin name must be 'ask-then-do-it'")
    if plugin["category"] != "Developer Tools":
        raise CatalogError("Plugin category must be 'Developer Tools'")

    source = require_object(plugin["source"], "catalog.plugins[0].source")
    require_exact_keys(source, {"source", "url", "path", "ref"}, "Plugin source")
    expected_source = {
        "source": "git-subdir",
        "url": "https://github.com/Mysterio1001/Ask-Then-Do-It.git",
        "path": "adapters/codex/plugin/ask-then-do-it",
        "ref": expected_ref,
    }
    if source != expected_source:
        raise CatalogError(
            f"Plugin source must match the official tag-pinned source at {expected_ref}"
        )

    policy = require_object(plugin["policy"], "catalog.plugins[0].policy")
    require_exact_keys(policy, {"installation", "authentication"}, "Plugin policy")
    expected_policy = {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }
    if policy != expected_policy:
        raise CatalogError("Plugin policy must be AVAILABLE with ON_INSTALL authentication")


def load_and_validate(path: Path, *, expected_ref: str = "v1.3.0") -> None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CatalogError(f"Missing marketplace catalog: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CatalogError(f"Invalid JSON in marketplace catalog {path}: {exc}") from exc
    validate_catalog(require_object(value, "catalog"), expected_ref=expected_ref)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    try:
        load_and_validate(args.catalog.resolve())
    except (CatalogError, OSError) as exc:
        print(f"Marketplace validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Marketplace validation passed: {args.catalog}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
