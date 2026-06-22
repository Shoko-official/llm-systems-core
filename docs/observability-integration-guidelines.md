# Observability and Telemetry Integration Guidelines

This document defines the integration standards, schemas, and context propagation rules for tracing spans and system logs across all repositories in the LLM systems ecosystem.

## 1. Tracing Standard and Core Schema

All service tracing spans must validate against [span.json](file:///f:/Code/AI_ML/Article/Arxiv/llm-systems-core/schemas/span.json).

### Core Tracing Identifiers

*   **Trace ID**: A unique 128-bit hexadecimal identifier (32 hex characters) representing the end-to-end transaction context.
*   **Span ID**: A unique 64-bit hexadecimal identifier (16 hex characters) representing a single segment/operation within a transaction.
*   **Parent Span ID**: The parent span ID context, or `"N/A"` if this span is the root span.

### Expected Service Names

*   `core`: Core schemas and program-level validation tools.
*   `ledger`: Research ledger and evidence databases.
*   `taxonomy`: Layer taxonomy definitions and stubs.
*   `matrix`: Decision criteria and evaluations.
*   `eval`: Evaluation harness metrics calculations.
*   `infer`: Serving benchmarks and inference simulators.
*   `rag`: Chunk retrieval and reranker engines.
*   `security`: Policy safety filter blocks and compliance logs.

---

## 2. Operation Names and Standard Attributes

To ensure clean aggregations in telemetry, use the following standard operation names and metadata attributes:

### Inference Spans (`infer`)
*   **Operation Name**: `generate_tokens`, `request_queue_latency`
*   **Attributes**:
    *   `model_id` (string): The identifier of the active model.
    *   `prompt_tokens` (number): Number of tokens in user prompt.
    *   `completion_tokens` (number): Number of tokens generated.
    *   `concurrency` (number): Active request concurrency level.

### RAG Spans (`rag`)
*   **Operation Name**: `hybrid_search`, `rerank_chunks`
*   **Attributes**:
    *   `query` (string): The search query text.
    *   `results_count` (number): Number of retrieved chunks.
    *   `alpha` (number): Linear fusion interpolation weight.
    *   `method` (string): linear/rrf.

### Security/Policy Spans (`security`)
*   **Operation Name**: `is_prompt_safe`, `check_tool_call`
*   **Attributes**:
    *   `block_action` (boolean): True if blocked by policy.
    *   `violation_category` (string): The type of violation (e.g. `instruction_override`, `unsafe_command`).

---

## 3. Running Telemetry Validations

Before merging any changes that generate trace logs, verify that the generated logs comply with the validation script:

```bash
# Validates all trace logs under examples/spans/
python scripts/validate_spans.py
```
