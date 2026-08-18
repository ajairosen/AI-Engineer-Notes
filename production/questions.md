# Production / Reliability Interview Questions

Covers failure handling, hallucination mitigation, monitoring, evals, and operating LLM systems in production.

## Q1: Handling agent failure in a multi-agent system

In a multi-agent system, one of the agents fails mid-task (e.g., times out or throws an exception). How would you design the system to handle that gracefully?

**Answer:**
I would isolate each agent using timeouts and exception handling, so one agent's failure doesn't bring down the whole workflow. For temporary failures, I would retry a few times with exponential backoff. If it still fails, I would fall back to a simpler/backup agent or return a partial result rather than failing silently. In LangGraph, I would checkpoint the state so we can resume from the failed node instead of starting the whole workflow again. I would also log failures for monitoring/observability, and use a circuit breaker so a consistently failing dependency isn't hammered with repeated calls.

