from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agent import ask_agent


class AgentState(TypedDict):
    question: str
    answer: str


def process_question(state: AgentState):
    """Process the user's question using the RAG agent."""

    answer = ask_agent(state["question"])

    return {
        "answer": answer
    }


# Create LangGraph workflow
graph = StateGraph(AgentState)

# Add processing node
graph.add_node("process_question", process_question)

# Connect workflow
graph.add_edge(START, "process_question")
graph.add_edge("process_question", END)

# Compile graph
app = graph.compile()


def run_workflow(question: str) -> str:
    """Run the LangGraph workflow."""

    result = app.invoke(
        {
            "question": question,
            "answer": ""
        }
    )

    return result["answer"]