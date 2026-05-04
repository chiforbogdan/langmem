from langmem import create_manage_memory_tool, create_search_memory_tool

from memory.store import store

FACTS_NAMESPACE = ("user", "facts")
EPISODES_NAMESPACE = ("episodes",)

manage_memory = create_manage_memory_tool(
    FACTS_NAMESPACE,
    store=store,
    instructions=(
        "Save facts as plain text strings. "
        "content must always be a simple sentence, never a dict or object. "
        "Good: 'User's name is John'. Bad: {'name': 'John'}."
    ),
)
search_memory = create_search_memory_tool(FACTS_NAMESPACE, store=store)
search_episodes = create_search_memory_tool(
    EPISODES_NAMESPACE,
    store=store,
    name="search_episodes",
    instructions="Search past interaction episodes to recall how similar situations were handled.",
)

memory_tools = [manage_memory, search_memory, search_episodes]
