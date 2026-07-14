from pydantic import BaseModel
from datetime import date
from typing import List

class SBooking(BaseModel):

    id : int
    room_id : int
    user_id : int
    date_from : date
    date_to : date
    price : int
    total_cost : int
    total_days : int

class ShemaBookings(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: float
    total_cost: float
    total_days: int
    image_id: int
    name: str
    description: str
    services: List[str]