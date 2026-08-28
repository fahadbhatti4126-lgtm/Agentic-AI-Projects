import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from tools import get_telecom_help, create_support_ticket


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


tools = [
    get_telecom_help,
    create_support_ticket
]


llm_with_tools = llm.bind_tools(tools)


def ask_agent(user_message):

    prompt = f"""
You are a Telecom Customer Support Agent.

Analyze the user's request and decide whether one of
the available tools should be used.

Available tools:
- get_telecom_help: Use for telecom troubleshooting questions.
- create_support_ticket: Use when the user wants to report
  a problem or create a support ticket.

Do not invent information.

User Request:
{user_message}
"""

    response = llm_with_tools.invoke(prompt)

    if response.tool_calls:

        tool_call = response.tool_calls[0]

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        if tool_name == "get_telecom_help":

            result = get_telecom_help.invoke(tool_args)

        elif tool_name == "create_support_ticket":

            result = create_support_ticket.invoke(tool_args)

        else:

            return "Unknown tool selected."

        return result

    return response.content