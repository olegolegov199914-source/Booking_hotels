from fastapi import HTTPException, status


class BookingException(HTTPException):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"

class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен истек"

class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"

class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"

class UserisNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED

class RoomCannotBeBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Не осталось свободных номеров"

class DateExeption(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Дата заезда должна быть раньше даты выезда"

class HotelIDExeption(BookingException):
    status_code=status.HTTP_404_NOT_FOUND
    detail = "Отель с таким id не найден"

class UserisNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Пользователь не найден"

class BookingNotFoundException(BookingException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="Это бронирование не принадлежит вам"

class LotOfDays(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Период бронирования не может быть более 30 дней"