from langgraph.store.memory import InMemoryStore

# Swap InMemoryStore for a persistent backend to survive process restarts:
# from langgraph.store.postgres import AsyncPostgresStore
# store = AsyncPostgresStore.from_conn_string("postgresql://...")
store = InMemoryStore()
