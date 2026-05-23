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


def conversation_agent(state):

    raw = state["messages"][-10:]
    history = "\n".join(raw)

    destination = state.get("destination")
    days = state.get("days")
    people = state.get("people")
    budget = state.get("budget")

    known = []
    if destination: known.append(f"Destination: {destination}")
    if days:        known.append(f"Days: {days}")
    if people:      known.append(f"People: {people}")
    if budget:      known.append(f"Budget: ₹{budget}")
    known_str = "\n".join(known) if known else "Nothing confirmed yet."

    # Check what's missing — only destination and days are required to plan
    missing = []
    if not destination: missing.append("destination (where they want to go)")
    if not days:        missing.append("number of days for the trip")
    if not budget:      missing.append("approximate budget")

    if missing:
        next_to_ask = missing[0]
        guidance = (
            f"You still need: {next_to_ask}. "
            f"Ask for it naturally — like a friend, not a form."
        )
    else:
        # ← KEY FIX: tell the LLM to make a statement, NOT ask a question
        # A question causes the user to say "yes" which loops back here
        guidance = (
            "You have everything you need to plan the trip! "
            "Make an enthusiastic statement like 'Let me put together your itinerary!' "
            "or 'I have everything I need, putting your plan together now!' "
            "Do NOT ask a question. Do NOT say 'shall we' or 'ready to'. "
            "Just confirm you're making the plan."
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

Write only your next reply:"""

    try:
        response = model.invoke(prompt)
        reply = response.content.strip()
    except Exception as e:
        print(f"Conversation agent error: {e}")
        reply = "That sounds amazing! Tell me more about what you have in mind."

    return {
        **state,
        "messages": [
            *state["messages"],
            f"AI: {reply}",
        ],
    }