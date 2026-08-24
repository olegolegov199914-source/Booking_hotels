import json

from pydantic import BaseModel, field_validator
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

    @field_validator('services', mode='before')
    @classmethod
    def parse_services(cls, value):
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
                return [parsed] if parsed else []
            except json.JSONDecodeError:
                return []
        return value