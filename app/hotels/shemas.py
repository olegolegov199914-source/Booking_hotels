from typing import Optional, List

from pydantic import BaseModel

class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

class SHotelWithFreeRooms(SHotel):
    rooms_left: int
