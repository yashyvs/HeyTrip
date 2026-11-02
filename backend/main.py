
import json
import logging
import os
import re
from typing import Annotated, Any, NotRequired, TypedDict

import psycopg
from dotenv import load_dotenv
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from tools.flight_tool import search_flights
from tools.tavily_tool import tavily_search

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from environment variables.")

llm = ChatGroq(model="openai/gpt-oss-120b")


# --------------------------------------------------
# TRIP STATE
# --------------------------------------------------

class TripDetails(TypedDict, total=False):
    destination: str
    origin: str
    travel_dates: str
    duration_days: str
    travellers: str
    budget_per_person: str
    activities: str
    accommodation: str
    dietary_preferences: str
    transport_preference: str
    additional_preferences: str


class TravelState(TypedDict):
    # add_messages preserves messages across graph invocations.
    messages: Annotated[list[AnyMessage], add_messages]

    # Structured trip information.
    trip_details: NotRequired[TripDetails]

    # Conversation control.
    planning_ready: NotRequired[bool]
    awaiting_preferences: NotRequired[bool]
    preferences_asked: NotRequired[bool]
    awaiting_confirmation: NotRequired[bool]
    next_question: NotRequired[str]

    # Search and itinerary results.
    flight_results: NotRequired[str]
    hotel_results: NotRequired[str]
    itinerary: NotRequired[str]


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

REQUIRED_FIELDS = [
    "destination",
    "origin",
    "duration_days",
    "travellers",
    "budget_per_person",
    "activities",
]

FIELD_QUESTIONS = {
    "destination": (
        "Great! Where would you like to travel? "
        "You can choose a destination such as Goa, Manali, Jaipur, "
        "or simply type another place."
    ),
    "origin": (
        "Where will you be travelling from? "
        "For example, Delhi, Mumbai, or Bengaluru."
    ),
    "duration_days": (
        "How many days are you planning for this trip? "
        "For example, 3 days, 5 days, or a week."
    ),
    "travellers": (
        "How many people will be travelling? "
        "Is it a solo trip, couple trip, family trip, or a group?"
    ),
    "budget_per_person": (
        "What's your approximate budget per person? "
        "You can give me a range too."
    ),
    "activities": (
        "What kind of activities do you prefer? "
        "For example, adventure, beaches, sightseeing, nightlife, "
        "food experiences, nature, or cultural activities. "
        "You can choose multiple."
    ),
}

EXTRACTION_PROMPT = """
You are the information extraction component of HeyTrip.

Extract travel requirements from the conversation.

Return ONLY a valid JSON object with these keys:

{
  "destination": null,
  "origin": null,
  "travel_dates": null,
  "duration_days": null,
  "travellers": null,
  "budget_per_person": null,
  "activities": null,
  "accommodation": null,
  "dietary_preferences": null,
  "transport_preference": null,
  "additional_preferences": null
}

Rules:
1. Extract only information explicitly provided by the user.
2. Never invent missing values.
3. If a value is unknown, return null.
4. Use previous conversation messages to understand short answers.
5. New user answers should update earlier values when the user changes them.
6. Preserve useful details such as multiple activities.
7. Keep values as short strings.
8. Do not include markdown or explanations. Return JSON only.
"""


def get_message_text(message: AnyMessage) -> str:
    content = getattr(message, "content", "")

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return " ".join(
            str(item.get("text", ""))
            if isinstance(item, dict)
            else str(item)
            for item in content
        )

    return str(content)


def is_affirmative(text: str) -> bool:
    return bool(
        re.match(
            r"^\s*(yes|yeah|yep|sure|okay|ok|confirm|go ahead|"
            r"generate|generate it|let's do it|proceed)\b",
            text.lower(),
        )
    )


def is_negative(text: str) -> bool:
    return bool(
        re.match(
            r"^\s*(no|nope|not yet|don't generate|do not generate)\b",
            text.lower(),
        )
    )


