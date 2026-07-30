#!/usr/bin/env python3
"""Build deterministic, runtime-only Ask Then Do It release packages.

The repository sources and ``release/release.json`` are authoritative. Generated
files under the selected output root are disposable and must not be edited.
This script intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import uuid
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "release" / "release.json"
DEFAULT_OUTPUT = ROOT / "dist"
LEGAL_FILES = ("LICENSE", "THIRD_PARTY_NOTICES.md")
START_GUIDE_FILES = (
    "START-HERE.zh-TW.md",
    "START-HERE.en.md",
    "START-HERE.ja.md",
)
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
TOP_LEVEL_KEYS = {
    "schema_version",
    "package_id",
    "display_name",
    "release_version",
    "core_version",
    "codex",
    "generic",
    "required_validation_checks",
    "managed_outputs",
}
CODEX_KEYS = {"source", "directory", "archive", "skills"}
GENERIC_KEYS = {
    "source",
    "directory",
    "archive",
    "entrypoint",
    "start_guide",
    "modules",
}


class BuildError(RuntimeError):
    """A release contract or safe-build boundary was violated."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--allow-test-output-root",
        action="store_true",
        help="Permit an isolated repository-owned output root for automated tests.",
    )
    parser.add_argument(
        "--package", choices=("all", "codex", "generic"), default="all"
    )
    return parser.parse_args()


