# Technical Details

## Stack

| Layer       | Library / tool                        |
|---|---|
| LLM         | `langchain-groq` → `ChatGroq(model="llama-3.3-70b-versatile")` |
| Agent       | `langgraph` → `create_react_agent`    |
| Memory      | `langmem`                             |
| Store       | `langgraph.store.memory.InMemoryStore` |
| CLI output  | `rich`                                |
| Config      | `python-dotenv` → `.env` file         |
| Packaging   | `uv` — dependency management and runner |

---

## Project layout

```
langmem-chatbot/
├── main.py                  # CLI entry point
├── agent.py                 # LangGraph agent definition
├── memory/
│   ├── store.py             # Shared store singleton
│   └── procedural.py        # System prompt load / save / optimize
├── tools/
│   └── memory_tools.py      # Hot-path memory tools
└── background/
    └── processor.py         # Post-session MemoryManager
```

---

## Memory types in detail

### Semantic memory — `("user", "facts")` namespace

Stored via langmem hot-path tools during the conversation.

```python
from langmem import create_manage_memory_tool, create_search_memory_tool

manage_memory = create_manage_memory_tool(store, namespace=("user", "facts"))
search_memory = create_search_memory_tool(store, namespace=("user", "facts"))
```

The agent decides when to call these. When it calls `manage_memory` it passes
a string fact; `search_memory` takes a query and returns ranked results.

---

### Episodic memory — `("episodes",)` namespace

Extracted **after** the session by `MemoryManager`. It reads the full message
list and writes structured snapshots: situation, thought process, outcome.

```python
from langmem import create_memory_manager

manager = create_memory_manager(
    llm,
    schemas=[EpisodicNote],   # Pydantic model with situation/thought/outcome
    namespace=("episodes",),
    store=store,
)
await manager.ainvoke({"messages": session_messages})
```

`EpisodicNote` is a small Pydantic model defined in `background/processor.py`.

---

### Procedural memory — `system_prompt.txt`

The agent's system prompt lives in `system_prompt.txt` at project root.
After each session the `PromptOptimizer` rewrites it.

```python
from langmem import create_prompt_optimizer

optimizer = create_prompt_optimizer(llm, kind="metaprompt")
result = await optimizer.ainvoke({
    "trajectories": [(session_messages, {})],
    "prompt": current_prompt,
})
```

Three optimizer kinds are available (`metaprompt`, `gradient`, `prompt_memory`).
This project uses `metaprompt` — it reflects on what worked and rewrites the
prompt in one pass.

---

## Hot path vs background

```
User message ──► Agent ──► LLM call
                  │
                  ├─► manage_memory (HOT PATH — happens NOW, adds latency)
                  └─► search_memory (HOT PATH — happens NOW, adds latency)

Session ends ──► MemoryManager (BACKGROUND — async, user doesn't wait)
             └── PromptOptimizer (BACKGROUND — async, user doesn't wait)
```

Hot path = higher latency, real-time transparency ("I just saved that").
Background = no latency impact, runs once at end of session.

---

## Data flow across sessions

```
Session N ends
  │
  ├─ background/processor.py
  │    └─ writes episodes to store ("episodes",) namespace
  │
  └─ memory/procedural.py
       └─ writes new system_prompt.txt

Session N+1 starts
  │
  ├─ loads system_prompt.txt  → agent system prompt (procedural)
  └─ agent calls search_memory on first message → recalls user facts (semantic)
```

---

## Key langmem API surface

| Function / class                  | What it does                                      |
|---|---|
| `create_manage_memory_tool`       | Returns a LangChain tool that writes to the store |
| `create_search_memory_tool`       | Returns a LangChain tool that reads from the store |
| `create_memory_manager`           | Returns an async runnable that extracts memories from messages |
| `create_prompt_optimizer`         | Returns an async runnable that rewrites a system prompt |

All are in the top-level `langmem` package.

---

## Environment

```
GROQ_API_KEY=   # required
```

Copy `.env.example` to `.env` and fill in the key.

---

## Running with uv

```bash
# Install dependencies
uv sync

# Run the chatbot
uv run python main.py
```
