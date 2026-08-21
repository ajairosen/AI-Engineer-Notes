# LLM Fundamentals Interview Questions

Covers core transformer/LLM architecture concepts, distinct from RAG (retrieval), agents (orchestration), and fine-tuning (PEFT techniques).

## Q1: Encoder-only vs. decoder-only vs. encoder-decoder architectures

**Answer:**

| Architecture        | Main job              | Attention                    | Examples   |
| -------------------- | ---------------------- | ----------------------------- | ---------- |
| **Encoder-only**     | Understand              | Bidirectional self-attention  | BERT       |
| **Decoder-only**     | Generate                | Causal self-attention         | GPT, Llama |
| **Encoder-Decoder**  | Understand → Generate   | Self + cross attention        | T5, BART   |
