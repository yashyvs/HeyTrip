import json
import re
import os

from dotenv import load_dotenv
from pydantic import ValidationError
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from models.trip_info import TripInfo

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    max_new_tokens=200,
    temperature=0.1,
)

model = ChatHuggingFace(llm=llm)


# ── Direct chip → state mapping (no LLM needed for these) ──────────────────
# This is the root fix for wrong options appearing:
# emoji chip text was going through the LLM which couldn't parse it,
# so the field stayed None and the wrong question kept repeating.
CHIP_MAPPINGS = {
    "🏕️ Hostel / Dorm":      {"accommodation_type": "hostel"},
    "🏨 Budget Hotel":        {"accommodation_type": "budget hotel"},
    "🏩 Mid-range Hotel":     {"accommodation_type": "mid-range hotel"},
    "🏰 Luxury Resort":       {"accommodation_type": "luxury resort"},
    "🛵 Rent a Scooter":      {"transport_preference": "scooter"},
    "🚕 Taxi / Cab":          {"transport_preference": "taxi"},
    "🛺 Tuk-tuk / Auto":      {"transport_preference": "tuk-tuk"},
    "🚌 Public Transport":    {"transport_preference": "public transport"},
    "🔀 Mix of everything":   {"transport_preference": "mix"},
    "🍜 Street Food":         {"food_preference": "street food"},
    "🍽️ Local Restaurants":  {"food_preference": "local restaurants"},
    "🌟 Fine Dining":         {"food_preference": "fine dining"},
    "🥗 Vegetarian":          {"food_preference": "vegetarian"},
    "🍱 Mix of everything":   {"food_preference": "mix"},
}


def extractor_agent(state):

    # Strip the "User: " prefix to get the raw message
    raw_message = state["messages"][-1].removeprefix("User: ").strip()

    # ── Fix 1: If message is an exact chip selection, map directly ──────────
    # No LLM call needed — clean, reliable, no emoji parsing issues
    if raw_message in CHIP_MAPPINGS:
        updated = {**state}
        updated.update(CHIP_MAPPINGS[raw_message])
        print(f"CHIP MATCHED: {raw_message} → {CHIP_MAPPINGS[raw_message]}")
        return updated

    # ── Fix 2: Pass last AI question as context ─────────────────────────────
    # Fixes "10" not being understood as days.
    # When AI asked "How many days?" and user says "10",
    # the extractor now knows the context.
    last_ai_msg = ""
    for msg in reversed(state["messages"][:-1]):
        if msg.startswith("AI:"):
            last_ai_msg = msg.removeprefix("AI:").strip()
            break

    prompt = f"""Extract travel information from the user's reply.

What the assistant just asked: {last_ai_msg}
User's reply: {raw_message}

Return ONLY valid JSON. Only include fields clearly mentioned or implied by the reply.

Allowed fields:
- destination        → string (where they want to travel TO)
- departure_city     → string (where they are flying FROM)
- people             → integer
- days               → integer (if assistant asked about days, a number reply means days)
- budget             → integer in INR (convert USD by multiplying by 84)
- accommodation_type → one of: "hostel", "budget hotel", "mid-range hotel", "luxury resort"
- transport_preference → one of: "scooter", "taxi", "tuk-tuk", "public transport", "mix"
- food_preference    → one of: "street food", "local restaurants", "fine dining", "vegetarian", "mix"

Examples:

Context: How many days do you have planned?
Reply: 10
Output: {{"days": 10}}

Context: How many days do you have planned?
Reply: around 7 days
Output: {{"days": 7}}

Context: Where will you be flying from?
Reply: Delhi
Output: {{"departure_city": "Delhi"}}

Context: Where are we traveling today?
Reply: I want to go to Thailand
Output: {{"destination": "Thailand"}}

Context: What is your budget?
Reply: around 60k
Output: {{"budget": 60000}}

Context: What is your budget?
Reply: you can take upto 60k
Output: {{"budget": 60000}}

Context: Where are we traveling today?
Reply: I am flying from Delhi to Thailand
Output: {{"destination": "Thailand", "departure_city": "Delhi"}}
"""

    response = model.invoke(prompt)
    raw = response.content
    print("\nRAW EXTRACTOR:", raw)

    extracted = {}

    try:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
            validated = TripInfo(**data)
            extracted = validated.model_dump(exclude_none=True)
    except (json.JSONDecodeError, ValidationError, Exception) as e:
        print(f"Extractor error: {e}")

    updated = {**state}
    updated.update(extracted)

    print("STATE:", {k: v for k, v in updated.items() if k != "messages"})
    return updated