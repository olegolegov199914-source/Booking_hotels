from datetime import date

from sqlalchemy import select, func, and_
from app.database import async_session_maker, engine
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_hotels_with_free_rooms(
        cls,
        location: str,
        date_from: date, 
        date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = select(
                Rooms.hotel_id,
                Rooms.id.label("room_id")
            ).join(
                Bookings,
                and_(
                    Bookings.room_id == Rooms.id,
                    Bookings.date_from < date_to,
                    Bookings.date_to > date_from
                )
            ).cte("booked_rooms")

            get_free_rooms = select(
                Hotels,
                (Hotels.rooms_quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
            ).select_from(Hotels).join(
                Rooms,
                Rooms.hotel_id == Hotels.id
            ).join(
                booked_rooms,
                booked_rooms.c.hotel_id == Hotels.id,
                isouter=True
            ).where(
                Hotels.location.ilike(f"%{location}%")
            ).group_by(
                Hotels.id
            )

            result = await session.execute(get_free_rooms)
            data = result.all()

            hotels_with_free_rooms =[]
            for hotel, rooms_left in data:
                if rooms_left is not None and rooms_left > 0:
                    hotels_with_free_rooms.append((hotel, rooms_left))

            return hotels_with_free_rooms

    @classmethod
    async def get_hotel_by_id(cls, hotel_id: int):
        async with async_session_maker() as session:
            query = select(Hotels).where(Hotels.id == hotel_id)
            result = await session.execute(query)
            hotel = result.scalar_one_or_none()
            return hotel