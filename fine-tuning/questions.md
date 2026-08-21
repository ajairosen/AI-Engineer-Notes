# Fine-Tuning Interview Questions

Covers LoRA/PEFT and related fine-tuning technique questions.

## Q1: Justifying LoRA rank and alpha choices

Why did you choose rank = 16 and alpha = 32 for a LoRA fine-tune?

**Answer:**
- I chose rank 16 as a balance between adaptation capacity and efficiency. Rank controls the capacity of the low-rank update — a higher rank can learn more complex task-specific patterns but increases trainable parameters, memory, and computation. For my domain-specific sentiment classification task, rank 16 provided sufficient capacity without making fine-tuning unnecessarily expensive.
- I used alpha 32, meaning the LoRA update is scaled by α/r = 32/16 = 2. This controls the effective strength of the LoRA adaptation added to the base model. I wanted the fine-tuned domain knowledge to have sufficient influence while keeping the pretrained model largely intact.
- These values were selected as a practical starting configuration and validated based on task performance.
