from datetime import date
from fastapi import APIRouter
from app.exceptions import DateExeption
from app.hotels.shemas import SHotel, SHotelWithFreeRooms
from app.hotels.dao import HotelDAO
from fastapi_cache.decorator import cache  # ← ВАЖНО: импорт декоратора
from typing import List
from pydantic import parse_obj_as
import asyncio
router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/{location}")
@cache(expire=30)
async def get_hotels(
    location: str,
    date_from: date,
    date_to: date
) -> List[SHotelWithFreeRooms]:
    if date_from >= date_to:
        raise DateExeption
    
    await asyncio.sleep(2)


    hotels = await HotelDAO.find_hotels_with_free_rooms(
        location=location,
        date_from=date_from,
        date_to=date_to
    )
    
    result = []
    for hotel, rooms_left in hotels:
        result.append(SHotelWithFreeRooms(
            id=hotel.id,
            name=hotel.name,
            location=hotel.location,
            services=hotel.services,
            rooms_quantity=hotel.rooms_quantity,
            image_id=hotel.image_id,
            rooms_left=rooms_left
        ))
    
    return result
    
@router.get("/id/{hotel_id}", response_model=SHotel)
async def get_hotel_by_id(
    hotel_id: int
):
    hotel = await HotelDAO.get_hotel_by_id(hotel_id)

    if not hotel:
        raise HotelIDExeption()
    
    return SHotel(
        id=hotel.id,
        name=hotel.name,
        location=hotel.location,
        services=hotel.services,
        rooms_quantity=hotel.rooms_quantity,
        image_id=hotel.image_id,
    )


