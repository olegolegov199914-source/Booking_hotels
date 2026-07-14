from datetime import date
from typing import List
from app.exceptions import HotelIDExeption, DateExeption
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.shemas import SRoom
from app.hotels.router import router

@router.get("/{hotels_id}/rooms", response_model=List[SRoom])
async def get_hotel_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date
):
    hotel = await HotelDAO.find_by_id(hotel_id)
    if not hotel:
        raise HotelIDExeption
    
    if date_from >= date_to:
        raise DateExeption
    
    rooms_data = await RoomDAO.find_rooms_by_hotels(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )

    result = []
    for item in rooms_data:
        room = item["room"]
        result.append(SRoom(
            id=room.id,
            hotel_id=room.hotel_id,
            name=room.name,
            description=room.description,
            services=room.servisces,
            price=room.price,
            quantity=room.quantity,
            image_id=room.image_id,
            total_cost=item["total_cost"],
            rooms_left=item["rooms_left"]
        ))
    
    return result