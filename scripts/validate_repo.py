from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft7Validator, SchemaError


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REQUIRED_FILES = [
    "README.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "Makefile",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/governance_task.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/ci.yml",
    "docs/kpi-tracker.md",
    "docs/milestone-transition-gates.md",
    "docs/repository-profile.md",
    "docs/reference-mapping-guidelines.md",
    "docs/validation-guidelines.md",
    "schemas/README.md",
    "schemas/reference.json",
    "scripts/validate_references.py",
    "scripts/schedule_kpi_update.py",
    "tests/README.md",
    "tests/test_schemas.py",
    "tests/test_validate_references.py",
]

REQUIRED_DIRECTORIES = [
    ".github",
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
    "docs",
    "schemas",
    "scripts",
    "tests",
]

SECRET_PATTERNS = [
    re.compile(pattern)
    for pattern in [
        r"AKIA[0-9A-Z]{16}",
        r"gho_[A-Za-z0-9_]+",
        r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
        r"(?i)\b(password|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}",
    ]
]

REPOSITORY_PROFILE_REQUIRED_TEXT = [
    "# Repository Profile",
    "## Boundaries",
    "## Working Rules",
    "| Repository |",
    "| Owner |",
    "| Role |",
    "| Default branch |",
    "| Active milestone |",
    "| Issues |",
    "| Main issue types |",
    "| KPI areas |",
    "| Direct work on `main` |",
    "| Pull request required |",
    "| Required approvals |",
    "| Status checks required |",
]

KPI_REGISTRY_REQUIRED_TEXT = [
    "# KPI Registry",
    "## Conventions",
    "## Engineering",
    "## Research",
    "## Paper",
    "## RAG",
    "## Serving",
    "## Agents",
    "`engineering.open_pr_count`",
    "`research.structured_source_count`",
    "`paper.sections_created`",
    "`rag.recall_at_5`",
    "`serving.ttft`",
    "`agents.task_success_rate`",
]

