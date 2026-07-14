from pydantic import BaseModel
from typing import List

class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: List[str]
    price: float
    quantity: int
    image_id: int
    total_cost: float  
    rooms_left: int    

