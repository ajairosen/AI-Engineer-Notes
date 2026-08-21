# Fine-Tuning Interview Questions

Covers LoRA/PEFT and related fine-tuning technique questions.

## Q1: Justifying LoRA rank and alpha choices

Why did you choose rank = 16 and alpha = 32 for a LoRA fine-tune?

**Answer:**
- I chose rank 16 as a balance between adaptation capacity and efficiency. Rank controls the capacity of the low-rank update — a higher rank can learn more complex task-specific patterns but increases trainable parameters, memory, and computation. For my domain-specific sentiment classification task, rank 16 provided sufficient capacity without making fine-tuning unnecessarily expensive.
- I used alpha 32, meaning the LoRA update is scaled by α/r = 32/16 = 2. This controls the effective strength of the LoRA adaptation added to the base model. I wanted the fine-tuned domain knowledge to have sufficient influence while keeping the pretrained model largely intact.
- These values were selected as a practical starting configuration and validated based on task performance.

## Q2: Fine-tuning vs. RAG

What's the difference between fine-tuning and RAG, and when would you choose one over the other?

**Answer:**
- **Fine-tuning** updates the model's weights on custom data, so the model internalizes new knowledge, style, or behavior directly into its parameters.
- **RAG** keeps the model's weights unchanged and instead retrieves relevant external context at query time, injecting it into the prompt so the model can answer using up-to-date or domain-specific information.
- **When to choose fine-tuning:**
  - Need to change the model's behavior/style/format consistently (e.g., always respond in a specific tone or structure).
  - The knowledge is stable and won't change often.
  - Need faster inference without retrieval overhead.
- **When to choose RAG:**
  - Knowledge changes frequently (news, live data, evolving docs) — no need to retrain.
  - Need traceability/citations — RAG can point to source documents, fine-tuning can't.
  - Cheaper and faster to update — just update the knowledge base, not retrain the model.
  - Reduces hallucination risk by grounding answers in retrieved facts.
- **In practice:** they're often combined — fine-tune for behavior/domain style, RAG for factual grounding.
