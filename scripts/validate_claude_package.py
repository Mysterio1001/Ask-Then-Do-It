#!/usr/bin/env python3
"""Standard-library Claude runtime inventory and source-parity checks.

This checks package bytes, not Claude behavior, authentication, or release gates.
"""
from __future__ import annotations

import json
from pathlib import Path, PurePosixPath


SOURCE = "adapters/claude-code/plugin/ask-then-do-it"
NAME = "ask-then-do-it"
MODULES = (
    "orchestration.md", "lite-workflow.md", "requirements.md",
    "documented-requirements.md", "specification.md", "ticket-planning.md",
    "tdd-implementation.md", "direct-implementation.md", "review.md",
    "architecture-improvement.md",
)
RUNTIME_FILES = frozenset({
    ".claude-plugin/plugin.json", "skills/ask-then-do-it/SKILL.md",
    "skills/ask-then-do-it-5/SKILL.md", "agents/ask-then-do-it-reviewer.md",
    "hooks/hooks.json", "scripts/router.mjs", "config/model-classifications.json",
    "START-HERE.en.md", "START-HERE.zh-TW.md", "START-HERE.ja.md",
    *(f"profiles/{profile}/{name}" for profile in ("general", "claude-5") for name in MODULES),
})
LEGAL_FILES = frozenset({"LICENSE", "THIRD_PARTY_NOTICES.md"})


class ClaudePackageError(ValueError):
    """The exact runtime/package boundary was violated."""


def is_link(path: Path) -> bool:
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def check_tree(root: Path, expected: set[str] | frozenset[str]) -> None:
    if is_link(root) or not root.is_dir():
        raise ClaudePackageError("Claude payload root must be a real directory")
    expected_dirs = {
        parent.as_posix() for name in expected for parent in PurePosixPath(name).parents
        if parent.as_posix() != "."
    }
    actual_files, actual_dirs = set(), set()
    for path in root.rglob("*"):
        name = path.relative_to(root).as_posix()
        if is_link(path) or not path.resolve().is_relative_to(root.resolve()):
            raise ClaudePackageError(f"Claude payload link or path escape: {name}")
        if path.is_file():
            actual_files.add(name)
        elif path.is_dir():
            actual_dirs.add(name)
        else:
            raise ClaudePackageError(f"Claude payload non-regular entry: {name}")
    if actual_files != set(expected) or actual_dirs != expected_dirs:
        raise ClaudePackageError(
            "Claude exact inventory mismatch: "
            f"missing={sorted(set(expected) - actual_files)}, "
            f"extra={sorted(actual_files - set(expected))}, "
            f"unexpected-directories={sorted(actual_dirs - expected_dirs)}"
        )


def validate_source(repository: Path, version: str) -> Path:
    source = repository / SOURCE
    for path in (source, *source.parents):
        if path == repository.parent:
            break
        if is_link(path):
            raise ClaudePackageError("Claude source ancestors must not be links")
    check_tree(source, RUNTIME_FILES)
    try:
        manifest = json.loads((source / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise ClaudePackageError("Invalid Claude package manifest") from exc
    if not isinstance(manifest, dict) or any(manifest.get(key) != value for key, value in {
        "name": NAME, "displayName": "Ask Then Do It", "version": version,
    }.items()):
        raise ClaudePackageError("Claude source package identity/version mismatch")
    for name in LEGAL_FILES:
        path = repository / name
        if is_link(path) or not path.is_file():
            raise ClaudePackageError(f"Missing regular canonical legal file: {name}")
    return source


def source_payload(repository: Path, version: str) -> dict[str, bytes]:
    source = validate_source(repository, version)
    return {
        **{name: (source / name).read_bytes() for name in sorted(RUNTIME_FILES)},
        **{name: (repository / name).read_bytes() for name in sorted(LEGAL_FILES)},
    }


def validate_parity(package: Path, repository: Path, version: str) -> None:
    check_tree(package, RUNTIME_FILES | LEGAL_FILES)
    for name, expected in source_payload(repository, version).items():
        if (package / name).read_bytes() != expected:
            raise ClaudePackageError(f"Claude package differs from canonical source: {name}")
