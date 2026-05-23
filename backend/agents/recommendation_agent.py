from tools.search_tool import search_places


def recommendation_agent(state):

    destination = state.get(
        "destination",
        ""
    )

    history = "\n".join(
        state["messages"]
    )


    recommendations = (
        search_places.invoke(

            f"""
            Best places in
            {destination}

            based on:

            {history}
            """
        )
    )


    return {

        **state,

        "recommendations":
        recommendations

    }