"""SELF-AUTHORED SYNTHETIC data builder for validator tests only.

It never invokes Claude and must never label any generated record actual.
"""

import json
from pathlib import Path

from scripts import validate_claude_behavior as behavior


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_synthetic(output: Path, plugin_root: Path = behavior.PLUGIN) -> Path:
    ledger_path = behavior.prepare(output, plugin_root)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    catalog, _, _ = behavior.contracts()
    recipes = behavior.run_recipes(catalog)
    ledger.update(evidence_kind="synthetic", status="recorded")
    ledger["operator_review"] = {
        "reviewer": "synthetic-test-author", "reviewed_at": ledger["prepared_at"],
        "provenance": "synthetic-test-only", "complete_transcripts_reviewed": True,
        "semantic_outcomes_reviewed": True,
    }
    for run, recipe in zip(ledger["runs"], recipes):
        run.update(evidence_kind="synthetic", status="recorded", started_at=ledger["prepared_at"],
                   ended_at=ledger["prepared_at"], fresh_session=True,
                   session_sha256=behavior.value_digest(["SYNTHETIC-NOT-A-CLAUDE-SESSION", run["id"]]))
        run["environment"].update(os="Windows", surface="CLI", claude_code="2.1.251", node="22.0.0",
                                  model="claude-opus-5", effort="high", tools=["read", "shell", "write"])
        messages, response_positions, input_positions, executions = [], [], [], []
        for index, prompt in enumerate(behavior.prompts(recipe)):
            input_positions.append(len(messages))
            messages.append({"role": "user", "text": prompt})
            for required in behavior.execution_requirements(recipe):
                if required["input_index"] == index:
                    output_text = f"SYNTHETIC fabricated tool output {run['id']} input {index} phase {required['phase']}; no command was executed."
                    position = len(messages)
                    messages.append({"role": "tool", "text": output_text})
                    executions.append({**required, "argv": ["synthetic-command", required["phase"]],
                                       "exit_code": 1 if required["phase"] in {"red", "known-failure"} else 0,
                                       "citation": {"message_index": position, "start": 0, "end": len(output_text), "quote": output_text}})
            response_positions.append(len(messages))
            messages.append({"role": "assistant", "text": f"SYNTHETIC fabricated response for {run['id']} input {index}; not an observed Claude answer. This marker exercises evidence references only."})
        for observation, expected in zip(run["observations"], behavior.outcome_contract(recipe)):
            position = response_positions[expected["input_index"]]
            quote = messages[position]["text"]
            observation.update(verdict="satisfied", assessment="SYNTHETIC test-only assessment; no human or model observation occurred.",
                               citations=[{"message_index": position, "start": 0, "end": len(quote), "quote": quote}])
        if recipe["category"] == "authority":
            operations = [{"profile": profile, "entry": "public-entry", "result": "bound-profile",
                           "first_message": input_positions[index], "last_message": response_positions[index],
                           "loaded_sources": [f"profiles/{profile}/orchestration.md"]}
                          for index, profile in enumerate([recipe["from_profile"], recipe["profile"]])]
        else:
            operations = [{"profile": recipe["profile"], "entry": "test-only-profile-selection", "result": "bound-profile",
                           "first_message": 0, "last_message": len(messages) - 1,
                           "loaded_sources": [f"profiles/{recipe['profile']}/orchestration.md"]}]
        transcript = {
            "schema_version": 1, "evidence_kind": "synthetic", "capture_method": "synthetic-fixture",
            "complete_scrubbed_export": True, "run_id": run["id"], "session_sha256": run["session_sha256"],
            "context_origin": "new-session", "started_at": run["started_at"], "ended_at": run["ended_at"],
            "environment": run["environment"], "input_sha256": run["input_sha256"],
            "source_manifest_sha256": behavior.value_digest(ledger["source_hashes"]),
            "messages": messages, "operations": operations, "executions": executions,
        }
        relative = "transcripts/" + run["id"].replace("/", "__") + ".json"
        transcript_path = output / relative
        write_json(transcript_path, transcript)
        run["transcript"] = {"path": relative, "sha256": behavior.digest(transcript_path.read_bytes())}
    write_json(ledger_path, ledger)
    return ledger_path
