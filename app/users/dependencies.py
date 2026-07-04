from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError
from app.config import settings
from datetime import datetime, timezone
from app.exceptions import IncorrectTokenFormatException, TokenAbsentException, TokenExpiredException, UserisNotPresentException
from app.users.dao import UserDAO
from app.users.models import Users
def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
        token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException
    user_id : str = payload.get("sub")
    if not user_id:
        raise UserisNotPresentException
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserisNotPresentException

    return user
