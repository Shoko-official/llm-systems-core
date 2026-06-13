# Roadmap

This roadmap is intentionally limited to governance-level work. Domain implementation belongs in later milestones and dedicated repositories.

## Milestone 0: Project Governance

Goal: establish a small, reviewable operating model for the first three repositories.

Initial repositories:

1. `llm-systems-core`
2. `llm-systems-research-ledger`
3. `modern-llm-systems-paper`

### Core Repository Issues

1. [#1 Create core governance documentation](https://github.com/Shoko-official/llm-systems-core/issues/1)
2. [#2 Add issue and MR templates](https://github.com/Shoko-official/llm-systems-core/issues/2)
3. [#3 Add minimal validation, CI, folder structure, and KPI tracker](https://github.com/Shoko-official/llm-systems-core/issues/3)

### Execution Order

1. Complete `llm-systems-core` issue #1.
2. Complete `llm-systems-core` issue #2.
3. Complete `llm-systems-core` issue #3.
4. Move to `llm-systems-research-ledger` issue #1.
5. Continue sequentially through the research ledger governance issues.
6. Move to `modern-llm-systems-paper` only after the ledger governance base is validated.

No major repository work should run in parallel during Milestone 0.

## Acceptance Criteria

Milestone 0 is complete when:

* each initial repository has governance documentation;
* each initial repository has issue and MR/PR templates;
* each initial repository has minimal validation commands;
* each initial repository has minimal CI;
* each initial repository has branch and review rules;
* `llm-systems-core` has an initial KPI tracker;
* every MR/PR is small, linked to an issue, reviewed, and merged only after explicit approval.

## Later Milestones

Later milestones are placeholders until Milestone 0 is complete.

Transition criteria are tracked in [Milestone Transition Gates](docs/milestone-transition-gates.md).

Expected sequence:

1. Core schemas and shared validation foundations.
2. Research ledger source and claim structure.
3. Paper skeleton and citation flow.
4. Architecture taxonomy.
5. Decision matrix.
6. Evaluation harness.
7. RAG reference only after retrieval evaluation exists.
8. Serving and inference benchmarks.
9. Security governance.
10. Observability and telemetry.
11. Memory layer with provenance, TTL, and revocation.
12. Agent runtime with budget, verifier, trace, and policy.

The sequence may change only with an explicit issue, rationale, and maintainer approval.
