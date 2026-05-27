from pydantic import BaseModel
from typing import Optional


class TripInfo(BaseModel):

    destination: Optional[str] = None
    departure_city: Optional[str] = None
    people: Optional[int] = None
    days: Optional[int] = None
    budget: Optional[int] = None
    accommodation_type: Optional[str] = None
    transport_preference: Optional[str] = None
    food_preference: Optional[str] = None