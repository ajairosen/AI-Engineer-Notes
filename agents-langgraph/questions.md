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

## Q2: LangChain vs. LangGraph

What's the difference between LangChain and LangGraph, and when would you reach for one over the other?

**Answer:**
- **LangChain** is a toolkit for building LLM apps — prompts, chains, retrievers, memory, integrations. Best suited for linear/sequential flows: prompt → LLM → parse → output.
- **LangGraph** is built on top of LangChain for stateful, cyclic workflows. It models the app as a graph of nodes (agents/functions) connected by edges, with explicit shared state passed between them. This enables loops, conditional branching, retries, and human-in-the-loop steps — things linear chains can't handle well.
- **Quick way to remember:** LangChain = building blocks. LangGraph = orchestrator that lets those blocks loop, branch, and make decisions like a real agent.

## Q3: LangGraph / agentic application — latency optimization

How would you reduce latency in a LangGraph-based agentic application? (See also [system-design/questions.md](../system-design/questions.md) Q1 for the narrower RAG-chat-specific version of this question.)

**Answer:**

1. **Async & parallel execution** — use async for I/O-bound tasks (LLM, DB, vector DB, API calls) so they don't block execution, and run independent agents/components concurrently instead of sequentially to reduce critical-path latency.
2. **Caching** — cache expensive/repeated operations: embeddings, retrieval results, LLM responses, API calls.
3. **Checkpointing** — persist workflow state so a failed long-running workflow can resume from the last checkpoint instead of restarting.
4. **Reduce LLM calls** — avoid unnecessary supervisor/planner calls; use deterministic logic or smaller models for simple decisions.
5. **Optimize RAG** — tune `top_k`, metadata filtering, chunk size, and reranking; keep retrieved context small and relevant.
6. **Vector DB indexing** — use approximate nearest-neighbor indexes (HNSW, IVF) for efficient search on large datasets.
7. **Timeouts & retries** — set timeouts for external calls, retry transient failures with exponential backoff instead of waiting indefinitely.
8. **Streaming** — stream LLM tokens to improve time-to-first-token (TTFT) and perceived latency.
9. **Optimize state & prompts** — keep graph state and LLM prompts small, passing only the data required by downstream nodes.
10. **Monitoring** — measure latency per node, LLM call, and DB/API call to identify the critical path before optimizing.

## Q4: What determines routing complexity in a multi-agent system?

**Answer:**

Routing complexity mainly depends on the number of possible paths, ambiguity of the user intent, dependencies between tasks, and how dynamically the system needs to decide the next action.

## Q5: ReAct vs. Plan-and-Execute

What's the difference between the ReAct agent pattern and the Plan-and-Execute pattern?

**Answer:**
- **ReAct (Reason + Act):** the agent interleaves reasoning and action in a loop — think, take one action, observe result, think again, take next action. Reactive — decides the next step only after seeing the previous result. Good for dynamic tasks where each step depends on prior output, but can be slower (many LLM calls) and less predictable.
- **Plan-and-Execute:** the agent first generates a full multi-step plan upfront, then executes each step (optionally re-planning if a step fails or new info emerges). Fewer LLM calls for planning, more predictable structure, easier to parallelize steps, but less adaptive to unexpected mid-task changes compared to ReAct.
- **Quick way to remember:** ReAct = think-as-you-go. Plan-and-Execute = plan first, then act.

