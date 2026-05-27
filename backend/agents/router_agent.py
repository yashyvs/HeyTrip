import re


def router_agent(state):

    if state.get("itinerary_done"):
        return {**state, "route": "conversation"}

    message = state["messages"][-1].lower()

    has_destination = bool(state.get("destination"))
    has_days = bool(state.get("days"))

    # Explicit planning phrases (these are unambiguous even without negation check)
    planning_triggers = [
        "make a plan", "plan trip", "plan a trip", "create itinerary",
        "plan now", "generate plan", "according to you", "let's go",
        "book it", "finalize", "make it", "go ahead", "build the plan",
        "create the plan", "yes please", "plan it", "plan my trip",
        "create my trip", "make my trip", "let's plan",
        "start planning", "begin planning",
    ]

    if any(trigger in message for trigger in planning_triggers) and has_destination:
        return {**state, "route": "planner"}

    # ── Fix: "plan" standalone word with negation check ─────────────────────
    # Before: \bplan\b matched "no i dont have a plan" → wrong trigger
    # Now: check if "plan" is preceded by negation words within 4 words
    has_plan_word = bool(re.search(r'\bplan\b', message))

    if has_plan_word and has_destination:
        negation_patterns = [
            r"\bno\b.{0,25}\bplan\b",
            r"\bnot\b.{0,25}\bplan\b",
            r"\bdon'?t\b.{0,25}\bplan\b",
            r"\bhaven'?t\b.{0,25}\bplan\b",
            r"\bwithout\b.{0,25}\bplan\b",
            r"\bno\s+plan\b",
            r"\bno\s+specific\b",
        ]
        is_negated = any(re.search(pat, message) for pat in negation_patterns)

        if not is_negated:
            return {**state, "route": "planner"}

    # Auto-trigger: if destination + days collected and user sounds ready
    soft_confirms = [
        "ok", "okay", "sure", "yes", "yeah", "yep",
        "great", "perfect", "let's", "sounds good", "awesome",
    ]

    if has_destination and has_days:
        if any(word in message for word in soft_confirms):
            return {**state, "route": "planner"}

    return {**state, "route": "conversation"}