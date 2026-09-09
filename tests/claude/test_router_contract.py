from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "adapters" / "claude-code" / "plugin" / "ask-then-do-it"
ROUTER = PLUGIN / "scripts" / "router.mjs"
MAPPING = PLUGIN / "config" / "model-classifications.json"
HOOKS = PLUGIN / "hooks" / "hooks.json"

# Ticket 3 must replace or confirm these simulated identities with exact
# Claude Code 2.1.251 observations before the 1.4.0 integration freeze.
PROVISIONAL_COMMAND_NAMES = {
    "automatic": "ask-then-do-it:ask-then-do-it",
    "explicit-claude-5": "ask-then-do-it:ask-then-do-it-5",
}
FAILURE_DISCLOSURE_CODES = {
    "command-identity-invalid",
    "internal-error",
    "invalid-hook-input",
    "mapping-invalid",
    "node-too-old",
    "state-indeterminate",
    "state-invalid",
    "state-missing",
    "state-ownership-mismatch",
    "state-pending",
    "state-read-failed",
    "state-schema-unsupported",
    "state-stale",
    "state-write-failed",
    "transition-invalid",
    "unsupported-model",
}


def run_router(
    action: str,
    event: dict[str, object],
    plugin_data: Path,
    plugin: Path = PLUGIN,
) -> subprocess.CompletedProcess[str]:
    node = shutil.which("node")
    if node is None:
        raise unittest.SkipTest("Node.js is required for the Claude router tests")
    environment = os.environ.copy()
    environment.update(
        {
            "CLAUDE_PLUGIN_DATA": str(plugin_data),
            "CLAUDE_PLUGIN_ROOT": str(plugin),
        }
    )
    return subprocess.run(
        [node, str(plugin / "scripts" / "router.mjs"), action],
        cwd=ROOT,
        env=environment,
        input=json.dumps(event),
        capture_output=True,
        text=True,
        check=False,
    )


def run_router_with_node_version(
    action: str,
    event: dict[str, object],
    plugin_data: Path,
    node_version: str,
    *,
    simulate_missing_is_well_formed: bool = False,
) -> subprocess.CompletedProcess[str]:
    node = shutil.which("node")
    if node is None:
        raise unittest.SkipTest("Node.js is required for the Claude router tests")
    environment = os.environ.copy()
    environment.update(
        {
            "CLAUDE_PLUGIN_DATA": str(plugin_data),
            "CLAUDE_PLUGIN_ROOT": str(PLUGIN),
        }
    )
    old_node_surface = (
        'Reflect.deleteProperty(String.prototype, "isWellFormed");'
        if simulate_missing_is_well_formed
        else ""
    )
    trusted_arguments = [action]
    if action == "user-prompt-expansion":
        trusted_arguments.append(str(event["command_name"]))
    probe = f"""
Object.defineProperty(process.versions, "node", {{ value: {json.dumps(node_version)} }});
{old_node_surface}
const {{ main }} = await import({json.dumps(ROUTER.as_uri())});
process.exitCode = await main({json.dumps(trusted_arguments)});
"""
    return subprocess.run(
        [node, "--input-type=module", "--eval", probe],
        cwd=ROOT,
        env=environment,
        input=json.dumps(event),
        capture_output=True,
        text=True,
        check=False,
    )


def session_start(session_id: str, model: str) -> dict[str, object]:
    return {
        "session_id": session_id,
        "transcript_path": "/simulated/private/transcript.jsonl",
        "cwd": "/simulated/private/project",
        "permission_mode": "default",
        "hook_event_name": "SessionStart",
        "source": "startup",
        "model": model,
    }


def expansion(session_id: str, entry: str = "automatic") -> dict[str, object]:
    command_name = PROVISIONAL_COMMAND_NAMES[entry]
    return {
        "session_id": session_id,
        "transcript_path": "/simulated/private/transcript.jsonl",
        "cwd": "/simulated/private/project",
        "permission_mode": "default",
        "hook_event_name": "UserPromptExpansion",
        "expansion_type": "slash_command",
        "command_name": command_name,
        "command_args": "private-argument",
        "command_source": "plugin",
        "prompt": f"/{command_name} private-prompt",
    }


