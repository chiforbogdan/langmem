from groq import APIConnectionError, InternalServerError
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from memory.procedural import load_system_prompt
from tools.memory_tools import memory_tools
from tools.shell import execute_bash_tool

_transient = retry_if_exception_type((InternalServerError, APIConnectionError))

@retry(retry=_transient, wait=wait_exponential(multiplier=1, min=2, max=30), stop=stop_after_attempt(5))
async def run_agent(messages: list) -> str:
    llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)
    agent = create_react_agent(llm, tools=[*memory_tools, execute_bash_tool], prompt=load_system_prompt())
    result = await agent.ainvoke({"messages": messages})
    return result["messages"][-1].content
