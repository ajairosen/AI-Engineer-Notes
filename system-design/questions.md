# System Design Interview Questions (Basics)

## Q1: Reducing latency in a RAG-based chat system

How would you reduce latency in a RAG-based chat system where users complain responses take too long?

**Answer:**
- **Profile first** — figure out where the time actually goes: embedding the query, vector search, reranking, prompt construction, or the LLM generation itself. Generation is usually the biggest chunk, but don't assume — measure.
- **Reduce retrieval latency:** use an approximate nearest-neighbor index (HNSW, IVF) instead of exact search; keep the vector DB warm/co-located with the app; cap `top_k` to only what you actually need.
- **Reduce LLM latency:** stream the response so the user sees tokens immediately instead of waiting for the full answer; use a smaller/faster model for simpler queries and route only hard queries to a bigger model; cache responses for repeated/common queries.
- **Parallelize independent steps:** e.g., run reranking and prompt-template prep concurrently if they don't depend on each other; kick off multiple retrieval sources (vector + keyword) in parallel rather than sequentially.
- **Reduce prompt size:** trim context to the most relevant chunks only (reranking helps here) — smaller prompts mean faster time-to-first-token and lower cost.
- **Async/non-blocking architecture:** make sure the API layer isn't blocking on synchronous calls; use connection pooling for DB/vector store calls.

The main thing interviewers want: you don't just say "make it faster" — you show you'd measure where the bottleneck is before optimizing, and you know the standard levers (streaming, caching, smaller models for easy cases, ANN indexes).

