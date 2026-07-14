from datetime import date
from sqlalchemy import select
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.database import async_session_maker
class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_rooms_by_hotels(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date
    ):
        async with async_session_maker() as session:
            query_rooms = select(Rooms).where(Rooms.hotel_id == hotel_id)
            get_rooms = await session.execute(query_rooms)
            rooms = get_rooms.scalars().all()

            if not rooms:
                return None
            
            room_ids = [room.id for room in rooms]

            query_bookings = select(Bookings).where(
                Bookings.room_id.in_(room_ids),
                Bookings.date_from < date_to,
                Bookings.date_to > date_from
            )
            get_bookings = await session.execute(query_bookings)
            bookings = get_bookings.scalars().all()

            booked_count = {}
            for booking in bookings:
                booked_count[booking.room_id] = booked_count.get(booking.room_id, 0) + 1

            days = (date_to - date_from).days

            result = []
            for room in rooms:
                booked = booked_count.get(room.id, 0)

                rooms_left = room.quantity - booked

                total_cost = room.price * days

                result.append({
                    "room": room,
                    "rooms_left": rooms_left,
                    "total_cost": total_cost
                })
            
            return result
