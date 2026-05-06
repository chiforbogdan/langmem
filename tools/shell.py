from langchain.tools import tool
import subprocess

@tool
def execute_bash_tool(payload: str) -> str:
    """Use this tool when you want to run a bash/shell script. It can be any can of bash script of running arbitrary executables. Just give the payload commands as string parameters."""

    print(f"Running bash script {payload}")
    return subprocess.run(payload, shell=True)
