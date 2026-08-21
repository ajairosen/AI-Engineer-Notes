# System Design Interview Questions (Basics)

## Q1: Reducing latency in a RAG-based chat system

How would you reduce latency in a RAG-based chat system where users complain responses take too long?

**Answer:**

*First find the bottleneck*
- Measure time for each step: embedding → vector search → reranking → prompt creation → LLM.

*Optimize vector search*
- Use ANN indexes like HNSW/IVF for faster search.
- Keep `top_k` small — retrieve only the chunks actually needed.
- Keep the vector DB close to the application to reduce network delay (warn DB + co-located)

*Optimize LLM*
- Use a smaller/faster model for simple queries.
- Reduce the amount of context sent to the LLM.
- Stream the response so users see output immediately.
- Cache responses for repeated queries.

*Run independent tasks in parallel*
- Run Vector Search + BM25 simultaneously.
- Don't run independent operations one after another unnecessarily.

*Use async*
- Don't block the API while waiting for the LLM or database.
- Async allows the server to handle other requests while waiting.

*Use connection pooling*
- Reuse database/vector DB connections instead of creating a new connection for every request.

## Q2: Handling a traffic spike into a RAG/agentic system

How would you design the request path to survive a sudden traffic spike into a RAG/agent-backed API?

**Answer:**

```
                      TRAFFIC SPIKE
                            ↓
        Users ───────→ [Load Balancer]
                            ↓
                     [Rate Limiter]
                    /              \
               Allowed            Too many
                  ↓                 ↓
            [API Servers]        HTTP 429
                  ↓
               [Cache]
              /       \
           HIT         MISS
            ↓           ↓
        Response   [Queue / Concurrency Limit]
                          ↓
                    [RAG / Agent]
                          ↓
                [LLM / Vector DB / Tools]
```

*Simple understanding*
- **Rate limiter** — stops one user/client from sending too many requests.
- **Load balancer** — distributes a traffic spike across multiple API servers.
- **Cache** — avoids repeating expensive work for similar/repeated queries.
- **Queue + concurrency limit** — prevents 1,000 requests from simultaneously calling the LLM.
- **Workers/agent** — process only a controlled number of requests at a time.

