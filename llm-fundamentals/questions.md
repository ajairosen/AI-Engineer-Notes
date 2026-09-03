# LLM Fundamentals Interview Questions

Covers core transformer/LLM architecture concepts, distinct from RAG (retrieval), agents (orchestration), and fine-tuning (PEFT techniques).

## Q1: Encoder-only vs. decoder-only vs. encoder-decoder architectures

**Answer:**

| Architecture        | Main job              | Attention                    | Examples   |
| -------------------- | ---------------------- | ----------------------------- | ---------- |
| **Encoder-only**     | Understand              | Bidirectional self-attention  | BERT       |
| **Decoder-only**     | Generate                | Causal self-attention         | GPT, Llama |
| **Encoder-Decoder**  | Understand → Generate   | Self + cross attention        | T5, BART   |

## Q2: Explain the attention mechanism in a transformer

Explain self-attention. What are queries, keys, and values, and why does self-attention handle long-range dependencies better than an RNN?

**Answer:**

**One-liner:** Attention lets every token look at every other token and decide which ones matter for understanding it.

**Query / Key / Value** — each token is projected (via learned matrices) into three vectors, because the role a word plays when *searching* differs from the role it plays when *being found*, which differs from the *information it hands over*:

- **Query** – what I'm looking for
- **Key** – what I offer
- **Value** – the information I carry

**How it works:** a token compares its query against every other token's key to get relevance scores, softmaxes them into weights that sum to 1, and takes a weighted sum of the values. That weighted sum is the token's new, context-aware representation.

**The formula (scaled dot-product attention):**

```
Attention(Q, K, V) = softmax( (Q Kᵀ) / √d_k ) · V
```

**Multi-head attention:** do this several times in parallel so different heads capture different relationships (grammar, meaning, position), then concatenate.

**Causal mask (decoder LLMs):** positions after the current token are set to −∞ before softmax, so a token only attends to itself and earlier tokens — this is what makes left-to-right generation valid.

**Why it beats RNNs for long-range dependencies:**
- **O(1) path length** — any two tokens interact directly in one step. In an RNN, token 1's signal must survive hundreds of sequential steps to reach token 500, so it decays and gradients vanish/explode.
- **Parallelism** — all positions compute simultaneously during training (no sequential unrolling), so it trains far faster.
- **Content-based routing** — attention weights are data-dependent; the model dynamically decides what to look at instead of compressing everything into one fixed-size hidden state.

**Trade-off:** attention is **O(n²)** in sequence length (every token attends to every token) in compute and memory — the main bottleneck for long context, and the reason for KV caching and efficient-attention variants (FlashAttention, sliding-window, GQA/MQA).

## Q3: What is the KV cache in LLM inference?

Why does it exist, what problem does it solve, and what does it cost you?

**Answer:**

**The problem it solves:** LLMs generate one token at a time. To produce the next token, attention needs the keys and values of *every* previous token. Without caching, each new token recomputes K and V for the entire sequence from scratch — generating token 500 redoes the work for tokens 1–499 (O(n²) wasted compute over a response).

**What the cache does:** a token's key and value vectors never change once computed, so store them. For the next token you compute Q, K, V only for the *one new token*, append its K and V to the cache, and attend against the whole cached set. Each step goes from "reprocess the whole sequence" to "process one token + look up the cache." This is the main reason autoregressive generation is fast enough to be practical.

**Two phases of inference:**
- **Prefill** — process the whole prompt in parallel, fill the cache. Compute-bound.
- **Decode** — generate tokens one by one, reading/appending to the cache. Memory-bandwidth-bound.

**What it costs — GPU memory.** The cache grows linearly with sequence length and batch size:

```
cache size ≈ 2 (K and V) × layers × heads × head_dim × seq_len × batch × bytes_per_param
```

For long contexts or big batches this can exceed the model weights themselves, and it's the main limit on how many concurrent requests you can serve.

**How to shrink it:**
- **GQA / MQA** — multiple query heads share one set of K/V heads (Llama 3, Mistral).
- **Quantize the cache** — store K/V in int8/fp8.
- **Sliding-window / local attention** — only keep the last N tokens.
- **PagedAttention (vLLM)** — allocate cache in pages to remove fragmentation and enable sharing across requests.

## Q4: What does the `temperature` parameter control?

What happens mathematically, and when would you set it to 0 vs. higher? (Also: top-p / top-k.)

**Answer:**

**What it controls:** how deterministic vs. random generation is. Low temperature → deterministic; high temperature → random/creative.

**The mechanism:** divide the **logits** (raw scores) by temperature **T** *before* softmax:

```
softmax(logits / T)
```

- **T = 1** → distribution unchanged.
- **T < 1** (e.g. 0.2) → logits scale up → gaps widen → softmax sharpens → top token dominates → near-deterministic.
- **T > 1** (e.g. 1.5) → logits shrink toward each other → distribution flattens → unlikely tokens sampled more often → creative, but more errors.
- **T = 0** → special-cased to pure **argmax** (greedy) — always the single highest-probability token. (Dividing by 0 is undefined, so implementations just take the max.)

**top-k / top-p (different knobs — they truncate the candidate pool; temperature reshapes the distribution):**
- **top-k** — only sample from the k highest-probability tokens.
- **top-p (nucleus)** — only sample from the smallest set of tokens whose probabilities sum to ≥ p.
- Usually combined with temperature.

**When to use what:**
- **T = 0 / low** — classification, extraction, structured/JSON output, code, math, RAG factual answers, evals, anything needing reproducibility.
- **T ≈ 0.7–1.0** — chat, general assistant responses.
- **T > 1.0** — brainstorming, creative writing, generating diverse candidates for reranking.
