from pathlib import Path

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
