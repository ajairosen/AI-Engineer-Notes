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

