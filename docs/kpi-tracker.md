# KPI Tracker

This tracker records the program-level KPIs that must be maintained as repositories are added. Values start as `TBD` until the corresponding measurement exists.

## Engineering

| KPI | Current value | Source | Notes |
| --- | --- | --- | --- |
| Open MR/PR count | TBD | GitHub project | Count active review work across initial repositories. |
| Median MR/PR size | TBD | GitHub pull requests | Track changed lines excluding generated files when possible. |
| Green CI rate | TBD | GitHub Actions | Track after CI exists in each repository. |
| Average issue to MR/PR time | TBD | GitHub issues and pull requests | Track once the workflow is stable. |
| Blocked issue count | TBD | GitHub project | Count issues explicitly marked blocked. |
| Test coverage | TBD | Repository-specific tooling | Record only when meaningful coverage tooling exists. |

## Research

| KPI | Current value | Source | Notes |
| --- | --- | --- | --- |
| Structured source count | TBD | Research ledger | Introduced after ledger schema work. |
| Structured claim count | TBD | Research ledger | Introduced after ledger schema work. |
| Claims with primary source | TBD | Research ledger | Percentage of claims backed by primary sources. |
| Claims marked `TODO:evidence_needed` | TBD | Research ledger | Must decrease as evidence is added. |
| Missing citations | TBD | Research ledger and paper | Track before paper drafting expands. |

## Paper

| KPI | Current value | Source | Notes |
| --- | --- | --- | --- |
| Sections created | TBD | Paper repository | Count section files or paper outline entries. |
| Sections drafted | TBD | Paper repository | Count sections with draft content. |
| Sections reviewed | TBD | Paper repository | Count reviewed sections. |
| Figures generated | TBD | Paper repository | Count reproducible figures only. |
| Tables generated | TBD | Paper repository | Count paper-ready tables. |
| LaTeX compilation | TBD | Paper CI | Track pass/fail after build setup. |
| Missing citations | TBD | Paper validation | Track unresolved citation markers. |
| Remaining TODOs | TBD | Paper validation | Track paper TODO markers. |

## RAG

| KPI | Current value | Source | Notes |
| --- | --- | --- | --- |
| recall@5 | TBD | Evaluation harness | Not available before retrieval evaluation exists. |
| recall@10 | TBD | Evaluation harness | Not available before retrieval evaluation exists. |
| precision@k | TBD | Evaluation harness | Not available before retrieval evaluation exists. |
| MRR | TBD | Evaluation harness | Not available before retrieval evaluation exists. |
| Citation accuracy | TBD | Evaluation harness | Requires citation evaluation data. |
| Groundedness | TBD | Evaluation harness | Requires groundedness checks. |
| p95 latency | TBD | RAG benchmark | Requires benchmark harness. |
| Permission failure rate | TBD | RAG benchmark | Requires permission model tests. |

## Serving

| KPI | Current value | Source | Notes |
| --- | --- | --- | --- |
| TTFT | TBD | Serving benchmark | Introduced in serving benchmark repository. |
| TPOT | TBD | Serving benchmark | Introduced in serving benchmark repository. |
| Throughput | TBD | Serving benchmark | Requests or tokens per second. |
| p95/p99 latency | TBD | Serving benchmark | Requires benchmark dataset. |
| VRAM | TBD | Serving benchmark | GPU memory measurement. |
| Cost per request | TBD | Serving benchmark | Requires pricing assumptions. |
| KV cache estimate | TBD | Serving benchmark | Requires model and sequence assumptions. |

## Agents

| KPI | Current value | Source | Notes |
| --- | --- | --- | --- |
| Task success rate | TBD | Evaluation harness | Requires task dataset. |
| Tool call accuracy | TBD | Evaluation harness | Requires tool-call traces. |
| Argument accuracy | TBD | Evaluation harness | Requires argument validation. |
| Final state success | TBD | Evaluation harness | Requires state verifier. |
| Loop rate | TBD | Runtime traces | Requires trace capture. |
| Unsafe action blocked rate | TBD | Policy checks | Requires policy layer. |
| Cost per success | TBD | Evaluation harness | Requires cost accounting. |
