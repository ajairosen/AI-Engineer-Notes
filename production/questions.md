# Production / Reliability Interview Questions

Covers failure handling, hallucination mitigation, monitoring, evals, and operating LLM systems in production.

## Q1: Handling agent failure in a multi-agent system

In a multi-agent system, one of the agents fails mid-task (e.g., times out or throws an exception). How would you design the system to handle that gracefully?

**Answer:**

A few strategies, usually combined:

1. **Isolate the blast radius** — wrap each agent/tool call in its own timeout and exception handling, so one agent's failure doesn't bring down the whole workflow.
2. **Retry with backoff** — transient failures (timeout, rate limit, flaky tool call) get retried a few times with exponential backoff before giving up.
3. **Fallback agent/model** — if the primary agent or model fails, route to a simpler fallback (smaller model, cached response, or rule-based logic) so the system degrades gracefully instead of breaking, or returns a partial result rather than failing silently.
4. **Supervisor-level error handling** — in a supervisor pattern, the supervisor catches the failure and decides whether to retry, reroute to a different sub-agent, or skip that step and continue with partial results.
5. **Checkpointing/state persistence** — save state at each node (LangGraph supports this natively) so on failure you can resume from the last good checkpoint instead of restarting the whole workflow.
6. **Structured error propagation** — the failing agent returns a typed error object (not a crash) so downstream nodes/supervisor can make a decision instead of the whole graph breaking.
7. **Observability** — log which agent failed, why, and what state it was in — needed to debug and to decide whether to retry, fallback, or alert a human.

## Q2: Production challenges building RAG/agentic LLM systems

Walk through some real production challenges you've faced building RAG/agentic LLM systems, and how you addressed them.

**Answer:**

1. **LLM latency and timeouts**
   - *Challenge:* LLM/API calls were sometimes slow or timed out, especially during high traffic.
   - *Solution:* Added timeouts, retries with exponential backoff, async I/O, caching, and used smaller models for simpler tasks.
2. **RAG hallucinations / irrelevant retrieval**
   - *Challenge:* The LLM sometimes generated incorrect answers because retrieved documents were irrelevant or insufficient.
   - *Solution:* Improved chunking and metadata filtering, tuned `top_k`, used hybrid retrieval/reranking, and added retrieval-quality checks before generation.
3. **Vector DB performance**
   - *Challenge:* Retrieval latency increased as the document collection grew.
   - *Solution:* Optimized vector indexing (HNSW/IVF), metadata filtering, `top_k`, and embedding/search configuration.
4. **Agent failures**
   - *Challenge:* One failing agent/tool could cause the entire workflow to fail.
   - *Solution:* Added structured error handling, retries, timeouts, fallback agents, circuit breakers, and checkpointing for recoverable workflows.
5. **LLM output inconsistency**
   - *Challenge:* The model sometimes returned unexpected formats, making downstream processing unreliable.
   - *Solution:* Used structured output/Pydantic schemas, validation, retry-on-invalid-output, and fallback handling.
6. **Prompt/context becoming too large**
   - *Challenge:* Passing too much conversation history or retrieved context increased latency and token cost.
   - *Solution:* Limited context, retrieved only relevant chunks, summarized older history, and passed only required state between agents.
7. **Data quality / stale data**
   - *Challenge:* The model could produce outdated answers because the underlying documents/data were stale.
   - *Solution:* Added ingestion monitoring, timestamps/metadata, scheduled refreshes, and validation checks before retrieval.
8. **Observability**
   - *Challenge:* When an answer was wrong or slow, it was difficult to identify whether the issue came from the router, agent, retrieval, database, or LLM.
   - *Solution:* Added tracing and logging for each node, prompt/response metadata, retrieval scores, latency, token usage, errors, and retry counts.

