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
    max_new_tokens=2500,
    temperature=0.7,
)

model = ChatHuggingFace(llm=llm)


def itinerary_agent(state):

    destination    = state.get("destination", "the destination")
    departure_city = state.get("departure_city", "your city")
    days           = state.get("days", 3)
    people         = state.get("people", 1)
    budget         = state.get("budget")
    accommodation  = state.get("accommodation_type", "mid-range hotel")
    transport      = state.get("transport_preference", "mix")
    food           = state.get("food_preference", "mix")

    budget_str = f"₹{budget} total for {people} person(s)" if budget else "moderate budget"

    prompt = f"""Create a detailed {days}-day trip itinerary for {destination}.

Trip details:
- Flying from: {departure_city}
- People: {people}
- Days: {days}
- Total budget: {budget_str}
- Accommodation preference: {accommodation}
- Local transport preference: {transport}
- Food preference: {food}

Return ONLY valid JSON. No explanation, no markdown fences. Use this exact structure:

{{
  "destination": "{destination}",
  "departure_city": "{departure_city}",
  "total_days": {days},
  "people": {people},
  "summary": "One exciting sentence about this trip",
  "accommodation": {{
    "type": "{accommodation}",
    "estimated_cost_per_night_inr": "e.g. ₹1500-2500",
    "recommended_areas": ["area1", "area2"]
  }},
  "transport": {{
    "type": "{transport}",
    "local_tips": "Practical tip about getting around in {destination}"
  }},
  "budget_breakdown": {{
    "flights": "estimated round trip cost from {departure_city}",
    "accommodation": "total for {days} nights",
    "food": "total estimate for all days",
    "local_transport": "total estimate",
    "activities": "total estimate",
    "total_estimated": "grand total in INR"
  }},
  "days": [
    {{
      "day": 1,
      "title": "Short catchy title",
      "places": ["Specific place 1", "Specific place 2", "Specific place 3"],
      "food_spots": ["Specific restaurant or dish 1", "Specific dish/place 2"],
      "transport_tip": "How to get around on this specific day",
      "tip": "One practical tip for the day"
    }}
  ]
}}

Generate all {days} days. Use real place names, real restaurants, and real food spots in {destination}.
Match the accommodation and food spots to the preference: {accommodation} and {food}.
If transport is scooter, mention scooter rental. If taxi, mention apps like Grab.
Make the itinerary genuinely useful and exciting."""

    itinerary_data = None

    try:
        response = model.invoke(prompt)
        raw = response.content
        print("\nITINERARY RAW:", raw[:300])

        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            itinerary_data = json.loads(match.group())

    except Exception as e:
        print(f"Itinerary error: {e}")

    # Fallback so app never crashes
    if not itinerary_data:
        itinerary_data = {
            "destination": destination,
            "departure_city": departure_city,
            "total_days": days,
            "people": people,
            "summary": f"An incredible {days}-day journey through {destination}!",
            "accommodation": {
                "type": accommodation,
                "estimated_cost_per_night_inr": "₹2000-4000",
                "recommended_areas": ["City centre", "Tourist district"],
            },
            "transport": {
                "type": transport,
                "local_tips": "Use Grab app for safe and metered rides.",
            },
            "budget_breakdown": {
                "flights": "₹15000-25000 round trip",
                "accommodation": f"₹{2500 * days} approx",
                "food": "₹5000 approx",
                "local_transport": "₹3000 approx",
                "activities": "₹5000 approx",
                "total_estimated": f"₹{budget or 40000}",
            },
            "days": [
                {
                    "day": i + 1,
                    "title": f"Day {i + 1} – Explore {destination}",
                    "places": ["Local landmark", "Popular market", "Scenic viewpoint"],
                    "food_spots": ["Local street food stall", "Popular restaurant nearby"],
                    "transport_tip": "Use a taxi or Grab for convenience.",
                    "tip": "Start early to beat the crowds.",
                }
                for i in range(days)
            ],
        }

    summary_msg = (
        f"AI: ✈️ Here's your {days}-day {destination} plan, "
        f"tailored to your preferences! Let me know if you want to tweak anything."
    )

    return {
        **state,
        "itinerary_done": True,
        "itinerary": itinerary_data,
        "messages": [*state["messages"], summary_msg],
    }