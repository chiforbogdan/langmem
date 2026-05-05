from pathlib import Path

from langchain_groq import ChatGroq
from langmem import create_prompt_optimizer

PROMPT_FILE = Path(__file__).parent.parent / "system_prompt.txt"

DEFAULT_PROMPT = (
    "You are a helpful assistant with long-term memory. "
    "Use manage_memory to save facts the user shares and "
    "search_memory to recall them before responding."
)


def load_system_prompt() -> str:
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text().strip()
    return DEFAULT_PROMPT


def save_system_prompt(prompt: str) -> None:
    PROMPT_FILE.write_text(prompt)


async def optimize_prompt(messages: list, current_prompt: str) -> str:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    optimizer = create_prompt_optimizer(llm, kind="metaprompt")
    new_prompt = await optimizer.ainvoke(
        {"trajectories": [(messages, {})], "prompt": current_prompt}
    )
    save_system_prompt(new_prompt)
    return new_prompt
