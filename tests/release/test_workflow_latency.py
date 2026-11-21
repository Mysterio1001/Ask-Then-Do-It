import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from measure_workflow_latency import record, report, summarize


class WorkflowLatencyTests(unittest.TestCase):
    def test_record_and_report_one_manually_marked_session(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "session.jsonl"
            args = SimpleNamespace(scenario="button", mode="lite", host="host", model="model", output=path)
            output = io.StringIO()
            with contextlib.redirect_stdout(output), patch(
                "builtins.input", side_effect=["", "first wait", "reply rework", "done"]
            ), patch("measure_workflow_latency.time.monotonic", side_effect=[100, 110, 130, 140]):
                record(args)
                report([path])
            self.assertIn("host\tmodel\tbutton\tlite\t10.000\t40.000\t20.000\t20.000\t1\t1", output.getvalue())
            saved = path.read_bytes()
            with contextlib.redirect_stdout(output), self.assertRaises(FileExistsError):
                record(args)
            self.assertEqual(path.read_bytes(), saved)

    def test_first_at_completion_and_invalid_wait_transitions(self):
        self.assertEqual(summarize([["start", 0], ["done", 5]]), (5, 5, 0, 0, 0))
        for marks in ([["reply", 1]], [["wait", 1], ["done", 2]], [["first", 2], ["done", 1]]):
            with self.subTest(marks=marks), self.assertRaises(ValueError):
                summarize([["start", 0], *marks])
