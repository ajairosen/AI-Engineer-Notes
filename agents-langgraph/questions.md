# Agents & LangGraph Interview Questions

## Q1: State vs. checkpoint in LangGraph

In LangGraph, what's the difference between a graph's "state" and a "checkpoint," and why does checkpointing matter for agent workflows?

**Answer:**
- **State** is the shared data structure (typically a `TypedDict` or Pydantic model) that flows through the graph — each node reads from it and returns updates that get merged in via reducers. It represents "what the agent currently knows/has done" at any point in execution.
- **Checkpoint** is a persisted snapshot of that state (plus metadata like which node ran, thread ID) saved at each step via a checkpointer (e.g., `MemorySaver`, `SqliteSaver`, `PostgresSaver`). It's what makes state durable across steps, not just an in-memory object.
- **Why it matters:**
  - **Resumability:** if a node fails or the process crashes, you can resume from the last checkpoint instead of restarting the whole workflow.
  - **Human-in-the-loop:** you can pause the graph at a checkpoint, let a human inspect/edit state, then resume.
  - **Time travel / debugging:** you can replay from any past checkpoint to see how state evolved, or branch from an earlier point.
  - **Multi-turn conversations:** checkpoints tied to a `thread_id` let you maintain separate persistent conversation histories per user/session.

