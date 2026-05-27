import os

from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    max_new_tokens=140,
    temperature=0.95,
)

model = ChatHuggingFace(llm=llm)

# ── Option chips sent to frontend for each preference question ──────────────
ACCOMMODATION_OPTIONS = [
    "🏕️ Hostel / Dorm",
    "🏨 Budget Hotel",
    "🏩 Mid-range Hotel",
    "🏰 Luxury Resort",
]

TRANSPORT_OPTIONS = [
    "🛵 Rent a Scooter",
    "🚕 Taxi / Cab",
    "🛺 Tuk-tuk / Auto",
    "🚌 Public Transport",
    "🔀 Mix of everything",
]

FOOD_OPTIONS = [
    "🍜 Street Food",
    "🍽️ Local Restaurants",
    "🌟 Fine Dining",
    "🥗 Vegetarian",
    "🍱 Mix of everything",
]


def conversation_agent(state):

    raw = state["messages"][-10:]
    history = "\n".join(raw)

    destination       = state.get("destination")
    departure_city    = state.get("departure_city")
    days              = state.get("days")
    people            = state.get("people")
    budget            = state.get("budget")
    accommodation     = state.get("accommodation_type")
    transport         = state.get("transport_preference")
    food              = state.get("food_preference")

    # Build known info summary
    known = []
    if destination:    known.append(f"Destination: {destination}")
    if departure_city: known.append(f"Flying from: {departure_city}")
    if days:           known.append(f"Days: {days}")
    if people:         known.append(f"People: {people}")
    if budget:         known.append(f"Budget: ₹{budget}")
    if accommodation:  known.append(f"Accommodation: {accommodation}")
    if transport:      known.append(f"Transport: {transport}")
    if food:           known.append(f"Food preference: {food}")
    known_str = "\n".join(known) if known else "Nothing confirmed yet."

    # ── Decide what to ask next, in order ───────────────────────────────────
    pending_options = []

    if not destination:
        guidance = "Ask where they want to travel to. Be excited about it."

    elif not departure_city:
        guidance = "Ask which city they will be flying or travelling FROM. Keep it casual."

    elif not days:
        guidance = "Ask how many days they have for the trip."

    elif not budget:
        guidance = (
            "Ask for their approximate budget for the whole trip in INR. "
            "You can give a range example to help them estimate."
        )

    elif not accommodation:
        guidance = (
            "Ask what type of accommodation they prefer. "
            "Mention options like hostel, budget hotel, mid-range, or luxury resort. "
            "Keep it short — the user will see clickable options."
        )
        pending_options = ACCOMMODATION_OPTIONS   # ← chips appear in frontend

    elif not transport:
        guidance = (
            "Ask how they prefer to get around at the destination. "
            "Mention options like renting a scooter, taking taxis, tuk-tuks, or public transport. "
            "Keep it short — the user will see clickable options."
        )
        pending_options = TRANSPORT_OPTIONS

    elif not food:
        guidance = (
            "Ask about their food preferences — street food, local restaurants, fine dining, etc. "
            "Keep it short — the user will see clickable options."
        )
        pending_options = FOOD_OPTIONS

    else:
        # All info collected — make a statement, NOT a question (avoids yes/yes/yes loop)
        guidance = (
            "All info is collected. Make ONE enthusiastic statement that you're putting the "
            "itinerary together now. Do NOT ask any question. "
            "Example: 'Perfect, I have everything I need — putting your plan together now! 🗺️'"
        )

    prompt = f"""You are HeyTrip, a friendly AI travel companion — NOT a customer support bot.

Talk like a fun, knowledgeable friend who loves travel.

--- Conversation so far ---
{history}
--- End ---

What we know:
{known_str}

Your task for this reply:
{guidance}

Rules:
- Keep it under 2 sentences
- Sound warm and human
- Never ask more than one question per reply
- Do NOT repeat a question that was already answered

Write only your next reply:"""

    try:
        response = model.invoke(prompt)
        reply = response.content.strip()
    except Exception as e:
        print(f"Conversation agent error: {e}")
        reply = "Sounds great! Tell me a bit more so I can plan the perfect trip."

    return {
        **state,
        "pending_options": pending_options,   # ← sent to frontend
        "messages": [
            *state["messages"],
            f"AI: {reply}",
        ],
    }