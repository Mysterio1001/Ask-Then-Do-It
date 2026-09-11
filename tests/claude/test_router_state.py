from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import time
import unittest

from tests.claude.test_router_contract import (
    expansion,
    route_envelope,
    run_router,
    session_start,
)


STATE_KEYS = {
    "schema_version",
    "session_key",
    "session_source",
    "routing_status",
    "model_generation",
    "model_id",
    "model_classification",
    "model_observed_from",
    "pending_switch",
    "updated_at",
    "operation",
}
MAX_SAFE_INTEGER = (1 << 53) - 1


def state_path(plugin_data: Path, session_id: str) -> Path:
    key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
    return plugin_data / "routing" / "v1" / "sessions" / f"{key}.json"


def load_state(plugin_data: Path, session_id: str) -> dict[str, object]:
    return json.loads(state_path(plugin_data, session_id).read_text(encoding="utf-8"))


def seed_maximum_generation_state(
    plugin_data: Path,
    session_id: str,
    model: str = "claude-sonnet-4-6",
) -> None:
    started = run_router(
        "session-start",
        lifecycle_event(session_id, "startup", model),
        plugin_data,
    )
    if started.returncode != 0:
        raise AssertionError(started.stderr)
    state = load_state(plugin_data, session_id)
    state["model_generation"] = MAX_SAFE_INTEGER
    state_path(plugin_data, session_id).write_text(json.dumps(state), encoding="utf-8")


def lifecycle_event(session_id: str, source: str, model: str | None = None) -> dict[str, object]:
    event = session_start(session_id, model or "placeholder")
    event["source"] = source
    if model is None:
        del event["model"]
    return event


def switch_event(
    session_id: str,
    event_name: str,
    from_model: str,
    to_model: str,
    source: str,
) -> dict[str, object]:
    return {
        "session_id": session_id,
        "transcript_path": "/simulated/private/transcript.jsonl",
        "cwd": "/simulated/private/project",
        "permission_mode": "default",
        "hook_event_name": event_name,
        "from_model": from_model,
        "to_model": to_model,
        "requested_model": to_model if source != "auto" else None,
        "source": source,
        "context_tokens": 123,
        "prompt_cache_warm": True,
        "cache_ttl": "5m",
        "estimated_cache_write_usd": 0.01,
        "pricing": "catalog",
    }


