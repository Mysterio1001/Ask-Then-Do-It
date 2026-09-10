from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest

from tests.claude.test_router_contract import (
    MAPPING,
    ROOT,
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


MAX_MAPPING_BYTES = 65_536
MAX_STATE_BYTES = 16_384
LOCK_RECORD_KEYS = {
    "schema_version",
    "owner_token",
    "pid",
    "created_at",
    "lease_until",
}


def node_path() -> str:
    node = shutil.which("node")
    if node is None:
        raise unittest.SkipTest("Node.js is required for the Claude router tests")
    return node


def run_module_probe(source: str, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [node_path(), "--input-type=module", "--eval", source, *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def run_router_with_raw_stdin(
    action: str,
    payload: bytes,
    plugin_data: Path,
    *trusted_arguments: str,
) -> subprocess.CompletedProcess[bytes]:
    plugin = ROUTER.parent.parent
    environment = os.environ.copy()
    environment.update(
        {
            "CLAUDE_PLUGIN_DATA": str(plugin_data),
            "CLAUDE_PLUGIN_ROOT": str(plugin),
        }
    )
    return subprocess.run(
        [node_path(), str(ROUTER), action, *trusted_arguments],
        cwd=ROOT,
        env=environment,
        input=payload,
        capture_output=True,
        check=False,
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_text(value: datetime) -> str:
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def padded_json(source: bytes, size: int) -> bytes:
    if len(source) > size:
        raise AssertionError(f"fixture is already larger than {size} bytes")
    return source + (b" " * (size - len(source)))


def lock_path(plugin_data: Path, session_id: str) -> Path:
    pathname = state_path(plugin_data, session_id)
    return pathname.with_name(f".{pathname.name}.lock")


def lock_record(
    *,
    pid: int,
    created_at: datetime,
    lease_until: datetime,
    owner_token: str,
) -> dict[str, object]:
    value: dict[str, object] = {
        "schema_version": 1,
        "owner_token": owner_token,
        "pid": pid,
        "created_at": utc_text(created_at),
        "lease_until": utc_text(lease_until),
    }
    if set(value) != LOCK_RECORD_KEYS:
        raise AssertionError("test lock record no longer matches the reviewed schema")
    return value


def write_lock(pathname: Path, value: dict[str, object] | bytes, mtime: datetime) -> bytes:
    source = value if isinstance(value, bytes) else json.dumps(value).encode("utf-8")
    pathname.write_bytes(source)
    timestamp = mtime.timestamp()
    os.utime(pathname, (timestamp, timestamp))
    return source


def terminated_process_id() -> int:
    process = subprocess.Popen(
        [node_path(), "--eval", "process.exit(0)"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    process.wait(timeout=5)
    return process.pid


class ClaudeRouterReviewRegressionTests(unittest.TestCase):
    def test_post_precommit_indeterminate_and_successful_commit_share_session_lock(
        self,
    ) -> None:
        source = ROUTER.read_text(encoding="utf-8")
        main_start = source.index("export async function main")
        post_dispatch = source.index(
            '    if (action === "post-model-switch") {',
            main_start,
        )
        lock_start = source.index(
            "      const output = await withSessionLock(pathname, async () => {",
            post_dispatch,
        )
        lock_end = source.index("\n      });", lock_start)
        precommit = source.index(
            "await markIndeterminate(pathname, prior);",
            lock_start,
        )
        validate = source.index("const event = validateEvent(rawEvent, action);", lock_start)
        commit = source.index("return commitPostModelSwitch(", lock_start)

        self.assertTrue(
            lock_start < precommit < validate < commit < lock_end,
            "Post precommit invalidation and successful commit must be one locked transaction",
        )

    def test_mapping_read_has_an_exact_bounded_limit(self) -> None:
        mapping_probe = f"""
import {{ loadMapping }} from {json.dumps(ROUTER.as_uri())};
try {{
  await loadMapping(process.argv[1]);
  console.log("accepted");
}} catch (error) {{
  console.log(error.code ?? error.name);
}}
"""
        with tempfile.TemporaryDirectory(prefix="claude bounded mapping ") as temporary:
            root = Path(temporary)
            baseline = MAPPING.read_bytes()
            exact = root / "exact-limit.json"
            oversized = root / "oversized.json"
            exact.write_bytes(padded_json(baseline, MAX_MAPPING_BYTES))
            oversized.write_bytes(padded_json(baseline, MAX_MAPPING_BYTES + 1))

            accepted = run_module_probe(mapping_probe, str(exact))
            rejected = run_module_probe(mapping_probe, str(oversized))
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.assertEqual(accepted.stdout.strip(), "accepted")
            self.assertEqual(rejected.returncode, 0, rejected.stderr)
            self.assertEqual(rejected.stdout.strip(), "mapping-invalid")

    def test_state_read_has_an_exact_bounded_limit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude bounded state ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            exact_session = "exact-state-limit"
            oversized_session = "oversized-state-limit"
            for session_id, size in (
                (exact_session, MAX_STATE_BYTES),
                (oversized_session, MAX_STATE_BYTES + 1),
            ):
                started = run_router(
                    "session-start",
                    lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                    plugin_data,
                )
                self.assertEqual(started.returncode, 0, started.stderr)
                pathname = state_path(plugin_data, session_id)
                pathname.write_bytes(padded_json(pathname.read_bytes(), size))

            exact_route = route_envelope(
                run_router("user-prompt-expansion", expansion(exact_session), plugin_data)
            )
            oversized_route = route_envelope(
                run_router("user-prompt-expansion", expansion(oversized_session), plugin_data)
            )
            self.assertEqual(exact_route["routing_status"], "ready")
            self.assertEqual(oversized_route["routing_status"], "failure")
            self.assertEqual(oversized_route["disclosure_code"], "state-invalid")
            self.assertIsNone(oversized_route["operation_id"])

    def test_bounded_handle_reader_rejects_growth_beyond_the_limit(self) -> None:
        probe = f"""
const router = await import({json.dumps(ROUTER.as_uri())});
if (typeof router.readBoundedHandle !== "function") {{
  console.log(JSON.stringify({{ available: false }}));
}} else {{
  const maximum = 16;
  const payload = Buffer.alloc(maximum + 1, 0x20);
  const requested = [];
  let cursor = 0;
  const growingHandle = {{
    async read(buffer, offset, length) {{
      requested.push(length);
      const bytesRead = Math.min(length, payload.length - cursor);
      if (bytesRead > 0) {{
        payload.copy(buffer, offset, cursor, cursor + bytesRead);
        cursor += bytesRead;
      }}
      return {{ bytesRead, buffer }};
    }},
  }};
  let code = "accepted";
  try {{
    await router.readBoundedHandle(growingHandle, maximum, "state-invalid");
  }} catch (error) {{
    code = error.code ?? error.name;
  }}
  console.log(JSON.stringify({{
    available: true,
    code,
    maximum_request: Math.max(...requested),
  }}));
}}
"""
        result = run_module_probe(probe)
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = json.loads(result.stdout)
        self.assertTrue(observed["available"], "router must expose its bounded handle reader")
        self.assertEqual(observed["code"], "state-invalid")
        self.assertLessEqual(observed["maximum_request"], 17)

    def test_expired_dead_router_lock_is_recovered(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude orphan lock ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "expired-dead-lock"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                plugin_data,
            )
            old = datetime(2000, 1, 1, tzinfo=timezone.utc)
            pathname = lock_path(plugin_data, session_id)
            write_lock(
                pathname,
                lock_record(
                    pid=terminated_process_id(),
                    created_at=old,
                    lease_until=old + timedelta(seconds=30),
                    owner_token="a" * 32,
                ),
                old,
            )

            routed = route_envelope(
                run_router("user-prompt-expansion", expansion(session_id), plugin_data)
            )
            self.assertEqual(routed["routing_status"], "ready")
            self.assertFalse(pathname.exists())

    def test_last_attempt_stale_recovery_reacquires_owned_lock_before_callback(self) -> None:
        probe = f"""
import path from "node:path";
import {{ readFile }} from "node:fs/promises";
const router = await import({json.dumps(ROUTER.as_uri())});
const pathname = process.argv[1];
const lockPath = path.join(path.dirname(pathname), `.${{path.basename(pathname)}}.lock`);
let firstLock = null;
let secondEntered = false;
let secondResult = "not-run";
await router.withSessionLock(pathname, async () => {{
  try {{
    firstLock = JSON.parse(await readFile(lockPath, "utf8"));
  }} catch {{
    firstLock = null;
  }}
  try {{
    await router.withSessionLock(pathname, async () => {{
      secondEntered = true;
    }}, {{ retryCount: 0, allowReclaim: false }});
    secondResult = "accepted";
  }} catch (error) {{
    secondResult = error.code ?? error.name;
  }}
}}, {{ retryCount: 0, allowReclaim: true }});
const exactKeys = ["created_at", "lease_until", "owner_token", "pid", "schema_version"];
const observedKeys = firstLock === null ? [] : Object.keys(firstLock).sort();
const createdAt = Date.parse(firstLock?.created_at);
const leaseUntil = Date.parse(firstLock?.lease_until);
console.log(JSON.stringify({{
  completeOwnedLock:
    firstLock !== null &&
    JSON.stringify(observedKeys) === JSON.stringify(exactKeys) &&
    firstLock.schema_version === 1 &&
    /^[0-9a-f]{{32}}$/.test(firstLock.owner_token) &&
    firstLock.pid === process.pid &&
    Number.isFinite(createdAt) &&
    Number.isFinite(leaseUntil) &&
    leaseUntil >= createdAt,
  secondEntered,
  secondResult,
}}));
"""
        with tempfile.TemporaryDirectory(prefix="claude last attempt reclaim ") as temporary:
            pathname = Path(temporary) / "sessions" / ("3" * 64 + ".json")
            pathname.parent.mkdir(parents=True)
            old = datetime(2000, 1, 1, tzinfo=timezone.utc)
            stale_lock = pathname.with_name(f".{pathname.name}.lock")
            write_lock(
                stale_lock,
                lock_record(
                    pid=terminated_process_id(),
                    created_at=old,
                    lease_until=old + timedelta(seconds=30),
                    owner_token="4" * 32,
                ),
                old,
            )
            result = run_module_probe(probe, pathname.as_posix())

        self.assertEqual(result.returncode, 0, result.stderr)
        observed = json.loads(result.stdout)
        self.assertEqual(
            observed,
            {
                "completeOwnedLock": True,
                "secondEntered": False,
                "secondResult": "state-write-failed",
            },
            "the recovered callback must own a complete lock and exclude a contender",
        )

    def test_lock_owner_release_does_not_delete_a_replacement_token(self) -> None:
        probe = f"""
import {{ rename, writeFile, readFile }} from "node:fs/promises";
const router = await import({json.dumps(ROUTER.as_uri())});
if (typeof router.withSessionLock !== "function") {{
  console.log(JSON.stringify({{ available: false }}));
}} else {{
  const pathname = process.argv[1];
  const lockPath = `${{pathname.slice(0, pathname.lastIndexOf('/') + 1)}}.${{pathname.slice(pathname.lastIndexOf('/') + 1)}}.lock`;
  const replacement = {{
    schema_version: 1,
    owner_token: "e".repeat(32),
    pid: process.pid,
    created_at: new Date().toISOString(),
    lease_until: new Date(Date.now() + 30000).toISOString(),
  }};
  await router.withSessionLock(pathname, async () => {{
    await rename(lockPath, `${{lockPath}}.former-owner`);
    await writeFile(lockPath, JSON.stringify(replacement), {{ flag: "wx" }});
  }}, {{ retryCount: 0, allowReclaim: false }});
  const observed = JSON.parse(await readFile(lockPath, "utf8"));
  console.log(JSON.stringify({{ available: true, owner_token: observed.owner_token }}));
}}
"""
        with tempfile.TemporaryDirectory(prefix="claude lock replacement ") as temporary:
            pathname = Path(temporary) / "sessions" / ("0" * 64 + ".json")
            result = run_module_probe(probe, pathname.as_posix())
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = json.loads(result.stdout)
        self.assertTrue(observed["available"])
        self.assertEqual(observed["owner_token"], "e" * 32)

    def test_session_start_and_post_switch_recover_expired_dead_locks(self) -> None:
        old = datetime(2000, 1, 1, tzinfo=timezone.utc)
        dead_pid = terminated_process_id()
        with tempfile.TemporaryDirectory(prefix="claude lifecycle orphan locks ") as temporary:
            plugin_data = Path(temporary) / "plugin data"

            clear_session = "clear-expired-dead-lock"
            run_router(
                "session-start",
                lifecycle_event(clear_session, "startup", "claude-sonnet-5"),
                plugin_data,
            )
            clear_lock = lock_path(plugin_data, clear_session)
            write_lock(
                clear_lock,
                lock_record(
                    pid=dead_pid,
                    created_at=old,
                    lease_until=old + timedelta(seconds=30),
                    owner_token="f" * 32,
                ),
                old,
            )
            cleared = run_router(
                "session-start",
                lifecycle_event(clear_session, "clear"),
                plugin_data,
            )
            self.assertEqual(cleared.returncode, 0, cleared.stderr)
            self.assertEqual(load_state(plugin_data, clear_session)["session_source"], "clear")
            self.assertFalse(clear_lock.exists())

            switch_session = "post-expired-dead-lock"
            old_model = "claude-sonnet-4-6"
            new_model = "claude-sonnet-5"
            run_router(
                "session-start",
                lifecycle_event(switch_session, "startup", old_model),
                plugin_data,
            )
            run_router(
                "pre-model-switch",
                switch_event(
                    switch_session,
                    "PreModelSwitch",
                    old_model,
                    new_model,
                    "command",
                ),
                plugin_data,
            )
            post_lock = lock_path(plugin_data, switch_session)
            write_lock(
                post_lock,
                lock_record(
                    pid=dead_pid,
                    created_at=old,
                    lease_until=old + timedelta(seconds=30),
                    owner_token="1" * 32,
                ),
                old,
            )
            posted = run_router(
                "post-model-switch",
                switch_event(
                    switch_session,
                    "PostModelSwitch",
                    old_model,
                    new_model,
                    "command",
                ),
                plugin_data,
            )
            self.assertEqual(posted.returncode, 0, posted.stderr)
            state = load_state(plugin_data, switch_session)
            self.assertEqual(state["routing_status"], "ready")
            self.assertEqual(state["model_id"], new_model)
            self.assertFalse(post_lock.exists())

    def test_concurrent_reclaimers_preserve_exclusive_complete_routes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude concurrent reclaim ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "concurrent-expired-dead-lock"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                plugin_data,
            )
            old = datetime(2000, 1, 1, tzinfo=timezone.utc)
            pathname = lock_path(plugin_data, session_id)
            write_lock(
                pathname,
                lock_record(
                    pid=terminated_process_id(),
                    created_at=old,
                    lease_until=old + timedelta(seconds=30),
                    owner_token="2" * 32,
                ),
                old,
            )
            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(
                    executor.map(
                        lambda _: run_router(
                            "user-prompt-expansion",
                            expansion(session_id),
                            plugin_data,
                        ),
                        range(4),
                    )
                )
            envelopes = [route_envelope(result) for result in results]
            self.assertTrue(all(item["routing_status"] == "ready" for item in envelopes))
            self.assertEqual(load_state(plugin_data, session_id)["routing_status"], "ready")
            leftovers = [
                item.name
                for item in state_path(plugin_data, session_id).parent.iterdir()
                if ".lock" in item.name
            ]
            self.assertEqual(leftovers, [])

    def test_fresh_live_and_malformed_locks_are_never_reclaimed(self) -> None:
        now = utc_now()
        old = datetime(2000, 1, 1, tzinfo=timezone.utc)
        cases: tuple[tuple[str, dict[str, object] | bytes, datetime], ...] = (
            (
                "fresh-dead",
                lock_record(
                    pid=terminated_process_id(),
                    created_at=now,
                    lease_until=now + timedelta(seconds=30),
                    owner_token="b" * 32,
                ),
                now,
            ),
            (
                "expired-live",
                lock_record(
                    pid=os.getpid(),
                    created_at=old,
                    lease_until=old + timedelta(seconds=30),
                    owner_token="c" * 32,
                ),
                old,
            ),
            ("malformed", b'{"schema_version":1', old),
        )
        for label, record, modified_at in cases:
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory(prefix=f"claude safe lock {label} ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"safe-lock-{label}"
                    run_router(
                        "session-start",
                        lifecycle_event(session_id, "startup", "claude-sonnet-5"),
                        plugin_data,
                    )
                    pathname = lock_path(plugin_data, session_id)
                    expected = write_lock(pathname, record, modified_at)

                    routed = route_envelope(
                        run_router("user-prompt-expansion", expansion(session_id), plugin_data)
                    )
                    self.assertEqual(routed["routing_status"], "failure")
                    self.assertEqual(routed["disclosure_code"], "state-write-failed")
                    self.assertEqual(pathname.read_bytes(), expected)

    def test_pre_model_switch_remains_non_waiting_with_a_live_lock(self) -> None:
        with tempfile.TemporaryDirectory(prefix="claude fast pre lock ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            session_id = "fast-pre-live-lock"
            model = "claude-sonnet-4-6"
            run_router(
                "session-start",
                lifecycle_event(session_id, "startup", model),
                plugin_data,
            )
            now = utc_now()
            pathname = lock_path(plugin_data, session_id)
            expected = write_lock(
                pathname,
                lock_record(
                    pid=os.getpid(),
                    created_at=now,
                    lease_until=now + timedelta(seconds=30),
                    owner_token="d" * 32,
                ),
                now,
            )

            started_at = time.monotonic()
            result = run_router(
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
            elapsed = time.monotonic() - started_at
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertLess(elapsed, 1.0)
            output = json.loads(result.stdout)
            self.assertIn("not denied or changed", output["systemMessage"])
            self.assertNotIn("decision", output)
            self.assertEqual(pathname.read_bytes(), expected)

    def test_resume_and_compact_preserve_binding_and_disclose_unsupported_model(self) -> None:
        unsupported_model = "claude-haiku-4-5-20251001"
        for source in ("resume", "compact"):
            with self.subTest(source=source):
                with tempfile.TemporaryDirectory(prefix=f"claude {source} unsupported ") as temporary:
                    plugin_data = Path(temporary) / "plugin data"
                    session_id = f"{source}-unsupported-binding"
                    run_router(
                        "session-start",
                        lifecycle_event(session_id, "startup", "claude-sonnet-4-6"),
                        plugin_data,
                    )
                    operation = route_envelope(
                        run_router("user-prompt-expansion", expansion(session_id), plugin_data)
                    )
                    self.assertEqual(operation["selected_profile"], "general")

                    continued = run_router(
                        "session-start",
                        lifecycle_event(session_id, source, unsupported_model),
                        plugin_data,
                    )
                    self.assertEqual(continued.returncode, 0, continued.stderr)
                    context = json.loads(continued.stdout)["hookSpecificOutput"][
                        "additionalContext"
                    ]
                    self.assertIn(operation["operation_id"], context)
                    self.assertIn("bound_profile=general", context)
                    self.assertIn("left formal Ask Then Do It model support", context)

                    state = load_state(plugin_data, session_id)
                    self.assertEqual(state["model_classification"], "unsupported")
                    self.assertEqual(
                        state["operation"]["operation_id"], operation["operation_id"]
                    )
                    self.assertEqual(state["operation"]["bound_profile"], "general")

    def test_stdin_rejects_replacement_colliding_invalid_utf8_session_ids(self) -> None:
        sentinel = "RAW_INVALID_UTF8_SESSION"
        encoded = json.dumps(
            lifecycle_event(sentinel, "startup", "claude-sonnet-5"),
            separators=(",", ":"),
        ).encode("utf-8")
        marker = sentinel.encode("ascii")
        self.assertEqual(encoded.count(marker), 1)
        payloads = [
            encoded.replace(marker, b"raw-" + bytes([invalid]) + b"-session")
            for invalid in (0xFF, 0xFE)
        ]

        with tempfile.TemporaryDirectory(prefix="claude invalid utf8 stdin ") as temporary:
            plugin_data = Path(temporary) / "plugin data"
            results = [
                run_router_with_raw_stdin("session-start", payload, plugin_data)
                for payload in payloads
            ]
            sessions = plugin_data / "routing" / "v1" / "sessions"
            state_files = sorted(sessions.glob("*.json")) if sessions.exists() else []
            replacement_collision = state_path(plugin_data, "raw-\ufffd-session")
            replacement_collision_exists = replacement_collision.exists()

        self.assertEqual(
            {
                "returncodes": [result.returncode for result in results],
                "empty_stdout": [result.stdout == b"" for result in results],
                "state_files": [pathname.name for pathname in state_files],
                "replacement_collision_exists": replacement_collision_exists,
            },
            {
                "returncodes": [0, 0],
                "empty_stdout": [True, True],
                "state_files": [],
                "replacement_collision_exists": False,
            },
            "raw 0xFF and 0xFE session identities must fail closed without sharing state",
        )

    def test_invalid_utf8_explicit_expansion_preserves_explicit_entry(self) -> None:
        sentinel = "RAW_INVALID_UTF8_EXPLICIT_SESSION"
        event = expansion(sentinel, "explicit-claude-5")
        self.assertEqual(
            event["command_name"],
            "ask-then-do-it:ask-then-do-it-5",
        )
        encoded = json.dumps(event, separators=(",", ":")).encode("utf-8")
        marker = sentinel.encode("ascii")
        self.assertEqual(encoded.count(marker), 1)
        payload = encoded.replace(marker, b"raw-\xff-session")

        with tempfile.TemporaryDirectory(
            prefix="claude invalid utf8 explicit expansion "
        ) as temporary:
            plugin_data = Path(temporary) / "plugin data"
            result = run_router_with_raw_stdin(
                "user-prompt-expansion",
                payload,
                plugin_data,
                "ask-then-do-it:ask-then-do-it-5",
            )
            envelope = route_envelope(result)
            sessions = plugin_data / "routing" / "v1" / "sessions"
            state_count = (
                len(list(sessions.glob("*.json"))) if sessions.exists() else 0
            )

        self.assertEqual(
            {
                "returncode": result.returncode,
                "entry": envelope["entry"],
                "routing_status": envelope["routing_status"],
                "operation_id": envelope["operation_id"],
                "disclosure_code": envelope["disclosure_code"],
                "state_count": state_count,
            },
            {
                "returncode": 0,
                "entry": "/ask-then-do-it:ask-then-do-it-5",
                "routing_status": "failure",
                "operation_id": None,
                "disclosure_code": "invalid-hook-input",
                "state_count": 0,
            },
        )


if __name__ == "__main__":
    unittest.main()
