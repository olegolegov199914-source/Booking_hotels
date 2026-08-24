
import pytest

from app.bookings.dao import BookingDAO
from datetime import datetime

async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2026-07-05", "%Y-%m-%d"),
        date_to=datetime.strptime("2026-07-15", "%Y-%m-%d"),)

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None

@pytest.mark.asyncio
async def test_crud_booking():
    new_booking = await BookingDAO.add(
        user_id=1,
        room_id=2,
        date_from=datetime.strptime("2026-07-05", "%Y-%m-%d"),
        date_to=datetime.strptime("2026-07-15", "%Y-%m-%d"),
    )

    if new_booking is None:
        pytest.skip("Нет свободных номеров для бронирования")
    
    booking_id = new_booking.id

    assert booking_id is not None
    assert booking_id > 0
    assert new_booking.user_id == 1
    assert new_booking.room_id == 2
    assert new_booking.date_from == datetime.strptime("2026-07-05", "%Y-%m-%d").date()
    assert new_booking.date_to == datetime.strptime("2026-07-15", "%Y-%m-%d").date()
    
    print(f"Создано бронирование с ID: {booking_id}")

    found_booking = await BookingDAO.find_by_id(booking_id)
    
    assert found_booking is not None
    assert found_booking.id == booking_id
    assert found_booking.user_id == 1
    assert found_booking.room_id == 2
    assert found_booking.date_from == datetime.strptime("2026-07-05", "%Y-%m-%d").date()
    assert found_booking.date_to == datetime.strptime("2026-07-15", "%Y-%m-%d").date()
    
    print(f"Прочитано бронирование ID: {found_booking.id}")

    deleted = await BookingDAO.delete_booking(
        booking_id=booking_id,
        user_id=1
    )
   
    assert deleted is not None
    assert deleted.id == booking_id
    
    print(f"Удалено бронирование ID: {booking_id}")

    not_found = await BookingDAO.find_by_id(booking_id)
    
    assert not_found is None
