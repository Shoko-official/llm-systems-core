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

        with open(self.schemas_dir / "reference.json", "r", encoding="utf-8") as f:
            self.reference_schema = json.load(f)

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

    def test_valid_reference(self) -> None:
        valid_ref = {
            "citation_key": "source-attention-2017",
            "ledger_source_id": "source-attention-2017",
            "ledger_claim_id": "claim-attention-parallelism",
            "paper_section_target": "sections/introduction.md",
            "readiness_state": "ready_for_bibliography",
            "missing_citation_detail": "None",
            "bibtex": {
                "entry_type": "article",
                "author": "Vaswani et al.",
                "title": "Attention Is All You Need",
                "year": "2017",
                "journal": "NeurIPS"
            }
        }
        validate(instance=valid_ref, schema=self.reference_schema)

    def test_invalid_reference_missing_required(self) -> None:
        invalid_ref = {
            "citation_key": "source-attention-2017",
            "ledger_source_id": "source-attention-2017"
            # readiness_state is missing
        }
        with self.assertRaises(ValidationError):
            validate(instance=invalid_ref, schema=self.reference_schema)

    def test_invalid_reference_extra_property(self) -> None:
        invalid_ref = {
            "citation_key": "source-attention-2017",
            "ledger_source_id": "source-attention-2017",
            "readiness_state": "ready_for_bibliography",
            "unknown_property": "not allowed"
        }
        with self.assertRaises(ValidationError):
            validate(instance=invalid_ref, schema=self.reference_schema)


class TestKPIs(unittest.TestCase):
    def test_kpi_tracker_parsing(self) -> None:
        from scripts.check_kpis import parse_kpi_tracker

        lines, kpis = parse_kpi_tracker()
        self.assertTrue(len(kpis) > 0)
        for kpi in kpis:
            self.assertIn("id", kpi)
            self.assertIn("value", kpi)
            self.assertIn("status", kpi)


class TestCrossRepoSchemaValidation(unittest.TestCase):
    def test_check_types_compatible(self) -> None:
        from scripts.validate_repo import check_types_compatible
        self.assertTrue(check_types_compatible("string", "string"))
        self.assertTrue(check_types_compatible("string", ["string", "null"]))
        self.assertTrue(check_types_compatible(["string", "null"], "string"))
        self.assertTrue(check_types_compatible("string", "integer"))
        self.assertTrue(check_types_compatible("string", ["integer", "null"]))

        self.assertFalse(check_types_compatible("boolean", "integer"))
        self.assertFalse(check_types_compatible("array", "string"))

    def test_schema_alignment_success(self) -> None:
        from scripts.validate_repo import validate_cross_repo_schemas
        try:
            validate_cross_repo_schemas()
        except SystemExit as e:
            self.fail(f"validate_cross_repo_schemas failed unexpectedly: {e}")
