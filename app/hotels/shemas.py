from typing import Optional, List
import json
from pydantic import BaseModel, field_validator

class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

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

class SHotelWithFreeRooms(SHotel):
    rooms_left: int
