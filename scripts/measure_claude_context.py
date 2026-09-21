#!/usr/bin/env python3
"""Measure captured Claude instruction context after validating behavior evidence.

Synthetic mode exercises arithmetic only. Captures and their independent review
are supplied evidence: hashes cannot establish that a host log is authentic or
that unrecorded injections did not occur. This tool never invokes a model.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "adapters/claude-code/plugin/ask-then-do-it"
# Require captures from the current release-owned runtime.
RUNTIME_VERSION = "1.4.3"
SCENARIOS = {
    "documented-requirements": "documented-requirements.md",
    "specification": "specification.md",
    "ticket-planning": "ticket-planning.md",
    "tdd-implementation": "tdd-implementation.md",
    "direct-implementation": "direct-implementation.md",
    "full-review": "review.md",
    "architecture-diagnosis": "architecture-improvement.md",
    "normal-lite": "lite-workflow.md",
    "high-risk-lite": "lite-workflow.md",
    "model-switch-continuation": "lite-workflow.md",
}
PROFILES = ("general", "claude-5")
STAGE_MODULES = frozenset(SCENARIOS.values()) | {"requirements.md"}
EXCLUDED = {
    "host-system", "tool-definitions", "user-task", "repository-source",
    "task-artifacts", "necessary-tool-output", "hidden-reasoning", "model-output",
}
CAPTURED = {"route-context", "hook-context", "skill-listing"}
FILE_KINDS = {"public-skill", "orchestration", "stage", "reviewer-description", "reviewer-prompt"}
FORMULA = "proxy_tokens=ceil(normalized_bytes/4); optimized*100<=general*50"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact(value, keys, label):
    require(isinstance(value, dict) and set(value) == set(keys), f"{label}: unexpected or missing fields")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)


def relative_file(root, name):
    require(isinstance(name, str) and name and "\\" not in name and ":" not in name, "capture path must be portable and relative")
    parts = PurePosixPath(name)
    require(not parts.is_absolute() and all(p not in (".", "..") for p in name.split("/")) and "//" not in name, "unsafe capture path")
    target = root
    for part in parts.parts:
        target = target / part
        require(not target.is_symlink() and not (hasattr(target, "is_junction") and target.is_junction()), "linked capture path is not allowed")
    require(target.resolve().is_relative_to(root.resolve()) and target.is_file(), "capture file missing or outside fixture")
    return target


def read_capture(root, ref):
    exact(ref, ("path", "sha256"), "capture reference")
    require(isinstance(ref["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", ref["sha256"]), "invalid raw SHA-256")
    raw = relative_file(root, ref["path"]).read_bytes()
    require(sha(raw) == ref["sha256"], "capture raw SHA-256 mismatch")
    return raw.decode("utf-8")


def body_and_description(text):
    text = text.replace("\r\n", "\n")
    require(text.startswith("---\n") and "\n---\n" in text[4:], "expected frontmatter")
    frontmatter, body = text[4:].split("\n---\n", 1)
    description = [line.removeprefix("description: ") for line in frontmatter.splitlines() if line.startswith("description: ")]
    require(len(description) == 1, "expected one description")
    return body, description[0]


def required_material(scenario, profile, checkpoint):
    stage = SCENARIOS[scenario]
    result = [
        ("route-context", "UserPromptExpansion"),
        ("public-skill", "skills/ask-then-do-it/SKILL.md"),
        ("orchestration", f"profiles/{profile}/orchestration.md"),
        ("stage", f"profiles/{profile}/{stage}"),
    ]
    if checkpoint == "reviewer-ready":
        result += [
            ("reviewer-description", "agents/ask-then-do-it-reviewer.md"),
            ("reviewer-prompt", "agents/ask-then-do-it-reviewer.md"),
        ]
    return result


def validate_route_text(text, profile):
    lines = text.splitlines()
    begin, end = "ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1", "END_ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1"
    require(lines.count(begin) == lines.count(end) == 1 and lines.index(begin) < lines.index(end), "capture requires one framed route envelope")
    payload = json.loads("\n".join(lines[lines.index(begin) + 1:lines.index(end)]))
    exact(payload, ("plugin", "version", "entry", "operation_id", "model_classification", "selected_profile", "routing_status", "disclosure_code"), "route envelope")
    require((payload["plugin"], payload["version"], payload["entry"], payload["selected_profile"], payload["routing_status"]) == ("ask-then-do-it", RUNTIME_VERSION, "/ask-then-do-it:ask-then-do-it", profile, "ready"), "route identity is not a ready automatic profile route")
    require(isinstance(payload["operation_id"], str) and re.fullmatch(r"op_[a-f0-9]{32}", payload["operation_id"]), "invalid route operation identity")
    allowed = {("supported-non-5", "none"), ("unknown", "unknown-model-general-compatibility")} if profile == "general" else {("claude-5", "none")}
    require((payload["model_classification"], payload["disclosure_code"]) in allowed, "route classification/disclosure mismatch")


def prepare_template():
    cases = []
    for scenario in SCENARIOS:
        checkpoints = ("stage-ready", "reviewer-ready") if scenario == "full-review" else ("stage-ready",)
        cases.append({
            "id": scenario, "task": {"path": "", "sha256": ""},
            "stage_outcome": {"path": "", "sha256": ""}, "capability": "unobserved",
            "profiles": {profile: {checkpoint: {
                "capture_complete": False, "trace": {"path": "", "sha256": ""},
                "events": [],
            } for checkpoint in checkpoints} for profile in PROFILES},
        })
    return {
        "schema_version": 1, "fixture_id": "claude-context-1.4.3", "version": "1.4.3",
        "evidence_kind": "unobserved", "capture_review": "", "scenarios": cases,
    }


def measure_texts(texts):
    normalized = [re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip() for text in texts]
    length = len("\n".join(normalized).encode("utf-8"))
    return {"normalized_bytes": length, "proxy_tokens": (length + 3) // 4}


def threshold(general, optimized):
    require(type(general) is int and type(optimized) is int and general > 0 and optimized >= 0, "invalid proxy totals")
    return optimized * 100 <= general * 50


def check_record(root, record, scenario, profile, checkpoint, synthetic, plugin_root):
    exact(record, ("capture_complete", "trace", "events"), "checkpoint")
    require(record["capture_complete"] is True, "checkpoint capture is incomplete")
    events = record["events"]
    require(isinstance(events, list) and events, "checkpoint has no events")
    if not synthetic:
        # Independent trace is retained separately so edits to the measurement
        # inventory cannot silently discard, reorder or invent captured events.
        trace = json.loads(read_capture(root, record["trace"]))
        exact(trace, ("scenario", "profile", "checkpoint", "events"), "capture trace")
        require((trace["scenario"], trace["profile"], trace["checkpoint"]) == (scenario, profile, checkpoint), "capture trace identity mismatch")
        require(trace["events"] == events, "event order/inventory differs from capture trace")
    required = required_material(scenario, profile, checkpoint)
    seen, texts, sources, exclusions = [], [], [], []
    for index, event in enumerate(events):
        exact(event, ("kind", "origin", "path", "sha256"), "event")
        kind, origin = event["kind"], event["origin"]
        require(isinstance(kind, str) and isinstance(origin, str), "event kind/origin must be text")
        text = read_capture(root, {"path": event["path"], "sha256": event["sha256"]})
        require(bool(text.strip()), "empty capture cannot count as material")
        identity = (kind, origin)
        if kind in EXCLUDED:
            # A Plugin origin can never be relabelled as excluded material.
            require(origin == kind, "excluded origin must identify a permitted non-Plugin category")
            exclusions.append({"load_order": index, **event})
            continue
        additional_stage = kind == "stage" and origin in {f"profiles/{profile}/{module}" for module in STAGE_MODULES}
        require(identity in required or kind in CAPTURED or additional_stage, "unexpected counted material or wrong profile")
        if kind in CAPTURED:
            expected_origin = {"route-context": "UserPromptExpansion", "hook-context": "hook-additional-context", "skill-listing": "host-skill-listing"}[kind]
            require(origin == expected_origin, "invalid model-visible output origin")
            if kind == "route-context" and not synthetic:
                validate_route_text(text, profile)
        elif not synthetic:
            canonical = relative_file(plugin_root, origin).read_text(encoding="utf-8")
            if kind in {"public-skill", "reviewer-prompt", "reviewer-description"}:
                body, description = body_and_description(canonical)
                canonical = description if kind == "reviewer-description" else body
            require(text.replace("\r\n", "\n") == canonical.replace("\r\n", "\n"), "captured Plugin instructions differ from current source")
        seen.append(identity)
        texts.append(text)
        sources.append({"load_order": index, **event})
    require(all(identity in seen for identity in required), "required instruction or visible route material omitted")
    # Route injection and Skill expansion order can differ by host. Stage and
    # reviewer loading must still follow their instruction prerequisites.
    orchestration = next(i for i, identity in enumerate(seen) if identity[0] == "orchestration")
    stage = next(i for i, identity in enumerate(seen) if identity[0] == "stage")
    require(orchestration < stage, "stage loaded before orchestration")
    if checkpoint == "reviewer-ready":
        require(stage < next(i for i, identity in enumerate(seen) if identity[0] == "reviewer-prompt"), "reviewer loaded before stage")
    return texts, sources, exclusions


def behavior_errors(path, plugin_root):
    if path is None:
        return ["actual behavior evidence is required before measurement"]
    scripts = str(Path(__file__).resolve().parent)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    try:
        from validate_claude_behavior import validate_behavior_evidence
        return validate_behavior_evidence(Path(path), plugin_root=plugin_root)
    except (ImportError, OSError, ValueError, TypeError, KeyError) as exc:
        return [f"behavior evidence is unavailable or invalid: {type(exc).__name__}"]


def evaluate(path, *, synthetic=False, behavior_evidence=None, plugin_root=PLUGIN):
    result = {"status": "blocked", "release_pass": False, "errors": [], "measurements": [], "formula": FORMULA}
    try:
        data = read_json(path)
        exact(data, ("schema_version", "fixture_id", "version", "evidence_kind", "capture_review", "scenarios"), "fixture")
        require(type(data["schema_version"]) is int and data["schema_version"] == 1 and data["fixture_id"] == "claude-context-1.4.3" and data["version"] == "1.4.3", "fixture identity/version mismatch")
        require(data["evidence_kind"] == ("synthetic" if synthetic else "observed"), "unobserved/synthetic captures cannot establish observed measurement")
        require(isinstance(data["capture_review"], str) and bool(data["capture_review"].strip()), "independent capture-completeness review is required")
        if not synthetic:
            errors = behavior_errors(behavior_evidence, plugin_root)
            if errors:
                result["errors"] = ["behavior gate: " + error for error in errors]
                return result
        cases = data["scenarios"]
        require(isinstance(cases, list) and len(cases) == len(SCENARIOS), "expected ten context scenarios")
        require([case.get("id") for case in cases if isinstance(case, dict)] == list(SCENARIOS), "scenario inventory/order mismatch")
        pending = []
        for case in cases:
            exact(case, ("id", "task", "stage_outcome", "capability", "profiles"), "scenario")
            require(case["capability"] in ("conversation", "tools", "multi_agent"), "invalid capability")
            if case["id"] == "full-review":
                require(case["capability"] == "multi_agent", "reviewer-ready requires multi_agent")
            for field in ("task", "stage_outcome"):
                require(bool(read_capture(path.parent, case[field]).strip()), f"empty shared {field}")
            exact(case["profiles"], PROFILES, "profiles")
            checkpoints = ("stage-ready", "reviewer-ready") if case["id"] == "full-review" else ("stage-ready",)
            for profile in PROFILES:
                exact(case["profiles"][profile], checkpoints, "checkpoint inventory")
                if case["id"] == "full-review":
                    stage_events = case["profiles"][profile]["stage-ready"]["events"]
                    reviewer_events = case["profiles"][profile]["reviewer-ready"]["events"]
                    def identities(events):
                        return [(event["kind"], event["origin"], event["sha256"]) for event in events]
                    require(identities(reviewer_events[:len(stage_events)]) == identities(stage_events), "reviewer-ready must retain all prior injections in order")
            for checkpoint in checkpoints:
                row = {"scenario": case["id"], "checkpoint": checkpoint, "capability": case["capability"], "input_hashes": {field: case[field]["sha256"] for field in ("task", "stage_outcome")}}
                excluded = []
                for profile in PROFILES:
                    texts, sources, omissions = check_record(path.parent, case["profiles"][profile][checkpoint], case["id"], profile, checkpoint, synthetic, plugin_root)
                    row[profile] = {"texts": texts, "sources": sources, "exclusions": omissions}
                    excluded.append([(entry["kind"], entry["sha256"]) for entry in omissions])
                require(excluded[0] == excluded[1], "asymmetric excluded material")
                pending.append(row)
        # No arithmetic until the whole inventory and prerequisites are valid.
        for row in pending:
            for profile in PROFILES:
                row[profile].update(measure_texts(row[profile].pop("texts")))
            general, optimized = (row[profile]["proxy_tokens"] for profile in PROFILES)
            row["threshold_pass"] = threshold(general, optimized)
            row["reduction_percent"] = (general - optimized) / general * 100
        result.update(fixture_id=data["fixture_id"], version=data["version"], fixture_sha256=sha(path.read_bytes()), evidence_kind=data["evidence_kind"], measurements=pending)
        result["status"] = "synthetic-only" if synthetic else "measured"
        result["release_pass"] = not synthetic and all(row["threshold_pass"] for row in pending)
        if not synthetic:
            result["behavior_evidence_sha256"] = sha(Path(behavior_evidence).read_bytes())
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError) as exc:
        result["errors"] = [str(exc) if isinstance(exc, ValueError) else f"invalid or unreadable capture: {type(exc).__name__}"]
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare", type=Path, help="write a new unexecuted capture template")
    mode.add_argument("--fixture", type=Path)
    parser.add_argument("--behavior-evidence", type=Path)
    parser.add_argument("--synthetic", action="store_true", help="calculator diagnostics only; never a release pass")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.prepare:
        try:
            with args.prepare.open("x", encoding="utf-8", newline="\n") as handle:
                json.dump(prepare_template(), handle, indent=2, ensure_ascii=False)
                handle.write("\n")
        except OSError as exc:
            parser.error(f"cannot create new template: {type(exc).__name__}")
        print("Prepared unobserved capture template; no model execution or measurement.")
        return 0
    result = evaluate(args.fixture, synthetic=args.synthetic, behavior_evidence=args.behavior_evidence)
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else f'{result["status"]}: release_pass={result["release_pass"]}; errors={result["errors"]}')
    if result["errors"]:
        return 1
    return 0 if args.synthetic or result["release_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
