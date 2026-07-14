from datetime import date

from fastapi import APIRouter, Request, Depends, status
from app.bookings.dao import BookingDAO
from app.bookings.shemas import SBooking
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exceptions import RoomCannotBeBooked, BookingNotFoundException
router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user))-> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    
@router.get("")
async def get_user_bookings(
    current_user: Users = Depends(get_current_user)
):
    bookings = await BookingDAO.get_user_bookings(user_id=current_user.id)
    return bookings

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user)
):
    deleted_booking = await BookingDAO.delete_booking(
        booking_id=booking_id,
        user_id=current_user.id
    )
    print(f"🔍 Удаляем бронирование {booking_id} для пользователя {current_user.id}")


    if not deleted_booking:
        raise BookingNotFoundException()
    
    return None