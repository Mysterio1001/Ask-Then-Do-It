#!/usr/bin/env python3
"""Validate Codex runtime references, rule mappings, and source-level measurements.

The context proxy reported here is a deterministic source measurement only. It
does not represent host-loaded total context or model billing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import string
import sys
import unicodedata
from dataclasses import dataclass
from html import unescape as unescape_html
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ADAPTER_ROOT = ROOT / "adapters" / "codex"
DEFAULT_SOURCE_PACKAGE = DEFAULT_ADAPTER_ROOT / "plugin" / "ask-then-do-it"
DEFAULT_RULE_MAPPING = DEFAULT_ADAPTER_ROOT / "rule-mapping.yaml"
DEFAULT_CORE_CATALOG = ROOT / "core" / "rules" / "rules.yaml"
DEFAULT_CONFORMANCE = DEFAULT_ADAPTER_ROOT / "conformance.yaml"
ALGORITHM_ID = "normalized-utf8-quarter-v1"
BYTES_PER_PROXY_TOKEN = 4
H2_HEADING = re.compile(r"^[ ]{0,3}##(?!#)(?:[ \t]+|$)(.*)$")
TOP_LEVEL_YAML_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]|$)")
RULE_ID = re.compile(r"^  ([A-Za-z][A-Za-z0-9-]*):[ \t]*$")
MAPPING_START = re.compile(r"^    - ([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*?)\s*$")
MAPPING_FIELD = re.compile(r"^      ([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*?)\s*$")
CORE_RULE_START = re.compile(r"^  - id:[ \t]*(.*?)\s*$")
CORE_RULE_MANDATORY = re.compile(r"^    mandatory:[ \t]*(.*?)\s*$")
YAML_LIST_ITEM = re.compile(r"^  -[ \t]+(.*?)\s*$")
WINDOWS_FORBIDDEN_COMPONENT_CHARACTERS = frozenset('<>:"|?*')
PERCENT_ENCODED_PATH_SEPARATOR = re.compile(r"%(?:2f|5c)", re.IGNORECASE)
WINDOWS_RESERVED_COMPONENT_BASENAMES = frozenset(
    {
        "con",
        "prn",
        "aux",
        "nul",
        *(f"com{number}" for number in range(1, 10)),
        *(f"lpt{number}" for number in range(1, 10)),
    }
)

DEFAULT_LOAD_SETS = {
    "root-router": ("skills/ask-then-do-it/SKILL.md",),
    "lite": (
        "skills/ask-then-do-it/SKILL.md",
        "skills/ask-then-do-it/references/lite-workflow.md",
    ),
    "full-requirements": (
        "skills/ask-then-do-it/SKILL.md",
        "skills/ask-then-do-it/references/full-routing.md",
        "skills/ask-requirements/SKILL.md",
    ),
    "full-documented-requirements": (
        "skills/ask-then-do-it/SKILL.md",
        "skills/ask-then-do-it/references/full-routing.md",
        "skills/ask-with-docs/SKILL.md",
    ),
    "full-specification": (
        "skills/ask-then-do-it/SKILL.md",
        "skills/ask-then-do-it/references/full-routing.md",
        "skills/write-spec/SKILL.md",
    ),
    "full-ticket-plan": (
        "skills/ask-then-do-it/SKILL.md",
        "skills/ask-then-do-it/references/full-routing.md",
        "skills/plan-tickets/SKILL.md",
    ),
    "full-implementation-tdd": (
        "skills/ask-then-do-it/SKILL.md",
        "skills/ask-then-do-it/references/full-routing.md",
        "skills/implement-tdd/SKILL.md",
    ),
    "full-implementation-direct": (
        "skills/ask-then-do-it/SKILL.md",
        "skills/ask-then-do-it/references/full-routing.md",
        "skills/implement-direct/SKILL.md",
    ),
    "full-review": (
        "skills/ask-then-do-it/SKILL.md",
        "skills/ask-then-do-it/references/full-routing.md",
        "skills/review-code/SKILL.md",
    ),
    "full-architecture": (
        "skills/ask-then-do-it/SKILL.md",
        "skills/ask-then-do-it/references/full-routing.md",
        "skills/improve-architecture/SKILL.md",
    ),
}

ARTIFACT_CONTRACT = "skills/ask-then-do-it/references/artifact-contract.md"
LENS_CONTRACT = (
    "skills/ask-then-do-it/references/architecture-refactoring-lenses.md"
)
ACTION_READY_LOAD_SETS = {
    name: (
        sources
        if not name.startswith("full-")
        else sources
        + ((LENS_CONTRACT,) if name in {"full-review", "full-architecture"} else ())
        + (ARTIFACT_CONTRACT,)
    )
    for name, sources in DEFAULT_LOAD_SETS.items()
}


@dataclass(frozen=True, order=True)
class Diagnostic:
    code: str
    detail: str
    source: str = ""
    target: str = ""

    def render(self) -> str:
        locations = []
        if self.source:
            locations.append(f"source={self.source}")
        if self.target:
            locations.append(f"target={self.target}")
        suffix = f" ({', '.join(locations)})" if locations else ""
        return f"{self.code}: {self.detail}{suffix}"


class CodexContractError(ValueError):
    """The Codex runtime contract has one or more fail-closed violations."""

    def __init__(self, diagnostics: list[Diagnostic]) -> None:
        self.diagnostics = tuple(sorted(set(diagnostics)))
        super().__init__("\n".join(item.render() for item in self.diagnostics))


@dataclass(frozen=True)
class ReferenceGraph:
    public_skills: tuple[str, ...]
    reference_targets: tuple[str, ...]
    graph: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class MappingSummary:
    runtime_targets: tuple[str, ...]
    metadata_targets: tuple[str, ...]


@dataclass(frozen=True)
class RuleMappingDocument:
    core_version: str | None
    rules: dict[str, list[dict[str, str]]]


@dataclass(frozen=True)
class CoreCatalog:
    core_version: str | None
    rule_ids: tuple[str, ...]
    mandatory_rule_ids: tuple[str, ...]


@dataclass(frozen=True)
class ConformanceManifest:
    core_version: str | None
    implemented_rule_ids: tuple[str, ...]


@dataclass(frozen=True)
class ContractSummary:
    reference_graph: ReferenceGraph
    mapping: MappingSummary


def is_link(path: Path) -> bool:
    return path.is_symlink() or (
        hasattr(path, "is_junction") and path.is_junction()  # type: ignore[attr-defined]
    )


def is_inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def lexical_absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def has_path_control_character(value: str) -> bool:
    return any(ord(character) < 32 or ord(character) == 127 for character in value)


def first_link_component(path: Path, root: Path) -> Path | None:
    root = lexical_absolute(root)
    path = lexical_absolute(path)
    try:
        relative = path.relative_to(root)
    except ValueError:
        return None
    probe = root
    if is_link(probe):
        return probe
    for part in relative.parts:
        probe /= part
        if is_link(probe):
            return probe
    return None


def first_case_mismatch(path: Path, root: Path) -> tuple[str, str] | None:
    root = lexical_absolute(root)
    path = lexical_absolute(path)
    try:
        relative = path.relative_to(root)
    except ValueError:
        return None

    probe = root
    for part in relative.parts:
        if not probe.is_dir():
            return None
        names = tuple(entry.name for entry in probe.iterdir())
        if part in names:
            probe /= part
            continue
        folded = unicodedata.normalize("NFC", part).casefold()
        actual = next(
            (
                name
                for name in names
                if unicodedata.normalize("NFC", name).casefold() == folded
            ),
            None,
        )
        if actual is not None:
            return part, actual
        return None
    return None


def resolves_through_unlisted_entry(path: Path, root: Path) -> bool:
    root = lexical_absolute(root)
    path = lexical_absolute(path)
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False

    probe = root
    for part in relative.parts:
        if not probe.is_dir():
            return False
        names = tuple(entry.name for entry in probe.iterdir())
        if part not in names:
            return path.exists()
        probe /= part
    return False


def read_utf8(
    path: Path,
    label: str,
    diagnostics: list[Diagnostic],
    *,
    code: str = "UNREADABLE_SOURCE",
) -> str | None:
    try:
        return path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        diagnostics.append(
            Diagnostic(code, f"cannot read {label}: {exc}", str(path))
        )
        return None


def relative_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


@dataclass(frozen=True)
class MarkdownContainer:
    kind: str
    width: int = 0


def parse_markdown_containers(
    line: str,
) -> tuple[str, tuple[MarkdownContainer, ...]]:
    expanded = line.expandtabs(4)
    cursor = 0
    containers: list[MarkdownContainer] = []
    while cursor < len(expanded):
        level_start = cursor
        indent = 0
        while cursor + indent < len(expanded) and expanded[cursor + indent] == " ":
            indent += 1
        if indent > 3:
            break
        probe = cursor + indent

        if probe < len(expanded) and expanded[probe] == ">":
            cursor = probe + 1
            if cursor < len(expanded) and expanded[cursor] == " ":
                cursor += 1
            containers.append(MarkdownContainer("quote"))
            continue

        marker = re.match(r"(?:[-+*]|\d{1,9}[.)])", expanded[probe:])
        if marker is None:
            cursor = level_start
            break
        marker_end = probe + len(marker.group(0))
        if marker_end == len(expanded):
            containers.append(
                MarkdownContainer("list", indent + len(marker.group(0)) + 1)
            )
            cursor = marker_end
            continue
        if expanded[marker_end] != " ":
            cursor = level_start
            break

        spacing_end = marker_end
        while spacing_end < len(expanded) and expanded[spacing_end] == " ":
            spacing_end += 1
        spacing = spacing_end - marker_end
        padding = spacing if spacing <= 4 else 1
        containers.append(
            MarkdownContainer(
                "list",
                indent + len(marker.group(0)) + padding,
            )
        )
        cursor = marker_end + padding if spacing > 4 else spacing_end

    return expanded[cursor:], tuple(containers)


def consume_markdown_containers(
    line: str,
    containers: tuple[MarkdownContainer, ...],
) -> str | None:
    expanded = line.expandtabs(4)
    cursor = 0
    for container in containers:
        if container.kind == "quote":
            indent = 0
            while cursor + indent < len(expanded) and expanded[cursor + indent] == " ":
                indent += 1
            if indent > 3:
                return None
            cursor += indent
            if cursor >= len(expanded) or expanded[cursor] != ">":
                return None
            cursor += 1
            if cursor < len(expanded) and expanded[cursor] == " ":
                cursor += 1
        else:
            required_end = cursor + container.width
            if expanded[cursor:required_end] != " " * container.width:
                return None
            cursor = required_end
    return expanded[cursor:]


def fenced_code_marker(line: str) -> tuple[str, int] | None:
    indent = len(line) - len(line.lstrip(" "))
    if indent > 3:
        return None
    match = re.match(r"(`{3,}|~{3,})(.*)$", line[indent:])
    if match is None:
        return None
    candidate = match.group(1)
    if candidate[0] == "`" and "`" in match.group(2):
        return None
    return candidate[0], len(candidate)


def strip_fenced_code(text: str) -> str:
    masked = list(text)
    in_fence = False
    marker = ""
    marker_length = 0
    fence_containers: tuple[MarkdownContainer, ...] = ()
    active_containers: tuple[MarkdownContainer, ...] = ()
    offset = 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        logical: str | None = None
        mask_line = False

        if in_fence:
            logical = (
                consume_markdown_containers(content, fence_containers)
                if fence_containers
                else content.expandtabs(4)
            )
            if logical is not None or not content.strip():
                logical = logical or ""
                indent = len(logical) - len(logical.lstrip(" "))
                close = re.fullmatch(
                    rf"{re.escape(marker)}{{{marker_length},}}[ ]*",
                    logical[indent:],
                )
                if close is not None and indent <= 3:
                    in_fence = False
                    marker = ""
                    marker_length = 0
                    fence_containers = ()
                mask_line = True
            else:
                in_fence = False
                marker = ""
                marker_length = 0
                fence_containers = ()

        if not in_fence and not mask_line:
            logical = (
                consume_markdown_containers(content, active_containers)
                if active_containers
                else None
            )
            if logical is not None:
                logical, extra = parse_markdown_containers(logical)
                line_containers = active_containers + extra
            else:
                logical, line_containers = parse_markdown_containers(content)
            if content.strip():
                active_containers = line_containers

            opener = fenced_code_marker(logical)
            if opener is not None:
                marker, marker_length = opener
                in_fence = True
                fence_containers = line_containers
                mask_line = True

        if mask_line:
            for position in range(offset, offset + len(content)):
                masked[position] = " "
        offset += len(line)
    return "".join(masked)


def mask_inline_code_and_comments(text: str) -> str:
    masked = list(text)
    index = 0
    while index < len(text):
        if text.startswith("<!--", index) and not is_escaped(text, index):
            closing_start = text.find("-->", index + 4)
            closing_end = len(text) if closing_start < 0 else closing_start + 3
            for position in range(index, closing_end):
                if masked[position] not in "\r\n":
                    masked[position] = " "
            index = closing_end
            continue
        if text[index] != "`" or is_escaped(text, index):
            index += 1
            continue
        opener_end = index
        while opener_end < len(text) and text[opener_end] == "`":
            opener_end += 1
        width = opener_end - index
        cursor = opener_end
        closing_start: int | None = None
        while cursor < len(text):
            if text[cursor] != "`":
                cursor += 1
                continue
            run_end = cursor
            while run_end < len(text) and text[run_end] == "`":
                run_end += 1
            if run_end - cursor == width:
                closing_start = cursor
                break
            cursor = run_end
        if closing_start is None:
            index = opener_end
            continue
        closing_end = closing_start + width
        for position in range(index, closing_end):
            if masked[position] not in "\r\n":
                masked[position] = " "
        index = closing_end
    return "".join(masked)


def leading_indentation(line: str) -> tuple[int, int]:
    characters = 0
    columns = 0
    while characters < len(line) and line[characters] in " \t":
        if line[characters] == "\t":
            columns += 4 - (columns % 4)
        else:
            columns += 1
        characters += 1
    return characters, columns


def strip_blockquote_prefixes(line: str) -> tuple[str, int]:
    expanded = line.expandtabs(4)
    cursor = 0
    depth = 0
    while cursor < len(expanded):
        indent = 0
        while cursor + indent < len(expanded) and expanded[cursor + indent] == " ":
            indent += 1
        if indent > 3:
            break
        marker = cursor + indent
        if marker >= len(expanded) or expanded[marker] != ">":
            break
        cursor = marker + 1
        if cursor < len(expanded) and expanded[cursor] == " ":
            cursor += 1
        depth += 1
    return expanded[cursor:], depth


def list_marker_details(
    line: str,
    parent_content_column: int | None = None,
) -> tuple[int, bool] | None:
    indent_end, indent_columns = leading_indentation(line)
    if parent_content_column is None:
        if indent_columns > 3:
            return None
    elif not (
        indent_columns <= 3
        or parent_content_column <= indent_columns <= parent_content_column + 3
    ):
        return None
    match = re.match(r"(?:[-+*]|\d{1,9}[.)])([ \t]+)", line[indent_end:])
    if match is None:
        return None
    marker_and_spacing = match.group(0)
    spacing = match.group(1)
    marker = marker_and_spacing[: -len(spacing)]
    marker_end_column = indent_columns + len(marker)
    columns = marker_end_column
    for character in spacing:
        if character == "\t":
            columns += 4 - (columns % 4)
        else:
            columns += 1
    spacing_columns = columns - marker_end_column
    if spacing_columns > 4:
        columns = marker_end_column + 1
    return columns, spacing_columns > 4


def mask_non_link_markdown(text: str) -> str:
    text = strip_fenced_code(text)
    masked = list(text)

    offset = 0
    active_list_content_column: int | None = None
    active_quote_depth = 0
    paragraph_open = False
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        logical, quote_depth = strip_blockquote_prefixes(content)
        if quote_depth != active_quote_depth:
            active_list_content_column = None
            paragraph_open = False
            active_quote_depth = quote_depth
        indent_end, indent_columns = leading_indentation(logical)
        nonblank = bool(logical[indent_end:])
        marker_details = list_marker_details(
            logical,
            active_list_content_column,
        )
        marker_content_column = marker_details[0] if marker_details is not None else None
        stripped = logical[indent_end:]
        starts_block = indent_columns <= 3 and bool(
            re.match(
                r"(?:#{1,6}(?:[ \t]+|$)|>|(?:[-*_][ \t]*){3,}$|<!--)",
                stripped,
            )
        )
        starts_setext_heading = (
            paragraph_open
            and indent_columns <= 3
            and bool(re.fullmatch(r"(?:=+|-+)[ \t]*", stripped))
        )
        if starts_block or starts_setext_heading:
            paragraph_open = False
        if marker_content_column is not None:
            active_list_content_column = marker_content_column
            is_indented_code = bool(marker_details[1])
            paragraph_open = False
        else:
            in_list = (
                active_list_content_column is not None
                and indent_columns >= active_list_content_column
            )
            if nonblank and active_list_content_column is not None and not in_list:
                active_list_content_column = None
            required_columns = (
                active_list_content_column + 4
                if in_list and active_list_content_column is not None
                else 4
            )
            is_indented_code = (
                nonblank
                and indent_columns >= required_columns
                and not paragraph_open
            )
            if not nonblank:
                paragraph_open = False
            elif is_indented_code:
                paragraph_open = False
            elif starts_block or starts_setext_heading:
                paragraph_open = False
            elif not paragraph_open:
                starts_reference_definition = bool(
                    re.match(r"\[[^\]]+\]:", stripped)
                )
                paragraph_open = not starts_reference_definition
        if is_indented_code:
            for position in range(offset, offset + len(content)):
                masked[position] = " "
        offset += len(line)

    return mask_inline_code_and_comments("".join(masked))


def markdown_h2_headings(text: str) -> list[str]:
    headings = []
    for line in mask_non_link_markdown(text).splitlines():
        match = H2_HEADING.fullmatch(line)
        if match is not None:
            heading = match.group(1).rstrip()
            heading = re.sub(r"[ \t]+#+[ \t]*$", "", heading).strip()
            headings.append(heading)
    return headings


def yaml_top_level_keys(text: str) -> set[str]:
    keys = set()
    for line in text.splitlines():
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = TOP_LEVEL_YAML_KEY.match(line)
        if match is not None:
            keys.add(match.group(1))
    return keys


def normalize_reference_label(value: str) -> str:
    return " ".join(unescape_html(unescape_markdown(value)).split()).casefold()


def unescape_markdown(value: str) -> str:
    result: list[str] = []
    index = 0
    while index < len(value):
        if (
            value[index] == "\\"
            and index + 1 < len(value)
            and value[index + 1] in string.punctuation
        ):
            index += 1
        result.append(value[index])
        index += 1
    return "".join(result)


def parse_optional_link_title(value: str) -> bool:
    if not value:
        return True
    if not value[0].isspace():
        return False
    value = value.strip()
    if not value:
        return True
    delimiters = {'"': '"', "'": "'", "(": ")"}
    closing = delimiters.get(value[0])
    if closing is None:
        return False
    escaped = False
    for index in range(1, len(value)):
        character = value[index]
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == closing:
            return not value[index + 1 :].strip()
    return False


def parse_link_destination(value: str) -> str | None:
    value = value.lstrip()
    if not value:
        return None
    if value.startswith("<"):
        escaped = False
        for index, character in enumerate(value[1:], start=1):
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == ">":
                if not parse_optional_link_title(value[index + 1 :]):
                    return None
                return unescape_markdown(value[1:index])
            elif character in "<>\r\n":
                return None
        return None

    destination: list[str] = []
    depth = 0
    escaped = False
    for character in value:
        if escaped:
            if character in string.punctuation:
                destination.append(character)
            else:
                destination.extend(("\\", character))
            escaped = False
            continue
        if character == "\\":
            escaped = True
            continue
        if character.isspace() and depth == 0:
            break
        if character == "(":
            depth += 1
        elif character == ")":
            if depth == 0:
                break
            depth -= 1
        destination.append(character)
    if escaped:
        destination.append("\\")
    if not destination or depth != 0:
        return None
    consumed = len(value)
    raw_destination = "".join(destination)
    destination_end = 0
    depth = 0
    escaped = False
    for destination_end, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character.isspace() and depth == 0:
            consumed = destination_end
            break
    if not parse_optional_link_title(value[consumed:]):
        return None
    return raw_destination


def find_closing_bracket(text: str, start: int) -> int | None:
    depth = 1
    escaped = False
    for index in range(start + 1, len(text)):
        character = text[index]
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
            if depth == 0:
                return index
    return None


def find_closing_parenthesis(text: str, start: int) -> int | None:
    depth = 1
    escaped = False
    angle_destination = False
    quote = ""
    content_started = False
    destination_finished = False
    for index in range(start + 1, len(text)):
        character = text[index]
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
            continue
        if not content_started and character.isspace():
            continue
        if not content_started:
            content_started = True
            angle_destination = character == "<"
        if angle_destination:
            if character == ">":
                angle_destination = False
                destination_finished = True
            continue
        if quote:
            if character == quote:
                quote = ""
            continue
        if character.isspace() and depth == 1:
            destination_finished = True
            continue
        if destination_finished and character in {'"', "'"} and depth == 1:
            quote = character
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return index
    return None


def is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def reference_definitions(
    text: str,
    diagnostics: list[Diagnostic] | None = None,
    source: str = "",
) -> tuple[dict[str, str], list[tuple[int, int]]]:
    definitions: dict[str, str] = {}
    spans: list[tuple[int, int]] = []
    lines = text.splitlines(keepends=True)
    offsets: list[int] = []
    offset = 0
    for line in lines:
        offsets.append(offset)
        offset += len(line)
    for line_index, line in enumerate(lines):
        content = line.rstrip("\r\n")
        logical, containers = parse_markdown_containers(content)
        indent = len(logical) - len(logical.lstrip(" "))
        if indent <= 3 and indent < len(logical) and logical[indent] == "[":
            label_end = find_closing_bracket(logical, indent)
            if label_end is not None and logical[label_end + 1 :].startswith(":"):
                raw_destination = logical[label_end + 2 :]
                spans.append((offsets[line_index], offsets[line_index] + len(content)))
                if not raw_destination.strip() and line_index + 1 < len(lines):
                    continuation = lines[line_index + 1].rstrip("\r\n")
                    logical_continuation = consume_markdown_containers(
                        continuation,
                        containers,
                    )
                    if logical_continuation is not None:
                        continuation_indent = len(logical_continuation) - len(
                            logical_continuation.lstrip(" ")
                        )
                    else:
                        continuation_indent = 0
                    if 1 <= continuation_indent <= 3:
                        raw_destination = logical_continuation[continuation_indent:]
                        spans.append(
                            (
                                offsets[line_index + 1],
                                offsets[line_index + 1] + len(continuation),
                            )
                        )
                destination = parse_link_destination(raw_destination)
                if destination is not None:
                    definitions.setdefault(
                        normalize_reference_label(
                            logical[indent + 1 : label_end]
                        ),
                        destination,
                    )
                elif diagnostics is not None and looks_like_malformed_local_markdown_link(
                    raw_destination
                ):
                    diagnostics.append(
                        Diagnostic(
                            "MARKDOWN_LINK_INVALID",
                            "invalid local Markdown link",
                            source,
                            raw_destination.strip(),
                        )
                    )
    return definitions, spans


def mask_images(text: str, definitions: dict[str, str]) -> str:
    masked = list(text)
    index = 0
    while index + 1 < len(text):
        if text[index] != "!" or text[index + 1] != "[" or is_escaped(text, index):
            index += 1
            continue
        label_start = index + 1
        label_end = find_closing_bracket(text, label_start)
        if label_end is None:
            index += 2
            continue
        label = text[label_start + 1 : label_end]
        cursor = label_end + 1
        image_end: int | None = None
        if cursor < len(text) and text[cursor] == "(":
            closing = find_closing_parenthesis(text, cursor)
            if closing is not None and parse_link_destination(text[cursor + 1 : closing]) is not None:
                image_end = closing + 1
        elif cursor < len(text) and text[cursor] == "[":
            reference_end = find_closing_bracket(text, cursor)
            if reference_end is not None:
                reference = text[cursor + 1 : reference_end] or label
                if normalize_reference_label(reference) in definitions:
                    image_end = reference_end + 1
        elif normalize_reference_label(label) in definitions:
            image_end = label_end + 1
        if image_end is None:
            index += 2
            continue
        for position in range(index, image_end):
            if masked[position] not in "\r\n":
                masked[position] = " "
        index = image_end
    return "".join(masked)


def local_markdown_target(
    value: str,
    diagnostics: list[Diagnostic] | None = None,
    source: str = "",
) -> str | None:
    value = unescape_html(value.strip())
    if not value or value.startswith("#"):
        return None
    if re.match(r"^[A-Za-z]:", value):
        return unquote(value)
    try:
        parsed = urlsplit(value)
    except ValueError:
        if diagnostics is not None:
            diagnostics.append(
                Diagnostic(
                    "MARKDOWN_LINK_INVALID",
                    "invalid local Markdown link",
                    source,
                    value,
                )
            )
        return None
    scheme = parsed.scheme.casefold()
    if scheme and scheme != "file":
        return None
    raw_path_and_authority = f"{parsed.netloc}{parsed.path}"
    if PERCENT_ENCODED_PATH_SEPARATOR.search(raw_path_and_authority):
        if diagnostics is not None:
            diagnostics.append(
                Diagnostic(
                    "REFERENCE_PATH_ESCAPE",
                    "reference path contains a percent-encoded separator",
                    source,
                    value,
                )
            )
        return None
    parsed_from_decoded_value = False
    if not scheme:
        decoded_value = unquote(value)
        try:
            decoded_parsed = urlsplit(decoded_value)
        except ValueError:
            if diagnostics is not None:
                diagnostics.append(
                    Diagnostic(
                        "MARKDOWN_LINK_INVALID",
                        "invalid local Markdown link",
                        source,
                        value,
                    )
                )
            return None
        if decoded_parsed.scheme.casefold() == "file":
            parsed = decoded_parsed
            scheme = "file"
            parsed_from_decoded_value = True
    target = parsed.path if parsed_from_decoded_value else unquote(parsed.path)
    if parsed.netloc:
        authority = parsed.netloc if parsed_from_decoded_value else unquote(parsed.netloc)
        target = f"//{authority}{target}"
    elif scheme == "file" and not target.startswith("/"):
        target = f"/{target}"
    lowered_target = target.casefold()
    if lowered_target.endswith(".md") or re.search(r"\.md/+$", lowered_target):
        return target
    return None


def looks_like_malformed_local_markdown_link(value: str) -> bool:
    entity_decoded = unescape_html(value).strip().casefold()
    lowered = unquote(entity_decoded)
    scheme_match = re.match(r"^<?([a-z][a-z0-9+.-]*):", entity_decoded)
    has_external_scheme = (
        scheme_match is not None
        and len(scheme_match.group(1)) > 1
        and scheme_match.group(1) != "file"
    )
    return (
        ".md" in lowered
        and not has_external_scheme
        and not lowered.lstrip().startswith("#")
    )


def local_markdown_targets(
    text: str,
    diagnostics: list[Diagnostic] | None = None,
    source: str = "",
) -> list[str]:
    text = mask_non_link_markdown(text)
    definitions, definition_spans = reference_definitions(text, diagnostics, source)

    body = list(text)
    for start, end in definition_spans:
        body[start:end] = " " * (end - start)
    body_text = mask_images("".join(body), definitions)
    targets: list[str] = []
    invalid: list[str] = []
    index = 0
    while index < len(body_text):
        if body_text[index] != "[" or is_escaped(body_text, index):
            index += 1
            continue
        if (
            index > 0
            and body_text[index - 1] == "!"
            and not is_escaped(body_text, index - 1)
        ):
            index += 1
            continue
        label_end = find_closing_bracket(body_text, index)
        if label_end is None:
            index += 1
            continue
        label = body_text[index + 1 : label_end]
        cursor = label_end + 1
        destination: str | None = None
        if cursor < len(body_text) and body_text[cursor] == "(":
            link_end = find_closing_parenthesis(body_text, cursor)
            if link_end is None:
                fragment = body_text[cursor + 1 :].splitlines()[0]
                if looks_like_malformed_local_markdown_link(fragment):
                    invalid.append(fragment.strip())
                index = cursor + 1
                continue
            destination = parse_link_destination(body_text[cursor + 1 : link_end])
            if destination is None and looks_like_malformed_local_markdown_link(
                body_text[cursor + 1 : link_end]
            ):
                invalid.append(body_text[cursor + 1 : link_end].strip())
            index = link_end + 1
        elif cursor < len(body_text) and body_text[cursor] == "[":
            reference_end = find_closing_bracket(body_text, cursor)
            if reference_end is None:
                index = cursor + 1
                continue
            reference = body_text[cursor + 1 : reference_end] or label
            destination = definitions.get(normalize_reference_label(reference))
            index = reference_end + 1
        else:
            destination = definitions.get(normalize_reference_label(label))
            index = label_end + 1
        if destination is not None:
            target = local_markdown_target(destination, diagnostics, source)
            if target is not None:
                targets.append(target)

    if diagnostics is not None:
        for fragment in invalid:
            diagnostics.append(
                Diagnostic(
                    "MARKDOWN_LINK_INVALID",
                    "invalid local Markdown link",
                    source,
                    fragment,
                )
            )
    return targets


def has_link_component(source: Path, target: str) -> bool:
    probe = lexical_absolute(source.parent)
    if is_link(probe):
        return True
    for part in PurePosixPath(target).parts:
        if part == "..":
            probe = probe.parent
        elif part != ".":
            probe = probe / part
        if is_link(probe):
            return True
    return False


def resolve_reference(
    source: Path,
    target: str,
    source_package: Path,
    diagnostics: list[Diagnostic],
) -> Path | None:
    source_package = lexical_absolute(source_package)
    source_name = relative_path(source, source_package)
    if has_path_control_character(target):
        diagnostics.append(
            Diagnostic(
                "REFERENCE_PATH_INVALID",
                "reference path contains a control character",
                source_name,
                target,
            )
        )
        return None
    raw_path = PurePosixPath(target)
    if not is_portable_relative_path(target) or raw_path.is_absolute():
        diagnostics.append(
            Diagnostic(
                "REFERENCE_PATH_ESCAPE",
                "reference path escapes package",
                source_name,
                target,
            )
        )
        return None

    candidate_path = lexical_absolute(source.parent / Path(*raw_path.parts))
    if not is_inside(candidate_path, source_package):
        diagnostics.append(
            Diagnostic("REFERENCE_PATH_ESCAPE", "reference path escapes package", source_name, target)
        )
        return None

    if (
        first_link_component(lexical_absolute(source), source_package) is not None
        or has_link_component(source, target)
        or first_link_component(candidate_path, source_package) is not None
    ):
        diagnostics.append(
            Diagnostic(
                "REFERENCE_SYMLINK_ESCAPE",
                "reference path traverses a link or junction",
                source_name,
                target,
            )
        )
        return None

    try:
        case_mismatch = first_case_mismatch(candidate_path, source_package)
    except OSError:
        diagnostics.append(
            Diagnostic(
                "REFERENCE_CASE_UNVERIFIABLE",
                "reference path casing could not be verified",
                source_name,
                target,
            )
        )
        return None
    if case_mismatch is not None:
        diagnostics.append(
            Diagnostic(
                "REFERENCE_CASE_MISMATCH",
                "reference path casing differs from package entry",
                source_name,
                target,
            )
        )
        return None
    try:
        unlisted_alias = resolves_through_unlisted_entry(
            candidate_path,
            source_package,
        )
    except OSError:
        diagnostics.append(
            Diagnostic(
                "REFERENCE_CASE_UNVERIFIABLE",
                "reference path casing could not be verified",
                source_name,
                target,
            )
        )
        return None
    if unlisted_alias:
        diagnostics.append(
            Diagnostic(
                "REFERENCE_PATH_ESCAPE",
                "reference path is not an exact package entry",
                source_name,
                target,
            )
        )
        return None

    source_root = source_package.resolve()
    candidate = candidate_path.resolve()
    if not is_inside(candidate, source_root):
        diagnostics.append(
            Diagnostic("REFERENCE_PATH_ESCAPE", "reference path escapes package", source_name, target)
        )
        return None
    if not candidate.is_file():
        diagnostics.append(
            Diagnostic(
                "MISSING_REFERENCE_TARGET",
                "missing reference target",
                source_name,
                target,
            )
        )
        return None
    if is_link(candidate):
        diagnostics.append(
            Diagnostic(
                "REFERENCE_SYMLINK_ESCAPE",
                "reference target must be a regular package file",
                source_name,
                target,
            )
        )
        return None
    return candidate


def validate_package_file(
    package_root: Path,
    relative: str,
    diagnostics: list[Diagnostic],
    *,
    missing_code: str,
    missing_detail: str,
    source: str = "",
) -> Path | None:
    package_root = lexical_absolute(package_root)
    if not is_portable_relative_path(relative):
        diagnostics.append(
            Diagnostic(
                "PACKAGE_PATH_ESCAPE",
                "package target escapes package root",
                source,
                relative,
            )
        )
        return None
    pure = PurePosixPath(relative)
    candidate_path = lexical_absolute(package_root / Path(*pure.parts))
    if not is_inside(candidate_path, package_root):
        diagnostics.append(
            Diagnostic(
                "PACKAGE_PATH_ESCAPE",
                "package target escapes package root",
                source,
                relative,
            )
        )
        return None
    if first_link_component(candidate_path, package_root) is not None:
        diagnostics.append(
            Diagnostic(
                "PACKAGE_PATH_LINK",
                "package path traverses a link or junction",
                source,
                relative,
            )
        )
        return None
    try:
        case_mismatch = first_case_mismatch(candidate_path, package_root)
    except OSError:
        diagnostics.append(
            Diagnostic(
                "PACKAGE_PATH_CASE_UNVERIFIABLE",
                "package target path casing could not be verified",
                source,
                relative,
            )
        )
        return None
    if case_mismatch is not None:
        diagnostics.append(
            Diagnostic(
                "PACKAGE_PATH_CASE_MISMATCH",
                "package target path casing differs from source",
                source,
                relative,
            )
        )
        return None
    try:
        unlisted_alias = resolves_through_unlisted_entry(
            candidate_path,
            package_root,
        )
    except OSError:
        diagnostics.append(
            Diagnostic(
                "PACKAGE_PATH_CASE_UNVERIFIABLE",
                "package target path casing could not be verified",
                source,
                relative,
            )
        )
        return None
    if unlisted_alias:
        diagnostics.append(
            Diagnostic(
                "PACKAGE_PATH_ESCAPE",
                "package target is not an exact package entry",
                source,
                relative,
            )
        )
        return None
    candidate = candidate_path.resolve()
    if not is_inside(candidate, package_root.resolve()):
        diagnostics.append(
            Diagnostic(
                "PACKAGE_PATH_ESCAPE",
                "package target resolves outside package root",
                source,
                relative,
            )
        )
        return None
    if not candidate.is_file():
        diagnostics.append(Diagnostic(missing_code, missing_detail, source, relative))
        return None
    if (
        read_utf8(
            candidate,
            "package target is not readable UTF-8",
            diagnostics,
            code="PACKAGE_TARGET_UNREADABLE",
        )
        is None
    ):
        return None
    return candidate


def validate_package_copy(
    source_package: Path,
    package_root: Path,
    relative: str,
    diagnostics: list[Diagnostic],
    *,
    missing_code: str,
    missing_detail: str,
) -> None:
    package_file = validate_package_file(
        package_root,
        relative,
        diagnostics,
        missing_code=missing_code,
        missing_detail=missing_detail,
        source=relative,
    )
    if package_file is None:
        return
    source_file = lexical_absolute(source_package / Path(*PurePosixPath(relative).parts))
    try:
        source_bytes = source_file.read_bytes()
        package_bytes = package_file.read_bytes()
    except OSError as exc:
        diagnostics.append(
            Diagnostic(
                "PACKAGE_CONTENT_UNREADABLE",
                f"cannot compare package runtime content: {exc}",
                relative,
            )
        )
        return
    if source_bytes != package_bytes:
        diagnostics.append(
            Diagnostic(
                "PACKAGE_CONTENT_MISMATCH",
                "package runtime content differs from source",
                relative,
                relative,
            )
        )


def detect_cycles(graph: dict[str, set[str]]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    visited: set[str] = set()
    active: list[str] = []
    active_set: set[str] = set()
    seen_cycles: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        visited.add(node)
        active.append(node)
        active_set.add(node)
        for target in sorted(graph.get(node, set())):
            if target in active_set:
                index = active.index(target)
                cycle = tuple(active[index:] + [target])
                canonical = min(
                    tuple(cycle[index:] + cycle[:index])
                    for index in range(len(cycle) - 1)
                )
                if canonical not in seen_cycles:
                    seen_cycles.add(canonical)
                    diagnostics.append(
                        Diagnostic(
                            "REFERENCE_CYCLE",
                            "reference cycle detected",
                            " -> ".join(cycle),
                        )
                    )
            elif target not in visited:
                visit(target)
        active.pop()
        active_set.remove(node)

    for node in sorted(graph):
        if node not in visited:
            visit(node)
    return diagnostics


def discover_public_skills(source_package: Path, diagnostics: list[Diagnostic]) -> tuple[str, ...]:
    skills_root = source_package / "skills"
    if not skills_root.is_dir() or is_link(skills_root):
        diagnostics.append(
            Diagnostic("SKILL_ROOT_MISSING", "skills directory is missing", "skills")
        )
        return ()
    try:
        skill_paths = sorted(skills_root.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        diagnostics.append(
            Diagnostic(
                "SKILL_ROOT_UNREADABLE",
                f"cannot enumerate skills directory: {exc}",
                "skills",
            )
        )
        return ()
    skill_ids = []
    for path in skill_paths:
        if is_link(path):
            diagnostics.append(
                Diagnostic("SKILL_LINK", "public skill must not be a link", path.name)
            )
            continue
        if path.is_dir() and (path / "SKILL.md").is_file():
            skill_ids.append(path.name)
    if not skill_ids:
        diagnostics.append(Diagnostic("PUBLIC_SKILL_MISSING", "no public SKILL.md found"))
    return tuple(skill_ids)


def validate_reference_graph(
    source_package: Path,
    package_root: Path,
) -> tuple[ReferenceGraph | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    source_package = lexical_absolute(source_package)
    package_root = lexical_absolute(package_root)
    if is_link(source_package):
        diagnostics.append(
            Diagnostic("SOURCE_ROOT_LINK", "source package root must not be a link or junction")
        )
        return None, diagnostics
    if not source_package.is_dir():
        diagnostics.append(
            Diagnostic("SOURCE_PACKAGE_MISSING", "source package root is missing")
        )
        return None, diagnostics
    if is_link(package_root):
        diagnostics.append(
            Diagnostic("PACKAGE_ROOT_LINK", "package root must not be a link or junction")
        )
        return None, diagnostics
    if not package_root.is_dir():
        diagnostics.append(
            Diagnostic("PACKAGE_ROOT_MISSING", "package root is missing")
        )
        return None, diagnostics

    public_skills = discover_public_skills(source_package, diagnostics)
    queue = [f"skills/{skill_id}/SKILL.md" for skill_id in public_skills]
    entrypoints = set(queue)
    visited: set[str] = set()
    graph: dict[str, set[str]] = {}
    reference_targets: set[str] = set()

    while queue:
        source_name = queue.pop(0)
        if source_name in visited:
            continue
        visited.add(source_name)
        source = lexical_absolute(
            source_package / Path(*PurePosixPath(source_name).parts)
        )
        if first_link_component(source, source_package) is not None:
            diagnostics.append(
                Diagnostic(
                    "REFERENCE_SYMLINK_ESCAPE",
                    "runtime Markdown path traverses a link or junction",
                    source_name,
                )
            )
            continue
        if not is_inside(source.resolve(), source_package.resolve()):
            diagnostics.append(
                Diagnostic(
                    "REFERENCE_PATH_ESCAPE",
                    "runtime Markdown resolves outside source package",
                    source_name,
                )
            )
            continue
        if not source.is_file():
            diagnostics.append(
                Diagnostic("PUBLIC_SKILL_MISSING", "public SKILL.md is missing", source_name)
            )
            continue
        text = read_utf8(source, "runtime markdown", diagnostics)
        if text is None:
            continue
        graph.setdefault(source_name, set())
        for target_text in local_markdown_targets(text, diagnostics, source_name):
            target = resolve_reference(source, target_text, source_package, diagnostics)
            if target is None:
                continue
            target_name = relative_path(target, source_package)
            if source_name in entrypoints and "references" not in PurePosixPath(target_name).parts:
                diagnostics.append(
                    Diagnostic(
                        "REFERENCE_TARGET_INVALID",
                        "public SKILL.md must link to a package references file",
                        source_name,
                        target_name,
                    )
                )
            if source_name not in entrypoints:
                diagnostics.append(
                    Diagnostic(
                        "REFERENCE_SECOND_HOP",
                        "reference requires a second-hop reference",
                        source_name,
                        target_name,
                    )
                )
            graph[source_name].add(target_name)
            reference_targets.add(target_name)
            if target_name not in visited:
                queue.append(target_name)

    diagnostics.extend(detect_cycles(graph))

    for source_name in entrypoints:
        validate_package_copy(
            source_package,
            package_root,
            source_name,
            diagnostics,
            missing_code="PACKAGE_SKILL_MISSING",
            missing_detail="package omission of public SKILL.md",
        )
    for target_name in sorted(reference_targets):
        validate_package_copy(
            source_package,
            package_root,
            target_name,
            diagnostics,
            missing_code="PACKAGE_REFERENCE_MISSING",
            missing_detail="package omission of reference target",
        )

    if diagnostics:
        return None, diagnostics
    return (
        ReferenceGraph(
            public_skills=public_skills,
            reference_targets=tuple(sorted(reference_targets)),
            graph={key: tuple(sorted(value)) for key, value in sorted(graph.items())},
        ),
        diagnostics,
    )


def parse_yaml_scalar(
    value: str,
    *,
    field: str,
    path: Path,
    diagnostics: list[Diagnostic],
) -> str | None:
    value = value.strip()
    invalid = False
    parsed: str | None = None
    if not value:
        invalid = True
    elif value.startswith('"'):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            invalid = True
        else:
            if isinstance(decoded, str):
                parsed = decoded
            else:
                invalid = True
    elif value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            invalid = True
        else:
            inner = value[1:-1]
            if "'" in inner.replace("''", ""):
                invalid = True
            else:
                parsed = inner.replace("''", "'")
    elif value[0] in "[]{}&*!|>@`" or value.startswith(("- ", "? ", ": ", "#")):
        invalid = True
    elif re.search(r"[ \t]#", value):
        invalid = True
    else:
        parsed = value

    if invalid or parsed is None or not parsed.strip():
        diagnostics.append(
            Diagnostic(
                "YAML_SCALAR_INVALID",
                f"invalid YAML scalar for {field}",
                str(path),
                value,
            )
        )
        return None
    return parsed


def parse_rule_mapping(
    path: Path,
    diagnostics: list[Diagnostic],
) -> RuleMappingDocument:
    text = read_utf8(path, "rule mapping", diagnostics)
    if text is None:
        return RuleMappingDocument(None, {})
    rules: dict[str, list[dict[str, str]]] = {}
    in_rules = False
    seen_core_version = False
    core_version: str | None = None
    current_rule: str | None = None
    current_entry: dict[str, str] | None = None

    def finish_entry() -> None:
        nonlocal current_entry
        if current_entry is not None:
            if set(current_entry) != {"file", "section", "implementation"} or any(
                not value.strip() for value in current_entry.values()
            ):
                diagnostics.append(
                    Diagnostic(
                        "MAPPING_ENTRY_INVALID",
                        "rule mapping entry must contain non-empty file, section, and implementation",
                        str(path),
                    )
                )
            elif current_rule is not None:
                rules.setdefault(current_rule, []).append(current_entry)
        current_entry = None

    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line == "rules:":
            if in_rules:
                diagnostics.append(
                    Diagnostic(
                        "MAPPING_RULES_DUPLICATE",
                        "duplicate rules key",
                        str(path),
                    )
                )
            else:
                in_rules = True
                current_rule = None
            continue
        if not in_rules:
            core_version_match = re.fullmatch(r"core_version:[ \t]*(.*?)\s*", line)
            if core_version_match is not None:
                if seen_core_version:
                    diagnostics.append(
                        Diagnostic(
                            "MAPPING_CORE_VERSION_DUPLICATE",
                            "duplicate core_version key",
                            str(path),
                        )
                    )
                seen_core_version = True
                parsed_version = parse_yaml_scalar(
                    core_version_match.group(1),
                    field="core_version",
                    path=path,
                    diagnostics=diagnostics,
                )
                if parsed_version is not None:
                    core_version = parsed_version
                continue
            diagnostics.append(
                Diagnostic(
                    "MAPPING_SYNTAX_INVALID",
                    "unsupported rule-mapping syntax",
                    str(path),
                    line,
                )
            )
            continue
        if not line[0].isspace():
            finish_entry()
            diagnostics.append(
                Diagnostic(
                    "MAPPING_SYNTAX_INVALID",
                    "unsupported rule-mapping syntax",
                    str(path),
                    line,
                )
            )
            break
        rule_match = RULE_ID.fullmatch(line)
        if rule_match is not None:
            finish_entry()
            current_rule = rule_match.group(1)
            if current_rule in rules:
                diagnostics.append(
                    Diagnostic("MAPPING_RULE_DUPLICATE", "duplicate rule mapping", current_rule)
                )
            rules.setdefault(current_rule, [])
            continue
        entry_match = MAPPING_START.fullmatch(line)
        if entry_match is not None:
            finish_entry()
            if current_rule is None:
                diagnostics.append(
                    Diagnostic("MAPPING_ENTRY_INVALID", "mapping entry has no rule", str(path))
                )
                continue
            key = entry_match.group(1)
            value = parse_yaml_scalar(
                entry_match.group(2),
                field=key,
                path=path,
                diagnostics=diagnostics,
            )
            current_entry = {key: value or ""}
            continue
        field_match = MAPPING_FIELD.fullmatch(line)
        if field_match is not None and current_entry is not None:
            key = field_match.group(1)
            if key in current_entry:
                diagnostics.append(
                    Diagnostic("MAPPING_ENTRY_INVALID", "duplicate mapping field", str(path), key)
                )
            value = parse_yaml_scalar(
                field_match.group(2),
                field=key,
                path=path,
                diagnostics=diagnostics,
            )
            current_entry[key] = value or ""
            continue
        diagnostics.append(
            Diagnostic("MAPPING_SYNTAX_INVALID", "unsupported rule-mapping syntax", str(path), line)
        )
    finish_entry()
    if not in_rules:
        diagnostics.append(Diagnostic("MAPPING_RULES_MISSING", "rule mapping has no rules key", str(path)))
    if not rules:
        diagnostics.append(Diagnostic("MAPPING_RULES_EMPTY", "rule mapping has no entries", str(path)))
    return RuleMappingDocument(core_version, rules)


def parse_core_catalog(
    path: Path,
    diagnostics: list[Diagnostic],
) -> CoreCatalog:
    text = read_utf8(path, "core catalog", diagnostics, code="CORE_CATALOG_UNREADABLE")
    if text is None:
        return CoreCatalog(None, (), ())

    core_version: str | None = None
    seen_core_version = False
    seen_rules = False
    in_rules = False
    current_rule: str | None = None
    current_mandatory: bool | None = None
    rule_ids: list[str] = []
    mandatory_rule_ids: list[str] = []

    def finish_rule() -> None:
        nonlocal current_rule, current_mandatory
        if current_rule is not None:
            if current_mandatory is None:
                diagnostics.append(
                    Diagnostic(
                        "CORE_RULE_INVALID",
                        "core catalog rule is missing a boolean mandatory field",
                        current_rule,
                    )
                )
            rule_ids.append(current_rule)
            if current_mandatory is True:
                mandatory_rule_ids.append(current_rule)
        current_rule = None
        current_mandatory = None

    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        version_match = re.fullmatch(r"core_version:[ \t]*(.*?)\s*", line)
        if version_match is not None:
            if seen_core_version:
                diagnostics.append(
                    Diagnostic(
                        "CORE_VERSION_DUPLICATE",
                        "duplicate core catalog core_version key",
                        str(path),
                    )
                )
            seen_core_version = True
            parsed = parse_yaml_scalar(
                version_match.group(1),
                field="core catalog core_version",
                path=path,
                diagnostics=diagnostics,
            )
            if parsed is not None:
                core_version = parsed
            continue
        if line.startswith("rules:"):
            finish_rule()
            if line != "rules:":
                diagnostics.append(
                    Diagnostic(
                        "CORE_RULES_INVALID",
                        "core catalog rules must be a block list",
                        str(path),
                        line,
                    )
                )
                in_rules = False
            elif seen_rules:
                diagnostics.append(
                    Diagnostic(
                        "CORE_RULES_DUPLICATE",
                        "duplicate core catalog rules key",
                        str(path),
                    )
                )
                in_rules = True
            else:
                seen_rules = True
                in_rules = True
            continue
        if not in_rules:
            continue
        if not line[0].isspace():
            finish_rule()
            in_rules = False
            continue
        rule_match = CORE_RULE_START.fullmatch(line)
        if rule_match is not None:
            finish_rule()
            parsed = parse_yaml_scalar(
                rule_match.group(1),
                field="core rule id",
                path=path,
                diagnostics=diagnostics,
            )
            if parsed is not None and re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", parsed):
                current_rule = parsed
            elif parsed is not None:
                diagnostics.append(
                    Diagnostic("CORE_RULE_INVALID", "invalid core rule id", str(path), parsed)
                )
            continue
        mandatory_match = CORE_RULE_MANDATORY.fullmatch(line)
        if mandatory_match is not None:
            parsed = parse_yaml_scalar(
                mandatory_match.group(1),
                field="core rule mandatory",
                path=path,
                diagnostics=diagnostics,
            )
            if current_rule is None:
                diagnostics.append(
                    Diagnostic(
                        "CORE_RULE_INVALID",
                        "mandatory field has no core rule",
                        str(path),
                    )
                )
            elif parsed not in {"true", "false"}:
                diagnostics.append(
                    Diagnostic(
                        "CORE_RULE_INVALID",
                        "core rule mandatory must be true or false",
                        current_rule,
                    )
                )
            else:
                current_mandatory = parsed == "true"
            continue
        if line.startswith("  -"):
            diagnostics.append(
                Diagnostic(
                    "CORE_RULE_INVALID",
                    "core catalog rule entry must start with id",
                    str(path),
                    line,
                )
            )

    finish_rule()
    if not seen_core_version:
        diagnostics.append(
            Diagnostic("CORE_VERSION_MISSING", "core catalog core_version is missing", str(path))
        )
    if not seen_rules:
        diagnostics.append(
            Diagnostic("CORE_RULES_MISSING", "core catalog rules are missing", str(path))
        )
    if not rule_ids:
        diagnostics.append(
            Diagnostic("CORE_RULES_EMPTY", "core catalog has no rule IDs", str(path))
        )
    duplicates = sorted({rule_id for rule_id in rule_ids if rule_ids.count(rule_id) > 1})
    if duplicates:
        diagnostics.append(
            Diagnostic(
                "CORE_RULE_DUPLICATE",
                f"duplicate core rule IDs: {', '.join(duplicates)}",
                str(path),
            )
        )
    return CoreCatalog(
        core_version,
        tuple(rule_ids),
        tuple(mandatory_rule_ids),
    )


def parse_conformance_manifest(
    path: Path,
    diagnostics: list[Diagnostic],
) -> ConformanceManifest:
    text = read_utf8(
        path,
        "conformance manifest",
        diagnostics,
        code="CONFORMANCE_UNREADABLE",
    )
    if text is None:
        return ConformanceManifest(None, ())

    core_version: str | None = None
    seen_core_version = False
    seen_implemented = False
    in_implemented = False
    implemented: list[str] = []

    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        version_match = re.fullmatch(r"core_version:[ \t]*(.*?)\s*", line)
        if version_match is not None:
            if seen_core_version:
                diagnostics.append(
                    Diagnostic(
                        "CONFORMANCE_VERSION_DUPLICATE",
                        "duplicate conformance core_version key",
                        str(path),
                    )
                )
            seen_core_version = True
            parsed = parse_yaml_scalar(
                version_match.group(1),
                field="conformance core_version",
                path=path,
                diagnostics=diagnostics,
            )
            if parsed is not None:
                core_version = parsed
            continue
        implemented_match = re.fullmatch(r"implemented_rules:[ \t]*(.*?)\s*", line)
        if implemented_match is not None:
            if seen_implemented:
                diagnostics.append(
                    Diagnostic(
                        "CONFORMANCE_RULES_DUPLICATE",
                        "duplicate implemented_rules key",
                        str(path),
                    )
                )
            seen_implemented = True
            in_implemented = True
            if implemented_match.group(1):
                diagnostics.append(
                    Diagnostic(
                        "CONFORMANCE_RULES_INVALID",
                        "implemented_rules must be a block list",
                        str(path),
                        line,
                    )
                )
                in_implemented = False
            continue
        if not in_implemented:
            continue
        if not line[0].isspace():
            in_implemented = False
            continue
        item_match = YAML_LIST_ITEM.fullmatch(line)
        if item_match is None:
            diagnostics.append(
                Diagnostic(
                    "CONFORMANCE_RULES_INVALID",
                    "invalid implemented_rules list item",
                    str(path),
                    line,
                )
            )
            continue
        parsed = parse_yaml_scalar(
            item_match.group(1),
            field="implemented rule id",
            path=path,
            diagnostics=diagnostics,
        )
        if parsed is not None:
            implemented.append(parsed)

    if not seen_core_version:
        diagnostics.append(
            Diagnostic(
                "CONFORMANCE_VERSION_MISSING",
                "conformance core_version is missing",
                str(path),
            )
        )
    if not seen_implemented:
        diagnostics.append(
            Diagnostic(
                "CONFORMANCE_RULES_MISSING",
                "conformance implemented_rules is missing",
                str(path),
            )
        )
    if not implemented:
        diagnostics.append(
            Diagnostic(
                "CONFORMANCE_RULES_EMPTY",
                "conformance implemented_rules is empty",
                str(path),
            )
        )
    duplicates = sorted({rule_id for rule_id in implemented if implemented.count(rule_id) > 1})
    if duplicates:
        diagnostics.append(
            Diagnostic(
                "CONFORMANCE_RULE_DUPLICATE",
                f"duplicate conformance rule IDs: {', '.join(duplicates)}",
                str(path),
            )
        )
    return ConformanceManifest(core_version, tuple(implemented))


def validate_rule_inventory(
    mapping: RuleMappingDocument,
    catalog: CoreCatalog,
    conformance: ConformanceManifest,
    diagnostics: list[Diagnostic],
) -> None:
    if mapping.core_version is None:
        diagnostics.append(
            Diagnostic("MAPPING_CORE_VERSION_MISSING", "rule mapping core_version is missing")
        )
    elif catalog.core_version is not None and mapping.core_version != catalog.core_version:
        diagnostics.append(
            Diagnostic(
                "MAPPING_CORE_VERSION_MISMATCH",
                "rule mapping core_version does not match core catalog",
                mapping.core_version,
                catalog.core_version,
            )
        )
    if conformance.core_version is not None and catalog.core_version is not None:
        if conformance.core_version != catalog.core_version:
            diagnostics.append(
                Diagnostic(
                    "CONFORMANCE_CORE_VERSION_MISMATCH",
                    "conformance core_version does not match core catalog",
                    conformance.core_version,
                    catalog.core_version,
                )
            )

    mandatory = set(catalog.mandatory_rule_ids)
    known = set(catalog.rule_ids)
    mapped = set(mapping.rules)
    implemented = set(conformance.implemented_rule_ids)
    missing_mapping = sorted(mandatory - mapped)
    extra_mapping = sorted(mapped - mandatory)
    missing_conformance = sorted(mandatory - implemented)
    unknown_conformance = sorted(implemented - known)
    if missing_mapping:
        diagnostics.append(
            Diagnostic(
                "MAPPING_RULE_MISSING",
                f"missing mandatory rule mapping: {', '.join(missing_mapping)}",
            )
        )
    if extra_mapping:
        diagnostics.append(
            Diagnostic(
                "MAPPING_RULE_UNKNOWN",
                f"unknown rule mapping: {', '.join(extra_mapping)}",
            )
        )
    if missing_conformance:
        diagnostics.append(
            Diagnostic(
                "CONFORMANCE_RULE_MISSING",
                f"missing mandatory conformance rule: {', '.join(missing_conformance)}",
            )
        )
    if unknown_conformance:
        diagnostics.append(
            Diagnostic(
                "CONFORMANCE_RULE_UNKNOWN",
                f"unknown conformance rule: {', '.join(unknown_conformance)}",
            )
        )


def is_portable_relative_path(value: str) -> bool:
    windows = PureWindowsPath(value)
    posix = PurePosixPath(value)
    if (
        not value
        or has_path_control_character(value)
        or "\\" in value
        or windows.drive
        or windows.root
        or posix.is_absolute()
        or Path(value).is_absolute()
    ):
        return False

    for component in value.split("/"):
        if component in {".", ".."}:
            continue
        if (
            not component
            or component.endswith((".", " "))
            or any(
                character in WINDOWS_FORBIDDEN_COMPONENT_CHARACTERS
                for character in component
            )
        ):
            return False
        basename = component.split(".", 1)[0].rstrip(" ").casefold()
        if basename in WINDOWS_RESERVED_COMPONENT_BASENAMES:
            return False
    return True


def validate_rule_mapping(
    adapter_root: Path,
    source_package: Path,
    package_root: Path,
    mapping_path: Path,
    reachable_runtime_paths: set[str] | None = None,
    core_catalog_path: Path | None = None,
    conformance_path: Path | None = None,
) -> tuple[MappingSummary | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    adapter_root = lexical_absolute(adapter_root)
    source_package = lexical_absolute(source_package)
    package_root = lexical_absolute(package_root)
    mapping_path = lexical_absolute(mapping_path)
    if is_link(adapter_root):
        return None, [
            Diagnostic("ADAPTER_ROOT_LINK", "adapter root must not be a link or junction")
        ]
    if not adapter_root.is_dir():
        return None, [Diagnostic("ADAPTER_ROOT_MISSING", "adapter root is missing")]
    if not is_inside(source_package, adapter_root):
        return None, [
            Diagnostic("SOURCE_PACKAGE_ESCAPE", "source package escapes adapter root")
        ]
    if first_link_component(source_package, adapter_root) is not None:
        return None, [
            Diagnostic("SOURCE_ROOT_LINK", "source package path traverses a link or junction")
        ]
    if not is_inside(source_package.resolve(), adapter_root.resolve()):
        return None, [
            Diagnostic("SOURCE_PACKAGE_ESCAPE", "source package escapes adapter root")
        ]
    if is_link(package_root):
        return None, [
            Diagnostic("PACKAGE_ROOT_LINK", "package root must not be a link or junction")
        ]
    if not package_root.is_dir():
        return None, [Diagnostic("PACKAGE_ROOT_MISSING", "package root is missing")]
    if not is_inside(mapping_path, adapter_root):
        return None, [
            Diagnostic("MAPPING_SOURCE_ESCAPE", "rule mapping escapes adapter root")
        ]
    if first_link_component(mapping_path, adapter_root) is not None:
        return None, [
            Diagnostic("MAPPING_SOURCE_LINK", "rule mapping path traverses a link or junction")
        ]
    if not is_inside(mapping_path.resolve(), adapter_root.resolve()):
        return None, [
            Diagnostic("MAPPING_SOURCE_ESCAPE", "rule mapping escapes adapter root")
        ]
    mapping = parse_rule_mapping(mapping_path, diagnostics)
    if core_catalog_path is not None and conformance_path is not None:
        catalog = parse_core_catalog(lexical_absolute(core_catalog_path), diagnostics)
        conformance = parse_conformance_manifest(
            lexical_absolute(conformance_path), diagnostics
        )
        validate_rule_inventory(mapping, catalog, conformance, diagnostics)
    rules = mapping.rules
    runtime_targets: set[str] = set()
    metadata_targets: set[str] = set()

    for rule_id, entries in sorted(rules.items()):
        if not entries:
            diagnostics.append(
                Diagnostic("MAPPING_RULE_EMPTY", "rule has no implementations", rule_id)
            )
        for entry in entries:
            raw_path = entry.get("file", "")
            section = entry.get("section", "")
            if not is_portable_relative_path(raw_path):
                diagnostics.append(
                    Diagnostic("MAPPING_SOURCE_ESCAPE", "mapping source escapes adapter root", rule_id, raw_path)
                )
                continue
            target_path = lexical_absolute(
                adapter_root / Path(*PurePosixPath(raw_path).parts)
            )
            if not is_inside(target_path, adapter_root):
                diagnostics.append(
                    Diagnostic("MAPPING_SOURCE_ESCAPE", "mapping source escapes adapter root", rule_id, raw_path)
                )
                continue
            if first_link_component(target_path, adapter_root) is not None:
                diagnostics.append(
                    Diagnostic(
                        "MAPPING_SOURCE_LINK",
                        "mapping source path traverses a link or junction",
                        rule_id,
                        raw_path,
                    )
                )
                continue
            try:
                case_mismatch = first_case_mismatch(target_path, adapter_root)
            except OSError:
                diagnostics.append(
                    Diagnostic(
                        "MAPPING_SOURCE_CASE_UNVERIFIABLE",
                        "mapping source path casing could not be verified",
                        rule_id,
                        raw_path,
                    )
                )
                continue
            if case_mismatch is not None:
                diagnostics.append(
                    Diagnostic(
                        "MAPPING_SOURCE_CASE_MISMATCH",
                        "mapping source path casing differs from filesystem entry",
                        rule_id,
                        raw_path,
                    )
                )
                continue
            try:
                unlisted_alias = resolves_through_unlisted_entry(
                    target_path,
                    adapter_root,
                )
            except OSError:
                diagnostics.append(
                    Diagnostic(
                        "MAPPING_SOURCE_CASE_UNVERIFIABLE",
                        "mapping source path casing could not be verified",
                        rule_id,
                        raw_path,
                    )
                )
                continue
            if unlisted_alias:
                diagnostics.append(
                    Diagnostic(
                        "MAPPING_SOURCE_ESCAPE",
                        "mapping source is not an exact adapter entry",
                        rule_id,
                        raw_path,
                    )
                )
                continue
            target = target_path.resolve()
            if not is_inside(target, adapter_root.resolve()):
                diagnostics.append(
                    Diagnostic("MAPPING_SOURCE_ESCAPE", "mapping source escapes adapter root", rule_id, raw_path)
                )
                continue
            if not target.is_file():
                diagnostics.append(
                    Diagnostic("MAPPING_SOURCE_MISSING", "mapping source is missing", rule_id, raw_path)
                )
                continue
            text = read_utf8(target, "mapping source", diagnostics)
            if text is None:
                continue
            if target.suffix.casefold() == ".md":
                count = markdown_h2_headings(text).count(section)
                if count == 0:
                    diagnostics.append(
                        Diagnostic(
                            "MAPPING_SECTION_MISSING",
                            "missing Markdown section",
                            rule_id,
                            f"{raw_path}#{section}",
                        )
                    )
                elif count > 1:
                    diagnostics.append(
                        Diagnostic(
                            "MAPPING_SECTION_DUPLICATE",
                            "duplicate Markdown section",
                            rule_id,
                            f"{raw_path}#{section}",
                        )
                    )
            elif target.suffix.casefold() in {".yaml", ".yml"}:
                if section not in yaml_top_level_keys(text):
                    diagnostics.append(
                        Diagnostic(
                            "MAPPING_SECTION_MISSING",
                            "missing YAML top-level section",
                            rule_id,
                            f"{raw_path}#{section}",
                        )
                    )
            else:
                diagnostics.append(
                    Diagnostic(
                        "MAPPING_SOURCE_INVALID",
                        "mapping source must be Markdown or YAML",
                        rule_id,
                        raw_path,
                    )
                )
                continue
            relative = relative_path(target, adapter_root)
            source_root = source_package.resolve()
            if is_inside(target, source_root):
                package_relative = target.relative_to(source_root).as_posix()
                if (
                    reachable_runtime_paths is not None
                    and package_relative not in reachable_runtime_paths
                ):
                    diagnostics.append(
                        Diagnostic(
                            "MAPPING_SOURCE_UNREACHABLE",
                            "unreachable runtime mapping source",
                            rule_id,
                            relative,
                        )
                    )
                validate_package_file(
                    package_root,
                    package_relative,
                    diagnostics,
                    missing_code="PACKAGE_MAPPING_MISSING",
                    missing_detail="package omission of runtime mapping source",
                    source=rule_id,
                )
                runtime_targets.add(relative)
            else:
                metadata_targets.add(relative)

    if diagnostics:
        return None, diagnostics
    return (
        MappingSummary(
            runtime_targets=tuple(sorted(runtime_targets)),
            metadata_targets=tuple(sorted(metadata_targets)),
        ),
        diagnostics,
    )


def validate_contract(
    adapter_root: Path,
    source_package: Path,
    package_root: Path,
    mapping_path: Path,
    core_catalog_path: Path = DEFAULT_CORE_CATALOG,
    conformance_path: Path = DEFAULT_CONFORMANCE,
) -> ContractSummary:
    graph, graph_diagnostics = validate_reference_graph(source_package, package_root)
    mapping, mapping_diagnostics = validate_rule_mapping(
        adapter_root,
        source_package,
        package_root,
        mapping_path,
        set(graph.graph) if graph is not None else None,
        core_catalog_path,
        conformance_path,
    )
    diagnostics = graph_diagnostics + mapping_diagnostics
    if diagnostics:
        raise CodexContractError(diagnostics)
    assert graph is not None
    assert mapping is not None
    return ContractSummary(graph, mapping)


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", normalized, flags=re.UNICODE).strip()


def resolve_measurement_path(package_root: Path, value: str) -> Path:
    package_root = lexical_absolute(package_root)
    if is_link(package_root):
        raise CodexContractError(
            [
                Diagnostic(
                    "MEASUREMENT_ROOT_LINK",
                    "measurement root must not be a link or junction",
                )
            ]
        )
    if not package_root.is_dir():
        raise CodexContractError(
            [Diagnostic("MEASUREMENT_INPUT_INVALID", "measurement root is unavailable")]
        )
    pure = PurePosixPath(value)
    if not is_portable_relative_path(value) or pure.is_absolute():
        raise CodexContractError(
            [Diagnostic("MEASUREMENT_INPUT_INVALID", "load-set path is not package-relative", target=value)]
        )
    candidate_path = lexical_absolute(package_root / Path(*pure.parts))
    if not is_inside(candidate_path, package_root):
        raise CodexContractError(
            [Diagnostic("MEASUREMENT_INPUT_INVALID", "load-set path is unavailable inside package", target=value)]
        )
    if first_link_component(candidate_path, package_root) is not None:
        raise CodexContractError(
            [
                Diagnostic(
                    "MEASUREMENT_PATH_LINK",
                    "load-set path traverses a link or junction",
                    target=value,
                )
            ]
        )
    try:
        case_mismatch = first_case_mismatch(candidate_path, package_root)
    except OSError:
        raise CodexContractError(
            [
                Diagnostic(
                    "MEASUREMENT_INPUT_CASE_UNVERIFIABLE",
                    "load-set path casing could not be verified",
                    target=value,
                )
            ]
        ) from None
    if case_mismatch is not None:
        raise CodexContractError(
            [
                Diagnostic(
                    "MEASUREMENT_INPUT_CASE_MISMATCH",
                    "load-set path casing differs from package entry",
                    target=value,
                )
            ]
        )
    try:
        unlisted_alias = resolves_through_unlisted_entry(
            candidate_path,
            package_root,
        )
    except OSError:
        raise CodexContractError(
            [
                Diagnostic(
                    "MEASUREMENT_INPUT_CASE_UNVERIFIABLE",
                    "load-set path casing could not be verified",
                    target=value,
                )
            ]
        ) from None
    if unlisted_alias:
        raise CodexContractError(
            [
                Diagnostic(
                    "MEASUREMENT_INPUT_INVALID",
                    "load-set path is not an exact package entry",
                    target=value,
                )
            ]
        )
    candidate = candidate_path.resolve()
    if not is_inside(candidate, package_root.resolve()) or not candidate.is_file():
        raise CodexContractError(
            [Diagnostic("MEASUREMENT_INPUT_INVALID", "load-set path is unavailable inside package", target=value)]
        )
    return candidate


def measure_load_set(package_root: Path, sources: tuple[str, ...]) -> dict[str, object]:
    if not sources:
        raise CodexContractError(
            [Diagnostic("MEASUREMENT_INPUT_INVALID", "load set must not be empty")]
        )
    normalized_parts = []
    for source in sources:
        path = resolve_measurement_path(package_root, source)
        diagnostics: list[Diagnostic] = []
        text = read_utf8(path, "measurement source", diagnostics)
        if diagnostics or text is None:
            raise CodexContractError(diagnostics)
        normalized_parts.append(normalize_text(text))
    normalized_bytes = len("\n".join(normalized_parts).encode("utf-8"))
    return {
        "sources": list(sources),
        "normalized_utf8_bytes": normalized_bytes,
        "loaded_context_proxy": (normalized_bytes + BYTES_PER_PROXY_TOKEN - 1)
        // BYTES_PER_PROXY_TOKEN,
    }


def measure_source_file(source_package: Path, skill_id: str) -> dict[str, object]:
    relative = f"skills/{skill_id}/SKILL.md"
    path = resolve_measurement_path(source_package, relative)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise CodexContractError(
            [
                Diagnostic(
                    "MEASUREMENT_INPUT_UNREADABLE",
                    f"cannot read public SKILL.md for measurement: {exc}",
                    str(path),
                )
            ]
        ) from None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CodexContractError(
            [Diagnostic("MEASUREMENT_INPUT_INVALID", "public SKILL.md is not UTF-8", skill_id)]
        ) from exc
    return {
        "path": relative,
        "raw_utf8_bytes": len(raw),
        "whitespace_words": len(text.split()),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def build_report(
    adapter_root: Path,
    source_package: Path,
    package_root: Path,
    mapping_path: Path,
    core_catalog_path: Path = DEFAULT_CORE_CATALOG,
    conformance_path: Path = DEFAULT_CONFORMANCE,
) -> dict[str, object]:
    summary = validate_contract(
        adapter_root,
        source_package,
        package_root,
        mapping_path,
        core_catalog_path,
        conformance_path,
    )
    adapter_root = lexical_absolute(adapter_root)
    source_package = lexical_absolute(source_package)
    package_root = lexical_absolute(package_root)
    source_files = {
        skill_id: measure_source_file(source_package, skill_id)
        for skill_id in summary.reference_graph.public_skills
    }
    return {
        "schema_version": 1,
        "algorithm": {
            "id": ALGORITHM_ID,
            "normalization": "Unicode NFC; collapse each Unicode whitespace run to one ASCII space; strip; join ordered load-set files with one LF; count ceil(UTF-8 bytes / 4).",
            "bytes_per_proxy_token": BYTES_PER_PROXY_TOKEN,
            "billing_guarantee": False,
            "total_context_guarantee": False,
            "limitation": "This is a source-level proxy, not billing or total-context measurement.",
        },
        "load_set_semantics": {
            "load_sets": "Cumulative package text after routing into the selected stage, before conditional action contracts are read; retained for direct comparison with the pre-refactor baseline.",
            "action_ready_load_sets": "Cumulative package text required to complete the selected stage action, including artifact and lens contracts when applicable.",
        },
        "package": {
            "source": relative_path(source_package, adapter_root),
            "package_matches_source": package_root == source_package,
        },
        "source_files": source_files,
        "action_ready_load_sets": {
            name: measure_load_set(package_root, sources)
            for name, sources in ACTION_READY_LOAD_SETS.items()
        },
        "load_sets": {
            name: measure_load_set(package_root, sources)
            for name, sources in DEFAULT_LOAD_SETS.items()
        },
        "validation": {
            "reference_targets": list(summary.reference_graph.reference_targets),
            "runtime_mapping_targets": list(summary.mapping.runtime_targets),
            "adapter_metadata_mapping_targets": list(summary.mapping.metadata_targets),
        },
    }


def write_report(path: Path, report: dict[str, object]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise CodexContractError(
            [
                Diagnostic(
                    "REPORT_WRITE_FAILED",
                    f"cannot write report: {exc}",
                    str(path),
                )
            ]
        ) from None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adapter-root", type=Path, default=DEFAULT_ADAPTER_ROOT)
    parser.add_argument(
        "--source-package-root", type=Path, default=DEFAULT_SOURCE_PACKAGE
    )
    parser.add_argument("--package-root", type=Path, default=DEFAULT_SOURCE_PACKAGE)
    parser.add_argument("--rule-mapping", type=Path, default=DEFAULT_RULE_MAPPING)
    parser.add_argument("--core-catalog", type=Path, default=DEFAULT_CORE_CATALOG)
    parser.add_argument("--conformance", type=Path, default=DEFAULT_CONFORMANCE)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.validate_only:
            validate_contract(
                args.adapter_root,
                args.source_package_root,
                args.package_root,
                args.rule_mapping,
                args.core_catalog,
                args.conformance,
            )
            report = {"status": "valid"}
        else:
            report = build_report(
                args.adapter_root,
                args.source_package_root,
                args.package_root,
                args.rule_mapping,
                args.core_catalog,
                args.conformance,
            )
        if args.report is not None:
            write_report(args.report, report)
    except CodexContractError as exc:
        print("Codex contract validation failed:", file=sys.stderr)
        for diagnostic in exc.diagnostics:
            print(f"- {diagnostic.render()}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Codex contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
