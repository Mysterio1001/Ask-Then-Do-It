#!/usr/bin/env python3
"""Measure the deterministic Full/Lite workflow-controlled token proxy."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath
from typing import Any

from build_release import compose_generic_workflow


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = (
    ROOT
    / "tests"
    / "release"
    / "fixtures"
    / "workflow-token-proxy"
    / "benchmark.json"
)
RELEASE_CONFIG = ROOT / "release" / "release.json"
EXPECTED_GENERIC_SOURCE = "adapters/generic-prompts"
ALGORITHM_ID = "normalized-utf8-quarter-v1"
BYTES_PER_PROXY_TOKEN = 4
MINIMUM_REDUCTION_BASIS_POINTS = 6000
TOP_LEVEL_KEYS = {
    "schema_version",
    "scenario",
    "shared_exclusions",
    "controlled_categories",
    "modes",
    "generic_composed_prompt",
}
SCENARIO_KEYS = {
    "id",
    "language",
    "host",
    "capability",
    "task",
    "decisions",
    "risk",
    "delivered_outcome",
    "ticket_count",
    "review_finding_count",
    "architecture_diagnosis",
}
DECISION_KEYS = {"id", "value"}
EXCLUSION_KEYS = {"kind", "reason"}
MODE_KEYS = {"events"}
EVENT_KEYS = {"id", "category", "source", "budget"}
GENERIC_KEYS = {"source", "module_order"}
CONTROLLED_CATEGORIES = (
    "selected-instructions",
    "questions",
    "scope-and-planning",
    "handoffs",
    "implementation-validation",
    "review-completion",
)
SHARED_EXCLUSIONS = {
    "task-specific-source-code",
    "necessary-tool-output",
    "hidden-model-reasoning",
}
LITE_BUDGETS = {
    "questions": ("questions", 500),
    "change-brief": ("scope-and-planning", 800),
    "completion": ("review-completion", 500),
}
LITE_BUDGET_EVENT_IDS = {
    "questions": "lite-questions",
    "change-brief": "lite-change-brief",
    "completion": "lite-completion",
}
EXPECTED_EVENT_CONTRACTS = {
    "full": (
        (
            "full-orchestrator",
            "selected-instructions",
            "adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md",
            None,
        ),
        (
            "full-documented-requirements",
            "selected-instructions",
            "adapters/codex/plugin/ask-then-do-it/skills/ask-with-docs/SKILL.md",
            None,
        ),
        (
            "full-write-spec",
            "selected-instructions",
            "adapters/codex/plugin/ask-then-do-it/skills/write-spec/SKILL.md",
            None,
        ),
        (
            "full-plan-tickets",
            "selected-instructions",
            "adapters/codex/plugin/ask-then-do-it/skills/plan-tickets/SKILL.md",
            None,
        ),
        (
            "full-implement-tdd",
            "selected-instructions",
            "adapters/codex/plugin/ask-then-do-it/skills/implement-tdd/SKILL.md",
            None,
        ),
        (
            "full-review-code",
            "selected-instructions",
            "adapters/codex/plugin/ask-then-do-it/skills/review-code/SKILL.md",
            None,
        ),
        (
            "full-questions",
            "questions",
            "tests/release/fixtures/workflow-token-proxy/full/questions.md",
            None,
        ),
        (
            "full-scope-and-planning",
            "scope-and-planning",
            "tests/release/fixtures/workflow-token-proxy/full/scope-and-planning.md",
            None,
        ),
        (
            "full-handoffs",
            "handoffs",
            "tests/release/fixtures/workflow-token-proxy/full/handoffs.md",
            None,
        ),
        (
            "full-implementation-evidence",
            "implementation-validation",
            "tests/release/fixtures/workflow-token-proxy/full/implementation-evidence.md",
            None,
        ),
        (
            "full-review",
            "review-completion",
            "tests/release/fixtures/workflow-token-proxy/full/review.md",
            None,
        ),
        (
            "full-completion",
            "review-completion",
            "tests/release/fixtures/workflow-token-proxy/full/completion.md",
            None,
        ),
    ),
    "lite": (
        (
            "lite-orchestrator",
            "selected-instructions",
            "adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/SKILL.md",
            None,
        ),
        (
            "lite-workflow-reference",
            "selected-instructions",
            "adapters/codex/plugin/ask-then-do-it/skills/ask-then-do-it/references/lite-workflow.md",
            None,
        ),
        (
            "lite-questions",
            "questions",
            "tests/release/fixtures/workflow-token-proxy/lite/questions.md",
            "questions",
        ),
        (
            "lite-change-brief",
            "scope-and-planning",
            "tests/release/fixtures/workflow-token-proxy/lite/change-brief.md",
            "change-brief",
        ),
        (
            "lite-handoffs",
            "handoffs",
            "tests/release/fixtures/workflow-token-proxy/lite/handoffs.md",
            None,
        ),
        (
            "lite-implementation-validation",
            "implementation-validation",
            "tests/release/fixtures/workflow-token-proxy/lite/implementation-validation.md",
            None,
        ),
        (
            "lite-review",
            "review-completion",
            "tests/release/fixtures/workflow-token-proxy/lite/review.md",
            None,
        ),
        (
            "lite-completion",
            "review-completion",
            "tests/release/fixtures/workflow-token-proxy/lite/completion.md",
            "completion",
        ),
    ),
}
EXPECTED_GENERIC_MODULES = (
    "bootstrap.md",
    "orchestration.md",
    "lite-workflow.md",
    "requirements.md",
    "documented-requirements.md",
    "specification.md",
    "ticket-planning.md",
    "direct-implementation.md",
    "tdd-implementation.md",
    "review.md",
    "architecture-improvement.md",
)


class ProxyError(RuntimeError):
    """The benchmark fixture or one of its controlled sources is invalid."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument(
        "--json", action="store_true", dest="as_json", help="Emit deterministic JSON."
    )
    return parser.parse_args()


