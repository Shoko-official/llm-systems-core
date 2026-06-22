#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KPI_TRACKER_PATH = ROOT / "docs" / "kpi-tracker.md"


def get_sibling_path(repo_name: str) -> Path:
    return ROOT.parent / repo_name


def parse_front_matter(text: str) -> dict | None:
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return None
    yaml_content = match.group(1)
    import yaml
    try:
        return yaml.safe_load(yaml_content)
    except Exception:
        return None


def compute_kpis() -> dict[str, str]:
    metrics: dict[str, str] = {}

    # 1. Research Ledger KPIs
    ledger_dir = get_sibling_path("llm-systems-research-ledger")
    if ledger_dir.is_dir():
        sources_dir = ledger_dir / "sources"
        claims_dir = ledger_dir / "claims"

        # research.structured_source_count
        if sources_dir.is_dir():
            source_files = [f for f in sources_dir.glob("*.md") if f.name.lower() != "readme.md"]
            metrics["research.structured_source_count"] = str(len(source_files))

        # research.structured_claim_count & research.evidence_needed_count & research.primary_source_claim_rate
        if claims_dir.is_dir():
            claim_files = [f for f in claims_dir.glob("*.md") if f.name.lower() != "readme.md"]
            metrics["research.structured_claim_count"] = str(len(claim_files))

            evidence_needed = 0
            for cf in claim_files:
                try:
                    text = cf.read_text(encoding="utf-8")
                    data = parse_front_matter(text)
                    if data and data.get("status") == "evidence_needed":
                        evidence_needed += 1
                except Exception:
                    pass
            metrics["research.evidence_needed_count"] = str(evidence_needed)

    # 2. Paper KPIs
    paper_dir = get_sibling_path("modern-llm-systems-paper")
    if paper_dir.is_dir():
        sections_dir = paper_dir / "sections"
        if sections_dir.is_dir():
            section_files = [
                f for f in sections_dir.glob("*.md") if f.name != "README.md"
            ]
            metrics["paper.sections_created"] = str(len(section_files))

            drafted = 0
            for sf in section_files:
                try:
                    text = sf.read_text(encoding="utf-8")
                    if "Draft status: Not drafted." not in text:
                        drafted += 1
                except Exception:
                    pass
            metrics["paper.sections_drafted"] = str(drafted)

    return metrics


def parse_kpi_tracker() -> tuple[list[str], list[dict[str, str]]]:
    if not KPI_TRACKER_PATH.is_file():
        print(f"Error: {KPI_TRACKER_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    lines = KPI_TRACKER_PATH.read_text(encoding="utf-8").splitlines()
    kpis: list[dict[str, str]] = []

    # Regex to match table rows: | `id` | KPI | Status | Value | Source | Notes |
    row_pattern = re.compile(
        r"^\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|"
    )

    for i, line in enumerate(lines):
        match = row_pattern.match(line)
        if match:
            kpi_id = match.group(1).strip()
            kpis.append(
                {
                    "line_index": i,
                    "id": kpi_id,
                    "name": match.group(2).strip(),
                    "status": match.group(3).strip(),
                    "value": match.group(4).strip(),
                    "source": match.group(5).strip(),
                    "notes": match.group(6).strip(),
                }
            )

    return lines, kpis


def update_kpi_tracker(lines: list[str], kpis: list[dict[str, str]], computed: dict[str, str]) -> str:
    new_lines = list(lines)
    for kpi in kpis:
        kpi_id = kpi["id"]
        if kpi_id in computed:
            new_val = computed[kpi_id]
            idx = kpi["line_index"]
            line = lines[idx]

            # Reconstruct the line replacing the old value
            parts = [p.strip() for p in line.split("|")]
            # parts looks like: ['', '`id`', 'Name', 'Status', 'Value', 'Source', 'Notes', '']
            if len(parts) >= 8:
                parts[4] = new_val
                new_line = " | ".join(parts).strip()
                if not new_line.startswith("|"):
                    new_line = "| " + new_line
                if not new_line.endswith("|"):
                    new_line = new_line + " |"
                new_lines[idx] = new_line
    return "\n".join(new_lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check/Update KPI tracker")
    parser.add_argument("--update", action="store_true", help="Update kpi-tracker.md with computed values")
    parser.add_argument("--check", action="store_true", help="Check if kpi-tracker.md values match computed values")
    args = parser.parse_args()

    lines, kpis = parse_kpi_tracker()
    computed = compute_kpis()

    if not kpis:
        print("Error: No KPIs found in tracker file.", file=sys.stderr)
        return 1

    if args.update:
        updated_content = update_kpi_tracker(lines, kpis, computed)
        KPI_TRACKER_PATH.write_text(updated_content, encoding="utf-8")
        print("KPI tracker updated successfully.")
        return 0

    if args.check:
        discrepancies = []
        for kpi in kpis:
            kpi_id = kpi["id"]
            if kpi_id in computed:
                expected = computed[kpi_id]
                actual = kpi["value"]
                if actual != expected:
                    discrepancies.append(
                        f"KPI '{kpi_id}': expected '{expected}' (computed), got '{actual}' in tracker."
                    )

        if discrepancies:
            print("KPI Discrepancies found:", file=sys.stderr)
            for d in discrepancies:
                print(f"  - {d}", file=sys.stderr)
            print("\nRun: python scripts/check_kpis.py --update to resolve.", file=sys.stderr)
            return 1
        else:
            print("KPI validation passed. No discrepancies found.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
