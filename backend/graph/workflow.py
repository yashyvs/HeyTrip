from langgraph.graph import (
    StateGraph,
    END
)

from graph.state import TripState

from agents.extractor_agent import extractor_agent
from agents.conversation_agent import conversation_agent
from agents.router_agent import router_agent
from agents.itinerary_agent import itinerary_agent


builder = StateGraph(
    TripState
)

builder.add_node(
    "extract",
    extractor_agent
)

builder.add_node(
    "router",
    router_agent
)

builder.add_node(
    "conversation",
    conversation_agent
)

builder.add_node(
    "planner",
    itinerary_agent
)


builder.set_entry_point(
    "extract"
)

builder.add_edge(
    "extract",
    "router"
)


builder.add_conditional_edges(

    "router",

    lambda state:
    state["route"],

    {

        "conversation":
        "conversation",

        "planner":
        "planner"
    }
)


builder.add_edge(
    "conversation",
    END
)

builder.add_edge(
    "planner",
    END
)

graph = builder.compile()