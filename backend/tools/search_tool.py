from langchain.tools import tool
from duckduckgo_search import DDGS


@tool
def search_places(query: str):

    """
    Search travel places from internet
    using DuckDuckGo.
    """

    results = []

    with DDGS() as ddgs:

        search_results = ddgs.text(
            query,
            max_results=5
        )

        for item in search_results:

            results.append(
                item["title"]
            )

    return results