from langmem import create_manage_memory_tool, create_search_memory_tool

from memory.store import store

NAMESPACE = ("user", "facts")

manage_memory = create_manage_memory_tool(store, namespace=NAMESPACE)
search_memory = create_search_memory_tool(store, namespace=NAMESPACE)

memory_tools = [manage_memory, search_memory]