def is_no_preferences(text: str) -> bool:
    normalized = text.lower().strip()

    phrases = [
        "no preferences",
        "no preference",
        "nothing specific",
        "no specific preference",
        "anything is fine",
        "you decide",
        "not sure",
        "skip",
        "none",
    ]

    return normalized in phrases


def extract_trip_details(
    messages: list[AnyMessage],
    existing_details: TripDetails,
) -> TripDetails:
    """
    Extract information from the conversation and merge it
    with the previously saved trip details.
    """

    conversation = []

    # Keep the latest messages to provide useful context.
    for message in messages[-25:]:
        role = (
            "User"
            if isinstance(message, HumanMessage)
            else "HeyTrip"
        )

        conversation.append(
            f"{role}: {get_message_text(message)}"
        )

    prompt = f"""
{EXTRACTION_PROMPT}

Previously collected trip details:
{json.dumps(existing_details, ensure_ascii=False)}

Conversation:
{chr(10).join(conversation)}
"""

    response = llm.invoke(
        [
            SystemMessage(
                content="You extract structured travel information accurately."
            ),
            HumanMessage(content=prompt),
        ]
    )

    raw_content = get_message_text(response).strip()

    # Handle accidental markdown code fences.
    start = raw_content.find("{")
    end = raw_content.rfind("}")

    if start == -1 or end == -1:
        logger.warning("Could not parse trip details from LLM response.")
        return existing_details

    try:
        extracted = json.loads(raw_content[start:end + 1])
    except json.JSONDecodeError:
        logger.exception("Invalid JSON returned by the extraction model.")
        return existing_details

    merged = dict(existing_details)

    allowed_fields = TripDetails.__annotations__.keys()

    for field in allowed_fields:
        value = extracted.get(field)

        if value is None:
            continue

        if isinstance(value, list):
            value = ", ".join(str(item) for item in value)

        value = str(value).strip()

        if value:
            merged[field] = value

    return merged


def get_missing_fields(details: TripDetails) -> list[str]:
    missing = []

    for field in REQUIRED_FIELDS:
        value = details.get(field)

        if value is None or not str(value).strip():
            missing.append(field)

    return missing


def create_trip_summary(details: TripDetails) -> str:
    labels = {
        "destination": "Destination",
        "origin": "Travelling from",
        "travel_dates": "Travel dates",
        "duration_days": "Duration",
        "travellers": "Travellers",
        "budget_per_person": "Budget per person",
        "activities": "Preferred activities",
        "accommodation": "Accommodation",
        "dietary_preferences": "Dietary preferences",
        "transport_preference": "Transport preference",
        "additional_preferences": "Other preferences",
    }

    lines = []

    for field, label in labels.items():
        value = details.get(field)

        if value:
            lines.append(f"- **{label}:** {value}")

    return "\n".join(lines)


# --------------------------------------------------
# CONVERSATION MANAGER
# --------------------------------------------------

