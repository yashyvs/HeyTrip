from typing import TypedDict, List, Dict, Any


class TripState(TypedDict, total=False):

    destination: str
    sub_destinations: List[str]
    departure_city: str
    people: int
    days: int
    budget: int
    accommodation_type: str
    transport_preference: str
    food_preference: str
    itinerary_done: bool
    itinerary: Dict[str, Any]
    route: str
    messages: List[str]
    pending_options: List[str]