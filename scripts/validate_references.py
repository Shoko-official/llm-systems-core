from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
import yaml
from jsonschema import validate, ValidationError

def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)

def parse_markdown_table(file_path: Path) -> list[dict]:
    if not file_path.is_file():
        fail(f"References index file not found: {file_path}")
    
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    
    headers = []
    rows = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line.startswith("|"):
            continue
        
        # Check if this is the header row
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if i + 1 < len(lines) and lines[i+1].strip().startswith("|---"):
            headers = [h.lower().replace(" ", "_") for h in parts]
            continue
        
        if line.startswith("|---") or not headers:
            continue
        
        # This is a data row
        row_dict = {}
        for idx, part in enumerate(parts):
            if idx < len(headers):
                val = part.replace("`", "").strip()
                row_dict[headers[idx]] = val
        
        if row_dict and not row_dict.get(headers[0], "").startswith("---"):
            rows.append(row_dict)
            
    return rows

def parse_front_matter(text: str) -> dict | None:
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except Exception as e:
        raise ValueError(f"YAML parsing error: {e}")

def validate_cross_repo(paper_dir: Path, ledger_dir: Path, schema_path: Path) -> None:
    if not paper_dir.is_dir():
        fail(f"Paper directory does not exist: {paper_dir}")
    if not ledger_dir.is_dir():
        fail(f"Ledger directory does not exist: {ledger_dir}")
    if not schema_path.is_file():
        fail(f"Schema file not found: {schema_path}")
        
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    index_path = paper_dir / "references" / "index.md"
    references = parse_markdown_table(index_path)
    
    # 1. Validate index rows against JSON schema
    citation_keys = set()
    ref_by_source_claim = {}
    
    for ref in references:
        key = ref.get("citation_key")
        if not key:
            fail("Reference row is missing citation_key")
            
        if key in citation_keys:
            fail(f"Duplicate citation key '{key}' in references/index.md")
        citation_keys.add(key)
        
        try:
            # We check if there's any bibtex fields to mock/test, but index doesn't have it.
            # jsonschema validate
            validate(instance=ref, schema=schema)
        except ValidationError as e:
            fail(f"Validation error for key '{key}': {e.message}")
            
        source_id = ref.get("ledger_source_id")
        claim_id = ref.get("ledger_claim_id")
        section_target = ref.get("paper_section_target")
        state = ref.get("readiness_state")
        detail = ref.get("missing_citation_detail")
        
        ref_by_source_claim[(source_id, claim_id)] = ref
        
        # 2. Check ledger alignment (sources and claims exist)
        if source_id and source_id != "N/A":
            source_file = ledger_dir / "sources" / f"{source_id}.md"
            if not source_file.is_file():
                fail(f"Source record '{source_id}' referenced by key '{key}' does not exist in ledger repository")
                
        if claim_id and claim_id != "N/A":
            claim_file = ledger_dir / "claims" / f"{claim_id}.md"
            if not claim_file.is_file():
                fail(f"Claim record '{claim_id}' referenced by key '{key}' does not exist in ledger repository")
                
        # 3. Check paper section target exists and contains the inline citation
        if section_target and section_target != "N/A":
            target_path = paper_dir / section_target
            if not target_path.is_file():
                fail(f"Section target '{section_target}' for key '{key}' does not exist in paper repository")
            
            # Read target and verify citation is present
            content = target_path.read_text(encoding="utf-8")
            inline_citations = re.findall(r"\[@([a-zA-Z0-9_\-]+)\]", content)
            if key not in inline_citations:
                fail(f"Citation key '{key}' lists target '{section_target}' but is not cited in that file")

    # 4. Check ledger citations alignment if citations directory exists
    citations_dir = ledger_dir / "citations"
    if citations_dir.is_dir():
        for path in citations_dir.glob("*.md"):
            if path.name.lower() == "readme.md":
                continue
            
            text = path.read_text(encoding="utf-8")
            try:
                front_matter = parse_front_matter(text)
            except Exception as e:
                fail(f"Invalid YAML front matter in ledger citations/{path.name}: {e}")
                
            if front_matter is None:
                fail(f"Missing YAML front matter in ledger citations/{path.name}")
                
            cit_id = front_matter.get("citation_id")
            src_id = front_matter.get("source_id")
            clm_id = front_matter.get("claim_id") or "N/A"
            sect_target = front_matter.get("paper_section_target") or "N/A"
            readiness = front_matter.get("readiness_state")
            miss_detail = front_matter.get("missing_citation_detail")
            
            # Match this ledger citation to references index
            # Ledger citation source/claim should match paper references source/claim
            ref_match = ref_by_source_claim.get((src_id, clm_id))
            if not ref_match:
                fail(f"Ledger citation '{cit_id}' (source='{src_id}', claim='{clm_id}') has no matching reference in paper index")
                
            # Verify alignment of fields
            if ref_match.get("paper_section_target") != sect_target:
                fail(f"Section target mismatch for ledger citation '{cit_id}': ledger has '{sect_target}', paper has '{ref_match.get('paper_section_target')}'")
                
            if ref_match.get("readiness_state") != readiness:
                fail(f"Readiness state mismatch for ledger citation '{cit_id}': ledger has '{readiness}', paper has '{ref_match.get('readiness_state')}'")
                
            # Compare detail (normalize None/null/N/A)
            ref_detail = ref_match.get("missing_citation_detail")
            norm_ref_detail = "" if ref_detail in (None, "None", "N/A", "null") else str(ref_detail).strip()
            norm_miss_detail = "" if miss_detail in (None, "None", "N/A", "null") else str(miss_detail).strip()
            if norm_ref_detail != norm_miss_detail:
                fail(f"Missing detail mismatch for ledger citation '{cit_id}': ledger has '{miss_detail}', paper has '{ref_detail}'")

    print("Cross-repo reference validation passed successfully.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Cross-repo reference validator")
    parser.add_argument("--paper-dir", type=str, help="Path to the paper repository")
    parser.add_argument("--ledger-dir", type=str, help="Path to the ledger repository")
    parser.add_argument("--schema", type=str, help="Path to the reference JSON schema")
    
    args = parser.parse_args()
    
    # Defaults
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent
    
    paper_path = Path(args.paper_dir) if args.paper_dir else root_dir.parent / "modern-llm-systems-paper"
    ledger_path = Path(args.ledger_dir) if args.ledger_dir else root_dir.parent / "llm-systems-research-ledger"
    schema_path = Path(args.schema) if args.schema else root_dir / "schemas" / "reference.json"
    
    validate_cross_repo(paper_path, ledger_path, schema_path)

if __name__ == "__main__":
    main()
