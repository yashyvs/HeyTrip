
import logging
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from main import app as travel_graph
from main import get_message_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = FastAPI(title="HeyTrip API")

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TravelRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=5000,
    )

    thread_id: str | None = None


@api.get("/")
def home():
    return {
        "message": "HeyTrip API is running"
    }


@api.post("/plan")
def plan_trip(request: TravelRequest):
    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Travel query cannot be empty",
        )

    thread_id = request.thread_id or str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    try:
        # IMPORTANT:
        # Send only the new user message.
        # LangGraph restores the previous state using thread_id.
        result = travel_graph.invoke(
            {
                "messages": [
                    HumanMessage(content=query)
                ]
            },
            config=config,
        )

        messages = result.get("messages", [])

        if not messages:
            raise ValueError("No response was generated.")

        assistant_response = get_message_text(
            messages[-1]
        )

        return {
            "thread_id": thread_id,
            "query": query,
            "response": assistant_response,
        }

    except Exception:
        logger.exception("Trip planning request failed.")

        raise HTTPException(
            status_code=500,
            detail=(
                "Trip planning failed. "
                "Please check the backend logs."
            ),
        )


@api.get("/history/{thread_id}")
def get_conversation_history(thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    try:
        snapshot = travel_graph.get_state(config)

        if not snapshot or not snapshot.values:
            return {
                "thread_id": thread_id,
                "messages": [],
            }

        messages = snapshot.values.get(
            "messages",
            [],
        )

        history = []

        for message in messages:
            message_type = getattr(
                message,
                "type",
                "ai",
            )

            if message_type == "human":
                role = "user"
            elif message_type == "ai":
                role = "assistant"
            else:
                continue

            history.append(
                {
                    "role": role,
                    "content": get_message_text(message),
                }
            )

        return {
            "thread_id": thread_id,
            "messages": history,
        }

    except Exception:
        logger.exception("Could not retrieve conversation history.")

        raise HTTPException(
            status_code=500,
            detail="Could not retrieve conversation history.",
        )
