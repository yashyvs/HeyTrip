
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from main import app as travel_graph


api = FastAPI(title="HeyTrip API")

# Allow requests from the Next.js development server.
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TravelRequest(BaseModel):
    query: str = Field(min_length=1, max_length=5000)
    thread_id: str | None = None


@api.get("/")
def home():
    return {"message": "HeyTrip API is running"}


@api.post("/plan")
def plan_trip(request: TravelRequest):
    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Travel query cannot be empty",
        )

    # Generate a separate conversation ID when one isn't supplied.
    thread_id = request.thread_id or str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    initial_state = {
        "messages": [HumanMessage(content=query)],
        "user_query": query,
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "llm_calls": 0,
    }

    try:
        result = travel_graph.invoke(
            initial_state,
            config=config,
        )

        final_message = result["messages"][-1]

        return {
            "thread_id": thread_id,
            "query": query,
            "response": final_message.content,
        }

    except Exception:
        # Keep internal errors and credentials out of API responses.
        raise HTTPException(
            status_code=500,
            detail="Trip planning failed. Check the backend logs.",
        )
