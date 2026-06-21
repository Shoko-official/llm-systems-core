from __future__ import annotations

import json
import sys
import unittest
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_references import validate_cross_repo

class TestCrossRepoValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
        # Create mock paper and ledger directories
        self.paper_dir = self.temp_path / "modern-llm-systems-paper"
        self.ledger_dir = self.temp_path / "llm-systems-research-ledger"
        
        self.paper_dir.mkdir(parents=True, exist_ok=True)
        self.ledger_dir.mkdir(parents=True, exist_ok=True)
        
        (self.paper_dir / "references").mkdir(parents=True, exist_ok=True)
        (self.paper_dir / "sections").mkdir(parents=True, exist_ok=True)
        
        (self.ledger_dir / "sources").mkdir(parents=True, exist_ok=True)
        (self.ledger_dir / "claims").mkdir(parents=True, exist_ok=True)
        (self.ledger_dir / "citations").mkdir(parents=True, exist_ok=True)
        
        self.schema_path = ROOT / "schemas" / "reference.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_index(self, content: str) -> None:
        (self.paper_dir / "references" / "index.md").write_text(content, encoding="utf-8")

    def write_section(self, filename: str, content: str) -> None:
        (self.paper_dir / "sections" / filename).write_text(content, encoding="utf-8")

    def write_source(self, source_id: str) -> None:
        (self.ledger_dir / "sources" / f"{source_id}.md").write_text(f"---\nsource_id: {source_id}\n---", encoding="utf-8")

    def write_claim(self, claim_id: str) -> None:
        (self.ledger_dir / "claims" / f"{claim_id}.md").write_text(f"---\nclaim_id: {claim_id}\n---", encoding="utf-8")

    def write_citation(self, filename: str, citation_id: str, source_id: str, claim_id: str, target: str, state: str, detail: str | None) -> None:
        content = f"""---
citation_id: {citation_id}
source_id: {source_id}
claim_id: {claim_id}
paper_section_target: "{target}"
readiness_state: {state}
missing_citation_detail: {detail if detail is not None else 'null'}
---
# Citation: {citation_id}
"""
        (self.ledger_dir / "citations" / filename).write_text(content, encoding="utf-8")

    def test_valid_empty_index(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
""")
        # Should pass because there are no references
        validate_cross_repo(self.paper_dir, self.ledger_dir, self.schema_path)

    def test_valid_reference_flow(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | sections/intro.md | ready_for_bibliography | None |
""")
        self.write_section("intro.md", "This is a statement [@key-1].")
        self.write_source("source-1")
        self.write_claim("claim-1")
        self.write_citation("cit1.md", "cit-1", "source-1", "claim-1", "sections/intro.md", "ready_for_bibliography", None)
        
        # Should pass
        validate_cross_repo(self.paper_dir, self.ledger_dir, self.schema_path)

    def test_duplicate_citation_key_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | sections/intro.md | ready_for_bibliography | None |
| key-1 | source-2 | claim-2 | sections/intro.md | ready_for_bibliography | None |
""")
        with self.assertRaises(SystemExit):
            validate_cross_repo(self.paper_dir, self.ledger_dir, self.schema_path)

    def test_missing_source_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | sections/intro.md | ready_for_bibliography | None |
""")
        self.write_section("intro.md", "This is a statement [@key-1].")
        self.write_claim("claim-1")
        
        with self.assertRaises(SystemExit):
            validate_cross_repo(self.paper_dir, self.ledger_dir, self.schema_path)

    def test_missing_claim_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | sections/intro.md | ready_for_bibliography | None |
""")
        self.write_section("intro.md", "This is a statement [@key-1].")
        self.write_source("source-1")
        
        with self.assertRaises(SystemExit):
            validate_cross_repo(self.paper_dir, self.ledger_dir, self.schema_path)

    def test_section_target_not_cited_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | sections/intro.md | ready_for_bibliography | None |
""")
        self.write_section("intro.md", "No citation here.")
        self.write_source("source-1")
        self.write_claim("claim-1")
        
        with self.assertRaises(SystemExit):
            validate_cross_repo(self.paper_dir, self.ledger_dir, self.schema_path)

    def test_mismatched_ledger_citation_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | sections/intro.md | ready_for_bibliography | None |
""")
        self.write_section("intro.md", "This is a statement [@key-1].")
        self.write_source("source-1")
        self.write_claim("claim-1")
        
        # Mismatched state: paper has ready_for_bibliography, ledger has missing_citation_detail
        self.write_citation("cit1.md", "cit-1", "source-1", "claim-1", "sections/intro.md", "missing_citation_detail", "needs pages")
        
        with self.assertRaises(SystemExit):
            validate_cross_repo(self.paper_dir, self.ledger_dir, self.schema_path)

    def test_na_fields_pass(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | N/A | N/A | N/A | ready_for_bibliography | None |
""")
        # N/A fields bypass existence checks, and since target is N/A, we don't need intro.md to cite it
        # Should pass
        validate_cross_repo(self.paper_dir, self.ledger_dir, self.schema_path)

    def test_invalid_yaml_in_citation_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | sections/intro.md | ready_for_bibliography | None |
""")
        self.write_section("intro.md", "This is a statement [@key-1].")
        self.write_source("source-1")
        self.write_claim("claim-1")
        
        # Write citation with invalid front matter (malformed yaml value)
        (self.ledger_dir / "citations" / "cit1.md").write_text("""---
citation_id: cit-1
source_id: source-1
claim_id: claim-1
paper_section_target: "sections/intro.md"
readiness_state: :invalid_colon
---
# Invalid
""", encoding="utf-8")
        
        with self.assertRaises(SystemExit):
            validate_cross_repo(self.paper_dir, self.ledger_dir, self.schema_path)

if __name__ == "__main__":
    unittest.main()
