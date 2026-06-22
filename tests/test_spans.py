from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

class TestSpans(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory(dir=str(ROOT))
        self.tmp_path = Path(self.tmpdir.name)

        # Create mock span schema
        self.schema_file = self.tmp_path / "span.json"
        self.schema_data = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "span_id": {"type": "string", "pattern": "^[a-fA-F0-9]{16}$"},
                "trace_id": {"type": "string", "pattern": "^[a-fA-F0-9]{32}$"},
                "parent_span_id": {"type": ["string", "null"], "pattern": "^([a-fA-F0-9]{16}|N/A)?$"},
                "name": {"type": "string"},
                "start_time": {"type": "string"},
                "end_time": {"type": "string"},
                "duration_ms": {"type": "number"},
                "service_name": {"type": "string"},
                "status": {"type": "string"},
                "attributes": {"type": "object"}
            },
            "required": ["span_id", "trace_id", "name", "start_time", "end_time", "duration_ms", "service_name", "status"],
            "additionalProperties": False
        }
        with open(self.schema_file, "w", encoding="utf-8") as f:
            json.dump(self.schema_data, f, indent=2)

        # Create mock span JSON file
        self.span_file = self.tmp_path / "span_test.json"
        self.span_data = {
            "span_id": "8a0f2b3c4d5e6f7a",
            "trace_id": "0123456789abcdef0123456789abcdef",
            "parent_span_id": "N/A",
            "name": "is_prompt_safe",
            "start_time": "2026-06-22T17:00:00.000Z",
            "end_time": "2026-06-22T17:00:00.125Z",
            "duration_ms": 125.0,
            "service_name": "security",
            "status": "ok"
        }
        with open(self.span_file, "w", encoding="utf-8") as f:
            json.dump(self.span_data, f, indent=2)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_validate_spans_success(self) -> None:
        script_path = ROOT / "scripts" / "validate_spans.py"
        res = subprocess.run([
            sys.executable,
            str(script_path),
            str(self.span_file),
            "--schema", str(self.schema_file)
        ], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Span validation failed: {res.stderr}\n{res.stdout}")

    def test_validate_spans_schema_failure(self) -> None:
        # Invalid trace_id length
        self.span_data["trace_id"] = "short"
        with open(self.span_file, "w", encoding="utf-8") as f:
            json.dump(self.span_data, f, indent=2)

        script_path = ROOT / "scripts" / "validate_spans.py"
        res = subprocess.run([
            sys.executable,
            str(script_path),
            str(self.span_file),
            "--schema", str(self.schema_file)
        ], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Schema validation error", res.stderr)

    def test_validate_spans_duration_mismatch(self) -> None:
        # Change duration_ms to cause mismatch
        self.span_data["duration_ms"] = 500.0
        with open(self.span_file, "w", encoding="utf-8") as f:
            json.dump(self.span_data, f, indent=2)

        script_path = ROOT / "scripts" / "validate_spans.py"
        res = subprocess.run([
            sys.executable,
            str(script_path),
            str(self.span_file),
            "--schema", str(self.schema_file)
        ], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("duration_ms", res.stderr)

    def test_validate_spans_time_order_failure(self) -> None:
        # End time before start time
        self.span_data["start_time"] = "2026-06-22T17:00:00.500Z"
        self.span_data["end_time"] = "2026-06-22T17:00:00.125Z"
        with open(self.span_file, "w", encoding="utf-8") as f:
            json.dump(self.span_data, f, indent=2)

        script_path = ROOT / "scripts" / "validate_spans.py"
        res = subprocess.run([
            sys.executable,
            str(script_path),
            str(self.span_file),
            "--schema", str(self.schema_file)
        ], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("chronologically before", res.stderr)

if __name__ == "__main__":
    unittest.main()
