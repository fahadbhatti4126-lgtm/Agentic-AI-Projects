import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


def research_agent(problem):
    """Research Agent: identifies important information about the problem."""

    prompt = f"""
You are the Research Agent.

Analyze the user's problem and identify the important facts,
requirements, questions, and information needed to solve it.

Do not provide a final solution yet.

User Problem:
{problem}

Return your research findings clearly.
"""

    response = llm.invoke(prompt)

    return response.content


def analysis_agent(problem, research):
    """Analysis Agent: analyzes the research and develops a solution."""

    prompt = f"""
You are the Analysis Agent.

Your job is to analyze the user's problem using the research
provided by the Research Agent.

Develop a logical solution or recommendation.

User Problem:
{problem}

Research Agent Findings:
{research}

Return your analysis and proposed solution.
"""

    response = llm.invoke(prompt)

    return response.content


def reviewer_agent(problem, research, analysis):
    """Reviewer Agent: reviews the work and produces the final answer."""

    prompt = f"""
You are the Reviewer Agent.

Review the research and analysis carefully.

Check whether the proposed solution actually addresses
the user's original problem.

Then produce a clear, useful final answer.

User Problem:
{problem}

Research:
{research}

Analysis:
{analysis}

Return ONLY the final answer for the user.
"""

    response = llm.invoke(prompt)

    return response.content