def route_envelope(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    self_describing = json.loads(result.stdout)
    context = self_describing["hookSpecificOutput"]["additionalContext"]
    lines = context.splitlines()
    if lines[0] != "ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1" or lines[-1] != "END_ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1":
        raise AssertionError(f"Unexpected route envelope framing: {context!r}")
    return json.loads("\n".join(lines[1:-1]))


class ClaudeRouterContractTests(unittest.TestCase):
    def test_two_sessions_route_independently(self) -> None:
        self.assertTrue(ROUTER.is_file(), "production Claude router is missing")
        self.assertTrue(MAPPING.is_file(), "production exact model mapping is missing")

        with tempfile.TemporaryDirectory(prefix="claude router ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            sessions = {
                "session-A/private": ("claude-sonnet-5", "claude-5"),
                "session-B/private": ("claude-sonnet-4-6", "general"),
            }
            observed: dict[str, tuple[dict[str, object], dict[str, object], Path]] = {}

            for session_id, (model, expected_profile) in sessions.items():
                started = run_router("session-start", session_start(session_id, model), plugin_data)
                self.assertEqual(started.returncode, 0, started.stderr)
                self.assertEqual(started.stdout, "")

                routed = run_router(
                    "user-prompt-expansion",
                    expansion(session_id),
                    plugin_data,
                )
                self.assertEqual(routed.returncode, 0, routed.stderr)
                envelope = route_envelope(routed)
                self.assertEqual(envelope["routing_status"], "ready")
                self.assertEqual(envelope["selected_profile"], expected_profile)

                session_key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
                state_path = plugin_data / "routing" / "v1" / "sessions" / f"{session_key}.json"
                self.assertTrue(state_path.is_file())
                state = json.loads(state_path.read_text(encoding="utf-8"))
                self.assertEqual(state["session_key"], session_key)
                self.assertEqual(state["operation"]["operation_id"], envelope["operation_id"])
                observed[session_id] = (envelope, state, state_path)

            self.assertNotEqual(
                observed["session-A/private"][0]["operation_id"],
                observed["session-B/private"][0]["operation_id"],
            )
            for session_id, (envelope, state, state_path) in observed.items():
                serialized = json.dumps(
                    {"envelope": envelope, "state": state, "path": str(state_path)},
                    ensure_ascii=False,
                )
                self.assertNotIn(session_id, serialized)
                self.assertNotIn("private-prompt", serialized)
                self.assertNotIn("private-argument", serialized)
                self.assertNotIn("/simulated/private", serialized)

    def test_exact_mapping_and_complete_route_table(self) -> None:
        mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
        self.assertEqual(mapping["schema_version"], 1)
        self.assertEqual(mapping["release_version"], "1.4.0-preview.1")
        self.assertEqual(mapping["evidence_checked_on"], "2026-09-07")
        self.assertEqual(mapping["lookup_mode"], "exact")
        self.assertEqual(mapping["unknown_classification"], "unknown")
        classifications = mapping["classifications"]
        self.assertEqual(len(classifications), 30)
        self.assertEqual(
            {value: list(classifications.values()).count(value) for value in set(classifications.values())},
            {"claude-5": 4, "supported-non-5": 4, "unsupported": 22},
        )
        for active_but_below_minimum in (
            "claude-opus-4-5-20251101",
            "claude-sonnet-4-5-20250929",
            "claude-haiku-4-5-20251001",
        ):
            self.assertEqual(classifications[active_but_below_minimum], "unsupported")

        cases = (
            ("claude-sonnet-5", "automatic", "claude-5", "claude-5", "none"),
            ("claude-sonnet-5", "explicit-claude-5", "claude-5", "claude-5", "none"),
            ("claude-opus-4-8", "automatic", "supported-non-5", "general", "none"),
            (
                "claude-opus-4-8",
                "explicit-claude-5",
                "supported-non-5",
                "general",
                "non-claude-5-explicit-general",
            ),
            (
                "custom-gateway/claude-opus-5",
                "automatic",
                "unknown",
                "general",
                "unknown-model-general-compatibility",
            ),
            (
                "custom-gateway/claude-opus-5",
                "explicit-claude-5",
                "unknown",
                "claude-5",
                "unknown-model-explicit-claude-5",
            ),
        )
        with tempfile.TemporaryDirectory(prefix="claude route matrix ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            for index, (model, entry, classification, profile, disclosure) in enumerate(cases):
                with self.subTest(model=model, entry=entry):
                    session_id = f"matrix-session-{index}"
                    started = run_router("session-start", session_start(session_id, model), plugin_data)
                    self.assertEqual(started.returncode, 0, started.stderr)
                    routed = run_router(
                        "user-prompt-expansion",
                        expansion(session_id, entry),
                        plugin_data,
                    )
                    self.assertEqual(routed.returncode, 0, routed.stderr)
                    envelope = route_envelope(routed)
                    self.assertEqual(envelope["version"], "1.4.0-preview.1")
                    self.assertEqual(
                        set(envelope),
                        {
                            "plugin",
                            "version",
                            "entry",
                            "operation_id",
                            "model_classification",
                            "selected_profile",
                            "routing_status",
                            "disclosure_code",
                        },
                    )
                    self.assertEqual(envelope["model_classification"], classification)
                    self.assertEqual(envelope["selected_profile"], profile)
                    self.assertEqual(envelope["disclosure_code"], disclosure)
                    self.assertEqual(envelope["routing_status"], "ready")
                    self.assertRegex(envelope["operation_id"], r"^op_[0-9a-f]{32}$")

            for index, entry in enumerate(PROVISIONAL_COMMAND_NAMES):
                with self.subTest(model="below-minimum", entry=entry):
                    session_id = f"unsupported-session-{index}"
                    started = run_router(
                        "session-start",
                        session_start(session_id, "claude-haiku-4-5-20251001"),
                        plugin_data,
                    )
                    self.assertEqual(started.returncode, 0, started.stderr)
                    routed = run_router(
                        "user-prompt-expansion",
                        expansion(session_id, entry),
                        plugin_data,
                    )
                    envelope = route_envelope(routed)
                    self.assertEqual(envelope["version"], "1.4.0-preview.1")
                    self.assertEqual(envelope["routing_status"], "failure")
                    self.assertEqual(envelope["model_classification"], "unsupported")
                    self.assertEqual(envelope["disclosure_code"], "unsupported-model")
                    self.assertIsNone(envelope["operation_id"])
                    self.assertIsNone(envelope["selected_profile"])
                    key = hashlib.sha256(session_id.encode()).hexdigest()
                    state = json.loads(
                        (plugin_data / "routing" / "v1" / "sessions" / f"{key}.json").read_text(
                            encoding="utf-8"
                        )
                    )
                    self.assertIsNone(state["operation"])

    def test_four_synchronous_exec_form_hooks_are_wired_to_the_router(self) -> None:
        self.assertTrue(HOOKS.is_file(), "production Claude hooks.json is missing")
        value = json.loads(HOOKS.read_text(encoding="utf-8"))
        self.assertEqual(set(value), {"description", "hooks"})
        hooks = value["hooks"]
        self.assertEqual(
            set(hooks),
            {"SessionStart", "PreModelSwitch", "PostModelSwitch", "UserPromptExpansion"},
        )
        expected = {
            "SessionStart": [("startup|resume|clear|compact|fork", ["session-start"])],
            "PreModelSwitch": [("", ["pre-model-switch"])],
            "PostModelSwitch": [("", ["post-model-switch"])],
            "UserPromptExpansion": [
                (
                    "^ask-then-do-it:ask-then-do-it$",
                    ["user-prompt-expansion", "ask-then-do-it:ask-then-do-it"],
                ),
                (
                    "^ask-then-do-it:ask-then-do-it-5$",
                    ["user-prompt-expansion", "ask-then-do-it:ask-then-do-it-5"],
                ),
            ],
        }
        for event_name, groups in expected.items():
            self.assertEqual(len(hooks[event_name]), len(groups))
            for actual, (matcher, trailing_args) in zip(hooks[event_name], groups, strict=True):
                self.assertEqual(set(actual), {"matcher", "hooks"})
                self.assertEqual(actual["matcher"], matcher)
                self.assertEqual(len(actual["hooks"]), 1)
                handler = actual["hooks"][0]
                self.assertEqual(set(handler), {"type", "command", "args", "timeout"})
                self.assertEqual(handler["type"], "command")
                self.assertEqual(handler["command"], "node")
                self.assertEqual(
                    handler["args"],
                    ["${CLAUDE_PLUGIN_ROOT}/scripts/router.mjs", *trailing_args],
                )
                self.assertIsInstance(handler["timeout"], int)
                self.assertGreater(handler["timeout"], 0)
                self.assertNotIn("async", handler)
                self.assertNotIn("shell", handler)

    def test_public_skills_define_the_exact_envelope_union_and_only_manual_fallback(self) -> None:
        automatic = (PLUGIN / "skills" / "ask-then-do-it" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        explicit = (PLUGIN / "skills" / "ask-then-do-it-5" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for body, entry in (
            (automatic, "/ask-then-do-it:ask-then-do-it"),
            (explicit, "/ask-then-do-it:ask-then-do-it-5"),
        ):
            with self.subTest(entry=entry):
                self.assertIn('`plugin` must equal `ask-then-do-it`', body)
                self.assertIn('`version` must equal `1.4.0-preview.1`', body)
                self.assertIn(f'`entry` must equal `{entry}`', body)
                self.assertIn("ready envelope", body)
                self.assertIn("failure envelope", body)
                self.assertIn("`operation_id: null`", body)
                self.assertIn("`selected_profile: null`", body)
                self.assertIn("contains unknown fields", body)
                self.assertIn("selected profile only", body)
                self.assertIn("Preserve the active model", body)
                for code in FAILURE_DISCLOSURE_CODES:
                    self.assertIn(f"`{code}`", body)

        self.assertIn("Stop for every failure envelope", automatic)
        self.assertNotIn("manual optimized fallback", automatic)
        self.assertIn("`node-too-old`", explicit)
        self.assertIn("manual optimized fallback", explicit)
        self.assertIn("Claude Code `2.1.251+`", explicit)
        self.assertIn("Node is genuinely missing", explicit)
        self.assertIn("Node `22+`", explicit)
        self.assertIn("stop for every other failure", explicit.lower())

    def test_node_22_minimum_uses_the_same_pure_gate_as_the_cli(self) -> None:
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js is required for the Claude router tests")
        probe = f"""
import {{ checkNodeVersion }} from {json.dumps(ROUTER.as_uri())};
const results = [];
for (const version of ["21.9.0", "22.0.0", "24.1.2", "invalid"]) {{
  try {{ checkNodeVersion(version); results.push([version, "supported"]); }}
  catch (error) {{ results.push([version, error.code]); }}
}}
console.log(JSON.stringify(results));
"""
        result = subprocess.run(
            [node, "--input-type=module", "--eval", probe],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            [
                ["21.9.0", "node-too-old"],
                ["22.0.0", "supported"],
                ["24.1.2", "supported"],
                ["invalid", "node-too-old"],
            ],
        )

    def test_node_21_failure_envelope_preserves_the_explicit_entry_identity(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude node 21 ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            result = run_router_with_node_version(
                "user-prompt-expansion",
                expansion("node-21-explicit-session", "explicit-claude-5"),
                plugin_data,
                "21.9.0",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            envelope = route_envelope(result)
            self.assertEqual(envelope["entry"], "/ask-then-do-it:ask-then-do-it-5")
            self.assertEqual(envelope["routing_status"], "failure")
            self.assertEqual(envelope["disclosure_code"], "node-too-old")
            self.assertIsNone(envelope["operation_id"])
            self.assertFalse(plugin_data.exists())

    def test_node_21_gate_precedes_plugin_data_access_for_all_actions(self) -> None:
        switch = lambda event_name: {
            "session_id": f"node-21-{event_name}",
            "transcript_path": "/simulated/private/transcript.jsonl",
            "cwd": "/simulated/private/project",
            "permission_mode": "default",
            "hook_event_name": event_name,
            "from_model": "claude-sonnet-4-6",
            "to_model": "claude-sonnet-5",
            "requested_model": "claude-sonnet-5",
            "source": "command",
        }
        cases = (
            ("session-start", session_start("node-21-session-start", "claude-sonnet-4-6")),
            (
                "user-prompt-expansion",
                expansion("node-21-explicit-no-state", "explicit-claude-5"),
            ),
            ("pre-model-switch", switch("PreModelSwitch")),
            ("post-model-switch", switch("PostModelSwitch")),
        )

        for action, event in cases:
            with self.subTest(action=action):
                with tempfile.TemporaryDirectory(prefix=f"claude node 21 {action} ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    result = run_router_with_node_version(
                        action,
                        event,
                        plugin_data,
                        "21.9.0",
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    if action == "user-prompt-expansion":
                        envelope = route_envelope(result)
                        self.assertEqual(
                            envelope["entry"],
                            "/ask-then-do-it:ask-then-do-it-5",
                        )
                        self.assertEqual(envelope["routing_status"], "failure")
                        self.assertEqual(envelope["disclosure_code"], "node-too-old")
                    elif action == "pre-model-switch":
                        warning = json.loads(result.stdout)
                        self.assertIn("not denied or changed", warning["systemMessage"])
                        self.assertNotIn("decision", warning)
                    elif action == "post-model-switch":
                        warning = json.loads(result.stdout)
                        self.assertIn("routing state warning", warning["systemMessage"])
                        self.assertIn("Stop both public entries", warning["hookSpecificOutput"]["additionalContext"])
                        self.assertNotIn("decision", warning)
                    else:
                        self.assertEqual(result.stdout, "")
                    self.assertFalse(
                        plugin_data.exists(),
                        "Node <22 must not access or persist CLAUDE_PLUGIN_DATA",
                    )

    def test_node_18_and_19_api_surface_preserves_explicit_node_too_old_failure(self) -> None:
        for node_version in ("18.20.8", "19.9.0"):
            with self.subTest(node_version=node_version):
                with tempfile.TemporaryDirectory(prefix="claude old node surface ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    result = run_router_with_node_version(
                        "user-prompt-expansion",
                        expansion("old-node-explicit-session", "explicit-claude-5"),
                        plugin_data,
                        node_version,
                        simulate_missing_is_well_formed=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    envelope = route_envelope(result)
                    self.assertEqual(
                        envelope["entry"],
                        "/ask-then-do-it:ask-then-do-it-5",
                    )
                    self.assertEqual(envelope["routing_status"], "failure")
                    self.assertEqual(envelope["disclosure_code"], "node-too-old")
                    self.assertIsNone(envelope["operation_id"])
                    self.assertFalse(plugin_data.exists())

    def test_explicit_entry_identity_is_preserved_for_state_failures(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude explicit failure ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            result = run_router(
                "user-prompt-expansion",
                expansion("missing-explicit-session", "explicit-claude-5"),
                plugin_data,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            envelope = route_envelope(result)
            self.assertEqual(envelope["entry"], "/ask-then-do-it:ask-then-do-it-5")
            self.assertEqual(envelope["routing_status"], "failure")
            self.assertEqual(envelope["disclosure_code"], "state-missing")

            malformed = expansion("invalid-explicit-session", "explicit-claude-5")
            malformed["session_id"] = 42
            result = run_router("user-prompt-expansion", malformed, plugin_data)
            envelope = route_envelope(result)
            self.assertEqual(envelope["entry"], "/ask-then-do-it:ask-then-do-it-5")
            self.assertEqual(envelope["disclosure_code"], "invalid-hook-input")


if __name__ == "__main__":
    unittest.main()
