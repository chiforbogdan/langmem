import asyncio

from dotenv import load_dotenv
from rich.console import Console

from agent import run_agent
from background.processor import extract_episodes

load_dotenv()

console = Console()
messages = []


async def chat():
    console.print("[bold green]LangMem Chatbot[/bold green] — type [bold]exit[/bold] to quit\n")
    while True:
        user_input = input("> ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            await extract_episodes(messages)
            console.print("[dim]Goodbye.[/dim]")
            break
        messages.append({"role": "user", "content": user_input})
        reply = await run_agent(messages)
        messages.append({"role": "assistant", "content": reply})
        console.print(f"\n[bold cyan]Agent:[/bold cyan] {reply}\n")


if __name__ == "__main__":
    asyncio.run(chat())
