# Implementation Tasks

Each task is a separate git branch off `main`.

---

## 1 — `feature/scaffold`

**Files:** `requirements.txt`, `.env.example`, `memory/__init__.py`,
`tools/__init__.py`, `background/__init__.py`

- Define all dependencies
- Provide `.env.example` with `ANTHROPIC_API_KEY=`
- Create package directories

---

## 2 — `feature/memory-store`

**File:** `memory/store.py`

- Instantiate a single `InMemoryStore` exported as `store`
- Add a comment showing how to swap it for a persistent backend

---

## 3 — `feature/hot-path-tools`

**File:** `tools/memory_tools.py`

- Wrap `create_manage_memory_tool` and `create_search_memory_tool`
- Use namespace `("user", "facts")`
- Export `memory_tools` list ready to pass to the agent

---

## 4 — `feature/agent`

**File:** `agent.py`

- Build a `create_react_agent` with `ChatAnthropic`
- Load system prompt via `memory.procedural.load_system_prompt()`
- Pass `memory_tools` as tools
- Export a `run_agent(messages)` async function

---

## 5 — `feature/background-processor`

**File:** `background/processor.py`

- Define `EpisodicNote` Pydantic model (`situation`, `thought`, `outcome`)
- Implement `async extract_episodes(messages)` using `create_memory_manager`
- Write extracted episodes to `("episodes",)` namespace
- Print extracted memories to stdout so they are visible when the session ends

---

## 6 — `feature/procedural-memory`

**File:** `memory/procedural.py`

- `load_system_prompt()` → reads `system_prompt.txt`, falls back to default
- `save_system_prompt(prompt)` → writes `system_prompt.txt`
- `async optimize_prompt(messages, current_prompt)` → runs `PromptOptimizer`
  with `kind="metaprompt"`, saves and returns the updated prompt

---

## 7 — `feature/cli`

**File:** `main.py`

- Load `.env`
- Print startup banner showing loaded memories and current system prompt
- Input loop: read user message → call agent → print response
- `/memory` command: print all items in `("user", "facts")` and `("episodes",)` namespaces
- `exit` / `quit`: run `extract_episodes` + `optimize_prompt`, print summary, exit
