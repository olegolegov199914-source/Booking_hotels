from fastapi import Request
from passlib.context import CryptContext
from  pydantic import EmailStr
from datetime import datetime, timedelta, timezone
import jwt
from app.exceptions import IncorrectTokenFormatException, TokenAbsentException, TokenExpiredException, UserisNotPresentException
from app.users.dao import UserDAO
from app.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})    
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not (user and verify_password(password, user.hashed_password)):
        return None
    return user

async def get_current_user(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException()
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise IncorrectTokenFormatException()
        
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    
    except jwt.InvalidTokenError:
        raise IncorrectTokenFormatException()
    
    except jwt.PyJWTError:
        raise IncorrectTokenFormatException()
    
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserisNotPresentException()
    
    user = await UserDAO.find_by_id(int(user_id))

    return user
    