# Milestone Transition Gates

This document defines when the program may move from one repository or milestone to the next.

## Default Rule

Open the next repository or milestone only when the current gate is satisfied, the relevant issues are closed, and the project board reflects the completed state.

## Core to Research Ledger

The program may expand `llm-systems-research-ledger` after `llm-systems-core` Milestone 1 is closed.

Required state:

* repository profile is present and validated;
* KPI registry is present and validated;
* transition gates are documented;
* CI is green on the closing PR;
* no Milestone 1 issue remains open in `llm-systems-core`.

Allowed next work:

* research ledger source structure;
* research ledger claim structure;
* citation and evidence rules.

Not allowed yet:

* paper drafting;
* RAG implementation;
* agent runtime;
* memory layer.

## Research Ledger to Paper

The program may expand `modern-llm-systems-paper` after the research ledger has a minimal source and claim structure.

Required state:

* source records have a stable format;
* claim records have a stable format;
* unsupported claims can be marked `TODO:evidence_needed`;
* citation handoff rules are documented;
* validation is available for the ledger structure.

## Evaluation Before RAG

RAG work may start only after a retrieval evaluation baseline exists.

Required state:

* a minimal evaluation dataset exists;
* recall@5 and recall@10 can be measured;
* citation accuracy has an initial definition;
* permission failure cases are represented.

## Policy Before Agents

Agent runtime work may start only after basic policy and trace expectations exist.

Required state:

* tool-call traces are required;
* action budgets are defined;
* verifier expectations are documented;
* unsafe actions have a blocking rule.

## Provenance Before Memory

Persistent memory work may start only after provenance and deletion expectations exist.

Required state:

* memory entries have provenance;
* TTL is defined;
* revocation is supported;
* stale or deleted memory cannot be reused silently.

## Changing the Order

Changing the sequence requires a dedicated issue with rationale, impact, risks, and maintainer approval.