def conversation_manager(state: TravelState):
    messages = state.get("messages", [])
    details = dict(state.get("trip_details", {}))

    if not messages:
        return {
            "planning_ready": False,
            "next_question": FIELD_QUESTIONS["destination"],
        }

    latest_user_message = next(
        (
            message
            for message in reversed(messages)
            if isinstance(message, HumanMessage)
        ),
        None,
    )

    if latest_user_message is None:
        return {
            "planning_ready": False,
            "next_question": FIELD_QUESTIONS["destination"],
        }

    user_text = get_message_text(latest_user_message).strip()

    awaiting_confirmation = state.get(
        "awaiting_confirmation", False
    )

    awaiting_preferences = state.get(
        "awaiting_preferences", False
    )

    preferences_asked = state.get(
        "preferences_asked", False
    )

    # --------------------------------------------------
    # USER CONFIRMS THE TRIP
    # --------------------------------------------------

    if awaiting_confirmation and is_affirmative(user_text):
        logger.info("User confirmed itinerary generation.")

        return {
            "trip_details": details,
            "planning_ready": True,
            "awaiting_confirmation": False,
            "awaiting_preferences": False,
            "next_question": "",
        }

    # If the user does not confirm, allow them to modify details.
    if awaiting_confirmation and is_negative(user_text):
        return {
            "planning_ready": False,
            "awaiting_confirmation": False,
            "next_question": (
                "No problem! What would you like to change "
                "about your trip?"
            ),
        }

    # --------------------------------------------------
    # EXTRACT INFORMATION FROM THE FULL CONVERSATION
    # --------------------------------------------------

    details = extract_trip_details(messages, details)

    # If the user has responded to the optional preferences
    # question, mark that step as completed.
    if awaiting_preferences:
        preferences_asked = True

    # --------------------------------------------------
    # CHECK REQUIRED INFORMATION
    # --------------------------------------------------

    missing_fields = get_missing_fields(details)

    if missing_fields:
        next_field = missing_fields[0]

        return {
            "trip_details": details,
            "planning_ready": False,
            "awaiting_confirmation": False,
            "awaiting_preferences": False,
            "preferences_asked": preferences_asked,
            "next_question": FIELD_QUESTIONS[next_field],
        }

    # --------------------------------------------------
    # ASK OPTIONAL PREFERENCE QUESTIONS
    # --------------------------------------------------

    if not preferences_asked:
        return {
            "trip_details": details,
            "planning_ready": False,
            "awaiting_preferences": True,
            "preferences_asked": False,
            "awaiting_confirmation": False,
            "next_question": (
                "Great! Just a couple more preferences before "
                "I prepare your trip. Do you have any preferred "
                "travel dates, accommodation type, food preferences, "
                "or transport preferences? You can mention anything "
                "specific, or simply say 'No preferences'."
            ),
        }

    # --------------------------------------------------
    # ASK FOR FINAL CONFIRMATION
    # --------------------------------------------------

    summary = create_trip_summary(details)

    return {
        "trip_details": details,
        "planning_ready": False,
        "awaiting_preferences": False,
        "preferences_asked": True,
        "awaiting_confirmation": True,
        "next_question": (
            "Perfect! Here's what I've understood about your trip:\n\n"
            f"{summary}\n\n"
            "Would you like me to search for travel options and "
            "generate your complete itinerary? "
            "You can also tell me if you want to change anything."
        ),
    }


# --------------------------------------------------
# ASK NEXT QUESTION
# --------------------------------------------------

def ask_question(state: TravelState):
    question = state.get(
        "next_question",
        "Could you tell me a little more about your trip?",
    )

    return {
        "messages": [
            AIMessage(content=question)
        ]
    }


# --------------------------------------------------
# FLIGHT AGENT
# --------------------------------------------------

def flight_agent(state: TravelState):
    details = state.get("trip_details", {})

    origin = details.get("origin", "")
    destination = details.get("destination", "")
    dates = details.get("travel_dates", "")

    query = (
        f"Flights from {origin} to {destination}. "
        f"Travel dates: {dates}"
    )

    try:
        results = search_flights(query)

        if not results:
            results = "No flight information was returned."

    except Exception:
        logger.exception("Flight search failed.")
        results = "Flight search is currently unavailable."

    return {
        "flight_results": results,
    }


# --------------------------------------------------
# HOTEL AGENT
# --------------------------------------------------

def hotel_agent(state: TravelState):
    details = state.get("trip_details", {})

    destination = details.get("destination", "")
    duration = details.get("duration_days", "")
    budget = details.get("budget_per_person", "")
    accommodation = details.get("accommodation", "")
    preferences = details.get("additional_preferences", "")

    query = (
        f"Best hotels and accommodation in {destination}. "
        f"Trip duration: {duration}. "
        f"Budget per person: {budget}. "
        f"Accommodation preference: {accommodation}. "
        f"Other preferences: {preferences}."
    )

    try:
        results = tavily_search(query)

        if not results:
            results = "No hotel information was returned."

    except Exception:
        logger.exception("Hotel search failed.")
        results = "Hotel search is currently unavailable."

    return {
        "hotel_results": results,
    }


