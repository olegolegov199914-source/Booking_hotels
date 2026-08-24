from contextlib import asynccontextmanager
from datetime import date
import time
from typing import Optional

from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import BaseModel
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from fastapi_versioning import VersionedFastAPI

from app.admin.auth import authentication_backend
from app.admin.view import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as rooms_router
from app.hotels.router import router
from app.images.router import router as router_images
from app.importer.router import router as import_router
from app.pages.router import router as router_pages
from app.users.models import Users
from app.users.router import router as router_users
from app.logger import logger

app = FastAPI()

app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router)
app.include_router(rooms_router)
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(import_router)

# origins = [
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET","POST","OPTIONS", "DELETE", "PUT", "PUTCH"],
#     allow_headers=["Conent-Type", "Set-Cookie","Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization",]
# )

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    await redis.close()

app.router.lifespan_context = lifespan


app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    description='Greet users with a nice message',
    lifespan=lifespan
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


app.mount("/static", StaticFiles(directory="app/static"), "static")