def require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    missing = sorted(expected - set(value))
    unknown = sorted(set(value) - expected)
    if missing or unknown:
        details = []
        if missing:
            details.append(f"missing {missing}")
        if unknown:
            details.append(f"unknown {unknown}")
        raise ProxyError(f"Invalid {label} fields: {', '.join(details)}")


def require_object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProxyError(f"{label} must be an object")
    return value


def require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProxyError(f"{label} must be a non-empty string")
    return value


def require_string_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ProxyError(f"{label} must be a non-empty string array")
    result = []
    for index, item in enumerate(value):
        result.append(require_string(item, f"{label}[{index}]"))
    return result


def resolve_fixture(path: Path) -> Path:
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ProxyError(f"Missing fixture: {path}") from exc
    if not resolved.is_relative_to(ROOT) or not resolved.is_file():
        raise ProxyError(f"Fixture must be a repository-owned file: {resolved}")
    return resolved


def resolve_relative_path(raw: object, label: str, *, directory: bool = False) -> Path:
    value = require_string(raw, label)
    pure = PurePosixPath(value)
    if (
        value != value.replace("\\", "/")
        or pure.is_absolute()
        or Path(value).is_absolute()
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        raise ProxyError(f"{label} must be a safe repository-relative POSIX path")
    candidate = (ROOT / Path(*pure.parts)).resolve()
    if not candidate.is_relative_to(ROOT):
        raise ProxyError(f"{label} escapes the repository: {value}")
    if directory:
        if not candidate.is_dir():
            raise ProxyError(f"Missing {label} directory: {value}")
    elif not candidate.is_file():
        raise ProxyError(f"Missing {label} source: {value}")
    return candidate


def read_utf8(path: Path, label: str) -> tuple[str, bytes]:
    try:
        raw = path.read_bytes()
        return raw.decode("utf-8"), raw
    except UnicodeDecodeError as exc:
        raise ProxyError(f"{label} must contain valid UTF-8: {path}") from exc
    except OSError as exc:
        raise ProxyError(f"Unable to read {label}: {path}: {exc}") from exc


def normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", normalized, flags=re.UNICODE).strip()


def proxy_tokens_for_bytes(normalized_bytes: int) -> int:
    return (normalized_bytes + BYTES_PER_PROXY_TOKEN - 1) // BYTES_PER_PROXY_TOKEN


def measure_normalized_parts(parts: list[str]) -> tuple[int, int]:
    stream = "\n".join(parts)
    normalized_bytes = len(stream.encode("utf-8"))
    return normalized_bytes, proxy_tokens_for_bytes(normalized_bytes)


def format_basis_points(basis_points: int) -> str:
    magnitude = abs(basis_points)
    sign = "-" if basis_points < 0 else ""
    return f"{sign}{magnitude // 100}.{magnitude % 100:02d}"


def load_fixture(path: Path) -> tuple[dict[str, Any], bytes]:
    text, raw = read_utf8(path, "fixture")
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ProxyError(f"Fixture must contain valid JSON: {path}: {exc}") from exc
    fixture = require_object(value, "fixture")
    require_exact_keys(fixture, TOP_LEVEL_KEYS, "fixture")
    if type(fixture["schema_version"]) is not int or fixture["schema_version"] != 1:
        raise ProxyError("fixture.schema_version must equal 1")
    return fixture, raw


def validate_scenario(raw: object) -> dict[str, Any]:
    scenario = require_object(raw, "fixture.scenario")
    require_exact_keys(scenario, SCENARIO_KEYS, "fixture.scenario")
    for key in ("id", "language", "task", "risk"):
        require_string(scenario[key], f"fixture.scenario.{key}")
    if scenario["language"] != "en":
        raise ProxyError("fixture.scenario.language must equal 'en'")
    if scenario["host"] != "codex" or scenario["capability"] != "tools":
        raise ProxyError("fixture scenario must use the tools-capable Codex host")
    decisions = scenario["decisions"]
    if not isinstance(decisions, list) or not decisions:
        raise ProxyError("fixture.scenario.decisions must be a non-empty array")
    decision_ids = set()
    for index, raw_decision in enumerate(decisions):
        decision = require_object(raw_decision, f"fixture.scenario.decisions[{index}]")
        require_exact_keys(
            decision, DECISION_KEYS, f"fixture.scenario.decisions[{index}]"
        )
        decision_id = require_string(
            decision["id"], f"fixture.scenario.decisions[{index}].id"
        )
        require_string(decision["value"], f"fixture.scenario.decisions[{index}].value")
        if decision_id in decision_ids:
            raise ProxyError(f"Duplicate scenario decision id: {decision_id}")
        decision_ids.add(decision_id)
    require_string_list(
        scenario["delivered_outcome"], "fixture.scenario.delivered_outcome"
    )
    if type(scenario["ticket_count"]) is not int or scenario["ticket_count"] != 1:
        raise ProxyError("fixture.scenario.ticket_count must equal 1")
    if (
        type(scenario["review_finding_count"]) is not int
        or scenario["review_finding_count"] != 0
    ):
        raise ProxyError("fixture.scenario.review_finding_count must equal 0")
    if scenario["architecture_diagnosis"] is not False:
        raise ProxyError("fixture.scenario.architecture_diagnosis must be false")
    return scenario


def validate_exclusions(raw: object) -> list[str]:
    if not isinstance(raw, list) or not raw:
        raise ProxyError("fixture.shared_exclusions must be a non-empty array")
    kinds = []
    for index, raw_item in enumerate(raw):
        item = require_object(raw_item, f"fixture.shared_exclusions[{index}]")
        require_exact_keys(item, EXCLUSION_KEYS, f"fixture.shared_exclusions[{index}]")
        kind = require_string(item["kind"], f"fixture.shared_exclusions[{index}].kind")
        require_string(item["reason"], f"fixture.shared_exclusions[{index}].reason")
        if kind in kinds:
            raise ProxyError(f"Duplicate shared exclusion: {kind}")
        kinds.append(kind)
    if set(kinds) != SHARED_EXCLUSIONS:
        raise ProxyError(
            "fixture.shared_exclusions must contain exactly task-specific-source-code, "
            "necessary-tool-output, and hidden-model-reasoning"
        )
    return kinds


def validate_event(
    raw: object,
    mode: str,
    index: int,
    categories: tuple[str, ...],
) -> dict[str, Any]:
    label = f"fixture.modes.{mode}.events[{index}]"
    item = require_object(raw, label)
    require_exact_keys(item, EVENT_KEYS, label)
    event_id = require_string(item["id"], f"{label}.id")
    category = require_string(item["category"], f"{label}.category")
    if category not in categories:
        raise ProxyError(f"{label}.category is unsupported: {category}")
    source_raw = require_string(item["source"], f"{label}.source")
    source = resolve_relative_path(source_raw, f"{label}.source")
    budget = item["budget"]
    if budget is not None and budget not in LITE_BUDGETS:
        raise ProxyError(f"{label}.budget is unsupported: {budget!r}")
    if mode == "full" and budget is not None:
        raise ProxyError("Full events cannot declare Lite output budgets")
    if budget is not None and LITE_BUDGETS[budget][0] != category:
        raise ProxyError(f"{label}.budget does not match category {category}")
    text, source_bytes = read_utf8(source, f"event {event_id}")
    normalized = normalize(text)
    if not normalized:
        raise ProxyError(f"Event source normalizes to empty content: {source_raw}")
    normalized_bytes = len(normalized.encode("utf-8"))
    return {
        "id": event_id,
        "category": category,
        "source": source_raw,
        "budget": budget,
        "normalized": normalized,
        "normalized_bytes": normalized_bytes,
        "proxy_tokens": proxy_tokens_for_bytes(normalized_bytes),
        "source_bytes": source_bytes,
    }


def measure_modes(
    raw_modes: object, categories: tuple[str, ...]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    modes = require_object(raw_modes, "fixture.modes")
    require_exact_keys(modes, {"full", "lite"}, "fixture.modes")
    all_ids = set()
    all_events = []
    reports: dict[str, Any] = {}
    for mode in ("full", "lite"):
        mode_data = require_object(modes[mode], f"fixture.modes.{mode}")
        require_exact_keys(mode_data, MODE_KEYS, f"fixture.modes.{mode}")
        raw_events = mode_data["events"]
        if not isinstance(raw_events, list) or not raw_events:
            raise ProxyError(f"fixture.modes.{mode}.events must be a non-empty array")
        events = [
            validate_event(raw, mode, index, categories)
            for index, raw in enumerate(raw_events)
        ]
        event_ids = tuple(item["id"] for item in events)
        expected_event_ids = tuple(
            contract[0] for contract in EXPECTED_EVENT_CONTRACTS[mode]
        )
        if event_ids != expected_event_ids:
            duplicate = next((item for item in event_ids if event_ids.count(item) > 1), None)
            if duplicate is not None:
                raise ProxyError(f"Duplicate event id: {duplicate}")
            raise ProxyError(f"{mode} event inventory does not match the fixed benchmark")
        duplicate_global = next((item for item in event_ids if item in all_ids), None)
        if duplicate_global is not None:
            raise ProxyError(f"Duplicate event id: {duplicate_global}")
        all_ids.update(event_ids)
        if {item["category"] for item in events} != set(categories):
            raise ProxyError(f"{mode} must include every controlled category")

        budget_events = {}
        for item in events:
            budget_name = item["budget"]
            if budget_name is None:
                continue
            if budget_name in budget_events:
                raise ProxyError(f"Duplicate Lite budget declaration: {budget_name}")
            budget_events[budget_name] = item
        if mode == "lite":
            if set(budget_events) != set(LITE_BUDGETS):
                raise ProxyError("Lite must declare exactly the questions, Change Brief, and completion budgets")
            for budget_name, expected_id in LITE_BUDGET_EVENT_IDS.items():
                if budget_events[budget_name]["id"] != expected_id:
                    raise ProxyError(
                        f"{budget_name} budget must belong to {expected_id}"
                    )
            for item in events:
                if item["category"] == "questions" and item["budget"] != "questions":
                    raise ProxyError("Every Lite question event must use the questions budget")
                if (
                    item["category"] == "scope-and-planning"
                    and item["budget"] != "change-brief"
                ):
                    raise ProxyError("The Lite scope event must use the Change Brief budget")
        elif budget_events:
            raise ProxyError("Full cannot contain budgeted Lite events")

        actual_contract = tuple(
            (item["id"], item["category"], item["source"], item["budget"])
            for item in events
        )
        if actual_contract != EXPECTED_EVENT_CONTRACTS[mode]:
            raise ProxyError(
                f"{mode} event contract does not match the fixed benchmark"
            )

        normalized_parts = [item["normalized"] for item in events]
        normalized_bytes, proxy_tokens = measure_normalized_parts(normalized_parts)
        category_reports = {}
        for category in categories:
            category_parts = [
                item["normalized"] for item in events if item["category"] == category
            ]
            category_bytes, category_proxy = measure_normalized_parts(category_parts)
            category_reports[category] = {
                "normalized_bytes": category_bytes,
                "proxy_tokens": category_proxy,
            }
        budgets = {}
        for budget_name, item in budget_events.items():
            limit = LITE_BUDGETS[budget_name][1]
            passed = item["proxy_tokens"] <= limit
            budgets[budget_name] = {
                "event_id": item["id"],
                "limit": limit,
                "proxy_tokens": item["proxy_tokens"],
                "passed": passed,
            }
            if not passed:
                raise ProxyError(
                    f"Lite {budget_name} fixture exceeds its {limit}-token proxy budget"
                )
        reports[mode] = {
            "normalized_bytes": normalized_bytes,
            "proxy_tokens": proxy_tokens,
            "categories": category_reports,
            "budgets": budgets,
            "events": [
                {
                    "id": item["id"],
                    "category": item["category"],
                    "source": item["source"],
                    "normalized_bytes": item["normalized_bytes"],
                    "proxy_tokens": item["proxy_tokens"],
                }
                for item in events
            ],
        }
        all_events.extend(events)
    return reports, all_events


def measure_generic(raw: object) -> tuple[dict[str, Any], bytes]:
    generic = require_object(raw, "fixture.generic_composed_prompt")
    require_exact_keys(generic, GENERIC_KEYS, "fixture.generic_composed_prompt")
    source_raw = require_string(generic["source"], "fixture.generic_composed_prompt.source")
    if source_raw != EXPECTED_GENERIC_SOURCE:
        raise ProxyError(
            "fixture.generic_composed_prompt.source must equal "
            f"{EXPECTED_GENERIC_SOURCE}"
        )
    source = resolve_relative_path(
        source_raw, "fixture.generic_composed_prompt.source", directory=True
    )
    modules = require_string_list(
        generic["module_order"], "fixture.generic_composed_prompt.module_order"
    )
    if tuple(modules) != EXPECTED_GENERIC_MODULES:
        raise ProxyError(
            "Generic module order must contain the final Lite inventory with "
            "lite-workflow.md immediately after orchestration.md"
        )
    for index, name in enumerate(modules):
        pure = PurePosixPath(name)
        if pure.is_absolute() or len(pure.parts) != 1 or pure.parts[0] in {"", ".", ".."}:
            raise ProxyError(
                f"fixture.generic_composed_prompt.module_order[{index}] is invalid"
            )
        if not (source / name).is_file():
            raise ProxyError(f"Missing Generic composed prompt module: {name}")
    try:
        config = json.loads(RELEASE_CONFIG.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProxyError(f"Unable to read release configuration: {exc}") from exc
    if not isinstance(config, dict) or not isinstance(config.get("generic"), dict):
        raise ProxyError("Release configuration lacks Generic composition data")
    composed_config = copy.deepcopy(config)
    composed_config["generic"]["modules"] = modules
    try:
        composed = compose_generic_workflow(composed_config, source)
        composed_text = composed.decode("utf-8")
    except (KeyError, OSError, UnicodeDecodeError) as exc:
        raise ProxyError(f"Unable to compose the Generic fixed prompt: {exc}") from exc
    normalized = normalize(composed_text)
    normalized_bytes = len(normalized.encode("utf-8"))
    report = {
        "gate_applied": False,
        "applies_equally_to": ["full", "lite"],
        "composed_prompt": {
            "normalized_bytes": normalized_bytes,
            "proxy_tokens": proxy_tokens_for_bytes(normalized_bytes),
            "sha256": hashlib.sha256(composed).hexdigest(),
            "source_modules": modules,
        },
        "limitation": (
            "The complete composed prompt is a fixed cost for both modes; "
            "no Generic 60% guarantee and no billing guarantee is claimed."
        ),
    }
    return report, composed


def fixture_fingerprint(
    fixture_bytes: bytes, events: list[dict[str, Any]], generic_bytes: bytes
) -> str:
    digest = hashlib.sha256()
    digest.update(b"fixture\0")
    digest.update(fixture_bytes)
    for item in events:
        digest.update(b"\0event\0")
        digest.update(item["id"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(item["source"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(item["source_bytes"])
    digest.update(b"\0generic-composed-prompt\0")
    digest.update(generic_bytes)
    return digest.hexdigest()


def build_report(fixture_path: Path) -> dict[str, Any]:
    fixture, fixture_bytes = load_fixture(fixture_path)
    scenario = validate_scenario(fixture["scenario"])
    exclusions = validate_exclusions(fixture["shared_exclusions"])
    categories = require_string_list(
        fixture["controlled_categories"], "fixture.controlled_categories"
    )
    if tuple(categories) != CONTROLLED_CATEGORIES:
        raise ProxyError(
            "fixture.controlled_categories must equal the fixed workflow-controlled inventory"
        )
    modes, events = measure_modes(fixture["modes"], tuple(categories))
    generic, generic_bytes = measure_generic(fixture["generic_composed_prompt"])

    full = modes["full"]["proxy_tokens"]
    lite = modes["lite"]["proxy_tokens"]
    if full <= 0:
        raise ProxyError("Full proxy count must be positive")
    difference = full - lite
    reduction_basis_points = (difference * 10000) // full
    passed = lite * 100 <= full * 40
    fixture_relative = fixture_path.relative_to(ROOT).as_posix()
    return {
        "schema_version": 1,
        "algorithm": {
            "id": ALGORITHM_ID,
            "normalization": (
                "Unicode NFC; collapse each Unicode whitespace run to one ASCII space; "
                "strip; join ordered events with one LF; count ceil(UTF-8 bytes / 4)."
            ),
            "bytes_per_proxy_token": BYTES_PER_PROXY_TOKEN,
            "billing_guarantee": False,
        },
        "fixture": {
            "path": fixture_relative,
            "sha256": fixture_fingerprint(fixture_bytes, events, generic_bytes),
            "scenario_id": scenario["id"],
            "shared_exclusions": exclusions,
        },
        "codex": {
            "host": "codex",
            "capability": "tools",
            "full": modes["full"],
            "lite": modes["lite"],
            "difference_proxy_tokens": difference,
            "gate": {
                "minimum_reduction_basis_points": MINIMUM_REDUCTION_BASIS_POINTS,
                "reduction_basis_points": reduction_basis_points,
                "reduction_percent": format_basis_points(reduction_basis_points),
                "formula": "(full - lite) / full * 100",
                "passed": passed,
            },
        },
        "generic": generic,
    }


def print_human(report: dict[str, Any]) -> None:
    codex = report["codex"]
    gate = codex["gate"]
    generic = report["generic"]
    print(f"Algorithm: {report['algorithm']['id']}")
    print(f"Fixture: {report['fixture']['path']} ({report['fixture']['sha256']})")
    print(f"Full proxy tokens: {codex['full']['proxy_tokens']}")
    print(f"Lite proxy tokens: {codex['lite']['proxy_tokens']}")
    print(f"Difference: {codex['difference_proxy_tokens']}")
    print(
        f"Reduction: {gate['reduction_percent']}% "
        f"(minimum {gate['minimum_reduction_basis_points'] / 100:.2f}%)"
    )
    print(f"Codex gate: {'passed' if gate['passed'] else 'failed'}")
    print(
        "Generic composed prompt fixed cost: "
        f"{generic['composed_prompt']['proxy_tokens']} proxy tokens"
    )
    print(f"Generic limitation: {generic['limitation']}")


def main() -> int:
    args = parse_args()
    try:
        fixture_path = resolve_fixture(args.fixture)
        report = build_report(fixture_path)
    except ProxyError as exc:
        print(f"Workflow token proxy validation failed: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True))
    else:
        print_human(report)
    return 0 if report["codex"]["gate"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
