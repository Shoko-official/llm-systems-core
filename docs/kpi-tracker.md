# KPI Registry

This registry defines the program-level KPI names used across repositories. Values stay `TBD` until a repository has a real measurement source.

## Conventions

| Field | Meaning |
|---|---|
| ID | Stable identifier used in issues, PRs, reports, and future automation. |
| KPI | Human-readable name. |
| Status | `active` when the current repositories can track it, `future` when the required repo or harness does not exist yet. |
| Value | Current value, or `TBD` when measurement is not available. |
| Source | Expected source of truth. |

## Engineering

| ID | KPI | Status | Value | Source | Notes |
|---|---|---|---|---|---|
| `engineering.open_pr_count` | Open PR count | active | TBD | GitHub project | Count active review work across initial repositories. |
| `engineering.median_pr_size` | Median PR size | active | TBD | GitHub pull requests | Track changed lines excluding generated files when possible. |
| `engineering.green_ci_rate` | Green CI rate | active | TBD | GitHub Actions | Track after CI exists in each repository. |
| `engineering.issue_to_pr_time` | Average issue to PR time | active | TBD | GitHub issues and pull requests | Track once the workflow is stable. |
| `engineering.blocked_issue_count` | Blocked issue count | active | TBD | GitHub project | Count issues explicitly marked blocked. |
| `engineering.test_coverage` | Test coverage | future | TBD | Repository-specific tooling | Record only when meaningful coverage tooling exists. |

## Research

| ID | KPI | Status | Value | Source | Notes |
|---|---|---|---|---|---|
| `research.structured_source_count` | Structured source count | future | 13 | Research ledger | Introduced after ledger schema work. |
| `research.structured_claim_count` | Structured claim count | future | 15 | Research ledger | Introduced after ledger schema work. |
| `research.primary_source_claim_rate` | Claims with primary source | future | TBD | Research ledger | Percentage of claims backed by primary sources. |
| `research.evidence_needed_count` | Claims marked `TODO:evidence_needed` | future | 0 | Research ledger | Must decrease as evidence is added. |
| `research.missing_citation_count` | Missing citations | future | TBD | Research ledger and paper | Track before paper drafting expands. |

## Paper

| ID | KPI | Status | Value | Source | Notes |
|---|---|---|---|---|---|
| `paper.sections_created` | Sections created | future | 12 | Paper repository | Count section files or paper outline entries. |
| `paper.sections_drafted` | Sections drafted | future | 12 | Paper repository | Count sections with draft content. |
| `paper.sections_reviewed` | Sections reviewed | future | TBD | Paper repository | Count reviewed sections. |
| `paper.figures_generated` | Figures generated | future | TBD | Paper repository | Count reproducible figures only. |
| `paper.tables_generated` | Tables generated | future | TBD | Paper repository | Count paper-ready tables. |
| `paper.latex_compilation` | LaTeX compilation | future | TBD | Paper CI | Track pass/fail after build setup. |
| `paper.missing_citation_count` | Missing citations | future | TBD | Paper validation | Track unresolved citation markers. |
| `paper.remaining_todo_count` | Remaining TODOs | future | TBD | Paper validation | Track paper TODO markers. |

## RAG

| ID | KPI | Status | Value | Source | Notes |
|---|---|---|---|---|---|
| `rag.recall_at_5` | recall@5 | future | TBD | Evaluation harness | Not available before retrieval evaluation exists. |
| `rag.recall_at_10` | recall@10 | future | TBD | Evaluation harness | Not available before retrieval evaluation exists. |
| `rag.precision_at_k` | precision@k | future | TBD | Evaluation harness | Not available before retrieval evaluation exists. |
| `rag.mrr` | MRR | future | TBD | Evaluation harness | Not available before retrieval evaluation exists. |
| `rag.citation_accuracy` | Citation accuracy | future | TBD | Evaluation harness | Requires citation evaluation data. |
| `rag.groundedness` | Groundedness | future | TBD | Evaluation harness | Requires groundedness checks. |
| `rag.p95_latency` | p95 latency | future | TBD | RAG benchmark | Requires benchmark harness. |
| `rag.permission_failure_rate` | Permission failure rate | future | TBD | RAG benchmark | Requires permission model tests. |

## Serving

| ID | KPI | Status | Value | Source | Notes |
|---|---|---|---|---|---|
| `serving.ttft` | TTFT | future | TBD | Serving benchmark | Introduced in serving benchmark repository. |
| `serving.tpot` | TPOT | future | TBD | Serving benchmark | Introduced in serving benchmark repository. |
| `serving.throughput` | Throughput | future | TBD | Serving benchmark | Requests or tokens per second. |
| `serving.p95_p99_latency` | p95/p99 latency | future | TBD | Serving benchmark | Requires benchmark dataset. |
| `serving.vram` | VRAM | future | TBD | Serving benchmark | GPU memory measurement. |
| `serving.cost_per_request` | Cost per request | future | TBD | Serving benchmark | Requires pricing assumptions. |
| `serving.kv_cache_estimate` | KV cache estimate | future | TBD | Serving benchmark | Requires model and sequence assumptions. |

## Agents

| ID | KPI | Status | Value | Source | Notes |
|---|---|---|---|---|---|
| `agents.agent_success_rate` | Agent success rate | active | 1.0000 | Evaluation harness | Percentage of agent tasks completed successfully. |
| `agents.task_success_rate` | Task success rate | active | 1.0000 | Evaluation harness | Synonym for agent success rate. |
| `agents.tool_call_accuracy` | Tool call accuracy | active | 1.0000 | Evaluation harness | F1 score of actual vs expected tool calls. |
| `agents.tool_call_latency` | Tool call latency (overhead) | active | 9.55% | Serving benchmark | Mean percentage overhead of tool executions. |
| `agents.planning_loop_p95` | Planning loop p95 latency | active | 18920 ms | Serving benchmark | 95th percentile planning loop latency in ms. |
| `agents.argument_accuracy` | Argument accuracy | future | TBD | Evaluation harness | Requires argument validation. |
| `agents.final_state_success` | Final state success | future | TBD | Evaluation harness | Requires state verifier. |
| `agents.loop_rate` | Loop rate | future | TBD | Runtime traces | Requires trace capture. |
| `agents.unsafe_action_blocked_rate` | Unsafe action blocked rate | future | TBD | Policy checks | Requires policy layer. |
| `agents.cost_per_success` | Cost per success | future | TBD | Evaluation harness | Requires cost accounting. |