class ClaudeRouterStateTests(unittest.TestCase):
    def assert_generation_state_remains_valid(
        self,
        plugin_data: Path,
        session_id: str,
    ) -> dict[str, object]:
        state = load_state(plugin_data, session_id)
        self.assertIs(type(state["model_generation"]), int)
        self.assertGreaterEqual(state["model_generation"], 0)
        self.assertLessEqual(state["model_generation"], MAX_SAFE_INTEGER)
        if state["pending_switch"] is not None:
            next_generation = state["pending_switch"]["next_generation"]
            self.assertIs(type(next_generation), int)
            self.assertLessEqual(next_generation, MAX_SAFE_INTEGER)

        validation = route_envelope(
            run_router("user-prompt-expansion", expansion(session_id), plugin_data)
        )
        self.assertNotEqual(validation["disclosure_code"], "state-invalid")
        return validation

    def assert_generation_exhaustion_fails_closed(
        self,
        plugin_data: Path,
        session_id: str,
    ) -> None:
        blocked = self.assert_generation_state_remains_valid(plugin_data, session_id)
        self.assertEqual(blocked["routing_status"], "failure")
        self.assertIsNone(blocked["operation_id"])
        self.assertIsNone(blocked["selected_profile"])

    def test_session_lifecycle_preserves_only_same_session_binding(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude lifecycle ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "lifecycle-session"

            started = run_router(
                "session-start",
                lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                plugin_data,
            )
            self.assertEqual(started.returncode, 0, started.stderr)
            first_route = run_router(
                "user-prompt-expansion", expansion(session_id), plugin_data
            )
            first_envelope = route_envelope(first_route)
            first_operation = first_envelope["operation_id"]

            compacted = run_router(
                "session-start", lifecycle_event(session_id, "compact"), plugin_data
            )
            self.assertEqual(compacted.returncode, 0, compacted.stderr)
            compact_context = json.loads(compacted.stdout)["hookSpecificOutput"]["additionalContext"]
            self.assertIn(first_operation, compact_context)
            self.assertIn("claude-5", compact_context)
            self.assertIn("If this operation is still in progress", compact_context)
            after_compact = load_state(plugin_data, session_id)
            self.assertEqual(after_compact["session_source"], "compact")
            self.assertEqual(after_compact["model_classification"], "claude-5")
            self.assertEqual(after_compact["operation"]["operation_id"], first_operation)

            resumed = run_router(
                "session-start", lifecycle_event(session_id, "resume"), plugin_data
            )
            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            resume_context = json.loads(resumed.stdout)["hookSpecificOutput"]["additionalContext"]
            self.assertIn(first_operation, resume_context)
            self.assertIn("claude-5", resume_context)
            after_resume = load_state(plugin_data, session_id)
            self.assertEqual(after_resume["session_source"], "resume")
            self.assertEqual(after_resume["model_classification"], "unknown")
            self.assertIsNone(after_resume["model_id"])
            self.assertEqual(after_resume["operation"]["operation_id"], first_operation)

            rerouted = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            self.assertEqual(rerouted["selected_profile"], "general")
            self.assertNotEqual(rerouted["operation_id"], first_operation)

            cleared = run_router(
                "session-start", lifecycle_event(session_id, "clear"), plugin_data
            )
            self.assertEqual(cleared.returncode, 0, cleared.stderr)
            self.assertEqual(cleared.stdout, "")
            after_clear = load_state(plugin_data, session_id)
            self.assertEqual(set(after_clear), STATE_KEYS)
            self.assertEqual(after_clear["session_source"], "clear")
            self.assertEqual(after_clear["model_classification"], "unknown")
            self.assertIsNone(after_clear["operation"])

            forked_session = "forked-lifecycle-session"
            forked = run_router(
                "session-start",
                lifecycle_event(forked_session, "fork", "claude-opus-4-8"),
                plugin_data,
            )
            self.assertEqual(forked.returncode, 0, forked.stderr)
            self.assertEqual(forked.stdout, "")
            forked_state = load_state(plugin_data, forked_session)
            self.assertEqual(forked_state["session_source"], "fork")
            self.assertEqual(forked_state["model_classification"], "supported-non-5")
            self.assertIsNone(forked_state["operation"])
            self.assertNotEqual(forked_state["session_key"], after_clear["session_key"])

    def test_compact_with_present_unmapped_model_recovers_nonready_state_as_unknown(
        self,
    ) -> None:
        for prior_status in ("pending", "indeterminate"):
            with self.subTest(prior_status=prior_status):
                with tempfile.TemporaryDirectory(
                    prefix="claude compact unmapped recovery "
                ) as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"compact-unmapped-{prior_status}"
                    old_model = "claude-sonnet-4-6"
                    started = run_router(
                        "session-start",
                        lifecycle_event(session_id, "startup", old_model),
                        plugin_data,
                    )
                    self.assertEqual(started.returncode, 0, started.stderr)
                    initial = route_envelope(
                        run_router(
                            "user-prompt-expansion",
                            expansion(session_id),
                            plugin_data,
                        )
                    )
                    from_model = (
                        old_model
                        if prior_status == "pending"
                        else "claude-opus-5"
                    )
                    pre = run_router(
                        "pre-model-switch",
                        switch_event(
                            session_id,
                            "PreModelSwitch",
                            from_model,
                            "claude-sonnet-5",
                            "command",
                        ),
                        plugin_data,
                    )
                    self.assertEqual(pre.returncode, 0, pre.stderr)
                    before_compact = load_state(plugin_data, session_id)
                    self.assertEqual(before_compact["routing_status"], prior_status)

                    compacted = run_router(
                        "session-start",
                        lifecycle_event(
                            session_id,
                            "compact",
                            "gateway/custom-model",
                        ),
                        plugin_data,
                    )

                    self.assertEqual(compacted.returncode, 0, compacted.stderr)
                    recovered = load_state(plugin_data, session_id)
                    self.assertEqual(recovered["routing_status"], "ready")
                    self.assertEqual(recovered["session_source"], "compact")
                    self.assertEqual(
                        recovered["model_generation"],
                        before_compact["model_generation"] + 1,
                    )
                    self.assertIsNone(recovered["model_id"])
                    self.assertEqual(recovered["model_classification"], "unknown")
                    self.assertIsNone(recovered["model_observed_from"])
                    self.assertIsNone(recovered["pending_switch"])
                    self.assertNotIn(
                        b"gateway/custom-model",
                        state_path(plugin_data, session_id).read_bytes(),
                    )
                    self.assertNotIn("gateway/custom-model", compacted.stdout)
                    self.assertEqual(
                        recovered["operation"]["operation_id"],
                        initial["operation_id"],
                    )

                    rerouted = route_envelope(
                        run_router(
                            "user-prompt-expansion",
                            expansion(session_id),
                            plugin_data,
                        )
                    )
                    self.assertEqual(rerouted["routing_status"], "ready")
                    self.assertEqual(rerouted["model_classification"], "unknown")
                    self.assertEqual(rerouted["selected_profile"], "general")

    def test_pre_and_post_switch_bind_current_operation_then_reroute_next_entry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude switch ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "switch-session"
            old_model = "claude-sonnet-4-6"
            new_model = "claude-sonnet-5"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", old_model),
                plugin_data,
            )
            initial = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            self.assertEqual(initial["selected_profile"], "general")

            pre = run_router(
                "pre-model-switch",
                switch_event(session_id, "PreModelSwitch", old_model, new_model, "command"),
                plugin_data,
            )
            self.assertEqual(pre.returncode, 0, pre.stderr)
            pending = load_state(plugin_data, session_id)
            self.assertEqual(pending["routing_status"], "pending")
            self.assertEqual(pending["model_generation"], 0)
            self.assertEqual(
                set(pending["pending_switch"]),
                {"next_generation", "from_model", "source", "started_at"},
            )
            self.assertEqual(pending["pending_switch"]["next_generation"], 1)
            self.assertEqual(pending["operation"]["operation_id"], initial["operation_id"])

            blocked_while_pending = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            self.assertEqual(blocked_while_pending["routing_status"], "failure")
            self.assertEqual(blocked_while_pending["disclosure_code"], "state-pending")

            post = run_router(
                "post-model-switch",
                switch_event(session_id, "PostModelSwitch", old_model, new_model, "command"),
                plugin_data,
            )
            self.assertEqual(post.returncode, 0, post.stderr)
            post_context = json.loads(post.stdout)["hookSpecificOutput"]["additionalContext"]
            self.assertIn(initial["operation_id"], post_context)
            self.assertIn("general", post_context)
            self.assertIn("next public entry", post_context)

            committed = load_state(plugin_data, session_id)
            self.assertEqual(committed["routing_status"], "ready")
            self.assertEqual(committed["model_generation"], 1)
            self.assertEqual(committed["model_id"], new_model)
            self.assertEqual(committed["model_classification"], "claude-5")
            self.assertEqual(committed["model_observed_from"], "PostModelSwitch")
            self.assertIsNone(committed["pending_switch"])
            self.assertEqual(committed["operation"]["operation_id"], initial["operation_id"])

            next_route = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            self.assertEqual(next_route["selected_profile"], "claude-5")
            self.assertNotEqual(next_route["operation_id"], initial["operation_id"])

    def test_mismatched_post_switch_becomes_indeterminate_without_changing_operation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude mismatch ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "mismatch-session"
            old_model = "claude-sonnet-4-6"
            new_model = "claude-sonnet-5"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", old_model),
                plugin_data,
            )
            initial = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            run_router(
                "pre-model-switch",
                switch_event(session_id, "PreModelSwitch", old_model, new_model, "command"),
                plugin_data,
            )

            mismatched = run_router(
                "post-model-switch",
                switch_event(session_id, "PostModelSwitch", old_model, new_model, "picker"),
                plugin_data,
            )
            self.assertEqual(mismatched.returncode, 0, mismatched.stderr)
            self.assertNotIn("decision", mismatched.stdout)
            state = load_state(plugin_data, session_id)
            self.assertEqual(state["routing_status"], "indeterminate")
            self.assertEqual(state["model_classification"], "unknown")
            self.assertIsNone(state["model_id"])
            self.assertIsNone(state["pending_switch"])
            self.assertEqual(state["operation"]["operation_id"], initial["operation_id"])

            blocked = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            self.assertEqual(blocked["routing_status"], "failure")
            self.assertEqual(blocked["disclosure_code"], "state-indeterminate")

    def test_mismatched_requested_pre_switch_becomes_indeterminate_without_blocking(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude pre mismatch ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "pre-mismatch-session"
            current_model = "claude-sonnet-4-6"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", current_model),
                plugin_data,
            )
            initial = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )

            pre = run_router(
                "pre-model-switch",
                switch_event(
                    session_id,
                    "PreModelSwitch",
                    "claude-opus-5",
                    "claude-sonnet-5",
                    "command",
                ),
                plugin_data,
            )

            self.assertEqual(pre.returncode, 0, pre.stderr)
            pre_output = json.loads(pre.stdout)
            self.assertIn("systemMessage", pre_output)
            self.assertNotIn("decision", pre_output)
            self.assertNotIn("permissionDecision", pre.stdout)
            self.assertIn("not denied or changed", pre_output["systemMessage"])

            state = load_state(plugin_data, session_id)
            self.assertEqual(state["routing_status"], "indeterminate")
            self.assertIsNone(state["model_id"])
            self.assertEqual(state["model_classification"], "unknown")
            self.assertIsNone(state["model_observed_from"])
            self.assertIsNone(state["pending_switch"])
            self.assertEqual(state["operation"]["operation_id"], initial["operation_id"])

            blocked = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            self.assertEqual(blocked["routing_status"], "failure")
            self.assertEqual(blocked["disclosure_code"], "state-indeterminate")
            self.assertIsNone(blocked["operation_id"])
            self.assertIsNone(blocked["selected_profile"])

    def test_automatic_post_switch_commits_without_pre_and_warns_for_unsupported(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude automatic switch ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "automatic-switch-session"
            old_model = "claude-sonnet-5"
            unsupported_model = "claude-haiku-4-5-20251001"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", old_model),
                plugin_data,
            )
            initial = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )

            post = run_router(
                "post-model-switch",
                switch_event(
                    session_id,
                    "PostModelSwitch",
                    old_model,
                    unsupported_model,
                    "auto",
                ),
                plugin_data,
            )
            self.assertEqual(post.returncode, 0, post.stderr)
            context = json.loads(post.stdout)["hookSpecificOutput"]["additionalContext"]
            self.assertIn("left formal Ask Then Do It model support", context)
            self.assertIn("claude-5", context)

            state = load_state(plugin_data, session_id)
            self.assertEqual(state["model_generation"], 1)
            self.assertEqual(state["model_classification"], "unsupported")
            self.assertEqual(state["operation"]["operation_id"], initial["operation_id"])
            blocked = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            self.assertEqual(blocked["disclosure_code"], "unsupported-model")

    def test_successful_post_switch_context_requires_complete_user_notification(self) -> None:
        cases = (
            ("requested-supported", "command", "claude-opus-4-6", "supported-non-5"),
            ("automatic-unknown", "auto", "claude-future-6-20990101", "unknown"),
        )
        for label, source, new_model, expected_classification in cases:
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(prefix=f"claude post notice {label} ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"post-notice-{label}"
                    old_model = "claude-sonnet-5"
                    run_router(
                        "session-start",
                        lifecycle_event(session_id, "startup", old_model),
                        plugin_data,
                    )
                    initial = route_envelope(
                        run_router(
                            "user-prompt-expansion",
                            expansion(session_id),
                            plugin_data,
                        )
                    )
                    if source == "command":
                        pre = run_router(
                            "pre-model-switch",
                            switch_event(
                                session_id,
                                "PreModelSwitch",
                                old_model,
                                new_model,
                                source,
                            ),
                            plugin_data,
                        )
                        self.assertEqual(pre.returncode, 0, pre.stderr)

                    post = run_router(
                        "post-model-switch",
                        switch_event(
                            session_id,
                            "PostModelSwitch",
                            old_model,
                            new_model,
                            source,
                        ),
                        plugin_data,
                    )
                    self.assertEqual(post.returncode, 0, post.stderr)
                    context = json.loads(post.stdout)["hookSpecificOutput"]["additionalContext"]
                    normalized = " ".join(context.lower().split())
                    self.assertIn("tell the user", normalized)
                    self.assertIn("active model changed", normalized)
                    self.assertIn("routing state is synchronized", normalized)
                    self.assertIn("current operation profile remains unchanged", normalized)
                    self.assertIn("only the next permitted public entry reroutes", normalized)
                    self.assertNotIn(new_model, context)

                    committed = load_state(plugin_data, session_id)
                    self.assertEqual(committed["routing_status"], "ready")
                    self.assertEqual(
                        committed["model_classification"], expected_classification
                    )
                    self.assertEqual(
                        committed["operation"]["operation_id"], initial["operation_id"]
                    )

    def test_same_session_clear_strictly_increments_generation_and_clears_authority(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude clear generation ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "clear-generation-session"
            old_model = "claude-sonnet-4-6"
            new_model = "claude-sonnet-5"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", old_model),
                plugin_data,
            )
            route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            run_router(
                "pre-model-switch",
                switch_event(
                    session_id,
                    "PreModelSwitch",
                    old_model,
                    new_model,
                    "command",
                ),
                plugin_data,
            )
            run_router(
                "post-model-switch",
                switch_event(
                    session_id,
                    "PostModelSwitch",
                    old_model,
                    new_model,
                    "command",
                ),
                plugin_data,
            )
            before_clear = load_state(plugin_data, session_id)
            self.assertEqual(before_clear["model_generation"], 1)
            self.assertIsNotNone(before_clear["operation"])

            cleared = run_router(
                "session-start",
                lifecycle_event(session_id, "clear"),
                plugin_data,
            )
            self.assertEqual(cleared.returncode, 0, cleared.stderr)
            self.assertEqual(cleared.stdout, "")

            after_clear = load_state(plugin_data, session_id)
            self.assertEqual(
                after_clear["model_generation"],
                before_clear["model_generation"] + 1,
            )
            self.assertGreater(
                after_clear["model_generation"], before_clear["model_generation"]
            )
            self.assertEqual(after_clear["session_source"], "clear")
            self.assertEqual(after_clear["routing_status"], "ready")
            self.assertIsNone(after_clear["model_id"])
            self.assertEqual(after_clear["model_classification"], "unknown")
            self.assertIsNone(after_clear["model_observed_from"])
            self.assertIsNone(after_clear["pending_switch"])
            self.assertIsNone(after_clear["operation"])

    def test_resume_generation_exhaustion_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude session max generation ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "session-start-max-generation"
            seed_maximum_generation_state(plugin_data, session_id)

            result = run_router(
                "session-start",
                lifecycle_event(session_id, "resume", "claude-sonnet-5"),
                plugin_data,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_generation_exhaustion_fails_closed(plugin_data, session_id)

    def test_requested_pre_switch_does_not_write_unsafe_next_generation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude pre max generation ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "pre-max-generation"
            old_model = "claude-sonnet-4-6"
            seed_maximum_generation_state(plugin_data, session_id, old_model)

            result = run_router(
                "pre-model-switch",
                switch_event(
                    session_id,
                    "PreModelSwitch",
                    old_model,
                    "claude-sonnet-5",
                    "command",
                ),
                plugin_data,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_generation_state_remains_valid(plugin_data, session_id)

    def test_automatic_post_switch_generation_exhaustion_fails_closed(self) -> None:
        for source in ("auto", "resume"):
            with self.subTest(source=source):
                with tempfile.TemporaryDirectory(prefix="claude post max generation ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"post-{source}-max-generation"
                    old_model = "claude-sonnet-4-6"
                    seed_maximum_generation_state(plugin_data, session_id, old_model)
                    before = load_state(plugin_data, session_id)

                    result = run_router(
                        "post-model-switch",
                        switch_event(
                            session_id,
                            "PostModelSwitch",
                            old_model,
                            "claude-sonnet-5",
                            source,
                        ),
                        plugin_data,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    warning = json.loads(result.stdout)
                    self.assertIn("routing state warning", warning["systemMessage"])

                    pathname = state_path(plugin_data, session_id)
                    failed_state = load_state(plugin_data, session_id)
                    self.assertEqual(set(failed_state), STATE_KEYS)
                    self.assertEqual(failed_state["routing_status"], "indeterminate")
                    self.assertEqual(failed_state["model_generation"], MAX_SAFE_INTEGER)
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
                        blocked = route_envelope(
                            run_router(
                                "user-prompt-expansion",
                                expansion(session_id, entry),
                                plugin_data,
                            )
                        )
                        self.assertEqual(blocked["routing_status"], "failure")
                        self.assertEqual(
                            blocked["disclosure_code"],
                            "state-indeterminate",
                        )
                        self.assertIsNone(blocked["operation_id"])
                        self.assertIsNone(blocked["selected_profile"])
                        self.assertEqual(load_state(plugin_data, session_id), failed_state)
                        self.assertEqual(
                            sorted(item.name for item in pathname.parent.iterdir()),
                            [pathname.name],
                        )

    def test_post_failure_recovers_without_secondary_persistent_state(self) -> None:
        recoveries = (
            ("auto", "post-commit"),
            ("resume", "model-bearing-session-start"),
            ("auto", "clear-session-start"),
        )
        for source, recovery in recoveries:
            with self.subTest(source=source, recovery=recovery):
                with tempfile.TemporaryDirectory(prefix="claude post recovery ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"post-recovery-{source}-{recovery}"
                    old_model = "claude-sonnet-4-6"
                    new_model = "claude-sonnet-5"
                    run_router(
                        "session-start",
                        lifecycle_event(session_id, "startup", old_model),
                        plugin_data,
                    )
                    initial = route_envelope(
                        run_router(
                            "user-prompt-expansion",
                            expansion(session_id),
                            plugin_data,
                        )
                    )
                    self.assertEqual(initial["selected_profile"], "general")

                    pathname = state_path(plugin_data, session_id)
                    before = load_state(plugin_data, session_id)
                    failed_event = switch_event(
                        session_id,
                        "PostModelSwitch",
                        old_model,
                        new_model,
                        source,
                    )
                    failed_event["pricing"] = "dynamic"
                    failed_post = run_router(
                        "post-model-switch",
                        failed_event,
                        plugin_data,
                    )

                    self.assertEqual(failed_post.returncode, 0, failed_post.stderr)
                    warning = json.loads(failed_post.stdout)
                    self.assertIn("routing state warning", warning["systemMessage"])
                    self.assertIn("Stop both public entries", warning["hookSpecificOutput"]["additionalContext"])
                    self.assertNotIn("decision", warning)
                    self.assertNotIn("permissionDecision", failed_post.stdout)
                    failed_state = load_state(plugin_data, session_id)
                    self.assertEqual(failed_state["routing_status"], "indeterminate")
                    self.assertEqual(
                        failed_state["model_generation"],
                        before["model_generation"],
                    )
                    self.assertEqual(failed_state["operation"], before["operation"])
                    self.assertEqual(
                        sorted(item.name for item in pathname.parent.iterdir()),
                        [pathname.name],
                    )

                    if recovery == "post-commit":
                        recovered = run_router(
                            "post-model-switch",
                            switch_event(
                                session_id,
                                "PostModelSwitch",
                                old_model,
                                new_model,
                                source,
                            ),
                            plugin_data,
                        )
                    elif recovery == "model-bearing-session-start":
                        recovered = run_router(
                            "session-start",
                            lifecycle_event(session_id, "resume", new_model),
                            plugin_data,
                        )
                    else:
                        recovered = run_router(
                            "session-start",
                            lifecycle_event(session_id, "clear"),
                            plugin_data,
                        )
                    self.assertEqual(recovered.returncode, 0, recovered.stderr)
                    recovered_state = load_state(plugin_data, session_id)
                    self.assertEqual(recovered_state["routing_status"], "ready")
                    self.assertEqual(
                        recovered_state["model_generation"],
                        before["model_generation"] + 1,
                    )
                    if recovery == "clear-session-start":
                        self.assertIsNone(recovered_state["operation"])
                    else:
                        self.assertEqual(
                            recovered_state["operation"],
                            before["operation"],
                        )
                    self.assertEqual(
                        sorted(item.name for item in pathname.parent.iterdir()),
                        [pathname.name],
                    )
                    rerouted = route_envelope(
                        run_router(
                            "user-prompt-expansion",
                            expansion(session_id),
                            plugin_data,
                        )
                    )
                    self.assertEqual(rerouted["routing_status"], "ready")
                    expected_classification = (
                        "unknown" if recovery == "clear-session-start" else "claude-5"
                    )
                    expected_profile = (
                        "general" if recovery == "clear-session-start" else "claude-5"
                    )
                    self.assertEqual(rerouted["model_classification"], expected_classification)
                    self.assertEqual(rerouted["selected_profile"], expected_profile)
                    self.assertEqual(
                        sorted(item.name for item in pathname.parent.iterdir()),
                        [pathname.name],
                    )

    def test_pre_switch_failure_never_returns_a_blocking_decision(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude pre failure ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            event = switch_event(
                "missing-state-session",
                "PreModelSwitch",
                "claude-sonnet-4-6",
                "claude-sonnet-5",
                "command",
            )
            result = run_router("pre-model-switch", event, plugin_data)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertIn("systemMessage", output)
            self.assertNotIn("decision", output)
            self.assertNotIn("permissionDecision", result.stdout)
            self.assertIn("not denied or changed", output["systemMessage"])

    def test_requested_switch_can_recover_from_valid_unknown_startup_model(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude unknown switch ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "unknown-startup-switch"
            run_router(
                "session-start", lifecycle_event(session_id, "startup"), plugin_data
            )
            pre = run_router(
                "pre-model-switch",
                switch_event(
                    session_id,
                    "PreModelSwitch",
                    "claude-sonnet-4-6",
                    "claude-sonnet-5",
                    "command",
                ),
                plugin_data,
            )
            self.assertEqual(pre.returncode, 0, pre.stderr)
            self.assertEqual(load_state(plugin_data, session_id)["routing_status"], "pending")

            post = run_router(
                "post-model-switch",
                switch_event(
                    session_id,
                    "PostModelSwitch",
                    "claude-sonnet-4-6",
                    "claude-sonnet-5",
                    "command",
                ),
                plugin_data,
            )
            self.assertEqual(post.returncode, 0, post.stderr)
            committed = load_state(plugin_data, session_id)
            self.assertEqual(committed["routing_status"], "ready")
            self.assertEqual(committed["model_classification"], "claude-5")

    def test_valid_unmapped_canonical_current_model_can_complete_requested_switch(self) -> None:
        current_model = "claude-sonnet-6"
        new_model = "claude-sonnet-5"
        for source in ("command", "picker", "sdk"):
            with self.subTest(source=source):
                with tempfile.TemporaryDirectory(prefix="claude canonical unknown switch ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"canonical-unknown-switch-{source}"
                    started = run_router(
                        "session-start",
                        lifecycle_event(session_id, "startup", current_model),
                        plugin_data,
                    )
                    self.assertEqual(started.returncode, 0, started.stderr)
                    initial = route_envelope(
                        run_router(
                            "user-prompt-expansion",
                            expansion(session_id),
                            plugin_data,
                        )
                    )
                    self.assertEqual(initial["routing_status"], "ready")
                    self.assertEqual(initial["model_classification"], "unknown")
                    self.assertEqual(initial["selected_profile"], "general")

                    pre = run_router(
                        "pre-model-switch",
                        switch_event(
                            session_id,
                            "PreModelSwitch",
                            current_model,
                            new_model,
                            source,
                        ),
                        plugin_data,
                    )
                    self.assertEqual(pre.returncode, 0, pre.stderr)
                    self.assertNotIn("decision", pre.stdout)
                    pending = load_state(plugin_data, session_id)
                    self.assertEqual(pending["routing_status"], "pending")
                    self.assertEqual(pending["pending_switch"]["from_model"], current_model)

                    post = run_router(
                        "post-model-switch",
                        switch_event(
                            session_id,
                            "PostModelSwitch",
                            current_model,
                            new_model,
                            source,
                        ),
                        plugin_data,
                    )
                    self.assertEqual(post.returncode, 0, post.stderr)
                    committed = load_state(plugin_data, session_id)
                    self.assertEqual(committed["routing_status"], "ready")
                    self.assertEqual(committed["model_id"], new_model)
                    self.assertEqual(committed["model_classification"], "claude-5")
                    self.assertEqual(committed["model_observed_from"], "PostModelSwitch")
                    next_route_result = run_router(
                        "user-prompt-expansion",
                        expansion(session_id),
                        plugin_data,
                    )
                    next_route = route_envelope(next_route_result)
                    self.assertEqual(next_route["routing_status"], "ready")
                    self.assertEqual(next_route["model_classification"], "claude-5")
                    self.assertEqual(next_route["selected_profile"], "claude-5")
                    for result in (started, pre, post, next_route_result):
                        self.assertNotIn(current_model, result.stdout)

    def test_requested_switch_to_valid_unmapped_canonical_target_stays_unknown(self) -> None:
        current_model = "claude-sonnet-5"
        new_model = "claude-sonnet-6"
        with tempfile.TemporaryDirectory(prefix="claude switch to canonical unknown ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "switch-to-canonical-unknown"
            started = run_router(
                "session-start",
                lifecycle_event(session_id, "startup", current_model),
                plugin_data,
            )
            self.assertEqual(started.returncode, 0, started.stderr)
            initial = route_envelope(
                run_router(
                    "user-prompt-expansion",
                    expansion(session_id),
                    plugin_data,
                )
            )
            pre = run_router(
                "pre-model-switch",
                switch_event(
                    session_id,
                    "PreModelSwitch",
                    current_model,
                    new_model,
                    "picker",
                ),
                plugin_data,
            )
            self.assertEqual(pre.returncode, 0, pre.stderr)
            self.assertEqual(load_state(plugin_data, session_id)["routing_status"], "pending")

            post = run_router(
                "post-model-switch",
                switch_event(
                    session_id,
                    "PostModelSwitch",
                    current_model,
                    new_model,
                    "picker",
                ),
                plugin_data,
            )
            self.assertEqual(post.returncode, 0, post.stderr)
            committed = load_state(plugin_data, session_id)
            self.assertEqual(committed["routing_status"], "ready")
            self.assertEqual(committed["model_id"], new_model)
            self.assertEqual(committed["model_classification"], "unknown")
            self.assertEqual(committed["model_observed_from"], "PostModelSwitch")
            self.assertEqual(committed["operation"]["operation_id"], initial["operation_id"])

            next_route_result = run_router(
                "user-prompt-expansion",
                expansion(session_id),
                plugin_data,
            )
            next_route = route_envelope(next_route_result)
            self.assertEqual(next_route["routing_status"], "ready")
            self.assertEqual(next_route["model_classification"], "unknown")
            self.assertEqual(next_route["selected_profile"], "general")
            self.assertEqual(
                next_route["disclosure_code"],
                "unknown-model-general-compatibility",
            )
            for result in (started, pre, post, next_route_result):
                self.assertNotIn(new_model, result.stdout)

    def test_pre_switch_lock_contention_returns_before_the_blocking_timeout(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude pre lock ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "pre-lock-contention"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", "claude-sonnet-4-6"),
                plugin_data,
            )
            pathname = state_path(plugin_data, session_id)
            lock_path = pathname.with_name(f".{pathname.name}.lock")
            lock_path.write_text("held", encoding="utf-8")
            started_at = time.perf_counter()
            result = run_router(
                "pre-model-switch",
                switch_event(
                    session_id,
                    "PreModelSwitch",
                    "claude-sonnet-4-6",
                    "claude-sonnet-5",
                    "command",
                ),
                plugin_data,
            )
            elapsed = time.perf_counter() - started_at
            lock_path.unlink()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertLess(elapsed, 1.8)
            self.assertIn("not denied or changed", json.loads(result.stdout)["systemMessage"])


if __name__ == "__main__":
    unittest.main()
