# RAG (Retrieval-Augmented Generation) Interview Questions

## Q1: Fixed-size vs. semantic chunking

What's the difference between chunking a document by fixed character/token count vs. semantic chunking? When would you pick one over the other?

**Answer:**
- **Fixed-size chunking** splits text every N tokens/characters (often with overlap, e.g. 500 tokens with 50-token overlap). It's cheap, fast, predictable, and works fine when documents don't have strong internal structure.
- **Semantic chunking** splits at natural boundaries — sentences, paragraphs, or by embedding-similarity shifts between sentences — so each chunk stays topically coherent. Costs more (extra embedding calls), produces variable-sized chunks.
- **Rule of thumb:** fixed-size for homogeneous, low-structure text (logs, chat transcripts) or when latency/cost matters; semantic/structure-aware chunking for long-form docs (manuals, contracts, articles) where topic coherence drives answer quality.

## Q2: How do you actually decide on a chunking strategy in practice?

**Answer:**

1. **Start from your use case — e.g. social media posts**
   - Each post/comment is a natural semantic unit → 1 row = 1 chunk/document.
   - If a post is unusually long, use semantic splitting while preserving the original post ID and metadata.
2. **Normal use cases — choose based on document structure**
   - Structured documents → semantic/structure-based splitting (headings, sections, paragraphs).
   - Plain/unstructured text → recursive character/token-based splitting as a baseline.
3. **Evaluate & tune**
   - Treat chunk size and overlap as hyperparameters and test different configurations.
   - Evaluate using retrieval metrics (Precision@K, Recall@K/MRR) and end-to-end answer relevance/accuracy.
   - Select the configuration that gives the best quality vs. latency/token-cost trade-off.

## Q3: RAG accuracy + latency optimization

How would you optimize a RAG pipeline for both accuracy and latency at the same time?

**Answer:**

1. **Good chunking**
   - Use semantically meaningful chunks so retrieval starts with high-quality candidates.
   - Avoid overly large chunks that add irrelevant context.
2. **Hybrid retrieval**
   - Combine dense vector search + BM25/sparse search.
   - Dense search handles semantic similarity; BM25 handles exact terms, names, hashtags, IDs, etc.
   - Often improves recall without requiring an expensive LLM call.
3. **Metadata filtering**
   - Filter by metadata (state, date, platform, author, topic) before/alongside retrieval.
   - Reduces the search space and can improve both relevance and latency.
4. **Retrieve moderately, don't over-retrieve**
   - Don't blindly retrieve 50–100 chunks.
   - Retrieve a reasonable candidate set (e.g. `top_k=10`) and evaluate whether more actually improves answer quality.
5. **Conditional reranking**
   - Don't rerank every query — if initial retrieval is already strong, send results directly to the LLM.
   - If retrieval confidence is poor/ambiguous, run the reranker.
6. **Use a fast reranker/model**
   - If reranking is required, use a lightweight cross-encoder rather than an unnecessarily large model.
   - Keep the reranking candidate set small.
7. **Optimize the vector database**
   - Use ANN indexes (HNSW/IVF) and tune search parameters.
   - Don't sacrifice retrieval quality blindly — benchmark recall vs. latency.
8. **Keep LLM context small**
   - Give the LLM only the most relevant chunks rather than dumping all retrieved documents into the prompt.
   - Reduces both input processing latency and hallucination from irrelevant context.
9. **Cache repeated work**
   - Cache embeddings, retrieval results, and frequently repeated queries where appropriate.
   - Especially useful for common queries or repeated application requests.
10. **Use evaluation to tune the pipeline**
    - Create representative questions and test different `chunk_size`, `top_k`, overlap, reranking thresholds, etc.
    - Compare Recall@K, Precision@K, answer relevance/faithfulness, latency, and token cost.

## Q4: Reciprocal Rank Fusion (RRF)

What is Reciprocal Rank Fusion, and why is it used in hybrid search?

**Answer:**
- Hybrid search combines dense (semantic/vector) retrieval and sparse (keyword, e.g. BM25) retrieval — each returns its own ranked list of results, but their scores aren't on the same scale (cosine similarity vs. BM25 score), so you can't just add them directly.
- **RRF** solves this by ignoring raw scores and using **rank position** instead. For each document, its final score is:

  ```
  score = Σ 1 / (k + rank)
  ```

  where `rank` is its position in each individual ranked list, and `k` is a constant (commonly 60) that controls how much weight lower-ranked results get. Scores from both lists are summed per document, then re-sorted.
- **Why it's used:** simple, doesn't need score normalization or tuning of weights between dense/sparse, and works well even when the two retrieval methods have very different score distributions.

## Q5: Cross-encoder reranker vs. initial retrieval

What is a cross-encoder reranker, and how is it different from the initial retrieval step?

**Answer:**
- **Initial retrieval (bi-encoder):** query and documents are encoded **separately** into embeddings, then compared using cosine similarity (or dot product). Fast, because document embeddings are precomputed and indexed (e.g., HNSW in Qdrant) — only the query needs embedding at search time, then a nearest-neighbor lookup. Accuracy is limited since query and document never directly interact.
- **Cross-encoder reranker:** takes the query and **each candidate document together** as a single input, and the model jointly attends over both to produce a relevance score. Captures much finer-grained semantic interaction between query and document, so it's far more accurate.
- **Trade-off:** cross-encoders are much slower (can't precompute embeddings, must run inference per query-document pair), so they're **not used for initial retrieval** over millions of documents. Typical pipeline:
  1. Bi-encoder (+ BM25 for hybrid) retrieves top-k candidates (e.g., top 50) fast.
  2. Cross-encoder reranks just those top-k candidates to get a more accurate final top-n (e.g., top 5) to pass to the LLM.
- This two-stage approach balances speed (broad retrieval) with accuracy (precise reranking).

## Q6: Exact vs. semantic caching for LLM queries — and the staleness problem

**Answer:**
1. **Exact cache**
   - Stores response keyed to the exact input string. Cache hit only if the new query is character-for-character identical to a past query. Very limited — rarely triggers since users phrase things differently.
2. **Semantic cache**
   - Stores past query embeddings + their responses. New query is embedded and compared (cosine similarity) to cached queries. If similarity crosses a threshold, the cached response is returned without calling the LLM — even if wording differs but meaning is the same.
   - **Drawbacks:**
     - Caches based on query *meaning only*, ignoring conversation/session state — so it can return **stale answers** when underlying facts change (e.g., a user updates their name, but the cache still returns the old answer since "what's my name" looks the same).
     - Wrong similarity threshold causes bad hits — too loose returns wrong answers for similar-but-different questions; too strict gives few cache hits, reducing usefulness.
     - Not safe for personalized/stateful queries by default.
   - **Fix:**
     - **Context-aware cache key** — key = query embedding + conversation/session state hash, not query alone. A state change → different key → cache miss → fresh LLM call.
     - **Per-user/per-session scoping** — separate cache buckets per user so there's no cross-user leakage.
     - **Cache invalidation** — actively clear cached entries tied to a user when relevant facts/memory update, forcing a fresh call even if the key would've matched.