# --------------------------------------------------
# ITINERARY AGENT
# --------------------------------------------------

def itinerary_agent(state: TravelState):
    details = state.get("trip_details", {})

    prompt = f"""
You are HeyTrip, an expert travel planner.

Create a detailed, practical, personalized travel itinerary.

TRIP DETAILS:
{json.dumps(details, indent=2, ensure_ascii=False)}

FLIGHT SEARCH INFORMATION:
{state.get("flight_results", "Unavailable")}

HOTEL SEARCH INFORMATION:
{state.get("hotel_results", "Unavailable")}

INSTRUCTIONS:

1. Create a day-by-day itinerary based on the trip duration.
2. Consider the user's budget, interests, group size and preferences.
3. Suggest activities that match the user's interests.
4. Organize activities geographically where possible.
5. Include approximate time slots for morning, afternoon and evening.
6. Include food and local experiences where relevant.
7. Suggest accommodation based on the user's preferences.
8. Include practical transportation suggestions.
9. Do not invent flight availability, hotel availability or confirmed prices.
10. Clearly distinguish search results from general recommendations.
11. If search information is unavailable, say so honestly.
12. Make the itinerary realistic and avoid overcrowding each day.

Use clear headings and readable formatting.

At the end, include:
- Estimated budget breakdown
- Important travel tips
- Things the user should verify before booking
"""

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are HeyTrip, a helpful and realistic "
                    "AI travel planning assistant."
                )
            ),
            HumanMessage(content=prompt),
        ]
    )

    itinerary = get_message_text(response)

    return {
        "itinerary": itinerary,
        "messages": [
            AIMessage(content=itinerary)
        ],
    }


# --------------------------------------------------
# GRAPH ROUTING
# --------------------------------------------------

def route_after_conversation(state: TravelState):
    if state.get("planning_ready", False):
        return "plan_trip"

    return "ask_question"


# --------------------------------------------------
# BUILD LANGGRAPH
# --------------------------------------------------

workflow = StateGraph(TravelState)

workflow.add_node(
    "conversation_manager",
    conversation_manager,
)

workflow.add_node(
    "ask_question",
    ask_question,
)

workflow.add_node(
    "flight_agent",
    flight_agent,
)

workflow.add_node(
    "hotel_agent",
    hotel_agent,
)

workflow.add_node(
    "itinerary_agent",
    itinerary_agent,
)

workflow.add_edge(
    START,
    "conversation_manager",
)

workflow.add_conditional_edges(
    "conversation_manager",
    route_after_conversation,
    {
        "ask_question": "ask_question",
        "plan_trip": "flight_agent",
    },
)

workflow.add_edge(
    "ask_question",
    END,
)

workflow.add_edge(
    "flight_agent",
    "hotel_agent",
)

workflow.add_edge(
    "hotel_agent",
    "itinerary_agent",
)

workflow.add_edge(
    "itinerary_agent",
    END,
)


# --------------------------------------------------
# POSTGRESQL CHECKPOINTER
# --------------------------------------------------

_conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True,
)

checkpointer = PostgresSaver(_conn)
checkpointer.setup()

app = workflow.compile(
    checkpointer=checkpointer
)


# --------------------------------------------------
# CLI TEST
# --------------------------------------------------

if __name__ == "__main__":
    thread_id = "heytrip_cli_test"

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    print("HeyTrip is ready! Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            break

        result = app.invoke(
            {
                "messages": [
                    HumanMessage(content=user_input)
                ]
            },
            config=config,
        )

        last_message = result["messages"][-1]

        print("\nHeyTrip:")
        print(get_message_text(last_message))
