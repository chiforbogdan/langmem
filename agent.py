from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from memory.procedural import load_system_prompt
from tools.memory_tools import memory_tools

_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


async def run_agent(messages: list) -> str:
    agent = create_react_agent(_llm, tools=memory_tools, prompt=load_system_prompt())
    result = await agent.ainvoke({"messages": messages})
    return result["messages"][-1].content
