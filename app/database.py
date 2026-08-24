from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings, DATABASE_URL, TEST_DATABASE_URL

if settings.MODE == "TEST":
    DATA_BASE_URL = TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATA_BASE_URL = DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATA_BASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session():
    async with async_session_maker() as session:
        yield session

class Base(DeclarativeBase):
    pass