import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from tools import prepare_email, prepare_notification


load_dotenv()


# Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


# Make tools available to the LLM
tools = [
    prepare_email,
    prepare_notification
]

llm_with_tools = llm.bind_tools(tools)


def create_communication(request):
    """
    Analyze the user's request and decide which
    communication tool should be used.
    """

    prompt = f"""
You are an Intelligent Communication Assistant.

Analyze the user's request and decide whether an email
or a notification should be prepared.

Use the appropriate tool when necessary.

Important:
- Do not invent recipient information.
- If an email is requested but no recipient is provided,
  use "Not specified" as the recipient.
- Prepare the communication clearly and professionally.
- Do not actually send any email or notification.

User Request:
{request}
"""

    response = llm_with_tools.invoke(prompt)

    # If the model requested a tool
    if response.tool_calls:

        tool_call = response.tool_calls[0]

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        if tool_name == "prepare_email":
            result = prepare_email.invoke(tool_args)

        elif tool_name == "prepare_notification":
            result = prepare_notification.invoke(tool_args)

        else:
            return "Unknown communication tool."

        return result

    # If no tool was selected
    return response.content