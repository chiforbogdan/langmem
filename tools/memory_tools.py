from langmem import create_manage_memory_tool, create_search_memory_tool

from memory.store import store

NAMESPACE = ("user", "facts")

manage_memory = create_manage_memory_tool(
    NAMESPACE,
    store=store,
    instructions=(
        "Save facts as plain text strings. "
        "content must always be a simple sentence, never a dict or object. "
        "Good: 'User's name is John'. Bad: {'name': 'John'}."
    ),
)
search_memory = create_search_memory_tool(NAMESPACE, store=store)

memory_tools = [manage_memory, search_memory]
