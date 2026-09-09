from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from tests.claude.test_router_contract import (
    PLUGIN,
    ROUTER,
    expansion,
    route_envelope,
    run_router,
)
from tests.claude.test_router_state import (
    lifecycle_event,
    load_state,
    state_path,
    switch_event,
)


def run_router_raw(action: str, source: str, plugin_data: Path) -> subprocess.CompletedProcess[str]:
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
    return subprocess.run(
        [node, str(ROUTER), action],
        cwd=PLUGIN,
        env=environment,
        input=source,
        capture_output=True,
        text=True,
        check=False,
    )


class ClaudeRouterSecurityTests(unittest.TestCase):
    def assert_marker_is_absent_from_persistence_and_output(
        self,
        plugin_data: Path,
        marker: str,
        *results: subprocess.CompletedProcess[str],
    ) -> None:
        encoded_marker = marker.encode("utf-8")
        for result in results:
            self.assertNotIn(marker, result.stdout)
        if plugin_data.exists():
            for pathname in plugin_data.rglob("*"):
                if pathname.is_file():
                    self.assertNotIn(
                        encoded_marker,
                        pathname.read_bytes(),
                        f"secret marker persisted in {pathname}",
                    )

    def test_untrusted_hook_input_fails_closed_without_changing_valid_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude invalid input ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "security-session"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                plugin_data,
            )
            pathname = state_path(plugin_data, session_id)
            baseline = pathname.read_bytes()
            valid = expansion(session_id)
            unknown_field = {**valid, "unexpected": "secret-unknown-value"}
            wrong_type = {**valid, "session_id": 42}
            wrong_source = {**valid, "command_source": "project"}
            cases = (
                ("invalid-json", "{", "invalid-hook-input"),
                (
                    "duplicate-key",
                    json.dumps(valid)[:-1] + ',"session_id":"another-session"}',
                    "invalid-hook-input",
                ),
                ("unknown-field", json.dumps(unknown_field), "invalid-hook-input"),
                ("wrong-type", json.dumps(wrong_type), "invalid-hook-input"),
                ("wrong-source", json.dumps(wrong_source), "command-identity-invalid"),
                ("oversized", json.dumps({**valid, "prompt": "x" * 70_000}), "invalid-hook-input"),
            )
            for label, raw, expected_code in cases:
                with self.subTest(label=label):
                    result = run_router_raw("user-prompt-expansion", raw, plugin_data)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    envelope = route_envelope(result)
                    self.assertEqual(envelope["routing_status"], "failure")
                    self.assertEqual(envelope["disclosure_code"], expected_code)
                    self.assertIsNone(envelope["operation_id"])
                    self.assertEqual(pathname.read_bytes(), baseline)
                    self.assertNotIn("secret-unknown-value", result.stdout)
                    self.assertNotIn("security-session", result.stdout)

    def test_router_declares_no_secondary_durable_post_state_path(self) -> None:
        legacy_suffix = "." + "post" + "-" + "failure"
        router_source = ROUTER.read_text(encoding="utf-8")

        self.assertFalse(
            legacy_suffix in router_source,
            "legacy secondary durable Post state suffix remains",
        )

    def test_state_schema_corruption_and_ownership_mismatch_are_rejected(self) -> None:
        mutations = {
            "unknown-key": (lambda value: value.update({"unexpected": True}), "state-invalid"),
            "unsupported-schema": (
                lambda value: value.update({"schema_version": 2}),
                "state-schema-unsupported",
            ),
            "ownership-mismatch": (
                lambda value: value.update({"session_key": "0" * 64}),
                "state-ownership-mismatch",
            ),
            "negative-generation": (
                lambda value: value.update({"model_generation": -1}),
                "state-invalid",
            ),
            "invalid-calendar-timestamp": (
                lambda value: value.update({"updated_at": "2026-99-01T00:00:00.000Z"}),
                "state-invalid",
            ),
        }
        for label, (mutate, expected_code) in mutations.items():
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(prefix="claude corrupt state ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"corrupt-{label}"
                    run_router(
                        "session-start",
                        lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                        plugin_data,
                    )
                    pathname = state_path(plugin_data, session_id)
                    state = json.loads(pathname.read_text(encoding="utf-8"))
                    mutate(state)
                    pathname.write_text(json.dumps(state), encoding="utf-8")
                    result = run_router(
                        "user-prompt-expansion", expansion(session_id), plugin_data
                    )
                    envelope = route_envelope(result)
                    self.assertEqual(envelope["routing_status"], "failure")
                    self.assertEqual(envelope["disclosure_code"], expected_code)
                    self.assertIsNone(envelope["operation_id"])

    def test_invalid_model_identifiers_and_operation_tuples_are_rejected(self) -> None:
        mutations = {
            "empty-model": lambda value: value.update({"model_id": ""}),
            "control-model": lambda value: value.update({"model_id": "claude\nmodel"}),
            "unpaired-surrogate-model": lambda value: value.update({"model_id": "\ud800"}),
            "automatic-wrong-profile": lambda value: value["operation"].update(
                {"bound_profile": "general"}
            ),
            "unsupported-operation": lambda value: value["operation"].update(
                {"bound_classification": "unsupported", "bound_profile": "general"}
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(prefix="claude invalid state tuple ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"invalid-tuple-{label}"
                    run_router(
                        "session-start",
                        lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                        plugin_data,
                    )
                    route_envelope(
                        run_router("user-prompt-expansion", expansion(session_id), plugin_data)
                    )
                    pathname = state_path(plugin_data, session_id)
                    state = json.loads(pathname.read_text(encoding="utf-8"))
                    mutate(state)
                    pathname.write_text(
                        json.dumps(state, ensure_ascii=True), encoding="utf-8"
                    )

                    result = run_router(
                        "user-prompt-expansion", expansion(session_id), plugin_data
                    )
                    envelope = route_envelope(result)
                    self.assertEqual(envelope["routing_status"], "failure")
                    self.assertEqual(envelope["disclosure_code"], "state-invalid")
                    self.assertIsNone(envelope["operation_id"])

    def test_stale_same_session_state_is_not_routed_or_resumed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude stale same session ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "stale-same-session"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                plugin_data,
            )
            pathname = state_path(plugin_data, session_id)
            state = json.loads(pathname.read_text(encoding="utf-8"))
            state["updated_at"] = "2000-01-01T00:00:00.000Z"
            pathname.write_text(json.dumps(state), encoding="utf-8")
            stale_bytes = pathname.read_bytes()

            routed = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            self.assertEqual(routed["routing_status"], "failure")
            self.assertEqual(routed["disclosure_code"], "state-stale")
            self.assertIsNone(routed["operation_id"])
            self.assertEqual(pathname.read_bytes(), stale_bytes)

            resumed = run_router(
                "session-start", lifecycle_event(session_id, "resume"), plugin_data
            )
            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            self.assertEqual(resumed.stdout, "")
            self.assertEqual(pathname.read_bytes(), stale_bytes)

            compacted = run_router(
                "session-start", lifecycle_event(session_id, "compact"), plugin_data
            )
            self.assertEqual(compacted.returncode, 0, compacted.stderr)
            self.assertEqual(compacted.stdout, "")
            self.assertEqual(pathname.read_bytes(), stale_bytes)

            cleared = run_router(
                "session-start", lifecycle_event(session_id, "clear"), plugin_data
            )
            self.assertEqual(cleared.returncode, 0, cleared.stderr)
            reset = load_state(plugin_data, session_id)
            self.assertEqual(reset["session_source"], "clear")
            self.assertEqual(
                reset["model_generation"], state["model_generation"] + 1
            )
            self.assertGreater(reset["model_generation"], state["model_generation"])
            self.assertEqual(reset["model_classification"], "unknown")
            self.assertIsNone(reset["operation"])

    def test_invalid_hook_model_identifiers_fail_closed_with_safe_state_transitions(
        self,
    ) -> None:
        invalid_models = ("", "claude\nmodel", "\ud800")
        for index, invalid_model in enumerate(invalid_models):
            with self.subTest(action="session-start", model=repr(invalid_model)):
                with tempfile.TemporaryDirectory(prefix="claude invalid event model ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"invalid-start-{index}"
                    event = lifecycle_event(
                        session_id, "startup", "temporary-valid-model"
                    )
                    event["model"] = invalid_model
                    result = run_router(
                        "session-start",
                        event,
                        plugin_data,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertFalse(state_path(plugin_data, session_id).exists())

            for action, event_name, field in (
                ("pre-model-switch", "PreModelSwitch", "from_model"),
                ("post-model-switch", "PostModelSwitch", "to_model"),
            ):
                with self.subTest(action=action, model=repr(invalid_model)):
                    with tempfile.TemporaryDirectory(prefix="claude invalid switch model ") as temporary:
                        plugin_data = Path(temporary) / "plugin data"
                        session_id = f"invalid-switch-{action}-{index}"
                        run_router(
                            "session-start",
                            lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                            plugin_data,
                        )
                        pathname = state_path(plugin_data, session_id)
                        baseline = pathname.read_bytes()
                        event = {
                            "session_id": session_id,
                            "hook_event_name": event_name,
                            "from_model": "claude-sonnet-5",
                            "to_model": "claude-opus-5",
                            "source": "command",
                        }
                        event[field] = invalid_model
                        result = run_router(action, event, plugin_data)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        if action == "pre-model-switch":
                            self.assertEqual(pathname.read_bytes(), baseline)
                        else:
                            failed_state = load_state(plugin_data, session_id)
                            self.assertEqual(failed_state["routing_status"], "indeterminate")
                            self.assertEqual(failed_state["model_generation"], 0)
                            self.assertIsNone(failed_state["model_id"])
                            self.assertEqual(
                                failed_state["model_classification"], "unknown"
                            )
                            self.assertIsNone(failed_state["model_observed_from"])
                            self.assertIsNone(failed_state["pending_switch"])
                            self.assertIsNone(failed_state["operation"])
                            self.assertEqual(
                                [path.name for path in pathname.parent.iterdir()],
                                [pathname.name],
                            )

    def test_unmapped_regex_shaped_session_start_model_is_unknown_without_secret_persistence(
        self,
    ) -> None:
        marker = "secretmarker-session-start-9f23d1"
        model = f"claude-tenant-{marker}"
        with tempfile.TemporaryDirectory(prefix="claude unmapped start ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "noncanonical-session-start"
            started = run_router(
                "session-start",
                lifecycle_event(session_id, "startup", model),
                plugin_data,
            )
            self.assertEqual(started.returncode, 0, started.stderr)

            routed = run_router(
                "user-prompt-expansion", expansion(session_id), plugin_data
            )
            self.assertEqual(routed.returncode, 0, routed.stderr)
            envelope = route_envelope(routed)
            self.assert_marker_is_absent_from_persistence_and_output(
                plugin_data, marker, started, routed
            )

            state = load_state(plugin_data, session_id)
            self.assertEqual(state["routing_status"], "ready")
            self.assertIsNone(state["model_id"])
            self.assertEqual(state["model_classification"], "unknown")
            self.assertEqual(envelope["routing_status"], "ready")
            self.assertEqual(envelope["model_classification"], "unknown")
            self.assertEqual(envelope["selected_profile"], "general")

    def test_unmapped_regex_shaped_pre_switch_from_model_fails_closed_without_secret_persistence(
        self,
    ) -> None:
        marker = "secretmarker-pre-switch-58a7c2"
        model = f"claude-tenant-{marker}"
        with tempfile.TemporaryDirectory(prefix="claude unmapped pre ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "noncanonical-pre-switch"
            started = run_router(
                "session-start", lifecycle_event(session_id, "startup"), plugin_data
            )
            self.assertEqual(started.returncode, 0, started.stderr)

            switched = run_router(
                "pre-model-switch",
                switch_event(
                    session_id,
                    "PreModelSwitch",
                    model,
                    "claude-sonnet-5",
                    "command",
                ),
                plugin_data,
            )
            self.assertEqual(switched.returncode, 0, switched.stderr)
            routed = run_router(
                "user-prompt-expansion", expansion(session_id), plugin_data
            )
            self.assertEqual(routed.returncode, 0, routed.stderr)
            envelope = route_envelope(routed)
            self.assert_marker_is_absent_from_persistence_and_output(
                plugin_data, marker, started, switched, routed
            )

            state = load_state(plugin_data, session_id)
            self.assertEqual(state["routing_status"], "indeterminate")
            self.assertIsNone(state["model_id"])
            self.assertEqual(state["model_classification"], "unknown")
            self.assertIsNone(state["pending_switch"])
            self.assertEqual(envelope["routing_status"], "failure")
            self.assertEqual(envelope["disclosure_code"], "state-indeterminate")
            self.assertIn("not denied or changed", switched.stdout)

    def test_unmapped_regex_shaped_post_switch_to_model_is_unknown_without_secret_persistence(
        self,
    ) -> None:
        marker = "secretmarker-post-switch-f61b04"
        model = f"claude-tenant-{marker}"
        with tempfile.TemporaryDirectory(prefix="claude unmapped post ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "noncanonical-post-switch"
            old_model = "claude-sonnet-4-6"
            started = run_router(
                "session-start",
                lifecycle_event(session_id, "startup", old_model),
                plugin_data,
            )
            self.assertEqual(started.returncode, 0, started.stderr)
            initial_result = run_router(
                "user-prompt-expansion", expansion(session_id), plugin_data
            )
            self.assertEqual(initial_result.returncode, 0, initial_result.stderr)
            initial = route_envelope(initial_result)

            switched = run_router(
                "post-model-switch",
                switch_event(
                    session_id,
                    "PostModelSwitch",
                    old_model,
                    model,
                    "auto",
                ),
                plugin_data,
            )
            self.assertEqual(switched.returncode, 0, switched.stderr)
            committed = load_state(plugin_data, session_id)
            routed = run_router(
                "user-prompt-expansion", expansion(session_id), plugin_data
            )
            self.assertEqual(routed.returncode, 0, routed.stderr)
            envelope = route_envelope(routed)
            self.assert_marker_is_absent_from_persistence_and_output(
                plugin_data, marker, started, initial_result, switched, routed
            )

            self.assertEqual(committed["routing_status"], "ready")
            self.assertIsNone(committed["model_id"])
            self.assertEqual(committed["model_classification"], "unknown")
            self.assertEqual(
                committed["operation"]["operation_id"], initial["operation_id"]
            )
            self.assertEqual(envelope["routing_status"], "ready")
            self.assertEqual(envelope["model_classification"], "unknown")
            self.assertEqual(envelope["selected_profile"], "general")

    def test_unmapped_canonical_future_model_id_remains_unknown(self) -> None:
        future_model = "claude-sonnet-6-20990101"
        with tempfile.TemporaryDirectory(prefix="claude future canonical model ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "future-canonical-model"
            started = run_router(
                "session-start",
                lifecycle_event(session_id, "startup", future_model),
                plugin_data,
            )
            self.assertEqual(started.returncode, 0, started.stderr)
            state = load_state(plugin_data, session_id)
            self.assertIsNone(state["model_id"])
            self.assertEqual(state["model_classification"], "unknown")

            routed = run_router(
                "user-prompt-expansion", expansion(session_id), plugin_data
            )
            self.assertEqual(routed.returncode, 0, routed.stderr)
            envelope = route_envelope(routed)
            self.assertEqual(envelope["routing_status"], "ready")
            self.assertEqual(envelope["model_classification"], "unknown")
            self.assertEqual(envelope["selected_profile"], "general")
            self.assert_marker_is_absent_from_persistence_and_output(
                plugin_data, future_model, started, routed
            )

    def test_release_allowlisted_model_ids_are_persisted_and_classified(self) -> None:
        cases = {
            "claude-sonnet-5": "claude-5",
            "claude-sonnet-4-6": "supported-non-5",
            "claude-sonnet-4-5-20250929": "unsupported",
        }
        for model, classification in cases.items():
            with self.subTest(model=model):
                with tempfile.TemporaryDirectory(
                    prefix="claude allowlisted model "
                ) as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"allowlisted-{classification}"
                    started = run_router(
                        "session-start",
                        lifecycle_event(session_id, "startup", model),
                        plugin_data,
                    )
                    self.assertEqual(started.returncode, 0, started.stderr)

                    state = load_state(plugin_data, session_id)
                    self.assertEqual(state["model_id"], model)
                    self.assertEqual(state["model_classification"], classification)

    def test_all_and_only_six_operation_tuples_are_valid(self) -> None:
        entries = (
            "/ask-then-do-it:ask-then-do-it",
            "/ask-then-do-it:ask-then-do-it-5",
        )
        profiles = ("general", "claude-5")
        classifications = ("claude-5", "supported-non-5", "unsupported", "unknown")
        allowed = {
            (entries[0], "claude-5", "claude-5"),
            (entries[0], "supported-non-5", "general"),
            (entries[0], "unknown", "general"),
            (entries[1], "claude-5", "claude-5"),
            (entries[1], "supported-non-5", "general"),
            (entries[1], "unknown", "claude-5"),
        }
        for entry in entries:
            for profile in profiles:
                for classification in classifications:
                    candidate_tuple = (entry, classification, profile)
                    with self.subTest(tuple=candidate_tuple):
                        with tempfile.TemporaryDirectory(prefix="claude operation tuple ") as temporary:
                            plugin_data = Path(temporary) / "plugin data"
                            session_id = "operation-tuple-session"
                            run_router(
                                "session-start",
                                lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                                plugin_data,
                            )
                            route_envelope(
                                run_router(
                                    "user-prompt-expansion", expansion(session_id), plugin_data
                                )
                            )
                            pathname = state_path(plugin_data, session_id)
                            state = json.loads(pathname.read_text(encoding="utf-8"))
                            state["operation"].update(
                                {
                                    "entry": entry,
                                    "bound_profile": profile,
                                    "bound_classification": classification,
                                }
                            )
                            pathname.write_text(json.dumps(state), encoding="utf-8")
                            envelope = route_envelope(
                                run_router(
                                    "user-prompt-expansion", expansion(session_id), plugin_data
                                )
                            )
                            expected = "ready" if candidate_tuple in allowed else "failure"
                            self.assertEqual(envelope["routing_status"], expected)

    def test_invalid_runtime_mapping_blocks_the_public_route(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude invalid runtime mapping ") as temporary:
            root = Path(temporary)
            candidate = root / "plugin"
            shutil.copytree(PLUGIN, candidate)
            plugin_data = root / "plugin data"
            session_id = "mapping-invalid-route"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                plugin_data,
                candidate,
            )
            mapping_path = candidate / "config" / "model-classifications.json"
            mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
            mapping["aliases"] = {}
            mapping_path.write_text(json.dumps(mapping), encoding="utf-8")

            envelope = route_envelope(
                run_router(
                    "user-prompt-expansion",
                    expansion(session_id),
                    plugin_data,
                    candidate,
                )
            )
            self.assertEqual(envelope["routing_status"], "failure")
            self.assertEqual(envelope["disclosure_code"], "mapping-invalid")
            self.assertIsNone(load_state(plugin_data, session_id)["operation"])

    def test_duplicate_keys_in_persisted_state_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude duplicate state ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "duplicate-state-session"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                plugin_data,
            )
            pathname = state_path(plugin_data, session_id)
            source = pathname.read_text(encoding="utf-8")
            pathname.write_text(
                source.replace('"schema_version":1', '"schema_version":2,"schema_version":1', 1),
                encoding="utf-8",
            )
            result = run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            envelope = route_envelope(result)
            self.assertEqual(envelope["routing_status"], "failure")
            self.assertEqual(envelope["disclosure_code"], "state-invalid")

    def test_successful_session_start_cleans_only_expired_regular_session_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude cleanup ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            expired_session = "expired-session"
            run_router(
                "session-start",
                lifecycle_event(expired_session, "startup", "claude-sonnet-4-6"),
                plugin_data,
            )
            expired_path = state_path(plugin_data, expired_session)
            expired_state = json.loads(expired_path.read_text(encoding="utf-8"))
            expired_state["updated_at"] = "2000-01-01T00:00:00.000Z"
            expired_path.write_text(json.dumps(expired_state), encoding="utf-8")
            unknown_file = expired_path.parent / "do-not-scan-or-delete.txt"
            unknown_file.write_text("keep", encoding="utf-8")

            current_session = "current-cleanup-session"
            started = run_router(
                "session-start",
                lifecycle_event(current_session, "startup", "claude-sonnet-5"),
                plugin_data,
            )
            self.assertEqual(started.returncode, 0, started.stderr)
            self.assertFalse(expired_path.exists())
            self.assertTrue(state_path(plugin_data, current_session).is_file())
            self.assertEqual(unknown_file.read_text(encoding="utf-8"), "keep")

    def test_cleanup_does_not_delete_a_session_while_its_lock_is_held(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude cleanup lock ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            expired_session = "locked-expired-session"
            run_router(
                "session-start",
                lifecycle_event(expired_session, "startup", "claude-sonnet-4-6"),
                plugin_data,
            )
            expired_path = state_path(plugin_data, expired_session)
            state = json.loads(expired_path.read_text(encoding="utf-8"))
            state["updated_at"] = "2000-01-01T00:00:00.000Z"
            expired_path.write_text(json.dumps(state), encoding="utf-8")
            lock_path = expired_path.with_name(f".{expired_path.name}.lock")
            lock_path.write_text("held", encoding="utf-8")

            run_router(
                "session-start",
                lifecycle_event("cleanup-lock-trigger-1", "startup", "claude-sonnet-5"),
                plugin_data,
            )
            self.assertTrue(expired_path.is_file())

            lock_path.unlink()
            run_router(
                "session-start",
                lifecycle_event("cleanup-lock-trigger-2", "startup", "claude-sonnet-5"),
                plugin_data,
            )
            self.assertFalse(expired_path.exists())

    def test_concurrent_same_session_routes_leave_one_complete_atomic_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude concurrent ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "concurrent-session"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                plugin_data,
            )

            with ThreadPoolExecutor(max_workers=8) as executor:
                results = list(
                    executor.map(
                        lambda _: run_router(
                            "user-prompt-expansion", expansion(session_id), plugin_data
                        ),
                        range(16),
                    )
                )
            envelopes = [route_envelope(result) for result in results]
            self.assertTrue(all(item["routing_status"] == "ready" for item in envelopes))
            state = load_state(plugin_data, session_id)
            self.assertEqual(set(state), {
                "schema_version", "session_key", "session_source", "routing_status",
                "model_generation", "model_id", "model_classification",
                "model_observed_from", "pending_switch", "updated_at", "operation",
            })
            self.assertIn(
                state["operation"]["operation_id"],
                {item["operation_id"] for item in envelopes},
            )
            leftovers = [
                path.name
                for path in state_path(plugin_data, session_id).parent.iterdir()
                if path.name.endswith(".tmp") or path.name.endswith(".lock")
            ]
            self.assertEqual(leftovers, [])

    def test_state_file_symlink_is_not_followed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude symlink ") as temporary:
            root = Path(temporary)
            plugin_data = root / "plugin data"
            session_id = "symlink-session"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                plugin_data,
            )
            pathname = state_path(plugin_data, session_id)
            outside = root / "outside.json"
            outside.write_bytes(pathname.read_bytes())
            pathname.unlink()
            try:
                pathname.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable on this host: {exc}")
            result = run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            envelope = route_envelope(result)
            self.assertEqual(envelope["routing_status"], "failure")
            self.assertEqual(envelope["disclosure_code"], "state-read-failed")
            self.assertEqual(outside.read_bytes(), pathname.read_bytes())

    def test_plugin_data_directory_link_is_rejected_without_writing_through_it(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude linked data ") as temporary:
            root = Path(temporary)
            outside = root / "outside data"
            outside.mkdir()
            linked = root / "linked plugin data"
            if os.name == "nt":
                node = shutil.which("node")
                if node is None:
                    self.skipTest("Node.js is unavailable")
                created = subprocess.run(
                    [
                        node,
                        "-e",
                        "require('node:fs').symlinkSync(process.argv[1], process.argv[2], 'junction')",
                        str(outside),
                        str(linked),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if created.returncode != 0:
                    self.skipTest(f"junction creation unavailable: {created.stderr}")
            else:
                linked.symlink_to(outside, target_is_directory=True)

            result = run_router(
                "session-start",
                lifecycle_event("linked-data-session", "startup", "claude-sonnet-5"),
                linked,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((outside / "routing").exists())


if __name__ == "__main__":
    unittest.main()
