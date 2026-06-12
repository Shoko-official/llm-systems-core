# Contributing

This repository uses a strict small-change workflow. The goal is to make every change reviewable, reversible, and tied to a real issue.

## Language

Repository artifacts must be written in English unless a dedicated issue explicitly requires another language.

## Workflow

Every change must follow this sequence:

1. Start from an existing issue.
2. Summarize the objective, scope, files, risks, validation commands, and estimated MR/PR size.
3. Create a local branch from `main`.
4. Make local changes only.
5. Run the narrowest relevant checks.
6. Review the diff locally.
7. Present the diff for review.
8. Wait for explicit approval before pushing.
9. Push the branch only after approval.
10. Open an MR/PR linked to the issue.
11. Wait for CI.
12. Request final approval before merge.

Direct work on `main` is forbidden after repository bootstrap.

## Branch Naming

Use one of these branch patterns:

* `feat/<repo>/<issue-id>-short-name`
* `docs/<repo>/<issue-id>-short-name`
* `fix/<repo>/<issue-id>-short-name`
* `eval/<repo>/<issue-id>-short-name`

Examples:

* `docs/core/1-governance-docs`
* `docs/core/2-issue-pr-templates`
* `feat/core/3-minimal-validation`

## MR/PR Size

Target size:

* ideal: 100 to 500 changed lines;
* maximum: 800 changed lines, excluding generated files.

If a change exceeds the maximum, split it into multiple issues or multiple MR/PRs before pushing.

## Review Rules

Before presenting a diff, verify:

* the issue scope is respected;
* no opportunistic refactor is included;
* no secret, token, credential, or private data is present;
* documentation is updated when required;
* schemas are versioned when schema work is in scope;
* validation commands were run or a clear reason is documented.

Before merge, verify:

* the MR/PR is linked to an issue;
* CI is green or the failure is explicitly accepted by the reviewer;
* acceptance criteria are met;
* the final merge has explicit maintainer approval.

## Issue Closing Rules

Use closing keywords only when the MR/PR fully completes the issue:

* `Closes #123`
* `Fixes #123`
* `Resolves #123`

Use non-closing references when the MR/PR is partial:

* `Refs #123`
* `Related to #123`
* `Part of #123`

Never invent an issue number. Create the issue first or ask for confirmation.

## Anti-Drift Rules

Do not:

* make large commits;
* work directly on `main`;
* push before diff review;
* merge without explicit approval;
* develop several major repositories in parallel;
* add heavy dependencies without a dedicated issue;
* mix refactors with features;
* add research claims without a source or `TODO:evidence_needed`;
* start RAG before retrieval evaluation exists;
* start agent work before budget, verifier, trace, and policy exist;
* add persistent memory before provenance, TTL, and revocation exist;
* add benchmarks without a minimal dataset;
* commit secrets, credentials, private data, or sensitive logs;
* ignore broken CI;
* change schemas without validation tests.

## Figures and Diagrams

Allowed source formats:

* Mermaid text files or Mermaid blocks.
* Python-generated image outputs.

External images, screenshots, manual drawings, and design-tool exports require explicit approval.

Temporary Python scripts used to generate images must be deleted after generation unless a dedicated issue approves keeping them under `scripts/figures/` for reproducibility.

Figure files must have clear names, such as:

* `figures/system_stack_overview.png`
* `figures/rag_pipeline.mmd`
* `figures/kv_cache_memory_curve.png`

Names such as `image1.png`, `test.png`, `final_final.png`, or `diagram_ok.png` are not acceptable.

## Validation

Milestone 0 will introduce the standard commands:

```bash
make validate
make lint
make test
```

Until the Makefile exists, document that these commands are not yet available and run the checks that are possible for the current issue.
