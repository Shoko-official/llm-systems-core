# Reference Mapping Guidelines

This document outlines the rules and procedures for adding, updating, and citing sources across the Shoko-official repositories to maintain consistency between the research ledger and the paper repository.

## Overview

The reference mapping model ensures that every claim made in the paper is backed by a verified source and tracked in the research ledger. This is achieved via a synchronized handoff flow between:
1. `llm-systems-research-ledger` (captures source identity, claims, and readiness states).
2. `modern-llm-systems-paper` (maps keys, target sections, and generates bibliography).

---

## Adding a Reference

To add a new reference to the program:

1. **Create the Source Record**:
   - Add a source file in `llm-systems-research-ledger/sources/source-<id>.md`.
   - Ensure it conforms to the `source.json` schema.

2. **Create the Claim Record**:
   - Add a claim file in `llm-systems-research-ledger/claims/claim-<id>.md`.
   - Conforms to the `claim.json` schema.
   - List the new `source_id` in its `source_references`.

3. **Register the Citation in the Ledger**:
   - Add a citation file in `llm-systems-research-ledger/citations/citation-<id>.md`.
   - Conforms to the `citation.json` schema.
   - Link the `source_id`, `claim_id`, target `paper_section_target`, and state.

4. **Register the Reference in the Paper**:
   - Add the matching entry to the table in `modern-llm-systems-paper/references/index.md`.
   - Ensure the `Citation Key`, `Ledger Source ID`, `Ledger Claim ID`, and other fields align exactly with the ledger.

---

## Updating a Reference

When updating an existing reference or changing its readiness:

1. **Readiness State Changes**:
   - Supported readiness states are:
     - `ready_for_bibliography`
     - `missing_citation_detail`
     - `missing_evidence`
     - `blocked`
   - If the state transitions to `ready_for_bibliography`, set the `missing_citation_detail` to `None` in both the ledger citation record and the paper reference index.
   - If the state is `missing_citation_detail`, provide clear, actionable details in both locations.

2. **Sync Requirements**:
   - Changes to citation readiness must be made in tandem across the ledger repository and the paper repository to prevent cross-repo validation failures.

---

## Citing a Reference

To cite a reference in the paper:

1. **Inline Citation Format**:
   - Use the format `[@citation_key]` in the markdown files located in `sections/` or `paper/main.md`.
   - The `citation_key` must match a registered key in `references/index.md`.

2. **Target Alignment**:
   - The citation key must appear in the section file specified by the reference's `paper_section_target`.

---

## Validation and Integrity Checks

Run the validation suite locally to ensure cross-repository compliance:

```bash
# Run local validation
python scripts/validate_repo.py test

# Run cross-repo reference validation
python scripts/validate_references.py --paper-dir ../modern-llm-systems-paper --ledger-dir ../llm-systems-research-ledger
```
