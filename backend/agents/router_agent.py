import re

def router_agent(state):

    if state.get("itinerary_done"):
        return {**state, "route": "conversation"}

    message = state["messages"][-1].lower()

    has_destination = bool(state.get("destination"))
    has_days = bool(state.get("days"))

    # ← Explicit planning phrases (expanded + added "plan" as standalone word)
    planning_triggers = [
        "make a plan", "plan trip", "plan a trip", "create itinerary",
        "plan now", "generate plan", "according to you", "let's go",
        "book it", "finalize", "make it", "go ahead", "build the plan",
        "create the plan", "yes please", "plan it", "plan my trip",
        "create my trip", "make my trip", "let's plan",
        "start planning", "begin planning",
    ]

    # ← "plan" as a standalone word (catches just "plan" without matching "explanation" etc.)
    has_plan_word = bool(re.search(r'\bplan\b', message))

    if any(trigger in message for trigger in planning_triggers) and has_destination:
        return {**state, "route": "planner"}

    if has_plan_word and has_destination:
        return {**state, "route": "planner"}

    # ← Auto-trigger: only needs destination + days now (removed has_people requirement)
    # Budget is nice to have but shouldn't block planning
    soft_confirms = [
        "ok", "okay", "sure", "yes", "yeah", "yep",
        "great", "perfect", "let's", "sounds good", "awesome",
    ]

    if has_destination and has_days:
        if any(word in message for word in soft_confirms):
            return {**state, "route": "planner"}

    return {**state, "route": "conversation"}