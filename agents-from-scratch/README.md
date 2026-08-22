# Agents From Scratch

Hands-on companion to the Q&A bank — instead of notes, this module builds runnable
LangChain / LangGraph code, one script at a time, from a plain LLM call up to a
supervisor multi-agent setup. Purpose is interview-prep understanding, not
production code — keep each script minimal and readable over "correct" abstractions.

## Stack
- `langchain` / `langchain-openai` — LLM calls, chains
- `langgraph` — stateful graphs, agent loops, multi-agent orchestration
- `langchain-tavily` — web search tool
- `langsmith` — tracing/eval (enabled via env vars, no code changes needed)
- `python-dotenv` — local secrets

Dependencies are managed with **uv** at the repo root (`pyproject.toml` / `uv.lock`),
not per-module — this folder doesn't have its own `requirements.txt`. Code lives under
`agents-from-scratch/src/`.

## Roadmap (module_item numbering, flexible — items get added/reordered as we go)
| File | Topic | Status |
|---|---|---|
| `src/1_1_basic_llm_call.py` | Plain LLM call via LangChain | done |
| `src/2_1_basic_rag.py` | Minimal RAG pipeline (load → split → embed → retrieve → answer) | pending |
| `src/2_2_rag_with_tool_call.py` | RAG exposed as a tool the LLM decides to call | pending |
| `src/3_1_react_agent.py` | Single ReAct-style agent with tools (Tavily search) | pending |
| `src/4_1_supervisor_agent.py` | Supervisor agent routing to worker agents | pending |
| `src/5_x_scenarios.py` | Grab-bag: memory, human-in-the-loop, structured output, etc. | TBD |

## Conventions
- Every file opens with a `"""Q: ..."""` docstring stating the interview question it answers.

## Workflow
- One file/topic at a time. I pose the task/question for that file; you attempt an
  answer (code or approach) first.
- You answer → I review/correct it and write the final version into the file.
- You say you can't / want me to → I write the implementation myself.
- Say **"next"** to move to the next planned item once a file is done.
- Say **"skip"** to leave an item for later and move on.
- Files stay editable — nothing here is final; we revise as understanding improves.

## Setup
```
uv sync
```
`.env` holds API keys (`OPENAI_API_KEY`, `TAVILY_API_KEY`, `LANGSMITH_*`) — already gitignored at repo root.
