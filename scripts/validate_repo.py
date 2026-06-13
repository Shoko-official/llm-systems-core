from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

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
    "schemas/README.md",
    "tests/README.md",
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


def lint_text() -> None:
    for path in iter_text_files():
        text = read_text(path)
        relative = path.relative_to(ROOT)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible secret in {relative}: {pattern.pattern}")


def run_validate() -> None:
    validate_required_paths()
    validate_repository_profile()
    validate_kpi_registry()
    validate_milestone_transition_gates()


def run_lint() -> None:
    lint_text()


def run_test() -> None:
    run_validate()
    run_lint()


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
