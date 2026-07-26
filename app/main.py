from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query, Depends
from fastapi.staticfiles import StaticFiles
from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router
from app.hotels.rooms.router import router as rooms_router
from app.pages.router import router as router_pages
from app.images.router import router as router_images

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.config import settings
from redis import asyncio as aioredis


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router)
app.include_router(rooms_router)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(router_images)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","OPTIONS", "DELETE", "PUT", "PUTCH"],
    allow_headers=["Conent-Type", "Set-Cookie","Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization",]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    await redis.close()

app.router.lifespan_context = lifespan


