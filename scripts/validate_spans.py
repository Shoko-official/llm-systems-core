from __future__ import annotations

"""validate_spans.py - Validate tracing span JSON records against schemas/span.json.

Checks:
1. Validates spans match schemas/span.json schema.
2. Checks that end_time is chronologically after start_time.
3. Checks that duration_ms is positive and aligns with timestamp delta.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("Error: jsonschema is required.", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SPAN_SCHEMA = ROOT / "schemas" / "span.json"


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def load_json(path: Path) -> dict:
    if not path.is_file():
        fail(f"File not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        fail(f"Failed to parse JSON from {path}: {e}")


def parse_iso_timestamp(ts_str: str) -> datetime:
    # Handle possible Z suffix or offset
    ts_str = ts_str.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(ts_str)
    except ValueError as e:
        fail(f"Invalid ISO timestamp format '{ts_str}': {e}")


def validate_span_logic(data: dict, source: str) -> None:
    start_str = data.get("start_time")
    end_str = data.get("end_time")
    duration = data.get("duration_ms")

    start_dt = parse_iso_timestamp(start_str)
    end_dt = parse_iso_timestamp(end_str)

    if end_dt < start_dt:
        fail(f"{source}: end_time '{end_str}' is chronologically before start_time '{start_str}'")

    delta_ms = (end_dt - start_dt).total_seconds() * 1000.0
    
    # Check that duration_ms is approximately aligned (within 2ms tolerance for rounding/parsing issues)
    if abs(delta_ms - duration) > 2.0:
        fail(f"{source}: duration_ms ({duration}) does not align with timestamp delta ({delta_ms:.2f} ms)")


def validate_span_file(span_path: Path, schema: dict) -> None:
    data = load_json(span_path)
    source = span_path.name
    
    # If the span file is an array of spans, validate each
    if isinstance(data, list):
        for idx, span in enumerate(data):
            try:
                validate(instance=span, schema=schema)
            except ValidationError as e:
                fail(f"Schema validation error in {source} at index {idx}: {e.message}")
            validate_span_logic(span, f"{source}[{idx}]")
    else:
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            fail(f"Schema validation error in {source}: {e.message}")
        validate_span_logic(data, source)

    print(f"  ok: {span_path.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate tracing span JSON records")
    parser.add_argument("spans", nargs="*", help="Path(s) to span JSON files. If omitted, scans examples/spans/")
    parser.add_argument("--schema", type=str, help="Path to span schema (schemas/span.json)")
    args = parser.parse_args()

    schema_path = Path(args.schema) if args.schema else SPAN_SCHEMA
    if not schema_path.is_file():
        fail(f"Schema file not found: {schema_path}")

    schema = load_json(schema_path)

    if args.spans:
        paths = [Path(p) for p in args.spans]
    else:
        spans_dir = ROOT / "examples" / "spans"
        if not spans_dir.is_dir():
            print(f"No examples/spans/ directory found. Skipping span examples scan.")
            sys.exit(0)
        paths = sorted(spans_dir.glob("*.json"))
        if not paths:
            print("No span JSON files found in examples/spans/.")
            sys.exit(0)

    print(f"Validating {len(paths)} span record file(s) against {schema_path.name}...")
    for path in paths:
        validate_span_file(path, schema)

    print(f"All {len(paths)} span file(s) valid.")


if __name__ == "__main__":
    main()