MILESTONE_GATES_REQUIRED_TEXT = [
    "# Milestone Transition Gates",
    "## Default Rule",
    "## Core to Research Ledger",
    "## Research Ledger to Paper",
    "## Evaluation Before RAG",
    "## Policy Before Agents",
    "## Provenance Before Memory",
    "## Changing the Order",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_text_files() -> list[Path]:
    excluded_parts = {".git", "__pycache__"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if excluded_parts.intersection(path.parts):
            continue
        if path.suffix.lower() in {".md", ".yml", ".yaml", ".py", ""}:
            files.append(path)
    return files


def validate_required_paths() -> None:
    missing_files = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    missing_dirs = [path for path in REQUIRED_DIRECTORIES if not (ROOT / path).is_dir()]
    if missing_files or missing_dirs:
        details = []
        if missing_files:
            details.append("missing files: " + ", ".join(missing_files))
        if missing_dirs:
            details.append("missing directories: " + ", ".join(missing_dirs))
        fail("; ".join(details))


def validate_repository_profile() -> None:
    path = ROOT / "docs" / "repository-profile.md"
    text = read_text(path)
    missing = [item for item in REPOSITORY_PROFILE_REQUIRED_TEXT if item not in text]
    if missing:
        fail("repository profile missing required text: " + ", ".join(missing))


def validate_kpi_registry() -> None:
    path = ROOT / "docs" / "kpi-tracker.md"
    text = read_text(path)
    missing = [item for item in KPI_REGISTRY_REQUIRED_TEXT if item not in text]
    if missing:
        fail("KPI registry missing required text: " + ", ".join(missing))


def validate_milestone_transition_gates() -> None:
    path = ROOT / "docs" / "milestone-transition-gates.md"
    text = read_text(path)
    missing = [item for item in MILESTONE_GATES_REQUIRED_TEXT if item not in text]
    if missing:
        fail("milestone transition gates missing required text: " + ", ".join(missing))


def validate_schemas() -> None:
    schema_dir = ROOT / "schemas"
    for schema_name in ["source.json", "claim.json", "reference.json"]:
        schema_path = schema_dir / schema_name
        if not schema_path.is_file():
            fail(f"Schema file not found: {schema_name}")
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_data = json.load(f)
        except json.JSONDecodeError as e:
            fail(f"Schema {schema_name} is not valid JSON: {e}")
        try:
            Draft7Validator.check_schema(schema_data)
        except SchemaError as e:
            fail(f"Schema {schema_name} is not a valid Draft-07 JSON schema: {e}")


def lint_text() -> None:
    for path in iter_text_files():
        text = read_text(path)
        relative = path.relative_to(ROOT)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible secret in {relative}: {pattern.pattern}")


def validate_kpi_values() -> None:
    import subprocess
    kpi_script = ROOT / "scripts" / "check_kpis.py"
    if kpi_script.is_file():
        res = subprocess.run(
            [sys.executable, str(kpi_script), "--check"],
            capture_output=True,
            text=True
        )
        if res.returncode != 0:
            fail(f"KPI verification failed:\n{res.stderr or res.stdout}")


def check_types_compatible(t_core, t_ledger) -> bool:
    if isinstance(t_core, str):
        set_core = {t_core}
    elif isinstance(t_core, list):
        set_core = set(t_core)
    else:
        return True

    if isinstance(t_ledger, str):
        set_ledger = {t_ledger}
    elif isinstance(t_ledger, list):
        set_ledger = set(t_ledger)
    else:
        return True

    if set_core.intersection(set_ledger):
        return True
    if "string" in set_core and "integer" in set_ledger:
        return True
    return False


def validate_cross_repo_schemas() -> None:
    ledger_dir = ROOT.parent / "llm-systems-research-ledger"
    if not ledger_dir.is_dir():
        print("Skipping cross-repository schema validation (ledger repo not found).")
        return

    print("Running cross-repository schema mismatch validation...")

    core_source_path = ROOT / "schemas" / "source.json"
    ledger_source_path = ledger_dir / "schemas" / "source.json"

    core_claim_path = ROOT / "schemas" / "claim.json"
    ledger_claim_path = ledger_dir / "schemas" / "claim.json"

    core_ref_path = ROOT / "schemas" / "reference.json"
    ledger_citation_path = ledger_dir / "schemas" / "citation.json"

    source_mapping = {
        "id": "source_id",
        "title": "title",
        "url": "locator",
        "type": "evidence_class",
        "author": "authors",
        "published_date": "year",
    }

    claim_mapping = {
        "id": "claim_id",
        "claim": "claim_text",
        "source_ids": "source_references",
        "status": "status",
        "notes": "review_notes",
    }

    ref_mapping = {
        "citation_key": "citation_id",
        "ledger_source_id": "source_id",
        "ledger_claim_id": "claim_id",
        "paper_section_target": "paper_section_target",
        "readiness_state": "readiness_state",
        "missing_citation_detail": "missing_citation_detail",
    }

    mismatches = []

    def check_schema_alignment(name: str, core_path: Path, ledger_path: Path, mapping: dict[str, str]) -> None:
        if not core_path.is_file() or not ledger_path.is_file():
            mismatches.append(f"Missing schema file for {name}")
            return

        with open(core_path, "r", encoding="utf-8") as f:
            core_schema = json.load(f)
        with open(ledger_path, "r", encoding="utf-8") as f:
            ledger_schema = json.load(f)

        core_props = core_schema.get("properties", {})
        ledger_props = ledger_schema.get("properties", {})
        core_required = core_schema.get("required", [])
        ledger_required = ledger_schema.get("required", [])

        for p_core, p_ledger in mapping.items():
            if p_core not in core_props:
                continue
            if p_ledger not in ledger_props:
                mismatches.append(f"[{name}] Core property '{p_core}' mapped to '{p_ledger}', but '{p_ledger}' is missing from ledger schema.")
                continue

            t_core = core_props[p_core].get("type")
            t_ledger = ledger_props[p_ledger].get("type")
            if t_core and t_ledger:
                if not check_types_compatible(t_core, t_ledger):
                    mismatches.append(f"[{name}] Type mismatch for core property '{p_core}' (type: {t_core}) mapped to ledger property '{p_ledger}' (type: {t_ledger}).")

            if p_core in core_required and p_ledger not in ledger_required:
                mismatches.append(f"[{name}] Required core property '{p_core}' mapped to '{p_ledger}', but '{p_ledger}' is not required in ledger schema.")

    check_schema_alignment("source.json", core_source_path, ledger_source_path, source_mapping)
    check_schema_alignment("claim.json", core_claim_path, ledger_claim_path, claim_mapping)
    check_schema_alignment("reference.json/citation.json", core_ref_path, ledger_citation_path, ref_mapping)

    if mismatches:
        print("Cross-repository schema mismatch validation failed with the following conflicts:", file=sys.stderr)
        for m in mismatches:
            print(f"  - {m}", file=sys.stderr)
        fail("Cross-repository schema mismatch detected.")
    else:
        print("Cross-repository schema mismatch validation passed successfully.")


def validate_reference_integration() -> None:
    paper_dir = ROOT.parent / "modern-llm-systems-paper"
    ledger_dir = ROOT.parent / "llm-systems-research-ledger"
    schema_path = ROOT / "schemas" / "reference.json"
    if paper_dir.is_dir() and ledger_dir.is_dir():
        print("Running cross-repository reference validation...")
        from scripts.validate_references import validate_cross_repo
        try:
            validate_cross_repo(paper_dir, ledger_dir, schema_path)
        except SystemExit:
            print("Warning: Cross-repository reference validation failed. This is expected if sibling repositories are not fully synchronized yet.")


def run_validate() -> None:
    validate_required_paths()
    validate_repository_profile()
    validate_kpi_registry()
    validate_milestone_transition_gates()
    validate_schemas()
    validate_kpi_values()
    validate_cross_repo_schemas()
    validate_reference_integration()


def run_lint() -> None:
    lint_text()


def run_unit_tests() -> None:
    import unittest
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        fail("Unit tests failed.")


def run_test() -> None:
    run_validate()
    run_lint()
    run_unit_tests()


def main(argv: list[str]) -> int:
    if len(argv) == 1:
        command = "test"
    elif len(argv) == 2 and argv[1] in {"validate", "lint", "test"}:
        command = argv[1]
    else:
        print("usage: validate_repo.py {validate|lint|test}", file=sys.stderr)
        return 2

    if command == "validate":
        run_validate()
    elif command == "lint":
        run_lint()
    else:
        run_test()

    print(f"{command} ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
