from typing import TypedDict, List


class TripState(TypedDict, total=False):

    destination: str

    sub_destinations: List[str]

    people: int

    days: int

    budget: int

    itinerary_done: bool

    route: str

    messages: List[str]