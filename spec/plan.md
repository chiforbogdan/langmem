# LangMem Chatbot — Project Spec

## What

A command-line chatbot backed by a LangGraph agent that demonstrates all three
types of long-term memory from the `langmem` library, plus both update
strategies (hot path and background).

This is a **learning project** — every memory operation is made visible so you
can observe what the agent remembers, why, and when.

---

## Why

`langmem` exposes three primitives that map to how humans store memory:

| Memory type  | Analogy                  | What the agent stores                                |
|---|---|---|
| Semantic     | Facts you know           | User preferences, profile facts ("prefers concise answers") |
| Episodic     | Events you remember      | Snapshots of past interactions ("helped user debug a KeyError") |
| Procedural   | Skills you have          | The agent's own system prompt, updated after each session |

The goal is to touch all three in one runnable project.

---

## What it does

- You type messages in the terminal; an agent responds.
- **During the conversation** (hot path): the agent can call `manage_memory`
  and `search_memory` tools to save and recall semantic facts in real time.
- **After you exit** (background): a `MemoryManager` processes the full
  transcript and extracts episodic snapshots asynchronously.
- **Also after exit**: a `PromptOptimizer` rewrites the agent's system prompt
  based on the session — this is procedural memory.
- On the **next run**: the agent greets you by name (semantic), the system
  prompt reflects what was learned (procedural), and past episodes are
  searchable (episodic).

---

## Commands

| Input       | Effect                                      |
|---|---|
| any text    | Chat with the agent                         |
| `/memory`   | Print all stored memories (debug view)      |
| `exit`      | Trigger background processing, then quit    |

---

## Scope

- Single user, local machine, no server.
- LLM: Anthropic Claude (`claude-sonnet-4-6`).
- Store: `InMemoryStore` (clearly marked as swappable for a persistent backend).
- No streaming, no auth, no UI beyond the terminal.
