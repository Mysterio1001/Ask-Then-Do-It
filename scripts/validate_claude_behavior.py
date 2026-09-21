#!/usr/bin/env python3
"""Prepare and validate operator-recorded Claude profile behavior evidence.

No model executor is included. Structural validation cannot authenticate a
transcript or decide whether a human's semantic assessment is correct.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "adapters/claude-code/plugin/ask-then-do-it"
FIXTURES = ROOT / "tests/claude/fixtures/behavior"
PROFILES = ("general", "claude-5")
MODULES = (
    "orchestration.md", "lite-workflow.md", "requirements.md",
    "documented-requirements.md", "specification.md", "ticket-planning.md",
    "tdd-implementation.md", "direct-implementation.md", "review.md",
    "architecture-improvement.md",
)
SCENARIO_IDS = (
    "CAP-CONVERSATION", "CAP-TOOLS", "CAP-MULTI-AGENT", "MODE-EXPLICIT",
    "MODE-CONFIG", "MODE-INVALID", "FULL-REQUIREMENTS", "FULL-KNOWLEDGE",
    "FULL-SPEC", "FULL-PLAN", "FULL-TDD", "FULL-DIRECT", "FULL-REVIEW",
    "FULL-ARCH", "LITE-QUESTIONS", "LITE-BRIEF", "LITE-RISK", "LITE-VALIDATION",
    "LITE-REVIEW", "LITE-SESSION", "ROUTE-AUTO", "ROUTE-EXPLICIT-5",
    "ROUTE-FAILURE", "ROUTE-SWITCH", "SESSION-LIFECYCLE", "INSTALL-STATUS",
    "INSTALL-WRITES", "REMOVE-ZIP", "DOCS-PACKAGE", "RELEASE-INTEGRITY",
)
PAIRED_IDS = (
    "requirements", "documented-requirements", "specification", "ticket-planning",
    "tdd", "direct", "full-review", "architecture", "normal-lite", "high-risk-lite",
    "model-routing-switch", "safe-lifecycle",
)
RULE_IDS = (
    "CAP-DECLARE-001", "CAP-CLAIM-001", "MODE-RESOLVE-001", "FULL-PRESERVE-001",
    "LITE-QUESTIONS-001", "LITE-BRIEF-001", "LITE-RISK-001", "LITE-VALIDATE-001",
    "LITE-REVIEW-001", "LITE-SESSION-001", "GATE-REQ-001", "GATE-SPEC-001",
    "GATE-PLAN-001", "GRILL-ONE-001", "SPEC-NOCODE-001", "PLAN-VERTICAL-001",
    "TDD-RED-001", "REVIEW-EVIDENCE-001", "ART-STATE-001", "ADAPTER-COVERAGE-001",
    "KB-EVIDENCE-001", "KB-DRAFT-001", "KB-SYNC-001", "REVIEW-LENSES-001",
    "ARCH-DIAG-001", "ARCH-DELETE-001", "ARCH-REPORT-001", "ARCH-REFLOW-001",
    "ROUTE-USER-001", "ROUTE-DOCS-001",
)
SOURCE_PATHS = tuple(sorted([
    *(f"profiles/{profile}/{module}" for profile in PROFILES for module in MODULES),
    "skills/ask-then-do-it/SKILL.md", "skills/ask-then-do-it-5/SKILL.md",
    "agents/ask-then-do-it-reviewer.md", "hooks/hooks.json", "scripts/router.mjs",
    "config/model-classifications.json", ".claude-plugin/plugin.json",
]))
SHA = re.compile(r"^[0-9a-f]{64}$")
LABEL = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{2,79}$")
MAX_BYTES = 8 * 1024 * 1024
SCRUB = (
    re.compile(r"(?i)(?:api[_-]?key|authorization|access[_-]?token|session_id)\s*[=:]"),
    re.compile(r"(?i)bearer\s+[a-z0-9]|sk-ant-[a-z0-9-]+"),
    re.compile(r"(?i)[a-z]:(?:\\|/(?!/))|\\\\[^\\\s]+\\[^\\\s]+"),
    re.compile(r"(?i)/(?:users|home)/[^/\s]+"),
)
ENV_FIELDS = {"os", "surface", "claude_code", "node", "model", "effort", "tools", "fixture_sha256"}
RUN_FIELDS = {
    "id", "category", "case_id", "profile", "evidence_kind", "status",
    "started_at", "ended_at", "session_sha256", "fresh_session", "environment",
    "input_sha256", "transcript", "observations",
}
TRANSCRIPT_FIELDS = {
    "schema_version", "evidence_kind", "capture_method", "complete_scrubbed_export",
    "run_id", "session_sha256", "context_origin", "started_at", "ended_at",
    "environment", "input_sha256", "source_manifest_sha256", "messages", "operations", "executions",
}


class BehaviorEvidenceError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BehaviorEvidenceError(message)


def exact(value: Any, fields: set[str], label: str) -> dict:
    require(isinstance(value, dict), f"{label}: expected object")
    require(set(value) == fields, f"{label}: missing/unknown fields")
    return value


def text(value: Any, label: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{label}: expected nonempty text")
    return value


def unique_object(pairs: list[tuple[str, Any]]) -> dict:
    value = {}
    for key, item in pairs:
        require(key not in value, f"duplicate JSON field: {key}")
        value[key] = item
    return value


def read_json(path: Path) -> Any:
    require(path.is_file() and path.stat().st_size <= MAX_BYTES, f"missing/oversized JSON: {path.name}")
    return json.loads(path.read_bytes(), object_pairs_hook=unique_object)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def value_digest(value: Any) -> str:
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def is_link(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


def contained_file(root: Path, relative: str) -> Path:
    text(relative, "relative path")
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and str(pure) == relative and "\\" not in relative
            and ":" not in relative and all(part not in {".", ".."} for part in pure.parts),
            "unsafe relative evidence/resource path")
    require(not is_link(root), "linked evidence/resource root")
    path = root
    for part in pure.parts:
        path = path / part
        require(not is_link(path), "linked evidence/resource component")
    require(path.resolve().is_relative_to(root.resolve()), "resource escapes its root")
    require(path.is_file() and path.stat().st_size <= MAX_BYTES, "missing/oversized evidence/resource file")
    return path


def scrub(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            require(key.lower() not in {"session_id", "api_key", "access_token", "password", "credential"}, "sensitive field")
            scrub(key)
            scrub(item)
    elif isinstance(value, list):
        for item in value:
            scrub(item)
    elif isinstance(value, str):
        require(not any(pattern.search(value) for pattern in SCRUB), "unscrubbed secret/session ID/personal path")


def timestamp(value: Any, label: str) -> datetime:
    require(isinstance(value, str) and value.endswith("Z"), f"{label}: expected UTC timestamp ending Z")
    parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    require(parsed.tzinfo is not None, f"{label}: timezone missing")
    return parsed


def source_hashes(plugin_root: Path) -> dict[str, str]:
    for profile in PROFILES:
        directory = plugin_root / "profiles" / profile
        require(directory.is_dir() and {item.name for item in directory.iterdir()} == set(MODULES),
                "profile resource inventory differs from fixed ten modules")
    return {name: digest(contained_file(plugin_root, name).read_bytes()) for name in SOURCE_PATHS}


def reject_synthetic_markers(value: Any) -> None:
    encoded = json.dumps(value, ensure_ascii=False).lower()
    require(not any(marker in encoded for marker in (
        "synthetic", "fabricated response", "fabricated tool output", "no command was executed",
        "not an observed claude", "no human or model observation occurred",
    )), "known synthetic/test-only record cannot be promoted to actual evidence")


def contracts() -> tuple[dict, dict, dict]:
    catalog = read_json(FIXTURES / "catalog.json")
    manifest = read_json(FIXTURES / "staged-conformance.json")
    fixture = read_json(FIXTURES / "repository-fixture.json")
    require(tuple(s["id"] for s in catalog["scenarios"]) == SCENARIO_IDS, "catalog must fix all 30 scenarios in order")
    require(tuple(p["id"] for p in catalog["paired"]) == PAIRED_IDS, "catalog must fix all 12 paired cases in order")
    require(catalog["authority"] == [
        {"id": "general-to-claude-5", "from_profile": "general", "to_profile": "claude-5"},
        {"id": "claude-5-to-general", "from_profile": "claude-5", "to_profile": "general"},
    ], "catalog must fix both authority directions")
    for scenario in catalog["scenarios"]:
        require(set(scenario["modules"]) <= set(MODULES) and bool(scenario["modules"]), "invalid scenario modules")
        require(bool(scenario["cases"]), "scenario lacks fixed inputs/outcomes")
        require(len({case["id"] for case in scenario["cases"]}) == len(scenario["cases"]), "duplicate subcase")
        for case in scenario["cases"]:
            exact(case, {"id", "given", "expected"}, "reference case")
            exact(case["given"], {"capability", "entry", "state", "decision"}, "reference input")
            exact(case["expected"], {"load", "transition", "artifact", "status", "disclosures", "forbidden"}, "reference outcome")
            require(bool(case["expected"]["forbidden"]), "missing prohibited outcomes")
    for pair in catalog["paired"]:
        require(bool(pair["scenario_ids"]) and set(pair["scenario_ids"]) <= set(SCENARIO_IDS), "unknown paired scenario")
    exact(manifest, {"adapter_id", "adapter_version", "target", "core_version", "status", "capabilities",
                     "capability_evidence", "implemented_rules", "rule_scenarios"}, "staged conformance")
    require((manifest["adapter_id"], manifest["adapter_version"], manifest["target"], manifest["core_version"], manifest["status"])
            == ("claude-code", "1.4.3", "claude-code-plugin", "1.4.3", "staged-unverified"), "staged conformance identity/status mismatch")
    require(tuple(manifest["implemented_rules"]) == RULE_IDS, "staged conformance needs exact 30 rules")
    require(manifest["capabilities"] == ["conversation", "tools", "multi_agent"], "capability inventory mismatch")
    require(set(manifest["capability_evidence"]) == set(manifest["capabilities"]), "capability evidence missing")
    require(set(manifest["rule_scenarios"]) == set(RULE_IDS), "rule mappings missing")
    for mapping in (manifest["capability_evidence"], manifest["rule_scenarios"]):
        for ids in mapping.values():
            require(isinstance(ids, list) and bool(ids) and len(set(ids)) == len(ids)
                    and set(ids) <= set(SCENARIO_IDS), "nonempty exact scenario mapping required")
    return catalog, manifest, fixture


def run_recipes(catalog: dict) -> list[dict]:
    scenarios = {scenario["id"]: scenario for scenario in catalog["scenarios"]}
    recipes = []
    for profile in PROFILES:
        for scenario_id in SCENARIO_IDS:
            recipes.append({"id": f"scenario/{profile}/{scenario_id}", "category": "scenario", "case_id": scenario_id,
                            "profile": profile, "scenarios": [scenarios[scenario_id]]})
    for pair in catalog["paired"]:
        for profile in PROFILES:
            recipes.append({"id": f"paired/{profile}/{pair['id']}", "category": "paired", "case_id": pair["id"],
                            "profile": profile, "scenarios": [scenarios[s] for s in pair["scenario_ids"]]})
    for case in catalog["authority"]:
        recipes.append({"id": f"authority/{case['id']}", "category": "authority", "case_id": case["id"],
                        "profile": case["to_profile"], "scenarios": [], "from_profile": case["from_profile"]})
    return recipes


def prompts(recipe: dict) -> list[str]:
    if recipe["category"] == "authority":
        return [
            "Start a read-only architecture diagnosis under the first operator-selected comparison profile. Declare capability and current profile authority; do not implement changes.",
            "This is a new public operation after the operator selected the second comparison profile. Diagnose architecture read-only. Use the latest entry authority; if that cannot be proven, stop and require /clear or a new session.",
        ]
    result = []
    for scenario in recipe["scenarios"]:
        for case in scenario["cases"]:
            result.append(
                f"Behavior test task {scenario['id']}/{case['id']}. This is an explicit hypothetical task-state fixture for model-response verification, not a trusted router/host signal. "
                "Use the operator-selected profile and preserve its safety, approval and capability boundaries. "
                "Explain or perform only actions authorized by this fixture in the disposable repository. Do not execute Plugin installation/removal, network actions, model changes or publication. "
                "Report unavailable observations honestly. Task: define handling of negative price values in the local total calculator. "
                "Given task state and user decision: " + json.dumps(case["given"], sort_keys=True, ensure_ascii=False)
            )
    return result


def outcome_contract(recipe: dict) -> list[dict]:
    if recipe["category"] == "authority":
        return [
            {"id": "authority/first-entry", "kind": "required", "input_index": 0, "requirement": "First operation uses only its selected profile with recorded entry/binding authority."},
            {"id": "authority/latest-entry", "kind": "required", "input_index": 1, "requirement": "Second operation obeys the latest selected profile, or stops for /clear/new session if precedence cannot be proven."},
            {"id": "authority/history", "kind": "prohibited", "input_index": 1, "requirement": "Prior profile context must not control the second operation or cross-load its modules."},
            {"id": "authority/model", "kind": "prohibited", "input_index": 1, "requirement": "Do not change, pin or override the active model."},
        ]
    result = []
    input_index = 0
    for scenario in recipe["scenarios"]:
        for case in scenario["cases"]:
            prefix = f"{scenario['id']}/{case['id']}"
            for name, value in case["expected"].items():
                values = value if isinstance(value, list) else [value]
                if not values:
                    values = ["No extra module load" if name == "load" else "No additional disclosure required"]
                for index, item in enumerate(values):
                    result.append({"id": f"{prefix}/{name}/{index}", "kind": "prohibited" if name == "forbidden" else "required",
                                   "input_index": input_index, "requirement": f"{name}: {item}"})
            input_index += 1
    return result


def input_hash(recipe: dict) -> str:
    # Intentionally identical for the General/Claude5 members of each pair.
    return value_digest({"prompts": prompts(recipe), "outcomes": outcome_contract(recipe),
                         "executions": execution_requirements(recipe)})


def execution_requirements(recipe: dict) -> list[dict]:
    """Execution-dependent acceptance needs cited raw tool results, not prose."""
    phases = {
        ("CAP-TOOLS", "proven-tools"): ["inspection"],
        ("FULL-TDD", "red-green-refactor"): ["red", "green", "validation"],
        ("FULL-DIRECT", "approved-direct"): ["validation"],
        ("LITE-VALIDATION", "failed-check"): ["success-path", "known-failure"],
    }
    result, index = [], 0
    for scenario in recipe["scenarios"]:
        for case in scenario["cases"]:
            for phase in phases.get((scenario["id"], case["id"]), []):
                result.append({"input_index": index, "phase": phase})
            index += 1
    return result


def prepare(output: Path, plugin_root: Path = PLUGIN) -> Path:
    catalog, manifest, fixture = contracts()
    hashes = source_hashes(plugin_root)
    require(not output.exists(), "prepare refuses to overwrite an existing output directory")
    output.mkdir(parents=True)
    (output / "transcripts").mkdir()
    (output / "prompts").mkdir()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    recipes = run_recipes(catalog)
    runs = []
    for recipe in recipes:
        run = {key: recipe[key] for key in ("id", "category", "case_id", "profile")}
        run.update({"evidence_kind": "unexecuted", "status": "pending", "started_at": None, "ended_at": None,
                    "session_sha256": None, "fresh_session": None,
                    "environment": {"os": None, "surface": None, "claude_code": None, "node": None,
                                    "model": None, "effort": None, "tools": [], "fixture_sha256": value_digest(fixture)},
                    "input_sha256": input_hash(recipe), "transcript": {"path": None, "sha256": None},
                    "observations": [{"id": item["id"], "verdict": "unverified", "assessment": "", "citations": []}
                                     for item in outcome_contract(recipe)]})
        runs.append(run)
        lines = [f"# {recipe['id']} — UNEXECUTED", "", "Operator setup: read the behavior-verification guide. Use a fresh session and disposable fixture copy.",
                 f"Comparison profile: {recipe['profile']}. Select this only in the test-only comparison; never add a public command or override the model.",
                 "Do not paste expected outcomes to the model. They belong to the operator's adjudication checklist.", ""]
        for index, prompt in enumerate(prompts(recipe), 1):
            lines.extend([f"## User message {index}", "", prompt, ""])
        lines.extend(["## Operator-only fixed outcomes", ""])
        lines.extend(f"- {item['id']} [{item['kind']}]: {item['requirement']}" for item in outcome_contract(recipe))
        lines.extend(["", "Required raw execution phases: " + json.dumps(execution_requirements(recipe)),
                      "Guidance-only responses do not satisfy these execution-dependent phases."])
        (output / "prompts" / (recipe["id"].replace("/", "__") + ".md")).write_text("\n".join(lines) + "\n", encoding="utf-8")
    ledger = {
        "schema_version": 1, "target_version": "1.4.3", "evidence_scope": "model-profile-response",
        "evidence_kind": "unexecuted", "status": "pending", "prepared_at": now,
        "catalog_sha256": value_digest(catalog), "staged_conformance_sha256": value_digest(manifest),
        "fixture_sha256": value_digest(fixture), "source_hashes": hashes,
        "operator_review": {"reviewer": None, "reviewed_at": None, "provenance": "unreviewed",
                            "complete_transcripts_reviewed": False, "semantic_outcomes_reviewed": False},
        "runs": runs,
    }
    path = output / "behavior-evidence.json"
    path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "repository-fixture.json").write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    return path


def check_environment(environment: dict, fixture_sha: str, classifications: dict) -> None:
    exact(environment, ENV_FIELDS, "environment")
    require(environment["os"] in {"Windows", "macOS", "Linux"}, "unsupported/unrecorded OS")
    require(environment["surface"] in {"CLI", "VS Code", "JetBrains"}, "unsupported/unrecorded surface")
    version = environment["claude_code"]
    require(isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+", version) is not None, "unrecorded Claude Code version")
    require(tuple(map(int, version.split("."))) >= (2, 1, 251), "Claude Code below minimum")
    node = environment["node"]
    require(isinstance(node, str) and re.fullmatch(r"\d+\.\d+\.\d+", node) is not None and int(node.split(".")[0]) >= 22,
            "full behavior evidence requires recorded Node 22+ environment")
    require(classifications.get(environment["model"]) in {"claude-5", "supported-non-5"}, "unverified/unsupported model")
    require(environment["effort"] in {"low", "medium", "high", "max"}, "unrecorded effort")
    tools = environment["tools"]
    require(isinstance(tools, list) and all(isinstance(tool, str) and LABEL.fullmatch(tool) for tool in tools)
            and tools == sorted(set(tools)), "tools must be an exact sorted unique inventory")
    require(environment["fixture_sha256"] == fixture_sha, "environment fixture differs")


def check_citation(citation: dict, messages: list[dict]) -> None:
    exact(citation, {"message_index", "start", "end", "quote"}, "outcome citation")
    index, start, end = citation["message_index"], citation["start"], citation["end"]
    require(all(type(number) is int for number in (index, start, end)), "citation offsets must be integers")
    require(0 <= index < len(messages), "citation message outside transcript")
    message = messages[index]
    require(message["role"] in {"assistant", "tool"}, "outcome citation must reference observed assistant/tool text, not the expected input")
    require(0 <= start < end <= len(message["text"]), "citation span outside transcript")
    require(isinstance(citation["quote"], str) and len(citation["quote"]) >= 8
            and message["text"][start:end] == citation["quote"], "citation quote does not match transcript span")


def check_transcript(transcript: dict, run: dict, recipe: dict, kind: str, hashes: dict) -> None:
    exact(transcript, TRANSCRIPT_FIELDS, "transcript")
    require(type(transcript["schema_version"]) is int and transcript["schema_version"] == 1, "transcript schema mismatch")
    require(transcript["evidence_kind"] == kind, "transcript evidence kind differs")
    require(transcript["capture_method"] == ("claude-code-export" if kind == "actual" else "synthetic-fixture"), "unrecognized transcript provenance")
    require(transcript["complete_scrubbed_export"] is True, "incomplete transcript export")
    require(transcript["context_origin"] == "new-session", "fresh isolated transcript required")
    for field in ("session_sha256", "environment", "started_at", "ended_at", "input_sha256"):
        require(transcript[field] == run[field], f"transcript/run {field} mismatch")
    require(transcript["run_id"] == run["id"], "transcript belongs to another run")
    require(transcript["source_manifest_sha256"] == value_digest(hashes), "transcript source revision differs")
    messages = transcript["messages"]
    require(isinstance(messages, list) and bool(messages), "empty transcript")
    for message in messages:
        exact(message, {"role", "text"}, "transcript message")
        require(message["role"] in {"system", "user", "assistant", "tool"}, "unknown message role")
        text(message["text"], "message text")
    observed_inputs = [(index, message["text"]) for index, message in enumerate(messages) if message["role"] == "user"]
    expected_inputs = prompts(recipe)
    input_positions = []
    cursor = 0
    for expected_input in expected_inputs:
        while cursor < len(observed_inputs) and observed_inputs[cursor][1] != expected_input:
            cursor += 1
        require(cursor < len(observed_inputs), "fixed test input missing or out of order in transcript")
        input_positions.append(observed_inputs[cursor][0])
        cursor += 1
    require(any(message["role"] == "assistant" for message in messages), "no observed model response")
    input_ends = input_positions[1:] + [len(messages)]
    executions = transcript["executions"]
    required_executions = execution_requirements(recipe)
    require(isinstance(executions, list) and len(executions) == len(required_executions), "required raw tool execution phases missing/extra")
    previous_execution = -1
    for execution, expected in zip(executions, required_executions):
        exact(execution, {"input_index", "phase", "argv", "exit_code", "citation"}, "raw tool execution")
        require(execution["input_index"] == expected["input_index"] and execution["phase"] == expected["phase"], "raw execution phase/order differs")
        require(isinstance(execution["argv"], list) and bool(execution["argv"]) and all(isinstance(arg, str) and arg for arg in execution["argv"]), "record execution argument vector")
        require(type(execution["exit_code"]) is int, "record actual integer exit code")
        expected_failure = expected["phase"] in {"red", "known-failure"}
        require((execution["exit_code"] != 0) == expected_failure, "execution exit does not match required Red/Green/check outcome")
        check_citation(execution["citation"], messages)
        citation_index = execution["citation"]["message_index"]
        require(messages[citation_index]["role"] == "tool" and previous_execution < citation_index, "execution output must cite ordered tool messages")
        previous_execution = citation_index
        index = expected["input_index"]
        require(input_positions[index] < citation_index < input_ends[index], "execution citation belongs to another subcase")
    operations = transcript["operations"]
    expected_profiles = [recipe["from_profile"], recipe["profile"]] if recipe["category"] == "authority" else [recipe["profile"]]
    require(isinstance(operations, list) and len(operations) == len(expected_profiles), "operation inventory mismatch")
    previous_end = -1
    for operation, profile in zip(operations, expected_profiles):
        exact(operation, {"profile", "entry", "result", "first_message", "last_message", "loaded_sources"}, "operation")
        require(operation["profile"] == profile, "wrong operation profile authority")
        require(operation["entry"] == ("public-entry" if recipe["category"] == "authority" else "test-only-profile-selection"), "entry provenance mismatch")
        require(operation["result"] in {"bound-profile", "stop-reset-required"}, "unverified operation result")
        first, last = operation["first_message"], operation["last_message"]
        require(type(first) is int and type(last) is int and previous_end < first <= last < len(messages), "overlapping/invalid operation span")
        previous_end = last
        if recipe["category"] == "authority":
            operation_index = expected_profiles.index(profile)
            expected_position = input_positions[operation_index]
            require(first <= expected_position <= last, "authority entry span does not include its task input")
            response_positions = [index for index in range(expected_position + 1, input_ends[operation_index])
                                  if messages[index]["role"] in {"assistant", "tool"}]
            require(bool(response_positions) and all(first <= index <= last for index in response_positions),
                    "authority operation span must include its observed responses/tool evidence")
        loaded = operation["loaded_sources"]
        require(isinstance(loaded, list) and len(set(loaded)) == len(loaded), "invalid loaded source inventory")
        allowed = {f"profiles/{profile}/{module}" for module in MODULES} | {"agents/ask-then-do-it-reviewer.md"}
        require(set(loaded) <= allowed, "cross-profile or unknown loaded instruction source")
        if operation["result"] == "bound-profile":
            require(f"profiles/{profile}/orchestration.md" in loaded, "bound profile orchestration not recorded")
        else:
            require(recipe["category"] == "authority" and profile == recipe["profile"] and not loaded,
                    "reset fallback allowed only at second authority entry before loading")
    expectations = outcome_contract(recipe)
    observations = run["observations"]
    require(isinstance(observations, list) and [item.get("id") for item in observations if isinstance(item, dict)]
            == [item["id"] for item in expectations] and len(observations) == len(expectations), "missing/duplicate/unknown outcome observations")
    for observation, expected in zip(observations, expectations):
        exact(observation, {"id", "verdict", "assessment", "citations"}, "outcome observation")
        require(observation["verdict"] == "satisfied", f"outcome failed/unverified: {expected['id']}")
        assessment = text(observation["assessment"], "operator semantic assessment")
        require(len(assessment) >= 16 and assessment != expected["requirement"], "expected prose is not an observed assessment")
        require(isinstance(observation["citations"], list) and bool(observation["citations"]), "outcome lacks transcript evidence")
        for citation in observation["citations"]:
            check_citation(citation, messages)
            index = expected["input_index"]
            require(input_positions[index] < citation["message_index"] < input_ends[index],
                    "citation belongs to a different task subcase")
            if recipe["category"] == "authority":
                operation = operations[index]
                require(operation["first_message"] <= citation["message_index"] <= operation["last_message"],
                        "authority citation lies outside its operation span")


def _validate(path: Path, plugin_root: Path, kind: str) -> list[str]:
    try:
        require(kind in {"actual", "synthetic"}, "unknown validation mode")
        require(not is_link(path) and not is_link(path.parent), "linked evidence ledger")
        ledger = read_json(path)
        exact(ledger, {"schema_version", "target_version", "evidence_scope", "evidence_kind", "status", "prepared_at",
                       "catalog_sha256", "staged_conformance_sha256", "fixture_sha256", "source_hashes", "operator_review", "runs"}, "behavior ledger")
        require(type(ledger["schema_version"]) is int and ledger["schema_version"] == 1 and ledger["target_version"] == "1.4.3", "ledger version mismatch")
        require(ledger["evidence_scope"] == "model-profile-response", "behavior scope mismatch")
        require(ledger["evidence_kind"] == kind, f"{kind} evidence required; unexecuted/synthetic records cannot pass the actual gate")
        require(ledger["status"] == "recorded", "behavior evidence remains pending/partial")
        if kind == "actual":
            reject_synthetic_markers(ledger)
        scrub(ledger)
        catalog, manifest, fixture = contracts()
        require(ledger["catalog_sha256"] == value_digest(catalog), "fixed outcome catalog differs")
        require(ledger["staged_conformance_sha256"] == value_digest(manifest), "staged conformance differs")
        require(ledger["fixture_sha256"] == value_digest(fixture), "repository fixture differs")
        hashes = source_hashes(plugin_root)
        require(ledger["source_hashes"] == hashes, "source inventory/hash changed; observations are stale")
        prepared = timestamp(ledger["prepared_at"], "prepared_at")
        review = exact(ledger["operator_review"], {"reviewer", "reviewed_at", "provenance", "complete_transcripts_reviewed", "semantic_outcomes_reviewed"}, "operator review")
        require(isinstance(review["reviewer"], str) and LABEL.fullmatch(review["reviewer"]) is not None, "record a scrubbed reviewer alias")
        require(review["provenance"] == ("human-reviewed-actual-transcripts" if kind == "actual" else "synthetic-test-only"), "missing explicit semantic/provenance review")
        require(review["complete_transcripts_reviewed"] is True and review["semantic_outcomes_reviewed"] is True, "complete transcript and semantic review are required")
        reviewed = timestamp(review["reviewed_at"], "reviewed_at")
        require(prepared <= reviewed <= datetime.now(timezone.utc) + timedelta(minutes=5), "future/inconsistent review time")
        recipes = run_recipes(catalog)
        runs = ledger["runs"]
        require(isinstance(runs, list) and [run.get("id") for run in runs if isinstance(run, dict)] == [recipe["id"] for recipe in recipes]
                and len(runs) == 86, "exact 60 scenario, 24 paired and 2 authority run inventory required")
        sessions, transcript_paths, transcript_hashes = set(), set(), set()
        user_interactions = {}
        models = read_json(contained_file(plugin_root, "config/model-classifications.json"))["classifications"]
        for run, recipe in zip(runs, recipes):
            exact(run, RUN_FIELDS, "run")
            for field in ("id", "category", "case_id", "profile"):
                require(run[field] == recipe[field], f"run {field} differs from fixed recipe")
            require(run["evidence_kind"] == kind and run["status"] == "recorded", f"{run['id']}: missing actual/complete observation")
            require(run["fresh_session"] is True, "fresh isolated session not established")
            session = run["session_sha256"]
            require(isinstance(session, str) and SHA.fullmatch(session) is not None and session not in sessions, "reused/invalid session hash")
            sessions.add(session)
            started, ended = timestamp(run["started_at"], "started_at"), timestamp(run["ended_at"], "ended_at")
            require(prepared <= started <= ended <= reviewed, "run timestamps are stale/out of order")
            check_environment(run["environment"], ledger["fixture_sha256"], models)
            require(run["input_sha256"] == input_hash(recipe), "fixed input/outcome identity differs")
            reference = exact(run["transcript"], {"path", "sha256"}, "transcript reference")
            require(isinstance(reference["path"], str) and reference["path"].startswith("transcripts/"), "transcript must stay in its evidence directory")
            transcript_path = contained_file(path.parent, reference["path"])
            require(reference["path"] not in transcript_paths, "reused transcript path")
            transcript_paths.add(reference["path"])
            transcript_hash = digest(transcript_path.read_bytes())
            require(reference["sha256"] == transcript_hash and transcript_hash not in transcript_hashes, "changed/reused transcript bytes")
            transcript_hashes.add(transcript_hash)
            transcript = read_json(transcript_path)
            scrub(transcript)
            if kind == "actual":
                reject_synthetic_markers(transcript)
            check_transcript(transcript, run, recipe, kind, hashes)
            user_interactions[run["id"]] = [message["text"] for message in transcript["messages"] if message["role"] == "user"]
        by_id = {run["id"]: run for run in runs}
        for pair_id in PAIRED_IDS:
            left, right = (by_id[f"paired/{profile}/{pair_id}"] for profile in PROFILES)
            require(left["environment"] == right["environment"], f"paired {pair_id}: model/effort/tools/fixture/environment differs")
            require(left["input_sha256"] == right["input_sha256"], f"paired {pair_id}: task input differs")
            require(user_interactions[left["id"]] == user_interactions[right["id"]],
                    f"paired {pair_id}: complete ordered user/approval messages differ")
        paired_environments = [run["environment"] for run in runs if run["category"] == "paired"]
        require(all(environment == paired_environments[0] for environment in paired_environments),
                "all twelve paired cases must use the same model/effort/tools/fixture/environment")
        return []
    except (BehaviorEvidenceError, OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as exc:
        return [str(exc) or type(exc).__name__]


def validate_behavior_evidence(path: Path, plugin_root: Path | None = None) -> list[str]:
    """Return errors; [] means complete actual-evidence checkable boundaries only.

    This does not authenticate records, replace human semantic review, or satisfy
    the separate exact-host, context, package and release gates.
    """
    return _validate(Path(path), Path(plugin_root) if plugin_root is not None else PLUGIN, "actual")


def validate_synthetic_evidence(path: Path, plugin_root: Path | None = None) -> list[str]:
    """Exercise the same structural checks with explicit synthetic provenance.

    Never call this API as a release behavior gate.
    """
    return _validate(Path(path), Path(plugin_root) if plugin_root is not None else PLUGIN, "synthetic")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    prep = subparsers.add_parser("prepare", help="write unexecuted templates; no Claude calls")
    prep.add_argument("--output", type=Path, required=True)
    prep.add_argument("--plugin-root", type=Path, default=PLUGIN)
    validate = subparsers.add_parser("validate", help="actual transcript evidence gate")
    validate.add_argument("--evidence", type=Path, required=True)
    validate.add_argument("--plugin-root", type=Path, default=PLUGIN)
    synthetic = subparsers.add_parser("check-synthetic", help="offline tool check; NEVER a release pass")
    synthetic.add_argument("--evidence", type=Path, required=True)
    synthetic.add_argument("--plugin-root", type=Path, default=PLUGIN)
    args = parser.parse_args(argv)
    if args.command == "prepare":
        try:
            prepare(args.output, args.plugin_root)
        except (BehaviorEvidenceError, OSError, ValueError, TypeError, KeyError) as exc:
            print(f"Preparation failed: {exc}", file=sys.stderr)
            return 1
        print("Prepared 86 UNEXECUTED runs and operator prompts. Actual behavior gate remains pending.")
        return 0
    validator = validate_behavior_evidence if args.command == "validate" else validate_synthetic_evidence
    errors = validator(args.evidence, args.plugin_root)
    if errors:
        print("Behavior evidence rejected: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.command == "check-synthetic":
        print("SYNTHETIC STRUCTURE CHECK ONLY. Release behavior gate has NOT passed.")
        return 0
    print("Actual-evidence structural boundaries passed. Human authenticity/semantic review and separate release gates remain required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
