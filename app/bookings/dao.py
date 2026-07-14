from datetime import date
from sqlalchemy import delete, insert, select, func, and_, or_ 
from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker, engine

class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date 
        ):
        """
        WITH booked_rooms AS (
            SELECT * from bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) from booked_rooms
        LEFT JOIN rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
            """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == 1,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte("booked_rooms")

            """
            SELECT rooms.quantity - COUNT(booked_rooms.room_id) from rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1
            GROUP BY rooms.quantity, booked_rooms.room_id
            """

            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(Rooms.id == room_id).group_by(
                    Rooms.quantity, booked_rooms.c.room_id
                )
            
            # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

            rooms_left = await session.execute(get_rooms_left)
            rooms_left : int = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price : int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def get_user_bookings(
        cls,
        user_id: int
    ):
        async with async_session_maker() as session:
            get_bookings = select(
                Bookings,
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services
            ).join(
                Rooms,
                Bookings.room_id == Rooms.id
            ).where(
                Bookings.user_id == user_id
            )

            result = await session.execute(get_bookings)
            bookings_with_rooms = result.all()

            result_list = []
            for booking, image_id, name, description, services in bookings_with_rooms:
                total_days = (booking.date_to - booking.date_from).days
                total_cost = booking.price * total_days
                
                result_list.append({
                    "booking": booking,
                    "image_id": image_id,
                    "name": name,
                    "description": description,
                    "services": services,
                    "total_days": total_days,
                    "total_cost": total_cost
                })
            
            return result_list
        
    @classmethod
    async def delete_booking(
        cls,
        booking_id: int,
        user_id: int
    ):
        async with async_session_maker() as session:
            get_user_bookings = select(Bookings).where(
                and_(
                    Bookings.id == booking_id,
                    Bookings.user_id == user_id
                )
            )
            result = await session.execute(get_user_bookings)
            booking = result.scalar_one_or_none()

            if not booking:
                print(f"❌ Бронирование {booking_id} не найдено или не принадлежит пользователю {user_id}")
                return None
            print(f"✅ Бронирование найдено: {booking.id}, user_id={booking.user_id}")
            
            get_delete = delete(Bookings).where(
                and_(
                    Bookings.id == booking_id,
                    Bookings.user_id == user_id
                )
            )
            await session.execute(get_delete)
            await session.commit()
            
            print(f"✅ Бронирование {booking_id} удалено из БД!")
            return booking