def read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BuildError(f"Missing {label}: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BuildError(f"Invalid JSON in {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BuildError(f"{label} must contain a JSON object: {path}")
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
        raise BuildError(f"Invalid {label} fields: {', '.join(details)}")


def require_string(value: dict[str, Any], key: str, label: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item.strip():
        raise BuildError(f"{label}.{key} must be a non-empty string")
    return item


def validate_relative_name(raw: str, label: str) -> str:
    path = PurePosixPath(raw.replace("\\", "/"))
    if path.is_absolute() or len(path.parts) != 1 or path.parts[0] in {"", ".", ".."}:
        raise BuildError(f"{label} must be one relative output name: {raw!r}")
    return path.as_posix()


def validate_relative_output_path(raw: str, label: str) -> str:
    path = PurePosixPath(raw.replace("\\", "/"))
    if (
        path.is_absolute()
        or len(path.parts) < 2
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise BuildError(
            f"{label} must be a nested relative output path: {raw!r}"
        )
    return path.as_posix()


def read_top_level_yaml_scalar(path: Path, key: str) -> str:
    """Read one unindented scalar without adding a YAML build dependency."""

    pattern = re.compile(rf"^{re.escape(key)}:\s*([^#\s]+)\s*(?:#.*)?$")
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise BuildError(f"Missing canonical declaration: {path}") from exc
    for line in lines:
        match = pattern.fullmatch(line)
        if match:
            return match.group(1).strip("\"'")
    raise BuildError(f"Missing top-level {key} declaration: {path}")


def load_config(path: Path) -> dict[str, Any]:
    config = read_json_object(path.resolve(), "release configuration")
    require_exact_keys(config, TOP_LEVEL_KEYS, "release configuration")
    if config["schema_version"] != 2:
        raise BuildError("release configuration schema_version must be 2")
    for key in ("package_id", "display_name", "release_version", "core_version"):
        require_string(config, key, "release configuration")
    for key in ("release_version", "core_version"):
        if SEMVER.fullmatch(config[key]) is None:
            raise BuildError(f"release configuration.{key} must be strict semver")
    core_declarations = (
        ROOT / "core" / "rules" / "rules.yaml",
        ROOT / "adapters" / "codex" / "conformance.yaml",
        ROOT / "adapters" / "generic-prompts" / "manifest.yaml",
    )
    for declaration in core_declarations:
        actual_core = read_top_level_yaml_scalar(declaration, "core_version")
        if actual_core != config["core_version"]:
            raise BuildError(
                "release configuration.core_version conflicts with "
                f"{declaration.relative_to(ROOT).as_posix()}: {actual_core}"
            )

    codex = config.get("codex")
    if not isinstance(codex, dict):
        raise BuildError("release configuration.codex must be an object")
    require_exact_keys(codex, CODEX_KEYS, "release configuration.codex")
    for key in ("source", "directory", "archive"):
        require_string(codex, key, "release configuration.codex")
    validate_relative_output_path(codex["directory"], "codex.directory")
    validate_relative_output_path(codex["archive"], "codex.archive")
    if PurePosixPath(codex["directory"]).parts[0] != "codex" or PurePosixPath(
        codex["archive"]
    ).parts[0] != "codex":
        raise BuildError("Codex outputs must stay under the codex provider directory")
    skills = codex.get("skills")
    if not isinstance(skills, list) or not skills or not all(
        isinstance(item, str) and item.strip() for item in skills
    ):
        raise BuildError("release configuration.codex.skills must be a non-empty string array")
    if len(skills) != len(set(skills)):
        raise BuildError("release configuration.codex.skills contains duplicates")

    generic = config.get("generic")
    if not isinstance(generic, dict):
        raise BuildError("release configuration.generic must be an object")
    require_exact_keys(generic, GENERIC_KEYS, "release configuration.generic")
    for key in ("source", "directory", "archive", "entrypoint", "start_guide"):
        require_string(generic, key, "release configuration.generic")
    for key in ("directory", "archive"):
        validate_relative_output_path(generic[key], f"generic.{key}")
    validate_relative_name(generic["entrypoint"], "generic.entrypoint")
    start_guide = (ROOT / generic["start_guide"]).resolve()
    if not start_guide.is_relative_to(ROOT) or not start_guide.is_file():
        raise BuildError(f"Missing Generic start guide source: {start_guide}")
    if start_guide.name != "START-HERE.zh-TW.md":
        raise BuildError(
            "generic.start_guide must identify START-HERE.zh-TW.md"
        )
    missing_start_guides = [
        name for name in START_GUIDE_FILES if not (start_guide.parent / name).is_file()
    ]
    if missing_start_guides:
        raise BuildError(f"Missing localized Generic start guides: {missing_start_guides}")
    if PurePosixPath(generic["directory"]).parts[0] != "generic" or PurePosixPath(
        generic["archive"]
    ).parts[0] != "generic":
        raise BuildError("Generic outputs must stay under the generic provider directory")
    modules = generic.get("modules")
    if not isinstance(modules, list) or not modules or not all(
        isinstance(item, str) and item.strip() for item in modules
    ):
        raise BuildError(
            "release configuration.generic.modules must be a non-empty string array"
        )
    for item in modules:
        validate_relative_name(item, "generic.modules entry")
    if len(modules) != len(set(modules)):
        raise BuildError("release configuration.generic.modules contains duplicates")

    required_checks = config.get("required_validation_checks")
    if not isinstance(required_checks, list) or not required_checks or not all(
        isinstance(item, str) and item.strip() for item in required_checks
    ):
        raise BuildError(
            "release configuration.required_validation_checks must be a "
            "non-empty string array"
        )
    if len(required_checks) != len(set(required_checks)):
        raise BuildError(
            "release configuration.required_validation_checks contains duplicates"
        )

    managed = config.get("managed_outputs")
    if not isinstance(managed, list) or not managed:
        raise BuildError("release configuration.managed_outputs must be a non-empty array")
    normalized = [validate_relative_name(item, "managed_outputs entry") for item in managed]
    if len(normalized) != len(set(normalized)):
        raise BuildError("release configuration.managed_outputs contains duplicates")
    expected = {"codex", "generic", "checksums.sha256"}
    if set(normalized) != expected:
        raise BuildError(f"managed_outputs must equal configured outputs: {sorted(expected)}")
    return config


def source_path(relative: str, label: str) -> Path:
    candidate = (ROOT / relative).resolve()
    if not candidate.is_relative_to(ROOT):
        raise BuildError(f"{label} escapes the repository: {relative}")
    if not candidate.is_dir():
        raise BuildError(f"Missing {label}: {candidate}")
    return candidate


def list_files(root: Path) -> list[Path]:
    return sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def validate_codex_source(config: dict[str, Any]) -> Path:
    codex = config["codex"]
    plugin = source_path(codex["source"], "Codex Plugin source")
    manifest = read_json_object(plugin / ".codex-plugin" / "plugin.json", "Plugin manifest")
    if plugin.name != config["package_id"] or manifest.get("name") != plugin.name:
        raise BuildError(
            "Codex Plugin folder, release package_id, and plugin.json name must match"
        )
    if PurePosixPath(codex["directory"]).name != plugin.name:
        raise BuildError("codex.directory basename must match the Codex Plugin root name")
    if manifest.get("version") != config["release_version"]:
        raise BuildError("Plugin version must match release_version")
    if manifest.get("skills") != "./skills/":
        raise BuildError("Plugin manifest skills must be './skills/'")
    interface = manifest.get("interface")
    if not isinstance(interface, dict) or interface.get("displayName") != config["display_name"]:
        raise BuildError("Plugin displayName must match release display_name")

    skills_root = plugin / "skills"
    actual_skills = sorted(path.name for path in skills_root.iterdir() if path.is_dir())
    if actual_skills != sorted(codex["skills"]):
        raise BuildError(
            f"Codex Skill inventory mismatch: expected {sorted(codex['skills'])}, "
            f"found {actual_skills}"
        )
    for skill in actual_skills:
        if not (skills_root / skill / "SKILL.md").is_file():
            raise BuildError(f"Codex Skill is missing SKILL.md: {skill}")
    missing_start_guides = [
        name for name in START_GUIDE_FILES if not (plugin / name).is_file()
    ]
    if missing_start_guides:
        raise BuildError(f"Codex Plugin source is missing start guides: {missing_start_guides}")
    top_level = {path.name for path in plugin.iterdir()}
    if top_level != {".codex-plugin", "skills", *START_GUIDE_FILES}:
        raise BuildError(f"Unexpected Codex Plugin source entries: {sorted(top_level)}")
    return plugin


def write_reproducible_zip(source: Path, archive: Path, archive_root: str) -> None:
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in list_files(source):
            relative = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(f"{archive_root}/{relative}", ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_file_names(root: Path) -> set[str]:
    return {path.relative_to(root).as_posix() for path in list_files(root)}


def verify_zip_equivalence(directory: Path, archive: Path, archive_root: str) -> None:
    expected = {
        f"{archive_root}/{relative}" for relative in relative_file_names(directory)
    }
    try:
        with zipfile.ZipFile(archive) as bundle:
            actual = {name for name in bundle.namelist() if not name.endswith("/")}
            if actual != expected:
                raise BuildError(
                    f"ZIP inventory differs from directory for {archive.name}"
                )
            for entry in sorted(expected):
                relative = entry.removeprefix(f"{archive_root}/")
                if bundle.read(entry) != (directory / relative).read_bytes():
                    raise BuildError(
                        f"ZIP content differs from directory: {archive.name}:{entry}"
                    )
    except (zipfile.BadZipFile, KeyError) as exc:
        raise BuildError(f"Invalid ZIP archive: {archive}") from exc


def read_checksums(path: Path) -> dict[str, str]:
    try:
        lines = path.read_text(encoding="ascii").splitlines()
    except (FileNotFoundError, UnicodeDecodeError) as exc:
        raise BuildError(f"Invalid or missing checksum file: {path}") from exc
    result: dict[str, str] = {}
    for line in lines:
        parts = line.split("  ", 1)
        if (
            len(parts) != 2
            or re.fullmatch(r"[0-9a-f]{64}", parts[0]) is None
            or not parts[1]
            or parts[1] in result
        ):
            raise BuildError(f"Invalid checksum entry in {path}: {line!r}")
        result[parts[1]] = parts[0]
    return result


def selected_output_names(config: dict[str, Any], selected: list[str]) -> list[str]:
    names = [PurePosixPath(config[package_id]["directory"]).parts[0] for package_id in selected]
    names.append("checksums.sha256")
    return names


def expected_package_files(
    config: dict[str, Any], package_id: str
) -> set[str]:
    if package_id == "codex":
        source = validate_codex_source(config)
        return relative_file_names(source) | set(LEGAL_FILES)
    generic = config["generic"]
    return {
        *START_GUIDE_FILES,
        *LEGAL_FILES,
        generic["entrypoint"],
        "manifest.yaml",
        *{f"prompts/{name}" for name in generic["modules"]},
    }


def validate_output_set(
    root: Path,
    config: dict[str, Any],
    selected: list[str],
    *,
    allow_absent: bool,
    require_source_equivalence: bool,
) -> list[str]:
    """Validate a complete output set, or report that no selected output exists."""

    names = selected_output_names(config, selected)
    present = sorted(path.name for path in root.iterdir()) if root.exists() else []
    if not present and allow_absent:
        return []
    if set(present) != set(names):
        collision = (root / (present[0] if present else names[0])).resolve()
        raise BuildError(f"Unmanaged or incomplete output collision: {collision}")

    archives = [config[package_id]["archive"] for package_id in selected]
    checksums = read_checksums(root / "checksums.sha256")
    if set(checksums) != set(archives):
        raise BuildError(
            f"Checksum inventory does not match selected release archives: {root}"
        )
    for archive_name in archives:
        archive = root / archive_name
        if sha256(archive) != checksums[archive_name]:
            raise BuildError(f"Checksum mismatch: {archive}")

    for package_id in selected:
        package = config[package_id]
        directory = root / package["directory"]
        archive = root / package["archive"]
        if require_source_equivalence and relative_file_names(
            directory
        ) != expected_package_files(config, package_id):
            raise BuildError(f"Runtime package inventory mismatch: {directory}")
        verify_zip_equivalence(
            directory, archive, PurePosixPath(package["directory"]).name
        )

    codex_manifest = root / config["codex"]["directory"] / ".codex-plugin" / "plugin.json"
    if "codex" in selected:
        manifest = read_json_object(codex_manifest, "built Plugin manifest")
        if (
            manifest.get("name") != config["package_id"]
            or manifest.get("version") != config["release_version"]
        ):
            raise BuildError(f"Built Plugin identity mismatch: {codex_manifest}")
    if "generic" in selected:
        manifest_path = root / config["generic"]["directory"] / "manifest.yaml"
        if manifest_path.read_text(encoding="utf-8") != generic_manifest(config):
            raise BuildError(f"Built Generic manifest identity mismatch: {manifest_path}")
    return names


def build_codex(config: dict[str, Any], staging: Path) -> list[str]:
    source = validate_codex_source(config)
    codex = config["codex"]
    package = staging / codex["directory"]
    package.parent.mkdir(parents=True)
    shutil.copytree(source, package, copy_function=shutil.copyfile)
    for legal_file in LEGAL_FILES:
        shutil.copyfile(ROOT / legal_file, package / legal_file)
    archive = staging / codex["archive"]
    write_reproducible_zip(package, archive, PurePosixPath(codex["directory"]).name)
    return [codex["directory"], codex["archive"]]


def validate_generic_source(config: dict[str, Any]) -> Path:
    generic = config["generic"]
    source = source_path(generic["source"], "Generic prompt source")
    missing = [name for name in generic["modules"] if not (source / name).is_file()]
    if missing:
        raise BuildError(f"Missing Generic prompt modules: {missing}")
    if (source / generic["entrypoint"]).exists():
        raise BuildError(
            "The Generic combined entrypoint must be generated, not maintained in source"
        )
    return source


def compose_generic_workflow(config: dict[str, Any], source: Path) -> bytes:
    generic = config["generic"]
    header = f"""<!-- GENERATED FILE — DO NOT EDIT -->
# {config['display_name']} — Generic Workflow

Release version: `{config['release_version']}`  
Core version: `{config['core_version']}`  
Capability: `conversation`

## Internal routing contract

Use the included sections internally; do not ask the user to paste another module prompt.
Match the user's language in user-facing output. Begin with the bootstrap section for a
fresh or resumed request, use the orchestration section to identify the first unmet gate,
then apply exactly one matching stage section at a time. Preserve every explicit approval
gate, stop condition, Artifact contract, and user-managed persistence reminder.

For a fresh workflow whose first unmet stage is requirement consensus, apply the selected
requirement section in the same effective response. After a concise capability and stage
declaration, ask exactly one high-impact requirement question in the user's language and
include a recommended answer and the principal tradeoff. Do not stop at routing status,
promise to ask later, or require the user to say "start".

## Conversation-only capability boundary

Do not claim repository access, file changes, command or test execution, durable storage,
completed TDD, or independent review. Implementation remains `UNEXECUTED IMPLEMENTATION
GUIDANCE`; review remains `limited-evidence` and `non-independent` unless a different
validated host takes over with the required raw artifacts.
"""
    payload = bytearray(header.encode("utf-8"))
    for name in generic["modules"]:
        payload.extend(f"\n\n<!-- BEGIN SOURCE: {name} -->\n".encode("utf-8"))
        module = (source / name).read_bytes()
        payload.extend(module)
        if not module.endswith((b"\n", b"\r")):
            payload.extend(b"\n")
        payload.extend(f"<!-- END SOURCE: {name} -->\n".encode("utf-8"))
    return bytes(payload)


def yaml_string(value: str) -> str:
    """Return a JSON string, which is also a valid YAML scalar."""

    return json.dumps(value, ensure_ascii=False)


def generic_manifest(config: dict[str, Any]) -> str:
    generic = config["generic"]
    lines = [
        "# GENERATED FILE — DO NOT EDIT",
        "schema_version: 1",
        f"package_id: {yaml_string(config['package_id'])}",
        f"display_name: {yaml_string(config['display_name'])}",
        f"release_version: {yaml_string(config['release_version'])}",
        f"core_version: {yaml_string(config['core_version'])}",
        'adapter_id: "generic-prompts"',
        'entrypoint: "generic-workflow.md"',
        'artifact_persistence: "user-managed-markdown"',
        "capabilities:",
        '  - "conversation"',
        "source_modules:",
    ]
    lines.extend(f"  - {yaml_string(name)}" for name in generic["modules"])
    lines.append("")
    return "\n".join(lines)


def build_generic(config: dict[str, Any], staging: Path) -> list[str]:
    source = validate_generic_source(config)
    generic = config["generic"]
    package = staging / generic["directory"]
    prompts = package / "prompts"
    prompts.mkdir(parents=True)
    for name in generic["modules"]:
        shutil.copyfile(source / name, prompts / name)
    start_guide_root = (ROOT / generic["start_guide"]).parent
    for name in START_GUIDE_FILES:
        shutil.copyfile(start_guide_root / name, package / name)
    for legal_file in LEGAL_FILES:
        shutil.copyfile(ROOT / legal_file, package / legal_file)
    (package / generic["entrypoint"]).write_bytes(
        compose_generic_workflow(config, source)
    )
    (package / "manifest.yaml").write_text(
        generic_manifest(config), encoding="utf-8", newline="\n"
    )
    archive = staging / generic["archive"]
    write_reproducible_zip(
        package, archive, PurePosixPath(generic["directory"]).name
    )
    return [generic["directory"], generic["archive"]]


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def commit(
    staging: Path,
    output_root: Path,
    names: list[str],
    *,
    existing_names: list[str],
) -> None:
    for name in names:
        target = (output_root / name).resolve()
        if not target.is_relative_to(output_root):
            raise BuildError(f"Managed target escapes output root: {target}")
    backup = staging / ".previous-release"
    moved_old: list[str] = []
    placed_new: list[str] = []
    try:
        if existing_names:
            backup.mkdir()
            for name in existing_names:
                os.replace(output_root / name, backup / name)
                moved_old.append(name)
        for name in names:
            os.replace(staging / name, output_root / name)
            placed_new.append(name)
    except OSError as exc:
        for name in reversed(placed_new):
            remove_path(output_root / name)
        for name in reversed(moved_old):
            if (backup / name).exists():
                os.replace(backup / name, output_root / name)
        raise BuildError(f"Atomic release replacement failed: {exc}") from exc


def main() -> int:
    args = parse_args()
    staging: Path | None = None
    try:
        config = load_config(args.config)
        output_root = args.output_root.resolve()
        if not output_root.is_relative_to(ROOT):
            raise BuildError(f"Output root must stay inside the repository: {output_root}")
        if output_root != DEFAULT_OUTPUT.resolve() and not args.allow_test_output_root:
            raise BuildError(
                "Non-default output is test-only; pass --allow-test-output-root "
                "explicitly for an isolated repository-owned test target"
            )
        output_root.mkdir(parents=True, exist_ok=True)
        staging = output_root.parent / f".{output_root.name}-release-staging-{uuid.uuid4().hex}"
        staging.mkdir()

        selected = (
            ["codex", "generic"] if args.package == "all" else [args.package]
        )
        archives: list[str] = []
        if "codex" in selected:
            build_codex(config, staging)
            archives.append(config["codex"]["archive"])
        if "generic" in selected:
            build_generic(config, staging)
            archives.append(config["generic"]["archive"])

        checksum_name = "checksums.sha256"
        (staging / checksum_name).write_text(
            "".join(
                f"{sha256(staging / archive_name)}  {archive_name}\n"
                for archive_name in archives
            ),
            encoding="ascii",
            newline="\n",
        )
        outputs = selected_output_names(config, selected)
        validate_output_set(
            staging,
            config,
            selected,
            allow_absent=False,
            require_source_equivalence=True,
        )
        existing_names = validate_output_set(
            output_root,
            config,
            selected,
            allow_absent=True,
            require_source_equivalence=False,
        )
        commit(
            staging,
            output_root,
            outputs,
            existing_names=existing_names,
        )
        print(
            f"Built {', '.join(selected)} release {config['release_version']} "
            f"in {output_root}"
        )
        return 0
    except (BuildError, OSError) as exc:
        print(f"Release build failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if staging is not None and staging.exists():
            shutil.rmtree(staging)


if __name__ == "__main__":
    raise SystemExit(main())
