from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents import (
    research_agent,
    analysis_agent,
    reviewer_agent
)


class AgentState(TypedDict):
    problem: str
    research: str
    analysis: str
    final_answer: str


# Research step
def research_step(state: AgentState):
    research = research_agent(state["problem"])

    return {
        "research": research
    }


# Analysis step
def analysis_step(state: AgentState):
    analysis = analysis_agent(
        state["problem"],
        state["research"]
    )

    return {
        "analysis": analysis
    }


# Review step
def review_step(state: AgentState):
    final_answer = reviewer_agent(
        state["problem"],
        state["research"],
        state["analysis"]
    )

    return {
        "final_answer": final_answer
    }


# Create LangGraph
graph = StateGraph(AgentState)


# Add agents as nodes
graph.add_node("research", research_step)
graph.add_node("analysis", analysis_step)
graph.add_node("review", review_step)


# Define workflow
graph.add_edge(START, "research")
graph.add_edge("research", "analysis")
graph.add_edge("analysis", "review")
graph.add_edge("review", END)


# Compile graph
app = graph.compile()


def solve_problem(problem: str) -> str:
    """Run the complete multi-agent workflow."""

    result = app.invoke(
        {
            "problem": problem,
            "research": "",
            "analysis": "",
            "final_answer": ""
        }
    )

    return result["final_answer"]