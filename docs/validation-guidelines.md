# Validation Guidelines

This document outlines the validation architecture for the Shoko-official repositories, specifically focusing on schema validation and KPI tracking.

## Overview

The repository validation framework ensures that all core schemas, documentation, and project KPIs remain consistent and free of drift. 

Validation is divided into two primary areas:
1. **Schema Validation**: Ensuring that the JSON schemas (`source.json`, `claim.json`) are valid Draft-07 schemas.
2. **KPI Validation**: Verifying that the KPIs tracked in `docs/kpi-tracker.md` are correctly formatted and reflect the actual state of the repositories.

## Validation Execution

To run validation checks locally:

```bash
# Validate files, paths, schemas, and KPIs
python scripts/validate_repo.py validate

# Lint files for secrets and formatting issues
python scripts/validate_repo.py lint

# Run all checks
python scripts/validate_repo.py test
```

## Adding New Schemas

When defining a new data structure schema:

1. Create a new JSON schema file in the `schemas/` directory (e.g., `schemas/my_schema.json`).
2. Ensure the schema defines `"$schema": "http://json-schema.org/draft-07/schema#"` and has correct Draft-07 properties.
3. Update `schemas/README.md` to list the new schema.
4. Add the new schema filename to the list of validated schemas in `scripts/validate_repo.py`:

```python
# Inside scripts/validate_repo.py
def validate_schemas() -> None:
    # ...
    for schema_name in ["source.json", "claim.json", "my_schema.json"]:
        # ...
```

## Adding and Updating KPIs

To register a new program KPI:

1. Locate the appropriate section in `docs/kpi-tracker.md`.
2. Add a new row to the table using the format:
   ```markdown
   | `my_repo.my_kpi` | KPI Name | active | TBD | Source Description | Notes |
   ```
3. If the KPI value can be automatically computed, add a parser/counter logic inside `scripts/check_kpis.py`:
   - Define a helper function to inspect files, counts, or fields.
   - Map the computed value to the matching KPI ID in `compute_kpis()`.
4. Update the tracker file using the automated script:
   ```bash
   python scripts/check_kpis.py --update
   ```

## Cross-Repository Schema Validation

To prevent schema drift and inconsistency across repositories, the validation framework includes a cross-repository schema mismatch checker. This checker runs automatically when the sibling repository `llm-systems-research-ledger` is checked out in the parent directory.

### Mapping Schema Properties

The checker verifies that schemas defined in `llm-systems-core/schemas/` are structurally compatible with the implementation schemas in `llm-systems-research-ledger/schemas/`. The property mappings are:

* **Source Schemas (`source.json`)**:
  - `id` &rarr; `source_id`
  - `title` &rarr; `title`
  - `url` &rarr; `locator`
  - `type` &rarr; `evidence_class`
  - `author` &rarr; `authors`
  - `published_date` &rarr; `year`

* **Claim Schemas (`claim.json`)**:
  - `id` &rarr; `claim_id`
  - `claim` &rarr; `claim_text`
  - `source_ids` &rarr; `source_references`
  - `status` &rarr; `status`
  - `notes` &rarr; `review_notes`

* **Reference vs. Citation Schemas (`reference.json` &rarr; `citation.json`)**:
  - `citation_key` &rarr; `citation_id`
  - `ledger_source_id` &rarr; `source_id`
  - `ledger_claim_id` &rarr; `claim_id`
  - `paper_section_target` &rarr; `paper_section_target`
  - `readiness_state` &rarr; `readiness_state`
  - `missing_citation_detail` &rarr; `missing_citation_detail`

### Compatibility Verification Rules

The checker enforces the following business logic:
1. **Property Existence**: Mapped properties defined in the core repository schemas must exist in the target ledger repository schemas.
2. **Type Compatibility**: Mapped property types must match or be compatible (e.g. `string` is compatible with `["string", "null"]`, and `published_date` (string) is compatible with `year` (integer)).
3. **Required Constraints**: If a property is required in the core repository schema, its mapped counterpart in the ledger repository schema must also be marked required.

## Automated KPI Updater Daemon

To keep the program-level metrics synchronized across files and repositories, an automated KPI updater script is provided.

The updater script:
1. Runs the KPI computation tool (`python scripts/check_kpis.py --update`).
2. Checks if there are any modifications made to `docs/kpi-tracker.md`.
3. If changes exist, stages them, commits with `chore: auto-update KPI tracker [skip ci]`, and pushes them to the remote repository.
4. Pauses/sleeps for a randomized duration between 32 minutes and 2 hours to avoid burst commits, before initiating the next check.

### Running the Daemon

To run the KPI updater background service, use the provided Makefile target:

```bash
make schedule-kpis
```

