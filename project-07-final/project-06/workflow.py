from typing import TypedDict

from langgraph.graph import StateGraph, END

from agent import ask_agent


class AgentState(TypedDict):
    user_message: str
    response: str


def run_agent(state: AgentState):

    response = ask_agent(state["user_message"])

    return {
        "response": response
    }


# Create LangGraph workflow
graph = StateGraph(AgentState)

# Add agent node
graph.add_node("agent", run_agent)

# Entry point
graph.set_entry_point("agent")

# End
graph.add_edge("agent", END)


# Compile workflow
workflow = graph.compile()


def run_workflow(user_message: str):

    result = workflow.invoke({
        "user_message": user_message,
        "response": ""
    })

    return result["response"]