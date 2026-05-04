import asyncio

from dotenv import load_dotenv
from rich.console import Console

from agent import run_agent
from background.processor import extract_episodes
from memory.procedural import load_system_prompt, optimize_prompt
from memory.store import store

load_dotenv()

console = Console()
messages = []


def print_banner():
    console.print("\n[bold green]LangMem Chatbot[/bold green]")
    console.print(f"[dim]System prompt:[/dim] {load_system_prompt()[:80]}...")
    facts = list(store.search(("user", "facts")))
    if facts:
        console.print(f"[dim]Loaded {len(facts)} memory fact(s) from previous sessions.[/dim]")
    console.print("[dim]Commands: /memory · exit[/dim]\n")


def print_memory():
    facts = list(store.search(("user", "facts")))
    episodes = list(store.search(("episodes",)))

    console.print("\n[bold]Semantic memory[/bold] — (\"user\", \"facts\")")
    for item in facts or []:
        console.print(f"  · {item.value}")
    if not facts:
        console.print("  [dim]empty[/dim]")

    console.print("\n[bold]Episodic memory[/bold] — (\"episodes\",)")
    for item in episodes or []:
        console.print(f"  · {item.value}")
    if not episodes:
        console.print("  [dim]empty[/dim]")
    console.print()


async def chat():
    print_banner()
    while True:
        user_input = input("> ").strip()
        if not user_input:
            continue
        if user_input.lower() == "/memory":
            print_memory()
            continue
        if user_input.lower() in ("exit", "quit"):
            if messages:
                await extract_episodes(messages)
                console.print("\n[dim]Updating system prompt...[/dim]")
                new_prompt = await optimize_prompt(messages, load_system_prompt())
                console.print(f"[dim]Prompt updated: {new_prompt[:80]}...[/dim]")
            console.print("[dim]Goodbye.[/dim]")
            break
        messages.append({"role": "user", "content": user_input})
        reply = await run_agent(messages)
        messages.append({"role": "assistant", "content": reply})
        console.print(f"\n[bold cyan]Agent:[/bold cyan] {reply}\n")


if __name__ == "__main__":
    asyncio.run(chat())
