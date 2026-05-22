from pydantic import BaseModel
from typing import Optional


class TripInfo(BaseModel):

    destination: Optional[str] = None
    people: Optional[int] = None
    days: Optional[int] = None
    budget: Optional[int] = None