# RAG (Retrieval-Augmented Generation) Interview Questions

## Q1: Fixed-size vs. semantic chunking

What's the difference between chunking a document by fixed character/token count vs. semantic chunking? When would you pick one over the other?

**Answer:**
- **Fixed-size chunking** splits text every N tokens/characters (often with overlap, e.g. 500 tokens with 50-token overlap). It's cheap, fast, predictable, and works fine when documents don't have strong internal structure.
- **Semantic chunking** splits at natural boundaries — sentences, paragraphs, or by embedding-similarity shifts between sentences — so each chunk stays topically coherent. Costs more (extra embedding calls), produces variable-sized chunks.
- **Rule of thumb:** fixed-size for homogeneous, low-structure text (logs, chat transcripts) or when latency/cost matters; semantic/structure-aware chunking for long-form docs (manuals, contracts, articles) where topic coherence drives answer quality.

