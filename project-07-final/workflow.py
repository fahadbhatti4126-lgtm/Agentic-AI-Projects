from typing import TypedDict, Optional, Any

from langgraph.graph import StateGraph, END

from agents.planner_agent import analyze_trip
from agents.research_agent import research_trip
from agents.budget_agent import analyze_budget
from agents.itinerary_agent import create_itinerary
from agents.validator_agent import validate_itinerary


# =========================================================
# WORKFLOW STATE
# =========================================================

class TripState(TypedDict, total=False):

    user_request: str

    trip: Any

    research: Any
    weather: Any
    places: Any
    location: Any

    budget: dict

    itinerary: str
    final_itinerary: str

    error: Optional[str]


# =========================================================
# PLANNER NODE
# =========================================================

def planner_node(state: TripState):

    trip = analyze_trip(
        state["user_request"]
    )

    return {
        "trip": trip
    }


# =========================================================
# RESEARCH NODE
# =========================================================

def research_node(state: TripState):

    research = research_trip(
        state["trip"]
    )

    return {
        "research": research,
        "weather": research.weather,
        "places": research.places,
        "location": research.location,
    }


# =========================================================
# BUDGET NODE
# =========================================================

def budget_node(state: TripState):

    budget = analyze_budget(
        state["trip"]
    )

    return {
        "budget": budget
    }


# =========================================================
# ITINERARY NODE
# =========================================================

def itinerary_node(state: TripState):

    itinerary = create_itinerary(
        state["trip"],
        state["research"]
    )

    return {
        "itinerary": itinerary
    }


# =========================================================
# VALIDATOR NODE
# =========================================================

def validator_node(state: TripState):

    itinerary = state.get(
        "itinerary",
        ""
    )

    if not itinerary:
        return {
            "final_itinerary": ""
        }

    final_itinerary = validate_itinerary(
        state["trip"],
        state["research"],
        itinerary
    )

    # If validator fails, NEVER lose the original itinerary
    if not final_itinerary or len(
        str(final_itinerary).strip()
    ) < 100:

        final_itinerary = itinerary

    return {
        "final_itinerary": final_itinerary
    }

# =========================================================
# BUILD WORKFLOW
# =========================================================

def build_workflow():

    workflow = StateGraph(
        TripState
    )

    # -----------------------------------------------------
    # Add nodes
    # -----------------------------------------------------

    workflow.add_node(
        "planner",
        planner_node
    )

    workflow.add_node(
        "research",
        research_node
    )

    workflow.add_node(
        "budget",
        budget_node
    )

    workflow.add_node(
        "itinerary",
        itinerary_node
    )

    workflow.add_node(
        "validator",
        validator_node
    )

    # -----------------------------------------------------
    # Entry point
    # -----------------------------------------------------

    workflow.set_entry_point(
        "planner"
    )

    # -----------------------------------------------------
    # Workflow flow
    # -----------------------------------------------------

    workflow.add_edge(
        "planner",
        "research"
    )

    workflow.add_edge(
        "research",
        "budget"
    )

    workflow.add_edge(
        "budget",
        "itinerary"
    )

    workflow.add_edge(
        "itinerary",
        "validator"
    )

    workflow.add_edge(
        "validator",
        END
    )

    # -----------------------------------------------------
    # Compile
    # -----------------------------------------------------

    return workflow.compile()