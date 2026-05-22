def router_agent(state):

    if state.get(
        "itinerary_done"
    ):

        return {

            **state,

            "route":"conversation"
        }


    message = (

        state["messages"][-1]
        .lower()
    )

    planning_words=[

        "make a plan",

        "plan trip",

        "create itinerary",

        "plan now",

        "generate plan",

        "according to you"
    ]


    if any(
        word in message
        for word in planning_words
    ):

        return {

            **state,

            "route":"planner"
        }


    return {

        **state,

        "route":"conversation"
    }