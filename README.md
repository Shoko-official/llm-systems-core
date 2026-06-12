# LLM Systems Core

`llm-systems-core` contains the shared governance and coordination foundation for the Modern LLM Systems 2026 / arXiv Report program.

This repository is not a product implementation repository. It exists to keep the cross-repository operating model consistent before domain work starts in research, paper writing, evaluation, RAG, inference, safety, observability, memory, and agent repositories.

## Program Role

This repository owns:

* project governance rules;
* shared contribution workflow;
* cross-repository milestone coordination;
* global anti-drift rules;
* KPI tracking conventions;
* shared schema and validation foundations when they are introduced by dedicated issues.

The central project board is:

* [Modern LLM Systems 2026 / arXiv Report](https://github.com/users/Shoko-official/projects/4)

## Current Scope

Milestone 0 is limited to project governance.

Included:

* governance documentation;
* issue and MR/PR templates;
* minimal validation commands;
* minimal CI;
* folder structure;
* branch and review rules;
* initial KPI tracker.

Out of scope:

* LLM architecture taxonomies;
* research claims and sources;
* paper drafting;
* RAG;
* inference benchmarking;
* agents;
* memory;
* GraphRAG;
* security frameworks;
* observability pipelines;
* training and alignment experiments.

## Required Workflow

All work must follow this sequence:

1. Issue
2. Short plan
3. Local branch
4. Local changes
5. Local validation
6. Diff presented for review
7. Maintainer approval to push
8. Branch push
9. MR/PR creation
10. CI review
11. Maintainer approval to merge
12. Merge

No branch may be pushed before the diff has been reviewed and approved.

No MR/PR may be merged without explicit final approval.

## Repository Order

The program advances sequentially. The initial order is:

1. `llm-systems-core`
2. `llm-systems-research-ledger`
3. `modern-llm-systems-paper`

Later repositories must not start until the required foundations are validated.

## Figure and Diagram Policy

Figures and diagrams must be traceable and reproducible.

Allowed source formats:

* Mermaid text diagrams for architecture, workflows, dependency graphs, state diagrams, and conceptual maps.
* Python-generated images for quantitative charts, visual tables, and paper figures that are not practical in Mermaid.
* Relevant and copyright-free images.

Temporary Python scripts used to generate figures must not be committed unless a dedicated issue explicitly approves long-term reproducibility storage under `scripts/figures/`.


## License

This repository is licensed under the Apache License 2.0. See [LICENSE](LICENSE).
