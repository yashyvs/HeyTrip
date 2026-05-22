def itinerary_agent(state):

    destination = state.get(
        "destination",
        "Trip"
    )

    days = state.get(
        "days",
        3
    )

    sub = state.get(
        "sub_destinations",
        []
    )


    plan = f"""
✈️ {destination} Trip Plan

"""

    for day in range(
        1,
        days + 1
    ):

        if day == 1:

            activity = (
                "Arrival + relax"
            )

        elif day == days:

            activity = (
                "Shopping + return"
            )

        elif sub:

            activity = (
                f"Explore {sub[0]}"
            )

        else:

            activity = (
                "Explore attractions"
            )


        plan += f"""

Day {day}
{activity}

"""


    return {

        **state,

        "itinerary_done":
        True,

        "messages":[

            *state["messages"],

            plan
        ]
    }