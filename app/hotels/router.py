from datetime import date
from app.exceptions import DateExeption, HotelIDExeption
from fastapi import APIRouter
from app.hotels.shemas import SHotel, SHotelWithFreeRooms
from app.hotels.dao import HotelDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)

@router.get("/{location}", response_model=list[SHotelWithFreeRooms])
async def get_hotels(
    location: str,
    date_from: date,
    date_to: date
):
    if date_from >= date_to:
        raise DateExeption
    
    hotels_with_free_rooms = await HotelDAO.find_hotels_with_free_rooms(
        location=location,
        date_from=date_from,
        date_to=date_to,
    )

    if not hotels_with_free_rooms:
        return []

    result = []
    for hotel, rooms_left in hotels_with_free_rooms:
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
