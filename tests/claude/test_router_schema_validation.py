from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from tests.claude.test_router_contract import expansion, route_envelope, run_router
from tests.claude.test_router_state import (
    STATE_KEYS,
    lifecycle_event,
    load_state,
    state_path,
    switch_event,
)


class ClaudeRouterSchemaValidationTests(unittest.TestCase):
    def _start_ready_session(self, plugin_data: Path, session_id: str) -> bytes:
        result = run_router(
            "session-start",
            lifecycle_event(session_id, "startup", "claude-sonnet-5"),
            plugin_data,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        return state_path(plugin_data, session_id).read_bytes()

    def _assert_expansion_schema_failure(
        self,
        plugin_data: Path,
        session_id: str,
        event: dict[str, object],
        baseline: bytes,
    ) -> None:
        result = run_router("user-prompt-expansion", event, plugin_data)
        self.assertEqual(result.returncode, 0, result.stderr)
        envelope = route_envelope(result)
        self.assertEqual(envelope["routing_status"], "failure")
        self.assertEqual(envelope["disclosure_code"], "invalid-hook-input")
        self.assertIsNone(envelope["operation_id"])
        self.assertEqual(state_path(plugin_data, session_id).read_bytes(), baseline)

    def test_common_optional_fields_reject_wrong_types_and_invalid_effort(self) -> None:
        cases = (
            ("prompt-id-type", "prompt_id", 7),
            ("transcript-path-type", "transcript_path", []),
            ("cwd-type", "cwd", {}),
            ("permission-mode-type", "permission_mode", False),
            ("agent-id-type", "agent_id", 7),
            ("agent-type-type", "agent_type", None),
            ("effort-type", "effort", "high"),
            ("effort-missing-level", "effort", {}),
            ("effort-level-enum", "effort", {"level": "ultra"}),
            (
                "effort-extra-field",
                "effort",
                {"level": "high", "unexpected": True},
            ),
        )
        for label, field, invalid_value in cases:
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(prefix="claude common schema ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"common-schema-{label}"
                    baseline = self._start_ready_session(plugin_data, session_id)
                    event = expansion(session_id)
                    event[field] = invalid_value
                    self._assert_expansion_schema_failure(
                        plugin_data,
                        session_id,
                        event,
                        baseline,
                    )

    def test_session_start_optional_fields_reject_wrong_types_without_state_change(self) -> None:
        cases = (
            ("model", 7),
            ("session_title", 7),
            ("seconds_since_last_response", "1"),
            ("context_tokens", True),
            ("prompt_cache_likely_expired", 1),
            ("estimated_cache_write_usd", None),
        )
        for field, invalid_value in cases:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory(prefix="claude start schema ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"start-schema-{field}"
                    baseline = self._start_ready_session(plugin_data, session_id)
                    event = lifecycle_event(
                        session_id,
                        "clear",
                        "claude-opus-4-8",
                    )
                    event[field] = invalid_value

                    result = run_router("session-start", event, plugin_data)

                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, "")
                    self.assertEqual(
                        state_path(plugin_data, session_id).read_bytes(),
                        baseline,
                    )

    def test_expansion_fields_reject_wrong_types_and_unknown_expansion_type(self) -> None:
        cases = (
            ("expansion-type-type", "expansion_type", 7),
            ("expansion-type-enum", "expansion_type", "tool"),
            ("command-name-type", "command_name", []),
            ("command-args-type", "command_args", None),
            ("command-source-type", "command_source", False),
            ("prompt-type", "prompt", {}),
        )
        for label, field, invalid_value in cases:
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(prefix="claude expansion schema ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"expansion-schema-{label}"
                    baseline = self._start_ready_session(plugin_data, session_id)
                    event = expansion(session_id)
                    event[field] = invalid_value
                    self._assert_expansion_schema_failure(
                        plugin_data,
                        session_id,
                        event,
                        baseline,
                    )

    def test_switch_optional_fields_reject_wrong_types_and_enums_before_pre_commit(self) -> None:
        cases = (
            ("requested-model-type", "requested_model", []),
            ("context-tokens-type", "context_tokens", "123"),
            ("prompt-cache-warm-type", "prompt_cache_warm", 1),
            ("cache-ttl-type", "cache_ttl", 5),
            ("cache-ttl-enum", "cache_ttl", "24h"),
            ("cache-write-usd-type", "estimated_cache_write_usd", False),
            ("pricing-type", "pricing", []),
            ("pricing-enum", "pricing", "dynamic"),
        )
        for label, field, invalid_value in cases:
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(prefix="claude pre schema ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"pre-schema-{label}"
                    baseline = self._start_ready_session(plugin_data, session_id)
                    event = switch_event(
                        session_id,
                        "PreModelSwitch",
                        "claude-sonnet-5",
                        "claude-opus-5",
                        "command",
                    )
                    event[field] = invalid_value

                    result = run_router("pre-model-switch", event, plugin_data)

                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(
                        state_path(plugin_data, session_id).read_bytes(),
                        baseline,
                    )
                    output = json.loads(result.stdout)
                    self.assertIn("systemMessage", output)
                    self.assertIn("not denied or changed", output["systemMessage"])
                    self.assertNotIn("decision", output)

    def test_locatable_invalid_post_schema_writes_only_canonical_indeterminate_state(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="claude post schema state ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "post-schema-canonical-state"
            self._start_ready_session(plugin_data, session_id)
            initial = route_envelope(
                run_router(
                    "user-prompt-expansion",
                    expansion(session_id),
                    plugin_data,
                )
            )
            self.assertEqual(initial["routing_status"], "ready")
            before = load_state(plugin_data, session_id)
            self.assertIsNotNone(before["operation"])
            event = switch_event(
                session_id,
                "PostModelSwitch",
                "claude-sonnet-5",
                "claude-3-7-sonnet-20250219",
                "auto",
            )
            event["pricing"] = "dynamic"

            failed_post = run_router("post-model-switch", event, plugin_data)

            self.assertEqual(failed_post.returncode, 0, failed_post.stderr)
            warning = json.loads(failed_post.stdout)
            self.assertIn("synchronization failed", warning["systemMessage"])
            self.assertNotIn("decision", warning)
            self.assertNotIn("permissionDecision", failed_post.stdout)

            pathname = state_path(plugin_data, session_id)
            failed_state = load_state(plugin_data, session_id)
            self.assertEqual(set(failed_state), STATE_KEYS)
            self.assertEqual(failed_state["routing_status"], "indeterminate")
            self.assertEqual(
                failed_state["model_generation"],
                before["model_generation"],
            )
            self.assertIsNone(failed_state["model_id"])
            self.assertEqual(failed_state["model_classification"], "unknown")
            self.assertIsNone(failed_state["model_observed_from"])
            self.assertIsNone(failed_state["pending_switch"])
            self.assertEqual(failed_state["operation"], before["operation"])
            self.assertEqual(
                sorted(item.name for item in pathname.parent.iterdir()),
                [pathname.name],
            )

            for entry in ("automatic", "explicit-claude-5"):
                with self.subTest(entry=entry):
                    blocked = route_envelope(
                        run_router(
                            "user-prompt-expansion",
                            expansion(session_id, entry),
                            plugin_data,
                        )
                    )

                    self.assertEqual(blocked["routing_status"], "failure")
                    self.assertEqual(blocked["disclosure_code"], "state-indeterminate")
                    self.assertIsNone(blocked["operation_id"])
                    self.assertIsNone(blocked["selected_profile"])
                    self.assertEqual(load_state(plugin_data, session_id), failed_state)
                    self.assertEqual(
                        sorted(item.name for item in pathname.parent.iterdir()),
                        [pathname.name],
                    )

    def test_full_session_start_optional_payload_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude valid start schema ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "valid-full-session-start"
            event = lifecycle_event(session_id, "startup", "claude-sonnet-5")
            event.update(
                {
                    "prompt_id": "prompt-1",
                    "effort": {"level": "high"},
                    "agent_id": "agent-1",
                    "agent_type": "main",
                    "session_title": "Schema validation",
                    "seconds_since_last_response": 0.25,
                    "context_tokens": 123.5,
                    "prompt_cache_likely_expired": False,
                    "estimated_cache_write_usd": 0.0,
                }
            )

            result = run_router("session-start", event, plugin_data)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            state = load_state(plugin_data, session_id)
            self.assertEqual(state["routing_status"], "ready")
            self.assertEqual(state["model_classification"], "claude-5")

    def test_all_documented_effort_levels_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude valid effort schema ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "valid-effort-levels"
            self._start_ready_session(plugin_data, session_id)
            for level in ("low", "medium", "high", "xhigh", "max"):
                with self.subTest(level=level):
                    event = expansion(session_id)
                    event.update(
                        {
                            "prompt_id": f"prompt-{level}",
                            "effort": {"level": level},
                            "agent_id": "agent-1",
                            "agent_type": "main",
                        }
                    )
                    envelope = route_envelope(
                        run_router("user-prompt-expansion", event, plugin_data)
                    )
                    self.assertEqual(envelope["routing_status"], "ready")
                    self.assertEqual(envelope["disclosure_code"], "none")

    def test_documented_switch_enums_and_nullable_requested_model_are_accepted(self) -> None:
        cases = (
            ("5m", "configured", None),
            ("1h", "catalog", "claude-opus-5"),
            ("5m", "default", "opus"),
        )
        for index, (cache_ttl, pricing, requested_model) in enumerate(cases):
            with self.subTest(
                cache_ttl=cache_ttl,
                pricing=pricing,
                requested_model=requested_model,
            ):
                with tempfile.TemporaryDirectory(prefix="claude valid switch schema ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"valid-switch-enums-{index}"
                    self._start_ready_session(plugin_data, session_id)
                    for action, event_name in (
                        ("pre-model-switch", "PreModelSwitch"),
                        ("post-model-switch", "PostModelSwitch"),
                    ):
                        event = switch_event(
                            session_id,
                            event_name,
                            "claude-sonnet-5",
                            "claude-opus-5",
                            "command",
                        )
                        event.update(
                            {
                                "requested_model": requested_model,
                                "cache_ttl": cache_ttl,
                                "pricing": pricing,
                                "effort": {"level": "max"},
                            }
                        )
                        result = run_router(action, event, plugin_data)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertEqual(result.stdout, "")
                    state = load_state(plugin_data, session_id)
                    self.assertEqual(state["routing_status"], "ready")
                    self.assertEqual(state["model_id"], "claude-opus-5")

    def test_mcp_prompt_is_schema_valid_but_not_a_supported_public_route(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude mcp prompt schema ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "schema-valid-mcp-prompt"
            baseline = self._start_ready_session(plugin_data, session_id)
            event = expansion(session_id)
            event["expansion_type"] = "mcp_prompt"

            result = run_router("user-prompt-expansion", event, plugin_data)

            self.assertEqual(result.returncode, 0, result.stderr)
            envelope = route_envelope(result)
            self.assertEqual(envelope["routing_status"], "failure")
            self.assertEqual(envelope["disclosure_code"], "command-identity-invalid")
            self.assertIsNone(envelope["operation_id"])
            self.assertEqual(state_path(plugin_data, session_id).read_bytes(), baseline)


if __name__ == "__main__":
    unittest.main()
