import json
import re
import os

from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    max_new_tokens=1800,   # ← needs more tokens for a full itinerary
    temperature=0.7,
)

model = ChatHuggingFace(llm=llm)


def itinerary_agent(state):

    destination = state.get("destination", "the destination")
    days = state.get("days", 3)
    people = state.get("people", 1)
    budget = state.get("budget")

    budget_str = f"₹{budget}" if budget else "moderate budget"

    # ← Ask the LLM for structured JSON, not a freeform string
    prompt = f"""Create a detailed {days}-day trip itinerary for {destination}.

Trip details:
- People: {people}
- Days: {days}
- Budget: {budget_str}

Return ONLY valid JSON, no explanation, no markdown. Exact format:

{{
  "destination": "{destination}",
  "total_days": {days},
  "summary": "One exciting sentence about this trip",
  "days": [
    {{
      "day": 1,
      "title": "Short catchy title for this day",
      "places": ["Real place name 1", "Real place name 2", "Real place name 3"],
      "tip": "One practical tip for the day"
    }}
  ]
}}

Generate all {days} days. Use real, specific place names in {destination}. Make it exciting."""

    itinerary_data = None

    try:
        response = model.invoke(prompt)
        raw = response.content

        # Extract the JSON block from the response
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            itinerary_data = json.loads(match.group())

    except Exception as e:
        print(f"Itinerary generation error: {e}")

    # ← Fallback so the app never crashes if JSON parsing fails
    if not itinerary_data:
        itinerary_data = {
            "destination": destination,
            "total_days": days,
            "summary": f"An incredible {days}-day journey through {destination}!",
            "days": [
                {
                    "day": i + 1,
                    "title": f"Day {i + 1} – Explore {destination}",
                    "places": ["Local market", "Historic area", "Popular restaurant"],
                    "tip": "Start early to beat the crowds."
                }
                for i in range(days)
            ]
        }

    summary_msg = (
        f"AI: ✈️ Here's your {days}-day {destination} plan! "
        f"Let me know if you want to tweak anything."
    )

    return {
        **state,
        "itinerary_done": True,
        "itinerary": itinerary_data,   # ← structured dict, not a string
        "messages": [
            *state["messages"],
            summary_msg,
        ],
    }