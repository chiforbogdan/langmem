from pydantic import BaseModel

from langchain_groq import ChatGroq
from langmem import create_memory_store_manager
from rich.console import Console

from memory.store import store

console = Console()


class EpisodicNote(BaseModel):
    """A notable episode from the conversation worth remembering."""

    situation: str
    thought: str
    outcome: str


async def extract_episodes(messages: list) -> None:
    if not messages:
        return

    llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)
    manager = create_memory_store_manager(
        llm,
        schemas=[EpisodicNote],
        namespace=("episodes",),
        store=store,
    )

    console.print("\n[dim]Extracting episodic memories...[/dim]")
    await manager.ainvoke({"messages": messages})

    episodes = list(store.search(("episodes",)))
    if episodes:
        console.print(f"[dim]Stored {len(episodes)} episode(s):[/dim]")
        for item in episodes:
            v = item.value
            console.print(f"  · [italic]{v.get('situation', v)}[/italic]")
    console.print()
