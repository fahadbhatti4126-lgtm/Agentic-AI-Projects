import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from tools import tools


load_dotenv()


llm = ChatGroq(
   model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are an Intelligent Task Execution Agent.

Your job is to understand the user's goal, break complex goals
into smaller tasks, choose appropriate tools, execute the tasks,
and provide a clear final result.

Use tools whenever they are useful.

For mathematical calculations, use the calculate tool.

When the user asks for a plan or wants a goal broken into steps,
use the create_task_list tool.

Do not invent tool results.
Provide a concise and useful final answer.
"""
)


def run_agent(user_input: str) -> str:
    """Run the agent and return its final response."""

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    )

    return response["messages"][-1].content