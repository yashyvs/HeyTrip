from typing import TypedDict, List, Optional, Dict, Any


class TripState(TypedDict, total=False):

    destination: str
    sub_destinations: List[str]
    people: int
    days: int
    budget: int
    itinerary_done: bool
    itinerary: Dict[str, Any]
    route: str
    messages: List[str]