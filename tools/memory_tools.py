from langmem import create_manage_memory_tool, create_search_memory_tool

from memory.store import store

NAMESPACE = ("user", "facts")

manage_memory = create_manage_memory_tool(NAMESPACE, store=store)
search_memory = create_search_memory_tool(NAMESPACE, store=store)

memory_tools = [manage_memory, search_memory]
