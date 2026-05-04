from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from memory.procedural import load_system_prompt
from tools.memory_tools import memory_tools

async def run_agent(messages: list) -> str:
    llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)
    agent = create_react_agent(llm, tools=memory_tools, prompt=load_system_prompt())
    result = await agent.ainvoke({"messages": messages})
    return result["messages"][-1].content
