import json
import sys
import unittest
from pathlib import Path
from jsonschema import validate, ValidationError

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestSchemas(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas_dir = ROOT / "schemas"

        with open(self.schemas_dir / "source.json", "r", encoding="utf-8") as f:
            self.source_schema = json.load(f)

        with open(self.schemas_dir / "claim.json", "r", encoding="utf-8") as f:
            self.claim_schema = json.load(f)

    def test_valid_source(self) -> None:
        valid_source = {
            "id": "SRC-001",
            "title": "A Great LLM Core Architecture Study",
            "url": "https://example.com/study",
            "type": "primary",
            "author": "John Doe",
            "published_date": "2026-05-12",
        }
        validate(instance=valid_source, schema=self.source_schema)

    def test_invalid_source_missing_required(self) -> None:
        invalid_source = {
            "id": "SRC-002",
        }
        with self.assertRaises(ValidationError):
            validate(instance=invalid_source, schema=self.source_schema)

    def test_invalid_source_extra_property(self) -> None:
        invalid_source = {
            "id": "SRC-003",
            "title": "Some study",
            "unknown_field": "not allowed",
        }
        with self.assertRaises(ValidationError):
            validate(instance=invalid_source, schema=self.source_schema)

    def test_valid_claim(self) -> None:
        valid_claim = {
            "id": "CLM-100",
            "claim": "Modern LLM systems require structured JSON schemas.",
            "source_ids": ["SRC-001"],
            "status": "verified",
            "notes": "Verified in simulation tests.",
        }
        validate(instance=valid_claim, schema=self.claim_schema)

    def test_invalid_claim_missing_required(self) -> None:
        invalid_claim = {
            "id": "CLM-101",
            "claim": "This claim has no source_ids or status.",
        }
        with self.assertRaises(ValidationError):
            validate(instance=invalid_claim, schema=self.claim_schema)


class TestKPIs(unittest.TestCase):
    def test_kpi_tracker_parsing(self) -> None:
        from scripts.check_kpis import parse_kpi_tracker

        lines, kpis = parse_kpi_tracker()
        self.assertTrue(len(kpis) > 0)
        for kpi in kpis:
            self.assertIn("id", kpi)
            self.assertIn("value", kpi)
            self.assertIn("status", kpi)
