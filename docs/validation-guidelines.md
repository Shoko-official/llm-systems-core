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
